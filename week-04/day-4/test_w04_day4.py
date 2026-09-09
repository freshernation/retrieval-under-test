"""Day 4 — the frontier, and what chunking is actually for.

`test_the_thesis` is the week.
"""

from functools import cache

import pytest

import raglab
from budget import Point, cheapest_meeting, context_cost, measure, pareto, savings
from sections import section_corpus
from windows import chunk_corpus

CORPUS = raglab.corpus.load()
DOCS = {d.id: d.title + "\n" + d.text for d in CORPUS}
DEV = raglab.judgments.load().split("dev")


def bm25_rank(query: str, chunks: dict[str, str], k: int) -> list[str]:
    import sys
    from pathlib import Path

    root = Path(__file__).resolve().parents[2]
    for day in ("day-3", "day-2", "day-1"):
        sys.path.insert(0, str(root / "week-03" / day))
    from bm25 import search

    from postings import Index

    return search(_index(tuple(sorted(chunks.items()))), query, k)


@cache
def _index(frozen_chunks: tuple):
    import sys
    from pathlib import Path

    root = Path(__file__).resolve().parents[2]
    for day in ("day-2", "day-1"):
        sys.path.insert(0, str(root / "week-03" / day))
    from postings import Index

    return Index(dict(frozen_chunks), stopwords=None)


@cache
def configs():
    """Lazy — days 1 and 3 may not be written yet, and that should fail these
    tests individually rather than stop the week from collecting."""
    return {
        "whole documents": DOCS,
        "fixed 800": chunk_corpus(DOCS, 800),
        "fixed 400": chunk_corpus(DOCS, 400),
        "fixed 200/25": chunk_corpus(DOCS, 200, 25),
        "sections 100-300": section_corpus(DOCS, 100, 300),
        "sections 60-150": section_corpus(DOCS, 60, 150),
    }


@cache
def frontier_points():
    return [
        measure(chunks, DEV, bm25_rank, name, k)
        for name, chunks in configs().items()
        for k in (1, 3, 5, 10)
    ]


# -- the pieces ---------------------------------------------------------------


def test_context_cost_counts_words_in_the_top_k():
    chunks = {"a": "one two three", "b": "four five"}
    assert context_cost(["a", "b"], chunks, 2) == 5
    assert context_cost(["a", "b"], chunks, 1) == 3
    assert context_cost(["a", "missing"], chunks, 2) == 3


def test_domination_needs_strictly_better_on_one_axis():
    a = Point("a", 5, 1.0, 100)
    b = Point("b", 5, 1.0, 200)
    same = Point("a", 5, 1.0, 100)
    assert a.dominates(b)
    assert not b.dominates(a)
    assert not a.dominates(same)
    assert not a.dominates(a)


def test_a_point_never_dominates_itself():
    """Get this wrong and `pareto` returns an empty frontier, which looks like a
    data problem and is not."""
    p = Point("x", 3, 0.9, 500)
    assert pareto([p]) == [p]


def test_the_frontier_is_cheapest_first():
    front = pareto(frontier_points())
    assert front == sorted(front, key=lambda p: p.tokens)
    assert len(front) < len(frontier_points())


# -- the measurements ---------------------------------------------------------


def test_whole_documents_retrieve_every_answer():
    """Three weeks of work and the unchunked baseline is *perfect* at k=3. Any
    story where chunking improves retrieval has to get past this."""
    p = next(p for p in frontier_points() if p.name == "whole documents" and p.k == 3)
    assert p.recall == 1.0


def test_and_cost_twenty_two_thousand_words_to_do_it():
    p = next(p for p in frontier_points() if p.name == "whole documents" and p.k == 3)
    assert p.tokens == pytest.approx(22943, abs=200)


def test_smaller_is_not_uniformly_cheaper_for_the_same_coverage():
    """`sections 60-150` never reaches full coverage at any k here. Below some
    size an answer is split or so diluted that the chunk carrying it stops
    winning, and more k does not rescue it.

    There is a floor, and it is not where the folklore puts it."""
    small = [p for p in frontier_points() if p.name == "sections 60-150"]
    assert max(p.recall for p in small) < 1.0


def test_k_and_chunk_size_trade_against_each_other():
    """`fixed 200/25` reaches full coverage only at k=10. `sections 100-300`
    reaches it at k=5. Halve the chunk and you need more of them, so the saving
    is smaller than the size suggests — which is why the decision is a frontier
    and not a size."""
    fixed = {p.k: p.recall for p in frontier_points() if p.name == "fixed 200/25"}
    sect = {p.k: p.recall for p in frontier_points() if p.name == "sections 100-300"}
    assert fixed[5] < 1.0 and fixed[10] == 1.0
    assert sect[5] == 1.0


# -- the decision -------------------------------------------------------------


def test_the_choice_needs_a_number_from_outside_the_system():
    """How often is it acceptable for the answer not to be in the context at
    all? A support search box and a system quoting drug interactions have very
    different answers, and nobody can compute it for you."""
    points = frontier_points()
    strict = cheapest_meeting(points, 1.0)
    relaxed = cheapest_meeting(points, 0.75)
    assert relaxed.tokens < strict.tokens
    assert cheapest_meeting(points, 1.01) is None


def test_the_thesis():
    """**The week.**

    Cheapest configuration retrieving every answer: `sections 100-300` at k=5,
    for **984 words** of context.

    Whole documents retrieve every answer too — at k=3, for 22,943 words.

    **Twenty-three times the cost, for identical coverage.** That is the entire
    value of chunking on this corpus, and note what it is not: it is not better
    retrieval. Three days of measurement and chunking never once retrieved an
    answer that whole documents missed.

    You chunk because 22,175 words is a bill you cannot pay — in money, in
    latency, and in week 7 in a generator's attention. Not because it finds
    more. Anyone who tells you their chunk size improved answer quality is
    describing a different measurement from this one, and it is worth asking
    which."""
    points = frontier_points()
    best = cheapest_meeting(points, 1.0)
    whole = next(p for p in points if p.name == "whole documents" and p.k == 3)

    assert best.name == "sections 100-300"
    assert best.k == 5
    assert best.tokens == pytest.approx(984, abs=30)
    assert best.recall == whole.recall == 1.0
    assert savings(whole, best) > 20


def test_the_recommended_size_is_on_nobody_s_frontier():
    """400-word fixed windows — the size the internet recommends — are dominated
    at every k by something on this frontier. Not beaten narrowly: dominated,
    meaning there is a configuration that is at least as accurate and cheaper.

    That number came from a default in an example notebook. This one came from
    your corpus."""
    front = {(p.name, p.k) for p in pareto(frontier_points())}
    assert not any(name == "fixed 400" for name, _ in front)
