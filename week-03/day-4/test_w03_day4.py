"""Day 4 — tuning, and four reasons to distrust a tuned number.

The tuned configuration on this corpus does generalise to the held-out split.
Read `test_it_happens_to_generalise_and_you_could_not_have_known` last.
"""

from functools import cache

import pytest

import raglab
from postings import Index
from tuning import (
    B_GRID,
    K1_GRID,
    at_edge,
    best,
    grid_search,
    looks,
    moved_queries,
    rank_of,
    spread,
)

CORPUS = raglab.corpus.load()
DOCS = {d.id: d.title + "\n" + d.text for d in CORPUS}
DEFAULT = (1.2, 0.75)


@cache
def index() -> Index:
    return Index(DOCS, stopwords=None)


@cache
def results():
    return grid_search(index(), raglab.judgments.load().split("dev"))


# -- the grid -----------------------------------------------------------------


def test_the_grid_is_complete_and_ordered():
    r = results()
    assert len(r) == len(K1_GRID) * len(B_GRID) == 45
    assert [s for s, _, _ in r] == sorted([s for s, _, _ in r], reverse=True)


def test_ties_resolve_to_the_smaller_parameters():
    """A real choice: on a plateau the least extreme values are the most likely
    to survive contact with other data."""
    r = [(0.9, 2.0, 0.5), (0.9, 1.0, 0.5)]
    assert best(sorted(r, key=lambda x: (-x[0], x[1], x[2]))) == (0.9, 1.0, 0.5)


def test_two_numbers_move_the_metric_by_eighteen_points():
    """0.710 to 0.886 across the grid. Tuning is the highest-leverage hour of the
    week, which is exactly why it is the easiest place to fool yourself."""
    low, high = spread(results())
    assert low == pytest.approx(0.7104, abs=0.001)
    assert high == pytest.approx(0.8861, abs=0.001)
    assert high - low > 0.17


def test_k1_zero_is_the_worst_corner():
    """k1=0 makes every term binary — present or absent, repetition worth
    nothing — and it is the bottom of the grid regardless of b."""
    worst = [(s, k1, b) for s, k1, b in results() if s == spread(results())[0]]
    assert all(k1 == 0.0 for _, k1, _ in worst)


# -- four reasons to distrust the answer --------------------------------------


def test_one_the_default_is_not_good_here():
    """`k1=1.2, b=0.75` is the value in most of the literature and most search
    engines. On this corpus it places **38th of 45**.

    That is not a scandal — the defaults were chosen on TREC collections of
    news articles, and this is ten RFCs. It is a demonstration that a convention
    is a convention, and that you cannot know whether yours is any good without
    doing this."""
    assert rank_of(results(), *DEFAULT) == 38


def test_two_the_optimum_is_at_the_edge_of_the_grid():
    """**The most important assertion in week 3.**

    The winner is k1=2.4, the largest value in the grid. A grid search that
    returns a boundary has not found an optimum; it has found the edge of your
    grid."""
    score, k1, b = best(results())
    assert (k1, b) == (2.4, 0.5)
    assert at_edge(k1, b)


def test_and_widening_it_shows_a_plateau_running_to_infinity():
    """k1 = 1.2 → 2.4 → 4 → 8 → 64 gives 0.822, 0.886, 0.889, 0.889, 0.889.

    It stops rising and never falls. A plateau extending to infinity means the
    tuner is asking for k1 = ∞, which is to say **turn term saturation off
    entirely** — score by raw term frequency.

    That is a substantive claim about this corpus, it contradicts thirty years
    of practice, and shipping it because the number said so would be exactly the
    superstition `EVALS.md` warns about. Investigate it: ten documents, long
    ones, few queries. Then decide."""
    from bm25 import search

    from raglab.metrics import evaluate

    qs = raglab.judgments.load().split("dev")
    scores = []
    for k1 in (1.2, 2.4, 4.0, 8.0, 64.0):
        ev = evaluate({q.id: search(index(), q.text, 10, k1, 0.5) for q in qs}, qs, ks=(3,))
        scores.append(round(ev.metrics["ndcg@3"], 4))
    assert scores == sorted(scores)
    assert scores[-1] == scores[-2] == pytest.approx(0.8892, abs=0.001)


def test_three_you_took_forty_five_looks():
    """At 95% confidence, forty-five comparisons should produce roughly two
    spuriously good results from noise alone. The count belongs in the report."""
    assert looks(results()) == 45


def test_four_the_whole_gain_rides_on_three_queries():
    """The same three that BM25 itself fixed on Wednesday. Six of the nine are
    untouched by anything you did this week.

    What you have tuned is r01, r06 and r07."""
    qs = raglab.judgments.load().split("dev")
    moved = moved_queries(index(), qs, best(results())[1:], DEFAULT)
    assert moved == ["r01", "r06", "r07"]


# -- and the uncomfortable ending ---------------------------------------------


def test_it_happens_to_generalise_and_you_could_not_have_known():
    """On the held-out split the tuned configuration scores **0.962** against the
    default's **0.917**. It generalised. You were right.

    Now notice what that is worth. Six test queries. One read. The four warnings
    above are all still true — the optimum is still at a boundary, you still took
    forty-five looks, the gain still rides on three dev queries, and the tuner is
    still asking you to disable saturation.

    **You got away with it, and nothing available to you from the inside
    distinguishes getting away with it from being right.** A held-out number that
    confirms a badly-founded choice is the most dangerous result in applied
    retrieval, because it retires the doubt.

    What to actually do: report the tuned number, report all four warnings next
    to it, and put "grow the eval set" at the top of the milestone — which is
    exactly what this week's milestone asks for, and why it asks now."""
    from bm25 import search

    from raglab.metrics import evaluate

    test = raglab.judgments.load().split("test")
    _, k1, b = best(results())
    tuned = evaluate({q.id: search(index(), q.text, 10, k1, b) for q in test}, test, ks=(3,))
    default = evaluate(
        {q.id: search(index(), q.text, 10, *DEFAULT) for q in test}, test, ks=(3,)
    )
    assert tuned.metrics["ndcg@3"] == pytest.approx(0.962, abs=0.005)
    assert default.metrics["ndcg@3"] == pytest.approx(0.917, abs=0.005)
    assert tuned.n == 6
