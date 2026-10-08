"""The control loop: retrieve, judge, rewrite, repeat.

This is the shape every agent framework draws. A model inspects what came back,
decides it is not good enough, rewrites, and goes again — and stops when it is
satisfied or when somebody capped it.

Three things make or break it and none of them is the model:

    the stopping condition      what counts as satisfied
    the cap                     what happens when it never is
    the cost                    which multiplies by the iteration count

Week 10 made the third one measurable, which is the only reason this day can be
honest. A loop that retrieves three times costs three times as much, and before
week 10 that sentence had no number in it.

Replace each `raise NotImplementedError` with your own code.
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class Run:
    """One query's trip through the loop.

    `confidences` and `shortlists` are per iteration, which is what makes the
    loop auditable: a run that reports only its final context cannot be asked
    whether the iterations did anything.
    """

    query_id: str
    context: dict[str, str] = field(default_factory=dict)
    retrievals: int = 0
    confidences: tuple[float, ...] = ()
    shortlists: tuple[tuple[str, ...], ...] = ()

    @property
    def iterations(self) -> int:
        raise NotImplementedError

    def capped(self, max_iters: int) -> bool:
        """Whether it stopped because it ran out of iterations rather than
        because it was satisfied. `max_iters` is passed in: a run does not know
        its own cap, and should not."""
        raise NotImplementedError


class Loop:
    """`stop_at` and `max_iters` are both required reading.

    `stop_at` is a threshold on a serving-time signal, because a stopping
    condition that needs ground truth is not a stopping condition — it is a
    measurement you can only make afterwards. Week 9's retrieval confidence is
    the only candidate this course has.

    `max_iters` is not a safety net. It is the **only** thing that terminates a
    loop on a query the corpus cannot answer, and day 4's out-of-scope query will
    run to whatever number you put there.
    """

    def __init__(self, shortlist, build_context, rewrite, *, stop_at: float = 0.8,
                 max_iters: int = 3) -> None:
        raise NotImplementedError

    def run(self, query_id: str, query_text: str) -> Run:
        """Iterate until the confidence of the **original** query against the
        context clears `stop_at`, or the cap.

        The original query, not the rewritten one. Scoring the rewritten query
        against a context retrieved *for* the rewritten query is a loop grading
        its own homework, and it will terminate early and confidently.

        Keep the best context seen, not the last. The last iteration is the one
        that failed to clear the bar.
        """
        raise NotImplementedError


def histogram(runs) -> dict[int, int]:
    """How many queries stopped at each iteration count.

    Read it before anything else. The shape of this distribution says whether
    the loop has more than two outcomes.
    """
    raise NotImplementedError


def cost_multiple(runs) -> float:
    """Retrievals over queries. One means you did not loop."""
    raise NotImplementedError


def churn(run: Run) -> int:
    """Iterations where the shortlist changed and the confidence did not improve.

    The number that distinguishes progress from motion. A loop can produce a
    different candidate set every time and get no closer, and nothing about the
    candidate set changing is evidence that it is working.
    """
    raise NotImplementedError


def loop_report(runs, answered: dict[str, bool], max_iters: int) -> dict:
    """`answered`, `retrievals`, `cost_multiple`, `iterations`, `capped`.

    `capped` is a sorted list of query ids, not a count. Which queries exhausted
    the loop is the most useful line in the report.
    """
    raise NotImplementedError
