"""Day 2 — reciprocal rank fusion.

`test_the_paper_default_costs_you_the_whole_headroom` is the day.
"""

from functools import cache

import pytest

import raglab
from dense import DenseRetriever
from fuse import contribution, flattening, ranks, rrf, rrf_scores
from sections import section_corpus
from spans import answer_recall_at_k

CORPUS = raglab.corpus.load()
DOCS = {d.id: d.title + "\n" + d.text for d in CORPUS}


@cache
def dev():
    return [q for q in raglab.judgments.load(file="queries-extended.yml").split("dev") if q.answer_spans]


@cache
def runs():
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
    lexical = {q.id: search(index, q.text, 50) for q in dev()}
    dense = {q.id: retriever.search(q.text, 50) for q in dev()}
    return chunks, lexical, dense


def measure(rank_fn, k):
    chunks, _, _ = runs()
    return sum(answer_recall_at_k(rank_fn(q, k), chunks, q, k) for q in dev()) / len(dev())


@cache
def oracle(k):
    chunks, lexical, dense = runs()
    hits = 0
    for q in dev():
        a = answer_recall_at_k(lexical[q.id][:k], chunks, q, k)
        b = answer_recall_at_k(dense[q.id][:k], chunks, q, k)
        hits += 1.0 if (a or b) else 0.0
    return hits / len(dev())


# -- mechanics ----------------------------------------------------------------


def test_ranks_are_one_based():
    """Zero-based first place would give it the same weight as `c` alone — a
    small bug that shifts every score and is invisible in the output."""
    assert ranks(["a", "b", "c"]) == {"a": 1, "b": 2, "c": 3}


def test_depth_cuts_the_input():
    assert ranks(["a", "b", "c"], depth=2) == {"a": 1, "b": 2}


def test_a_document_in_both_lists_beats_one_in_either():
    assert rrf([["a", "x"], ["a", "y"]])[0] == "a"


def test_absence_contributes_nothing_rather_than_a_penalty():
    """The important difference from yesterday's `combine`, where a missing score
    became 0.0 and actively harmed the document. Evidence you do not have is
    simply evidence you do not have."""
    both = rrf_scores([["a", "b"], ["b", "a"]])
    one = rrf_scores([["a", "b"], ["b"]])
    assert one["a"] < both["a"]
    assert one["a"] > 0


def test_weights_are_checked_and_c_must_be_positive():
    with pytest.raises(ValueError):
        rrf([["a"]], c=0)
    with pytest.raises(ValueError):
        rrf([["a"], ["b"]], weights=[1.0])


def test_ties_break_by_id():
    assert rrf([["a", "b"], ["a", "b"]]) == ["a", "b"]
    assert rrf([["b"], ["a"]]) == ["a", "b"]


def test_it_fuses_more_than_two():
    assert rrf([["a"], ["a"], ["b"]])[0] == "a"


# -- what c does --------------------------------------------------------------


def test_c_controls_how_much_position_matters():
    """Stated as a ratio the knob is legible: at c=1 first place is worth 5.5×
    tenth place; at c=60 it is worth 1.15× — practically nothing."""
    assert flattening(1) == pytest.approx(5.5, abs=0.1)
    assert flattening(60) == pytest.approx(1.15, abs=0.02)
    assert contribution(1, 60) > contribution(10, 60)


def test_large_c_says_being_returned_matters_more_than_where():
    small, large = rrf_scores([["a", "b"]], c=1), rrf_scores([["a", "b"]], c=200)
    assert small["a"] / small["b"] > large["a"] / large["b"]


# -- and what it buys ---------------------------------------------------------


def test_fusion_reaches_the_oracle_at_three():
    """0.737 — every query either retriever gets. All of the headroom, captured
    by four lines that never look at a score."""
    chunks, lexical, dense = runs()
    fused = measure(lambda q, k: rrf([lexical[q.id], dense[q.id]], k, c=60), 3)
    assert fused == pytest.approx(oracle(3))
    assert fused > measure(lambda q, k: lexical[q.id][:k], 3)


def test_but_at_five_it_is_worse_than_lexical_alone():
    """**The rule this week exists to teach.**

    At k=5, lexical alone scores 0.789 and every fusion scores 0.737. Not a tie:
    fusion is strictly worse than one of its own inputs, at every value of c and
    every weighting including one that favours lexical two to one.

    Fusion is not free. Mixing a weaker signal into a stronger one dilutes it,
    and a fused ranking that beats *one* input is not an improvement — it is a
    worse version of the other one.

    **A fusion result must beat both inputs.** Tomorrow makes that a check."""
    chunks, lexical, dense = runs()
    lex = measure(lambda q, k: lexical[q.id][:k], 5)
    assert lex == pytest.approx(0.789, abs=0.005)
    for c in (1, 10, 60, 200):
        assert measure(lambda q, k, c=c: rrf([lexical[q.id], dense[q.id]], k, c), 5) < lex
    for w in ([2.0, 1.0], [1.0, 1.0], [1.0, 2.0]):
        assert measure(lambda q, k, w=w: rrf([lexical[q.id], dense[q.id]], k, 60, w), 5) < lex


def test_the_paper_default_costs_you_the_whole_headroom():
    """At k=10 the oracle is 0.895. RRF with c ≤ 20 reaches it. RRF with **c=60**
    — the value from the original paper and the default in every implementation
    — scores 0.842, exactly matching lexical alone and capturing none of the
    headroom.

    The same shape as week 3's k1=1.2 placing 38th of 45: a constant chosen on
    somebody else's collection, shipped as a default, and never checked.

    Sweep it. It costs a minute."""
    chunks, lexical, dense = runs()
    assert oracle(10) == pytest.approx(0.895, abs=0.005)
    assert measure(lambda q, k: rrf([lexical[q.id], dense[q.id]], k, 10), 10) == pytest.approx(
        oracle(10)
    )
    assert measure(lambda q, k: rrf([lexical[q.id], dense[q.id]], k, 60), 10) == pytest.approx(
        measure(lambda q, k: lexical[q.id][:k], 10)
    )
