"""Chunking is a cost decision.

Three days of measurement point at one conclusion, and it is not the one the
folklore prepares you for. Chunking did not improve retrieval on this corpus.
Whole documents get **every** answer into the top 3.

They do it with 22,175 words of context per query.

That is the finding. You do not chunk because it retrieves better — here it
retrieves the same or worse. You chunk because 22,175 words is a bill you cannot
pay, and the question is how little context you can spend and still have the
answer in it.

Which makes this a two-dimensional problem with a frontier, not a parameter with
an optimum. Today you draw the frontier and pick a point on it.

Replace each `raise NotImplementedError` with your own code.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Point:
    """One configuration at one `k`: what it retrieves and what it costs."""

    name: str
    k: int
    recall: float
    tokens: float

    def dominates(self, other: "Point") -> bool:
        """Whether this point is at least as good on both axes and strictly
        better on one — higher recall, lower cost.

        A point never dominates itself, and neither does an identical
        `(name, k)`. Get that wrong and `pareto` returns an empty frontier,
        which looks like a data problem and is not.
        """
        raise NotImplementedError


def context_cost(ranked: list[str], chunks: dict[str, str], k: int) -> int:
    """Words in the top `k` chunks. Skip ids that are not in `chunks`.

    This is the number that becomes money, latency, and — in week 7 — a
    generator's attention budget. It is the axis nobody plots.
    """
    raise NotImplementedError


def measure(chunks, queries, rank_fn, name: str, k: int) -> Point:
    """Run `rank_fn(query_text, chunks, k)` over the queries and build a Point.

    Average the cost over the **answerable** queries only, so that recall and
    cost are computed on the same denominator. Mixing them is how you produce a
    frontier whose two axes describe different query sets.
    """
    raise NotImplementedError


def pareto(points: list[Point]) -> list[Point]:
    """The non-dominated points, cheapest first.

    Everything else can be discarded without argument: for each discarded point
    there is another that is at least as accurate and no more expensive.

    This is the honest way to present a chunking decision, and it is what a
    table of "chunk size versus nDCG" cannot be, because that table has one axis
    and the decision has two.
    """
    raise NotImplementedError


def cheapest_meeting(points: list[Point], target: float) -> Point | None:
    """The cheapest point reaching at least `target` recall, or None.

    **This is the function that makes the decision**, and it needs a number from
    outside the system: how often is it acceptable for the answer not to be in
    the context at all? Nobody can compute that for you. A support search box and
    a system quoting drug interactions have very different answers, and pretending
    the difference is a chunk size is how a real decision gets made by default.

    Break ties by `k` then name, so the result is stable.
    """
    raise NotImplementedError


def savings(a: Point, b: Point) -> float:
    """How many times cheaper `b` is than `a`, to one decimal. 0.0 if b is free.

    The number to put in the report, because "sections beat fixed windows" is an
    opinion and "23× less context for the same answers" is a result.
    """
    raise NotImplementedError
