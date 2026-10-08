"""Milestone 10 — the pipeline behind a service boundary.

`test_the_service_refuses_to_ship_itself` is the milestone.
"""

from functools import cache

import pytest

import raglab
from caching import LRU
from dense import DenseRetriever
from fuse import rrf
from order import order_by_rank
from postings import Index
from raglab.generator import SimulatedGenerator
from sections import section_corpus
from service import Service, service_report, ship_check, slo
from tracing import NO_FAILURE, STATION_4, STATION_5, STATION_6
from window import pack

CORPUS = raglab.corpus.load()
DOCS = {d.id: d.title + "\n" + d.text for d in CORPUS}


@cache
def dev():
    return list(raglab.judgments.load(file="queries-extended.yml").split("dev"))


@cache
def parts():
    import sys
    from pathlib import Path

    root = Path(__file__).resolve().parents[2]
    for day in ("day-3", "day-2", "day-1"):
        sys.path.insert(0, str(root / "week-03" / day))
    from bm25 import search

    chunks = section_corpus(DOCS, 100, 300)
    index = Index(chunks, stopwords=None)
    retriever = DenseRetriever(dims=192).fit(chunks)

    def build_context(text, budget=800):
        shortlist = rrf([search(index, text, 60), retriever.search(text, 60)], 20, 10)
        selected, texts = pack(shortlist, chunks, budget)
        return shortlist, {c: texts[c] for c in order_by_rank(selected)}

    return chunks, index, build_context


def make(**kwargs):
    chunks, index, build_context = parts()
    return Service(build_context, SimulatedGenerator(), chunks, index, **kwargs)


# -- the contract -------------------------------------------------------------


def test_the_cache_defaults_to_off():
    """Week 7's rule, one week on. A cache does not merely speed the system up —
    day 2 measured a cached answer grounded in a withdrawn RFC — so it is a
    change to what the system says, and it goes in the config."""
    assert make().config["cache"] is False
    assert make(cache=LRU(capacity=5)).config["cache"] is True
    assert make(cache=LRU(capacity=5)).config["cache_capacity"] == 5


def test_a_cached_run_and_an_uncached_run_are_two_different_systems():
    """So the run id must separate them. Two configs that differ only in the
    cache must not hash alike, or week 1's run ledger will quietly compare
    them."""
    assert raglab.runs.config_hash(make().config) != raglab.runs.config_hash(
        make(cache=LRU()).config
    )


def test_the_service_hands_back_its_trace():
    """A service that swallows its own trace is a service you debug by adding
    print statements to somebody else's code."""
    answer, context, trace = make().answer(dev()[0])
    assert trace.query_id == dev()[0].id
    assert trace.ids("shortlist")
    assert trace.ids("context")
    assert set(trace.ids("context")) <= set(trace.ids("shortlist"))


def test_a_second_identical_request_is_served_from_the_cache():
    service = make(cache=LRU())
    service.answer(dev()[0])
    _, _, trace = service.answer(dev()[0])
    assert service.cache.hit_rate == pytest.approx(0.5)
    assert trace.ids("shortlist"), "a cache hit still produces a complete trace"


# -- the report ---------------------------------------------------------------


def test_the_service_report_carries_no_quality_number():
    """Deliberate. The quality numbers are weeks 8 and 9's, and week 9 measured
    what happens when a quality-shaped number reaches a dashboard."""
    report = service_report(make(), dev(), parts()[0])
    assert "faithfulness" not in report
    assert "answered" not in report
    assert set(report) == {
        "n",
        "work_p50",
        "work_p95",
        "tokens_per_query",
        "attribution",
        "cache",
        "exceeds",
    }


def test_the_report_states_the_tail_next_to_the_middle():
    """p50 379, p95 829. One number would have been a lie of omission."""
    report = service_report(make(), dev(), parts()[0])
    assert report["work_p50"] == 379.0
    assert report["work_p95"] == 829.0
    assert report["tokens_per_query"] == pytest.approx(885.0, abs=1.0)


def test_the_attribution_names_five_candidate_set_failures_and_no_prompt_failure():
    report = service_report(make(), dev(), parts()[0])
    assert report["attribution"][STATION_4] == 2
    assert report["attribution"][STATION_5] == 3
    assert report["attribution"][STATION_6] == 0
    assert report["attribution"][NO_FAILURE] == 14


# -- the refusal --------------------------------------------------------------


def test_an_slo_target_has_no_default():
    """Nothing in this repository derives a latency target. A default would read
    as though something did."""
    report = service_report(make(), dev(), parts()[0])
    assert slo(report, {"tokens_per_query": 1000})["tokens_per_query"]["met"] is True
    assert slo(report, {"tokens_per_query": 500})["tokens_per_query"]["met"] is False
    assert slo(report, {})== {}


def test_an_unmeasured_metric_fails_its_slo_rather_than_passing_it():
    """A target naming something the report does not contain is not satisfied.
    Treating a missing number as a pass is how an SLO survives the deletion of
    the metric behind it."""
    report = service_report(make(), dev(), parts()[0])
    assert slo(report, {"p99_ms": 250})["p99_ms"]["met"] is False


def test_the_service_refuses_to_ship_itself():
    """**The milestone.**

    Every SLO met, no stage over budget, and `ship_check` still refuses — because
    the attribution report has six failures in it, and an operational green light
    over a system that cannot answer six of twenty questions is the thing this
    course exists to prevent.

    Nothing was broken this week. The pipeline is exactly as good as it was on
    Friday of week 8, it is now fast, cached, traced and priced, and the refusal
    is the same refusal. **Packaging is not improvement**, and a service report
    that could not say so would be a worse artefact than no service report."""
    report = service_report(make(), dev(), parts()[0])
    met = slo(report, {"tokens_per_query": 1000, "work_p95": 1000})
    assert all(row["met"] for row in met.values())
    assert report["exceeds"] == []

    reasons = ship_check(report, met)
    assert len(reasons) == 3
    assert any("station 4 retrieve" in r for r in reasons)
    assert any("station 5 rank" in r for r in reasons)
    assert any("station 1 corpus" in r for r in reasons)
    assert not any("6 generate" in r for r in reasons)
