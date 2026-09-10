"""A simulated LLM-as-judge: deterministic, offline, and biased on purpose.

Week 9 is about whether to trust a model that scores your answers. You cannot
learn that from a judge that is right, so this one is wrong in the ways the
literature documents — and the ways are switchable, so you can measure each one
in isolation.

Like `raglab.generator`, this is a **stipulated model**. Its *base* judgment is
word-overlap support, the same proxy week 8 used. Its *biases* are the ones
reported for real judges:

    length_bias        prefers longer answers, independently of content
    self_preference    prefers answers produced by a familiar generator
    position_bias      in a pairwise comparison, prefers whichever is shown first
    noise              disagrees with itself between runs

Every one defaults to zero. A judge with all four at zero is a word-overlap
metric with a confident voice, which is itself the point: **the authority comes
from the interface, not from the accuracy.**

Assert the direction, never the value.
"""

from __future__ import annotations

import random
import re
from dataclasses import dataclass

_WORD = re.compile(r"[a-z0-9]+")


def _words(text: str) -> set[str]:
    return set(_WORD.findall(text.lower()))


@dataclass(frozen=True)
class Verdict:
    """A judge's output: a score in [0, 1] and the reason it would print."""

    score: float
    reason: str

    @property
    def label(self) -> bool:
        """The binary call, at the conventional midpoint."""
        return self.score >= 0.5


class SimulatedJudge:
    """Scores an answer against a context. Deterministic given its seed."""

    def __init__(
        self,
        *,
        length_bias: float = 0.0,
        self_preference: float = 0.0,
        position_bias: float = 0.0,
        noise: float = 0.0,
        familiar: str = "simulated",
        seed: int = 0,
    ) -> None:
        for name, value in (
            ("length_bias", length_bias),
            ("self_preference", self_preference),
            ("position_bias", position_bias),
            ("noise", noise),
        ):
            if not 0.0 <= value <= 1.0:
                raise ValueError(f"{name} must be between 0 and 1")
        self.length_bias = length_bias
        self.self_preference = self_preference
        self.position_bias = position_bias
        self.noise = noise
        self.familiar = familiar
        self.seed = seed

    def _base(self, answer_text: str, context: dict[str, str]) -> float:
        claim = _words(answer_text)
        if not claim:
            return 1.0
        available = set().union(*(_words(t) for t in context.values())) if context else set()
        return len(claim & available) / len(claim)

    def score(
        self,
        query: str,
        answer_text: str,
        context: dict[str, str],
        *,
        produced_by: str = "simulated",
        run: int = 0,
    ) -> Verdict:
        value = self._base(answer_text, context)
        reasons = ["support"]

        if self.length_bias:
            words = len(answer_text.split())
            bonus = self.length_bias * min(1.0, words / 120.0)
            value += bonus
            reasons.append("length")

        if self.self_preference and produced_by == self.familiar:
            value += self.self_preference
            reasons.append("familiar")

        if self.noise:
            rng = random.Random(f"{self.seed}:{run}:{query}:{answer_text[:40]}")
            value += self.noise * (rng.random() - 0.5)
            reasons.append("noise")

        value = max(0.0, min(1.0, value))
        return Verdict(round(value, 4), "+".join(reasons))

    def compare(
        self,
        query: str,
        first: str,
        second: str,
        context: dict[str, str],
        *,
        run: int = 0,
    ) -> str:
        """Pairwise: returns `"first"`, `"second"` or `"tie"`.

        `position_bias` tilts it towards whichever was shown first, which is the
        effect that makes pairwise judging require running both orders.
        """
        a = self.score(query, first, context, run=run).score + self.position_bias
        b = self.score(query, second, context, run=run).score
        if abs(a - b) < 1e-9:
            return "tie"
        return "first" if a > b else "second"
