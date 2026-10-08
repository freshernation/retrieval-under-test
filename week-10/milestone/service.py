"""Milestone 10 — the pipeline behind a service boundary.

Everything this week measured, in one object: a cache in front, a trace per
request, a token count, a per-stage budget, and an attribution walk that runs in
CI rather than in production.

The boundary is the point. Nine weeks produced a pipeline; a service is a
pipeline with a **contract** — what it promises, what it costs, what it records
when it fails, and what it refuses to promise.

Replace each `raise NotImplementedError` with your own code.
"""

from __future__ import annotations


class Service:
    """One request in, one answer and one trace out.

    `cache` is optional and defaults to off. The default matters: week 7 shipped
    a milestone whose every optional stage defaulted to off, for the same reason
    — a stage nobody switched on deliberately is a stage nobody measured. A
    cache in particular changes what the system *says*, not just how fast it
    says it, and day 2 measured that.
    """

    def __init__(self, build_context, generator, chunks, index, *, cache=None, budget=None) -> None:
        raise NotImplementedError

    @property
    def config(self) -> dict:
        """Everything a run id has to pin down, including whether the cache was
        on and what its capacity was. A cached run and an uncached run of the
        same code are two different systems."""
        raise NotImplementedError

    def answer(self, query):
        """Returns `(answer, context, trace)`.

        `build_context(query_text)` returns `(shortlist, context)` — both,
        because the trace needs the shortlist ids and day 3 showed what a trace
        without ids is worth.

        The trace records a span per stage **with ids** — see day 3 — and the
        service hands it back rather than logging it, so the caller decides what
        to keep. A service that swallows its own trace is a service you debug by
        adding print statements to somebody else's code.
        """
        raise NotImplementedError


def service_report(service, queries, chunks) -> dict:
    """What the service costs and where it breaks.

    `work` (p50 and p95 of the per-request total), `tokens_per_query`,
    `attribution` (day 3's station counts), `cache` (hits and hit rate), and
    `exceeds` (the stages over budget).

    No quality number. The quality numbers are weeks 8 and 9's and they belong
    in the eval harness, not in a service report — a service report that carries
    a faithfulness score invites somebody to watch it on a dashboard, where
    week 9 measured it as useless.
    """
    raise NotImplementedError


def slo(report: dict, targets: dict) -> dict:
    """Per target: `value`, `target`, `met`.

    Targets are an argument because every one of them is a judgment. Nothing in
    this repository derives a latency target, and a default would read as though
    something did.
    """
    raise NotImplementedError


def ship_check(report: dict, slo_result: dict) -> list[str]:
    """Reasons to refuse, sorted. Empty means ship.

    Refuse when an SLO is unmet, when a stage is over budget, when the budget
    curve has a wasteful step, and when the attribution report puts a failure at
    a station nobody has looked at.

    Week 6's `ship_check` refused hybrid retrieval because BM25 scored higher.
    This one refuses for operational reasons, and the pattern is the same: the
    function that says no is the one worth writing.
    """
    raise NotImplementedError
