"""The first week with a generator, and the first answers.

Seven weeks of retrieval produce a context window. Today something turns it into
prose, and you measure the only thing that can be measured without a human:
**was the answer even in the context?**

## The generator here is a stipulated model

There is no language model in this course. `raglab.generator.SimulatedGenerator`
is a hundred lines of rules that reproduce the behaviours week 8 is about — it
answers whatever it is given, grounds its wording in the retrieved text, cites,
and prefers the highest-ranked chunk.

It does not reproduce paraphrase, synthesis, or reasoning. **Do not use it to
estimate how good your answers will be.** Use it to test the machinery that
checks answers, which is what this week builds and which is the part that
transfers. Week 7's rule applies: assert the direction, never the value.

Replace each `raise NotImplementedError` with your own code.
"""

from __future__ import annotations

from raglab.generator import SimulatedGenerator, is_refusal


def answer_all(generator, queries, build_context) -> dict[str, object]:
    """Query id → `Answer`, for every query.

    `build_context(query)` returns the chunk-id-to-text mapping your week-7
    assembler produced. It is passed in rather than imported so that the same
    measurement runs against any context you can build — which is the whole
    point of having spent a week making one.
    """
    raise NotImplementedError


def answer_in_context(query, context: dict[str, str]) -> bool:
    """Whether every one of the query's answer spans is somewhere in the context.

    Week 4's ground truth, doing a new job. It says nothing about the generated
    text — only whether the generator **had** what it needed.

    A query with no spans returns False, including an `unanswerable` one. That is
    correct and worth pausing on: for those queries the context *cannot* contain
    the answer, so "was it there" is always no, and the interesting question is
    what the system did about it. That is Thursday.
    """
    raise NotImplementedError


def response_rate(answers) -> float:
    """Fraction of queries that got prose rather than a refusal.

    Expect **1.0**, and expect that to be uncomfortable. A system that answers
    everything is not being helpful; it is failing to distinguish the cases.
    """
    raise NotImplementedError


def grounded_rate(answers, queries, contexts) -> float:
    """Fraction of all queries that were answered **and** had the answer present.

    Divide by every query, not by the answered ones. Dividing by the answered
    ones is how a system that refuses hard queries reports a higher score for
    answering fewer of them, and it is a real and common way of gaming this.
    """
    raise NotImplementedError


def confidently_wrong(answers, queries, contexts) -> list[str]:
    """Query ids that received prose while the context held no answer. Sorted.

    **The most important list in the week.** Every one of these is a fluent,
    well-cited, confident answer to a question the system could not answer, and
    nothing in the answer itself distinguishes it from a correct one.

    Compare it with week 6's `unreachable`. It will contain those queries and
    more, and the "more" is what retrieval was already failing at without anyone
    seeing prose about it.
    """
    raise NotImplementedError


def report(answers, queries, contexts) -> dict:
    """`n`, `response_rate`, `grounded_rate`, `confidently_wrong`,
    `confidently_wrong_rate`.

    Report the list as well as the rate. A rate tells you how bad it is; the list
    tells you which queries to go and read, and reading them is the only way this
    becomes real rather than a number.
    """
    raise NotImplementedError
