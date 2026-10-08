"""Project 3 — the agent, and the refusal.

`test_the_best_configuration_does_not_ship` is the milestone.
"""

from functools import cache

import pytest

import raglab
from agent import Agent, agent_report, ship_check, verdict
from dense import DenseRetriever
from fuse import rrf
from lineage import supersession
from order import order_by_rank
from postings import Index
from raglab.generator import SimulatedGenerator
from rewrite import expand, prf_terms
from sections import section_corpus
from window import pack

CORPUS = raglab.corpus.load()
DOCS = {d.id: d.title + "\n" + d.text for d in CORPUS}
MDE = 0.1003


@cache
def graph():
    """Lazy: `supersession` is a lab, and a module-level call to a stub turns
    every test in this file into a collection error."""
    return supersession(DOCS)


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

    def shortlist(text, depth=10):
        return rrf([search(index, text, 60), retriever.search(text, 60)], 20, depth)

    def build(ranked, budget=800):
        selected, texts = pack(ranked, chunks, budget)
        return {c: texts[c] for c in order_by_rank(selected)}

    def rewrite(text):
        return expand(text, prf_terms(index, chunks, shortlist(text, 3), text))

    return chunks, shortlist, build, rewrite


def make(**kwargs):
    chunks, shortlist, build, rewrite = parts()
    return Agent(shortlist, build, SimulatedGenerator(), chunks, graph(), rewrite, **kwargs)


@cache
def report(**kwargs):
    chunks, _, _, _ = parts()
    return agent_report(make(**kwargs), dev(), chunks, graph())


@cache
def baseline():
    return report()


# -- the contract -------------------------------------------------------------


def test_every_stage_defaults_to_off():
    """Third week running. A stage nobody switched on deliberately is a stage
    nobody measured — and two of this week's four cost more than they buy."""
    config = make().config
    assert config["rewrite_queries"] is False
    assert config["hop"] is False
    assert config["max_iters"] == 1


def test_the_default_agent_is_week_eights_pipeline():
    """The baseline has to be runnable from the same object, or the comparison
    acquires a second variable nobody is tracking."""
    assert baseline()["answered"] == pytest.approx(0.70)
    assert baseline()["retrievals"] == 20
    assert baseline()["citing_superseded"] == ["r05", "r07", "r23"]
    assert baseline()["faithfulness"] == pytest.approx(1.0)


def test_a_setting_with_no_effect_is_reported_as_none():
    """`stop_at=0.8` on a single-shot agent is a config claiming a setting that
    did nothing. There is at least one of those in every agent anybody ships."""
    assert make().config["stop_at"] is None
    assert make(max_iters=3).config["stop_at"] == 0.8


def test_retrievals_and_tokens_are_different_costs():
    """The loop makes 44 retrievals for 20 queries and leaves the token count
    **exactly** where it was. A cost report denominated in tokens would call it
    free, and the token price is the one everybody watches."""
    looped = report(max_iters=3)
    assert looped["retrievals"] == 44
    assert looped["tokens_per_query"] == pytest.approx(baseline()["tokens_per_query"])


# -- the stages, individually -------------------------------------------------


def test_rewriting_alone_breaks_three_citations_nobody_was_watching():
    """Day 1 measured the rewrite costing 0.05 on the answered rate. It does
    something else nobody looked for: `r02`, `r20` and `r24` **start** citing
    superseded documents.

    Rewriting changes which documents are retrieved, and three of the newly
    retrieved ones are withdrawn. A second-order effect, in a metric the day's
    report did not carry, and this is why `citing_superseded` is a list of ids
    rather than a count — one stage sets it to zero and another adds to it."""
    result = verdict(baseline(), report(rewrite_queries=True), MDE)
    assert result["superseded_broken"] == ["r02", "r20", "r24"]
    assert result["superseded_fixed"] == ["r07"]
    assert result["answered_delta"] == pytest.approx(-0.05)


def test_the_hop_alone_is_the_cheapest_real_fix():
    """Three citations to zero at 1.25× the retrievals — and day 3 showed a
    week-2 metadata filter doing the same at 1.0×."""
    result = verdict(baseline(), report(hop=True), MDE)
    assert result["superseded_fixed"] == ["r05", "r07", "r23"]
    assert result["retrieval_multiple"] == pytest.approx(1.25)


def test_the_loop_alone_is_pure_cost():
    """2.2× the retrievals, zero movement in every metric in the report."""
    result = verdict(baseline(), report(max_iters=3), MDE)
    assert result["answered_delta"] == 0.0
    assert result["superseded_fixed"] == []
    assert result["retrieval_multiple"] == pytest.approx(2.2)


def test_two_stages_compose_into_a_gain_neither_has_alone():
    """Loop **and** hop: answered 0.70 → **0.75**, citations 3 → **0**.

    Neither stage does that by itself — the loop alone moves nothing and the hop
    alone costs 0.05. The loop's extra iterations change which documents are in
    the context, which changes which of them are superseded, which gives the hop
    something different to repair.

    This is the best result anybody gets on this corpus, and it is an interaction
    rather than a feature. Which means it is also the result least likely to
    survive a change to either stage."""
    result = verdict(baseline(), report(max_iters=3, hop=True), MDE)
    assert report(max_iters=3, hop=True)["answered"] == pytest.approx(0.75)
    assert report(max_iters=3, hop=True)["citing_superseded"] == []
    assert result["answered_delta"] == pytest.approx(0.05)
    assert report(hop=True)["answered"] == pytest.approx(0.65)
    assert report(max_iters=3)["answered"] == pytest.approx(0.70)


def test_a_dial_that_does_nothing_still_appears_in_the_config():
    """Turn query rewriting on **with** the loop and the report is byte-identical,
    because the loop already rewrites. The config says `rewrite_queries: True`
    and nothing downstream of it changed.

    A dial that does nothing is worse than a dial that hurts: it survives every
    review, it gets copied into the next system, and somebody eventually
    attributes the result to it."""
    assert report(rewrite_queries=True, hop=True, max_iters=3) == report(hop=True, max_iters=3)


# -- the verdict --------------------------------------------------------------


def test_the_best_configuration_does_not_ship():
    """**Project 3.**

    | | baseline | best agent |
    |---|---|---|
    | answered | 0.700 | **0.750** |
    | citing superseded | 3 | **0** |
    | retrievals | 20 | **49** |
    | faithfulness | 1.000 | 1.000 |

    The best numbers in the course, and `ship_check` refuses on two grounds:

    - **+0.05 is inside the MDE.** Week 9 measured 0.1003 for this eval set at
      this n. The gain is one query. It is not distinguishable from zero, and
      the fact that it took four days of work to produce does not change that
    - **2.45× the retrievals**, for it

    So the recommendation Project 3 asks for is: **ship the hop, do not ship the
    loop, and go and write more queries.** Week 9 priced that too — five points
    costs seventy-seven queries — and it is the only one of the three that would
    let you find out whether the agent works."""
    best = report(max_iters=3, hop=True)
    result = verdict(baseline(), best, MDE)

    assert result["answered_delta"] == pytest.approx(0.05)
    assert result["detectable"] is False
    assert result["retrieval_multiple"] == pytest.approx(2.45)

    reasons = ship_check(result)
    assert len(reasons) == 2
    assert any("inside the MDE" in r for r in reasons)
    assert any("2.45" in r for r in reasons)


def test_no_configuration_clears_the_floor():
    """Six configurations, and not one produces a detectable change in the
    answered rate. The largest effect available from everything this week built
    is half the smallest effect this eval set can resolve."""
    configs = (
        {},
        {"rewrite_queries": True},
        {"hop": True},
        {"max_iters": 3},
        {"rewrite_queries": True, "hop": True},
        {"max_iters": 3, "hop": True},
    )
    deltas = [verdict(baseline(), report(**c), MDE) for c in configs]
    assert not any(v["detectable"] for v in deltas)
    assert max(abs(v["answered_delta"]) for v in deltas) == pytest.approx(0.05)
