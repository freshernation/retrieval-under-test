"""The analyzer: turning a document into the terms an index will hold.

The fence is lifted. You may change the retriever this week, and today you
change the part of it that runs before any scoring happens.

Today's result is negative, and it is worth knowing that in advance so you do
not conclude you made a mistake: the two classic analyzer improvements —
removing stopwords and stemming — **do not help on this corpus**, and one of
them actively hurts. Finding out why is the arc into day 3.

Replace each `raise NotImplementedError` with your own code.
"""

from __future__ import annotations

import re
from collections import Counter

_SPLIT = re.compile(r"[^a-z0-9]+")

STOPWORDS = frozenset(
    """a an and are as at be but by for from has have how i if in into is it its
    of on or that the their them then there these they this to was what when
    where which who will with you your""".split()
)


def split_terms(text: str) -> list[str]:
    """Lowercase, split on runs of non-alphanumerics, drop empties.

    The same tokeniser as week 1's `normalise`. It is here so that everything
    today is measured against it.
    """
    raise NotImplementedError


def keep_identifiers(text: str) -> list[str]:
    """`split_terms`, plus the compound tokens the split destroyed.

    `utf-8` becomes `utf` and `8`, and `8` appears in nine of ten documents while
    `utf-8` is a term somebody would actually search for. Emit **both** — the
    pieces and the compound — so that a query for either matches.

    Add a token for each match of a letter-digit run (`utf8`, `8259`), a
    digit-letter run, or a hyphenated compound (`utf-8`, `31-day`). Duplicates
    are fine; the index will count them.

    This is additive rather than a replacement, which is a deliberate and
    slightly wasteful choice. Say why you would or would not make it on a corpus
    a thousand times larger.
    """
    raise NotImplementedError


def remove_stopwords(tokens: list[str], stopwords: frozenset[str] = STOPWORDS) -> list[str]:
    """Drop the listed terms."""
    raise NotImplementedError


def stem(token: str) -> str:
    """Crude suffix stripping: `ies` → `y`, then `ing`, `ed`, `es`, `s`.

    Only strip when at least 4 characters would remain, which is the standard
    guard against turning short words into noise.

    It is crude on purpose. Run it over the corpus vocabulary and read the
    output before you believe in it — `status` becomes `statu` and `cookies`
    becomes `cooky`, and `cache` and `caching` still do not match each other.
    A real stemmer is better than this one and makes the same *kind* of mistake.
    """
    raise NotImplementedError


def stem_all(tokens: list[str]) -> list[str]:
    raise NotImplementedError


def analyze(
    text: str,
    stopwords: frozenset[str] | None = STOPWORDS,
    stemming: bool = False,
    identifiers: bool = False,
) -> list[str]:
    """The pipeline: tokenise, optionally drop stopwords, optionally stem.

    **The same analyzer must run over the query and over the documents.** If they
    differ in any way, terms that should match do not, silently, and the failure
    looks exactly like a ranking problem. It is the most common bug in
    hand-built search and it survives code review, because the two call sites
    are usually in different files.
    """
    raise NotImplementedError


def vocabulary(documents: dict[str, str], **options) -> Counter:
    """Every term and how often it occurs across the corpus."""
    raise NotImplementedError


def document_frequency(documents: dict[str, str], **options) -> Counter:
    """Every term and **how many documents** contain it, counted once each.

    This is the number the whole of day 3 is built on, and it is worth staring
    at before you get there. On this corpus `status` appears in 10 documents out
    of 10 and `429` appears in 1 — and a scoring function that treats them
    equally is week 1's, which is the one you are still using.
    """
    raise NotImplementedError
