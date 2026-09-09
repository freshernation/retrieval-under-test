"""Day 1 — reranking, and why this one loses.

`test_the_best_alpha_is_the_one_that_does_nothing` is the day.
"""

from functools import cache

import pytest

import raglab
from dense import DenseRetriever
from fuse import rrf
from rerank import (
    DEFAULT_WEIGHTS,
    ceiling,
    document_frequencies,
    feature_score,
    features,
    idf,
    prior,
    rerank,
)
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
    df = document_frequencies(chunks)
    return chunks, shortlists, df, len(chunks)


def measure(rank_fn, k):
    chunks, _, _, _ = setup()
    return sum(answer_recall_at_k(rank_fn(q)[:k], chunks, q, k) for q in dev()) / len(dev())


# -- features -----------------------------------------------------------------


def test_coverage_is_weighted_by_rarity():
    """Covering `429` matters. Covering `the` does not."""
    chunks, _, df, n = setup()
    rare = features("429", "the 429 status code", df, n)["coverage"]
    common = features("the", "the 429 status code", df, n)["coverage"]
    assert rare == pytest.approx(1.0)
    assert common == pytest.approx(1.0)
    mixed = features("the 429", "the status code", df, n)["coverage"]
    assert mixed < 0.5


def test_an_unseen_term_gets_the_maximum_weight():
    """Correct — a term nothing contains is maximally discriminating — and worth
    noticing, because a typo in a query then scores like a rare word."""
    chunks, _, df, n = setup()
    assert idf("kubernetes", df, n) > idf("the", df, n)


def test_phrase_is_adjacency():
    chunks, _, df, n = setup()
    assert features("too many", "sent too many requests", df, n)["phrase"] == 1.0
    assert features("too many", "many things, not too few", df, n)["phrase"] == 0.0


def test_earliest_prefers_an_early_mention():
    chunks, _, df, n = setup()
    early = features("cookie", "cookie attributes are defined below " + "x " * 50, df, n)
    late = features("cookie", "x " * 50 + "cookie", df, n)
    assert early["earliest"] > late["earliest"]


def test_an_empty_query_does_not_divide_by_zero():
    chunks, _, df, n = setup()
    assert features("", "some text", df, n) == {"coverage": 0.0, "phrase": 0.0, "earliest": 0.0}


# -- the prior and the blend --------------------------------------------------


def test_the_prior_is_the_retrievers_opinion():
    """A reranker that discards the retriever's ranking starts from nothing."""
    p = prior(["a", "b", "c"])
    assert p["a"] == 1.0
    assert p["a"] > p["b"] > p["c"]


def test_alpha_one_is_the_identity():
    chunks, shortlists, df, n = setup()
    q = dev()[0]
    assert rerank(q.text, shortlists[q.id][:10], chunks, df, n, alpha=1.0) == shortlists[q.id][:10]


def test_a_reranker_with_nothing_to_say_changes_nothing():
    chunks, shortlists, df, n = setup()
    q = dev()[0]
    flat = rerank(q.text, shortlists[q.id][:10], chunks, df, n, alpha=1.0, weights={})
    assert flat == shortlists[q.id][:10]


def test_a_bad_alpha_is_refused():
    chunks, shortlists, df, n = setup()
    with pytest.raises(ValueError):
        rerank("x", shortlists[dev()[0].id][:5], chunks, df, n, alpha=2.0)


# -- the ceiling --------------------------------------------------------------


def test_reranking_cannot_exceed_the_shortlist():
    """Reordering cannot introduce a chunk retrieval did not return. Compute this
    before building a reranker; if it equals your recall at k, stop."""
    chunks, shortlists, _, _ = setup()
    for q in dev():
        assert ceiling(shortlists[q.id], chunks, q, 10) >= answer_recall_at_k(
            shortlists[q.id][:5], chunks, q, 5
        )


def test_and_the_ceiling_here_is_worth_sixteen_points():
    """Answer recall at k=5 is 0.737. Over a depth-10 shortlist it is **0.895**.

    So a perfect reranker would gain sixteen points, and there genuinely is
    something to win. That is the honest case for this week."""
    chunks, shortlists, _, _ = setup()
    at5 = sum(answer_recall_at_k(shortlists[q.id][:5], chunks, q, 5) for q in dev()) / len(dev())
    at10 = sum(
        ceiling(shortlists[q.id], chunks, q, 10) for q in dev()
    ) / len(dev())
    assert at5 == pytest.approx(0.737, abs=0.005)
    assert at10 == pytest.approx(0.895, abs=0.005)


def test_a_deeper_shortlist_does_not_raise_it_further():
    """0.895 at depth 10, 20 and 50. Beyond ten candidates there is nothing more
    to reorder — which also caps how deep a shortlist is worth paying for."""
    chunks, shortlists, _, _ = setup()
    at = lambda d: sum(ceiling(shortlists[q.id], chunks, q, d) for q in dev()) / len(dev())  # noqa: E731
    assert at(10) == pytest.approx(at(20)) == pytest.approx(at(50))


# -- and the negative result --------------------------------------------------


def test_the_features_alone_are_much_worse_than_the_retriever():
    """alpha=0 — trust the features, discard the ranking — takes k=3 from 0.737
    to 0.474. Three hand-picked features are a far worse model of relevance than
    BM25 plus RRF, which are the product of fifty years and four pages
    respectively."""
    chunks, shortlists, df, n = setup()
    features_only = measure(
        lambda q: rerank(q.text, shortlists[q.id][:20], chunks, df, n, alpha=0.0), 3
    )
    retriever_only = measure(lambda q: shortlists[q.id], 3)
    assert features_only == pytest.approx(0.474, abs=0.02)
    assert retriever_only == pytest.approx(0.737, abs=0.005)


def test_the_best_alpha_is_the_one_that_does_nothing():
    """**The day.**

    Sweep alpha from 0 to 1 at k=3: 0.474, 0.579, 0.579, 0.579, 0.737, 0.737.
    Monotone, and the maximum is at alpha=1 — the identity.

    Every amount of this reranker makes the ranking worse or leaves it alone.
    There is a sixteen-point ceiling sitting right there and these features
    capture **none** of it.

    A reranker is not a step you add. It is a **claim that you have a better
    model of relevance than your retriever**, and three features you invented on
    Monday are not that. A cross-encoder wins because it reads the query and the
    chunk together and was trained on millions of judgments — neither of which is
    true of anything you can write by hand.

    The transferable rule, and it is week 6's rule again in a new costume:
    **compare the reranked list against the un-reranked shortlist.** Almost
    nobody does, because a reranker is assumed to help."""
    chunks, shortlists, df, n = setup()
    scores = [
        measure(lambda q, a=a: rerank(q.text, shortlists[q.id][:20], chunks, df, n, alpha=a), 3)
        for a in (0.0, 0.3, 0.5, 0.7, 0.9, 1.0)
    ]
    assert scores == sorted(scores)
    assert scores[-1] == pytest.approx(measure(lambda q: shortlists[q.id], 3))
    assert scores[0] < scores[-1]
