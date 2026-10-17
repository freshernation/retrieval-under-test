"""Day 4 — sharding, and the statistics it splits.

`test_four_shards_scoring_alone_change_twenty_five_top_tens` is the day.
"""

from functools import cache

import raglab
from bm25 import search
from postings import Index
from sections import section_corpus
from shards import build_shards, global_stats, scatter_gather, shard_of, split

CORPUS = raglab.corpus.load()
DOCS = {d.id: d.title + "\n" + d.text for d in CORPUS}


@cache
def chunks():
    return section_corpus(DOCS, 100, 300)


@cache
def queries():
    j = raglab.judgments.load(file="queries-extended.yml")
    return list(j.split("dev")) + list(j.split("test"))


@cache
def whole():
    return Index(chunks(), stopwords=None)


@cache
def four():
    return build_shards(chunks(), 4, stopwords=None)


def test_shard_of_is_stable():
    assert shard_of("rfc-6265#3", 4) == shard_of("rfc-6265#3", 4)
    assert {shard_of(c, 4) for c in chunks()} == {0, 1, 2, 3}


def test_split_keeps_every_chunk_once():
    parts = split(chunks(), 4)
    assert [len(p) for p in parts] == [69, 50, 80, 67]
    assert sorted(c for p in parts for c in p) == sorted(chunks())


def test_global_stats_are_the_whole_indexs():
    terms = whole().analyze_query("json cookie status")
    stats = global_stats(four(), terms)
    assert stats["n_documents"] == whole().n_documents
    assert abs(stats["average_length"] - whole().average_length) < 1e-9
    assert stats["df"] == {t: whole().document_frequency(t) for t in terms}


def test_four_shards_scoring_alone_change_twenty_five_top_tens():
    """Each shard scores with its own statistics: 25 of 26 top tens and 5 top results
    are not the whole index's."""
    tens = sum(scatter_gather(four(), q.text, 10, shared=False) != search(whole(), q.text, 10) for q in queries())
    ones = sum(scatter_gather(four(), q.text, 1, shared=False) != search(whole(), q.text, 1) for q in queries())
    assert (tens, ones) == (25, 5)


def test_shared_statistics_give_back_the_whole_index():
    for n in (2, 4, 8):
        parts = build_shards(chunks(), n, stopwords=None)
        for q in queries():
            assert scatter_gather(parts, q.text, 10, shared=True) == search(whole(), q.text, 10)
