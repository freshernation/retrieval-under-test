"""Day 3 — BM25.

The last three tests are the week: a large, clean improvement that the eval set
is too small to confirm.
"""

from functools import cache

import pytest

import raglab
from bm25 import idf, length_norm, saturate, score, score_term, search
from postings import Index

CORPUS = raglab.corpus.load()
DOCS = {d.id: d.title + "\n" + d.text for d in CORPUS}


@cache
def index() -> Index:
    return Index(DOCS, stopwords=None)


@cache
def evaluations():
    import sys
    from pathlib import Path

    sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "week-01" / "day-4"))
    from overlap import rank

    from raglab.metrics import evaluate

    qs = raglab.judgments.load().split("dev")
    before = evaluate({q.id: rank(q.text, DOCS, 10) for q in qs}, qs, ks=(3, 5))
    after = evaluate({q.id: search(index(), q.text, 10) for q in qs}, qs, ks=(3, 5))
    return before, after


# -- idf ----------------------------------------------------------------------


def test_a_term_in_every_document_is_worth_almost_nothing():
    """`status` is in all ten. `429` is in one. Forty times the weight, from one
    logarithm — and this is week 1's first defect, repaired."""
    assert idf(10, 10) == pytest.approx(0.047, abs=0.001)
    assert idf(1, 10) == pytest.approx(1.992, abs=0.001)
    assert idf(1, 10) / idf(10, 10) > 40


def test_idf_falls_as_the_term_spreads():
    values = [idf(df, 10) for df in range(1, 11)]
    assert values == sorted(values, reverse=True)


def test_the_smoothing_keeps_a_universal_term_alive():
    """Without the halves, a term in every document scores exactly zero and a
    query made only of common words returns nothing rather than something weak."""
    assert idf(10, 10) > 0


# -- saturation ---------------------------------------------------------------


def test_repetition_has_diminishing_returns():
    assert [round(saturate(t), 3) for t in (1, 2, 10, 100)] == [1.0, 1.375, 1.964, 2.174]


def test_a_hundred_occurrences_are_worth_barely_twice_one():
    """Week 1's `frequency_score` gave the eleven-page document the top slot by
    repetition. This is why that cannot happen again."""
    assert saturate(100) < 2.5 * saturate(1)


def test_k1_zero_makes_every_term_binary():
    assert saturate(1, k1=0.0) == pytest.approx(1.0)
    assert saturate(50, k1=0.0) == pytest.approx(1.0)


def test_absent_terms_contribute_nothing():
    assert saturate(0) == 0.0


# -- length -------------------------------------------------------------------


def test_b_zero_disables_normalisation():
    assert length_norm(19462, 5277.9, b=0.0) == 1.0


def test_b_one_divides_fully_by_relative_length():
    assert length_norm(19462, 5277.9, b=1.0) == pytest.approx(19462 / 5277.9)


def test_the_long_document_is_penalised_and_the_short_one_is_not():
    long = length_norm(19462, 5277.9)
    short = length_norm(1247, 5277.9)
    assert long > 1 > short


# -- the term score -----------------------------------------------------------


def test_the_normalisation_lives_in_the_denominator_with_k1():
    """Not applied to the whole term. A long document needs *more* occurrences to
    reach the same saturation, which is the intended behaviour and is easy to
    get wrong by dividing at the end."""
    short = score_term(3, 1, 10, 1000, 5000)
    long = score_term(3, 1, 10, 20000, 5000)
    assert short > long
    assert score_term(3, 1, 10, 5000, 5000) == pytest.approx(
        score_term(3, 1, 10, 1000, 5000, b=0.0)
    )


def test_a_rare_term_beats_a_common_one_at_the_same_frequency():
    rare = score_term(2, 1, 10, 5000, 5000)
    common = score_term(2, 10, 10, 5000, 5000)
    assert rare > 30 * common


def test_zero_where_it_should_be():
    assert score_term(0, 5, 10, 100, 100) == 0.0
    assert score_term(3, 0, 10, 100, 100) == 0.0


# -- search -------------------------------------------------------------------


def test_the_exact_identifier_still_works():
    assert search(index(), "451", 5) == ["rfc-7725"]


def test_documents_sharing_no_term_are_absent():
    assert search(index(), "kubernetes helm", 10) == []


def test_the_acronym_query_that_week_one_ranked_last():
    """Week 1's `what does ROCC stand for` had its answer in position 22 of 22,
    because `what`, `does` and `for` outvoted the one term that mattered. The
    equivalent here is `what does ABNF stand for`, and BM25 puts a document
    containing the expansion in the top three."""
    assert set(search(index(), "what does ABNF stand for", 3)) & {
        "rfc-3986",
        "rfc-9309",
        "rfc-6265",
    }


# -- and the week's result ----------------------------------------------------


def test_it_is_a_large_improvement():
    """recall@3 0.759 → 0.963. ndcg@3 0.651 → 0.805. recall@5 reaches 1.000."""
    before, after = evaluations()
    assert after.metrics["recall@3"] == pytest.approx(0.963, abs=0.005)
    assert after.metrics["ndcg@3"] == pytest.approx(0.805, abs=0.005)
    assert after.metrics["recall@5"] == pytest.approx(1.0)


def test_nothing_got_worse():
    before, after = evaluations()
    assert after.worse_than(before, "ndcg@3") == []


def test_and_the_eval_set_still_cannot_confirm_it():
    """delta +0.204 on recall@3, and the 95% interval's lower bound is **exactly
    zero**.

    Not nearly zero. Zero — and the reason is exact arithmetic rather than bad
    luck. Three of the nine answerable queries improved and **six were
    unchanged**, so a bootstrap resample that happens to draw only unchanged
    queries has a delta of exactly 0. That happens with probability
    `(6/9)**9 = 0.0260` — just over the 0.025 that pins the 2.5th percentile —
    and no improvement, however large, can lift the lower bound above it.

    At the same two-thirds unchanged rate, **ten** answerable queries clears it:
    `(2/3)**10 = 0.0173`. One more query, judged by hand, in an afternoon — not
    a bigger corpus, not a better retriever, not a cleverer test.

    The milestone computes that number for you and then makes you go and write
    the queries.

    **The binding constraint is no longer the retriever. It is the eval set.**
    That is what this week's milestone is for, and it is why it arrives now
    rather than in week 1 — you needed a retriever good enough to make the
    instrument the limitation."""
    from raglab.metrics import bootstrap

    before, after = evaluations()
    delta, low, high = bootstrap(after, before, "recall@3")
    assert delta == pytest.approx(0.204, abs=0.005)
    assert low == 0.0
    improved = [
        q
        for q in after.per_query
        if after.per_query[q]["recall@3"] > before.per_query[q]["recall@3"]
    ]
    assert sorted(improved) == ["r01", "r06", "r07"]
