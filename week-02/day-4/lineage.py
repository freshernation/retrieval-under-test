"""Provenance: going and getting the metadata the text will not give you.

Yesterday ended at a wall. Two pairs of documents in this corpus stand in
exactly the same relationship — one obsoletes the other — and their textual
similarity is 0.547 and 0.185. No threshold separates that relationship from
coincidence, because **supersession is not a property of the text.**

It is written down, though. Every RFC carries a header block, and the header of
the *newer* document names the one it replaces. Today you go and read it.

This is the day where looking at the corpus buys something that no amount of
retrieval work could have produced, which is the argument for station 1.

Replace each `raise NotImplementedError` with your own code.
"""

from __future__ import annotations

import re

HEADER_LINES = 16


def parse_header(text: str) -> dict:
    """The metadata block at the top of an RFC.

    Return `rfc`, `obsoletes` (list of ints), `updates` (list of ints),
    `category`, `date` ("Month YYYY"), and `year` (int). Use `None` and `[]` for
    what is absent — and things are absent, on purpose, in this corpus.

    Only look at the first `HEADER_LINES` lines. Four traps, all real, all in
    front of you:

    - **The layout is not fixed.** The date is right-aligned on the `Request for
      Comments:` line in one document, on the `Obsoletes:` line in another, and
      alone on line 12 in a third
    - **Author names share the line.** `Category: Standards Track       G. Illyes`
      is a category of "Standards Track", not "Standards Track G. Illyes". Two or
      more spaces is the column separator
    - **The window is a guess.** RFC 3986 carries `STD`, `Updates` *and*
      `Obsoletes`, which pushes its date to line 12. A twelve-line window works
      on nine documents and loses the date on the one with the most metadata,
      which is exactly the wrong one to lose it on
    - **One document starts with a byte-order mark**, and one dates itself
      "1 April 1998", day first

    Every one of these is what "just parse the header" means on a real corpus.
    """
    raise NotImplementedError


def supersession(documents: dict[str, str]) -> dict[str, str]:
    """Map each obsolete document to the one that replaced it.

    Built from the *newer* document's `Obsoletes:` line, because that is the only
    place the fact exists — an RFC is never edited after publication, so RFC 7159
    will never mention RFC 8259. **The information that makes a retrieved passage
    wrong lives in a different document.** Nothing in the passage warns you, and
    nothing ever will.

    Ignore obsoleted numbers that are not in the corpus. RFC 7159 obsoletes 4627
    and 7158, which you do not have, and a KeyError here would be a crash caused
    entirely by a document being absent.
    """
    raise NotImplementedError


def is_current(doc_id: str, graph: dict[str, str]) -> bool:
    """Whether nothing in the corpus obsoletes this document."""
    raise NotImplementedError


def current_version(doc_id: str, graph: dict[str, str]) -> str:
    """Follow the chain to the newest version. Returns `doc_id` if it is current.

    Chains are real — 4627 → 7158 → 7159 → 8259 is four documents — so follow
    until you stop, do not take one step. Raise `ValueError` on a cycle: it
    should be impossible, it costs three lines to detect, and an infinite loop
    inside an ingest job is a very expensive way to find out you were wrong.
    """
    raise NotImplementedError


def annotate(ranked: list[str], graph: dict[str, str]) -> list[tuple[str, str | None]]:
    """Pair each result with the document that supersedes it, or `None`.

    The minimum honest thing to do with this knowledge, and it is worth noticing
    that it is not a ranking change at all — it is a change to what the answer
    is allowed to say. Week 8 turns this into a citation that carries a warning.
    """
    raise NotImplementedError


def demote_superseded(ranked: list[str], graph: dict[str, str]) -> list[str]:
    """Move every superseded document below every current one, order preserved
    within each group.

    Demote rather than drop. The obsolete document is the only answer to "what
    changed", and query r14 in the held-out split needs both halves of the pair —
    so removing it would trade one failure for another and the mean might not
    even notice.
    """
    raise NotImplementedError
