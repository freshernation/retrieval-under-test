"""Day 1 — changing an index in place.

`test_a_tombstoned_index_is_not_the_index_you_would_build` is the day.
"""

from functools import cache

import raglab
from bm25 import search
from liveindex import LiveIndex, drift
from postings import Index
from sections import section_corpus
from windows import parent

CORPUS = raglab.corpus.load()
DOCS = {d.id: d.title + "\n" + d.text for d in CORPUS}
WITHDRAWN = {"rfc-7159", "rfc-5785"}  # both obsoleted, by 8259 and 8615


@cache
def chunks():
    return section_corpus(DOCS, 100, 300)


@cache
def judged():
    j = raglab.judgments.load(file="queries-extended.yml")
    return list(j.split("dev")), list(j.split("dev")) + list(j.split("test"))


def live_chunks():
    return {c: t for c, t in chunks().items() if parent(c) not in WITHDRAWN}


def tombstoned():
    index = LiveIndex(chunks(), stopwords=None)
    for c in chunks():
        if parent(c) in WITHDRAWN:
            index.tombstone(c)
    return index


# -- the same index, built another way ----------------------------------------


def test_an_index_built_by_adding_is_the_index():
    """Add 266 chunks one at a time and you have week 3's index: same counts,
    same postings, and the same top ten for all twenty-six queries."""
    live, built = LiveIndex(chunks(), stopwords=None), Index(chunks(), stopwords=None)
    assert live.n_documents == built.n_documents == 266
    assert live.doc_ids == built.doc_ids
    assert live.average_length == built.average_length
    assert live.postings("json") == built.postings("json")
    for q in judged()[1]:
        assert search(live, q.text, 10) == search(built, q.text, 10)


def test_adding_an_existing_id_replaces_it():
    index = LiveIndex({"a": "cookie cookie cookie", "b": "status code"}, stopwords=None)
    index.add("a", "status")
    assert index.n_documents == 2
    assert index.document_frequency("cookie") == 0
    assert index.document_frequency("status") == 2
    assert index.lengths["a"] == 1


def test_remove_takes_everything_with_it():
    """Postings, length, and the vocabulary entry of any term nobody else uses."""
    index = LiveIndex({"a": "cookie jar", "b": "status code"}, stopwords=None)
    index.remove("a")
    assert index.doc_ids == ["b"]
    assert "a" not in index.lengths
    assert index.postings("cookie") == {}
    assert index.document_frequency("jar") == 0
    index.remove("never-there")  # ignored


def test_removing_gives_back_the_index_you_would_have_built():
    index = LiveIndex(chunks(), stopwords=None)
    for c in chunks():
        if parent(c) in WITHDRAWN:
            index.remove(c)
    rebuilt = Index(live_chunks(), stopwords=None)
    assert index.n_documents == rebuilt.n_documents == 238
    assert drift(index, rebuilt, judged()[1], 10, search) == []


# -- the cheap way out --------------------------------------------------------


def test_a_tombstone_hides_the_document():
    index = tombstoned()
    dev, _ = judged()
    assert not any(parent(c) in WITHDRAWN for q in dev for c in search(index, q.text, 10))
    assert len(index.doc_ids) == 238
    assert len(index.dead) == 28


def test_and_changes_nothing_else():
    """Twenty-eight dead chunks, and the index still believes in all of them.

    `json` is in 32 chunks according to the tombstoned index and 16 according
    to one built from the live corpus: half its document frequency belongs to a
    withdrawn RFC."""
    index, rebuilt = tombstoned(), Index(live_chunks(), stopwords=None)
    assert index.n_documents == 266 and rebuilt.n_documents == 238
    assert index.document_frequency("json") == 32
    assert rebuilt.document_frequency("json") == 16
    assert index.average_length != rebuilt.average_length


def test_a_tombstoned_index_is_not_the_index_you_would_build():
    """**Eight of twenty top-tens differ. No top-one does.**

    No dead document is returned, and the ranking of the live ones has still
    moved, because BM25 is computed from statistics that count the dead.

    Both halves matter. Eight of twenty is too many to call the indexes the
    same. Zero changed first results is why nobody notices: every spot check
    passes."""
    dev, _ = judged()
    index, rebuilt = tombstoned(), Index(live_chunks(), stopwords=None)
    assert len(drift(index, rebuilt, dev, 10, search)) == 8
    assert len(drift(index, rebuilt, dev, 5, search)) == 4
    assert drift(index, rebuilt, dev, 1, search) == []


def test_debt_is_the_number_to_watch():
    assert LiveIndex(chunks(), stopwords=None).debt == 0.0
    assert round(tombstoned().debt, 3) == 0.105
    assert LiveIndex().debt == 0.0


def test_compaction_pays_it_off():
    dev, _ = judged()
    index, rebuilt = tombstoned(), Index(live_chunks(), stopwords=None)
    assert index.compact() == 28
    assert index.debt == 0.0 and index.dead == set()
    assert index.n_documents == 238
    assert drift(index, rebuilt, dev, 10, search) == []
    assert index.compact() == 0


def test_tombstoning_something_that_is_not_there_is_not_debt():
    index = LiveIndex({"a": "x"}, stopwords=None)
    index.tombstone("ghost")
    assert index.debt == 0.0


def test_drift_reports_ids_in_the_order_given():
    dev, _ = judged()
    index, rebuilt = tombstoned(), Index(live_chunks(), stopwords=None)
    found = drift(index, rebuilt, dev, 10, search)
    order = [q.id for q in dev]
    assert found == sorted(found, key=order.index)
