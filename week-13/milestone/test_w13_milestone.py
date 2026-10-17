"""Milestone 13 — the service, operated.

`test_a_restart_remembers_what_was_withdrawn` is the milestone.
"""

from fastapi.testclient import TestClient

import raglab
from ingestqueue import UPSERT, Change, chunks_of
from operations import boot, create_service, operations_check, save_versions, work_once
from sections import section_corpus
from windows import parent

CORPUS = raglab.corpus.load()
DOCS = {d.id: d.title + "\n" + d.text for d in CORPUS}
ACL = {d.id: set() for d in CORPUS}
KEYS = {"k-public-0123456789": {"name": "public", "groups": set(), "writer": False},
        "k-writer-0123456789": {"name": "publisher", "groups": set(), "writer": True}}
PUBLIC = {"Authorization": "Bearer k-public-0123456789"}
WRITER = {"Authorization": "Bearer k-writer-0123456789"}


def chunker(documents):
    return section_corpus(documents, 100, 300)


def start(tmp_path, documents=DOCS):
    return boot(tmp_path / "index.json", tmp_path / "versions.json", tmp_path / "queue.db",
                documents, chunker, stopwords=None)


def test_save_versions(tmp_path):
    save_versions(tmp_path / "v.json", {"b": 2, "a": 1})
    assert (tmp_path / "v.json").read_text() == '{"a": 1, "b": 2}'


def test_built_then_loaded(tmp_path):
    first = start(tmp_path)
    assert first["source"] == "built" and len(first["index"].doc_ids) == 266
    second = start(tmp_path)
    assert second["source"] == "snapshot" and second["index"].doc_ids == first["index"].doc_ids
    assert second["versions"] == {d: 1 for d in DOCS}


def test_a_change_through_the_door_survives_a_restart(tmp_path):
    without = {d: t for d, t in DOCS.items() if d != "rfc-9309"}
    state = start(tmp_path, without)
    http = TestClient(create_service(state, ACL, KEYS))
    http.post("/documents", json={"doc_id": "rfc-9309", "version": 1, "text": DOCS["rfc-9309"]}, headers=WRITER)
    assert work_once(state, chunker)["applied"] == 1

    again = start(tmp_path, without)
    found = TestClient(create_service(again, ACL, KEYS)).post(
        "/search", json={"query": "robots exclusion protocol"}, headers=PUBLIC).json()["results"]
    assert parent(found[0]) == "rfc-9309"


def test_a_restart_remembers_what_was_withdrawn(tmp_path):
    """Withdraw RFC 7159 at version 2, restart, then the queue redelivers the old
    version 1. With the versions saved, it is stale and 7159 stays gone."""
    state = start(tmp_path)
    TestClient(create_service(state, ACL, KEYS)).post(
        "/documents", json={"doc_id": "rfc-7159", "version": 2, "withdraw": True}, headers=WRITER)
    work_once(state, chunker)

    again = start(tmp_path)
    again["queue"].put(Change("rfc-7159", 1, UPSERT, DOCS["rfc-7159"]))
    assert work_once(again, chunker) == {"applied": 0, "stale": 1, "dead": 0}
    assert chunks_of(again["index"], "rfc-7159") == []


def test_ready_or_not(tmp_path):
    state = start(tmp_path)
    assert operations_check(state) == {"ready": True, "problems": [], "debt": 0.0}
    state["queue"].put(Change("rfc-2324", 2, UPSERT, None))
    state["queue"].put(Change("rfc-2324", 3, UPSERT, DOCS["rfc-2324"]))
    assert operations_check(state)["problems"] == ["2 change(s) waiting"]
    work_once(state, chunker)
    assert operations_check(state) == {"ready": False, "problems": ["1 change(s) could not be applied"],
                                       "debt": 0.0}


def lines(name):
    from pathlib import Path
    text = (Path(__file__).resolve().parent / name).read_text()
    kept = [l for l in text.splitlines() if l.strip() and not l.strip().startswith("#")]
    assert kept, f"{name} contains only comments so far - write it."
    return "\n".join(kept)


def test_the_dockerfile():
    text = lines("Dockerfile")
    assert text.startswith("FROM python:3.12")
    assert text.index("pip install") < text.index("COPY . .")
    assert "USER " in text and "0.0.0.0" in text and "/data" in text


def test_compose_runs_the_api_and_the_worker_on_one_volume():
    text = lines("compose.yaml")
    assert "worker:" in text and "run_worker.py" in text and text.count("data:/data") == 2
    assert "KEYS_FILE" in text
