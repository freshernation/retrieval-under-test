"""Day 3 — tracing, and the walk a machine can do.

`test_nothing_failed_at_station_six` is the day.
"""

from functools import cache

import pytest

import raglab
from dense import DenseRetriever
from faithful import faithfulness
from fuse import rrf
from order import order_by_rank
from postings import Index
from raglab.generator import SimulatedGenerator
from sections import section_corpus
from tracing import (
    NO_FAILURE,
    STATION_1,
    STATION_2,
    STATION_4,
    STATION_5,
    STATION_6,
    Trace,
    attribute,
    attribution_report,
    critical_path,
    missing_ids,
)
from window import pack

CORPUS = raglab.corpus.load()
DOCS = {d.id: d.title + "\n" + d.text for d in CORPUS}


@cache
def dev():
    return list(raglab.judgments.load(file="queries-extended.yml").split("dev"))


@cache
def traced():
    """Run the pipeline and keep a trace per query. Durations are this laptop's;
    the ids are not."""
    import sys
    import time
    from pathlib import Path

    root = Path(__file__).resolve().parents[2]
    for day in ("day-3", "day-2", "day-1"):
        sys.path.insert(0, str(root / "week-03" / day))
    from bm25 import search

    chunks = section_corpus(DOCS, 100, 300)
    index = Index(chunks, stopwords=None)
    retriever = DenseRetriever(dims=192).fit(chunks)
    generator = SimulatedGenerator()

    traces, faithfuls = {}, {}
    for query in dev():
        trace = Trace(query.id)

        start = time.perf_counter()
        lexical = search(index, query.text, 60)
        trace.record("lexical", (time.perf_counter() - start) * 1000, lexical[:10])

        start = time.perf_counter()
        semantic = retriever.search(query.text, 60)
        trace.record("dense", (time.perf_counter() - start) * 1000, semantic[:10])

        start = time.perf_counter()
        shortlist = rrf([lexical, semantic], 20, 10)
        trace.record("fuse", (time.perf_counter() - start) * 1000, shortlist)
        trace.record("shortlist", 0.0, shortlist)

        selected, texts = pack(shortlist, chunks, 800)
        context = {c: texts[c] for c in order_by_rank(selected)}
        trace.record("context", 0.0, tuple(context))

        start = time.perf_counter()
        answer = generator.answer(query.text, context)
        trace.record("generate", (time.perf_counter() - start) * 1000, ())

        traces[query.id] = trace
        faithfuls[query.id] = faithfulness(answer, context, chunks)
    return chunks, traces, faithfuls


# -- the record ---------------------------------------------------------------


def test_the_total_is_not_the_latency():
    """A sum of spans excludes the gaps between them, and the gaps are where a
    queue hides. Report both or report neither."""
    trace = Trace("q1")
    trace.record("lexical", 8.0, ("a", "b"))
    trace.record("generate", 2.0)
    assert trace.total == pytest.approx(10.0)
    assert critical_path(trace) == ("lexical", pytest.approx(0.8))
    assert trace.ids("generate") == ()
    assert trace.ids("nonexistent") == ()


def test_the_cheapest_field_in_the_system_is_the_one_that_gets_dropped():
    """Two lists of ten short strings per request. Without them a trace can time
    an incident and cannot explain one, and the explanation is the reason anyone
    turned tracing on."""
    timing_only = Trace("q1")
    timing_only.record("lexical", 8.0)
    timing_only.record("generate", 2.0)
    assert missing_ids(timing_only) == ["context", "shortlist"]

    _, traces, _ = traced()
    assert missing_ids(traces["r01"]) == []


# -- the walk -----------------------------------------------------------------


def test_the_walk_stops_at_the_first_station_that_failed():
    """Never fix downstream of the break. The rule has been the spine of the
    course since week 1; here it is nine lines of code over a record you were
    already keeping."""
    chunks, traces, faithfuls = traced()
    assert attribute(traces["r10"], _q("r10"), chunks, 1.0) == STATION_1
    assert attribute(traces["r19"], _q("r19"), chunks, 1.0) == STATION_4
    assert attribute(traces["r09"], _q("r09"), chunks, 1.0) == STATION_5


def test_a_downstream_failure_cannot_be_reported_while_an_upstream_one_exists():
    """`r19`'s answer is unfaithful *and* its shortlist never had the answer.
    The walk reports retrieve, because fixing the prompt for a query whose
    candidates are empty is the characteristic wasted week."""
    chunks, traces, _ = traced()
    assert attribute(traces["r19"], _q("r19"), chunks, 0.0) == STATION_4
    assert attribute(traces["r01"], _q("r01"), chunks, 0.0) == STATION_6


def test_the_attribution_finds_exactly_week_eights_six_wrong_answers():
    """Week 8 measured six of twenty answers as confident prose about questions
    the system could not answer. The walk names a station for all six and clears
    the other fourteen — without being told which six they were."""
    chunks, traces, faithfuls = traced()
    stations = {q.id: attribute(traces[q.id], q, chunks, faithfuls[q.id]) for q in dev()}
    broken = sorted(i for i, s in stations.items() if s != NO_FAILURE)
    assert broken == ["r09", "r10", "r19", "r20", "r21", "r23"]


def test_nothing_failed_at_station_six():
    """**The day.**

    | station | queries |
    |---|---|
    | 1 corpus | 1 |
    | 2 chunk | **0** |
    | 4 retrieve | 2 |
    | 5 rank | 3 |
    | 6 generate | **0** |
    | 7 none | 14 |

    Zero at station 6, and station 6 is where the work goes. Zero at station 2,
    and the chunker is the other thing people rewrite.

    Five of the six failures are the candidate set — two queries whose shortlist
    never contained the answer (week 6 named the same pair unreachable) and three
    where the word budget dropped a chunk that did.

    The trace does not make this easier to fix. It makes it impossible to spend
    the week on the prompt by accident."""
    chunks, traces, faithfuls = traced()
    report = attribution_report(
        attribute(traces[q.id], q, chunks, faithfuls[q.id]) for q in dev()
    )
    assert report == {
        STATION_1: 1,
        STATION_2: 0,
        STATION_4: 2,
        STATION_5: 3,
        STATION_6: 0,
        NO_FAILURE: 14,
    }


def test_seven_none_does_not_mean_the_answer_was_right():
    """`r05` asks whether JSON must be UTF-8. Every station did its job, the
    answer is perfectly faithful, and it is grounded in RFC 7159 — withdrawn in
    December 2017 and wrong about exactly this.

    The attribution walk is blind to it for the same reason week 8's faithfulness
    was: the disqualifying fact is in a different document, and no station
    failed. A clean trace is not a correct answer, and station 7 is where that
    belongs."""
    chunks, traces, faithfuls = traced()
    assert attribute(traces["r05"], _q("r05"), chunks, faithfuls["r05"]) == NO_FAILURE
    assert faithfuls["r05"] == pytest.approx(1.0)
    assert any(c.startswith("rfc-7159") for c in traces["r05"].ids("context"))


def test_station_two_is_empty_and_that_is_a_result():
    """No query in the set has an answer that exists in the corpus and in no
    chunk. The section chunker is not the problem on this corpus, which is worth
    knowing before a week is spent on a better one."""
    chunks, traces, faithfuls = traced()
    stations = [attribute(traces[q.id], q, chunks, faithfuls[q.id]) for q in dev()]
    assert STATION_2 not in stations


def _q(query_id: str):
    return next(q for q in dev() if q.id == query_id)
