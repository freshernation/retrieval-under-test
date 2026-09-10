"""How many queries, answered properly.

Week 3 found a *floor*: with six of nine queries unchanged, a bootstrap could
not exclude zero however large the improvement. That was necessary and not
sufficient — it said when measurement is impossible, not when it is reliable.

Today is the sufficient version, and it produces a number you can put in a plan.

Replace each `raise NotImplementedError` with your own code.
"""

from __future__ import annotations

import math
import statistics

Z95 = 1.959963985


def paired_differences(a: dict[str, float], b: dict[str, float]) -> list[float]:
    """Per-query differences over the shared queries, in sorted id order.

    Paired, for week 3's reason: the same queries are hard for both systems, and
    pairing removes that variance. It also means the quantity that matters is
    the spread of the **differences**, not the spread of either system's scores.
    """
    raise NotImplementedError


def paired_sd(a: dict[str, float], b: dict[str, float]) -> float:
    """Standard deviation of those differences. 0.0 for fewer than two.

    This is the number that determines everything below, and on a binary metric
    it is large: a per-query score of 0 or 1 gives differences of −1, 0 or +1,
    and the spread is close to the maximum a bounded quantity can have.

    **Graded metrics need fewer queries than binary ones**, which is an argument
    for nDCG over recall that has nothing to do with which is more meaningful.
    """
    raise NotImplementedError


def mde(n: int, sd: float, z: float = Z95) -> float:
    """Minimum detectable effect: `z * sd / sqrt(n)`.

    The smallest difference a paired comparison at this size can distinguish
    from zero. Compute it **before** running an experiment: if the effect you
    are hoping for is smaller than this, the experiment cannot answer your
    question and running it wastes a week and produces a number somebody will
    quote.
    """
    raise NotImplementedError


def queries_needed(effect: float, sd: float, z: float = Z95) -> int:
    """The `n` at which `effect` becomes detectable: `(z * sd / effect)²`.

    Note the square. Halving the effect you want to detect **quadruples** the
    queries, which is why "we will add a few more queries" is not a plan and why
    small improvements are genuinely expensive to prove.
    """
    raise NotImplementedError


def judge_noise_floor(label_agreement: float) -> float:
    """`1 - label_agreement`: the fraction of labels a judge changes its mind
    about between runs.

    A hard floor that **more queries cannot lower.** If a judge disagrees with
    itself on 10% of cases, a 5-point difference is inside its own noise at any
    sample size — the disagreement is not sampling error, it is the instrument.

    Week 3's floor came from the eval set. This one comes from the judge, and
    the two compose.
    """
    raise NotImplementedError


def detectable(effect: float, n: int, sd: float, label_agreement: float = 1.0) -> bool:
    """Whether `effect` clears **both** floors — sampling, and judge noise.

    Both, because they bind for different reasons and the larger one wins. Adding
    queries fixes one and does nothing to the other.
    """
    raise NotImplementedError


def power_table(sd: float, sizes, effects) -> dict[int, dict[float, bool]]:
    """`n` → effect → detectable. The planning artefact.

    Put it in the report *before* the results. A table showing that your
    experiment could never have detected the effect you are claiming is
    embarrassing after the fact and free beforehand.
    """
    raise NotImplementedError
