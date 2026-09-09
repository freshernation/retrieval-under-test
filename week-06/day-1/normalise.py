"""Why you cannot add a BM25 score to a cosine.

Week 5 left you with two retrievers and a measured reason not to fuse them: the
headroom on nine dev queries was zero at every k.

So the first thing this week does is fix the instrument. The course ships
`data/gold/rfc/queries-extended.yml` — the sixteen you have plus ten more dev
queries, written the same way — and from today the labs load that.

Note what is *not* happening: the old file is not edited. An eval set that grows
is a **new instrument**, not a corrected one, and numbers taken with the two are
not comparable. Weeks 1 to 5 keep the set they measured against.

    queries = raglab.judgments.load(file="queries-extended.yml")

With nineteen answerable dev queries the headroom is no longer zero, and the
question of how to combine two retrievers becomes worth asking. Today is the
obvious answer, and why it does not work.

Replace each `raise NotImplementedError` with your own code.
"""

from __future__ import annotations

import statistics


def min_max(scores: dict[str, float]) -> dict[str, float]:
    """Rescale to [0, 1] per query.

    Return all-1.0 when every score is equal — including the single-result case.
    Returning 0.0 there would silently rank a sole exact match last.

    Then look at what this does, because it is the day's second lesson: **every
    query's top result becomes exactly 1.0**, whether its raw top score was 24.7
    or 16.3, whether the runner-up was far behind or a whisker away. The
    normalisation discards precisely the signal you would want in order to
    decide how much to trust this retriever on this query.
    """
    raise NotImplementedError


def z_score(scores: dict[str, float]) -> dict[str, float]:
    """Standardise to mean 0, standard deviation 1, per query.

    Return all-0.0 for a constant set or a single value.

    Better than min-max in one way — the shape of the distribution survives — and
    it assumes the scores are roughly symmetric around a mean, which retrieval
    scores are not: a handful of good matches and a long tail of near-zeros.
    """
    raise NotImplementedError


def combine(a: dict[str, float], b: dict[str, float], weight: float = 0.5) -> dict[str, float]:
    """`weight * a + (1 - weight) * b`, over the union, missing scores as 0.0.

    Treating a missing score as 0.0 is a real assumption and it is usually
    wrong: absent from the top 50 is not "scored zero", it is "not measured".
    With min-max normalised scores 0.0 is the *worst* result rather than no
    result, so a chunk one retriever never saw is actively penalised.

    Raise ValueError for a weight outside [0, 1].
    """
    raise NotImplementedError


def ranked(scores: dict[str, float], k: int | None = None) -> list[str]:
    """Ids best first, ties broken by id."""
    raise NotImplementedError


def top_gap(scores: dict[str, float]) -> float:
    """`(top - second) / |top|`. 0.0 for fewer than two scores or a zero top.

    A cheap confidence signal: a large gap means one result stood out, a small
    one means the retriever could not separate its candidates. It is exactly
    what `min_max` destroys, and week 11's routing is built from signals like it.
    """
    raise NotImplementedError
