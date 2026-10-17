"""Milestone 14 — guarded, cached, scaled.

One search path through everything this week built, in the only order that is safe:

    1. the guard       refuse an empty or oversized query; redact card numbers and
                       email addresses from the rest. From here on nobody sees them.
    2. the cache       day 2's semantic cache, keyed by the REDACTED text and the
                       reader's groups, guarding identifiers
    3. the shards      day 4's scatter-gather, with shared statistics, top 60
    4. the reader      week 12's filter, then the first k
    5. remember        store the result in the cache, for this reader only

Put the cache before the guard and a card number becomes a cache key. Put the
filter after the cache's fill but key the cache without the reader, and week 12's
leak is back.

Replace each `raise NotImplementedError` with your own code.
"""

from __future__ import annotations


def guarded_search(query: str, groups, *, cache, shards, acl: dict, k: int = 5) -> dict:
    """{"status": "refused" | "cached" | "searched", "results": [chunk ids],
        "problems": <the guard's problems>}"""
    raise NotImplementedError


def scale_report(measured: dict) -> list[str]:
    """One line per number, in this order, for REPORT.md:
        card_false_positives, cache_wrong_answers, graph_share, sharded_drift
    as "<name> <value>", or "<name> not measured"."""
    raise NotImplementedError
