"""Milestone 14 — guarded, cached, scaled.

`test_the_card_number_never_reaches_the_cache` is the milestone.
"""

from functools import cache

import raglab
from bm25 import search
from dense import DenseRetriever
from guarded import guarded_search, scale_report
from postings import Index
from sections import section_corpus
from semcache import SemanticCache, embedder
from shards import build_shards
from windows import parent

CORPUS = raglab.corpus.load()
DOCS = {d.id: d.title + "\n" + d.text for d in CORPUS}
RESTRICTED = {"rfc-2324", "rfc-6585", "rfc-7725"}
ACL = {d.id: ({"staff"} if d.id in RESTRICTED else set()) for d in CORPUS}


@cache
def chunks():
    return section_corpus(DOCS, 100, 300)


@cache
def shards():
    return build_shards(chunks(), 4, stopwords=None)


@cache
def embed():
    return embedder(DenseRetriever(dims=192).fit(chunks()))


def fresh_cache():
    return SemanticCache(embed(), 0.8)


def run(query, groups, store, k=5):
    return guarded_search(query, groups, cache=store, shards=shards(), acl=ACL, k=k)


def test_refused():
    assert run("   ", set(), fresh_cache()) == {"status": "refused", "results": [], "problems": ["empty"]}


def test_the_same_as_the_whole_index_filtered():
    whole = Index(chunks(), stopwords=None)
    expected = [c for c in search(whole, "how do cookies expire", 60) if parent(c) not in RESTRICTED][:5]
    assert run("how do cookies expire", set(), fresh_cache())["results"] == expected


def test_the_second_asking_is_cached():
    store = fresh_cache()
    first = run("must JSON be encoded in UTF-8", set(), store)
    second = run("does JSON have to be encoded as UTF-8", set(), store)
    assert first["status"] == "searched" and second["status"] == "cached"
    assert second["results"] == first["results"]


def test_a_near_miss_is_searched_not_served():
    store = fresh_cache()
    run("what does section 3.2 of RFC 3986 define", set(), store)
    assert run("what does section 3.4 of RFC 3986 define", set(), store)["status"] == "searched"


def test_staff_results_never_reach_the_public():
    store = fresh_cache()
    staff = run("what does the 418 status code mean", {"staff"}, store, k=10)
    assert any(parent(c) == "rfc-2324" for c in staff["results"])
    public = run("what does the 418 status code mean", set(), store, k=10)
    assert public["status"] == "searched" and not any(parent(c) in RESTRICTED for c in public["results"])


def test_the_card_number_never_reaches_the_cache():
    store = fresh_cache()
    result = run("why was card 4242424242424242 charged for robots.txt", set(), store)
    assert result["problems"] == ["contained a card number"]
    stored = [entry for entry in store.entries]
    assert stored, "The result should have been cached."
    assert not any("4242" in repr(entry) for entry in stored), (
        "A card number reached the cache. Guard first, then everything else."
    )
    again = run("why was card 5555555555554444 charged for robots.txt", set(), store)
    assert again["status"] == "cached", "Two questions that differ only in a redacted card are the same question."


def test_scale_report():
    assert scale_report({"card_false_positives": 18, "graph_share": 0.906}) == [
        "card_false_positives 18", "cache_wrong_answers not measured",
        "graph_share 0.906", "sharded_drift not measured"]
