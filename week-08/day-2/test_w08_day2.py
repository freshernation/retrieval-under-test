"""Day 2 — citations.

`test_a_perfect_citation_report_says_nothing_about_correctness` is the day.
"""

from functools import cache

import pytest

import raglab
from cite import (
    chunk_citations,
    cited_sentences,
    citation_report,
    not_in_context,
    parse_citations,
    strip_citations,
    uncited_sentences,
    unresolvable,
)
from dense import DenseRetriever
from fuse import rrf
from ground import answer_all, confidently_wrong
from order import order_by_rank
from raglab.generator import SimulatedGenerator
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


# -- parsing ------------------------------------------------------------------


def test_citations_come_out_in_order():
    """Order is evidence: a citation attaches to the sentence it follows."""
    assert parse_citations("A [x] B [y] C [x]") == ["x", "y"]


def test_prose_comes_out_clean():
    assert strip_citations("The code is 429. [rfc-6585#4]") == "The code is 429."


def test_the_unit_is_the_sentence():
    """An answer-level citation list says the answer drew on four chunks. It does
    not say which chunk supports which claim."""
    pairs = cited_sentences("First claim. [a] Second claim. [b]")
    assert pairs == [("First claim.", ["a"]), ("Second claim.", ["b"])]


def test_uncited_sentences_are_found():
    """Not automatically wrong, and exactly where an unsupported claim hides —
    there is no citation to check it against."""
    assert uncited_sentences("Cited. [a] Uncited.") == ["Uncited."]
    assert uncited_sentences("All cited. [a]") == []


# -- the two failures ---------------------------------------------------------


def test_an_unresolvable_citation_is_an_id_that_never_existed():
    chunks, _, _ = run()
    real = next(iter(chunks))
    assert unresolvable([real, "rfc-9999#1"], chunks) == ["rfc-9999#1"]
    assert unresolvable([real], chunks) == []


def test_not_in_context_is_the_subtle_one():
    """The id resolves, the chunk is real, a reader following the link sees
    plausible text — and the generator never saw it. A system citing something
    it was not given is not grounded, however plausible the pairing looks."""
    chunks, _, contexts = run()
    context = contexts["r03"]
    outside = next(c for c in chunks if c not in context)
    assert unresolvable([outside], chunks) == []
    assert not_in_context([outside], context) == [outside]


def test_a_fabricating_generator_is_caught_immediately():
    """Twenty invented ids on top of the five corpus artifacts, every one
    detectable mechanically, with no model and no judgment. The count of
    citations that actually resolve does not move."""
    chunks, answers, contexts = run(fabricate=True)
    r = citation_report(answers, contexts, chunks)
    clean = citation_report(run()[1], contexts, chunks)
    assert r["citations"] == 64 and clean["citations"] == 44
    assert r["unresolvable"] == 25 and clean["unresolvable"] == 5
    assert sum(len(chunk_citations(a.text, chunks)) for a in answers.values()) == 39


def test_refusals_do_not_count_as_perfect_attribution():
    """Otherwise a system that declines everything reports flawless citations."""
    chunks, _, contexts = run()
    from raglab.generator import REFUSAL, Answer

    only_refusals = {q.id: Answer(REFUSAL, ()) for q in dev()}
    r = citation_report(only_refusals, contexts, chunks)
    assert r["citations"] == 0
    assert r["sentences"] == 0


# -- and the day --------------------------------------------------------------


def test_your_checker_reports_fabrications_that_never_happened():
    """**The day's best surprise, and it is a bug in your checker.**

    The naive parser finds 44 citations and reports **5 unresolvable**. The
    generator emitted 39 and invented none.

    The five are `[RFC3629]`, `[RFC3986]`, `[RFC6585]`, `[RFC2818]` — bracketed
    cross-references **quoted from the corpus**, in sentences the generator
    copied verbatim. RFCs are full of them.

    So your fabrication metric has an 11% false-positive rate, sourced from the
    documents, and you would have blamed the model."""
    chunks, answers, contexts = run()
    r = citation_report(answers, contexts, chunks)
    assert r["citations"] == 44
    assert r["unresolvable"] == 5
    assert r["not_in_context"] == 5

    bogus = {c for a in answers.values() for c in unresolvable(parse_citations(a.text), chunks)}
    assert bogus == {"RFC3629", "RFC3986", "RFC6585", "RFC2818"}


def test_resolving_against_the_chunk_ids_papers_over_it():
    """39 citations, all real, all present. The number is now right and the
    ambiguity is not gone — the real fix is upstream: make the citation marker
    something the corpus cannot contain."""
    chunks, answers, contexts = run()
    resolved = sum(len(chunk_citations(a.text, chunks)) for a in answers.values())
    assert resolved == 39
    for answer in answers.values():
        cites = chunk_citations(answer.text, chunks)
        assert unresolvable(cites, chunks) == []


def test_a_perfect_citation_report_says_nothing_about_correctness():
    """**The day.**

    Every citation the generator actually made resolves and was in the context.
    Six of the twenty answers are still confident prose about a question the
    system could not answer.

    The citations are *valid* — real chunks, genuinely in the context, honestly
    the source of the wording. And the wording is about the wrong thing.

    Verifiability and correctness are different properties. A citation proves
    where text came from; it proves nothing about whether that text answers the
    question. Every "cited answers are trustworthy" claim you will read this
    year confuses the two."""
    chunks, answers, contexts = run()
    wrong = confidently_wrong(answers, dev(), contexts)
    assert len(wrong) == 6
    for query_id in wrong:
        cites = chunk_citations(answers[query_id].text, chunks)
        assert cites
        assert not_in_context(cites, contexts[query_id]) == []
