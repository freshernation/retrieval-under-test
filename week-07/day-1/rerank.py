"""Reordering a shortlist with a better model of relevance.

A reranker takes the top `n` from retrieval and reorders them using something
more expensive and, in principle, more accurate. In production that is usually a
cross-encoder — a model that reads the query and the chunk *together*, which a
retriever cannot do because it must embed the chunk before it has seen the query.

There is no model in this course, so today you build the other kind: a
**feature-based reranker**, which is what learning-to-rank did for twenty years
and what a cross-encoder replaced. Term coverage weighted by rarity, exact
phrase presence, where in the chunk the first match falls.

Today's result is negative and you should know that going in: **it loses.** Why
it loses is the most useful thing in the week.

Replace each `raise NotImplementedError` with your own code.
"""

from __future__ import annotations

import math

from analyzer import analyze


def document_frequencies(chunks: dict[str, str]) -> dict[str, int]:
    """Term → number of chunks containing it. Computed once, over the corpus."""
    raise NotImplementedError


def idf(term: str, df: dict[str, int], n: int) -> float:
    """Week 3's idf, over chunks. An unseen term gets the maximum weight, which
    is correct — a term nothing contains is maximally discriminating — and worth
    noticing, because it means a typo in a query scores like a rare word."""
    raise NotImplementedError


def features(query: str, text: str, df: dict[str, int], n: int) -> dict[str, float]:
    """Three features, each in [0, 1]:

    - `coverage` — idf-weighted fraction of the query's distinct terms present.
      Weighted, because covering `429` matters and covering `the` does not
    - `phrase` — 1.0 if any adjacent query bigram appears in the chunk. Week 3's
      phrase search, as a feature rather than a filter
    - `earliest` — how near the start the first query term falls, in [0, 1].
      The intuition is that a chunk *about* the query mentions it early. It is an
      intuition, it is not derived from anything, and today you find out what it
      is worth

    Return zeros for an empty query rather than dividing by zero.
    """
    raise NotImplementedError


DEFAULT_WEIGHTS = {"coverage": 1.0, "phrase": 0.5, "earliest": 0.2}


def feature_score(query, text, df, n, weights=None) -> float:
    """Weighted sum of the features."""
    raise NotImplementedError


def prior(shortlist: list[str], c: float = 10.0) -> dict[str, float]:
    """The retriever's own opinion, as a score in [0, 1] from rank alone.

    `1 / (c + rank)`, normalised so the top is 1.0 — week 6's RRF contribution,
    reused. It is here because **the retriever's ranking is evidence**, and a
    reranker that discards it starts from nothing.
    """
    raise NotImplementedError


def rerank(query, shortlist, chunks, df, n, alpha: float = 0.5, weights=None) -> list[str]:
    """`alpha * prior + (1 - alpha) * features`, best first.

    `alpha = 1.0` is the identity — the retriever's order, unchanged. `alpha =
    0.0` throws the retriever away and trusts the features alone.

    Break ties by the shortlist's original order, so that a reranker with nothing
    to say leaves the ranking exactly as it found it.

    Sweep `alpha` and read the whole curve. On this corpus it is monotone, and
    the best value is the one that does nothing.
    """
    raise NotImplementedError


def ceiling(shortlist: list[str], chunks, query, depth: int) -> float:
    """Answer recall over the whole shortlist — the best a **perfect** reranker
    could achieve at any k, since reordering cannot introduce a chunk retrieval
    did not return.

    Compute this before building any reranker. If it equals your current recall
    at k, there is nothing to win and you can stop.
    """
    raise NotImplementedError
