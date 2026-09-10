"""An eval harness, and a gate that guards it.

Nine weeks of measurements, in one runnable thing that a machine can execute on
every change and a person can read on a Monday.

Replace each `raise NotImplementedError` with your own code.
"""

from __future__ import annotations


class EvalSuite:
    """Everything measured about one configuration, in one call.

    The suite owns the **contexts**: it builds them once and hands the same ones
    to every check. A harness that rebuilds retrieval per metric can report a
    faithfulness computed against a context the generator never saw, and the
    numbers will look completely normal.
    """

    def __init__(self, answerer, queries, chunks, graph) -> None:
        raise NotImplementedError

    def run(self) -> dict:
        """The full report: week 8's card, plus this week's additions.

            card             the week-8 report card
            proxies          serving-time signals and their separation
            power            sd, n, mde, and what is detectable
            judge            accuracy, kappa, baseline kappa, self-agreement

        `judge` is reported **with its baseline**, always. A judge's accuracy
        without the constant-baseline accuracy next to it is a number that
        cannot be interpreted, and this week found one that matched it exactly.
        """
        raise NotImplementedError


def guarded_metrics(report: dict) -> dict[str, float]:
    """The flat metric dict a gate consumes, pulled out of a nested report.

    Keep it small. The compounding arithmetic says ten guarded metrics fire
    spuriously two times in five, so guard only the ones whose regression you
    would actually roll back for — and let the rest be reported.
    """
    raise NotImplementedError


def regression_check(baseline: dict, candidate: dict, gate) -> dict:
    """Run the gate over two reports. Adds `detectable`, per failing metric.

    **`detectable` is the field that makes a gate honest.** A failure smaller
    than the minimum detectable effect is a coin flip reported as a regression,
    and a gate that cannot say which of its failures are real will be muted.
    """
    raise NotImplementedError


def summary(report: dict) -> list[str]:
    """The lines a person reads on Monday, in order of what would change a
    decision. Sorted is wrong here — **ranked** is right.

    First anything that would block a release. Then anything the eval set cannot
    measure. Then the numbers. A summary that opens with a metric is a summary
    nobody finishes.
    """
    raise NotImplementedError
