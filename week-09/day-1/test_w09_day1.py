"""Day 1 — what you cannot measure once it is running.

`test_the_signals_a_dashboard_would_track_are_useless` is the day.
"""

from functools import cache

import pytest

import raglab
from cite import chunk_citations
from dense import DenseRetriever
from fuse import rrf
from ground import answer_all
from order import order_by_rank
from proxies import (
    OFFLINE_ONLY,
    SERVING,
    auc,
    availability,
    needs_ground_truth,
    proxy_report,
    separation_strength,
    useful_proxies,
)
from raglab.generator import SimulatedGenerator
from refuse import confidence, has_answer
from sections import section_corpus
from window import pack

CORPUS = raglab.corpus.load()
DOCS = {d.id: d.title + "\n" + d.text for d in CORPUS}


@cache
def dev():
    return list(raglab.judgments.load(file="queries-extended.yml").split("dev"))


@cache
def run():
    import sys
    from pathlib import Path

    root = Path(__file__).resolve().parents[2]
    for day in ("day-3", "day-2", "day-1"):
        sys.path.insert(0, str(root / "week-03" / day))
    from bm25 import search

    from postings import Index

    chunks = section_corpus(DOCS, 100, 300)
    index = Index(chunks, stopwords=None)
    retriever = DenseRetriever(dims=192).fit(chunks)

    def build_context(query):
        shortlist = rrf([search(index, query.text, 60), retriever.search(query.text, 60)], 20, 10)
        selected, texts = pack(shortlist, chunks, 800)
        return {c: texts[c] for c in order_by_rank(selected)}

    contexts = {q.id: build_context(q) for q in dev()}
    answers = answer_all(SimulatedGenerator(), dev(), build_context)
    truth = {q.id: has_answer(q, contexts[q.id]) for q in dev()}
    return chunks, contexts, answers, truth


@cache
def signals():
    chunks, contexts, answers, _ = run()
    return {
        "retrieval_confidence": {q.id: confidence(q.text, contexts[q.id]) for q in dev()},
        "distinct_documents": {
            q.id: float(len({c.split("#")[0] for c in contexts[q.id]})) for q in dev()
        },
        "answer_words": {q.id: float(len(answers[q.id].text.split())) for q in dev()},
        "citation_count": {
            q.id: float(len(chunk_citations(answers[q.id].text, chunks))) for q in dev()
        },
    }


# -- the audit ----------------------------------------------------------------


def test_the_test_is_could_i_compute_this_for_an_unseen_query():
    """Faithfulness passes — it compares the answer to the context and you have
    both. Groundedness fails — it needs to know what the right answer was."""
    metrics = availability()
    assert metrics["faithfulness"] == SERVING
    assert metrics["citation_validity"] == SERVING
    assert metrics["grounded_rate"] == OFFLINE_ONLY
    assert metrics["correctness"] == OFFLINE_ONLY


def test_the_offline_only_list_is_short_and_alarming():
    """Four of ten, and they are the four you would most want: whether the
    answer was available, whether the system was confidently wrong, retrieval
    recall, and correctness."""
    missing = needs_ground_truth(availability())
    assert missing == ["answer_recall", "confidently_wrong", "correctness", "grounded_rate"]


# -- the measure --------------------------------------------------------------


def test_auc_is_threshold_free():
    """Picking a threshold first is how a useful signal gets discarded for
    scoring badly at a cutoff nobody chose."""
    assert auc([1.0, 2.0], [0.0, 0.5]) == 1.0
    assert auc([0.0, 0.5], [1.0, 2.0]) == 0.0
    assert auc([1.0], [1.0]) == 0.5
    assert auc([], [1.0]) == 0.5


def test_an_inverse_predictor_is_a_predictor():
    """A signal with AUC 0.17 is as informative as one with 0.83. Reporting only
    the raw number throws away every inverse predictor."""
    assert separation_strength(0.17) == pytest.approx(0.83)
    assert separation_strength(0.83) == pytest.approx(0.83)
    assert separation_strength(0.5) == 0.5


def test_direction_is_reported_because_the_sign_is_not_obvious():
    report = proxy_report(signals(), run()[3])
    assert report["retrieval_confidence"]["direction"] == "higher"
    assert report["distinct_documents"]["direction"] == "lower"


# -- what actually predicts ---------------------------------------------------


def test_retrieval_confidence_predicts_well():
    """AUC 0.83. Week 8's refusal signal, doing a second job."""
    report = proxy_report(signals(), run()[3])
    assert report["retrieval_confidence"]["auc"] == pytest.approx(0.83, abs=0.03)


def test_and_so_does_a_signal_nobody_would_think_to_use():
    """**Distinct documents in the context: AUC 0.17 — strength 0.83, inverted.**

    As predictive as retrieval confidence, and pointing the other way: when the
    context is drawn from *one* document the answer is usually there, and when
    it is scraped from three the retriever was floundering.

    Nobody instruments this. It costs one line, needs no ground truth, and is
    available on every request."""
    report = proxy_report(signals(), run()[3])
    assert report["distinct_documents"]["auc"] == pytest.approx(0.17, abs=0.03)
    assert report["distinct_documents"]["strength"] == pytest.approx(0.83, abs=0.03)


def test_the_signals_a_dashboard_would_track_are_useless():
    """**The day.**

    Answer length: AUC 0.45. Citation count: 0.46. Both indistinguishable from
    chance.

    These are exactly what gets put on a dashboard — they are easy, they are
    always available, and they *feel* like quality. A system producing longer,
    more heavily cited answers looks better and is not.

    Being available is not the same as being informative, and the difference is
    one line of AUC away."""
    report = proxy_report(signals(), run()[3])
    assert report["answer_words"]["strength"] < 0.6
    assert report["citation_count"]["strength"] < 0.6
    assert useful_proxies(report) == ["distinct_documents", "retrieval_confidence"]


def test_the_floor_is_a_judgment_not_a_result():
    """0.7 is this course's choice and nothing derives it. Say so wherever you
    use it."""
    report = proxy_report(signals(), run()[3])
    assert len(useful_proxies(report, floor=0.4)) > len(useful_proxies(report, floor=0.9))
