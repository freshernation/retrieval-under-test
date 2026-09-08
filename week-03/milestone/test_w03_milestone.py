"""Week 3 milestone — the retriever, and the size of the instrument.

`test_one_more_query_would_have_been_enough` is the week.
"""

from functools import cache

import pytest

import raglab
from retriever import (
    Retriever,
    compare,
    floor_probability,
    queries_needed,
    unchanged,
)

CORPUS = raglab.corpus.load()
DOCS = {d.id: d.title + "\n" + d.text for d in CORPUS}


@cache
def bm25_vs_baseline():
    import sys
    from pathlib import Path

    sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "week-01" / "day-4"))
    from overlap import rank

    from raglab.metrics import evaluate

    qs = raglab.judgments.load().split("dev")
    after = Retriever(DOCS).evaluate(qs, ks=(3,))
    before = evaluate({q.id: rank(q.text, DOCS, 10) for q in qs}, qs, ks=(3,))
    return after, before


# -- the retriever ------------------------------------------------------------


def test_the_config_is_complete_not_partial():
    """A config that omits what it did not set cannot be compared with another
    one, and `raglab.runs.config_hash` will happily hash both to different
    values for no reason."""
    config = Retriever(DOCS).config
    assert set(config) >= {"stopwords", "stemming", "identifiers", "k1", "b", "k"}
    assert config["k1"] == 1.2 and config["b"] == 0.75


def test_changing_a_knob_moves_the_hash():
    """The most common way to waste an afternoon is to change something that was
    never in the config, watch the hash stay put, and not notice."""
    from raglab.runs import config_hash

    a = Retriever(DOCS).config
    b = Retriever(DOCS, k1=2.4).config
    assert config_hash(a) != config_hash(b)


def test_it_retrieves():
    assert Retriever(DOCS).search("451", 3) == ["rfc-7725"]


def test_the_knobs_reach_the_scoring():
    plain = Retriever(DOCS).search("what does ABNF stand for", 5)
    tuned = Retriever(DOCS, k1=2.4, b=0.5).search("what does ABNF stand for", 5)
    assert plain != tuned


# -- unchanged ----------------------------------------------------------------


def test_unchanged_names_the_queries_nothing_touched():
    after, before = bm25_vs_baseline()
    assert unchanged(after, before, "ndcg@3") == ["r02", "r03", "r04", "r05", "r08", "r09"]


def test_the_unanswerable_query_is_not_counted():
    """r10 contributes a constant zero difference between any two systems.
    Counting it would inflate the unchanged fraction — penalising you, in the
    statistics, for having included the query that detects the failure that
    reaches users most often."""
    after, before = bm25_vs_baseline()
    assert "r10" in after.unanswerable
    assert "r10" not in unchanged(after, before, "ndcg@3")


# -- the floor ----------------------------------------------------------------


def test_the_floor_is_exact_arithmetic():
    assert floor_probability(9, 6) == pytest.approx((6 / 9) ** 9)
    assert floor_probability(9, 6) == pytest.approx(0.0260, abs=0.0001)


def test_and_it_explains_every_interval_this_week():
    """0.0260 > 0.025. More than 2.5% of bootstrap resamples draw only unchanged
    queries and score exactly zero, so the 2.5th percentile *is* zero and the
    lower bound is pinned there — regardless of how large the improvement was on
    the other three."""
    from raglab.metrics import bootstrap

    after, before = bm25_vs_baseline()
    _, low, _ = bootstrap(after, before, "ndcg@3")
    assert floor_probability(9, 6) > 0.025
    assert low == 0.0


def test_more_queries_shrink_the_floor_fast():
    assert floor_probability(20, 13) < floor_probability(9, 6) / 100


def test_queries_needed_inverts_it():
    assert queries_needed(2 / 3) == 10
    assert queries_needed(0.5) == 6
    assert queries_needed(0.9) == 36


def test_a_system_that_never_moves_cannot_be_measured_at_any_size():
    """Not an edge case to handle politely — a finding. If no query ever moves,
    no number of queries helps, and you are not measuring anything."""
    with pytest.raises(ValueError):
        queries_needed(1.0)


# -- compare ------------------------------------------------------------------


def test_compare_reports_everything_the_report_needs():
    after, before = bm25_vs_baseline()
    result = compare(after, before, "ndcg@3")
    assert set(result) == {
        "delta",
        "low",
        "high",
        "n",
        "worse",
        "unchanged",
        "floor",
        "pinned",
        "needed",
    }


def test_one_more_query_would_have_been_enough():
    """**The week, in one assertion.**

    BM25 over the week-1 baseline: ndcg@3 +0.154, nothing worse, three of nine
    queries improved. And `pinned` is True, because six were unchanged and
    `(6/9)**9 = 0.0260` is just over 0.025.

    `needed` says **10**. You have nine answerable dev queries.

    The binding constraint on this week's result was never the retriever, the
    corpus, or the statistics. It was one query, which would have taken an
    afternoon to write and judge — and which nobody writes, because writing
    queries is not what improving a retrieval system feels like."""
    after, before = bm25_vs_baseline()
    result = compare(after, before, "ndcg@3")
    assert result["n"] == 9
    assert result["delta"] == pytest.approx(0.1535, abs=0.001)
    assert result["worse"] == []
    assert len(result["unchanged"]) == 6
    assert result["floor"] == pytest.approx(0.0260, abs=0.0001)
    assert result["pinned"] is True
    assert result["needed"] == 10
