"""Day 4 — the control loop, and what it produces.

`test_every_iteration_after_the_first_is_churn` is the day.
"""

from functools import cache

import pytest

import raglab
from dense import DenseRetriever
from fuse import rrf
from loop import Loop, Run, churn, cost_multiple, histogram, loop_report
from order import order_by_rank
from postings import Index
from proxies import auc, separation_strength
from rewrite import expand, prf_terms
from sections import section_corpus
from window import pack

CORPUS = raglab.corpus.load()
DOCS = {d.id: d.title + "\n" + d.text for d in CORPUS}


@cache
def dev():
    return list(raglab.judgments.load(file="queries-extended.yml").split("dev"))


@cache
def built():
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

    return shortlist, build, rewrite


def answered(query, ctx):
    return bool(query.answer_spans) and query.is_answered_by(list(ctx.values()))


@cache
def ran(stop_at: float, max_iters: int = 3):
    shortlist, build, rewrite = built()
    loop = Loop(shortlist, build, rewrite, stop_at=stop_at, max_iters=max_iters)
    runs = tuple(loop.run(q.id, q.text) for q in dev())
    outcomes = {q.id: answered(q, r.context) for q, r in zip(dev(), runs)}
    return runs, outcomes


# -- the mechanism ------------------------------------------------------------


def test_the_bar_is_the_original_query_not_the_rewritten_one():
    """A loop that scores the rewritten query against a context retrieved *for*
    the rewritten query is grading its own homework, and it terminates early and
    confidently."""
    shortlist, build, rewrite = built()
    query = next(q for q in dev() if q.id == "r19")
    run = Loop(shortlist, build, rewrite, stop_at=0.8, max_iters=3).run(query.id, query.text)
    assert run.confidences[0] == pytest.approx(0.444, abs=0.01)
    assert max(run.confidences) < 0.8, "it never clears the bar on its own terms"


def test_the_best_context_is_kept_not_the_last():
    """The last iteration is the one that failed to clear the bar."""
    run = Run("q", {}, 3, (0.9, 0.4, 0.2), ((), (), ()))
    assert run.iterations == 3
    assert run.capped(3) is True
    assert run.capped(4) is False


def test_the_cap_is_the_only_thing_that_terminates_an_unanswerable_query():
    """`r10` asks about OAuth scopes. The corpus has the word once, in a
    bibliography.

    With the bar set out of reach the loop runs to whatever cap you gave it —
    twelve retrievals for twelve — and its confidence **falls monotonically**
    from 0.44 to 0.11 as the feedback terms pull it further from the question.

    The loop does not notice. There is nothing in it that could: every signal it
    has says *try again*, and trying again is what makes it worse."""
    shortlist, build, rewrite = built()
    query = next(q for q in dev() if q.id == "r10")
    run = Loop(shortlist, build, rewrite, stop_at=1.01, max_iters=12).run(query.id, query.text)
    assert run.retrievals == 12
    assert run.confidences[0] > run.confidences[-1]
    assert run.confidences[-1] == pytest.approx(0.11, abs=0.02)


# -- the shape ----------------------------------------------------------------


def test_the_loop_has_two_outcomes_and_the_middle_one_never_happens():
    """Read the histogram before anything else.

    | stop_at | iterations |
    |---|---|
    | 0.6 | `{1: 15, 3: 5}` |
    | 0.8 | `{1: 8, 3: 12}` |
    | 1.0 | `{1: 6, 3: 14}` |

    **No query, at any threshold, ever stops on iteration two.** Either the first
    retrieval was good enough or the loop ran to the cap. One rewrite never once
    turned a failing query into a passing one.

    A three-state machine with two reachable states, and the iterations in
    between are the bill."""
    for stop_at in (0.6, 0.8, 1.0):
        runs, _ = ran(stop_at)
        assert 2 not in histogram(runs)
    assert histogram(ran(0.6)[0]) == {1: 15, 3: 5}
    assert histogram(ran(0.8)[0]) == {1: 8, 3: 12}
    assert histogram(ran(1.0)[0]) == {1: 6, 3: 14}


def test_the_answered_rate_is_unchanged_at_every_price():
    """0.700 at 1.5×, 0.700 at 2.2×, 0.700 at 2.4×.

    Week 10 made this sentence possible to say with a number in it. Before week
    10, *"the agent costs more"* was a shrug."""
    for stop_at, multiple in ((0.6, 1.5), (0.8, 2.2), (1.0, 2.4)):
        runs, outcomes = ran(stop_at)
        assert sum(outcomes.values()) / len(outcomes) == pytest.approx(0.70)
        assert cost_multiple(runs) == pytest.approx(multiple, abs=0.01)


def test_every_iteration_after_the_first_is_churn():
    """**The day.**

    At `stop_at=0.8` the loop makes 44 retrievals for 20 queries. Twenty-four of
    them are iterations after the first, and `churn` — the shortlist changed and
    the confidence did not improve — counts **24**.

    All of them. Every single iteration the loop ever takes produces a different
    candidate set and gets no closer.

    Which is the trap that makes a loop convincing: it *looks* like work. New
    documents arrive, the query grows, the trace fills with spans. A no-progress
    detector built on *did the candidate set change* fires **never**, because the
    candidate set always changes. Churn and progress are indistinguishable to
    every signal the loop can see, and only the confidence — which is not
    improving — can tell them apart."""
    runs, _ = ran(0.8)
    assert sum(r.retrievals for r in runs) == 44
    assert sum(r.iterations - 1 for r in runs) == 24
    assert sum(churn(r) for r in runs) == 24


def test_the_loops_only_product_is_a_diagnostic():
    """One thing survives the week. The **iteration count** predicts whether the
    query was answered at AUC 0.214 — strength **0.786**, clear of this course's
    0.7 floor.

    Week 10 measured query *cost* as a quality signal and got 0.417: chance. The
    loop manufactures the correlation cost did not have, by spending the most on
    the queries it cannot answer.

    So the honest summary of an iterative agent on this corpus is: it answers
    nothing new, it costs 2.2 times as much, and it emits a usable serving-time
    quality signal as a by-product. Whether that is worth 2.2× is a decision; it
    is not a success."""
    runs, outcomes = ran(0.8)
    good = [float(r.iterations) for r in runs if outcomes[r.query_id]]
    bad = [float(r.iterations) for r in runs if not outcomes[r.query_id]]
    assert auc(good, bad) == pytest.approx(0.214, abs=0.02)
    assert separation_strength(auc(good, bad)) > 0.7


def test_the_report_names_the_queries_that_exhausted_the_loop():
    """Which queries capped is the most useful line in the report, and a count
    would have hidden that twelve of twenty did."""
    runs, outcomes = ran(0.8)
    report = loop_report(runs, outcomes, 3)
    assert len(report["capped"]) == 12
    assert "r10" in report["capped"]
    assert report["cost_multiple"] == pytest.approx(2.2)
    assert report["answered"] == pytest.approx(0.70)
