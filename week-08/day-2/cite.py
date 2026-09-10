"""Citations, and the two different things wrong with them.

An answer with a citation reads as verifiable. Whether it *is* verifiable is a
separate question with two separate parts, and they fail independently:

    the citation points at nothing        — the id is not a chunk, or not one
                                            that was in this context
    the citation points at the wrong thing — the id is real and present, and the
                                            text it names does not support the
                                            claim

Today is the first. Tomorrow is the second, and it is much harder.

Replace each `raise NotImplementedError` with your own code.
"""

from __future__ import annotations

import re

from raglab.generator import is_refusal, sentences

CITATION = re.compile(r"\[([^\[\]\s]+)\]")


def parse_citations(text: str) -> list[str]:
    """Cited ids, first-seen order, deduplicated.

    Order-preserving because it is evidence: a citation attaches to the sentence
    it follows, and losing the order loses which claim each one was for.
    """
    raise NotImplementedError


def strip_citations(text: str) -> str:
    """The prose with the markers removed and whitespace normalised.

    Needed because every downstream check — support, length, readability — must
    look at what was *claimed*, and `[rfc-6585#4]` is not a claim.
    """
    raise NotImplementedError


def cited_sentences(text: str) -> list[tuple[str, list[str]]]:
    """Each sentence as `(prose, citations in it)`.

    The unit that matters. An answer-level citation list tells you the answer
    drew on four chunks; it does not tell you **which chunk supports which
    claim**, and that is the only question worth asking.

    There is a trap here and it is worth getting right rather than around. A
    citation follows the sentence it supports, so it comes **after** the full
    stop — and a sentence splitter therefore puts it at the *start of the next
    sentence*. Split naively and every citation is attached to the following
    claim, which is off by one for the entire answer and produces a support
    check that is wrong everywhere while looking fine.

    Pull leading markers back onto the sentence before them.
    """
    raise NotImplementedError


def uncited_sentences(text: str) -> list[str]:
    """Sentences carrying prose and no citation.

    Not automatically wrong — a summarising sentence may legitimately cite
    nothing — and it is exactly where an unsupported claim hides, because there
    is no citation to check it against.
    """
    raise NotImplementedError


def chunk_citations(text: str, chunks) -> list[str]:
    """Only the parsed ids that are actually chunks.

    You will need this and the reason is the day's best surprise. The corpus is
    full of bracketed cross-references — `[RFC2119]`, `[RFC3629]` — and the
    generator quotes sentences containing them. A parser that treats every
    `[...]` as a citation therefore reports **fabricated citations for a
    generator that never fabricated one**, at a rate of about one answer in four.

    You would have blamed the model. The bug is in your checker, and it is
    sourced from the corpus.

    The real fix is upstream: **make the citation marker something the corpus
    cannot contain.** Until then, resolve against the chunk ids and know that you
    are papering over an ambiguity rather than removing it.
    """
    raise NotImplementedError


def unresolvable(citations, chunks) -> list[str]:
    """Cited ids that are not chunks at all. Sorted.

    The crude failure: an id that never existed. Trivial to detect, and worth
    detecting first because a system doing this is broken in a way no amount of
    prompt work fixes.
    """
    raise NotImplementedError


def not_in_context(citations, context) -> list[str]:
    """Cited ids that exist but were not in **this** context. Sorted.

    The subtle one. The id resolves, the chunk is real, a reader who follows the
    link sees plausible text — and the generator never saw it, so whatever it
    said was not drawn from there.

    A retrieval-augmented system citing something it was not given is not
    grounded, however plausible the pairing looks.
    """
    raise NotImplementedError


def citation_report(answers, contexts, chunks) -> dict:
    """`citations`, `not_in_context`, `unresolvable`, `sentences`,
    `uncited_sentences`, over every non-refusal answer.

    Skip refusals. A refusal cites nothing and counting it as perfectly cited
    would let a system that declines everything report flawless attribution.
    """
    raise NotImplementedError
