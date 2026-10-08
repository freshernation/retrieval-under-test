"""Caching: the metric that is not the hit rate.

A cache is the cheapest latency win available and the easiest one to report
dishonestly, because every number it produces is a property of **traffic you
have not measured**.

Start with the thing that should stop you: run a cache over your eval set and
the hit rate is zero. Twenty-six queries, twenty-six distinct. An eval set is
built to have no duplicates — duplicates would weight it — so the instrument you
have spent nine weeks building cannot measure this at all.

What follows is therefore honest simulation, and the honesty is in saying which
assumption produced which number.

Replace each `raise NotImplementedError` with your own code.
"""

from __future__ import annotations


def cache_key(query_text: str) -> str:
    """A normalised key: lowercased, punctuation dropped, whitespace collapsed.

    Every normalisation widens the key's blast radius. Lowercasing merges
    `Set-Cookie` with `set-cookie`, which is probably right, and the next step
    after that is sorting the terms, which merges two different questions. Stop
    early and know what you merged.
    """
    raise NotImplementedError


def distinct(texts) -> int:
    """How many distinct keys. Run it on your eval set first."""
    raise NotImplementedError


class LRU:
    """Least-recently-used, with counters. Forty lines, and it is what the
    service in front of your retriever is doing.

    `capacity=None` is unbounded, which is the case worth measuring first
    because it is the ceiling every bounded cache is working towards.
    """

    def __init__(self, capacity: int | None = None) -> None:
        raise NotImplementedError

    def get(self, key: str):
        """Return the value and count a hit, or `None` and count a miss.

        A hit must also refresh recency, or it is not an LRU — it is a FIFO with
        a misleading name, and the difference shows up only under capacity
        pressure, which is to say only in production.
        """
        raise NotImplementedError

    def put(self, key: str, value) -> None:
        """Insert, evicting the least recently used if over capacity."""
        raise NotImplementedError

    @property
    def hit_rate(self) -> float:
        """Hits over hits plus misses. Zero when nothing has been asked."""
        raise NotImplementedError


def stream(ids, n: int, skew: float, seed: int = 0) -> list[str]:
    """Synthetic traffic: `n` requests over `ids`, weighted `1 / rank ** skew`.

    `skew=0` is uniform, `skew=1` is Zipf, `skew=2` is the concentration a real
    popular-query distribution often shows. Seeded, so the number is
    reproducible — which is not the same as being right.

    **This function is the assumption.** Whatever hit rate you report came from
    here, and the report must say so.
    """
    raise NotImplementedError


def work_saved(hit_ids, costs: dict[str, float]) -> float:
    """Fraction of total work removed by hitting exactly `hit_ids` once each,
    out of serving every id in `costs` once.

    The number that matters, and the one nobody quotes. Hit rate counts
    requests; this counts the thing you were trying to avoid doing.
    """
    raise NotImplementedError


def replay(requests, costs: dict[str, float], capacity: int | None = None) -> dict:
    """Run `requests` through an `LRU(capacity)`.

    Returns `requests`, `hits`, `hit_rate` and `work_saved` — the last as a
    fraction of the work the same stream would have cost with no cache at all.
    """
    raise NotImplementedError


def staleness(cached: dict[str, str], fresh: dict[str, str]) -> dict:
    """Compare a cached context against one rebuilt now.

    Returns `overlap` (fraction of cached keys a fresh build still chooses),
    `missing` (keys the fresh build chose and the cached one does not have), and
    `stale` (keys the cache is serving that a fresh build would not).

    `overlap` is the trap. A cached context can agree with a fresh one about
    five chunks of six and be wrong about the only one that mattered, and the
    cache will report a hit either way.
    """
    raise NotImplementedError
