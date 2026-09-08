"""The milestone plumbing: run your own eval set, and audit it.

The three functions below are small. The one that matters is
`unjudged_in_top_k`, and it is the one people skip.

Replace each `raise NotImplementedError` with your own code.
"""

from __future__ import annotations

from pathlib import Path

from raglab.judgments import Query, QuerySet


def read_queries(path: str | Path) -> QuerySet:
    """Load a `queries.yml` you wrote yourself into a `QuerySet`.

    Same schema as `data/gold/sample/queries.yml`: a top-level `queries:` list of
    entries with `id`, `text`, `split`, and a `judgments` mapping of document id
    to grade.

    Validate as you load — an unknown split, a grade outside 0..3, or a duplicate
    query id should raise `ValueError` here rather than produce a quietly wrong
    number in three days' time.
    """
    raise NotImplementedError


def search_all(
    queries: QuerySet, documents: dict[str, str], rank_fn, k: int = 10
) -> dict[str, list[str]]:
    """Run `rank_fn(query_text, documents, k)` over every query.

    Returns query id to ranked document ids. `rank_fn` is day 4's `rank`, passed
    in rather than imported so that week 3 can hand this the same thing with a
    different scorer and get a comparable number.
    """
    raise NotImplementedError


def unjudged_in_top_k(
    rankings: dict[str, list[str]], queries: QuerySet, k: int = 10
) -> dict[str, list[str]]:
    """Documents the retriever put in the top k that you never judged at all.

    Return only the queries that have any, mapping query id to the unjudged
    document ids in rank order.

    **This is the audit that matters.** Every one of these scored 0 in your
    metrics, silently, because unjudged means irrelevant. Some of them are
    genuinely irrelevant. Some are documents you would have graded 2 or 3 if you
    had looked — and for those, your retriever was punished for being right.

    You cannot fix this by judging everything; the corpus is too big, and on a
    real corpus it is hopeless. What you can do is look at this list every time
    you change a retriever, judge what turns up, and know that your eval set is
    biased towards the systems that helped build it. Every published retrieval
    benchmark has this problem and most of them do not mention it.
    """
    raise NotImplementedError


def judged_coverage(queries: QuerySet, corpus_ids: set[str]) -> float:
    """Fraction of the corpus that carries at least one judgment, from any query.

    A number to state in the report and be uncomfortable about. On the sample
    corpus a thorough week-1 eval set reaches perhaps half. On a real corpus it
    will be far below one percent, and every claim you make rests on it.
    """
    raise NotImplementedError
