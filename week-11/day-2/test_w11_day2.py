"""Day 2 — routing, and the field production does not have.

`test_the_router_captures_none_of_it` is the day.
"""

from functools import cache

import pytest

import raglab
from dense import DenseRetriever
from fuse import rrf
from order import order_by_rank
from postings import Index
from proxies import auc, separation_strength
from refuse import confidence
from rewrite import variants
from route import (
    BASELINE,
    REWRITE,
    apply_routes,
    capture,
    headroom,
    oracle_best,
    route,
    sweep,
)
from sections import section_corpus
from window import pack

CORPUS = raglab.corpus.load()
DOCS = {d.id: d.title + "\n" + d.text for d in CORPUS}
THRESHOLDS = (0.0, 0.5, 0.55, 0.6, 0.65, 0.7, 0.75, 0.8, 0.9, 1.01)


@cache
def dev():
    return list(raglab.judgments.load(file="queries-extended.yml").split("dev"))


@cache
def built():
    import sys
    from pathlib import Path

    root = Path(__file__).resolve().parents[2]
    for day in ("day-3", "day-2", "day-1"):
        sys.path.insert(0, str(root / "week-03" / day))
    from bm25 import search

    chunks = section_corpus(DOCS, 100, 300)
    index = Index(chunks, stopwords=None)
    retriever = DenseRetriever(dims=192).fit(chunks)

    def shortlist(text, depth=10):
        return rrf([search(index, text, 60), retriever.search(text, 60)], 20, depth)

    return chunks, index, shortlist


def context(shortlist, budget=800):
    chunks, _, _ = built()
    selected, texts = pack(shortlist, chunks, budget)
    return {c: texts[c] for c in order_by_rank(selected)}


def answered(query, ctx):
    return bool(query.answer_spans) and query.is_answered_by(list(ctx.values()))


@cache
def measured():
    chunks, index, shortlist = built()
    base_context = {q.id: context(shortlist(q.text)) for q in dev()}
    rewritten = {
        q.id: variants(index, chunks, q.text, shortlist(q.text, 3))[2] for q in dev()
    }
    outcomes = {
        BASELINE: {q.id: answered(q, base_context[q.id]) for q in dev()},
        REWRITE: {q.id: answered(q, context(shortlist(rewritten[q.id]))) for q in dev()},
    }
    signal = {q.id: confidence(q.text, base_context[q.id]) for q in dev()}
    return outcomes, signal


# -- the ceiling, computed first ----------------------------------------------


def test_the_ceiling_comes_before_the_router():
    """Baseline 0.70, rewrite 0.65, and a perfect router would reach **0.80** —
    ten points of headroom, from two strategies neither of which gets there.

    Week 7 computed the reranking ceiling before building the reranker, for the
    same reason: a router whose ceiling you have not computed is a router you
    cannot evaluate."""
    outcomes, _ = measured()
    oracle = oracle_best(outcomes)
    assert sum(outcomes[BASELINE].values()) / 20 == pytest.approx(0.70)
    assert sum(outcomes[REWRITE].values()) / 20 == pytest.approx(0.65)
    assert sum(oracle.values()) / 20 == pytest.approx(0.80)
    assert headroom(outcomes[BASELINE], oracle) == pytest.approx(0.10)


def test_the_oracle_is_not_achievable_and_that_is_why_it_is_computed():
    """It requires knowing whether a strategy answered the query before choosing
    the strategy. It is a ceiling, not a design."""
    outcomes, _ = measured()
    oracle = oracle_best(outcomes)
    assert oracle["r21"] is True, "the rewrite answers it"
    assert outcomes[BASELINE]["r21"] is False, "and the baseline does not"


# -- the router ---------------------------------------------------------------


def test_routing_is_a_direction_and_a_threshold():
    routes = route({"a": 0.3, "b": 0.9}, 0.5)
    assert routes == {"a": REWRITE, "b": BASELINE}
    assert apply_routes(routes, {BASELINE: {"a": True, "b": True}, REWRITE: {"a": False, "b": False}}) == {
        "a": False,
        "b": True,
    }


def test_capture_is_negative_when_routing_hurts():
    """Legal, and information. A raw comparison against the baseline says the
    same thing more quietly."""
    baseline = {"a": True, "b": False}
    oracle = {"a": True, "b": True}
    assert capture(baseline, {"a": True, "b": True}, oracle) == pytest.approx(1.0)
    assert capture(baseline, {"a": False, "b": False}, oracle) == pytest.approx(-1.0)
    assert capture(baseline, baseline, baseline) == 0.0


def test_the_router_captures_none_of_it():
    """**The day.**

    Ten points of headroom. Week 9's best serving-time signal — retrieval
    confidence, AUC 0.83, available on every request — swept across ten
    thresholds:

    | threshold | answered | capture |
    |---|---|---|
    | 0.50 | 0.700 | 0% |
    | 0.65 | 0.700 | 0% |
    | 0.70 | 0.650 | **-50%** |
    | 0.80 | 0.700 | 0% |
    | 1.01 | 0.650 | -50% |

    **Zero per cent at best**, negative at four of the ten. No threshold beats
    not routing.

    Week 6 found RRF's default constant capturing 0% of the available headroom.
    This is the second time a reasonable-looking default has captured none of a
    real gap, and the reason is the same both times: the quantity being
    thresholded is not the quantity that decides the outcome."""
    outcomes, signal = measured()
    table = sweep(signal, outcomes, THRESHOLDS)
    assert max(row["capture"] for row in table.values()) == 0.0
    assert table[0.7]["capture"] == pytest.approx(-0.5)
    assert table[0.8]["answered"] == pytest.approx(0.70)
    assert min(row["capture"] for row in table.values()) == pytest.approx(-0.5)


def test_a_signal_is_informative_about_the_question_it_was_validated_on():
    """Week 9 validated retrieval confidence against *"was the answer in the
    context"* and got AUC 0.83.

    Asked a different question — *"will a rewrite help this query"* — the same
    signal scores **0.333, strength 0.667**. Under this course's 0.7 floor.

    Nothing was wrong with week 9's measurement. The signal simply does not
    carry that second fact, and nothing about the first result suggested it
    would. A proxy is validated for one decision at a time."""
    outcomes, signal = measured()
    helps = [signal[i] for i in signal if outcomes[REWRITE][i] and not outcomes[BASELINE][i]]
    hurts = [signal[i] for i in signal if outcomes[BASELINE][i] and not outcomes[REWRITE][i]]
    assert sorted(helps) and sorted(hurts)
    assert auc(helps, hurts) == pytest.approx(0.333, abs=0.01)
    assert separation_strength(auc(helps, hurts)) < 0.7


def test_the_router_would_have_to_be_validated_on_five_queries():
    """Two queries the rewrite gains, three it loses. Those five are the only
    ones where the routing decision changes anything, and they are the entire
    evidence base for the router.

    Week 9's minimum detectable effect at n=19 was 0.1003. At n=5 nothing is
    detectable, which means **a router cannot be validated on this eval set at
    all** — not that it does not work, but that the set cannot say."""
    outcomes, _ = measured()
    decisive = [
        i
        for i in outcomes[BASELINE]
        if outcomes[BASELINE][i] != outcomes[REWRITE][i]
    ]
    assert sorted(decisive) == ["r04", "r06", "r07", "r21", "r23"]
    assert len(decisive) == 5


def test_the_only_router_that_works_needs_a_field_production_does_not_have():
    """Route by query **family** — rewrite the `plain` and `vocabulary-gap`
    queries, leave the rest — and it captures **100%** of the headroom. 0.80,
    exactly the oracle.

    Family is a label in the eval set. It is written by the person who wrote the
    judgments, it does not arrive with a request, and no serving-time signal in
    this course predicts it.

    So the routing opportunity is real, it is fully realisable, and it is
    realisable only with information the running system does not possess. That
    is week 9's serving-time gap in its strongest form: not a metric you cannot
    compute, but **a decision you cannot make**."""
    outcomes, _ = measured()
    oracle = oracle_best(outcomes)
    by_family = {
        q.id: outcomes[REWRITE if q.family in ("plain", "vocabulary-gap") else BASELINE][q.id]
        for q in dev()
    }
    assert sum(by_family.values()) / 20 == pytest.approx(0.80)
    assert capture(outcomes[BASELINE], by_family, oracle) == pytest.approx(1.0)
