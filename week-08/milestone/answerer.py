"""Project 2 — the whole pipeline, and the report card that grades it.

Seven stations, end to end: a query goes in, prose with citations comes out, and
**every claim the system makes about itself is checked by machinery you wrote.**

Replace each `raise NotImplementedError` with your own code.
"""

from __future__ import annotations


class Answerer:
    """Assemble a context, generate, and apply a refusal policy.

    The config carries the assembler's config plus `refuse_below` and the
    generator's flags, because a report that does not say which generator
    produced its numbers is not reproducible — and the flags are the difference
    between a faithfulness of 1.00 and one of 0.09.
    """

    def __init__(self, assembler, generator, *, refuse_below: float = 0.0) -> None:
        raise NotImplementedError

    @property
    def config(self) -> dict:
        raise NotImplementedError

    def context_for(self, query) -> dict[str, str]:
        """The chunk-id-to-text mapping the generator will actually see."""
        raise NotImplementedError

    def answer(self, query):
        """Returns `(Answer, context)`.

        Return the context as well as the answer. Every check in this week needs
        it, and a pipeline that discards it forces every evaluation to re-run
        retrieval — which is slow, and worse, allows the evaluated context to
        differ from the generated one.
        """
        raise NotImplementedError


def report_card(answerer, queries, chunks, graph) -> dict:
    """Project 2's deliverable. One dict, seven numbers, and three lists:

        n, response_rate, grounded_rate
        outcomes                     the four-way refusal table
        faithfulness
        citations                    parsed, resolved, unresolvable, not_in_context
        confidently_wrong            query ids
        citing_superseded            query ids
        uncited_sentences

    Skip refusals wherever a count would otherwise reward them: a refusal cites
    nothing and claims nothing, so counting its one sentence as uncited, or its
    zero citations as perfect, both mislead in opposite directions.

    Every field is computed by machinery from earlier this week, over the
    **same** contexts the answers were generated from.

    Two rules about this dict, and they are the milestone:

    - **`faithfulness` and `confidently_wrong` must both be reported.** Either
      alone is misleading, and the pairing is the week's whole finding
    - **Nothing here is a quality score.** There is no field for "how good are
      the answers", because nothing in this course can compute one. Week 9 is
      about what happens when you ask a model to
    """
    raise NotImplementedError


def compare(cards: dict[str, dict], primary: str = "grounded_rate") -> list[str]:
    """Configuration names ordered by `primary`, best first, ties by name.

    Then read the whole card for each, not just the ordering. A configuration
    that raises `grounded_rate` while raising `confidently_wrong` has moved the
    system in two directions at once, and a single-metric ordering hides that —
    which is week 6's rule, at the last station.
    """
    raise NotImplementedError
