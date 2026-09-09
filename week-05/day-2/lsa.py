"""Changing the axes.

Yesterday's space has one axis per word, which is why two texts sharing no word
are exactly orthogonal however related they are. The vocabulary gap is a
property of the *axes*, so today you change them.

The technique is **latent semantic analysis**: factor the chunk-term matrix,
keep the strongest few hundred directions, and throw the rest away. Terms that
co-occur end up sharing a direction, so a text using one of them lands near a
text using the other.

It is 1990 technology and it is the direct ancestor of everything the field now
calls an embedding. It is also **not** what a modern embedding model does, and
today's second half is about the difference — which is not a footnote, because
one of the two limitations you will measure does not apply to a trained model at
all.

Replace each `raise NotImplementedError` with your own code.
"""

from __future__ import annotations

import numpy as np

from similarity import l2_normalise


def decompose(W: np.ndarray):
    """`U, S, Vt` from a thin SVD of the weighted matrix.

    `W ≈ U @ diag(S) @ Vt`, and the three pieces have readable meanings:

    - **`Vt`** — each row is a direction in *term* space: a weighted mixture of
      words that tend to occur together. These are the new axes
    - **`S`** — how much of the matrix each direction accounts for, largest first
    - **`U`** — where each chunk sits along those directions

    Use `full_matrices=False`. The full version allocates a 4273×4273 matrix you
    will never look at.
    """
    raise NotImplementedError


def variance_kept(S: np.ndarray, k: int) -> float:
    """Fraction of squared singular value mass in the first `k` directions.

    The standard way to talk about how much you kept, and it is a **weaker**
    claim than it sounds: variance is not relevance, and the directions that
    explain the most variance are the ones describing what your corpus is mostly
    about rather than what distinguishes its documents.
    """
    raise NotImplementedError


def dimensions_for(S: np.ndarray, target: float) -> int:
    """The smallest `k` reaching `target` variance.

    Run it at 0.90 on this corpus and look at the answer against the number of
    chunks. The gap between them is the honest measure of how much structure
    there was to find.
    """
    raise NotImplementedError


def embed_chunks(U: np.ndarray, S: np.ndarray, k: int) -> np.ndarray:
    """The chunk embeddings: `U[:, :k] * S[:k]`, rows normalised.

    Scaling by `S` matters — it weights each direction by its importance, and
    dropping it treats the strongest direction and the 200th as equals. Then
    normalise, so that comparison is by angle as it was yesterday.
    """
    raise NotImplementedError


def embed_query(q: np.ndarray, Vt: np.ndarray, k: int) -> np.ndarray:
    """Project a sparse query vector into the same `k` dimensions, normalised.

    `q @ Vt[:k].T`. The query never sees `U` — it was not in the matrix — so it
    is placed using the *term* directions alone. This is the folding-in step, and
    it is the reason a query and a chunk end up comparable at all.

    It also means the query must have been built with the same vocabulary and the
    same idf. A vector from a different `vocab` ordering projects perfectly
    happily and produces numbers that mean nothing.
    """
    raise NotImplementedError


def neighbours(D: np.ndarray, ids: list[str], q: np.ndarray, k: int = 5) -> list[str]:
    """The `k` nearest chunk ids by cosine, best first, stable ties.

    `D` is already normalised, so this is one matrix multiply. Note what that
    costs: **every** row, every query. 266 rows is nothing and ten million is a
    problem, which is Thursday.
    """
    raise NotImplementedError


def term_axes(Vt: np.ndarray, vocab: list[str], axis: int, n: int = 5):
    """The `n` highest-magnitude terms on one direction, as `(term, weight)`.

    Print the first few axes and read them. They are not concepts and they will
    not be tidy — the strongest directions on this corpus are dominated by
    whichever document is longest — and seeing that is worth more than being told
    that LSA finds topics, which it does not.
    """
    raise NotImplementedError
