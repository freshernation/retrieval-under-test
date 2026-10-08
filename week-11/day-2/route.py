"""Routing: send each query to the strategy that works for it.

Day 1 found a rewrite that gains two queries and loses three. The obvious next
move — and it is the right next move — is to apply it only where it helps.

This is also the first use the course has for week 9's best discovery.
Retrieval confidence predicted whether the answer reached the context at AUC
0.83, needing no ground truth and available on every request. A router is
exactly what a signal like that is for.

Today measures the headroom first, then tries to capture it. In that order,
because a router whose ceiling you have not computed is a router you cannot
evaluate — week 7 computed the reranking ceiling before the reranker for the
same reason.

Replace each `raise NotImplementedError` with your own code.
"""

from __future__ import annotations

BASELINE = "baseline"
REWRITE = "rewrite"


def oracle_best(outcomes: dict[str, dict[str, bool]]) -> dict[str, bool]:
    """Per query: did **any** strategy answer it.

    A perfect router's result, and therefore the ceiling. It is not achievable —
    it requires knowing the answer before choosing the strategy — and that is
    the point of computing it.
    """
    raise NotImplementedError


def headroom(baseline: dict[str, bool], oracle: dict[str, bool]) -> float:
    """What routing could buy, at most. If this is small, stop."""
    raise NotImplementedError


def route(signal: dict[str, float], threshold: float) -> dict[str, str]:
    """Below `threshold` take `REWRITE`, at or above take `BASELINE`.

    The direction is a decision and it should be the one your evidence supports.
    Here it is the intuitive one — rewrite the queries the retriever seems
    unsure about — and intuitive is not the same as measured.
    """
    raise NotImplementedError


def apply_routes(routes: dict[str, str], outcomes: dict[str, dict[str, bool]]) -> dict[str, bool]:
    """The outcome each query actually got, under those routes."""
    raise NotImplementedError


def capture(baseline: dict[str, bool], routed: dict[str, bool], oracle: dict[str, bool]) -> float:
    """Fraction of the headroom the router captured. `0.0` when there was none.

    Negative is legal and it is information: a router that captures -0.5 is
    doing worse than not routing, which a raw answered-rate comparison against
    the baseline would also tell you, more quietly.
    """
    raise NotImplementedError


def sweep(signal: dict[str, float], outcomes: dict[str, dict[str, bool]], thresholds) -> dict:
    """Per threshold: `answered`, `routed` (how many queries went the non-default
    way), and `capture`.

    Sweep rather than pick. A single threshold that happens to work is a
    threshold chosen on the dev set, and week 9 has the arithmetic for how much
    that is worth at this n.
    """
    raise NotImplementedError
