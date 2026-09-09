"""The context assembler: everything between retrieval and the generator.

Six weeks produced a ranking. A generator needs a **string**, of a size you
chose, containing what it needs, arranged deliberately.

Replace each `raise NotImplementedError` with your own code.
"""

from __future__ import annotations


class ContextAssembler:
    """Shortlist → rerank → diversify → pack → order → assemble.

    Every stage is **optional and off by default**, because this week found that
    two of them cost more than they bought on this corpus. A pipeline whose
    stages default to on is a pipeline nobody measured.

    The config records every stage's setting plus the budget, so that
    `raglab.runs.record` can tell two assemblers apart.
    """

    def __init__(self, retrieve, chunks, budget: int = 800, *, rerank_alpha: float | None = None,
                 mmr_lambda: float | None = None, dedupe_threshold: float | None = None,
                 order: str = "rank", truncate: bool = False, depth: int = 20) -> None:
        raise NotImplementedError

    @property
    def config(self) -> dict:
        raise NotImplementedError

    def build(self, query) -> dict:
        """The assembled context and everything you need to report about it:

            text        the string a generator would receive
            chunks      the ids, in window order
            words       how many words it actually used
            answered    whether every answer span is present
            density     the answer-bearing fraction
            positions   where the answer-bearing chunks landed

        `query` is a `raglab.judgments.Query`, because `answered` and `density`
        need its spans. That makes `build` an **evaluation-time** method — in
        production you have no spans, and the numbers it reports are exactly the
        ones you cannot compute live. Say that in the report rather than
        pretending the pipeline monitors itself.
        """
        raise NotImplementedError


def compare(assemblers: dict[str, "ContextAssembler"], queries) -> dict[str, dict]:
    """Mean `answered`, `density` and `words` per configuration.

    Report all three. A configuration that answers as often for fewer words is
    strictly better; one that answers more often for more words is a point on a
    frontier and needs a requirement to choose between.
    """
    raise NotImplementedError


def regressions(before: dict, after: dict, queries, assembler_before, assembler_after) -> list[str]:
    """Query ids answered by `before` and not by `after`. Sorted.

    Week 6's rule, one stage later: a change that raises the mean while breaking
    a query is a trade, and a trade needs naming.
    """
    raise NotImplementedError
