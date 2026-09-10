"""Day 2 — validating a judge.

`test_the_judge_scores_exactly_what_a_coin_that_always_says_yes_scores` is the day.
"""

from functools import cache

import pytest

import raglab
from dense import DenseRetriever
from fuse import rrf
from ground import answer_all
from judgecheck import (
    accuracy,
    constant_baseline,
    kappa,
    labels,
    length_probe,
    position_probe,
    self_agreement,
    validated,
)
from order import order_by_rank
from raglab.generator import SimulatedGenerator
from raglab.judge import SimulatedJudge
from refuse import has_answer
from sections import section_corpus
from window import pack

CORPUS = raglab.corpus.load()
DOCS = {d.id: d.title + "\n" + d.text for d in CORPUS}
SOURCE = "The 429 status code indicates that the user has sent too many requests."
SHORT = "The 429 status code indicates rate limiting."
PADDING = "status code indicates that the user has sent too many requests"


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
    cases = {q.id: (q.text, answers[q.id].text, contexts[q.id]) for q in dev()}
    truth = {q.id: int(has_answer(q, contexts[q.id])) for q in dev()}
    return cases, truth


# -- the measurement ----------------------------------------------------------


def test_accuracy_needs_a_baseline_to_mean_anything():
    """Two lines, computed before looking at the judge."""
    _, truth = run()
    base = constant_baseline(truth, label=1)
    assert base["accuracy"] == pytest.approx(0.70)
    assert base["kappa"] == pytest.approx(0.0, abs=0.001)


def test_kappa_is_week_ones_function_doing_a_new_job():
    assert kappa({"a": 1, "b": 0}, {"a": 1, "b": 0}) == pytest.approx(1.0)
    assert kappa({"a": 1, "b": 1}, {"a": 1, "b": 1}) == pytest.approx(1.0)


# -- the day ------------------------------------------------------------------


def test_the_judge_scores_exactly_what_a_coin_that_always_says_yes_scores():
    """**The day.**

    The judge labels **20 of 20 answers "good"**. Its accuracy is **0.70** and
    its Cohen's kappa is **0.000**.

    A judge that returns "yes" without reading anything scores 0.70 and 0.000.
    They are indistinguishable, and the accuracy figure alone would have looked
    respectable on a slide.

    Six of those twenty answers are confident prose about questions the system
    could not answer, and the judge called every one of them good — because it
    is a faithfulness judge, the answers *are* faithful, and week 8's keystone
    does not stop being true because a model is doing the checking."""
    cases, truth = run()
    judged = labels(SimulatedJudge(), cases)

    assert sum(judged.values()) == 20
    assert accuracy(judged, truth) == pytest.approx(0.70)
    assert kappa(judged, truth) == pytest.approx(0.0, abs=0.001)

    base = constant_baseline(truth, label=1)
    assert accuracy(judged, truth) == pytest.approx(base["accuracy"])
    assert kappa(judged, truth) == pytest.approx(base["kappa"], abs=0.001)


# -- self-consistency ---------------------------------------------------------


def test_a_clean_judge_agrees_with_itself():
    cases, _ = run()
    report = self_agreement(SimulatedJudge(), cases)
    assert report["identical_scores"] == report["n"] == 20
    assert report["mean_drift"] == 0.0
    assert report["label_agreement"] == 1.0


def test_a_noisy_judge_sets_a_ceiling_on_everything_downstream():
    """Sixteen of twenty scores differ between two runs, mean drift 0.148.

    If a judge changes its mind about a fifth of cases, no difference smaller
    than that is detectable however many queries you have — which is week 3's
    floor arithmetic, arriving through a completely different door."""
    cases, _ = run()
    report = self_agreement(SimulatedJudge(noise=0.6), cases)
    assert report["identical_scores"] < 6
    assert report["mean_drift"] == pytest.approx(0.148, abs=0.03)


def test_score_drift_and_label_drift_are_different_problems():
    """A judge can move a lot in score while never crossing the threshold —
    harmless for a gate, fatal for a trend line."""
    cases, _ = run()
    report = self_agreement(SimulatedJudge(noise=0.6), cases)
    assert report["mean_drift"] > 0.1
    assert report["label_agreement"] >= 0.9


# -- controlled bias probes ---------------------------------------------------


def test_padding_alone_raises_the_score_even_with_no_length_bias_set():
    """**The uncomfortable one.**

    The clean judge scores the short claim 0.71 and the padded one 0.86 — and
    `length_bias` is zero.

    The bias is *in the metric*, not in a flag: more words means more words
    overlapping the context. Any word-overlap judge rewards verbosity by
    construction, and this is the proxy week 8 used, so week 8's faithfulness
    numbers have this in them too."""
    cases, _ = run()
    context = {"c": SOURCE}
    probe = length_probe(SimulatedJudge(), "q", SHORT, PADDING, context)
    assert probe["padded_words"] > 3 * probe["short_words"]
    assert probe["padded"] > probe["short"] + 0.1


def test_and_an_explicit_length_bias_makes_it_worse():
    context = {"c": SOURCE}
    clean = length_probe(SimulatedJudge(), "q", SHORT, PADDING, context)
    biased = length_probe(SimulatedJudge(length_bias=0.5), "q", SHORT, PADDING, context)
    assert biased["padded"] >= clean["padded"]
    assert biased["padded"] == pytest.approx(1.0, abs=0.01)


def test_comparing_an_answer_with_itself_should_be_a_tie():
    """Anything else means position decides something, and every pairwise result
    is partly a measurement of which one you showed first."""
    context = {"c": SOURCE}
    assert position_probe(SimulatedJudge(), "q", SHORT, context)["identical_pair"] == "tie"
    biased = position_probe(SimulatedJudge(position_bias=0.1), "q", SHORT, context)
    assert biased["identical_pair"] == "first"


# -- the bar ------------------------------------------------------------------


def test_the_validation_bar_is_low_and_this_judge_fails_it():
    """Three cheap conditions: beats the constant baseline on kappa, agrees with
    itself, is not length-sensitive.

    Passing means *not known to be useless*. It does not mean good — and this
    judge does not even pass, because its kappa is the baseline's."""
    cases, truth = run()
    judged = labels(SimulatedJudge(), cases)
    base = constant_baseline(truth, label=1)
    consistency = self_agreement(SimulatedJudge(), cases)
    report = {
        "kappa": kappa(judged, truth),
        "baseline_kappa": base["kappa"],
        "label_agreement": consistency["label_agreement"],
        "length_sensitive": True,
    }
    assert validated(report) is False

    report["length_sensitive"] = False
    assert validated(report) is False
