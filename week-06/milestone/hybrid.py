"""A hybrid retriever, and a check that stops you shipping a worse one.

Replace each `raise NotImplementedError` with your own code.
"""

from __future__ import annotations


class HybridRetriever:
    """Lexical plus dense, fused by rank, optionally filtered.

    The config records `c`, the weights, the shortlist `depth`, both component
    configs, and the filter's name. Two hybrids differing only in `c` are
    different systems, and a config that hides that lets you compare them as if
    they were the same.
    """

    def __init__(self, lexical, dense, c: float = 60.0, weights=None, depth: int = 50,
                 predicate=None, filter_name: str = "none") -> None:
        raise NotImplementedError

    @property
    def config(self) -> dict:
        raise NotImplementedError

    def search(self, query: str, k: int = 5) -> list[str]:
        """Fuse the two shortlists, then apply the filter, then take `k`.

        **Filter after fusing, not before.** Filtering each input first means
        each contributes a *different* set of candidates, so the ranks being
        fused are ranks within different populations — and RRF's whole premise
        is that a rank means the same thing on both sides.
        """
        raise NotImplementedError

    def shortfall(self, query: str, k: int = 5) -> int:
        """How many short of `k` this query came, after filtering."""
        raise NotImplementedError


def tune_c(retriever_factory, inputs, chunks, queries, k: int, candidates=(1, 10, 20, 60, 200)):
    """Sweep `c` on `dev` and return `(best_c, {c: recall})`.

    Both, because the sweep is the result. The paper's 60 is a default chosen on
    somebody else's collection in 2009, and on this corpus at k=10 it captures
    **none** of the available headroom while a smaller value captures all of it.

    Break ties towards the value nearest the conventional 60 — on a flat region,
    the least surprising choice is the one that will not need defending twice.
    """
    raise NotImplementedError


def ship_check(fused, inputs: dict[str, dict], chunks, queries, k: int) -> dict:
    """`{"ship": bool, "reason": str, ...}` — the gate.

    Ship only when the fusion **strictly beats every input** at the k you will
    deploy at. Otherwise return the reason and the name of the input that beat
    it, so the report says "we did not ship hybrid retrieval because BM25 alone
    scored higher at k=5", which is a real finding and a good report.

    This exists because the alternative is the most common hybrid-retrieval
    claim there is: a fused system compared against the weaker of its own two
    inputs, reported as an improvement, by somebody who did not lie.
    """
    raise NotImplementedError
