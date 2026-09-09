"""Cutting on the document's own boundaries instead of on a word count.

A fixed window is a decision made with no information: cut every 400 words,
wherever that lands. The document already tells you where its ideas end — it has
headings — and using them costs one regex.

It is not free. Real structure gives you units of wildly varying size: in this
corpus the shortest section is **2 words** and the longest is **3,547**, a
spread of more than a thousand times. So structure gets you the boundaries and
you still have to do the sizing, which is what `pack` is for.

Replace each `raise NotImplementedError` with your own code.
"""

from __future__ import annotations

import re

HEADING = re.compile(r"^(\d+(?:\.\d+)*)\.?\s+(\S.*)$")


def heading(line: str) -> tuple[str, str] | None:
    """`("2.3.1", "Access Results")` for a section heading, else None.

    Anchored at the start of the line, so an indented `2.3.1` inside a paragraph
    is not a heading — and in this corpus, indentation is exactly what
    distinguishes them, because RFC body text is indented three spaces and
    headings are not.

    That is a fact about *this* format. Every corpus has an equivalent fact and
    it is never written down anywhere; you find it by reading a document, which
    you did in week 2.
    """
    raise NotImplementedError


def split_sections(text: str) -> list[tuple[str, str, str]]:
    """`(number, title, body)` for each section, body whitespace-collapsed and
    **including its own heading line**.

    Keeping the heading in the body is the cheapest useful thing in this file: a
    chunk that begins `2.4. Caching` carries its own topic, so a query about
    caching matches it on the heading alone. Chunks that were cut at word 400 do
    not know what they are about.

    Text before the first heading becomes a `front matter` section rather than
    being dropped — it is the abstract and the metadata block, and week 2 argued
    about whether to keep it.

    A document with no headings is one section. Handle that; one of these ten is
    close to it.
    """
    raise NotImplementedError


def section_lengths(documents: dict[str, str]) -> list[int]:
    """Word counts of every section in the corpus.

    Print the distribution before you write `pack`. Median 116, minimum 2,
    maximum 3,547, and seventy-one sections under fifty words. **Structure is
    semantically right and dimensionally useless**, and seeing that is what
    makes `pack` obviously necessary rather than an extra step.
    """
    raise NotImplementedError


def pack(sections, min_words: int, max_words: int) -> list[str]:
    """Merge consecutive sections until they reach `min_words`; split any single
    section longer than `max_words` into `max_words` pieces.

    Two rules and one order:

    - a section longer than `max_words` **flushes the buffer first**, then
      splits. Appending it to a half-full buffer and then splitting mixes
      unrelated material into the first piece
    - a section that would push the buffer past `max_words` **also flushes
      first**, so that `max_words` is an invariant of the output rather than an
      aspiration. Without this, merging overshoots — a 131-word buffer plus a
      250-word section is 381 in a corpus configured for 300, and nothing
      complains
    - merging is only ever of *consecutive* sections, so a chunk is always a
      contiguous span of one document

    Raise ValueError unless `0 < min_words <= max_words`.

    Merging adjacent sections is a real compromise and worth naming: section 4
    and section 5 are different topics, and a chunk containing both is less
    focused than either. You are trading that against the alternative, which is
    a two-word chunk that retrieves for nothing.
    """
    raise NotImplementedError


def section_corpus(documents: dict[str, str], min_words: int, max_words: int) -> dict[str, str]:
    """The whole corpus, packed, keyed by `doc#index`. Sorted document order."""
    raise NotImplementedError
