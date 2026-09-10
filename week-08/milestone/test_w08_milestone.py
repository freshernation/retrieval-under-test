"""Week 8 milestone — Project 2, and the report card."""

from functools import cache

import pytest

import raglab
from answerer import Answerer, compare, report_card
from context import ContextAssembler
from dense import DenseRetriever
from fuse import rrf
from lineage import supersession
from raglab.generator import SimulatedGenerator, is_refusal
from sections import section_corpus

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

    from postings import Index

    chunks = section_corpus(DOCS, 100, 300)
    index = Index(chunks, stopwords=None)
    retriever = DenseRetriever(dims=192).fit(chunks)

    def retrieve(text, depth):
        return rrf([search(index, text, 60), retriever.search(text, 60)], depth, 10)

    assembler = ContextAssembler(retrieve, chunks, budget=800, depth=20)
    return chunks, assembler, supersession({d.id: d.text for d in CORPUS})


@cache
def card(**kwargs):
    chunks, assembler, graph = parts()
    refuse_below = kwargs.pop("refuse_below", 0.0)
    answerer = Answerer(assembler, SimulatedGenerator(**kwargs), refuse_below=refuse_below)
    return report_card(answerer, dev(), chunks, graph)


# -- the pipeline -------------------------------------------------------------


def test_the_answer_comes_with_the_context_it_was_generated_from():
    """A pipeline that discards it forces every evaluation to re-run retrieval —
    slow, and worse, it allows the evaluated context to differ from the
    generated one."""
    chunks, assembler, _ = parts()
    answerer = Answerer(assembler, SimulatedGenerator())
    answer, context = answerer.answer(dev()[0])
    assert isinstance(context, dict) and context
    assert all(c in chunks for c in context)


def test_the_config_names_the_generator():
    """A report that does not say which generator produced its numbers is not
    reproducible, and the flags are the difference between faithfulness 1.00 and
    0.09."""
    from raglab.runs import config_hash

    _, assembler, _ = parts()
    plain = Answerer(assembler, SimulatedGenerator()).config
    broken = Answerer(assembler, SimulatedGenerator(misattribute=True)).config
    assert config_hash(plain) != config_hash(broken)
    assert "refuse_below" in plain and "budget" in plain


def test_the_refusal_policy_short_circuits_the_generator():
    _, assembler, _ = parts()
    always = Answerer(assembler, SimulatedGenerator(), refuse_below=1.01)
    answer, _ = always.answer(dev()[0])
    assert is_refusal(answer.text)


# -- the report card ----------------------------------------------------------


def test_it_reports_everything_and_grades_nothing():
    """There is no field for "how good are the answers", because nothing in this
    course can compute one. Week 9 is about what happens when you ask a model
    to."""
    c = card()
    assert set(c) == {
        "n",
        "response_rate",
        "grounded_rate",
        "outcomes",
        "faithfulness",
        "citations",
        "confidently_wrong",
        "citing_superseded",
        "uncited_sentences",
    }
    assert "quality" not in c and "score" not in c


def test_the_baseline_card():
    c = card()
    assert c["n"] == 20
    assert c["response_rate"] == 1.0
    assert c["grounded_rate"] == pytest.approx(0.70)
    assert c["faithfulness"] == 1.0
    assert c["outcomes"] == {
        "answered_right": 14,
        "answered_wrong": 6,
        "refused_right": 0,
        "refused_wrong": 0,
    }
    assert c["confidently_wrong"] == ["r09", "r10", "r19", "r20", "r21", "r23"]
    assert c["citing_superseded"] == ["r05", "r07", "r23"]


def test_refusal_removes_wrong_answers_and_costs_nothing_here():
    c = card(refuse_below=0.55)
    assert c["outcomes"]["answered_right"] == 14
    assert c["outcomes"]["refused_wrong"] == 0
    assert c["outcomes"]["refused_right"] == 2
    assert c["response_rate"] == pytest.approx(0.9)
    assert len(c["confidently_wrong"]) == 4


def test_a_refusal_is_not_counted_as_an_uncited_claim():
    """It cites nothing and claims nothing. Counting its sentence as uncited, or
    its zero citations as perfect, mislead in opposite directions."""
    assert card(refuse_below=0.55)["uncited_sentences"] == 0


# -- and the milestone's argument ---------------------------------------------


def test_one_metric_hides_a_catastrophe():
    """**The milestone.**

    `grounded_rate` is **0.70 for all three configurations** — the plain one, the
    refusing one, and the one whose every citation is attached to a claim it does
    not support.

    That last system has faithfulness **0.09**. Retrieval is unchanged, so the
    metric that only looks at retrieval is unchanged, and a report leading with
    `grounded_rate` would call the three equivalent."""
    plain = card()
    broken = card(misattribute=True)
    assert plain["grounded_rate"] == broken["grounded_rate"] == pytest.approx(0.70)
    assert plain["faithfulness"] == 1.0
    assert broken["faithfulness"] < 0.15


def test_and_faithfulness_hides_the_other_one():
    """The mirror image, and the pairing is the week's whole finding.

    The plain configuration scores a **perfect 1.00 faithfulness** while six of
    its twenty answers are confident prose about questions it could not answer.

    Either number alone is misleading. Both must be reported, together, always."""
    c = card()
    assert c["faithfulness"] == 1.0
    assert len(c["confidently_wrong"]) == 6


def test_compare_orders_but_the_card_decides():
    """A single-metric ordering hides a configuration that moved the system in
    two directions at once — week 6's rule, at the last station."""
    cards = {"plain": card(), "broken": card(misattribute=True)}
    order = compare(cards, "grounded_rate")
    assert set(order) == {"plain", "broken"}
    assert cards[order[0]]["grounded_rate"] == cards[order[1]]["grounded_rate"]
