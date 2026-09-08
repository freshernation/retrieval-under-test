"""The metrics, written by hand once so you can never misread one again.

`raglab.metrics` already contains all of these. You are writing them anyway,
because a metric you have not implemented is a metric you will quote without
knowing what it hides — and every one of these hides something specific.

From tomorrow, use `raglab.metrics`. It is the definition of record.

Every function takes `ranked`, a list of document ids best-first, and
`judgments`, a dict of document id to grade. A document not in `judgments` is
graded 0.

Replace each `raise NotImplementedError` with your own code.
"""

from __future__ import annotations

import math

RELEVANT_AT = 2


def grade(judgments: dict[str, int], doc_id: str) -> int:
    """The grade for a document, 0 if it was never judged.

    Read that default twice. It says an unjudged document is irrelevant, which
    is false often enough to matter on a hand-built set: a retriever that finds
    a genuinely good document nobody labelled is punished for it, and the better
    your retriever gets the more often this happens.
    """
    raise NotImplementedError


def recall_at_k(ranked: list[str], judgments: dict[str, int], k: int = 10) -> float:
    """Fraction of this query's relevant documents inside the top k.

    The station-4 metric. When this is low, nothing you do downstream matters.

    Returns 0.0 when the query has no relevant documents — such a query should
    not be in an eval set, which is what yesterday's `smells` was for.
    """
    raise NotImplementedError


def precision_at_k(ranked: list[str], judgments: dict[str, int], k: int = 10) -> float:
    """Fraction of the top k that is relevant.

    Divide by `k`, not by the length of `ranked`. A retriever that returns three
    documents and gets all three right has not achieved precision@10 of 1.0 — it
    left seven slots empty, and the metric should say so.
    """
    raise NotImplementedError


def reciprocal_rank(ranked: list[str], judgments: dict[str, int]) -> float:
    """1/rank of the first relevant document, 1-indexed. 0.0 if there is none.

    Answers "how far does the user scroll". Answers nothing about a question
    that needs three documents, which is most interesting questions.
    """
    raise NotImplementedError


def dcg_at_k(ranked: list[str], judgments: dict[str, int], k: int = 10) -> float:
    """Discounted cumulative gain over the top k.

        sum over positions i (1-indexed) of  (2**grade - 1) / log2(i + 1)

    Two decisions are baked into that formula and both are conventions rather
    than truths: the exponential gain says a grade 3 is worth seven times a
    grade 1, and the log discount says position 1 is worth 1.58 times position
    3. Neither was derived from user behaviour. They are what the field settled
    on, and you should know they are choices.
    """
    raise NotImplementedError


def ndcg_at_k(ranked: list[str], judgments: dict[str, int], k: int = 10) -> float:
    """DCG divided by the DCG of the best possible ranking of these judgments.

    In [0, 1], which is the entire reason it exists — raw DCG cannot be averaged
    across queries because a query with five relevant documents has a bigger
    ceiling than one with two.

    Returns 0.0 when the ideal DCG is 0.
    """
    raise NotImplementedError


def average_precision(ranked: list[str], judgments: dict[str, int]) -> float:
    """Mean of precision@i taken at each position i holding a relevant document,
    divided by the number of relevant documents.

    The metric TREC actually reports, and the one nobody in RAG uses. It rewards
    finding *all* the relevant documents early, where MRR stops caring after the
    first. Worth having in your hands when you read an IR paper.
    """
    raise NotImplementedError


def mean_over_queries(
    metric, rankings: dict[str, list[str]], judgments_by_query: dict[str, dict[str, int]], **kwargs
) -> float:
    """Apply `metric` to every query and average.

    A query with no ranking scores whatever the metric gives an empty list —
    zero — rather than being skipped. A retriever that returns nothing for the
    hard queries has not avoided them, and a mean computed only over the queries
    a system answered is the most common dishonest number in this field.
    """
    raise NotImplementedError


def paired_bootstrap(
    scores_a: dict[str, float],
    scores_b: dict[str, float],
    iterations: int = 10_000,
    seed: int = 0,
) -> tuple[float, float, float]:
    """Resample the per-query differences and report `(delta, low, high)` at 95%.

    Paired: take the difference per query first, then resample the differences.
    The same queries are hard for both systems, and pairing removes that shared
    variance — an unpaired bootstrap on eight queries will tell you nothing is
    ever significant.

    Use `random.Random(seed)` so the interval does not move when you rerun it.
    A confidence interval that changes on every run teaches exactly the wrong
    lesson about confidence.

    **If the interval contains zero, you did not measure an improvement.**
    """
    raise NotImplementedError
