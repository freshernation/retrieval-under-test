"""Day 2 — an index that survives a restart.

`test_the_wrong_analyzer_changes_nineteen_top_tens_and_raises_nothing` is the day.
"""

import json
from functools import cache

import pytest

import raglab
from bm25 import search
from liveindex import LiveIndex
from sections import section_corpus
from snapshot import SnapshotMismatch, fingerprint, load, manifest, save

CORPUS = raglab.corpus.load()
DOCS = {d.id: d.title + "\n" + d.text for d in CORPUS}


@cache
def chunks():
    return section_corpus(DOCS, 100, 300)


@cache
def queries():
    j = raglab.judgments.load(file="queries-extended.yml")
    return list(j.split("dev")) + list(j.split("test"))


def built():
    return LiveIndex(chunks(), stopwords=None)


def test_the_manifest():
    index = built()
    found = manifest(index)
    assert found["format"] == 1 and found["options"] == {"stopwords": None}
    assert found["n_documents"] == 266 and found["fingerprint"] == fingerprint(index)


def test_a_fingerprint_sees_a_tombstone():
    a, b = built(), built()
    b.tombstone(sorted(b.lengths)[0])
    assert fingerprint(a) != fingerprint(b)


def test_a_loaded_index_is_the_index(tmp_path):
    path = tmp_path / "index.json"
    index = built()
    index.tombstone(sorted(index.lengths)[0])
    save(index, path)
    back = load(path, stopwords=None)
    assert back.doc_ids == index.doc_ids and back.dead == index.dead
    for q in queries():
        assert search(back, q.text, 10) == search(index, q.text, 10)


def test_a_loaded_index_can_still_delete(tmp_path):
    path = tmp_path / "index.json"
    save(built(), path)
    back = load(path, stopwords=None)
    victim = sorted(back.lengths)[0]
    back.remove(victim)
    assert victim not in back.lengths and back.n_documents == 265


def test_a_crash_mid_save_keeps_the_old_snapshot(tmp_path):
    path = tmp_path / "index.json"
    save(built(), path)
    before = path.read_text()

    def dies(body, handle):
        handle.write('{"manifest": ')
        raise OSError("disk full")

    with pytest.raises(OSError):
        save(LiveIndex({"x": "nothing"}, stopwords=None), path, writer=dies)
    assert path.read_text() == before, "A half-written snapshot replaced a good one."


def test_the_wrong_analyzer_changes_nineteen_top_tens_and_raises_nothing():
    """Build without stopwords, then analyze queries with the default stoplist:
    19 of 26 top tens change, 6 of them at rank one. No error anywhere."""
    right, wrong = built(), built()
    wrong.options = {}
    tens = [q.id for q in queries() if search(wrong, q.text, 10) != search(right, q.text, 10)]
    ones = [q.id for q in queries() if search(wrong, q.text, 1) != search(right, q.text, 1)]
    assert (len(tens), len(ones)) == (19, 6)


def test_loading_with_other_options_is_refused(tmp_path):
    path = tmp_path / "index.json"
    save(built(), path)
    with pytest.raises(SnapshotMismatch):
        load(path)


def test_a_tampered_snapshot_is_refused(tmp_path):
    path = tmp_path / "index.json"
    save(built(), path)
    body = json.loads(path.read_text())
    first = sorted(body["lengths"])[0]
    body["lengths"][first] += 1
    path.write_text(json.dumps(body))
    with pytest.raises(SnapshotMismatch):
        load(path, stopwords=None)
