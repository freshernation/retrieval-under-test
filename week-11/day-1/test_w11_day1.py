"""Day 1 — rewriting the query, aimed at a failure identified in advance.

`test_the_rewrite_helps_what_it_was_not_aimed_at_and_breaks_what_worked` is the day.
"""

from functools import cache

import pytest

import raglab
from dense import DenseRetriever
from fuse import rrf
from order import order_by_rank
from postings import Index
from rewrite import (
    drop_low_idf,
    expand,
    prf_terms,
    rewrite_report,
    term_idf,
    variants,
)
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

    return chunks, index, shortlist


def context(shortlist, budget=800):
    chunks, _, _ = built()
    selected, texts = pack(shortlist, chunks, budget)
    return {c: texts[c] for c in order_by_rank(selected)}


def answered(query, ctx):
    return bool(query.answer_spans) and query.is_answered_by(list(ctx.values()))


def three(text):
    chunks, index, shortlist = built()
    return variants(index, chunks, text, shortlist(text, 3))


@cache
def baseline():
    _, _, shortlist = built()
    return {q.id: answered(q, context(shortlist(q.text))) for q in dev()}


@cache
def after(pick: int):
    _, _, shortlist = built()
    return {q.id: answered(q, context(shortlist(three(q.text)[pick]))) for q in dev()}


# -- the pieces ---------------------------------------------------------------


def test_idf_is_what_decides_which_words_matter():
    _, index, _ = built()
    assert term_idf(index, "428") > 4.0
    assert term_idf(index, "the") < 0.2
    assert term_idf(index, "zzzznotaterm") == 0.0


def test_dropping_low_idf_terms_keeps_the_ones_already_doing_the_work():
    """Which is the reason to expect it to do very little: the words it removes
    were contributing almost nothing to the score."""
    _, index, _ = built()
    assert drop_low_idf(index, "which specification defines the scheme part of a URI") == (
        "which defines scheme part"
    )
    assert drop_low_idf(index, "") == ""


def test_expansion_appends_and_never_replaces():
    """A rewrite that discards the user's words can lose an exact identifier, and
    week 5 measured what exact identifiers are worth on this corpus."""
    assert expand("428", ["status", "code"]) == "428 status code"
    assert expand("428", []) == "428"


def test_the_original_query_is_the_first_variant():
    """Week 6's RRF rewards agreement across input rankings. A fan-out whose
    variants all drift together agrees loudly about the wrong documents, so the
    undrifted query has to be in the set."""
    assert three("how do I stop search engines indexing my site")[0] == (
        "how do I stop search engines indexing my site"
    )
    assert len(three("428")) == 3


# -- what the feedback actually contains --------------------------------------


def test_feedback_from_the_wrong_documents_is_confidently_wrong_feedback():
    """**Query drift, visible.**

    `r19` asks how to stop search engines indexing a site. The corpus answers it
    with `crawler`, `disallow` and `access`. The feedback terms are
    `web accessed their sites rec` — a stopword, a word fragment, and nothing
    that bridges the gap.

    `r06` asks what ABNF stands for and gets `generic et al berners lee`: the
    bibliography. `r04` asks about 418 and gets `codes head 6585 2012 body`,
    which drags in the *other* status-code RFC.

    Pseudo-relevance feedback assumes the first retrieval was about the right
    thing. When it was not, the second retrieval is wrong with more
    conviction."""
    chunks, index, shortlist = built()
    drift = prf_terms(index, chunks, shortlist("how do I stop search engines indexing my site", 3),
                      "how do I stop search engines indexing my site")
    assert drift == ["web", "accessed", "their", "sites", "rec"]
    assert "crawler" not in drift and "disallow" not in drift


def test_the_report_names_queries_rather_than_counting_them():
    """A net delta of -0.05 hides two queries fixed and three broken, and those
    are different facts about the rewrite."""
    report = rewrite_report({"a": True, "b": False}, {"a": False, "b": True})
    assert report == {"gained": ["b"], "lost": ["a"], "before": 0.5, "after": 0.5, "delta": 0.0}


# -- the three rewrites -------------------------------------------------------


def test_dropping_terms_loses_two_queries_and_gains_none():
    """0.70 → 0.60. The cheapest rewrite is also the one with no upside: it
    removes words that were already contributing nothing, and occasionally the
    one word that was."""
    report = rewrite_report(baseline(), after(1))
    assert report["delta"] == pytest.approx(-0.10)
    assert report["gained"] == []
    assert report["lost"] == ["r07", "r22"]


def test_fusion_cannot_rescue_a_bad_variant_set():
    """Fan-out over all three, fused with week 6's RRF, with the original query
    included. 0.70 → **0.65**, gaining nothing.

    Two of the three variants are worse than the original, and fusion averages
    towards them. Week 6 measured fusion losing to its best input at k=5; a
    variant set is an input set, and the same arithmetic applies."""
    _, _, shortlist = built()
    fused = {
        q.id: answered(q, context(rrf([shortlist(v, 20) for v in three(q.text)], 20, 10)))
        for q in dev()
    }
    report = rewrite_report(baseline(), fused)
    assert report["gained"] == []
    assert report["delta"] == pytest.approx(-0.05)


def test_the_rewrite_helps_what_it_was_not_aimed_at_and_breaks_what_worked():
    """**The day.**

    Expansion by pseudo-relevance feedback, 0.70 → **0.65**. And the net number
    is the least interesting part of it:

    | | |
    |---|---|
    | gained | `r21`, `r23` |
    | lost | `r04`, `r06`, `r07` |
    | `paraphrase` | 1/3 → **1/3** |

    The two queries this day was aimed at — the station-4 failures week 10 named,
    which week 6 had independently flagged as retrieved by nothing — are
    **untouched**. The technique pointed at them does not move them.

    What it does move is everything else, in both directions, and the direction
    depends on the family: plain 4/5 → 5/5 and vocabulary-gap 2/4 → 3/4, against
    identifier 4/4 → 3/4, acronym 1/1 → **0/1** and superseded 2/2 → 1/2.

    Which is week 5's finding wearing a different hat. Adding terms helps when
    the query is loose prose and hurts when it is a precise identifier, because
    dilution is exactly what an exact match cannot survive."""
    report = rewrite_report(baseline(), after(2))
    assert report["gained"] == ["r21", "r23"]
    assert report["lost"] == ["r04", "r06", "r07"]
    assert report["delta"] == pytest.approx(-0.05)

    paraphrase = [q.id for q in dev() if q.family == "paraphrase"]
    assert sum(baseline()[i] for i in paraphrase) == 1
    assert sum(after(2)[i] for i in paraphrase) == 1


def test_the_family_split_is_the_mechanism_and_the_net_number_is_not():
    """Two families up, three down, one unchanged, net -0.05. A report that
    quotes the net has discarded the only actionable thing it measured — that
    this rewrite is right for one half of the query mix and wrong for the
    other, which is tomorrow's problem."""
    helped = [q.id for q in dev() if q.family in ("plain", "vocabulary-gap")]
    hurt = [q.id for q in dev() if q.family in ("identifier", "acronym", "superseded")]
    assert sum(after(2)[i] for i in helped) > sum(baseline()[i] for i in helped)
    assert sum(after(2)[i] for i in hurt) < sum(baseline()[i] for i in hurt)
