"""Week 6 milestone — a hybrid retriever, and the gate that refuses it."""

from functools import cache

import pytest

import raglab
from dense import DenseRetriever
from filters import chunk_metadata, current_only, published_since
from hybrid import HybridRetriever, ship_check, tune_c
from sections import section_corpus
from spans import answer_recall_at_k

CORPUS = raglab.corpus.load()
DOCS = {d.id: d.title + "\n" + d.text for d in CORPUS}


@cache
def dev():
    return [q for q in raglab.judgments.load(file="queries-extended.yml").split("dev") if q.answer_spans]


@cache
def parts():
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
    lexical = lambda text, depth: search(index, text, depth)  # noqa: E731
    dense = lambda text, depth: retriever.search(text, depth)  # noqa: E731
    inputs = {
        "lexical": {q.id: lexical(q.text, 50) for q in dev()},
        "dense": {q.id: dense(q.text, 50) for q in dev()},
    }
    return chunks, lexical, dense, inputs, chunk_metadata(chunks, CORPUS)


def rankings_of(retriever, k):
    return {q.id: retriever.search(q.text, k) for q in dev()}


# -- the retriever ------------------------------------------------------------


def test_the_config_distinguishes_two_constants():
    """Two hybrids differing only in `c` are different systems."""
    from raglab.runs import config_hash

    _, lexical, dense, _, _ = parts()
    a = HybridRetriever(lexical, dense, c=10).config
    b = HybridRetriever(lexical, dense, c=60).config
    assert config_hash(a) != config_hash(b)
    assert set(a) >= {"c", "weights", "depth", "filter"}


def test_it_retrieves_and_respects_k():
    _, lexical, dense, _, _ = parts()
    h = HybridRetriever(lexical, dense, c=60)
    assert len(h.search("how long may a crawler cache robots.txt", 5)) == 5


def test_the_filter_runs_after_the_fusion():
    """Filtering each input first means each contributes a different set of
    candidates, so the ranks being fused are ranks within different populations
    — and RRF's premise is that a rank means the same thing on both sides."""
    chunks, lexical, dense, _, meta = parts()
    predicate = current_only(meta)
    h = HybridRetriever(lexical, dense, c=60, predicate=predicate, filter_name="current")
    for q in dev()[:5]:
        assert all(predicate(c) for c in h.search(q.text, 5))


def test_a_selective_filter_leaves_it_short():
    chunks, lexical, dense, _, meta = parts()
    h = HybridRetriever(lexical, dense, predicate=published_since(meta, 2015),
                        filter_name="since2015")
    assert max(h.shortfall(q.text, 5) for q in dev()) > 0


# -- tuning -------------------------------------------------------------------


def test_the_sweep_is_the_result():
    """The paper's 60 was chosen on somebody else's collection in 2009."""
    chunks, lexical, dense, inputs, _ = parts()
    best, scores = tune_c(
        lambda c: HybridRetriever(lexical, dense, c=c), inputs, chunks, dev(), 10
    )
    assert set(scores) == {1, 10, 20, 60, 200}
    assert scores[10] > scores[60]
    assert best in (1, 10, 20)


def test_ties_resolve_towards_the_convention():
    """On a flat region the least surprising choice is the one that will not
    need defending twice."""
    chunks, lexical, dense, inputs, _ = parts()
    best, _ = tune_c(
        lambda c: HybridRetriever(lexical, dense, c=c), inputs, chunks, dev(), 3,
        candidates=(10, 20, 60),
    )
    assert best == 60


# -- the gate -----------------------------------------------------------------


def test_it_ships_at_three():
    chunks, lexical, dense, inputs, _ = parts()
    h = HybridRetriever(lexical, dense, c=60)
    result = ship_check(rankings_of(h, 3), inputs, chunks, dev(), 3)
    assert result["ship"] is True
    assert result["fused"] > result["best"]


def test_it_refuses_at_five_and_says_why():
    """**The milestone.**

    "We did not ship hybrid retrieval because BM25 alone scored higher at k=5"
    is a real finding and a good report. The alternative — comparing the fusion
    against the weaker of its own two inputs and reporting an improvement — is
    the most common hybrid-retrieval claim there is, and nobody making it
    lied."""
    chunks, lexical, dense, inputs, _ = parts()
    h = HybridRetriever(lexical, dense, c=60)
    result = ship_check(rankings_of(h, 5), inputs, chunks, dev(), 5)
    assert result["ship"] is False
    assert result["best_input"] == "lexical"
    assert "lexical" in result["reason"] and "k=5" in result["reason"]


def test_and_ships_at_ten_only_with_the_tuned_constant():
    chunks, lexical, dense, inputs, _ = parts()
    good = ship_check(rankings_of(HybridRetriever(lexical, dense, c=10), 10), inputs, chunks, dev(), 10)
    default = ship_check(rankings_of(HybridRetriever(lexical, dense, c=60), 10), inputs, chunks, dev(), 10)
    assert good["ship"] is True
    assert default["ship"] is False


def test_the_gate_reports_the_ceiling_either_way():
    chunks, lexical, dense, inputs, _ = parts()
    result = ship_check(rankings_of(HybridRetriever(lexical, dense), 5), inputs, chunks, dev(), 5)
    assert result["oracle"] >= result["best"]
