"""The context window is a budget, and k was never the right unit.

Every week so far has retrieved "the top k". A generator does not consume k
chunks; it consumes **words**, and your chunks are not the same size — sections
here run from 100 to 300.

So `k = 5` is not a budget. It is between 500 and 1,500 words depending on the
query, which is a range of three and nobody chose it.

Today `k` is replaced by a word budget, and two numbers appear that no earlier
metric could produce: how much of the window is **answer-bearing**, and how much
is waste.

Replace each `raise NotImplementedError` with your own code.
"""

from __future__ import annotations


def word_count(text: str) -> int:
    """Whitespace words. As in week 4, this is not model tokens — it is what you
    can count without a model, and the ratio is roughly 0.75 words per token for
    English prose and much worse for the identifier-heavy text in this corpus."""
    raise NotImplementedError


def truncate_to(text: str, words: int) -> str:
    """First `words` words. Empty string for a non-positive budget."""
    raise NotImplementedError


def pack(ranked: list[str], chunks: dict[str, str], budget: int, truncate: bool = False):
    """Fill the budget from the ranking, best first. Returns
    `(selected ids, {id: text})`.

    **Stop at the first chunk that does not fit.** Do not skip it and take a
    smaller one further down: that silently reorders the results by size, so the
    window no longer reflects the ranking you spent six weeks building.

    With `truncate=True`, cut the first non-fitting chunk to the remaining space
    and stop. That is a real choice with a real cost — see the tests — and it is
    worth measuring both ways rather than assuming.
    """
    raise NotImplementedError


def used_words(texts: dict[str, str]) -> int:
    raise NotImplementedError


def answer_density(texts: dict[str, str], query) -> float:
    """Fraction of the packed words that sit in an **answer-bearing** chunk.

    The number no earlier metric could produce, and the first one that describes
    the thing you are actually paying for. Baseline here is about 0.24 at 800
    words: three quarters of the context is not carrying the answer.

    It is a *loose upper bound* on usefulness, not a measure of it — a chunk
    containing the span is counted whole, including the 250 words around it.
    """
    raise NotImplementedError


def answered(texts: dict[str, str], query) -> bool:
    """Whether the packed window contains **every** answer span."""
    raise NotImplementedError


def budget_curve(ranked, chunks, query, budgets, truncate: bool = False):
    """Per budget: `chunks`, `words`, `answered`, `density`.

    Week 4's frontier again, one stage later. Same shape, same conclusion, and
    now the cost axis is the one the generator actually charges for.
    """
    raise NotImplementedError
