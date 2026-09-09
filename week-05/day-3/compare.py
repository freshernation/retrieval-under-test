"""Comparing two retrievers, which is harder than improving one.

You now have two systems with similar aggregate scores. The obvious question is
which is better, and today is about why that question does not have an answer at
this sample size — and what to produce instead.

Replace each `raise NotImplementedError` with your own code.
"""

from __future__ import annotations

from collections import Counter, defaultdict

from spans import answer_recall_at_k

BOTH, A_ONLY, B_ONLY, NEITHER = "both", "a only", "b only", "neither"


def head_to_head(a_rankings, b_rankings, chunks, queries, k: int = 5) -> dict[str, str]:
    """Query id → `both`, `a only`, `b only`, or `neither`.

    The whole point of the day is in the shape of this table rather than in any
    mean computed from it. Two systems scoring 0.80 can agree on every query or
    disagree on every query, and those are completely different situations that
    the mean cannot distinguish.

    Skip unanswerable queries, as everything since week 4 does.
    """
    raise NotImplementedError


def tally(table: dict[str, str]) -> dict[str, int]:
    """Counts for all four categories, including the zeros.

    Include the zeros deliberately: `"b only": 0` is a finding, and a dict that
    silently omits it makes the reader do the subtraction.
    """
    raise NotImplementedError


def recall_of(table: dict[str, str], side: str) -> float:
    """`"a"` or `"b"`'s answer recall, recovered from the table."""
    raise NotImplementedError


def oracle_recall(table: dict[str, str]) -> float:
    """What a perfect chooser would score — every query either system gets.

    This is the **ceiling on fusion**, and it is the number week 6 is aimed at.
    If the oracle equals the better system, the two are redundant and combining
    them cannot help however cleverly you do it.
    """
    raise NotImplementedError


def headroom(table: dict[str, str]) -> float:
    """`oracle − max(a, b)`, to 4 decimals.

    The honest way to decide whether to spend a week on fusion. Headroom of zero
    means there is nothing there.
    """
    raise NotImplementedError


def by_family(table: dict[str, str], queries) -> dict[str, dict]:
    """Per query family: `n`, and each side's recall within it.

    A mean over a mixed query set hides that two retrievers can score identically
    and be good at entirely different things — and the family table is the only
    view that shows it.

    **Report `n` for every row.** On this corpus most families have one or two
    queries, which makes the table suggestive and not evidence, and a table
    without `n` invites everyone to forget that.
    """
    raise NotImplementedError


def winner_flips(tables: dict[int, dict[str, str]]) -> bool:
    """Whether the winner changes across a dict of `k` → table.

    If it does, you do not have a better system. You have two systems and a
    parameter, and any sentence of the form "X beats Y" is incomplete without
    the k it was measured at.
    """
    raise NotImplementedError
