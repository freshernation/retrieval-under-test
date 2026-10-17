"""A graph index, by hand - and the size at which it is worth it.

Week 5 built an approximate index by clustering: probe the nearest few clusters,
skip the rest. The index most vector databases use instead is HNSW - a hierarchy of
navigable small-world graphs. Each vector is linked to a few near neighbours; a
search starts at the top of the hierarchy, where links are long, walks greedily
towards the query, and drops a layer each time it can get no closer.

It is very good, at scale. Today you build one, and measure where "at scale"
starts.

Replace each `raise NotImplementedError` with your own code.
"""

from __future__ import annotations


class HNSW:
    """HNSW(M=8, ef_construction=32, seed=0)

    Vectors are unit vectors; distance is 1 - dot product. Every call to
    `distance` adds 1 to `self.distances` - that is the cost you are measuring.

        .random_level() -> int     int(-log(1 - random()) / log(M)), from a
                                   random.Random(seed) the index owns
        .search_layer(q, entries, ef, layer) -> [(distance, node), ...] nearest first
                                   the standard greedy best-first search: a
                                   candidate heap and a best-ef heap; stop when the
                                   nearest candidate is farther than the worst of ef
        .add(doc_id, vector)       pick a level; descend from the entry point with
                                   ef=1 above it; at each layer at or below it, find
                                   ef_construction neighbours, keep the nearest M
                                   (2*M on layer 0), link both ways, and prune any
                                   neighbour that now has too many links to its
                                   nearest ones. A new highest level becomes the entry.
        .search(q, k=10, ef=16) -> [doc ids]
                                   descend with ef=1, then search layer 0 with
                                   max(ef, k)
    """

    def __init__(self, M: int = 8, ef_construction: int = 32, seed: int = 0) -> None:
        raise NotImplementedError

    def distance(self, a, b: int) -> float:
        raise NotImplementedError

    def random_level(self) -> int:
        raise NotImplementedError

    def search_layer(self, q, entries, ef, layer):
        raise NotImplementedError

    def add(self, doc_id: str, vector) -> None:
        raise NotImplementedError

    def search(self, q, k: int = 10, ef: int = 16) -> list[str]:
        raise NotImplementedError


def build(ids, D, M: int = 8, ef_construction: int = 32, seed: int = 0) -> HNSW:
    """Add every row of D under its id, in order; then reset `distances` to 0."""
    raise NotImplementedError


def brute_force(ids, D, q, k: int = 10) -> list[str]:
    """The exact top k by dot product, ties by position."""
    raise NotImplementedError


def recall(approx: list[str], exact: list[str]) -> float:
    """Share of `exact` found in `approx`. 1.0 when exact is empty."""
    raise NotImplementedError
