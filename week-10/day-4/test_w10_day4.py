"""Day 4 — cost, and the step that buys nothing.

`test_one_step_costs_fifty_eight_percent_more_and_answers_nothing_new` is the day.
"""

from functools import cache

import pytest

import raglab
from cost import (
    TOKENS_PER_WORD,
    context_tokens,
    cost_curve,
    marginal,
    price,
    tokens,
    waste,
)
from dense import DenseRetriever
from fuse import rrf
from order import order_by_rank
from postings import Index
from sections import section_corpus
from window import pack

CORPUS = raglab.corpus.load()
DOCS = {d.id: d.title + "\n" + d.text for d in CORPUS}
BUDGETS = (200, 400, 800, 1200, 2000, 4000)


@cache
def dev():
    return list(raglab.judgments.load(file="queries-extended.yml").split("dev"))


@cache
def build():
    import sys
    from pathlib import Path

    root = Path(__file__).resolve().parents[2]
    for day in ("day-3", "day-2", "day-1"):
        sys.path.insert(0, str(root / "week-03" / day))
    from bm25 import search

    chunks = section_corpus(DOCS, 100, 300)
    index = Index(chunks, stopwords=None)
    retriever = DenseRetriever(dims=192).fit(chunks)

    def context(text, budget):
        shortlist = rrf([search(index, text, 60), retriever.search(text, 60)], 20, 10)
        selected, texts = pack(shortlist, chunks, budget)
        return {c: texts[c] for c in order_by_rank(selected)}

    return context


@cache
def curve():
    return cost_curve(BUDGETS, build(), dev())


# -- the quantity -------------------------------------------------------------


def test_tokens_are_stipulated_and_the_lab_says_so():
    """1.3 per word is a stand-in. This corpus is full of `rfc-7231` and `428`,
    which tokenise badly, so the real ratio here is worse than the usual quoted
    figure — and the direction is all that transfers."""
    assert TOKENS_PER_WORD == 1.3
    assert tokens("must json be encoded in utf 8") == 10
    assert tokens("") == 0
    assert context_tokens({"a": "one two", "b": "three"}) == 3 + 2


def test_a_price_has_no_default():
    """A default price is a result quoted by accident, and it is the fastest
    ageing number in this repository."""
    assert price(1000, 0.5) == pytest.approx(0.5)
    with pytest.raises(TypeError):
        price(1000)


# -- the curve ----------------------------------------------------------------


def test_the_curve_is_the_week_seven_finding_in_money():
    """Week 7 measured answer density collapsing from 0.237 at an 800-word budget
    to 0.098 at 2,000. Same pipeline, same decision, counted in tokens:

    | budget | tokens/query | answered | tokens/answer |
    |---|---|---|---|
    | 200 | 93 | 0.20 | 372 |
    | 400 | 375 | 0.50 | 834 |
    | 800 | 885 | 0.70 | 1,264 |
    | 1200 | 1,403 | 0.70 | 2,004 |
    | 2000 | 2,445 | 0.80 | 3,260 |
    | 4000 | 4,922 | 0.85 | 5,791 |
    """
    rows = curve()
    assert rows[800]["tokens_per_query"] == pytest.approx(885.0, abs=1.0)
    assert rows[800]["answered"] == pytest.approx(0.70, abs=0.01)
    assert rows[4000]["answered"] == pytest.approx(0.85, abs=0.01)
    assert rows[4000]["tokens_per_query"] / rows[800]["tokens_per_query"] > 5


def test_one_step_costs_fifty_eight_percent_more_and_answers_nothing_new():
    """**The day.**

    800 → 1200 words. Tokens per query go from 885 to 1,403 — **58% more spend,
    on every request, forever** — and the answered rate does not move: 0.70 to
    0.70.

    Not an optimisation opportunity. A setting that should be turned down. And
    nothing on a dashboard distinguishes the two: latency is close, faithfulness
    is identical, the answers are longer and read better.

    `waste` finds it in one line over a curve you can compute in an afternoon,
    and it is the easiest win available in a production RAG system."""
    rows = curve()
    assert rows[1200]["answered"] == rows[800]["answered"]
    assert rows[1200]["tokens_per_query"] / rows[800]["tokens_per_query"] == pytest.approx(
        1.58, abs=0.02
    )
    assert waste(rows) == [1200]


def test_the_marginal_answer_costs_seventeen_times_more_at_the_dear_end():
    """1,411 tokens for an extra answered query at the 200 → 400 step. **24,768**
    at the 2000 → 4000 step. Seventeen-fold, and the step in between buys none at
    any price.

    Meanwhile the *average* — tokens per answered query — climbs smoothly from
    372 to 5,791 and shows no cliff at all. An average over a budget curve
    cannot tell you where to stop spending; only the margin can."""
    steps = marginal(curve())
    assert steps[(200, 400)] == pytest.approx(1411, abs=20)
    assert steps[(800, 1200)] == float("inf")
    assert steps[(2000, 4000)] == pytest.approx(24768, abs=200)
    assert steps[(2000, 4000)] / steps[(200, 400)] > 17


def test_the_best_quality_setting_is_the_dearest_and_that_is_a_decision():
    """4,000 words answers 0.85 against 800's 0.70 — the best number in the
    table, at 5.6 times the tokens.

    There is no measurement that settles this. It needs a price, a request
    volume and somebody's judgment about what an unanswered question costs, and
    none of those three live in the repository. Say which of them you assumed."""
    rows = curve()
    best = max(rows, key=lambda b: (rows[b]["answered"], -b))
    assert best == 4000
    assert rows[best]["tokens_per_query"] > rows[800]["tokens_per_query"] * 5
