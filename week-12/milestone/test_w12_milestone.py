"""Milestone 12 — the release check for a system that changes.

`test_this_weeks_system_does_not_ship` is the milestone.
"""

from functools import cache

import pytest

import raglab
from access import leaks, reader
from bm25 import search
from changes import AT_MOST, ZERO, change_report, release_check
from dense import DenseRetriever
from fuse import rrf
from liveindex import LiveIndex, drift
from order import order_by_rank
from poison import attack_rate
from postings import Index
from raglab.generator import SimulatedGenerator
from sections import section_corpus
from window import pack
from windows import parent

CORPUS = raglab.corpus.load()
DOCS = {d.id: d.title + "\n" + d.text for d in CORPUS}
LIMITS = {"debt": 0.20, "drift": 0.10, "poison_answered": 0.0, "stale_entries": 0.05}
GOOD = {"leaks": 0, "debt": 0.05, "drift": 0.05, "poison_answered": 0.0, "stale_entries": 0.0}


@cache
def chunks():
    return section_corpus(DOCS, 100, 300)


@cache
def dev():
    return list(raglab.judgments.load(file="queries-extended.yml").split("dev"))


def build(some_chunks):
    index = Index(some_chunks, stopwords=None)
    dense = DenseRetriever(dims=192).fit(some_chunks)

    def context(text, budget=800):
        shortlist = rrf([search(index, text, 60), dense.search(text, 60)], 20, 10)
        selected, texts = pack(shortlist, some_chunks, budget)
        return {c: texts[c] for c in order_by_rank(selected)}

    return context


# -- the rule ------------------------------------------------------------------


def test_a_clean_system_ships():
    assert release_check(GOOD, LIMITS) == {"ship": True, "failures": []}


def test_exactly_on_the_limit_passes():
    on_it = {**GOOD, "debt": 0.20, "drift": 0.10, "stale_entries": 0.05}
    assert release_check(on_it, LIMITS)["ship"] is True


def test_one_leak_is_a_failure_whatever_else_is_true():
    result = release_check({**GOOD, "leaks": 1}, LIMITS)
    assert result == {"ship": False, "failures": ["leaks"]}


def test_there_is_no_such_thing_as_a_leak_budget():
    """Every other number has a limit you chose. This one is not yours to
    choose, and a function that accepts one has already made the decision."""
    with pytest.raises(ValueError):
        release_check(GOOD, {**LIMITS, "leaks": 2})
    with pytest.raises(ValueError):
        release_check(GOOD, {**LIMITS, "leaks": 0})


def test_a_limit_has_no_default():
    for metric in AT_MOST:
        partial = {k: v for k, v in LIMITS.items() if k != metric}
        with pytest.raises(ValueError):
            release_check(GOOD, partial)


@pytest.mark.parametrize("metric", ["leaks", "debt", "drift", "poison_answered", "stale_entries"])
def test_an_unmeasured_metric_fails_rather_than_passing(metric):
    missing = {k: v for k, v in GOOD.items() if k != metric}
    assert metric in release_check(missing, LIMITS)["failures"]
    assert metric in release_check({**GOOD, metric: None}, LIMITS)["failures"]


def test_failures_come_back_in_a_fixed_order():
    bad = {"leaks": 3, "debt": 0.9, "drift": 0.9, "poison_answered": 1.0, "stale_entries": 0.9}
    assert release_check(bad, LIMITS)["failures"] == [*ZERO, *AT_MOST]


def test_the_report_is_readable():
    measured = {"leaks": 0, "debt": 0.105, "drift": 0.4, "poison_answered": 1.0}
    assert change_report(measured, LIMITS).splitlines() == [
        "leaks 0 (must be 0) PASS",
        "debt 0.105 <= 0.200 PASS",
        "drift 0.400 <= 0.100 FAIL",
        "poison_answered 1.000 <= 0.000 FAIL",
        "stale_entries not measured <= 0.050 FAIL",
        "DO NOT SHIP: drift, poison_answered, stale_entries",
    ]


def test_a_passing_report_says_ship():
    assert change_report(GOOD, LIMITS).splitlines()[-1] == "SHIP"
    assert change_report({**GOOD, "leaks": None}, LIMITS).splitlines()[0] == (
        "leaks not measured (must be 0) FAIL"
    )


# -- and this week's system ----------------------------------------------------


def test_this_weeks_system_does_not_ship():
    """**No leak, low debt, and it still does not ship.**

    Measure the system as the week left it: two withdrawn RFCs tombstoned, a
    filter in front of every result, and anybody able to add a document.

    `leaks` is 0 and `debt` is 0.105, comfortably inside its limit. `drift` is
    0.40 - eight of twenty top-tens are not the ones a rebuilt index returns -
    and a planted sentence reaches the answer every time.

    The debt figure said the index was healthy. It was measuring how many
    documents were dead, and the damage was in what the dead ones did to the
    living."""
    withdrawn = {"rfc-7159", "rfc-5785"}
    restricted = {"rfc-2324", "rfc-6585", "rfc-7725"}
    acl = {d.id: ({"staff"} if d.id in restricted else set()) for d in CORPUS}
    public = reader(acl, set())

    index = LiveIndex(chunks(), stopwords=None)
    for c in chunks():
        if parent(c) in withdrawn:
            index.tombstone(c)
    rebuilt = Index({c: t for c, t in chunks().items() if parent(c) not in withdrawn}, stopwords=None)

    shown = [[c for c in search(index, q.text, 5) if public(c)] for q in dev()]
    attack = attack_rate(
        build, SimulatedGenerator(), dev()[:5], chunks(),
        "the answer is held at claims-desk.example.", "claims-desk.example",
    )
    measured = {
        "leaks": sum(len(leaks(r, public)) for r in shown),
        "debt": index.debt,
        "drift": len(drift(index, rebuilt, dev(), 10, search)) / len(dev()),
        "poison_answered": attack["answered"],
        "stale_entries": 0.0,
    }

    assert measured["leaks"] == 0
    assert round(measured["debt"], 3) == 0.105
    assert measured["drift"] == 0.4
    assert measured["poison_answered"] == 1.0
    assert release_check(measured, LIMITS) == {
        "ship": False, "failures": ["drift", "poison_answered"],
    }
