"""Project 3 — an agent, and the question of whether it earns its keep.

Four stages, from four days: rewrite the query, route it, hop to a superseding
document, loop until satisfied. **Every one of them defaults to off**, which is
week 7's rule and week 10's rule and now week 11's, for the third time: a stage
nobody switched on deliberately is a stage nobody measured.

The brief is not "build an agent". It is **beat week 8's single-shot pipeline,
measured, and report what it cost.** Those are different briefs and only one of
them can be failed.

You have two things weeks 1 to 10 did not: a cost in retrievals and tokens, and
a minimum detectable effect. Use both. A gain inside the MDE is a gain you did
not measure, however much work went into it.

Replace each `raise NotImplementedError` with your own code.
"""

from __future__ import annotations


class Agent:
    """One query in, one answer and one telemetry dict out.

    `max_iters=1` means no loop, which is the default and is week 8's pipeline
    exactly. Keep it that way: the baseline this is judged against has to be
    runnable from the same object, or the comparison acquires a second variable
    nobody is tracking.
    """

    def __init__(self, shortlist, build_context, generator, chunks, graph, rewrite, *,
                 rewrite_queries: bool = False, hop: bool = False, max_iters: int = 1,
                 stop_at: float = 0.8) -> None:
        raise NotImplementedError

    @property
    def config(self) -> dict:
        """Every dial, and `stop_at` as `None` when there is no loop to stop.

        A config reporting `stop_at=0.8` on a single-shot agent is a config
        claiming a setting that had no effect, and you will find at least one of
        those today.
        """
        raise NotImplementedError

    def answer(self, query):
        """Returns `(answer, context, telemetry)`.

        `telemetry` carries `retrievals`, `iterations`, `churn`, `tokens` and
        `confidence`. Retrievals and tokens are different costs and they do not
        move together — one of this week's stages triples the retrievals and
        leaves the tokens alone, so a cost report in tokens would call it free.
        """
        raise NotImplementedError


def agent_report(agent, queries, chunks, graph) -> dict:
    """`n`, `answered`, `citing_superseded`, `retrievals`, `tokens_per_query`,
    `faithfulness`.

    `citing_superseded` as a sorted id list, because this week has a stage that
    sets it to zero and a different stage that *adds* to it, and counts cannot
    show you that both happened.
    """
    raise NotImplementedError


def verdict(baseline: dict, agent: dict, mde: float = 0.1003) -> dict:
    """The comparison, with week 9's floor applied to it.

    `answered_delta`, `detectable` (is the delta at least the MDE),
    `superseded_fixed`, `superseded_broken`, `retrieval_multiple`,
    `token_multiple`, `tokens_per_extra_answer`.

    `mde` defaults to the figure week 9 measured for this eval set at n=19. It is
    an argument because it is a property of the set, not of the code — change the
    set and this number changes, which nobody ever remembers to do.
    """
    raise NotImplementedError


def ship_check(result: dict) -> list[str]:
    """Reasons to refuse, sorted. Empty means ship.

    Refuse when the answered rate did not improve, when it improved by less than
    the MDE, when the agent costs more retrievals, and when it newly cites a
    superseded document.

    Week 6's `ship_check` refused hybrid retrieval. Week 10's refused a service
    that met every SLO. This one will refuse the best configuration you build,
    and the reason it refuses is the most valuable sentence in Project 3.
    """
    raise NotImplementedError
