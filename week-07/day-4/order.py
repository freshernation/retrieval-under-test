"""Where in the window, and a model we cannot check.

Everything so far has asked whether the answer is *in* the context. Today asks
where, and it is the first day in this course where **the honest answer is that
we cannot measure it.**

A language model's use of information in a long context varies with position:
material near the start and end is used more reliably than material in the
middle. That is a Tier 1 result, published, replicated, and about models this
course does not run.

So today you build a **stipulated model** — a U-shaped weighting whose *shape*
comes from the literature and whose *numbers* come from nowhere. Every test here
asserts the **direction** of a comparison and never a value, exactly as week 4
refused to assert a chunk size.

If that feels unsatisfying, good. It is the correct amount of confidence
available without a generator, and week 8 has one.

Replace each `raise NotImplementedError` with your own code.
"""

from __future__ import annotations

from windows import parent


def order_by_rank(selected: list[str]) -> list[str]:
    """The retriever's order, unchanged. The default, and rarely a decision."""
    raise NotImplementedError


def order_by_document(selected: list[str]) -> list[str]:
    """Group by parent document, then by chunk index within it.

    Restores reading order, which matters for a reason the metrics cannot see:
    two consecutive sections of one RFC read as an argument, and the same two
    interleaved with a third document read as three fragments.

    It also throws away the ranking entirely, which is the trade.
    """
    raise NotImplementedError


def ends_first(selected: list[str]) -> list[str]:
    """Best results at the **outside** of the window, worst in the middle.

    Take alternate items from the ranking into a front list and a back list,
    then reverse the back list and concatenate. Rank 1 is first, rank 2 is last,
    rank 3 second, and so on.

    This is the standard mitigation for the positional effect and it is a
    *hypothesis*: it assumes the U-shape is real for your model, your prompt and
    your window size. Nothing here checks that.
    """
    raise NotImplementedError


def attention_weight(position: int, n: int, dip: float = 0.5) -> float:
    """**A stipulated model.** U-shaped over the window, 1.0 at both ends and
    `dip` in the middle.

        1 − 4(1 − dip)·x·(1 − x)   where x = position / (n − 1)

    The *shape* is from the literature. The parabola, and `dip = 0.5`, are ours
    and are not measured — a real curve depends on the model, the prompt, the
    window length and the task, and none of those exist in this course.

    Use it to compare orderings. Do not quote its values. Raise ValueError for
    a non-positive `n` or a `dip` outside [0, 1]; return 1.0 when `n == 1`.
    """
    raise NotImplementedError


def answer_positions(order: list[str], chunks: dict[str, str], query) -> list[int]:
    """Indices in the window whose chunk carries an answer span.

    This one is **measured**, not stipulated, and it is worth looking at on its
    own: on this corpus the first answer-bearing chunk sits about a third of the
    way in, which is the region the stipulated model penalises most.
    """
    raise NotImplementedError


def expected_use(order: list[str], chunks: dict[str, str], query, dip: float = 0.5) -> float:
    """The best attention weight over the answer-bearing positions. 0.0 if none.

    A comparison device, not a measurement. Its **ordering** of strategies is
    the output; its magnitude means nothing.
    """
    raise NotImplementedError


def assemble(order: list[str], texts: dict[str, str]) -> str:
    """The final context: each chunk labelled with its id, blank line between.

    The label is not decoration. Week 8 asks the generator to cite, and it can
    only cite what it can name — a context of unlabelled prose makes attribution
    impossible for the model and unverifiable for you, which is one of the two
    ways a citation ends up pointing at nothing.
    """
    raise NotImplementedError
