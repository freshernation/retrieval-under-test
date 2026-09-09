"""Did it beat both?

Yesterday produced a fusion that reaches the oracle at k=3, matches lexical at
k=5 while being strictly worse than it, and captures all the headroom at k=10
only if you abandon the paper's default constant.

Three different verdicts from one technique, and the only way to have any of
them is to compare against **every input**, at **every k you care about**.

The failure this prevents is specific and extremely common: fuse, compare
against the weaker input, report an improvement. The fused system is better than
dense retrieval and worse than the BM25 you already had, and the report says
"hybrid retrieval improved recall by 5 points". Nobody lied.

Replace each `raise NotImplementedError` with your own code.
"""

from __future__ import annotations

from collections import defaultdict

from spans import answer_recall_at_k


def recall(rankings, chunks, queries, k: int) -> float:
    """Mean answer recall over the answerable queries."""
    raise NotImplementedError


def oracle(inputs: dict[str, dict], chunks, queries, k: int) -> float:
    """What a perfect chooser over these inputs would score.

    Takes a **dict of named rankings** rather than two, because there is no
    reason to stop at two retrievers and the arithmetic does not care.
    """
    raise NotImplementedError


def verdict(fused, inputs: dict[str, dict], chunks, queries, k: int) -> dict:
    """The whole judgment, in one dict:

        k, fused, inputs, best_input, beats_all, dilution, oracle, captured

    `beats_all` is **strictly greater than every input**, and it is the field
    that decides whether you ship.

    `dilution` is how far below the best input the fusion fell, floored at zero.
    Mixing a weaker signal into a stronger one costs something, and naming that
    cost is what stops "fusion is free" surviving contact with your data.

    `captured` is the fraction of the available headroom the fusion took —
    `(fused − best) / (oracle − best)` — and it is `None` when there was no
    headroom, because a percentage of nothing is not a number.
    """
    raise NotImplementedError


def by_family(fused, inputs, chunks, queries, k: int) -> dict[str, dict]:
    """Per query family: `n`, the fused recall, and each input's.

    The mean says fusion helped or did not. This says **where**, and on this
    corpus it says something the mean cannot: one family is failing for every
    system at every k, and no fusion of things that both miss it will ever find
    it.
    """
    raise NotImplementedError


def unreachable(inputs, chunks, queries, k: int) -> list[str]:
    """Query ids no input retrieves at `k`. Sorted.

    **The most important list in the week.** These are the queries fusion
    cannot help with by construction — the oracle already excludes them — so
    every point of headroom you chase is a point that is not here, and this list
    is where the remaining failure actually lives.
    """
    raise NotImplementedError
