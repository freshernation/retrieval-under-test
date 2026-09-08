"""Day 2 — relevance judgments.

The test to read twice: `test_kappa_is_zero_when_both_judges_just_say_no`. Two
judges agreeing 90% of the time, having told you nothing at all.
"""

import pytest

from judging import (
    agreement,
    binary_disagreements,
    cohens_kappa,
    overlap_size,
    parse_grade,
    pool,
    relevant_set,
    smells,
)

# -- parse_grade --------------------------------------------------------------


def test_valid_grades_pass_through():
    assert [parse_grade(g) for g in (0, 1, 2, 3)] == [0, 1, 2, 3]


def test_strings_of_grades_are_accepted():
    assert parse_grade("2") == 2


@pytest.mark.parametrize("bad", [4, -1, 2.5, "2 ", "two", None, "", []])
def test_everything_else_is_refused(bad):
    with pytest.raises(ValueError):
        parse_grade(bad)


def test_true_is_not_the_grade_one():
    """`True == 1` in Python, so a bool sails through a naive check and puts a
    judgment in your file that nobody wrote."""
    with pytest.raises(ValueError):
        parse_grade(True)


# -- relevant_set -------------------------------------------------------------


def test_relevant_is_two_and_above():
    assert relevant_set({"a": 3, "b": 2, "c": 1, "d": 0}) == {"a", "b"}


def test_the_threshold_moves():
    assert relevant_set({"a": 3, "b": 2, "c": 1}, threshold=1) == {"a", "b", "c"}
    assert relevant_set({"a": 3, "b": 2, "c": 1}, threshold=3) == {"a"}


# -- agreement ----------------------------------------------------------------


def test_agreement_uses_only_the_overlap():
    a = {"x": 2, "y": 0, "z": 3}
    b = {"x": 2, "y": 1, "w": 0}
    assert overlap_size(a, b) == 2
    assert agreement(a, b) == pytest.approx(0.5)


def test_no_overlap_is_not_a_disagreement():
    assert agreement({"x": 2}, {"y": 2}) == 1.0
    assert overlap_size({"x": 2}, {"y": 2}) == 0


def test_a_perfect_agreement_on_three_documents_is_still_only_three():
    """The number to report next to every agreement figure you ever quote."""
    a = b = {"x": 2, "y": 1, "z": 0}
    assert agreement(a, b) == 1.0
    assert overlap_size(a, b) == 3


# -- binary_disagreements -----------------------------------------------------


def test_only_disagreements_that_cross_the_line_count():
    a = {"p": 3, "q": 2, "r": 1, "s": 0}
    b = {"p": 2, "q": 1, "r": 1, "s": 2}
    # p: 3 vs 2 — both relevant, does not cross. q and s cross.
    assert binary_disagreements(a, b) == ["q", "s"]


def test_a_two_versus_three_argument_changes_no_recall_number():
    assert binary_disagreements({"a": 2}, {"a": 3}) == []


# -- cohens_kappa -------------------------------------------------------------


def test_kappa_is_one_for_identical_judgments():
    a = {"p": 3, "q": 2, "r": 0, "s": 1}
    assert cohens_kappa(a, dict(a)) == pytest.approx(1.0)


def test_kappa_is_zero_when_both_judges_just_say_no():
    """Nine documents out of ten graded 0 by both judges, one disagreement. Raw
    agreement is 90%. Kappa is near zero, because two judges who label almost
    everything irrelevant will agree almost always by accident.

    Report raw agreement in a paper and a reviewer will ask for this number.
    Report it to yourself and you will stop trusting your own eval set, which is
    the appropriate amount to trust it."""
    a = {f"d{i}": 0 for i in range(10)}
    b = dict(a)
    b["d9"] = 2
    assert agreement(a, b) == pytest.approx(0.9)
    assert cohens_kappa(a, b) == pytest.approx(0.0, abs=0.05)


def test_kappa_is_negative_when_judges_are_worse_than_chance():
    a = {"p": 2, "q": 0, "r": 2, "s": 0}
    b = {"p": 0, "q": 2, "r": 0, "s": 2}
    assert cohens_kappa(a, b) < 0


# -- pool ---------------------------------------------------------------------


def test_pooling_unions_the_tops_in_order():
    assert pool([["a", "b", "c"], ["b", "d"]], depth=2) == ["a", "b", "d"]


def test_depth_cuts_each_list_before_the_union():
    assert pool([["a", "b", "c"], ["z"]], depth=1) == ["a", "z"]


def test_a_document_no_system_surfaced_is_never_judged():
    """The permanent bias in every retrieval benchmark ever published, in one
    assertion. `q` exists, it is relevant, and no pool will ever contain it."""
    assert "q" not in pool([["a", "b"], ["b", "c"]], depth=10)


# -- smells -------------------------------------------------------------------


CORPUS = {"a", "b", "c", "d"}


def test_a_query_with_nothing_relevant_is_flagged():
    problems = smells({"q1": {"a": 1, "b": 0, "c": 1}}, CORPUS)
    assert len(problems) == 1 and problems[0].startswith("q1")


def test_the_one_that_ruins_eval_sets():
    """Every judged document relevant. The metrics look fine. The query cannot
    punish any retriever for any result, and nothing will ever tell you."""
    problems = smells({"q1": {"a": 2, "b": 3, "c": 2}}, CORPUS)
    assert any("every judged document" in p for p in problems)


def test_a_judgment_outside_the_corpus_is_flagged():
    problems = smells({"q1": {"a": 2, "b": 0, "zzz": 3}}, CORPUS)
    assert any("zzz" in p for p in problems)


def test_a_thin_query_is_flagged():
    problems = smells({"q1": {"a": 2, "b": 0}}, CORPUS)
    assert any("q1" in p for p in problems)


def test_a_sound_set_smells_of_nothing():
    assert smells({"q1": {"a": 3, "b": 1, "c": 0, "d": 2}}, CORPUS) == []


def test_problems_are_sorted_so_the_output_is_stable():
    problems = smells(
        {"q2": {"a": 2, "b": 3, "c": 2}, "q1": {"a": 1, "b": 0, "c": 0}}, CORPUS
    )
    assert problems == sorted(problems)
