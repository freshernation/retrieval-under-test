"""A simulated generator: deterministic, offline, and openly not a language model.

Weeks 8 and 9 need something that turns a context window into an answer. This
course runs offline, so there is no model here — and rather than pretend, this
module is a **stipulated model of a generator**, in exactly the sense week 7
introduced: its *behaviours* are the ones documented in the literature and
observed in practice, and its *implementation* is a hundred lines of rules.

What it reproduces faithfully, because these are the behaviours the week is
about:

- it answers **whatever it is given**, including when the context contains no
  answer, unless refusal is designed in
- it grounds its wording in the retrieved text, so its answers *read* as
  well-supported whether or not they are
- it cites, and its citations are sometimes wrong in the two distinct ways a
  real system's are
- it prefers the highest-ranked context chunk, so a superseded document that
  outranks its replacement produces a confident, fluent, wrong answer

What it does not reproduce: paraphrase, synthesis across chunks, reasoning,
fluency failures, and every emergent behaviour that makes a real model
interesting. **Do not use it to estimate how good your answers will be.** Use it
to test the machinery that checks answers, which is what weeks 8 and 9 build and
which is the part that transfers.

Rule 1 of `EVALS.md` applies to this module as it does to any stipulated model:
assert the direction, never the value.
"""

from __future__ import annotations

import random
import re
from dataclasses import dataclass

_WORD = re.compile(r"[a-z0-9]+")
_SENTENCE = re.compile(r"(?<=[.!?])\s+")

REFUSAL = "I could not find an answer to that in the provided sources."

OVERREACH_SENTENCES = (
    "This behaviour is consistent across all major implementations.",
    "In practice most deployments configure this automatically.",
    "This has been the recommended approach for several years.",
)


def _terms(text: str) -> list[str]:
    return _WORD.findall(text.lower())


def sentences(text: str) -> list[str]:
    """Split into sentence-ish units. Crude, deterministic, and shared by the
    labs so that everyone's faithfulness check counts the same things."""
    parts = [s.strip() for s in _SENTENCE.split(" ".join(text.split()))]
    return [s for s in parts if s]


@dataclass(frozen=True)
class Answer:
    """What the generator returned: the prose, and the ids it cited."""

    text: str
    citations: tuple[str, ...]

    @property
    def sentences(self) -> list[str]:
        return sentences(self.text)


class SimulatedGenerator:
    """A stipulated generator with switchable failure modes.

    Every option defaults to the behaviour a real system exhibits **before
    anybody designs against it**, which is the point: week 8 is about noticing
    that none of this is free.

        refuse_below   score under which it declines. 0.0 means never refuse,
                       which is the default and is what an undesigned system does
        overreach      append a confident sentence supported by nothing
        fabricate      cite a chunk that was not in the context
        misattribute   cite a real, present chunk that does not support the claim
        cite           emit citations at all

    The three citation faults are deliberately **orthogonal**, because they are
    detected by different machinery: `fabricate` by resolving ids, `misattribute`
    by checking support against the cited chunk, `overreach` by checking support
    against anything at all.
    """

    def __init__(
        self,
        *,
        refuse_below: float = 0.0,
        overreach: bool = False,
        fabricate: bool = False,
        misattribute: bool = False,
        cite: bool = True,
        seed: int = 0,
    ) -> None:
        self.refuse_below = refuse_below
        self.overreach = overreach
        self.fabricate = fabricate
        self.misattribute = misattribute
        self.cite = cite
        self.seed = seed

    # -- scoring ------------------------------------------------------------

    def _score(self, query: str, text: str) -> float:
        q = set(_terms(query))
        if not q:
            return 0.0
        return len(q & set(_terms(text))) / len(q)

    def _best_sentences(self, query: str, text: str, limit: int = 2) -> list[str]:
        q = set(_terms(query))
        scored = [
            (len(q & set(_terms(s))), -i, s) for i, s in enumerate(sentences(text))
        ]
        scored.sort(reverse=True)
        chosen = [s for hits, _, s in scored[:limit] if hits > 0]
        return chosen or sentences(text)[:1]

    # -- generation ---------------------------------------------------------

    def answer(self, query: str, context: dict[str, str]) -> Answer:
        """Answer `query` from `context`, a mapping of chunk id to text.

        Deterministic: same query, same context, same answer, on every machine.
        """
        if not context:
            return Answer(REFUSAL, ())

        ranked = sorted(context, key=lambda c: (-self._score(query, context[c]), c))
        best = ranked[0]
        score = self._score(query, context[best])

        if score < self.refuse_below:
            return Answer(REFUSAL, ())

        # Each part carries the id of the chunk it was actually drawn from.
        parts = [(s, best) for s in self._best_sentences(query, context[best])]

        second = ranked[1] if len(ranked) > 1 else None
        if second and self._score(query, context[second]) >= max(0.2, score - 0.2):
            parts += [(s, second) for s in self._best_sentences(query, context[second], limit=1)]

        if self.overreach:
            rng = random.Random(f"{self.seed}:{query}")
            parts.append((rng.choice(OVERREACH_SENTENCES), best))

        if self.misattribute and len(ranked) > 1:
            other = ranked[1]
            parts = [(s, other if src == best else best) for s, src in parts]

        cited = []
        for _, source in parts:
            if source not in cited:
                cited.append(source)

        if self.fabricate:
            rng = random.Random(f"{self.seed}:fab:{query}")
            invented = f"{best.split('#')[0]}#{rng.randrange(900, 999)}"
            parts.append((f"See also the related provisions.", invented))
            cited.append(invented)

        if self.cite:
            text = " ".join(f"{part} [{source}]" for part, source in parts)
        else:
            text = " ".join(part for part, _ in parts)

        return Answer(text, tuple(cited) if self.cite else ())


def is_refusal(text: str) -> bool:
    """Whether an answer declines to answer.

    Deliberately a substring check against one fixed phrase. A real refusal
    detector is a much harder problem — models decline in dozens of phrasings,
    some of them mid-answer — and week 8's exercises say so. Here the phrasing is
    fixed so that the *machinery around it* is what gets tested.
    """
    return REFUSAL.lower() in " ".join(text.lower().split())
