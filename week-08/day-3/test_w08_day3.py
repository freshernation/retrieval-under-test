"""Day 3 — faithfulness, and the thing it is not.

`test_perfect_faithfulness_and_a_wrong_answer` is the keystone of the course.
"""

from functools import cache

import pytest

import raglab
from cite import chunk_citations
from dense import DenseRetriever
from faithful import (
    best_support,
    cites_superseded,
    content_words,
    faithfulness,
    faithfulness_rate,
    sentence_verdicts,
    support,
)
from fuse import rrf
from ground import answer_all, confidently_wrong
from lineage import supersession
from order import order_by_rank
from raglab.generator import REFUSAL, Answer, SimulatedGenerator
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
def run(**options):
    chunks, build_context = pipeline()
    contexts = {q.id: build_context(q) for q in dev()}
    answers = answer_all(SimulatedGenerator(**options), dev(), build_context)
    return chunks, answers, contexts


@cache
def graph():
    return supersession({d.id: d.text for d in CORPUS})


# -- the proxy ----------------------------------------------------------------


def test_support_is_word_overlap():
    assert support("the cat sat", "the cat sat on the mat") == 1.0
    assert support("the cat sat", "a dog barked") == 0.0
    assert support("", "anything") == 1.0


def test_it_rewards_copying_and_punishes_paraphrase():
    """Backwards as a measure of quality, and exactly why this is a proxy. A
    generator that quotes verbatim scores 1.0; one that paraphrases correctly
    scores lower."""
    source = "The 429 status code indicates that the user has sent too many requests."
    quoted = "The 429 status code indicates that the user has sent too many requests."
    paraphrased = "Return 429 when a client is being throttled."
    assert support(quoted, source) == 1.0
    assert support(paraphrased, source) < 0.6


def test_it_cannot_see_a_negation():
    """The failure that matters most and the one word overlap cannot catch. A
    real faithfulness check needs entailment, which needs a model — week 9."""
    source = "A crawler MUST assume complete disallow."
    claim = "A crawler MUST NOT assume complete disallow."
    assert support(claim, source) > 0.8


def test_best_support_takes_the_highest():
    assert best_support("cat", ["dog", "cat"]) == 1.0
    assert best_support("cat", []) == 0.0


# -- verdicts -----------------------------------------------------------------


def test_the_basis_records_what_it_was_checked_against():
    """The field that keeps this honest — checking an uncited claim against the
    whole window is the lenient choice, and it should be visible."""
    chunks, answers, contexts = run()
    verdicts = sentence_verdicts(answers["r03"], contexts["r03"], chunks)
    assert verdicts
    assert {v["basis"] for v in verdicts} <= {"cited", "context", "uncited"}
    assert all(set(v) == {"claim", "citations", "support", "supported", "basis"} for v in verdicts)


def test_a_refusal_claims_nothing_so_it_cannot_be_unfaithful():
    chunks, _, contexts = run()
    assert faithfulness(Answer(REFUSAL, ()), contexts["r03"], chunks) == 1.0


def test_the_aggregate_excludes_refusals():
    """Include them and a system that declines everything scores a perfect 1.0 —
    the easiest way to game any faithfulness metric, and not hypothetical."""
    chunks, _, contexts = run()
    only_refusals = {q.id: Answer(REFUSAL, ()) for q in dev()}
    assert faithfulness_rate(only_refusals, contexts, chunks) == 1.0


# -- what it catches ----------------------------------------------------------


def test_it_catches_overreach():
    """A confident sentence supported by nothing drops faithfulness from 1.00 to
    0.74, and the verdict names the sentence."""
    chunks, answers, contexts = run(overreach=True)
    assert faithfulness_rate(answers, contexts, chunks) == pytest.approx(0.738, abs=0.01)


def test_it_catches_misattribution():
    """The second citation failure, and the one yesterday could not see: every id
    resolves, every id was in the context, and each one is attached to a claim it
    does not support. Faithfulness collapses to **0.09**."""
    chunks, answers, contexts = run(misattribute=True)
    assert faithfulness_rate(answers, contexts, chunks) == pytest.approx(0.092, abs=0.02)
    for answer in answers.values():
        assert chunk_citations(answer.text, chunks)


def test_the_three_faults_are_caught_by_different_machinery():
    """`fabricate` by resolving ids, `misattribute` by checking support against
    the cited chunk, `overreach` by checking support against anything at all.
    A system with only one of the three checks misses two of the three faults."""
    chunks, _, contexts = run()
    plain = faithfulness_rate(run()[1], contexts, chunks)
    assert plain > faithfulness_rate(run(overreach=True)[1], contexts, chunks)
    assert plain > faithfulness_rate(run(misattribute=True)[1], contexts, chunks)


# -- and the keystone ---------------------------------------------------------


def test_perfect_faithfulness_and_a_wrong_answer():
    """**The keystone of the course.**

    The default generator scores **faithfulness 1.000**. Every sentence is
    supported by the chunk it cites. Every citation resolves and was in the
    context.

    Six of its twenty answers — thirty percent — are confident prose about
    questions the system could not answer.

    These are not in tension. **Faithfulness is a relation between the answer and
    the context.** Correctness is a relation between the answer and the world.
    A perfectly faithful answer to a context that does not contain the answer is
    perfectly faithful and wrong, and no amount of measuring the first tells you
    anything about the second.

    Every "we measure faithfulness, so our answers are trustworthy" claim you
    will read this year is this confusion."""
    chunks, answers, contexts = run()
    assert faithfulness_rate(answers, contexts, chunks) == 1.0
    assert len(confidently_wrong(answers, dev(), contexts)) == 6


def test_and_the_withdrawn_specification_scores_a_perfect_one():
    """`r05` — *must JSON be encoded in UTF-8*.

    The answer opens: *"JSON text SHALL be encoded in UTF-8, UTF-16, or UTF-32"*,
    cited to `rfc-7159#10`. Faithfulness **1.0**: the chunk says exactly that.

    RFC 7159 was withdrawn in December 2017. The rule is wrong. Week 2 found the
    trap, week 6 watched retrieval walk into it, and this is what it produces at
    the last station: a fluent, correctly cited, perfectly faithful, false
    answer.

    Nothing inside the faithfulness machinery can see it, because the fact that
    makes it wrong is not in the passage — it is in a **different document**,
    which was week 2's whole finding."""
    chunks, answers, contexts = run()
    assert faithfulness(answers["r05"], contexts["r05"], chunks) == 1.0
    assert "SHALL be encoded in UTF-8, UTF-16, or UTF-32" in answers["r05"].text
    assert "rfc-7159#10" in chunk_citations(answers["r05"].text, chunks)


def test_the_currency_check_lives_outside_the_faithfulness_machinery():
    """Three answers cite a superseded document. Catching that needs week 2's
    graph — metadata, not text — and it does not belong inside a faithfulness
    metric.

    That separation is the day's design lesson: a check that needs a different
    kind of evidence is a different check, and folding it in would make a
    faithfulness score that quietly means something else."""
    chunks, answers, contexts = run()
    flagged = {q: cites_superseded(answers[q], chunks, graph()) for q in answers}
    flagged = {q: v for q, v in flagged.items() if v}
    assert set(flagged) == {"r05", "r07", "r23"}
    assert faithfulness_rate(answers, contexts, chunks) == 1.0
