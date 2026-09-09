"""Day 3 — the window as a budget.

`test_more_context_is_monotonically_more_wasteful` is the day.
"""

from functools import cache

import pytest

import raglab
from dense import DenseRetriever
from fuse import rrf
from sections import section_corpus
from window import (
    answer_density,
    answered,
    budget_curve,
    pack,
    truncate_to,
    used_words,
    word_count,
)

CORPUS = raglab.corpus.load()
DOCS = {d.id: d.title + "\n" + d.text for d in CORPUS}


@cache
def dev():
    return [q for q in raglab.judgments.load(file="queries-extended.yml").split("dev") if q.answer_spans]


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
    shortlists = {
        q.id: rrf([search(index, q.text, 60), retriever.search(q.text, 60)], 60, 10)
        for q in dev()
    }
    return chunks, shortlists


@cache
def curve(budget: int, truncate: bool):
    chunks, shortlists = setup()
    rows = [budget_curve(shortlists[q.id], chunks, q, [budget], truncate)[budget] for q in dev()]
    return {
        "chunks": sum(r["chunks"] for r in rows) / len(rows),
        "words": sum(r["words"] for r in rows) / len(rows),
        "answered": sum(1 for r in rows if r["answered"]) / len(rows),
        "density": sum(r["density"] for r in rows) / len(rows),
    }


# -- k was never a budget -----------------------------------------------------


def test_five_chunks_is_not_a_number_of_words():
    """`k = 5` is between 500 and 1,500 words here depending on the query — a
    range of three, and nobody chose it."""
    chunks, shortlists = setup()
    sizes = [sum(word_count(chunks[c]) for c in shortlists[q.id][:5]) for q in dev()]
    assert max(sizes) > 2 * min(sizes)


# -- packing ------------------------------------------------------------------


def test_it_fills_the_budget_in_rank_order():
    chunks, shortlists = setup()
    q = dev()[0]
    selected, texts = pack(shortlists[q.id], chunks, 600)
    assert selected == [c for c in shortlists[q.id] if c in selected]
    assert used_words(texts) <= 600


def test_it_stops_rather_than_skipping_ahead():
    """Skipping a chunk that does not fit and taking a smaller one further down
    silently reorders the window by size, so it no longer reflects the ranking
    you spent six weeks building."""
    chunks = {"a": "x " * 100, "b": "y " * 10}
    selected, _ = pack(["a", "b"], chunks, 50)
    assert selected == []


def test_truncation_fills_the_remainder():
    chunks = {"a": " ".join(str(i) for i in range(100))}
    selected, texts = pack(["a"], chunks, 30, truncate=True)
    assert selected == ["a"]
    assert word_count(texts["a"]) == 30


def test_truncate_to_is_exact():
    assert truncate_to("a b c d", 2) == "a b"
    assert truncate_to("a b", 0) == ""


# -- the new numbers ----------------------------------------------------------


def test_answer_density_is_the_number_nothing_earlier_could_produce():
    """At 800 words, **0.237** — three quarters of the context is not carrying
    the answer. Every metric before today stopped at "the answer is present"."""
    assert curve(800, False)["density"] == pytest.approx(0.237, abs=0.02)


def test_density_is_a_loose_upper_bound_not_a_measure():
    """A chunk containing the span counts whole, including the 250 words around
    it. The real useful fraction is much smaller and needs a generator to
    measure — week 8."""
    chunks, shortlists = setup()
    q = dev()[0]
    _, texts = pack(shortlists[q.id], chunks, 800)
    carrying = [t for t in texts.values() if q.spans_in(t)]
    if carrying:
        span_words = sum(len(s.split()) for s in q.answer_spans)
        assert span_words < word_count(carrying[0])


# -- truncation is a real trade -----------------------------------------------


def test_truncation_helps_at_a_tight_budget():
    """At 200 words, packing whole chunks answers **0.263** of queries — most
    chunks are larger than the whole budget, so nothing fits and you send 75
    words. Truncating answers **0.474**.

    Half a chunk beats no chunk, which is not obvious and is worth measuring
    rather than assuming in either direction."""
    assert curve(200, False)["answered"] == pytest.approx(0.263, abs=0.02)
    assert curve(200, True)["answered"] == pytest.approx(0.474, abs=0.02)
    assert curve(200, False)["words"] < 100
    assert curve(200, True)["words"] == pytest.approx(200, abs=1)


def test_and_truncation_can_destroy_an_answer():
    """Week 4's boundary problem, at assembly time. A span at the end of a chunk
    does not survive being cut to fit — and this failure happens *after*
    retrieval succeeded, so every retrieval metric you have says the system
    worked."""
    q = raglab.judgments.load(file="queries-extended.yml").by_id("r05")
    span = q.answer_spans[0]
    text = "padding " * 40 + span
    assert q.spans_in(text) == {span}
    assert q.spans_in(truncate_to(text, 40)) == set()


# -- and the frontier again ---------------------------------------------------


def test_more_context_answers_more_and_stops():
    """0.474 at 400 words, 0.737 at 800, 0.789 at 2000 — and no further. The
    ceiling is retrieval's, and no budget buys past it."""
    assert curve(400, False)["answered"] < curve(800, False)["answered"]
    assert curve(2000, False)["answered"] == pytest.approx(0.789, abs=0.02)


def test_more_context_is_monotonically_more_wasteful():
    """**The day.**

    | budget | answered | density |
    |---|---|---|
    | 200 | 0.263 | 0.263 |
    | 400 | 0.474 | 0.309 |
    | 800 | 0.737 | 0.237 |
    | 2000 | 0.789 | **0.098** |

    Answered rises and flattens. Density **falls throughout** — at 2000 words,
    nine tenths of what you are paying for is not carrying the answer.

    Week 4 said chunking is a cost decision. This is the same frontier at the
    assembly stage, and it is the one the generator actually charges for: going
    from 800 words to 2000 buys **five points** of answered for 2.5× the
    context, and week 8 will show that the extra 1,200 words are not free in a
    second way."""
    densities = [curve(b, False)["density"] for b in (400, 800, 1200, 2000)]
    assert densities == sorted(densities, reverse=True)
    assert curve(2000, False)["density"] < 0.11
    assert curve(2000, False)["answered"] - curve(800, False)["answered"] < 0.07
