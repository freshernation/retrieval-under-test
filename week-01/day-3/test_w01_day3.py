"""Day 3 — the metrics.

The pair to read together: `test_recall_is_blind_to_order` and
`test_ndcg_is_not`. Same documents, same judgments, one number moves and one
does not, and the gap between them is the whole of station 5.
"""

import pytest

from scoring import (
    average_precision,
    dcg_at_k,
    grade,
    mean_over_queries,
    ndcg_at_k,
    paired_bootstrap,
    precision_at_k,
    recall_at_k,
    reciprocal_rank,
)

J = {"a": 3, "b": 2, "c": 1, "d": 0}


# -- grade --------------------------------------------------------------------


def test_unjudged_is_zero():
    assert grade(J, "a") == 3
    assert grade(J, "never-seen") == 0


# -- recall -------------------------------------------------------------------


def test_recall_counts_the_relevant_ones_found():
    assert recall_at_k(["a", "b"], J, k=10) == 1.0
    assert recall_at_k(["a", "c", "d"], J, k=10) == 0.5


def test_recall_respects_k():
    assert recall_at_k(["d", "c", "a", "b"], J, k=2) == 0.0
    assert recall_at_k(["d", "c", "a", "b"], J, k=3) == 0.5


def test_recall_is_blind_to_order():
    """Read with `test_ndcg_is_not`."""
    assert recall_at_k(["a", "b", "c"], J, k=10) == recall_at_k(["c", "b", "a"], J, k=10)


def test_a_query_with_nothing_relevant_scores_zero_not_an_error():
    assert recall_at_k(["c", "d"], {"c": 1, "d": 0}, k=10) == 0.0


# -- precision ----------------------------------------------------------------


def test_precision_divides_by_k_not_by_what_you_returned():
    """Three results, all relevant, is not precision@10 of 1.0. Seven slots were
    left empty and the metric says so."""
    assert precision_at_k(["a", "b"], J, k=10) == pytest.approx(0.2)
    assert precision_at_k(["a", "b"], J, k=2) == 1.0


def test_precision_at_ten_is_capped_by_the_judgments():
    """Two relevant documents in the whole set means precision@10 cannot exceed
    0.2, for any retriever, ever. Comparing this number across queries compares
    the judgments and not the system."""
    perfect = ["a", "b"] + [f"pad{i}" for i in range(8)]
    assert precision_at_k(perfect, J, k=10) == pytest.approx(0.2)


# -- reciprocal rank ----------------------------------------------------------


def test_reciprocal_rank_is_the_first_hit():
    assert reciprocal_rank(["a", "b"], J) == 1.0
    assert reciprocal_rank(["d", "c", "b"], J) == pytest.approx(1 / 3)
    assert reciprocal_rank(["c", "d"], J) == 0.0


def test_reciprocal_rank_ignores_everything_after_the_first_hit():
    """Two systems, wildly different quality, identical MRR."""
    assert reciprocal_rank(["a", "d", "d"], J) == reciprocal_rank(["a", "b", "b"], J)


# -- dcg and ndcg -------------------------------------------------------------


def test_dcg_matches_the_formula():
    # a at position 1: (2**3 - 1)/log2(2) = 7.0 ; b at position 2: 3/log2(3)
    import math

    expected = 7.0 + 3 / math.log2(3)
    assert dcg_at_k(["a", "b"], J, k=10) == pytest.approx(expected)


def test_ndcg_is_one_for_the_ideal_order():
    assert ndcg_at_k(["a", "b", "c", "d"], J, k=10) == pytest.approx(1.0)


def test_ndcg_is_not():
    """Read with `test_recall_is_blind_to_order`."""
    assert ndcg_at_k(["c", "b", "a"], J, k=10) < ndcg_at_k(["a", "b", "c"], J, k=10)


def test_ndcg_ideal_is_computed_from_the_judgments_not_the_ranking():
    """A retriever that returns only the second-best document still gets marked
    against the best possible ranking, which is the point of normalising."""
    assert ndcg_at_k(["b"], J, k=10) < 1.0


def test_ndcg_is_zero_when_nothing_is_relevant():
    assert ndcg_at_k(["x", "y"], {"x": 0, "y": 0}, k=10) == 0.0


def test_ndcg_uses_grades_and_recall_does_not():
    """The only reason to record grades rather than yes/no."""
    top_heavy = ["a", "d", "b"]
    bottom_heavy = ["b", "d", "a"]
    assert recall_at_k(top_heavy, J, k=10) == recall_at_k(bottom_heavy, J, k=10)
    assert ndcg_at_k(top_heavy, J, k=10) > ndcg_at_k(bottom_heavy, J, k=10)


# -- average precision --------------------------------------------------------


def test_average_precision_rewards_finding_all_of_them_early():
    early = average_precision(["a", "b", "d", "d"], J)
    late = average_precision(["a", "d", "d", "b"], J)
    assert early > late


def test_average_precision_of_a_perfect_ranking_is_one():
    assert average_precision(["a", "b", "c", "d"], J) == pytest.approx(1.0)


def test_average_precision_with_nothing_relevant_is_zero():
    assert average_precision(["x"], {"x": 0}) == 0.0


# -- means --------------------------------------------------------------------


RANKINGS = {"q1": ["a", "b"], "q2": ["d", "a"]}
JUDGED = {"q1": J, "q2": J}


def test_mean_over_queries_averages():
    assert mean_over_queries(recall_at_k, RANKINGS, JUDGED, k=10) == pytest.approx(0.75)


def test_a_query_with_no_ranking_scores_zero_rather_than_vanishing():
    """The most common dishonest number in this field: a mean computed only over
    the queries the system managed to answer."""
    assert mean_over_queries(recall_at_k, {"q1": ["a", "b"]}, JUDGED, k=10) == pytest.approx(0.5)


# -- bootstrap ----------------------------------------------------------------


A = {f"q{i}": v for i, v in enumerate([1.0, 1.0, 1.0, 0.5, 1.0, 1.0, 0.5, 1.0])}
B = {f"q{i}": v for i, v in enumerate([0.5, 0.5, 1.0, 0.0, 0.5, 1.0, 0.0, 0.5])}


def test_bootstrap_is_seeded():
    assert paired_bootstrap(A, B) == paired_bootstrap(A, B)


def test_a_system_against_itself_is_exactly_nothing():
    delta, low, high = paired_bootstrap(A, A)
    assert (delta, low, high) == (0.0, 0.0, 0.0)


def test_the_delta_is_the_mean_difference():
    delta, _, _ = paired_bootstrap(A, B)
    assert delta == pytest.approx(0.375)


def test_the_interval_brackets_the_delta():
    delta, low, high = paired_bootstrap(A, B)
    assert low <= delta <= high


def test_a_one_query_win_on_eight_queries_is_not_a_result():
    """Eight queries, one of which improved by 0.25. The mean moved. The interval
    contains zero. You have measured nothing, and on a hand-built eval set this
    is what most of your week-4 results will look like."""
    a = {f"q{i}": 0.5 for i in range(8)}
    b = dict(a)
    b["q3"] = 0.25
    delta, low, high = paired_bootstrap(a, b)
    assert delta > 0
    assert low <= 0 <= high
