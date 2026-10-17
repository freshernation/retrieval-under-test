"""Day 1 — changes arrive out of order.

`test_in_arrival_order_the_index_is_wrong_nineteen_times_in_twenty` is the day.
"""

import random
from functools import cache

import pytest

import raglab
from ingestqueue import UPSERT, WITHDRAW, Change, ChangeQueue, apply, apply_naive, chunks_of, drain, snapshot_of
from liveindex import LiveIndex
from sections import section_corpus

CORPUS = raglab.corpus.load()
DOCS = {d.id: d.title + "\n" + d.text for d in CORPUS}


def chunker(documents):
    return section_corpus(documents, 100, 300)


def revised(text):
    lines = text.splitlines()
    return "\n".join(lines[: len(lines) // 2])


@cache
def log():
    """Every RFC published at version 1; then two withdrawn and one revised."""
    changes = [Change(d, 1, UPSERT, DOCS[d]) for d in sorted(DOCS)]
    return changes + [Change("rfc-7159", 2, WITHDRAW), Change("rfc-5785", 2, WITHDRAW),
                      Change("rfc-6265", 2, UPSERT, revised(DOCS["rfc-6265"]))]


def replay(order, versioned):
    index, versions = LiveIndex(stopwords=None), {}
    for change in order:
        if versioned:
            apply(index, versions, change, chunker)
        else:
            apply_naive(index, change, chunker)
    return snapshot_of(index)


@cache
def truth():
    return replay(log(), versioned=True)


def deliveries(n=20):
    """At least once, in any order: the log, plus two changes delivered twice."""
    out = []
    for seed in range(n):
        order = list(log()) + [log()[3], log()[10]]
        random.Random(seed).shuffle(order)
        out.append(order)
    return out


# -- one change ---------------------------------------------------------------


def test_chunks_of():
    index = LiveIndex(chunker({"rfc-9309": DOCS["rfc-9309"]}), stopwords=None)
    assert chunks_of(index, "rfc-9309") == sorted(index.lengths)
    assert chunks_of(index, "rfc-2324") == []


def test_an_upsert_replaces_every_chunk():
    index = LiveIndex(stopwords=None)
    apply_naive(index, Change("rfc-6265", 1, UPSERT, DOCS["rfc-6265"]), chunker)
    before = len(chunks_of(index, "rfc-6265"))
    apply_naive(index, Change("rfc-6265", 2, UPSERT, revised(DOCS["rfc-6265"])), chunker)
    assert 0 < len(chunks_of(index, "rfc-6265")) < before


def test_a_withdrawal_removes_every_chunk():
    index = LiveIndex(chunker({"rfc-7159": DOCS["rfc-7159"]}), stopwords=None)
    apply_naive(index, Change("rfc-7159", 2, WITHDRAW), chunker)
    assert chunks_of(index, "rfc-7159") == [] and index.n_documents == 0


def test_an_upsert_with_no_text_is_refused():
    with pytest.raises(ValueError):
        apply_naive(LiveIndex(stopwords=None), Change("x", 1, UPSERT, "  "), chunker)


def test_a_stale_change_changes_nothing():
    index, versions = LiveIndex(stopwords=None), {}
    apply(index, versions, Change("rfc-6265", 2, UPSERT, revised(DOCS["rfc-6265"])), chunker)
    before = snapshot_of(index)
    assert apply(index, versions, Change("rfc-6265", 1, UPSERT, DOCS["rfc-6265"]), chunker) == "stale"
    assert snapshot_of(index) == before and versions == {"rfc-6265": 2}


def test_a_withdrawal_is_remembered():
    """The late copy of version 1 must not bring a withdrawn document back."""
    index, versions = LiveIndex(stopwords=None), {}
    apply(index, versions, Change("rfc-7159", 2, WITHDRAW), chunker)
    assert apply(index, versions, Change("rfc-7159", 1, UPSERT, DOCS["rfc-7159"]), chunker) == "stale"
    assert chunks_of(index, "rfc-7159") == []


# -- the day -------------------------------------------------------------------


def test_in_order_both_ways_agree():
    assert replay(log(), versioned=False) == truth()
    assert len(truth()) == 211


def test_in_arrival_order_the_index_is_wrong_nineteen_times_in_twenty():
    """Shuffle the log, deliver two changes twice, and apply in arrival order: the
    final index differs from the right one in 19 of 20 deliveries. With versions,
    in none."""
    naive = sum(replay(order, versioned=False) != truth() for order in deliveries())
    versioned = sum(replay(order, versioned=True) != truth() for order in deliveries())
    assert (naive, versioned) == (19, 0)


def test_twice_is_the_same_as_once():
    order = list(log())
    assert replay(order + order, versioned=True) == truth()


# -- the queue -----------------------------------------------------------------


def test_the_queue_keeps_its_order_and_survives_reopening(tmp_path):
    path = str(tmp_path / "q.db")
    queue = ChangeQueue(path)
    first = queue.put(Change("a", 1, UPSERT, "hello"))
    queue.put(Change("b", 1, WITHDRAW))
    again = ChangeQueue(path)
    seq, change = again.claim()
    assert seq == first and change == Change("a", 1, UPSERT, "hello")
    assert again.counts() == {"working": 1, "queued": 1}


def test_a_bad_change_is_set_aside_after_three_tries(tmp_path):
    queue = ChangeQueue(str(tmp_path / "q.db"))
    queue.put(Change("rfc-9309", 1, UPSERT, None))
    queue.put(Change("rfc-2324", 1, UPSERT, DOCS["rfc-2324"]))
    index, versions = LiveIndex(stopwords=None), {}
    assert drain(queue, index, versions, chunker) == {"applied": 1, "stale": 0, "dead": 1}
    assert queue.counts() == {"dead": 1, "done": 1}
    assert chunks_of(index, "rfc-2324"), "One bad document must not stop the changes behind it."


def test_draining_a_shuffled_delivery(tmp_path):
    queue = ChangeQueue(str(tmp_path / "q.db"))
    for change in deliveries()[0]:
        queue.put(change)
    index, versions = LiveIndex(stopwords=None), {}
    tally = drain(queue, index, versions, chunker)
    assert tally["applied"] + tally["stale"] == len(deliveries()[0]) and tally["dead"] == 0
    assert snapshot_of(index) == truth()
