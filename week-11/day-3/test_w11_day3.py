"""Day 3 — the second hop, and what it turns out to be.

`test_the_hop_buys_exactly_what_week_twos_one_liner_bought` is the day.
"""

from functools import cache

import pytest

import raglab
from cost import context_tokens
from dense import DenseRetriever
from faithful import cites_superseded
from fuse import rrf
from hop import add_hop, follow, hop_report, replace_hop, stale_in, successors
from lineage import is_current, supersession
from order import order_by_rank
from postings import Index
from raglab.generator import SimulatedGenerator
from sections import section_corpus
from window import pack

CORPUS = raglab.corpus.load()
DOCS = {d.id: d.title + "\n" + d.text for d in CORPUS}


@cache
def graph():
    """Lazy: `supersession` is a lab, and a module-level call to a stub turns
    every test in this file into a collection error."""
    return supersession(DOCS)


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


def hopped(query, replace: bool):
    """One strategy, one query. Returns `(context, retrievals)`."""
    chunks, _, shortlist = built()
    first = shortlist(query.text)
    ctx = context(first)
    stale = stale_in(ctx, graph())
    if not stale:
        return ctx, 1
    extra = follow(shortlist(query.text, 60), successors(stale, graph()), len(stale))
    merged = replace_hop(first, stale, extra) if replace else add_hop(first, extra)
    return context(merged), 2


@cache
def strategies():
    chunks, _, shortlist = built()
    generator = SimulatedGenerator()
    out = {}

    def score(contexts, retrievals):
        return {
            "superseded": {
                q.id: cites_superseded(generator.answer(q.text, contexts[q.id]), chunks, graph())
                for q in dev()
            },
            "answered": {q.id: answered(q, contexts[q.id]) for q in dev()},
            "retrievals": retrievals,
            "tokens": sum(context_tokens(contexts[q.id]) for q in dev()) / len(dev()),
        }

    plain = {q.id: context(shortlist(q.text)) for q in dev()}
    out["baseline"] = score(plain, len(dev()))

    for name, replace in (("add", False), ("replace", True)):
        contexts, total = {}, 0
        for q in dev():
            ctx, n = hopped(q, replace)
            contexts[q.id] = ctx
            total += n
        out[name] = score(contexts, total)

    filtered = {
        q.id: context([c for c in shortlist(q.text, 60) if is_current(c.split("#")[0], graph())][:10])
        for q in dev()
    }
    out["prefilter"] = score(filtered, len(dev()))
    return out


# -- the mechanism ------------------------------------------------------------


def test_the_supersession_graph_is_week_twos_and_has_two_edges():
    assert graph() == {"rfc-7159": "rfc-8259", "rfc-5785": "rfc-8615"}


def test_the_chain_is_followed_to_its_end_not_one_step():
    """A document can be obsoleted by a document that is itself obsoleted. A
    one-step hop lands on another withdrawn specification, which is worse than
    not hopping because it looks like diligence."""
    chain = {"a": "b", "b": "c"}
    assert successors(["a#1"], chain) == ["c"]
    assert successors(["c#1"], chain) == ["c"]


def test_the_hop_fires_on_a_quarter_of_the_queries():
    """Five of twenty. The trigger is the *context*, not the shortlist — a
    deep shortlist contains a superseded chunk for fifteen of twenty queries, and
    hopping on all of them triples the retrievals to fix nothing."""
    chunks, _, shortlist = built()
    fires = [q.id for q in dev() if stale_in(context(shortlist(q.text)), graph())]
    assert sorted(fires) == ["r02", "r05", "r07", "r21", "r23"]


# -- the version everybody writes ---------------------------------------------


def test_adding_the_correction_does_not_stop_the_citation():
    """`add_hop` puts RFC 8259's chunk in the context next to RFC 7159's, which
    is the humane design: present both, let the reader judge.

    **`citing_superseded` does not move.** Three queries before, three after.

    The generator picks sentences by word overlap and the withdrawn document's
    chunk still wins. Whatever you believe a real model would do differently,
    the mechanism here is that **supplying the correction is not the same as
    removing the error**, and nothing in the pipeline prefers one over the
    other."""
    table = strategies()
    assert hop_report(**{k: table["baseline"][k] for k in ("superseded", "answered", "retrievals")})[
        "citing_superseded"
    ] == ["r05", "r07", "r23"]
    added = hop_report(
        table["add"]["superseded"], table["add"]["answered"], table["add"]["retrievals"]
    )
    assert added["citing_superseded"] == ["r05", "r07", "r23"]


def test_dropping_the_chunk_you_noticed_promotes_the_next_one():
    """The trap, and it is worth meeting.

    Remove only the stale chunks present in the context and the next chunk of
    the **same withdrawn document** moves up into the freed budget. `r23` goes
    on citing RFC 7159 and the other four queries are fixed, so the bug reads as
    a near miss rather than a category error.

    The unit of supersession is the document. The unit you noticed it on was a
    chunk."""
    chunks, _, shortlist = built()
    generator = SimulatedGenerator()
    query = next(q for q in dev() if q.id == "r23")
    first = shortlist(query.text)
    ctx = context(first)
    stale = stale_in(ctx, graph())
    extra = follow(shortlist(query.text, 60), successors(stale, graph()), len(stale))

    by_chunk = [c for c in first if c not in stale]
    naive = context(extra + [c for c in by_chunk if c not in extra])
    assert cites_superseded(generator.answer(query.text, naive), chunks, graph())

    whole = context(replace_hop(first, stale, extra))
    assert not cites_superseded(generator.answer(query.text, whole), chunks, graph())


def test_replacing_it_does():
    """Two list comprehensions' difference. **Three to zero.**"""
    table = strategies()
    replaced = hop_report(
        table["replace"]["superseded"], table["replace"]["answered"], table["replace"]["retrievals"]
    )
    assert replaced["citing_superseded"] == []
    assert replaced["retrievals"] == 25


# -- the day ------------------------------------------------------------------


def test_the_hop_buys_exactly_what_week_twos_one_liner_bought():
    """**The day.**

    | strategy | citing superseded | answered | retrievals |
    |---|---|---|---|
    | baseline | 3 | 0.700 | 20 |
    | second hop, replacing | **0** | 0.650 | **25** |
    | week 2's `is_current` filter | **0** | 0.650 | 20 |

    Identical outcomes. The multi-hop retrieval — trigger detection, successor
    resolution, a second retrieval, a merge — produces exactly the numbers a
    one-line metadata filter produces, at **1.25 times the retrievals**.

    And the filter was available in week 2, before embeddings, before fusion,
    before any of this.

    The agentic win is a metadata join. That is not a criticism of multi-hop
    retrieval; it is what multi-hop retrieval *is* when the relationship being
    hopped along is already in your metadata. The question to ask before
    building one is **which edge am I following, and is it already a field**."""
    table = strategies()
    hop = table["replace"]
    cheap = table["prefilter"]
    assert sorted(i for i, c in hop["superseded"].items() if c) == []
    assert sorted(i for i, c in cheap["superseded"].items() if c) == []
    assert sum(hop["answered"].values()) == sum(cheap["answered"].values()) == 13
    assert hop["retrievals"] == 25
    assert cheap["retrievals"] == 20


def test_the_fix_breaks_the_query_where_supersession_was_not_an_error():
    """Both strategies take `answered` from 0.700 to 0.650, and the lost query is
    **`r07`** — *"where do well-known URIs live"*, graded relevant against RFC
    5785 **and** RFC 8615.

    RFC 8615 obsoletes RFC 5785 and the answer did not change. So the superseded
    document is still correct, still relevant, and still carries an answer span
    — and a blanket *drop the superseded* rule removes it.

    Week 2 built this into the corpus deliberately: one supersession pair where
    the fact changed, one where it did not, graded differently. A rule that
    cannot tell them apart is right about `r05` and wrong about `r07`, and no
    amount of hopping fixes that, because the distinction is semantic and the
    edge is not."""
    table = strategies()
    lost = [
        i
        for i in table["baseline"]["answered"]
        if table["baseline"]["answered"][i] and not table["replace"]["answered"][i]
    ]
    assert lost == ["r07"]
    query = next(q for q in dev() if q.id == "r07")
    assert sorted(query.relevant) == ["rfc-5785", "rfc-8615"]
    assert query.family == "superseded"


def test_the_report_carries_all_three_numbers():
    """A report with the citation metric and not the answered rate would be an
    advertisement."""
    report = hop_report({"a": ["x#1"], "b": []}, {"a": True, "b": False}, 3)
    assert report == {"citing_superseded": ["a"], "answered": 0.5, "retrievals": 3}
