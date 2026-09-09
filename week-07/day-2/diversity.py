"""Redundancy, and a metric that cannot see it.

Look at what a top-5 actually contains on this corpus: **2.4 distinct documents**
for five chunks, 57% of the pairs from the same document, and one pair 95%
identical by word overlap.

Five results, two documents. That is a context window mostly spent saying the
same thing twice.

Today you build the standard fixes — deduplication and maximal marginal
relevance — and discover that your metric is **structurally incapable** of
telling you whether they helped. That is the day, and it is a lesson about
measurement rather than about diversity.

Replace each `raise NotImplementedError` with your own code.
"""

from __future__ import annotations

import itertools

from windows import parent


def similarity(a: str, b: str) -> float:
    """Word-level Jaccard between two chunk texts. Two empty texts are identical.

    Crude on purpose. Week 2 built shingles and MinHash for near-duplicate
    *documents*; here you are comparing five short texts inside one result list,
    so exact set overlap is cheap and adequate — and using the heavier machinery
    would obscure that the interesting question today is not how you measure
    similarity.
    """
    raise NotImplementedError


def redundancy(ranked: list[str], chunks: dict[str, str], k: int) -> float:
    """Mean pairwise similarity within the top `k`. 0.0 for fewer than two.

    The number to report next to any diversity claim. Baseline here is 0.139.
    """
    raise NotImplementedError


def same_document_pairs(ranked: list[str], k: int) -> int:
    """Pairs in the top `k` sharing a parent document.

    Week 4's `parent()` again. On this corpus the top-5 averages **5.68 of 10
    possible pairs** from the same document — which is a fact about the chunker
    as much as about the retriever, and neither is wrong.
    """
    raise NotImplementedError


def distinct_documents(ranked: list[str], k: int) -> int:
    """How many different documents the top `k` came from."""
    raise NotImplementedError


def dedupe(ranked: list[str], chunks: dict[str, str], threshold: float = 0.8) -> list[str]:
    """Greedily drop any chunk too similar to one already kept.

    Order preserved, first occurrence wins. It is the conservative fix: it only
    removes near-identical text, so it cannot cost you an answer unless two
    chunks were nearly the same and only one carried it.

    Run it and look at how little it removes. On this corpus, near-duplicate
    *chunks* inside one result list are rare — the redundancy is different
    sections of the same document saying related things, which is not the same
    problem and which `dedupe` correctly leaves alone.
    """
    raise NotImplementedError


def mmr(ranked: list[str], chunks: dict[str, str], k: int, lam: float = 0.7) -> list[str]:
    """Maximal marginal relevance: pick greedily, trading relevance against
    similarity to what is already chosen.

        value(d) = lam * relevance(d) − (1 − lam) * max similarity to selected

    Use `1 / (rank + 1)` as the relevance, since you have an order rather than
    comparable scores — week 6's lesson, reused.

    `lam = 1.0` is the identity. Lower `lam` buys diversity and, at some point,
    costs relevance. Raise ValueError outside [0, 1].
    """
    raise NotImplementedError
