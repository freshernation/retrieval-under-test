"""Faithfulness, and the thing it is not.

Yesterday checked that a citation **points** somewhere real. Today checks that
what it points at **says what the sentence claims** — the second and harder
citation failure.

And then the day's real content: a system can score **perfectly** on
faithfulness and be wrong, and this corpus contains the case.

## The support check is a proxy and you must say so

Real faithfulness is entailment: does this claim follow from that passage? That
needs a model, and week 9 is about whether to trust one for it.

Today's `support` is **word overlap** — what fraction of a claim's words appear
in its source. It catches copied text and blatant invention. It cannot catch a
negation, a swapped number, or a paraphrase. Report it as what it is.

Replace each `raise NotImplementedError` with your own code.
"""

from __future__ import annotations

import re

from cite import chunk_citations, cited_sentences
from raglab.generator import is_refusal

_WORD = re.compile(r"[a-z0-9]+")


def content_words(text: str) -> set[str]:
    """Lowercase alphanumeric words, as a set."""
    raise NotImplementedError


def support(claim: str, source: str) -> float:
    """Fraction of the claim's words present in the source. In [0, 1].

    An empty claim is 1.0 — vacuously supported — rather than 0.0, so that a
    stray empty fragment does not drag an answer's score down.

    Note what this rewards: **copying**. A generator that quotes verbatim scores
    1.0, and one that paraphrases correctly scores lower. That is backwards as a
    measure of quality and it is exactly why this is a proxy.
    """
    raise NotImplementedError


def best_support(claim: str, sources) -> float:
    """The highest support over several sources. 0.0 for none."""
    raise NotImplementedError


def sentence_verdicts(answer, context, chunks, threshold: float = 0.8):
    """Per sentence: `claim`, `citations`, `support`, `supported`, `basis`.

    `basis` records **what the claim was checked against**, and it is the field
    that keeps this honest:

    - `cited` — it named chunks that were in the context; checked against those
    - `context` — it named chunks, none of them present; checked against the
      whole context, which is generous
    - `uncited` — it named nothing; checked against the whole context

    Checking an uncited sentence against the entire window is the lenient
    choice. A stricter system would score it zero, on the grounds that an
    unattributed claim is unverifiable by a reader. Pick one deliberately and
    write down which.
    """
    raise NotImplementedError


def faithfulness(answer, context, chunks, threshold: float = 0.8) -> float:
    """Fraction of an answer's sentences that clear the threshold.

    **A refusal returns 1.0**, and it needs an explicit check rather than falling
    out of the arithmetic: "I could not find an answer" is a sentence, it shares
    almost no words with the context, and a naive implementation scores it 0.0 —
    punishing a system for the one behaviour week 8 is trying to encourage.

    A refusal makes no claim about the corpus, so it cannot be unfaithful to it.
    It is also why the aggregate below must *exclude* refusals rather than
    average them in at 1.0.
    """
    raise NotImplementedError


def faithfulness_rate(answers, contexts, chunks, threshold: float = 0.8) -> float:
    """Mean faithfulness over non-refusal answers.

    Excluding refusals is not a detail. Include them and a system that declines
    everything scores a perfect 1.0, which is the single easiest way to game any
    faithfulness metric and it is not hypothetical.
    """
    raise NotImplementedError


def cites_superseded(answer, chunks, graph) -> list[str]:
    """Cited chunks whose parent document something supersedes. Sorted.

    Week 2's supersession graph, six weeks later, at the last station. This is
    the check that catches what faithfulness cannot: an answer perfectly
    supported by a document that was withdrawn in 2017.

    It is not a faithfulness metric and it does not belong inside one. It is a
    **currency** check, it needs metadata rather than text, and the fact that it
    lives outside the faithfulness machinery is the point of the day.
    """
    raise NotImplementedError
