"""Latency: the number that is not the mean.

Nine weeks of this course measured quality. None of it measured time, and a
retrieval system that is right in four seconds is a system nobody uses.

The trap is immediate. The honest way to time a stage is a stopwatch, and a
stopwatch measures **this implementation on this laptop** — a number that is
useless for comparison and that changes when the machine is busy. So today does
both:

    count the work          deterministic, comparable, the algorithm's cost
    time the wall clock     real, local, and not reportable

The tests assert the counts exactly and the clock not at all, which is the same
discipline week 7 applied to the stipulated model: the shape transfers, the
values do not.

Replace each `raise NotImplementedError` with your own code.
"""

from __future__ import annotations


def work(index, query_text: str) -> int:
    """Postings touched by a lexical search: the sum of the document frequencies
    of the query's distinct terms.

    This is the real cost model of an inverted index — a term appearing in two
    hundred chunks costs two hundred times one appearing in one — and it is the
    reason a one-word query can be cheaper than a ten-word one by two orders of
    magnitude.

    Use `index.analyze_query` and `index.document_frequency` from week 3. Do not
    count a repeated term twice; the index is consulted once per distinct term.
    """
    raise NotImplementedError


def constant_work(n_chunks: int) -> int:
    """Comparisons made by an exhaustive dense search: one per chunk, every time.

    Week 5 built this. Its cost does not depend on the query at all, which is
    either its best property or its worst depending on the query.
    """
    raise NotImplementedError


def percentile(values, p: float) -> float:
    """The nearest-rank percentile: the smallest observed value at or above the
    `p` fraction of the sorted data.

    No interpolation. An interpolated p95 is a number no request experienced,
    and on twenty samples it is also arithmetic performed on a sample size that
    cannot support it. Return something that actually happened.
    """
    raise NotImplementedError


def spread(values) -> float:
    """`max / min`. The one number a mean destroys."""
    raise NotImplementedError


def under_provision(values, p: float = 0.95) -> float:
    """`percentile(values, p) / mean(values) - 1`.

    How far wrong you are if you size capacity on the average request. Positive
    means the tail costs more than you planned for, as a fraction.
    """
    raise NotImplementedError


def budget_report(measured: dict[str, float], budget: dict[str, float]) -> dict[str, dict]:
    """Per stage: `measured`, `budget`, `over` (measured - budget), `within`.

    A budget is per stage and not just a total, because a total that passes
    tells you nothing about which stage is about to stop passing.
    """
    raise NotImplementedError


def exceeds(report: dict[str, dict]) -> list[str]:
    """The stages over budget, sorted. Empty is the happy answer."""
    raise NotImplementedError
