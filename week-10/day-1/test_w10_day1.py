"""Day 1 — latency, and the number that is not the mean.

`test_cost_tells_you_nothing_about_quality` is the day.
"""

from functools import cache

import pytest

import raglab
from dense import DenseRetriever
from fuse import rrf
from latency import (
    budget_report,
    constant_work,
    exceeds,
    percentile,
    spread,
    under_provision,
    work,
)
from order import order_by_rank
from postings import Index
from proxies import auc, separation_strength
from refuse import has_answer
from sections import section_corpus
from window import pack

CORPUS = raglab.corpus.load()
DOCS = {d.id: d.title + "\n" + d.text for d in CORPUS}


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

    def context(text, budget=800):
        shortlist = rrf([search(index, text, 60), retriever.search(text, 60)], 20, 10)
        selected, texts = pack(shortlist, chunks, budget)
        return {c: texts[c] for c in order_by_rank(selected)}

    return chunks, index, context


@cache
def costs():
    _, index, _ = built()
    return {q.id: work(index, q.text) for q in dev()}


# -- counting the work --------------------------------------------------------


def test_work_is_postings_touched_not_seconds():
    """A term in two hundred chunks costs two hundred times one in a single
    chunk, and that is true on every machine."""
    _, index, _ = built()
    assert work(index, "428") == 4
    assert work(index, "451") == 6
    assert work(index, "428 428 428") == 4, "a repeated term is one postings list"
    assert work(index, "") == 0


def test_dense_cost_does_not_depend_on_the_query():
    """266 comparisons, every query, forever. Either its best property or its
    worst, depending on the query."""
    chunks, _, _ = built()
    assert constant_work(len(chunks)) == 266
    assert constant_work(len(chunks)) == constant_work(len(chunks))


def test_lexical_work_spans_two_orders_of_magnitude():
    """**4 postings for `428`, 1,075 for a seven-word question: 269-fold.**

    The mean of that distribution is 423 and describes nothing. The cheapest
    query in the set costs 0.9% of the dearest, and both arrive at the same
    endpoint with the same timeout."""
    values = list(costs().values())
    assert min(values) == 4
    assert max(values) == 1075
    assert spread(values) == pytest.approx(268.75, abs=0.01)


# -- the tail -----------------------------------------------------------------


def test_the_percentile_is_an_observed_value():
    """No interpolation. An interpolated p95 is a number no request
    experienced."""
    assert percentile([1, 2, 3, 4], 0.5) == 2.0
    assert percentile([1, 2, 3, 4], 1.0) == 4.0
    assert percentile([5], 0.95) == 5.0
    assert percentile([], 0.95) == 0.0


def test_sizing_on_the_mean_under_provisions_by_half_again():
    """Mean 423, p95 829. Capacity planned on the average request is 96% short
    of the 95th, and the people who hit the 95th are the ones who complain."""
    values = list(costs().values())
    assert percentile(values, 0.50) == 379.0
    assert percentile(values, 0.95) == 829.0
    assert under_provision(values) == pytest.approx(0.961, abs=0.002)


def test_a_p95_on_twenty_samples_is_one_sample():
    """p95 is 829 and p99 is 1,075 — **30% apart, and adjacent in the sorted
    data**. There is exactly one observation between them.

    Week 9 said a mean on nineteen queries cannot resolve five points. A tail
    percentile on twenty is worse: it is a single request, and it moves by a
    third when that request changes."""
    values = list(costs().values())
    assert percentile(values, 0.99) / percentile(values, 0.95) == pytest.approx(1.297, abs=0.01)
    assert percentile(values, 0.99) == max(values)


# -- the budget ---------------------------------------------------------------


def test_the_budget_is_per_stage_because_a_total_hides_which_stage_is_moving():
    report = budget_report(
        {"retrieve": 40.0, "rank": 5.0, "generate": 900.0},
        {"retrieve": 50.0, "rank": 10.0, "generate": 800.0},
    )
    assert report["retrieve"]["within"] is True
    assert report["generate"]["over"] == pytest.approx(100.0)
    assert exceeds(report) == ["generate"]


def test_a_stage_with_no_budget_is_over_budget():
    """An unbudgeted stage is not a free stage. It is a stage nobody has thought
    about, which is how a 200ms reranker arrives without a decision."""
    assert exceeds(budget_report({"rerank": 200.0}, {})) == ["rerank"]


# -- the day ------------------------------------------------------------------


def test_cost_tells_you_nothing_about_quality():
    """**The day.**

    Run week 9's AUC over a new signal: does the cost of a query predict whether
    the answer ended up in its context? **0.417 — strength 0.583**, under the
    0.7 floor. Chance.

    So cost cannot triage. You cannot route the expensive queries to a cheaper
    path on the grounds that they were not going to work anyway, and you cannot
    spend your way to an answer. Latency and quality are two independent
    budgets, and a system that trades one for the other should be made to show
    the exchange rate."""
    _, _, context = built()
    good, bad = [], []
    for q in dev():
        (good if has_answer(q, context(q.text)) else bad).append(float(costs()[q.id]))
    assert auc(good, bad) == pytest.approx(0.417, abs=0.02)
    assert separation_strength(auc(good, bad)) < 0.7


def test_the_family_table_tells_a_story_the_split_refutes():
    """By family: identifier costs 67 and answers 1.00, paraphrase costs 163 and
    answers 0.33, plain costs 617 and answers 0.80. That reads like a trend.

    Split the same twenty queries at the median cost and the cheap half answers
    **0.67** against the dear half's **0.73** — six hundredths apart, on nine and
    eleven queries, with an MDE week 9 measured at 0.10. The families have one to
    five queries each; the trend is a story told by n=1, and week 9 is the reason
    you check."""
    _, _, context = built()
    answered = {q.id: has_answer(q, context(q.text)) for q in dev()}
    median = percentile(list(costs().values()), 0.5)
    cheap = [i for i, c in costs().items() if c < median]
    dear = [i for i, c in costs().items() if c >= median]
    cheap_rate = sum(answered[i] for i in cheap) / len(cheap)
    dear_rate = sum(answered[i] for i in dear) / len(dear)
    assert cheap_rate == pytest.approx(0.667, abs=0.01)
    assert dear_rate == pytest.approx(0.727, abs=0.01)
    assert abs(cheap_rate - dear_rate) < 0.1, "and 0.10 is the MDE, so this is zero"
