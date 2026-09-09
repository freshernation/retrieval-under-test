"""Day 1 — cutting documents up, and discovering the metric cannot see it.

The last three tests are the day. Read them in order.
"""

from functools import cache

import pytest

import raglab
from windows import (
    chunk_corpus,
    chunk_id,
    coverage,
    fixed_windows,
    parent,
    split_words,
    to_documents,
)

CORPUS = raglab.corpus.load()
DOCS = {d.id: d.title + "\n" + d.text for d in CORPUS}


@cache
def chunked(size: int, overlap: int = 0):
    return chunk_corpus(DOCS, size, overlap)


@cache
def document_level(size: int, overlap: int = 0):
    """Rank chunks with week 3's BM25, fold up to documents, score against the
    document-level judgments."""
    import sys
    from pathlib import Path

    root = Path(__file__).resolve().parents[2]
    for day in ("day-3", "day-2", "day-1"):
        sys.path.insert(0, str(root / "week-03" / day))
    from bm25 import search

    from postings import Index
    from raglab.metrics import evaluate

    chunks = chunked(size, overlap)
    index = Index(chunks, stopwords=None)
    qs = raglab.judgments.load().split("dev")
    rankings = {q.id: to_documents(search(index, q.text, 40), 10) for q in qs}
    return evaluate(rankings, qs, ks=(3,))


# -- windows ------------------------------------------------------------------


def test_windows_tile_the_text():
    assert fixed_windows("a b c d e", 2) == ["a b", "c d", "e"]


def test_overlap_repeats_the_join():
    assert fixed_windows("a b c d e", 3, 1) == ["a b c", "c d e"]


def test_the_last_window_is_short_rather_than_padded():
    assert fixed_windows("a b c d e", 4) == ["a b c d", "e"]


def test_empty_text_gives_no_windows():
    """Not one empty window. A chunk of nothing is a chunk your retriever will
    happily score."""
    assert fixed_windows("", 10) == []
    assert fixed_windows("   ", 10) == []


def test_an_overlap_as_large_as_the_size_is_refused():
    """It is an infinite loop, and it is the first thing anybody types."""
    with pytest.raises(ValueError):
        fixed_windows("a b c", 3, 3)
    with pytest.raises(ValueError):
        fixed_windows("a b c", 0)


# -- identity -----------------------------------------------------------------


def test_a_chunk_carries_its_parent():
    assert chunk_id("rfc-7725", 3) == "rfc-7725#3"
    assert parent("rfc-7725#3") == "rfc-7725"


def test_the_parent_split_is_on_the_last_separator():
    """Document ids can contain the separator and yours will one day."""
    assert parent("a#b#12") == "a#b"


def test_every_chunk_is_attributable():
    """Station 1 surviving into station 2. A chunk with no route back cannot be
    cited, attributed, or checked against week 2's supersession graph."""
    chunks = chunked(400)
    assert all(parent(c) in DOCS for c in chunks)


# -- the corpus ---------------------------------------------------------------


def test_ten_documents_become_many_chunks():
    assert len(chunked(800)) == 72
    assert len(chunked(400)) == 137
    assert len(chunked(200)) == 269


def test_nothing_is_lost_without_overlap():
    assert all(v == 1.0 for v in coverage(DOCS, chunked(400)).values())


def test_overlap_costs_index_size_and_says_how_much():
    over = coverage(DOCS, chunked(400, 50))
    assert all(v > 1.0 for v in over.values())
    assert len(chunked(400, 50)) > len(chunked(400))


# -- and now the point --------------------------------------------------------


def test_chunking_barely_moves_the_document_level_metric():
    """Whole documents score ndcg@3 0.805. Cut into 400-word windows — 137 pieces
    where there were 10 — and it is 0.844.

    Four points, on nine queries, from a change that restructured the entire
    index. That is not nothing and it is nowhere near what you expected."""
    assert document_level(400).metrics["ndcg@3"] == pytest.approx(0.844, abs=0.005)
    assert document_level(800).metrics["ndcg@3"] == pytest.approx(0.859, abs=0.005)


def test_and_it_is_not_monotonic_in_size():
    """800 beats 400 beats 200 — except 200 does not lose to 400 on recall, and a
    100-word chunk beats all of them on nDCG.

    There is no trend here. On nine queries you are watching noise, and every
    published chunk-size recommendation you have ever read was produced by
    somebody looking at a table like this one."""
    scores = {s: document_level(s).metrics["ndcg@3"] for s in (200, 400, 800)}
    assert scores[200] < scores[400] < scores[800]
    assert document_level(100).metrics["ndcg@3"] > scores[800]


def test_an_answer_is_destroyed_and_the_metric_rewards_it():
    """**The day, and it is worse than it looks.**

    At 200 words with no overlap, a chunk boundary falls inside the sentence
    that answers query `r15` — `SHOULD NOT use the cached version for more than
    24 hours`. After chunking, **no chunk in the corpus contains it.** The
    answer is present in the corpus and unretrievable at any k.

    Twenty-five words of overlap rescue it.

    Now look at what your evaluation says about that rescue: ndcg@3 falls from
    0.834 to **0.779**. The change that repairs a destroyed answer is scored as
    a regression, and four queries move down to say so.

    And the destroyed answer never appears in the number at all, because `r15`
    is in the **held-out split**. The instrument you are tuning on does not
    contain the query that would have noticed.

    Two independent failures at once: the metric is at the wrong granularity to
    see span destruction, and the split you tune on does not contain the case.
    Neither is fixed by more queries or better statistics. Tomorrow changes the
    ground truth instead."""
    span = "SHOULD NOT use the cached version for more than 24 hours"
    assert not any(span in c for c in chunked(200).values())
    assert any(span in c for c in chunked(200, 25).values())

    assert "r15" not in {q.id for q in raglab.judgments.load().split("dev")}
    assert raglab.judgments.load().by_id("r15").answer_spans == (span,)

    a, b = document_level(200), document_level(200, 25)
    assert a.metrics["ndcg@3"] == pytest.approx(0.834, abs=0.005)
    assert b.metrics["ndcg@3"] == pytest.approx(0.779, abs=0.005)
    assert b.metrics["ndcg@3"] < a.metrics["ndcg@3"]
    assert len(b.worse_than(a, "ndcg@3")) == 4
