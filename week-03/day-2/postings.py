"""The inverted index: from "scan every document" to "look the term up".

Week 1's retriever re-analyses all ten documents on every query. At ten
documents that is instant and at ten million it is a career-limiting decision.

An inverted index turns the loop inside out: instead of *document → terms*, hold
*term → documents*. Everything a scoring function needs — how often a term
occurs in a document, how many documents contain it, how long each document is —
becomes a lookup, and day 3's arithmetic becomes possible.

`day-1/analyzer.py` is importable. Do not reimplement `analyze`.

Replace each `raise NotImplementedError` with your own code.
"""

from __future__ import annotations

import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "day-1"))
from analyzer import analyze  # noqa: E402


class Index:
    """Term → document → positions, plus the statistics day 3 needs.

    Store **positions**, not just counts. They cost memory — this is the single
    biggest line item in a real index — and they buy phrase search, which
    nothing else can do. Knowing what you are paying for is the point of
    building it rather than importing it.
    """

    def __init__(self, documents: dict[str, str], **options) -> None:
        """Analyse every document once and record, per term: which documents
        contain it and at which token positions.

        Keep `options` so that `analyze_query` can use **exactly** the same
        analyzer. An index that was built with stemming and is queried without
        it silently matches nothing, and that bug is invisible from the outside.
        """
        raise NotImplementedError

    @property
    def n_documents(self) -> int:
        raise NotImplementedError

    @property
    def vocabulary_size(self) -> int:
        raise NotImplementedError

    @property
    def average_length(self) -> float:
        """Mean document length in tokens. 0.0 for an empty index.

        Day 3's `b` parameter is entirely about this number, so it is worth
        looking at the spread behind it now: the longest document here is more
        than fifteen times the shortest.
        """
        raise NotImplementedError

    def postings(self, term: str) -> dict[str, list[int]]:
        """Document id → positions, for one term. Empty dict if unknown."""
        raise NotImplementedError

    def term_frequency(self, term: str, doc_id: str) -> int:
        """How many times a term occurs in a document."""
        raise NotImplementedError

    def document_frequency(self, term: str) -> int:
        """How many documents contain a term. **The number day 3 is built on.**"""
        raise NotImplementedError

    def analyze_query(self, query: str) -> list[str]:
        """Analyse a query with the index's own options. Use this rather than
        calling `analyze` — it is what makes the two sides agree by construction
        instead of by remembering."""
        raise NotImplementedError

    def total_postings(self) -> int:
        """Total term-document pairs. The size of the index, roughly."""
        raise NotImplementedError


def search_or(index: Index, query: str) -> dict[str, int]:
    """Documents containing any query term, mapped to how many distinct terms
    they contain.

    This is week 1's scorer, reached by lookup rather than by scanning. It
    returns the same ranking — which is worth confirming, because "I made it
    faster" and "I made it different" are things you must be able to tell apart.
    """
    raise NotImplementedError


def search_and(index: Index, query: str) -> set[str]:
    """Documents containing **every** query term.

    Precise, and brittle in a specific way: one unusual word in a five-word
    question empties the result set, and the user cannot tell which word did it.
    This is why boolean search lost, and it is worth having built the thing that
    lost.
    """
    raise NotImplementedError


def phrase(index: Index, query: str) -> set[str]:
    """Documents containing the query terms **adjacent and in order**.

    This is what the positions were for. **Carry a set of candidate start
    positions** through the query and intersect it term by term: start with the
    positions of the first term, then for each later term at offset `i`, keep
    only the starts `s` for which that term occurs at `s + i`.

    The trap, which caught this course's own reference solution: it is not enough
    to check each term against the first term's positions *independently*. Do
    that and a document containing `pot` at 40 with `of` at 41, and `pot` at 900
    with `coffee` at 902, matches the phrase `pot of coffee` — which it does not
    contain. Every term found a start that worked; no single start worked for
    every term. The bug produces plausible extra results and no error.

    On this corpus `too many requests` matches exactly one document, where the
    boolean OR ties two and AND returns both. Phrase search is the sharpest tool
    in the lexical box and the most fragile — it needs the user to have used the
    document's exact wording, which they usually have not.
    """
    raise NotImplementedError
