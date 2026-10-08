"""Cost: the number that ages fastest, over the quantity that does not.

A price per thousand tokens is the most perishable number in this repository.
It has fallen by more than an order of magnitude over the life of this
technology and it will have moved again before you read this.

So today measures **tokens**, which are a property of your pipeline, and treats
the price as an argument. The fence forbids quoting a price as a result; the
same stipulated-model discipline weeks 7, 8 and 9 used, applied to money.

The thing being costed was decided in week 7: the word budget. Week 7 measured
what it did to answer density. Today measures what it does to the bill, and the
two findings are the same finding.

Replace each `raise NotImplementedError` with your own code.
"""

from __future__ import annotations

TOKENS_PER_WORD = 1.3
"""Stipulated. Real tokenisers vary by model, by language, and by how much of
your corpus is identifiers — and this corpus is full of `rfc-7231` and `428`,
which tokenise badly. Direction transfers; the value does not. Measure it with
your own tokeniser before you put it in a budget."""


def tokens(text: str) -> int:
    """Words times `TOKENS_PER_WORD`, rounded up."""
    raise NotImplementedError


def context_tokens(context: dict[str, str]) -> int:
    """The prompt's retrieved portion. The one term in the bill you control
    directly, and the one week 7 already taught you to measure."""
    raise NotImplementedError


def cost_curve(budgets, build_context, queries) -> dict[int, dict]:
    """Per word budget: `tokens_per_query`, `answered`, `tokens_per_answered`.

    `build_context(query_text, budget)` returns the packed context;
    `answered` is the fraction whose answer spans survive into it.

    `tokens_per_answered` is the only one of the three worth putting in a
    decision. A cost per query says what you spend; a cost per answer says what
    you get, and they move in opposite directions over part of this range.
    """
    raise NotImplementedError


def marginal(curve: dict[int, dict]) -> dict[tuple[int, int], float]:
    """Between each adjacent pair of budgets: tokens spent per **additional**
    answered query, over the whole query set. `inf` when the step buys none.

    Averages hide this completely. The average cost per answer falls and then
    rises, and the marginal cost is what tells you where the turn is.
    """
    raise NotImplementedError


def waste(curve: dict[int, dict]) -> list[int]:
    """The budgets that cost more than the step below and answer no more
    questions. Pure loss, sorted.

    Not an optimisation opportunity — a setting that should be turned down. It
    is the easiest win in a production RAG system and it is invisible without
    the curve, because every number on the dashboard looks the same before and
    after.
    """
    raise NotImplementedError


def price(token_count: int, per_1k: float) -> float:
    """`per_1k` is an argument, deliberately. There is no default, because a
    default price is a result quoted by accident.
    """
    raise NotImplementedError
