"""Day 3 — who may read what the retriever found.

`test_the_retriever_never_leaked_and_the_cache_leaks_eleven_times` is the day.
"""

from functools import cache

import raglab
from access import can_read, leaks, reader, revoke, scoped_key
from bm25 import search
from caching import cache_key
from dense import DenseRetriever
from filters import post_filter, pre_filter, shortfall
from fuse import rrf
from postings import Index
from sections import section_corpus
from windows import parent

CORPUS = raglab.corpus.load()
DOCS = {d.id: d.title + "\n" + d.text for d in CORPUS}

# Stipulated, like every permission in this course: three RFCs are for staff.
RESTRICTED = {"rfc-2324", "rfc-6585", "rfc-7725"}
ACL = {d.id: ({"staff"} if d.id in RESTRICTED else set()) for d in CORPUS}
K = 5


@cache
def chunks():
    return section_corpus(DOCS, 100, 300)


@cache
def dev():
    return list(raglab.judgments.load(file="queries-extended.yml").split("dev"))


def retriever_over(some_chunks):
    index = Index(some_chunks, stopwords=None)
    dense = DenseRetriever(dims=192).fit(some_chunks)

    def shortlist(text, depth):
        return rrf([search(index, text, 60), dense.search(text, 60)], depth, 10)

    return shortlist


@cache
def everything():
    return retriever_over(chunks())


@cache
def visible_only():
    return retriever_over(pre_filter(chunks(), reader(ACL, set())))


# -- the rule ------------------------------------------------------------------


def test_can_read():
    assert can_read(set(), set()) is True            # public document
    assert can_read({"staff"}, {"staff"}) is True
    assert can_read({"staff", "legal"}, {"legal"}) is True
    assert can_read(set(), {"staff"}) is False
    assert can_read({"sales"}, {"staff"}) is False


def test_a_document_with_no_recorded_rule_is_invisible():
    """It reached the index before its permissions did. Fail closed."""
    assert can_read({"staff"}, None) is False
    public = reader({"rfc-3986": set()}, {"staff"})
    assert public("rfc-3986#0") is True
    assert public("rfc-9999#0") is False


def test_a_reader_is_a_predicate_over_chunks():
    public, staff = reader(ACL, set()), reader(ACL, {"staff"})
    assert public("rfc-6585#3") is False and staff("rfc-6585#3") is True
    assert public("rfc-3986#3") is True
    assert len(pre_filter(chunks(), public)) == 232
    assert len(pre_filter(chunks(), staff)) == 266


# -- neither filter leaks ------------------------------------------------------


def test_filtering_after_retrieval_returns_nothing_five_times():
    """**Eleven of twenty questions come back short. Five come back empty.**

    Take the top five, drop what this reader may not see, return the rest. For
    five questions every one of the five was restricted, so the public reader is
    told there is nothing - about questions the public documents can answer."""
    public = reader(ACL, set())
    results = {q.id: post_filter(everything()(q.text, K), public, K) for q in dev()}
    assert sum(1 for r in results.values() if shortfall(r, K)) == 11
    assert sum(1 for r in results.values() if not r) == 5
    assert not any(leaks(r, public) for r in results.values())


def test_fetching_more_first_fixes_the_shortfall_here():
    """Fetch twenty, filter, keep five: no shortfall on this corpus. How far to
    over-fetch depends on how much of the corpus the reader cannot see, which
    is a different number for every reader."""
    public = reader(ACL, set())
    results = {q.id: post_filter(everything()(q.text, 20), public, K) for q in dev()}
    assert sum(1 for r in results.values() if shortfall(r, K)) == 0
    assert not any(leaks(r, public) for r in results.values())


def test_filtering_first_is_short_only_when_the_corpus_is():
    """Search only what the reader may see. Two questions still come back
    short, and this time it is true: there are not five visible chunks that
    match."""
    public = reader(ACL, set())
    results = {q.id: visible_only()(q.text, K) for q in dev()}
    assert sum(1 for r in results.values() if shortfall(r, K)) == 2
    assert not any(leaks(r, public) for r in results.values())


# -- and the leak is in front of the retriever ---------------------------------


def test_the_retriever_never_leaked_and_the_cache_leaks_eleven_times():
    """**A cache keyed on the question serves staff results to everyone.**

    A member of staff asks all twenty questions and week 10's cache stores what
    came back. Then a public reader asks the same twenty. Eleven of the cached
    results contain a chunk they may not read.

    Every retrieval was filtered correctly. The cache sits in front of the
    filter and has never heard of a reader."""
    public = reader(ACL, set())
    store = {cache_key(q.text): everything()(q.text, K) for q in dev()}   # staff
    served = [store[cache_key(q.text)] for q in dev()]                    # public
    assert sum(1 for r in served if leaks(r, public)) == 11


def test_a_key_that_knows_the_reader_cannot_be_shared():
    assert scoped_key("Hello, World?", {"b", "a"}) == "hello world|a,b"
    assert scoped_key("Hello, World?", set()) == "hello world|"
    assert scoped_key("x", {"staff"}) != scoped_key("x", set())
    assert scoped_key("x", {"a", "b"}) == scoped_key("x", ["b", "a", "a"])


def test_with_scoped_keys_the_public_reader_misses_and_nothing_leaks():
    public = reader(ACL, set())
    store = {scoped_key(q.text, {"staff"}): everything()(q.text, K) for q in dev()}
    assert not any(scoped_key(q.text, set()) in store for q in dev())
    for q in dev():
        store[scoped_key(q.text, set())] = visible_only()(q.text, K)
    served = [store[scoped_key(q.text, set())] for q in dev()]
    assert not any(leaks(r, public) for r in served)
    assert len(store) == 40  # the price: one entry per question per kind of reader


# -- taking a permission away --------------------------------------------------


def test_revoking_drops_what_was_built_on_the_document():
    entries = {
        "a|staff": ["rfc-6585#1", "rfc-3986#2"],
        "b|staff": ["rfc-3986#4"],
        "c|staff": ["rfc-6585#9"],
    }
    assert revoke(entries, "rfc-6585") == {"b|staff": ["rfc-3986#4"]}
    assert len(entries) == 3  # not changed in place


def test_leaks_keeps_the_order_it_was_given():
    public = reader(ACL, set())
    assert leaks(["rfc-7725#1", "rfc-3986#0", "rfc-2324#2"], public) == [
        "rfc-7725#1", "rfc-2324#2"
    ]
