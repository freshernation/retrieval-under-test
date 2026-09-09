"""Day 2 — redundancy, and a metric that cannot see it.

`test_the_metric_cannot_see_any_of_this` is the day.
"""

from functools import cache

import pytest

import raglab
from dense import DenseRetriever
from diversity import (
    dedupe,
    distinct_documents,
    mmr,
    redundancy,
    same_document_pairs,
    similarity,
)
from fuse import rrf
from sections import section_corpus
from spans import answer_recall_at_k

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


def mean(fn):
    return sum(fn(q) for q in dev()) / len(dev())


# -- measuring redundancy -----------------------------------------------------


def test_similarity_is_word_overlap():
    assert similarity("a b c", "a b c") == 1.0
    assert similarity("a b", "c d") == 0.0
    assert similarity("a b", "b c") == pytest.approx(1 / 3)
    assert similarity("", "") == 1.0


def test_the_top_five_is_two_documents():
    """Five chunks, **2.4 distinct documents**, and 5.68 of the 10 possible pairs
    sharing a parent. A context window mostly spent saying related things twice."""
    chunks, shortlists = setup()
    assert mean(lambda q: distinct_documents(shortlists[q.id], 5)) == pytest.approx(2.37, abs=0.1)
    assert mean(lambda q: same_document_pairs(shortlists[q.id], 5)) == pytest.approx(5.68, abs=0.2)


def test_baseline_redundancy():
    chunks, shortlists = setup()
    assert mean(lambda q: redundancy(shortlists[q.id], chunks, 5)) == pytest.approx(0.139, abs=0.01)


# -- the two fixes ------------------------------------------------------------


def test_dedupe_is_conservative_and_barely_fires():
    """Near-duplicate *chunks* inside one result list are rare here. The
    redundancy is different sections of the same document saying related things,
    which is a different problem and which `dedupe` correctly leaves alone.

    A tool that does nothing is not broken. It is telling you your problem is
    not the one it solves."""
    chunks, shortlists = setup()
    before = mean(lambda q: redundancy(shortlists[q.id], chunks, 5))
    after = mean(lambda q: redundancy(dedupe(shortlists[q.id], chunks, 0.8), chunks, 5))
    assert after <= before
    assert abs(after - before) < 0.01


def test_mmr_is_the_identity_at_one():
    chunks, shortlists = setup()
    q = dev()[0]
    assert mmr(shortlists[q.id][:20], chunks, 5, lam=1.0) == shortlists[q.id][:5]


def test_mmr_trades_relevance_for_diversity():
    """0.139 redundancy and 2.37 documents at the baseline; 0.091 and 2.90 at
    lam=0.3. The knob does exactly what it says."""
    chunks, shortlists = setup()
    diverse = mean(lambda q: redundancy(mmr(shortlists[q.id][:20], chunks, 5, 0.3), chunks, 5))
    docs = mean(lambda q: distinct_documents(mmr(shortlists[q.id][:20], chunks, 5, 0.3), 5))
    assert diverse == pytest.approx(0.091, abs=0.01)
    assert docs == pytest.approx(2.89, abs=0.1)


def test_a_bad_lambda_is_refused():
    chunks, shortlists = setup()
    with pytest.raises(ValueError):
        mmr(shortlists[dev()[0].id], chunks, 5, lam=-0.1)


# -- and the day --------------------------------------------------------------


def test_the_metric_cannot_see_any_of_this():
    """**The day, and it is about measurement rather than diversity.**

    Answer recall at k=5 is **0.737 for the baseline, for MMR at 0.9, at 0.7, at
    0.5, and for every deduplication threshold**. Identical. It falls to 0.684
    only at lam=0.3, where diversity starts costing relevance.

    So every diversity technique either does nothing measurable or makes things
    worse, and that is not because they are useless — it is because
    `answer_recall_at_k` asks *"is the answer present"* and is **completely
    indifferent** to whether the other four chunks repeat each other.

    A metric that stops at "present" cannot value non-redundancy. To measure
    diversity you need a question whose answer needs more than one chunk — and
    the only such query in this corpus, `r14`, is in the held-out split.

    Which is the honest finding: **on this eval set, diversity is unmeasurable.**
    Not unimportant. Unmeasurable. Those are different, and reporting the first
    as the second is how a useful technique gets abandoned."""
    chunks, shortlists = setup()
    baseline = mean(lambda q: answer_recall_at_k(shortlists[q.id][:5], chunks, q, 5))
    for lam in (0.9, 0.7, 0.5):
        scored = mean(
            lambda q, l=lam: answer_recall_at_k(mmr(shortlists[q.id][:20], chunks, 5, l), chunks, q, 5)
        )
        assert scored == pytest.approx(baseline)
    for threshold in (0.9, 0.8, 0.5):
        scored = mean(
            lambda q, t=threshold: answer_recall_at_k(
                dedupe(shortlists[q.id], chunks, t)[:5], chunks, q, 5
            )
        )
        assert scored == pytest.approx(baseline)
    aggressive = mean(
        lambda q: answer_recall_at_k(mmr(shortlists[q.id][:20], chunks, 5, 0.3), chunks, q, 5)
    )
    assert aggressive < baseline


def test_the_only_query_that_could_measure_it_is_held_out():
    """`r14` needs spans from two different documents. It is the one query whose
    answer a diverse result set would help and a redundant one would not, and it
    is in the `test` split, where you may look at it once.

    Write more like it. That is the actionable finding."""
    everything = raglab.judgments.load(file="queries-extended.yml")
    r14 = everything.by_id("r14")
    assert len(r14.answer_spans) == 2
    assert r14.split == "test"
    assert not any(len(q.answer_spans) > 1 for q in dev())
