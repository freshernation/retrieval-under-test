"""Refusal, which does not happen on its own.

Twenty queries, twenty answers, zero refusals — including the out-of-scope one
and the two nothing retrieves. That is the default behaviour of every generation
system before somebody designs against it, and today you design against it.

The instrument you need already exists: **answer spans**, from week 4. They let
you say, per query, whether the context contained the answer — so you can score
a refusal as right or wrong rather than merely counting them.

Replace each `raise NotImplementedError` with your own code.
"""

from __future__ import annotations

import re

from raglab.generator import SimulatedGenerator, is_refusal

_WORD = re.compile(r"[a-z0-9]+")

ANSWERED_RIGHT = "answered_right"
ANSWERED_WRONG = "answered_wrong"
REFUSED_RIGHT = "refused_right"
REFUSED_WRONG = "refused_wrong"


def confidence(query_text: str, context: dict[str, str]) -> float:
    """A confidence signal: the best chunk's query-term coverage, in [0, 1].

    Crude on purpose, and it is the **only** signal available at serving time.
    Everything else you have measured this week — groundedness, faithfulness,
    correctness — needs answer spans, and in production there are none.

    That asymmetry is the whole difficulty of refusal: the decision must be made
    from what you can see, and what you can see is much less than what you can
    measure offline.
    """
    raise NotImplementedError


def has_answer(query, context: dict[str, str]) -> bool:
    """Whether the context contains every answer span. False when there are none."""
    raise NotImplementedError


def outcome(query, context, answer) -> str:
    """One of the four constants above.

    The four-way table is the point. Counting refusals tells you nothing —
    refusing everything and refusing nothing both produce a single number — and
    only splitting by whether the answer was actually there makes a refusal
    scorable.
    """
    raise NotImplementedError


def outcomes(answers, queries, contexts) -> dict[str, int]:
    """The four counts, all four keys always present, zeros included."""
    raise NotImplementedError


def frontier(queries, contexts, thresholds) -> dict[float, dict[str, int]]:
    """Threshold → outcome counts. The trade, measured.

    Sweep it. There is a region where refusal is **free** — wrong answers
    removed, right answers kept — and a point past which every further refusal
    costs you a correct answer. Nobody can tell you where that point is on your
    corpus and it takes a minute to find.
    """
    raise NotImplementedError


def free_threshold(points: dict[float, dict[str, int]]) -> float:
    """The **highest** threshold that still keeps every correct answer.

    Highest, not lowest: among the settings that cost nothing, take the one that
    refuses most. Below it you are declining to use information you have.
    """
    raise NotImplementedError


def separation(points_present_and_absent, contexts) -> dict:
    """`min_present`, `max_absent`, `overlaps`.

    The honest limit of the whole exercise. If the lowest confidence among
    queries whose answer *was* present is below the highest among those where it
    was not, **no threshold separates them** — every setting trades one kind of
    error for the other, and the frontier is all there is.

    Report `overlaps`. A refusal policy presented without it implies a
    separation that does not exist.
    """
    raise NotImplementedError
