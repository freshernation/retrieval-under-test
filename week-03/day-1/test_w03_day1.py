"""Day 1 — the analyzer, and the limits of fixing things before the scoring.

Read the last three tests together. Today's headline result is negative.
"""

from functools import cache

import pytest

import raglab
from analyzer import (
    STOPWORDS,
    analyze,
    document_frequency,
    keep_identifiers,
    remove_stopwords,
    split_terms,
    stem,
    stem_all,
    vocabulary,
)

CORPUS = raglab.corpus.load()
DOCS = {d.id: d.title + "\n" + d.text for d in CORPUS}


@cache
def df():
    return document_frequency(DOCS, stopwords=None)


def overlap_rank(query: str, k: int = 10, **options) -> list[str]:
    """Week 1's retriever, with a configurable analyzer bolted on. The *scoring*
    is unchanged — count matching terms — which is the point of today."""
    terms = set(analyze(query, **options))
    scored = []
    for doc_id, text in DOCS.items():
        score = len(terms & set(analyze(text, **options)))
        if score:
            scored.append((-score, doc_id))
    scored.sort()
    return [doc_id for _, doc_id in scored[:k]]


# -- tokenising ---------------------------------------------------------------


def test_split_terms_matches_week_one():
    assert split_terms("Status Code 429!") == ["status", "code", "429"]


def test_the_split_destroys_compounds():
    assert split_terms("UTF-8") == ["utf", "8"]


def test_keeping_identifiers_emits_both():
    """`8` appears in nine of ten documents. `utf-8` is what somebody searches
    for. Emit the pieces and the compound."""
    tokens = keep_identifiers("UTF-8")
    assert "utf" in tokens and "8" in tokens and "utf-8" in tokens


def test_identifiers_catch_letter_digit_runs():
    assert "rfc8259" in keep_identifiers("see RFC8259 for details")


# -- stopwords ----------------------------------------------------------------


def test_stopwords_come_out():
    assert remove_stopwords(["what", "is", "a", "cookie"]) == ["cookie"]


def test_stopwords_are_a_quarter_of_the_corpus_by_token_and_nothing_by_type():
    """52,779 tokens become 38,027 — 28% removed. The vocabulary falls by 44
    terms out of 4,273, about one percent.

    A handful of types carry a quarter of the text. That asymmetry is the whole
    reason a *frequency-based* weighting works, and it is why the fix is
    arithmetic rather than a list."""
    all_terms = vocabulary(DOCS, stopwords=None)
    kept = vocabulary(DOCS)
    assert sum(all_terms.values()) == 52_779
    assert sum(kept.values()) == 38_027
    assert len(all_terms) - len(kept) == 44


# -- stemming -----------------------------------------------------------------


def test_stemming_does_what_it_says():
    assert stem("requests") == "request"
    assert stem("policies") == "policy"
    assert stem_all(["caching", "encoded"]) == ["cach", "encod"]


def test_short_words_are_left_alone():
    assert stem("uses") == "uses"
    assert stem("is") == "is"


def test_the_stemmer_damages_real_terms():
    """`status` is not a plural. `cookies` is not a cook.

    Both are what a suffix stripper does, both are in this corpus, and a real
    stemmer makes the same kind of mistake with better manners."""
    assert stem("status") == "statu"
    assert stem("cookies") == "cooky"


def test_and_still_fails_the_case_it_was_for():
    """The whole argument for stemming is that `cache` should match `caching`.
    It does not: one strips to `cach` and the other keeps its `e`."""
    assert stem("caching") != stem("cache")


# -- the pipeline -------------------------------------------------------------


def test_the_pipeline_composes():
    assert analyze("What are the Requests?", stemming=True) == ["request"]


def test_analysis_is_the_same_on_both_sides_or_nothing_matches():
    """The most common bug in hand-built search, and it survives code review
    because the two call sites live in different files."""
    doc = analyze("Caching policies", stemming=True)
    query = analyze("caching policy", stemming=True)
    assert set(doc) & set(query)


# -- document frequency -------------------------------------------------------


def test_the_table_that_explains_week_one():
    """Every term in the user's question is in every document. The one term that
    identifies the answer is in one — and the user did not type it.

    Week 1's scorer gives all of these the same weight. That is not a tokeniser
    problem and no analyzer setting fixes it."""
    assert df()["status"] == 10
    assert df()["code"] == 10
    assert df()["429"] == 1
    assert df()["451"] == 1


def test_document_frequency_counts_documents_not_occurrences():
    assert df()["the"] == 10
    assert vocabulary(DOCS, stopwords=None)["the"] > 2000


# -- and now the negative results ---------------------------------------------


def test_removing_stopwords_does_not_help():
    """recall@3 goes **down**, 0.759 → 0.685. The interval spans zero in both
    directions, so strictly you have measured nothing — but you certainly have
    not measured an improvement, and everybody expects one."""
    from raglab.metrics import evaluate

    qs = raglab.judgments.load().split("dev")
    without = evaluate({q.id: overlap_rank(q.text, stopwords=None) for q in qs}, qs, ks=(3,))
    with_stop = evaluate({q.id: overlap_rank(q.text) for q in qs}, qs, ks=(3,))
    assert without.metrics["recall@3"] == pytest.approx(0.759, abs=0.005)
    assert with_stop.metrics["recall@3"] == pytest.approx(0.685, abs=0.005)
    assert with_stop.metrics["recall@3"] < without.metrics["recall@3"]


def test_stemming_actively_breaks_two_queries():
    """ndcg@3 falls from 0.633 to 0.596, and `worse_than` names the casualties.

    A stopword list is a crude approximation of "this term carries no
    information", and a stemmer is a crude approximation of "these two strings
    mean the same thing". Both are guesses applied before any evidence is
    available."""
    from raglab.metrics import evaluate

    qs = raglab.judgments.load().split("dev")
    plain = evaluate({q.id: overlap_rank(q.text) for q in qs}, qs, ks=(3,))
    stemmed = evaluate({q.id: overlap_rank(q.text, stemming=True) for q in qs}, qs, ks=(3,))
    assert stemmed.metrics["ndcg@3"] < plain.metrics["ndcg@3"]
    assert stemmed.worse_than(plain, "ndcg@3") == ["r08", "r10"]


def test_the_one_change_that_does_help_is_the_one_that_loses_no_information():
    """Keeping identifiers raises ndcg@3 from 0.651 to 0.675. It is the only
    change today that **adds** rather than discards, and it is the only one that
    helps.

    That is the day's thesis. Stopword lists and stemmers throw information away
    in the hope that it was noise. Day 3 keeps everything and weighs it
    instead — and it is one line of arithmetic."""
    from raglab.metrics import evaluate

    qs = raglab.judgments.load().split("dev")
    plain = evaluate({q.id: overlap_rank(q.text, stopwords=None) for q in qs}, qs, ks=(3,))
    ident = evaluate(
        {q.id: overlap_rank(q.text, identifiers=True) for q in qs}, qs, ks=(3,)
    )
    assert ident.metrics["ndcg@3"] > plain.metrics["ndcg@3"]
