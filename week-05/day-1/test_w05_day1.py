"""Day 1 — text as geometry.

The last two tests are why tomorrow exists.
"""

from functools import cache

import numpy as np
import pytest

import raglab
from sections import section_corpus
from similarity import (
    build_vocabulary,
    cosine,
    count_matrix,
    idf_weights,
    l2_normalise,
    nearest,
    query_vector,
    sparsity,
    weight,
)

CORPUS = raglab.corpus.load()
DOCS = {d.id: d.title + "\n" + d.text for d in CORPUS}
QUERIES = raglab.judgments.load()
ANSWERABLE = [q for q in QUERIES if q.answer_spans]


@cache
def space():
    chunks = section_corpus(DOCS, 100, 300)
    ids, vocab = build_vocabulary(chunks)
    X = count_matrix(chunks, ids, vocab)
    idf = idf_weights(X)
    return chunks, ids, vocab, X, idf, weight(X, idf)


# -- the axes -----------------------------------------------------------------


def test_the_axes_are_sorted_and_that_is_not_cosmetic():
    """Ids and vocabulary are the axes of the space, and every stored vector
    indexes into them by position. A vocabulary that changes order between runs
    makes every saved vector silently meaningless — the numbers are fine and
    they refer to different words."""
    _, ids, vocab, _, _, _ = space()
    assert ids == sorted(ids)
    assert vocab == sorted(vocab)


def test_the_matrix_is_chunks_by_vocabulary():
    _, ids, vocab, X, _, _ = space()
    assert X.shape == (266, 4273)
    assert X.shape == (len(ids), len(vocab))


def test_counts_are_counts():
    ids, vocab = build_vocabulary({"a": "cat cat dog"})
    X = count_matrix({"a": "cat cat dog"}, ids, vocab)
    assert X[0, vocab.index("cat")] == 2
    assert X[0, vocab.index("dog")] == 1


# -- weighting ----------------------------------------------------------------


def test_chunking_raised_the_idf_of_a_rare_term():
    """`429` was in 1 document of 10. It is now in a few chunks of 266, so its
    idf went **up**. Chunking changed your scoring function without touching
    your scoring function."""
    _, _, vocab, _, idf, _ = space()
    assert idf[vocab.index("429")] > idf[vocab.index("status")]


def test_the_log_is_saturation_in_its_simplest_form():
    idf = np.ones(1)
    assert weight(np.array([[10.0]]), idf)[0, 0] < 4 * weight(np.array([[1.0]]), idf)[0, 0]


# -- geometry -----------------------------------------------------------------


def test_cosine_ignores_length_and_the_dot_product_does_not():
    """A long chunk beats a short one on the dot product for having more of
    everything. Cosine asks only about direction — which words, in what
    proportion — and that is week 3's length normalisation arriving from a
    completely different direction."""
    a = np.array([1.0, 2.0, 3.0])
    assert cosine(a, a) == pytest.approx(1.0)
    assert cosine(a, 2 * a) == pytest.approx(1.0)
    assert np.dot(a, 2 * a) == 2 * np.dot(a, a)


def test_orthogonal_is_zero_and_opposite_is_negative():
    assert cosine(np.array([1.0, 0.0]), np.array([0.0, 1.0])) == 0.0
    assert cosine(np.array([1.0, 0.0]), np.array([-1.0, 0.0])) == pytest.approx(-1.0)


def test_a_zero_vector_is_zero_not_nan():
    """You will have zero rows — a chunk whose every term was filtered — and one
    `nan` propagates through a matrix multiply into every score you compute."""
    assert cosine(np.zeros(3), np.ones(3)) == 0.0
    assert not np.isnan(l2_normalise(np.zeros(3))).any()
    assert not np.isnan(l2_normalise(np.zeros((2, 3)))).any()


def test_normalising_gives_unit_rows():
    rows = l2_normalise(np.array([[3.0, 4.0], [1.0, 0.0]]))
    assert np.allclose(np.linalg.norm(rows, axis=1), 1.0)


# -- retrieval ----------------------------------------------------------------


def test_it_retrieves():
    chunks, ids, vocab, _, idf, W = space()
    q = QUERIES.by_id("r03")
    top = nearest(W, ids, query_vector(q.text, vocab, idf), 5)
    assert any("451" in chunks[c] for c in top)


def test_an_entirely_unknown_query_matches_nothing():
    """Returning the arbitrary first k rows would be worse than returning
    nothing, and it is what a naive implementation does."""
    _, ids, vocab, _, idf, W = space()
    assert nearest(W, ids, query_vector("kubernetes helm istio", vocab, idf), 5) == []


def test_the_ranking_is_stable():
    _, ids, vocab, _, idf, W = space()
    q = query_vector("robots.txt caching", vocab, idf)
    assert nearest(W, ids, q, 5) == nearest(W, ids, q, 5)


# -- and why tomorrow exists --------------------------------------------------


def test_the_space_is_almost_entirely_empty():
    """4,273 dimensions, and **97.5% of the matrix is zero.**

    Each chunk uses about a hundred of four thousand axes. Almost every pair of
    chunks is exactly orthogonal — not nearly, exactly — because they share no
    term at all."""
    _, _, _, X, _, _ = space()
    assert sparsity(X) > 0.97


def test_two_chunks_about_the_same_thing_can_be_exactly_orthogonal():
    """**The structural problem, in one assertion.**

    Cosine similarity in this space is zero whenever two texts share no term.
    Not small — zero. `31-day pass` and `monthly pass` are perpendicular, and so
    are `rate limiting` and `slow down`.

    This is not a tuning failure and no weighting scheme repairs it. The
    vocabulary gap is a **property of the representation**: one axis per word
    means words are the only thing that can be similar.

    Tomorrow changes the axes."""
    _, _, vocab, _, idf, _ = space()
    a = query_vector("throttle the client", vocab, idf)
    b = query_vector("rate limiting", vocab, idf)
    assert cosine(a, b) == 0.0


def test_and_the_sparse_vector_space_still_loses_to_bm25():
    """0.87 against 0.93 on answer recall at 5. Four weeks of lexical retrieval
    and its best form is BM25, which you already had."""
    import sys
    from pathlib import Path

    root = Path(__file__).resolve().parents[2]
    for day in ("day-3", "day-2", "day-1"):
        sys.path.insert(0, str(root / "week-03" / day))
    from bm25 import search

    from postings import Index
    from spans import answer_recall_at_k

    chunks, ids, vocab, _, idf, W = space()
    index = Index(chunks, stopwords=None)
    cos = sum(
        answer_recall_at_k(nearest(W, ids, query_vector(q.text, vocab, idf), 5), chunks, q, 5)
        for q in ANSWERABLE
    ) / len(ANSWERABLE)
    lex = sum(
        answer_recall_at_k(search(index, q.text, 5), chunks, q, 5) for q in ANSWERABLE
    ) / len(ANSWERABLE)
    assert cos == pytest.approx(0.867, abs=0.02)
    assert lex == pytest.approx(0.933, abs=0.02)
    assert cos < lex
