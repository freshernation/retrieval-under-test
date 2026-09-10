"""raglab — the deterministic harness this course's labs run on.

You use this. You do not build it. It ships finished and green so that every
number you produce is exact, offline, and identical on every machine — which is
the only way `pytest` can grade a retrieval result at all.

    corpus      the shipped documents, and your own once you add them
    judgments   queries, graded relevance judgments, and the dev/test split
    metrics     recall, nDCG, MRR, precision, and a bootstrap confidence interval
    runs        the run ledger: every measurement you have ever taken
    vectors     frozen precomputed embeddings, so week 5 needs no model
    cassette    recorded model responses, so week 8 needs no network
    generator   a stipulated generator, so week 8 needs no model
    judge       a stipulated LLM-as-judge, biased on purpose, for week 9
    text        the token counter the context-budget labs share

Nothing in here retrieves anything. Retrieval is the course.
"""

from raglab import (
    cassette,
    corpus,
    generator,
    judge,
    judgments,
    metrics,
    runs,
    text,
    vectors,
)

__all__ = [
    "cassette",
    "corpus",
    "generator",
    "judge",
    "judgments",
    "metrics",
    "runs",
    "text",
    "vectors",
]
