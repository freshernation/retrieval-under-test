"""Text as geometry.

Four weeks of treating a document as a bag of terms. Today the bag becomes a
**point in space**, and similarity becomes an angle.

That is a smaller step than it sounds — everything today is still lexical, and
today's last test proves it in one line — but the geometry is what week 5 is
built on, and it is worth having in your hands before the interesting part.

A note on what this course uses for vectors, said now rather than discovered
later: there is no model here. Weeks 5 to 9 run **offline and deterministically**,
so the dense representation you build tomorrow is computed from the corpus
itself by linear algebra. It is a real technique with a real literature and it
is not what a modern embedding model does. Day 3's second article says exactly
which lessons transfer and which do not.

Replace each `raise NotImplementedError` with your own code.
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "week-03" / "day-1"))
from analyzer import analyze  # noqa: E402


def build_vocabulary(chunks: dict[str, str]) -> tuple[list[str], list[str]]:
    """`(chunk ids sorted, vocabulary sorted)`.

    Both sorted, because they are the **axes of your space** and every matrix,
    every vector and every saved artefact indexes into them by position. A
    vocabulary that changes order between two runs makes every stored vector
    silently meaningless — the numbers are fine and they refer to different
    words. This is `raglab.vectors`' manifest check, and it is the most common
    way an embedding index breaks in production.
    """
    raise NotImplementedError


def count_matrix(chunks: dict[str, str], ids: list[str], vocab: list[str]) -> np.ndarray:
    """A `len(ids) × len(vocab)` matrix of raw term counts.

    One row per chunk, one column per term. Build the term-position lookup
    **once** outside the loop; `vocab.index(term)` inside a double loop is a
    linear scan of four thousand strings per token and it will take minutes.
    """
    raise NotImplementedError


def idf_weights(X: np.ndarray) -> np.ndarray:
    """The BM25 idf, per column, computed from the matrix.

    Same formula as week 3, over chunks rather than documents. Note what
    chunking did to it: `429` was in 1 document of 10 and is now in a handful of
    266 chunks, so its idf went **up**. Chunking changes your scoring function
    without touching your scoring function.
    """
    raise NotImplementedError


def weight(X: np.ndarray, idf: np.ndarray) -> np.ndarray:
    """`log(1 + tf) * idf`.

    The log is week 3's saturation, in the simplest form that has one: the tenth
    occurrence is worth much less than the second. It is not BM25 — there is no
    length normalisation here, and cosine will handle that instead, which is a
    real difference and not a simplification.
    """
    raise NotImplementedError


def l2_normalise(v: np.ndarray) -> np.ndarray:
    """Scale to unit length. Works on a vector or on each row of a matrix.

    A zero vector stays zero rather than becoming `nan`. You will have zero
    rows — a chunk of pure boilerplate whose every term was filtered — and one
    `nan` propagates through a matrix multiply into every score you compute.
    """
    raise NotImplementedError


def cosine(a: np.ndarray, b: np.ndarray) -> float:
    """Cosine of the angle between two vectors. 0.0 if either is zero.

    **Why cosine and not the dot product**: the dot product grows with length,
    so a long chunk beats a short one for having more of everything. Cosine
    divides it out and asks only about *direction* — which words, in what
    proportion.

    That is week 3's length normalisation arriving from a completely different
    direction, and it is why `b` matters less once you are working in this
    representation.
    """
    raise NotImplementedError


def query_vector(query: str, vocab: list[str], idf: np.ndarray) -> np.ndarray:
    """The query, in the same space, weighted the same way.

    **The same space.** A query vector built against a different vocabulary
    ordering, or without the idf weighting, produces plausible numbers that mean
    nothing. This is week 3's index-time-versus-query-time analyzer bug in its
    linear-algebra costume, and it is harder to spot because nothing errors.
    """
    raise NotImplementedError


def nearest(matrix: np.ndarray, ids: list[str], q: np.ndarray, k: int = 5) -> list[str]:
    """The `k` ids whose rows are closest to `q` by cosine, best first.

    Normalise both sides once and use a single matrix multiply rather than a
    Python loop over rows. Break ties by row order so the ranking is stable.

    Return `[]` for a zero query vector — a query whose every term is unknown
    matches nothing, and returning the arbitrary first `k` rows would be worse
    than returning nothing.
    """
    raise NotImplementedError


def sparsity(matrix: np.ndarray) -> float:
    """Fraction of entries that are zero.

    Compute it and look at it before tomorrow. It is the number that makes the
    case for everything that follows.
    """
    raise NotImplementedError
