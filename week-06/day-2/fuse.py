"""Fusing by rank, because the scores were never comparable.

Yesterday's problem: BM25 scores and cosines are different kinds of number, and
every attempt to make them comparable either destroyed information or produced
a fused ranking that was just BM25.

Today's answer sidesteps it completely. **Do not look at the scores.** Use only
the positions, which every retriever produces on the same scale by construction:
first is first.

Reciprocal rank fusion, Cormack, Clarke and Buettcher, 2009. Four pages, one
formula, and it beat every score-combination method they tested.

    score(d) = sum over retrievers of  1 / (c + rank of d in that retriever)

Replace each `raise NotImplementedError` with your own code.
"""

from __future__ import annotations

MISSING = 10**6


def ranks(ranking: list[str], depth: int | None = None) -> dict[str, int]:
    """Document id to **1-based** position, cut at `depth`.

    One-based because the formula divides by `c + rank` and a zero-based first
    place would give it the same weight as `c` alone — a small bug that shifts
    every score and is invisible in the output.
    """
    raise NotImplementedError


def rrf(
    rankings: list[list[str]],
    k: int | None = None,
    c: float = 60.0,
    weights: list[float] | None = None,
    depth: int = 50,
) -> list[str]:
    """Fuse any number of rankings. Ties broken by id.

    A document absent from a ranking contributes **nothing** from it — not a
    penalty. That is the important difference from yesterday's `combine`, where
    a missing score became 0.0 and actively harmed the document. Here, evidence
    you do not have is simply evidence you do not have.

    `depth` cuts each input list first. It matters: without a cut, a document at
    position 4,000 in one retriever still contributes, and on a large corpus the
    tail is most of the compute for none of the signal.

    Raise ValueError for a non-positive `c` or a weight list of the wrong length.
    """
    raise NotImplementedError


def rrf_scores(
    rankings: list[list[str]], c: float = 60.0, weights: list[float] | None = None, depth: int = 50
) -> dict[str, float]:
    """The fused scores, for when you need them rather than the order."""
    raise NotImplementedError


def contribution(position: int, c: float = 60.0) -> float:
    """What one retriever's `position` contributes: `1 / (c + position)`."""
    raise NotImplementedError


def flattening(c: float, positions: int = 10) -> float:
    """Ratio of first place's contribution to `positions`-th place's.

    This is what `c` actually controls, and stating it as a ratio makes the knob
    legible: at `c = 1` first place is worth **5.5×** tenth place, and at
    `c = 60` it is worth **1.15×** — practically nothing.

    Large `c` says "I trust the fact that a retriever returned this at all, more
    than where it put it". Small `c` says the opposite. The paper's 60 is a
    strong vote for the first, chosen on TREC runs in 2009, and today you find
    out what this corpus thinks.
    """
    raise NotImplementedError
