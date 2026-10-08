"""Day 2 — caching, and the metric that is not the hit rate.

`test_the_same_cache_scores_point_two_or_point_eight` is the day.
"""

from functools import cache

import pytest

import raglab
from caching import LRU, cache_key, distinct, replay, staleness, stream, work_saved
from dense import DenseRetriever
from fuse import rrf
from latency import work
from order import order_by_rank
from postings import Index
from sections import section_corpus
from window import pack

CORPUS = raglab.corpus.load()
DOCS = {d.id: d.title + "\n" + d.text for d in CORPUS}


@cache
def dev():
    return list(raglab.judgments.load(file="queries-extended.yml").split("dev"))


@cache
def everything():
    judged = raglab.judgments.load(file="queries-extended.yml")
    return list(judged.split("dev")) + list(judged.split("test"))


def build(docs):
    import sys
    from pathlib import Path

    root = Path(__file__).resolve().parents[2]
    for day in ("day-3", "day-2", "day-1"):
        sys.path.insert(0, str(root / "week-03" / day))
    from bm25 import search

    chunks = section_corpus(docs, 100, 300)
    index = Index(chunks, stopwords=None)
    retriever = DenseRetriever(dims=192).fit(chunks)

    def context(text, budget=800):
        shortlist = rrf([search(index, text, 60), retriever.search(text, 60)], 20, 10)
        selected, texts = pack(shortlist, chunks, budget)
        return {c: texts[c] for c in order_by_rank(selected)}

    return chunks, index, context


@cache
def built():
    return build(DOCS)


@cache
def costs():
    _, index, _ = built()
    return {q.id: float(work(index, q.text)) for q in dev()}


# -- the instrument you do not have -------------------------------------------


def test_the_eval_set_cannot_measure_a_cache():
    """**Twenty-six queries, twenty-six distinct keys, hit rate zero.**

    An eval set is built without duplicates on purpose — a duplicate would
    weight it — so the instrument nine weeks went into is structurally unable to
    produce the number this day is about. Normalising does not help: nothing
    collides."""
    texts = [q.text for q in everything()]
    assert len(texts) == 26
    assert distinct(texts) == 26

    cache_ = LRU()
    for text in texts:
        if cache_.get(cache_key(text)) is None:
            cache_.put(cache_key(text), True)
    assert cache_.hit_rate == 0.0


def test_normalisation_merges_what_you_told_it_to_and_no_more():
    assert cache_key("Must JSON be encoded in UTF-8?") == cache_key("must json be encoded in utf 8")
    assert cache_key("  428  ") == "428"
    assert cache_key("428 429") != cache_key("429 428"), "term order is not yours to discard"


# -- the mechanism ------------------------------------------------------------


def test_a_hit_refreshes_recency_or_it_is_a_fifo_with_a_better_name():
    """The difference between LRU and FIFO appears only under capacity pressure,
    which is to say only in production."""
    lru = LRU(capacity=2)
    lru.put("a", 1)
    lru.put("b", 2)
    assert lru.get("a") == 1
    lru.put("c", 3)
    assert lru.get("a") == 1, "a was used most recently, so b is the one that goes"
    assert lru.get("b") is None


def test_an_unbounded_cache_hit_rate_is_one_minus_distinct_over_requests():
    """Uniform traffic: 0.800. Zipf traffic: **0.800**. Identical, because both
    streams touch all twenty queries and an unbounded cache keeps everything it
    has ever seen. The shape of the distribution is irrelevant here, so a hit
    rate measured this way is not evidence about the traffic."""
    ids = [q.id for q in dev()]
    uniform = replay(stream(ids, 100, 0.0), costs())
    zipf = replay(stream(ids, 100, 1.0), costs())
    assert uniform["hit_rate"] == pytest.approx(0.80, abs=0.01)
    assert zipf["hit_rate"] == pytest.approx(0.80, abs=0.01)


def test_the_same_cache_scores_point_two_or_point_eight():
    """**The day.**

    One cache, capacity five, three assumptions about traffic:

    | skew | hit rate |
    |---|---|
    | 0 — uniform | 0.19 |
    | 1 — Zipf | 0.30 |
    | 2 — concentrated | **0.79** |

    Four times the hit rate from the same code, decided by a number typed into
    the simulator. Nobody measured which one their traffic is, and the hit rate
    is the figure that justifies the cache.

    So: a cache hit rate is a claim about traffic. Report the distribution you
    assumed, or report nothing."""
    ids = [q.id for q in dev()]
    rates = {s: replay(stream(ids, 100, s), costs(), capacity=5)["hit_rate"] for s in (0.0, 1.0, 2.0)}
    assert rates[0.0] == pytest.approx(0.19, abs=0.02)
    assert rates[1.0] == pytest.approx(0.30, abs=0.02)
    assert rates[2.0] == pytest.approx(0.79, abs=0.02)
    assert rates[2.0] / rates[0.0] > 4


# -- the metric that is not the hit rate --------------------------------------


def test_the_same_hit_rate_saves_three_times_the_work_or_a_third():
    """Half the queries cached, two ways. Hit the cheap half and **22.7%** of the
    work goes away; hit the dear half and **77.3%** does.

    Identical hit rate, 3.4-fold difference in the thing you were trying to
    avoid doing, from the same ten entries. And day 1 measured a 269-fold cost spread, so this gap is
    available on any real workload — in the unhelpful direction, because the
    popular queries tend to be the short ones."""
    ordered = sorted(costs(), key=lambda i: costs()[i])
    cheap, dear = ordered[:10], ordered[10:]
    assert len(cheap) == len(dear) == 10
    assert work_saved(cheap, costs()) == pytest.approx(0.227, abs=0.005)
    assert work_saved(dear, costs()) == pytest.approx(0.773, abs=0.005)
    assert work_saved(dear, costs()) / work_saved(cheap, costs()) > 3


# -- what the cache is actually holding ---------------------------------------


def test_a_cached_answer_outlives_the_document_that_corrected_it():
    """RFC 8259 obsoletes RFC 7159 and says the opposite about UTF-8. Serve
    `r05` from a corpus that predates 8259, cache it, then let 8259 arrive:

    - the cached context is grounded entirely in the **withdrawn** RFC
    - a fresh build puts `rfc-8259#12` at rank two
    - the cache reports a **hit**, and nothing in the system disagrees

    Week 2 found this trap, week 6 watched retrieval walk into it, week 8 watched
    the generator cite it with a perfect support score. A cache makes it
    permanent."""
    before = {k: v for k, v in DOCS.items() if k != "rfc-8259"}
    query = next(q for q in dev() if q.id == "r05")
    cached = build(before)[2](query.text)
    fresh = built()[2](query.text)

    assert not any(c.startswith("rfc-8259") for c in cached)
    assert any(c.startswith("rfc-8259") for c in fresh)
    assert any(c.startswith("rfc-7159") for c in cached)


def test_an_overlap_check_scores_point_eight_three_and_misses_the_point():
    """Five of the six cached chunks are still the right ones. A staleness check
    built on overlap sees 83% agreement and passes.

    The one chunk that changed is the answer. **An aggregate over a context
    cannot see which member of it mattered** — the same blindness week 7 found in
    answer recall, and week 9 in faithfulness."""
    before = {k: v for k, v in DOCS.items() if k != "rfc-8259"}
    query = next(q for q in dev() if q.id == "r05")
    report = staleness(build(before)[2](query.text), built()[2](query.text))
    assert report["overlap"] == pytest.approx(0.833, abs=0.01)
    assert report["missing"] == ["rfc-8259#12"]
