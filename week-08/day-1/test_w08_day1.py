"""Day 1 — the first answers, and the first thing measurable about them.

`test_thirty_percent_are_confidently_wrong` is the day.
"""

from functools import cache

import pytest

import raglab
from dense import DenseRetriever
from fuse import rrf
from ground import (
    answer_all,
    answer_in_context,
    confidently_wrong,
    grounded_rate,
    report,
    response_rate,
)
from order import order_by_rank
from raglab.generator import SimulatedGenerator, is_refusal
from sections import section_corpus
from window import pack

CORPUS = raglab.corpus.load()
DOCS = {d.id: d.title + "\n" + d.text for d in CORPUS}


@cache
def dev():
    return list(raglab.judgments.load(file="queries-extended.yml").split("dev"))


@cache
def pipeline():
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

    return chunks, build_context


@cache
def run():
    _, build_context = pipeline()
    contexts = {q.id: build_context(q) for q in dev()}
    answers = answer_all(SimulatedGenerator(), dev(), build_context)
    return answers, contexts


# -- the machinery ------------------------------------------------------------


def test_every_query_gets_an_answer_object():
    answers, _ = run()
    assert set(answers) == {q.id for q in dev()}
    assert all(hasattr(a, "text") and hasattr(a, "citations") for a in answers.values())


def test_answer_in_context_reads_the_spans_not_the_prose():
    """It says nothing about what was generated — only whether the generator had
    what it needed."""
    q = raglab.judgments.load(file="queries-extended.yml").by_id("r03")
    assert answer_in_context(q, {"c": q.answer_spans[0]})
    assert not answer_in_context(q, {"c": "something else entirely"})


def test_an_unanswerable_query_can_never_have_its_answer_in_context():
    """Correct, and worth pausing on: for those queries the interesting question
    is not whether the answer was there but what the system did about its
    absence. That is Thursday."""
    q = raglab.judgments.load(file="queries-extended.yml").by_id("r10")
    assert q.unanswerable and not q.answer_spans
    assert not answer_in_context(q, {"c": "anything at all"})


def test_grounded_rate_divides_by_every_query():
    """Dividing by the answered ones is how a system that refuses hard queries
    reports a higher score for answering fewer of them."""
    answers, contexts = run()
    assert grounded_rate(answers, dev(), contexts) == pytest.approx(14 / 20, abs=0.001)


# -- the numbers --------------------------------------------------------------


def test_it_answers_everything():
    """**1.0.** Twenty queries, twenty answers, no refusals — including the
    out-of-scope one and the two nothing retrieves.

    That is not helpfulness. It is a failure to distinguish the cases, and it is
    the default behaviour of every generation system before somebody designs
    against it."""
    answers, _ = run()
    assert response_rate(answers) == 1.0
    assert not any(is_refusal(a.text) for a in answers.values())


def test_the_answers_read_as_well_supported():
    """Every one of them quotes the retrieved text and carries a citation. There
    is no tell. A wrong answer and a right one are the same object with
    different contents — week 1's claim, now demonstrable."""
    answers, _ = run()
    for query_id in ("r03", "r19"):
        text = answers[query_id].text
        assert "[" in text and "]" in text
        assert len(text.split()) > 10


def test_thirty_percent_are_confidently_wrong():
    """**The day.**

    Fourteen of twenty queries had the answer somewhere in the context. All
    twenty got a fluent, cited answer.

    So **six answers — thirty percent — are confident prose about a question the
    system could not answer.** Nothing in the text distinguishes them. A reader
    cannot tell. You can only tell because you wrote answer spans in week 4."""
    answers, contexts = run()
    wrong = confidently_wrong(answers, dev(), contexts)
    assert wrong == ["r09", "r10", "r19", "r20", "r21", "r23"]
    assert len(wrong) / len(dev()) == pytest.approx(0.30)


def test_it_contains_week_six_unreachable_and_more():
    """`r19` and `r20` have been unreachable since week 6 — three weeks of
    knowing retrieval could not find them, and this is the first week you can
    see what the system says instead.

    And there are four more. Those were retrieval failures too; nobody had
    looked at them because no metric put prose in front of you."""
    answers, contexts = run()
    wrong = set(confidently_wrong(answers, dev(), contexts))
    assert {"r19", "r20"} < wrong
    assert len(wrong - {"r19", "r20"}) == 4


def test_the_report_gives_the_rate_and_the_list():
    """A rate tells you how bad it is. The list tells you which queries to go and
    read, and reading them is the only way this becomes real."""
    answers, contexts = run()
    r = report(answers, dev(), contexts)
    assert r["n"] == 20
    assert r["response_rate"] == 1.0
    assert r["grounded_rate"] == pytest.approx(0.70)
    assert r["confidently_wrong_rate"] == pytest.approx(0.30)
    assert isinstance(r["confidently_wrong"], list)
