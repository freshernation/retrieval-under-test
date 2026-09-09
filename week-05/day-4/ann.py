"""Not looking at everything.

`neighbours()` is one matrix multiply against every row. At 266 chunks that is
free. At ten million vectors it is the whole system, and every vector database
you will ever use exists to avoid it.

The trade is exact for approximate: examine a fraction of the vectors and accept
that you will sometimes miss a true neighbour. Today you build the simplest
version that really works — cluster the vectors, and search only the nearest
clusters — and measure exactly what the approximation costs.

**Be clear that this is a demonstration.** At 266 vectors an approximate index
is slower than brute force, and today's last test proves it. You are building it
so that you know what a service is doing when it does this for you, and so that
you can read its recall numbers.

Replace each `raise NotImplementedError` with your own code.
"""

from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np

from similarity import l2_normalise


def kmeans(D: np.ndarray, n_clusters: int, seed: int = 0, iterations: int = 25):
    """Spherical k-means: `(centroids, assignments)`.

    The vectors are unit length, so "nearest" is largest dot product and the
    centroid update is the normalised mean of a cluster's members.

    Seed the initial choice with `np.random.default_rng(seed)` and sort the
    chosen rows, so the clustering is **identical on every machine**. An index
    that reshuffles between builds makes two runs of the same configuration
    disagree, and you will spend a day on it.

    Stop early when nothing moves.
    """
    raise NotImplementedError


@dataclass
class IVF:
    """An inverted file index: centroids, and the rows belonging to each.

    `comparisons` records how many vectors the last search actually looked at.
    It is the only honest measure of what the index bought, and no vector
    database exposes it.
    """

    ids: list[str]
    vectors: np.ndarray
    centroids: np.ndarray
    lists: dict[int, list[int]] = field(default_factory=dict)
    comparisons: int = 0

    @property
    def n_lists(self) -> int:
        raise NotImplementedError


def build_ivf(D: np.ndarray, ids: list[str], n_clusters: int = 16, seed: int = 0) -> IVF:
    """Cluster the vectors and record which rows fell into each list.

    Create an entry for **every** cluster, including empty ones. A cluster that
    won no members still exists, still gets compared against, and a `KeyError`
    at query time on a rare probe order is a delightful bug to find in
    production.
    """
    raise NotImplementedError


def brute_force(D: np.ndarray, ids: list[str], q: np.ndarray, k: int = 5) -> list[str]:
    """Exact search over every row. The thing you are approximating, and the
    only way to know what the approximation costs."""
    raise NotImplementedError


def search_ivf(ivf: IVF, q: np.ndarray, k: int = 5, nprobe: int = 1) -> list[str]:
    """Search the `nprobe` nearest clusters. Sets `ivf.comparisons`.

    Count the centroid comparisons **as well as** the vector ones. They are not
    free, there are `n_lists` of them on every query, and leaving them out is how
    an index reports a saving it did not make — which today's last test
    demonstrates.

    `nprobe` of at least 1, always. A search that probes nothing returns nothing
    and looks like a broken index rather than a misconfigured one.
    """
    raise NotImplementedError


def ann_recall(approx: list[str], exact: list[str]) -> float:
    """Fraction of the exact top-k the approximate search also found.

    **This is not retrieval recall and confusing the two is the day's real
    lesson.** It measures agreement with brute force over the same vectors — a
    property of the index — and says nothing about whether those vectors were
    the right answer.

    An empty exact result is 1.0: the index correctly found nothing.
    """
    raise NotImplementedError
