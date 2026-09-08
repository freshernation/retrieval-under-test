"""One shared, boring token counter.

Context budgets (week 7) and chunk sizes (week 4) are meaningless unless everyone
counts the same way, so the count lives here rather than in each lab.

It is a *four-characters-per-token* approximation, not a real tokeniser, and that
is deliberate: a real tokeniser is model-specific, would pull in a dependency, and
would make week 4's numbers change when the model changed. The approximation is
wrong by 10-20% on English prose and wrong by much more on code and on
acronym-heavy text — which is itself a week 7 discussion, not a bug to fix.
"""

import re

_WORD = re.compile(r"\w+|[^\w\s]")


def approx_tokens(s: str) -> int:
    """Approximate token count. Deterministic, model-free, and slightly wrong."""
    if not s:
        return 0
    return max(1, round(len(s) / 4))


def words(s: str) -> list[str]:
    """Split into word-ish units. Used by the harness for reporting only —
    week 3 is where you write the tokeniser that actually feeds an index, and
    this one is not it."""
    return _WORD.findall(s)


def truncate_to_tokens(s: str, budget: int) -> str:
    """Cut a string to roughly `budget` tokens, on a word boundary."""
    if budget <= 0:
        return ""
    if approx_tokens(s) <= budget:
        return s
    cut = s[: budget * 4]
    space = cut.rfind(" ")
    return cut[:space] if space > 0 else cut
