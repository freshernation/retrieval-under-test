"""Day 4 — a retriever in forty lines, and its four defects.

The test to read before you write anything:
`test_the_glossary_ranks_last_for_the_query_it_answers_perfectly`. One document
in this corpus answers "what does ROCC stand for" completely. This retriever
puts it in position 22 of 22, and the reason is the whole of week 3.
"""

import pytest

import raglab
from overlap import (
    coverage_score,
    explain,
    frequency_score,
    normalise,
    overlap_score,
    rank,
    term_set,
)

CORPUS = raglab.corpus.load("sample")
DOCS = {d.id: d.title + "\n" + d.text for d in CORPUS}
QUERIES = raglab.judgments.load("sample")


# -- normalise ----------------------------------------------------------------


def test_lowercases_and_splits_on_non_letters():
    assert normalise("Fare Policy (2024)") == ["fare", "policy", "2024"]


def test_digits_survive():
    """`4213` and `42` are the most retrievable strings in this corpus."""
    assert "4213" in normalise("Stop 4213 is closed")


def test_it_destroys_things_you_will_want_back_in_week_3():
    assert normalise("$3.00") == ["3", "00"]
    assert normalise("31-day pass") == ["31", "day", "pass"]
    assert normalise("ROCC") == normalise("rocc")


def test_empty_input_is_empty_output():
    assert normalise("") == []
    assert normalise("!!! ---") == []


def test_term_set_deduplicates():
    assert term_set("fare fare fare") == {"fare"}


# -- scoring ------------------------------------------------------------------


def test_overlap_counts_distinct_query_terms_present():
    assert overlap_score({"fare", "refund"}, {"fare", "policy"}) == 1
    assert overlap_score({"fare"}, {"policy"}) == 0


def test_every_term_is_worth_the_same_and_that_is_the_defect():
    """`the` is worth exactly as much as `4213`. State this before you run
    anything else today; the rest of the day is watching it cost you."""
    common = overlap_score({"the"}, term_set("the fare policy"))
    rare = overlap_score({"4213"}, term_set("stop 4213 is closed"))
    assert common == rare == 1


def test_coverage_is_comparable_across_queries():
    assert coverage_score({"a", "b"}, {"a"}) == 0.5
    assert coverage_score(set(), {"a"}) == 0.0


# -- ranking ------------------------------------------------------------------


def test_a_document_sharing_nothing_is_not_returned():
    """Not a worse answer — not an answer. Padding the top ten with zero-score
    documents inflates every precision number you compute."""
    assert rank("zzz qqq", DOCS, k=10) == []


def test_ties_break_by_document_id_so_the_benchmark_holds_still():
    assert rank("the", DOCS, k=5) == [
        "mrta-001",
        "mrta-002",
        "mrta-003",
        "mrta-004",
        "mrta-005",
    ]


def test_k_is_a_ceiling_not_a_target():
    assert len(rank("refund", DOCS, k=3)) <= 3


def test_it_does_get_the_easy_ones_right():
    """Route 42's detour notice, first, for `route 42 detour`. A retriever this
    simple is not useless — it is useless in a specific pattern."""
    assert rank(QUERIES.by_id("q06").text, DOCS, k=5)[0] == "mrta-006"


def test_the_glossary_ranks_last_for_the_query_it_answers_perfectly():
    """`what does ROCC stand for`. The glossary contains the answer in five
    characters and shares exactly one term with the query. Four documents share
    `what`, `does` and `for` — the three words carrying no information at all —
    and outrank it.

    Position 22 of 22. Nothing about this is a bug; it is the scoring function
    doing precisely what it says. Week 3 is the fix and it is one line of
    arithmetic, which is worth knowing before you reach for anything larger."""
    ranked = rank(QUERIES.by_id("q07").text, DOCS, k=30)
    assert ranked.index("mrta-030") == len(ranked) - 1


def test_frequency_scoring_hands_the_top_slot_to_the_longest_document():
    """The obvious improvement, and it is worse. Counting repeats promotes the
    eleven-page governance document over the enforcement policy that actually
    answers the question, because it says `fare` more times in more pages.

    Length normalisation and term saturation — the two things BM25 is for — both
    exist because of exactly this."""
    q = QUERIES.by_id("q05").text
    assert rank(q, DOCS, k=1, score=overlap_score) == ["mrta-010"]
    assert rank(q, DOCS, k=1, score=frequency_score) == ["mrta-009"]


# -- explain ------------------------------------------------------------------


def test_explain_names_what_was_missing():
    """The vocabulary gap, in one assertion: the corpus says `31-day` and the
    user said `monthly`, so the word that mattered most is in `missed`. No
    amount of station 4, 5 or 6 work fixes this. Week 5 is the fix."""
    report = explain(QUERIES.by_id("q02").text, DOCS["mrta-003"])
    assert "monthly" in report["missed"]
    assert "refund" in report["matched"]


def test_explain_partitions_the_query():
    q = "fare refund policy"
    report = explain(q, DOCS["mrta-003"])
    assert report["matched"] | report["missed"] == term_set(q)
    assert not (report["matched"] & report["missed"])


# -- the baseline number ------------------------------------------------------


def test_the_baseline_scores_this_on_dev():
    """Your number for the rest of the course. Write it down.

    And then read the next test, because 0.875 is not as good as it sounds."""
    from raglab.metrics import evaluate

    dev = QUERIES.split("dev")
    ev = evaluate({q.id: rank(q.text, DOCS, k=10) for q in dev}, dev)
    assert ev.metrics["recall@10"] == pytest.approx(0.875)
    assert ev.metrics["ndcg@10"] == pytest.approx(0.7547, abs=0.001)


def test_the_top_ten_is_a_third_of_this_corpus():
    """30 documents. Asking for the top 10 asks for a third of everything, so
    recall@10 flatters every retriever on this set — including the one that
    ranks the correct answer 22nd.

    Recall@10 on 30 documents and recall@10 on 3 million are not the same
    measurement and they are written down identically. This is the single most
    common way a retrieval number is quoted misleadingly, and it is usually not
    deliberate."""
    assert len(CORPUS) == 30
    assert 10 / len(CORPUS) > 0.3
