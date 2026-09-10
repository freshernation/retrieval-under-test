"""What you cannot measure once it is running.

Week 8 produced a report card of ten numbers. Most of them are **unavailable in
production**, because they need answer spans and a live system has no spans — it
has a query it has never seen and an answer nobody has labelled.

That gap is the whole reason this week exists, and it has two possible answers:

    find a signal that correlates with the thing you cannot see     — today
    ask a model to judge                                            — tomorrow

Today first, because it is cheaper, it has no failure modes of its own, and
almost nobody looks.

Replace each `raise NotImplementedError` with your own code.
"""

from __future__ import annotations

OFFLINE_ONLY = "offline only"
SERVING = "available at serving time"


def availability() -> dict[str, str]:
    """Every metric from week 8, classified.

    Write it out by hand. It takes five minutes and the resulting list — the
    things you genuinely cannot compute live — is shorter and more alarming than
    people expect.

    The test to apply to each: *could I compute this for a query I have never
    seen, right now, with no human involved?* Faithfulness passes, because it
    compares the answer to the context and you have both. Groundedness fails,
    because it needs to know what the right answer was.
    """
    raise NotImplementedError


def needs_ground_truth(metrics: dict[str, str]) -> list[str]:
    """The offline-only ones, sorted. The list this week is about."""
    raise NotImplementedError


def auc(good: list[float], bad: list[float]) -> float:
    """The probability that a randomly chosen `good` case scores above a randomly
    chosen `bad` one, with ties at half. In [0, 1].

    This is the right way to ask *"does this signal predict that outcome"*
    without picking a threshold — and picking a threshold first is how a useful
    signal gets discarded for scoring badly at a cutoff nobody chose.

    0.5 is chance. 1.0 is perfect. **And 0.0 is also perfect**, inverted, which
    is why the next function exists.
    """
    raise NotImplementedError


def separation_strength(value: float) -> float:
    """`max(auc, 1 - auc)`: how much the signal separates, ignoring direction.

    A signal with AUC 0.17 is as informative as one with 0.83. Reporting only
    the raw AUC throws away every inverse predictor, and inverse predictors are
    where the surprises live — a signal nobody would think to use, pointing the
    other way.
    """
    raise NotImplementedError


def proxy_report(signals: dict[str, dict[str, float]], truth: dict[str, bool]) -> dict[str, dict]:
    """Per signal: `auc`, `strength`, and `direction` (`higher` or `lower`).

    `direction` is not decoration. A proxy shipped with the sign wrong is worse
    than no proxy, and the sign is not always the one intuition suggests.
    """
    raise NotImplementedError


def useful_proxies(report: dict[str, dict], floor: float = 0.7) -> list[str]:
    """Signals whose separation clears `floor`, sorted.

    The floor is a judgment, not a result. 0.7 is this course's choice and
    nothing derives it — say so wherever you use it.
    """
    raise NotImplementedError
