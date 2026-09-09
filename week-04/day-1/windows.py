"""The unit of retrieval stops being a document.

For three weeks you have retrieved whole documents. That was never going to
survive contact with a language model: the ten documents in this corpus are
31,000 words, and putting the top three in a context window is not a design, it
is a bill.

So you cut them up. Today is the simplest possible way to do that, and the
discovery that **your evaluation cannot see any of it.**

A note on units: `size` here is in **whitespace-separated words**, not model
tokens. Those differ by 20-30% on English prose and by much more on the
identifier-heavy text in this corpus. Week 7 cares about the difference; today
words are what you can count without a model, and a unit you can count by hand
is worth a lot in a week with no ground truth.

Replace each `raise NotImplementedError` with your own code.
"""

from __future__ import annotations

SEPARATOR = "#"


def split_words(text: str) -> list[str]:
    """Whitespace-separated words. Nothing clever, on purpose."""
    raise NotImplementedError


def fixed_windows(text: str, size: int, overlap: int = 0) -> list[str]:
    """Cut `text` into windows of `size` words, advancing by `size - overlap`.

    Rejoin each window with single spaces. That is lossy — the original line
    breaks are gone — and it is what makes a chunk comparable to a query, which
    is also a single line of words.

    Raise `ValueError` for a non-positive size, and for an overlap that is
    negative or at least as large as the size. An overlap equal to the size is
    an infinite loop, and it is the first thing anybody types by accident.

    Empty text gives no windows, not one empty window. A chunk of nothing is a
    chunk your retriever will happily score.
    """
    raise NotImplementedError


def chunk_id(doc_id: str, index: int) -> str:
    """`doc#index`. The chunk must carry its parent, in the id.

    This looks like a detail and it is the whole of station 1 surviving into
    station 2. A chunk with no route back to its document cannot be attributed,
    cannot be cited, and cannot be checked against a supersession graph — and
    every one of those is something you built in week 2 and would silently lose
    here.
    """
    raise NotImplementedError


def parent(chunk: str) -> str:
    """The document id a chunk came from.

    Split on the **last** separator. Document ids can contain `#` and yours will
    one day.
    """
    raise NotImplementedError


def chunk_corpus(documents: dict[str, str], size: int, overlap: int = 0) -> dict[str, str]:
    """Every document, cut up, keyed by chunk id. Iterate documents in sorted
    order so the result is stable."""
    raise NotImplementedError


def to_documents(ranked_chunks: list[str], k: int | None = None) -> list[str]:
    """Ranked chunk ids to ranked document ids, first occurrence wins, no
    duplicates, stopping once `k` documents are collected.

    **This function is where today's lesson lives.** It is how you compare a
    chunk retriever against three weeks of document-level judgments — and in
    doing so it throws away *which* chunk matched, which is the only thing that
    changed. Write it, use it, and then read the last three tests.
    """
    raise NotImplementedError


def coverage(documents: dict[str, str], chunks: dict[str, str]) -> dict[str, float]:
    """Per document, words produced divided by words in the original.

    A sanity check worth having: without overlap this is 1.0 and any other value
    is a bug that silently drops text. With overlap it is above 1.0 and tells
    you exactly what the overlap is costing you in index size.
    """
    raise NotImplementedError
