"""Ground truth at the granularity of the thing you are measuring.

Yesterday ended badly. A chunk boundary destroyed an answer, the answer became
unretrievable at any k, and the document-level metric **scored the repair as a
regression**. Nothing about that is fixable with more queries or better
statistics: the instrument measures documents and the system retrieves chunks.

So today the eval set changes. Each answerable query now carries one or more
**answer spans** — short verbatim strings from the corpus that constitute the
answer. `raglab.judgments.Query` holds them, `Query.spans_in` finds them, and
`Query.is_answered_by` requires **all** of them.

They were written by hand, they are quotations rather than paraphrases, and you
can check any of them in fifteen seconds. Argue with them: a span that is too
long makes chunking look worse than it is, and one that is too short makes it
look better.

Replace each `raise NotImplementedError` with your own code.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "day-1"))
from windows import chunk_corpus  # noqa: E402


def carrying_chunks(chunks: dict[str, str], query) -> dict[str, set[str]]:
    """Chunk id → the answer spans that chunk contains. Only chunks with at
    least one.

    Usually one chunk. Sometimes several, when overlap duplicates a span — which
    is worth seeing, because it is the cost of overlap made visible.
    """
    raise NotImplementedError


def survives(chunks: dict[str, str], query) -> bool:
    """Whether **every** span of this query is present in some chunk.

    Every, not any: `r14` needs both halves of a superseded pair, in two
    documents, and neither contains the comparison.

    A query with no spans returns False rather than True. That is deliberate and
    slightly rude: an unanswerable query has nothing to survive, and silently
    counting it as a success would put it in your numerator.
    """
    raise NotImplementedError


def broken_by(chunks: dict[str, str], queries) -> list[str]:
    """Query ids whose answer this chunking destroyed. Sorted.

    **Run this before any retrieval, on every chunking configuration you
    consider.** It costs nothing, it needs no index and no queries executed, and
    it catches the one failure that no amount of downstream work can repair. A
    span not in any chunk is not a ranking problem, a recall problem or a
    prompting problem — the answer has left the index.
    """
    raise NotImplementedError


def answer_recall_at_k(ranked: list[str], chunks: dict[str, str], query, k: int = 5) -> float:
    """1.0 if the top `k` chunks **together** answer the query, else 0.0.

    Together, because that is what a context window does — it concatenates. This
    is the metric the rest of the course uses for chunking decisions, and it is
    binary per query on purpose: a context window either contains the answer or
    it does not, and there is no partial credit for nearly.
    """
    raise NotImplementedError


def mean_answer_recall(rankings, chunks, queries, k: int = 5) -> float:
    """`answer_recall_at_k` averaged over the queries that have spans.

    Queries without spans are excluded rather than scored zero — they are
    unanswerable, and an unanswerable query cannot fail to have its answer
    retrieved.
    """
    raise NotImplementedError


def smallest_overlap_that_saves(documents, query, size: int, limit: int | None = None) -> int | None:
    """The least overlap at which this query's spans all survive, or None.

    Overlap is usually chosen by folklore — "10% is standard" — and it is
    actually answerable: it is a function of your longest answer span and your
    chunk size, and you can compute it. That is not the whole story, because
    tomorrow's structure-aware chunking removes most of the need for it, but it
    is a great deal better than a percentage somebody put in a tutorial.
    """
    raise NotImplementedError
