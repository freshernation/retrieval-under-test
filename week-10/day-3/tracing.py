"""Tracing: the field that costs nothing and is always missing.

A trace is usually sold as a latency tool — spans, a waterfall, find the slow
one. That is the small half of what it is for.

The large half is this: the course's central rule is *attribute the failure to
exactly one station before you change anything*, and a trace carrying the
**ids** each stage chose lets a machine perform that walk, after the fact, on an
incident nobody can reproduce.

Durations tell you which stage was slow. Ids tell you which stage was wrong, and
they are one list per stage.

Replace each `raise NotImplementedError` with your own code.
"""

from __future__ import annotations

from dataclasses import dataclass, field

STATION_1 = "1 corpus"
STATION_2 = "2 chunk"
STATION_4 = "4 retrieve"
STATION_5 = "5 rank"
STATION_6 = "6 generate"
NO_FAILURE = "7 none"

REQUIRED_IDS = ("shortlist", "context")


@dataclass
class Span:
    """One stage. `ids` is what makes the trace worth keeping.

    A plain record with no computed fields: a span that knows its own share
    needs to know the total, which means it goes stale the moment the next stage
    runs. Let `critical_path` do the division.
    """

    name: str
    ms: float
    ids: tuple[str, ...] = ()


@dataclass
class Trace:
    """One request. Spans in the order they ran.

    Keep this a plain record. A trace that computes anything is a trace that can
    disagree with the system it is describing.
    """

    query_id: str
    spans: list[Span] = field(default_factory=list)

    def record(self, name: str, ms: float, ids=()) -> None:
        """Append a span. Ids optional in the signature and mandatory in
        practice — see `missing_ids`."""
        raise NotImplementedError

    @property
    def total(self) -> float:
        """Sum of the spans. Not the request's latency: that includes the gaps
        between spans, and the gaps are where a queue hides."""
        raise NotImplementedError

    def ids(self, stage: str) -> tuple[str, ...]:
        """What that stage chose. `()` if the stage did not record any, which is
        not the same as a stage that chose nothing."""
        raise NotImplementedError


def critical_path(trace: Trace) -> tuple[str, float]:
    """The slowest span's name and its share of the total.

    One number, and it is the only latency number worth putting in a summary:
    everything else is a decision about a stage that is not the problem.
    """
    raise NotImplementedError


def missing_ids(trace: Trace) -> list[str]:
    """Which of `REQUIRED_IDS` the trace failed to record, sorted.

    A trace missing these can time a request and cannot explain one. It is the
    cheapest field in the system — two lists of ten short strings — and it is the
    one that gets dropped when somebody trims the log volume.
    """
    raise NotImplementedError


def attribute(trace: Trace, query, chunks: dict[str, str], faithful: float) -> str:
    """Walk 1 → 7 and stop at the first station that failed.

    | station | the test |
    |---|---|
    | 1 corpus | the query has no answer spans at all |
    | 2 chunk | spans exist, and no chunk contains them |
    | 4 retrieve | a chunk has them, and the shortlist does not |
    | 5 rank | the shortlist has them, and the packed context does not |
    | 6 generate | the context has them, and the answer is unfaithful |
    | 7 none | every station did its job |

    There is no station 3 branch, because an index failure presents as a
    retrieval failure and the trace cannot tell them apart. Say that rather than
    inventing a test for it.

    `7 none` does **not** mean the answer was right. Hold on to that.
    """
    raise NotImplementedError


def attribution_report(stations) -> dict[str, int]:
    """Counts per station, including zeros for the stations nothing hit.

    The zeros are the point. A station with no failures is a station nobody
    should be working on, and it is usually where the work is going.
    """
    raise NotImplementedError
