"""Day 2 — changing the axes.

Read `test_the_vocabulary_gap_closes` and `test_but_only_for_words_the_corpus_has_seen`
together. The second is the honest half.
"""

from functools import cache

import numpy as np
import pytest

import raglab
from lsa import (
    decompose,
    dimensions_for,
    embed_chunks,
    embed_query,
    neighbours,
    term_axes,
    variance_kept,
)
from sections import section_corpus
from similarity import (
    build_vocabulary,
    cosine,
    count_matrix,
    idf_weights,
    l2_normalise,
    query_vector,
    weight,
)
from spans import answer_recall_at_k

CORPUS = raglab.corpus.load()
DOCS = {d.id: d.title + "\n" + d.text for d in CORPUS}
QUERIES = raglab.judgments.load()
ANSWERABLE = [q for q in QUERIES if q.answer_spans]


@cache
def factored():
    chunks = section_corpus(DOCS, 100, 300)
    ids, vocab = build_vocabulary(chunks)
    X = count_matrix(chunks, ids, vocab)
    idf = idf_weights(X)
    W = l2_normalise(weight(X, idf))
    U, S, Vt = decompose(W)
    return chunks, ids, vocab, idf, U, S, Vt


def dense_recall(k: int, at: int = 5) -> float:
    chunks, ids, vocab, idf, U, S, Vt = factored()
    D = embed_chunks(U, S, k)
    total = 0.0
    for q in ANSWERABLE:
        qv = embed_query(query_vector(q.text, vocab, idf), Vt, k)
        total += answer_recall_at_k(neighbours(D, ids, qv, at), chunks, q, at)
    return total / len(ANSWERABLE)


# -- the decomposition --------------------------------------------------------


def test_the_shapes_line_up():
    _, ids, vocab, _, U, S, Vt = factored()
    assert U.shape == (len(ids), len(ids))
    assert Vt.shape == (len(ids), len(vocab))
    assert S.shape == (len(ids),)


def test_it_reconstructs_the_matrix():
    chunks, ids, vocab, idf, U, S, Vt = factored()
    X = count_matrix(chunks, ids, vocab)
    W = l2_normalise(weight(X, idf))
    assert np.allclose(U @ np.diag(S) @ Vt, W, atol=1e-8)


def test_singular_values_are_ordered():
    _, _, _, _, _, S, _ = factored()
    assert np.all(np.diff(S) <= 1e-12)


def test_variance_is_cumulative_and_reaches_one():
    _, _, _, _, _, S, _ = factored()
    assert variance_kept(S, 1) < variance_kept(S, 64) < variance_kept(S, len(S))
    assert variance_kept(S, len(S)) == pytest.approx(1.0)


def test_there_is_less_structure_here_than_you_would_like():
    """191 directions of 266 to reach 90% of the variance. On a corpus this
    small there is not much redundancy to exploit, and a technique whose whole
    premise is redundancy therefore has little to work with.

    Say this out loud before believing anything else today."""
    _, ids, _, _, _, S, _ = factored()
    assert dimensions_for(S, 0.90) == 191
    assert dimensions_for(S, 0.90) / len(ids) > 0.7


# -- the axes -----------------------------------------------------------------


def test_the_axes_are_mixtures_of_terms_not_concepts():
    """Read the first few and be disappointed. The strongest directions on this
    corpus are dominated by whichever document is longest — RFC 6265, on cookies
    — rather than by anything you would call a topic.

    LSA does not find concepts. It finds directions of variance, and on a small
    corpus that is mostly "which document is this"."""
    _, _, vocab, _, _, _, Vt = factored()
    top = [term for term, _ in term_axes(Vt, vocab, 0, 6)]
    assert "cookie" in top
    assert all(t in vocab for t in top)


def test_weights_are_returned_with_the_terms():
    _, _, vocab, _, _, _, Vt = factored()
    pairs = term_axes(Vt, vocab, 1, 3)
    assert len(pairs) == 3
    assert all(isinstance(w, float) for _, w in pairs)


# -- retrieval ----------------------------------------------------------------


def test_more_dimensions_retrieve_more_until_they_stop():
    """0.40 at 16 dimensions, 0.80 at 128, 0.87 at 192 — and 256 adds nothing.

    There is no elbow to find here. It rises and flattens, and picking a
    dimension count is the same kind of decision as picking a chunk size: a
    frontier, not an optimum."""
    assert dense_recall(16) == pytest.approx(0.40, abs=0.05)
    assert dense_recall(128) == pytest.approx(0.80, abs=0.05)
    assert dense_recall(192) == pytest.approx(0.87, abs=0.05)
    assert dense_recall(256) == pytest.approx(dense_recall(192), abs=0.05)


def test_an_unknown_query_still_matches_nothing():
    chunks, ids, vocab, idf, U, S, Vt = factored()
    D = embed_chunks(U, S, 128)
    qv = embed_query(query_vector("kubernetes helm istio", vocab, idf), Vt, 128)
    assert neighbours(D, ids, qv, 5) == []


# -- the point ----------------------------------------------------------------


def test_the_vocabulary_gap_closes():
    """**What you came for.**

    In yesterday's space these pairs are exactly orthogonal — they share no
    term, so the cosine is 0.00. In 128 dimensions:

        too many requests   /  rate limiting          0.00 -> 0.73
        cookie expires      /  max age attribute      0.00 -> 0.61
        crawler             /  robots                 0.00 -> 0.58
        case insensitive    /  uppercase lowercase    0.00 -> 0.56

    Nothing was told to the system about synonyms. The terms co-occur in this
    corpus, so the factorisation put them on shared directions, and now a text
    using one lands near a text using the other."""
    _, _, vocab, idf, _, S, Vt = factored()
    pairs = [
        ("too many requests", "rate limiting", 0.73),
        ("cookie expires", "max age attribute", 0.61),
        ("crawler", "robots", 0.58),
    ]
    for a, b, expected in pairs:
        va, vb = query_vector(a, vocab, idf), query_vector(b, vocab, idf)
        assert cosine(va, vb) == 0.0
        da = embed_query(va, Vt, 128)
        db = embed_query(vb, Vt, 128)
        assert float(da @ db) == pytest.approx(expected, abs=0.06)


def test_but_only_for_words_the_corpus_has_seen():
    """**The honest half, and it is the difference from a trained model.**

    `censorship` is a reasonable word for what RFC 7725 is about. It does not
    appear in this corpus, so it has no column, so it has no position, so it
    contributes exactly nothing. Dense similarity is 0.00, the same as sparse.

    LSA learns its axes *from your corpus and only from your corpus*. A
    vocabulary it never saw does not exist for it.

    This is the limitation that does **not** apply to a trained embedding model:
    those are fitted on far more text than you have, so they place `censorship`
    somewhere sensible without ever seeing your documents. It is the single
    biggest practical difference, and day 3 says which of today's other findings
    survive it and which do not."""
    _, _, vocab, idf, _, _, Vt = factored()
    assert "censorship" not in vocab
    a = embed_query(query_vector("legal reasons", vocab, idf), Vt, 128)
    b = embed_query(query_vector("censorship", vocab, idf), Vt, 128)
    assert float(a @ b) == 0.0


def test_and_it_still_loses_to_bm25():
    """0.87 at its best against BM25's 0.93, after all of that.

    Four weeks of lexical retrieval, one day of linear algebra, and the old
    thing is still ahead. Tomorrow is about *which queries* each one gets, which
    turns out to be a much more interesting question than which mean is
    larger."""
    import sys
    from pathlib import Path

    root = Path(__file__).resolve().parents[2]
    for day in ("day-3", "day-2", "day-1"):
        sys.path.insert(0, str(root / "week-03" / day))
    from bm25 import search

    from postings import Index

    chunks, *_ = factored()
    index = Index(chunks, stopwords=None)
    lex = sum(
        answer_recall_at_k(search(index, q.text, 5), chunks, q, 5) for q in ANSWERABLE
    ) / len(ANSWERABLE)
    assert dense_recall(192) < lex
