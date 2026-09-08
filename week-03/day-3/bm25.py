"""BM25 — the one line of arithmetic that week 1 was missing.

Three ideas, each fixing a defect you named in week 1 and could not repair:

    inverse document frequency  ->  every term is worth the same
    term-frequency saturation   ->  the tenth occurrence counts ten times
    length normalisation        ->  the longest document wins everything

None of them is clever. All three were understood by 1994. Together they are
the strongest lexical retriever there is, and they are about forty lines.

`day-2/postings.py` is importable.

Replace each `raise NotImplementedError` with your own code.
"""

from __future__ import annotations

import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "day-2"))
from postings import Index  # noqa: E402

K1 = 1.2
B = 0.75


def idf(document_frequency: int, n_documents: int) -> float:
    """How much a term's presence tells you.

        ln(1 + (N - df + 0.5) / (df + 0.5))

    On this corpus `status` appears in all ten documents and scores **0.047**;
    `429` appears in one and scores **1.992**. Forty times the weight, from one
    logarithm, and it is the entire fix for week 1's first defect.

    The halves are smoothing, and they matter: without them a term in every
    document gives `ln(1 + 0/10) = 0` exactly, so it contributes nothing at all
    and a query made only of common words returns nothing rather than something
    weak. The BM25 form keeps such a term barely alive, which is almost always
    what you want.
    """
    raise NotImplementedError


def saturate(tf: int, k1: float = K1) -> float:
    """`tf * (k1 + 1) / (tf + k1)`. Diminishing returns on repetition.

    At k1=1.2 the values are 1.00, 1.38, 1.96, 2.17 for tf of 1, 2, 10, 100 —
    a hundred occurrences are worth barely twice one. That is the fix for week
    1's `frequency_score`, where the eleven-page governance document won by
    repetition.

    `k1` controls how fast it flattens. k1=0 makes every term binary — present
    or not, repetition worth nothing. Large k1 approaches raw counting. The
    default 1.2 is a convention, not a result, and tomorrow you measure it.
    """
    raise NotImplementedError


def length_norm(doc_length: int, average_length: float, b: float = B) -> float:
    """`1 - b + b * (dl / avgdl)`. A divisor that penalises long documents.

    `b = 0` disables it entirely; `b = 1` divides fully by relative length. The
    default 0.75 is three quarters of the way to full normalisation.

    The reason it is needed here is concrete: this corpus's longest document is
    **fifteen times** its shortest, so without it every query lands on RFC 3986.
    The reason it is not simply `b = 1` is that a long document genuinely is more
    likely to be relevant — it covers more — and full normalisation punishes it
    for that.
    """
    raise NotImplementedError


def score_term(
    tf: int,
    document_frequency: int,
    n_documents: int,
    doc_length: int,
    average_length: float,
    k1: float = K1,
    b: float = B,
) -> float:
    """One term's contribution:

        idf(df, N) * (tf * (k1 + 1)) / (tf + k1 * length_norm(dl, avgdl, b))

    Note where the normalisation goes: **in the denominator, multiplied by k1**,
    not applied to the whole term. That is what makes length interact with
    saturation rather than scaling the result — a long document needs *more*
    occurrences to reach the same saturation, which is the intended behaviour and
    is easy to get wrong by dividing at the end.

    Zero when the term is absent, or when nothing in the corpus contains it.
    """
    raise NotImplementedError


def score(index: Index, query: str, doc_id: str, k1: float = K1, b: float = B) -> float:
    """Sum `score_term` over the analysed query terms.

    Terms repeated in the query are summed again, which is the standard
    formulation and is defensible: a user who types a word twice meant it.
    """
    raise NotImplementedError


def search(index: Index, query: str, k: int = 10, k1: float = K1, b: float = B) -> list[str]:
    """Rank document ids best-first, at most `k`, dropping zero scores.

    Break ties by document id, as in week 1, and for the same reason: ties are
    common and a benchmark that shifts underneath you is not a benchmark.
    """
    raise NotImplementedError
