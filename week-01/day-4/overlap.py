"""A retriever, in about forty lines, using nothing you have not met.

No weighting, no IDF, no stemming, no stopwords, no index — all of that is
fenced out this week and most of it is week 3. Split on non-letters, count how
many of the query's words a document contains, sort.

This is a bad retriever. That is the assignment. You need a number on the board
that later weeks are measured against, and it has to be one you built, because a
baseline you did not build is a baseline you will quietly stop comparing to.

Replace each `raise NotImplementedError` with your own code.
"""

from __future__ import annotations

import re
from collections import Counter

_SPLIT = re.compile(r"[^a-z0-9]+")


def normalise(text: str) -> list[str]:
    """Lowercase, split on runs of non-alphanumeric characters, drop empties.

    Keep digits. `4213` and `42` are the most retrievable things in this corpus
    and a tokeniser that throws away numbers throws away the only queries this
    baseline is any good at.

    Note what this destroys, because week 3 is largely about undoing it:
    `$3.00` becomes `3` and `00`, `31-day` becomes `31` and `day`, and
    `ROCC` and `rocc` become the same thing — which helps here and will hurt
    later.
    """
    raise NotImplementedError


def term_set(text: str) -> set[str]:
    """The distinct normalised terms in a string."""
    raise NotImplementedError


def overlap_score(query_terms: set[str], doc_terms: set[str]) -> int:
    """How many distinct query terms the document contains.

    The whole scoring function. Every term is worth exactly one, so `the` counts
    as much as `4213` — which is the defect that motivates the entire of week 3,
    and you should be able to state it before you run anything.
    """
    raise NotImplementedError


def coverage_score(query_terms: set[str], doc_terms: set[str]) -> float:
    """`overlap_score` divided by the number of query terms. In [0, 1].

    Comparable across queries in a way the raw count is not, which matters the
    moment you start looking at per-query numbers.
    """
    raise NotImplementedError


def frequency_score(query_terms: set[str], doc_tokens: list[str]) -> int:
    """Total occurrences of query terms, counting repeats.

    The obvious "improvement" over `overlap_score`, and it is worse. Run
    `test_frequency_scoring_hands_the_top_slot_to_the_longest_document` and see
    what it does. Length normalisation and term saturation — the two things BM25
    is actually for — both exist because of what you are about to watch happen.
    """
    raise NotImplementedError


def rank(
    query: str,
    documents: dict[str, str],
    k: int = 10,
    score=overlap_score,
) -> list[str]:
    """Rank document ids best-first, at most `k`.

    Two rules that are not optional:

    - **Drop zero scores.** A document sharing no query term is not a worse
      answer, it is not an answer. Padding the top ten with them inflates every
      precision number you will ever compute.
    - **Break ties by document id, ascending.** Ties are the normal case for
      this scorer — hundreds of documents will score 2 — and if the order of a
      tie depends on dict iteration order then your metric moves when you add an
      unrelated document to the corpus. Determinism is not tidiness here; a
      benchmark that shifts underneath you is not a benchmark.
    """
    raise NotImplementedError


def explain(query: str, document: str) -> dict[str, set[str]]:
    """Which query terms this document has and which it lacks.

    Returns `{"matched": {...}, "missed": {...}}`.

    The most useful forty lines in week 1. Every failure this baseline has is
    visible in the `missed` set — and week 5's whole argument is that the
    interesting failures are the ones where `missed` contains a word the
    document is *about* but does not contain.
    """
    raise NotImplementedError
