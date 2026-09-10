"""Day 4 — refusal.

`test_the_first_refusals_are_free` and `test_and_then_they_are_not` are the day.
"""

from functools import cache

import pytest

import raglab
from dense import DenseRetriever
from fuse import rrf
from ground import answer_all
from order import order_by_rank
from raglab.generator import SimulatedGenerator, is_refusal
from refuse import (
    ANSWERED_RIGHT,
    ANSWERED_WRONG,
    REFUSED_RIGHT,
    REFUSED_WRONG,
    confidence,
    free_threshold,
    frontier,
    has_answer,
    outcome,
    outcomes,
    separation,
)
from sections import section_corpus
from window import pack

CORPUS = raglab.corpus.load()
DOCS = {d.id: d.title + "\n" + d.text for d in CORPUS}
THRESHOLDS = (0.0, 0.45, 0.5, 0.55, 0.6, 0.65, 0.7, 0.8)


@cache
def dev():
    return list(raglab.judgments.load(file="queries-extended.yml").split("dev"))


@cache
def setup():
    import sys
    from pathlib import Path

    root = Path(__file__).resolve().parents[2]
    for day in ("day-3", "day-2", "day-1"):
        sys.path.insert(0, str(root / "week-03" / day))
    from bm25 import search

    from postings import Index

    chunks = section_corpus(DOCS, 100, 300)
    index = Index(chunks, stopwords=None)
    retriever = DenseRetriever(dims=192).fit(chunks)

    def build_context(query):
        shortlist = rrf([search(index, query.text, 60), retriever.search(query.text, 60)], 20, 10)
        selected, texts = pack(shortlist, chunks, 800)
        return {c: texts[c] for c in order_by_rank(selected)}

    contexts = {q.id: build_context(q) for q in dev()}
    return chunks, build_context, contexts


@cache
def points():
    _, _, contexts = setup()
    return frontier(dev(), contexts, THRESHOLDS)


# -- the signal ---------------------------------------------------------------


def test_confidence_needs_nothing_you_would_not_have_in_production():
    """Everything else measured this week needs answer spans, and in production
    there are none. That asymmetry is the whole difficulty of refusal."""
    assert confidence("too many requests", {"c": "sent too many requests"}) == 1.0
    assert confidence("too many requests", {"c": "unrelated"}) == 0.0
    assert confidence("", {"c": "anything"}) == 0.0
    assert confidence("anything", {}) == 0.0


# -- the four-way table -------------------------------------------------------


def test_counting_refusals_tells_you_nothing():
    """Refusing everything and refusing nothing both produce a single number.
    Only splitting by whether the answer was there makes a refusal scorable."""
    _, _, contexts = setup()
    counts = points()[0.0]
    assert set(counts) == {ANSWERED_RIGHT, ANSWERED_WRONG, REFUSED_RIGHT, REFUSED_WRONG}
    assert sum(counts.values()) == 20


def test_the_four_outcomes():
    _, _, contexts = setup()
    query = raglab.judgments.load(file="queries-extended.yml").by_id("r03")
    from raglab.generator import REFUSAL, Answer

    good = SimulatedGenerator().answer(query.text, contexts["r03"])
    assert has_answer(query, contexts["r03"])
    assert outcome(query, contexts["r03"], good) == ANSWERED_RIGHT
    assert outcome(query, contexts["r03"], Answer(REFUSAL, ())) == REFUSED_WRONG

    unanswerable = raglab.judgments.load(file="queries-extended.yml").by_id("r10")
    assert not has_answer(unanswerable, contexts["r10"])
    assert outcome(unanswerable, contexts["r10"], Answer(REFUSAL, ())) == REFUSED_RIGHT


def test_the_undesigned_system_refuses_nothing():
    counts = points()[0.0]
    assert counts[REFUSED_RIGHT] == counts[REFUSED_WRONG] == 0
    assert counts[ANSWERED_RIGHT] == 14
    assert counts[ANSWERED_WRONG] == 6


# -- the frontier -------------------------------------------------------------


def test_the_first_refusals_are_free():
    """**Half the day.**

    At threshold 0.5: fourteen correct answers kept — all of them — four wrong
    answers still given, and **two wrong answers correctly refused**.

    Two of the six confidently-wrong answers removed, at a cost of exactly
    nothing. Refusal is not always a trade, and the free region is the part
    nobody looks for."""
    counts = points()[0.5]
    assert counts[ANSWERED_RIGHT] == 14
    assert counts[REFUSED_WRONG] == 0
    assert counts[REFUSED_RIGHT] == 2
    assert counts[ANSWERED_WRONG] == 4


def test_and_then_they_are_not():
    """**The other half.**

    At 0.6, one more correct refusal costs **two correct answers**. At 0.7, four
    correct refusals cost six. At 0.8 every wrong answer is gone and so are six
    right ones.

    Past the free region every refusal is bought with a correct answer, and the
    exchange rate gets worse. Where you stop is a question about what a wrong
    answer costs relative to an unhelpful one — which is not a technical
    question and is not yours to answer alone."""
    assert points()[0.6][REFUSED_WRONG] == 2
    assert points()[0.7][REFUSED_WRONG] == 6
    assert points()[0.8][ANSWERED_WRONG] == 0
    assert points()[0.8][ANSWERED_RIGHT] == 8

    lost = [points()[t][REFUSED_WRONG] for t in (0.5, 0.6, 0.65, 0.7, 0.8)]
    assert lost == sorted(lost)


def test_free_threshold_takes_the_highest_that_costs_nothing():
    """Among the settings that lose no correct answer, take the one that refuses
    most. Below it you are declining to use information you have."""
    assert free_threshold(points()) == 0.55


# -- and the honest limit -----------------------------------------------------


def test_no_threshold_separates_the_two_populations():
    """**The limit of the whole exercise.**

    Confidence when the answer *was* in the context: mean 0.81, minimum **0.56**.
    When it was not: mean 0.59, maximum **0.78**.

    The distributions overlap. There is no threshold that keeps every correct
    answer and refuses every wrong one, because a query whose answer is present
    can score lower than one whose answer is absent.

    So the frontier is all there is, and a refusal policy presented without this
    fact implies a separation that does not exist."""
    _, _, contexts = setup()
    s = separation(dev(), contexts)
    assert s["min_present"] == pytest.approx(0.56, abs=0.02)
    assert s["max_absent"] == pytest.approx(0.78, abs=0.02)
    assert s["overlaps"] is True


def test_a_better_signal_is_the_only_way_out():
    """The overlap is a property of *this* signal, not of refusal. A signal that
    separated the two populations would give a threshold with no trade at all.

    Building one is week 11's routing problem, and knowing that today's crude
    overlap is the floor rather than the ceiling is what stops the frontier
    reading as a law of nature."""
    _, _, contexts = setup()
    perfect = {
        q.id: 1.0 if has_answer(q, contexts[q.id]) else 0.0 for q in dev()
    }
    assert min(v for v in perfect.values() if v == 1.0) > max(
        v for v in perfect.values() if v == 0.0
    )
