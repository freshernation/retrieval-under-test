"""The metrics, and a bootstrap so you can tell a result from a coincidence.

Every function here takes a *ranked list of document ids* and a `Query`, and
returns one number. The ranking is yours; nothing in this module retrieves.

Week 1 makes you implement recall and nDCG yourself before you are allowed to
import these, for the reason that a metric you have not written is a metric you
will misread. After week 1, use these — they are the definition of record, and a
milestone that disagrees with them is wrong by definition rather than
interestingly different.
"""

from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np

from raglab.judgments import RELEVANT_AT, Query, QuerySet


def recall_at_k(ranked: list[str], query: Query, k: int = 10) -> float:
    """Fraction of this query's relevant documents that appear in the top k.

    The station-4 metric. If this is low, nothing you do to the ranker matters,
    because the answer was never in the candidate set.

    A query with no relevant documents returns 0.0 — such a query should not be
    in your eval set at all, and `judgments.check_against` complains about it.
    """
    relevant = query.relevant
    if not relevant:
        return 0.0
    return len(relevant & set(ranked[:k])) / len(relevant)


def precision_at_k(ranked: list[str], query: Query, k: int = 10) -> float:
    """Fraction of the top k that is relevant.

    Reported less often than it should be, and read wrong more often than any
    other metric: when a query has 3 relevant documents, precision@10 cannot
    exceed 0.3, so comparing it across queries compares the judgments rather
    than the retriever.
    """
    if k <= 0:
        return 0.0
    relevant = query.relevant
    return sum(1 for d in ranked[:k] if d in relevant) / k


def mrr(ranked: list[str], query: Query, k: int | None = None) -> float:
    """Reciprocal rank of the first relevant document. 0.0 if there is none.

    Answers 'how far does the user scroll', and answers nothing at all when the
    question needs several documents — which is most interesting questions.
    """
    cut = ranked if k is None else ranked[:k]
    for i, doc_id in enumerate(cut, start=1):
        if query.grade(doc_id) >= RELEVANT_AT:
            return 1.0 / i
    return 0.0


def dcg_at_k(ranked: list[str], query: Query, k: int = 10) -> float:
    """Discounted cumulative gain, with the standard 2^g - 1 gain."""
    total = 0.0
    for i, doc_id in enumerate(ranked[:k], start=1):
        gain = (2 ** query.grade(doc_id)) - 1
        if gain:
            total += gain / math.log2(i + 1)
    return total


def ndcg_at_k(ranked: list[str], query: Query, k: int = 10) -> float:
    """DCG divided by the DCG of the best possible ranking. In [0, 1].

    The station-5 metric. High recall with low nDCG means you found the right
    documents and put them in the wrong order, which is a rerank problem and not
    a retrieval one — the single most useful thing these two numbers do together.
    """
    ideal_grades = sorted(query.judgments.values(), reverse=True)[:k]
    ideal = sum(
        ((2 ** g) - 1) / math.log2(i + 1)
        for i, g in enumerate(ideal_grades, start=1)
        if g > 0
    )
    if ideal == 0:
        return 0.0
    return dcg_at_k(ranked, query, k) / ideal


METRICS = {
    "recall": recall_at_k,
    "precision": precision_at_k,
    "ndcg": ndcg_at_k,
    "mrr": mrr,
}


@dataclass(frozen=True)
class Evaluation:
    """The result of running one retriever over one split."""

    split: str
    n: int
    metrics: dict[str, float]
    per_query: dict[str, dict[str, float]]
    n_unanswerable: int = 0
    """How many queries in this split the corpus cannot answer.

    These are **excluded from every mean in `metrics`**, and kept in
    `per_query` so you can look at them. Including them would be wrong in a way
    that is easy to miss: a query with no relevant document still earns a
    non-zero nDCG for surfacing a grade-1 document, so an unanswerable query
    silently rewards a retriever for confidently returning something. That is
    the exact behaviour the query was added to detect.

    Retrieval metrics cannot score a refusal. What these queries measure is what
    station 6 does with a candidate set that contains no answer, which needs a
    generator and is week 8.
    """

    def worse_than(self, other: "Evaluation", metric: str = "recall@10") -> list[str]:
        """Query ids where this run scores lower than `other`.

        Rule 3 of `EVALS.md` is that you report what got worse. This is how.
        """
        return sorted(
            qid
            for qid, scores in self.per_query.items()
            if qid in other.per_query
            and scores.get(metric, 0.0) < other.per_query[qid].get(metric, 0.0)
        )


def evaluate(
    rankings: dict[str, list[str]],
    queries: QuerySet,
    ks: tuple[int, ...] = (5, 10),
) -> Evaluation:
    """Score a set of rankings. `rankings` maps query id to ranked document ids.

    A query in `queries` with no ranking scores zero rather than being skipped,
    because a retriever that returns nothing for a hard query has not avoided the
    question.

    Queries marked `unanswerable` are scored into `per_query` and **left out of
    every mean**, and counted in `n_unanswerable`. See `Evaluation`.
    """
    splits = {q.split for q in queries}
    if len(splits) > 1:
        raise ValueError(f"evaluate one split at a time, got {sorted(splits)}")
    per_query: dict[str, dict[str, float]] = {}
    scored: set[str] = set()
    for q in queries:
        if not q.unanswerable:
            scored.add(q.id)
        ranked = rankings.get(q.id, [])
        scores: dict[str, float] = {"mrr": mrr(ranked, q)}
        for k in ks:
            scores[f"recall@{k}"] = recall_at_k(ranked, q, k)
            scores[f"precision@{k}"] = precision_at_k(ranked, q, k)
            scores[f"ndcg@{k}"] = ndcg_at_k(ranked, q, k)
        per_query[q.id] = scores
    names = sorted({name for s in per_query.values() for name in s})
    answerable = [s for qid, s in per_query.items() if qid in scored]
    means = {
        name: (sum(s.get(name, 0.0) for s in answerable) / len(answerable))
        if answerable
        else 0.0
        for name in names
    }
    return Evaluation(
        split=next(iter(splits)) if splits else "dev",
        n=len(answerable),
        metrics=means,
        per_query=per_query,
        n_unanswerable=len(per_query) - len(answerable),
    )


def bootstrap(
    a: Evaluation,
    b: Evaluation,
    metric: str = "recall@10",
    iterations: int = 10_000,
    seed: int = 0,
) -> tuple[float, float, float]:
    """Paired bootstrap of `a - b` on the queries they share.

    Returns `(delta, low, high)` — the observed difference in the mean, and a 95%
    confidence interval. **If the interval crosses zero, you did not measure an
    improvement**, however much you would like to have.

    Paired, because the same queries are hard for both systems and pairing
    removes that variance. Seeded, because a confidence interval that moves when
    you rerun it teaches the wrong lesson about confidence.
    """
    shared = sorted(set(a.per_query) & set(b.per_query))
    if not shared:
        raise ValueError("no queries in common")
    xa = np.array([a.per_query[q].get(metric, 0.0) for q in shared], dtype=float)
    xb = np.array([b.per_query[q].get(metric, 0.0) for q in shared], dtype=float)
    diff = xa - xb
    rng = np.random.default_rng(seed)
    idx = rng.integers(0, len(diff), size=(iterations, len(diff)))
    means = diff[idx].mean(axis=1)
    return float(diff.mean()), float(np.percentile(means, 2.5)), float(np.percentile(means, 97.5))
