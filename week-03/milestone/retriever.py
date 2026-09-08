"""The retriever you will carry for the rest of the course — and the arithmetic
that says how big your eval set has to be.

Four days assembled into one object with a config, plus the four functions that
explain why every interval this week touched zero and what to do about it.

Replace each `raise NotImplementedError` with your own code.
"""

from __future__ import annotations

import sys
from pathlib import Path

_WEEK = Path(__file__).resolve().parents[1]
for _day in ("day-1", "day-2", "day-3", "day-4"):
    sys.path.insert(0, str(_WEEK / _day))


class Retriever:
    """An analyzer, an index and a scoring function, with the whole
    configuration in one place.

    The config dict is not decoration. `raglab.runs.record` hashes it, so two
    runs with the same hash measured the same system — and the most common way
    to waste an afternoon is to change something that was never in the config,
    watch the hash stay put, and not notice.

    Every knob you have met this week goes in it: the analyzer options, k1, b,
    and k.
    """

    def __init__(self, documents: dict[str, str], **config) -> None:
        """Build the index once. Keep the config.

        `config` accepts `stopwords`, `stemming`, `identifiers`, `k1`, `b`, `k`,
        and anything else you add. Store defaults for the ones not given, so
        that `self.config` is complete rather than partial — a config that omits
        what it did not set cannot be compared against another one.
        """
        raise NotImplementedError

    @property
    def config(self) -> dict:
        """The complete configuration, for the run ledger."""
        raise NotImplementedError

    def search(self, query: str, k: int | None = None) -> list[str]:
        """Ranked document ids. `k` defaults to the configured one."""
        raise NotImplementedError

    def evaluate(self, queries, ks=(3, 5)):
        """Score this retriever over a query set. Returns a `raglab.metrics.Evaluation`."""
        raise NotImplementedError


def unchanged(a, b, metric: str = "ndcg@3") -> list[str]:
    """Query ids that scored **identically** under both evaluations, sorted.

    Exclude the unanswerable ones, exactly as `raglab.metrics.bootstrap` does.
    They contribute a constant zero difference between any two systems, so
    counting them would inflate the unchanged fraction — and penalise you, in
    the statistics, for having included the query that detects the failure that
    reaches users most often.

    The number that decides everything below. Report it next to every delta you
    ever quote — a system that moved three queries and left six alone has not
    been measured on six of them, and the mean does not say so.
    """
    raise NotImplementedError


def floor_probability(n: int, n_unchanged: int) -> float:
    """The probability that a bootstrap resample of `n` queries draws **only**
    unchanged ones: `(n_unchanged / n) ** n`.

    Every such resample has a delta of exactly zero. If this probability exceeds
    0.025, the 2.5th percentile of the bootstrap distribution *is* zero, so the
    lower bound of a 95% interval is pinned at zero **no matter how large the
    improvement on the other queries**.

    This is not a subtlety about statistics. It is the exact, arithmetic reason
    that every interval you computed this week touched zero, and you can check
    it by hand: nine dev queries, six unchanged, `(6/9)**9 = 0.0260`. Just over.
    """
    raise NotImplementedError


def queries_needed(unchanged_fraction: float, alpha: float = 0.025) -> int:
    """The smallest `n` for which `unchanged_fraction ** n < alpha`.

    At two thirds unchanged the answer is **10**.

    You had nine answerable dev queries this week. **One more would have made
    BM25's result reportable.** Not a bigger corpus, not a better retriever, not
    a cleverer test — one more query, judged by hand, in an afternoon.

    Raise ValueError for a fraction of 1.0: if nothing ever moves, no number of
    queries helps, and the honest answer is that you are not measuring anything.
    """
    raise NotImplementedError


def compare(a, b, metric: str = "ndcg@3", seed: int = 0) -> dict:
    """Everything the report needs about one change, in one dict:

        delta, low, high        from raglab.metrics.bootstrap
        n                       queries scored
        worse                   query ids that regressed
        unchanged               query ids that did not move
        floor                   floor_probability(n, len(unchanged))
        pinned                  whether the lower bound is pinned at zero
        needed                  queries_needed at this unchanged fraction

    A report that quotes `delta` without `pinned` is a report that will claim an
    improvement it did not measure.
    """
    raise NotImplementedError
