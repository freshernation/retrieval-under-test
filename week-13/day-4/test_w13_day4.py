"""Day 4 — a service with a door.

`test_accepted_is_not_searchable_until_the_queue_is_drained` is the day.
"""

from functools import cache

from fastapi.testclient import TestClient

import raglab
from ingestqueue import ChangeQueue, chunks_of, drain
from liveindex import LiveIndex
from searchapi import caller_for, create_app
from sections import section_corpus
from windows import parent

CORPUS = raglab.corpus.load()
DOCS = {d.id: d.title + "\n" + d.text for d in CORPUS}
RESTRICTED = {"rfc-2324", "rfc-6585", "rfc-7725"}
ACL = {d.id: ({"staff"} if d.id in RESTRICTED else set()) for d in CORPUS}
KEYS = {"k-public-0123456789": {"name": "public", "groups": set(), "writer": False},
        "k-staff-01234567890": {"name": "staff", "groups": {"staff"}, "writer": False},
        "k-writer-0123456789": {"name": "publisher", "groups": set(), "writer": True}}
PUBLIC = {"Authorization": "Bearer k-public-0123456789"}
STAFF = {"Authorization": "Bearer k-staff-01234567890"}
WRITER = {"Authorization": "Bearer k-writer-0123456789"}


def chunker(documents):
    return section_corpus(documents, 100, 300)


def service(tmp_path, documents=None):
    index = LiveIndex(chunker(documents if documents is not None else DOCS), stopwords=None)
    queue = ChangeQueue(str(tmp_path / "q.db"))
    versions = {d: 1 for d in (documents if documents is not None else DOCS)}
    return TestClient(create_app(index, ACL, KEYS, queue, versions)), index, queue, versions


def test_caller_for():
    assert caller_for("Bearer k-staff-01234567890", KEYS)["name"] == "staff"
    assert caller_for("Bearer nope", KEYS) is None and caller_for("", KEYS) is None


def test_health_needs_no_key(tmp_path):
    http, *_ = service(tmp_path)
    assert http.get("/health").json() == {"status": "ok", "chunks": 266, "debt": 0.0, "queued": 0, "dead": 0}


def test_search_needs_a_key(tmp_path):
    http, *_ = service(tmp_path)
    assert http.post("/search", json={"query": "418"}).status_code == 401


def test_a_public_key_never_sees_a_restricted_rfc(tmp_path):
    http, *_ = service(tmp_path)
    public = http.post("/search", json={"query": "what does the 418 status code mean", "k": 10},
                       headers=PUBLIC).json()["results"]
    staff = http.post("/search", json={"query": "what does the 418 status code mean", "k": 10},
                      headers=STAFF).json()["results"]
    assert not any(parent(c) in RESTRICTED for c in public)
    assert any(parent(c) == "rfc-2324" for c in staff)


def test_only_a_writer_may_change_documents(tmp_path):
    http, *_ = service(tmp_path)
    body = {"doc_id": "rfc-7159", "version": 2, "withdraw": True}
    assert http.post("/documents", json=body, headers=PUBLIC).status_code == 403
    assert http.post("/documents", json=body, headers=WRITER).status_code == 202
    assert http.post("/documents", json={"doc_id": "x", "version": 1}, headers=WRITER).status_code == 422


def test_accepted_is_not_searchable_until_the_queue_is_drained(tmp_path):
    """202 means queued. Until a worker drains the queue, the new RFC is not there -
    and /health is the only place that says so."""
    without = {d: t for d, t in DOCS.items() if d != "rfc-9309"}
    http, index, queue, versions = service(tmp_path, without)
    query = {"query": "robots exclusion protocol", "k": 5}
    accepted = http.post("/documents", json={"doc_id": "rfc-9309", "version": 1, "text": DOCS["rfc-9309"]},
                         headers=WRITER)
    assert accepted.status_code == 202 and accepted.json()["status"] == "queued"
    found = http.post("/search", json=query, headers=PUBLIC).json()["results"]
    assert not any(parent(c) == "rfc-9309" for c in found)
    assert http.get("/health").json()["queued"] == 1

    drain(queue, index, versions, chunker)
    found = http.post("/search", json=query, headers=PUBLIC).json()["results"]
    assert parent(found[0]) == "rfc-9309"
    assert http.get("/health").json()["queued"] == 0


def test_a_withdrawal_through_the_door(tmp_path):
    http, index, queue, versions = service(tmp_path)
    http.post("/documents", json={"doc_id": "rfc-7159", "version": 2, "withdraw": True}, headers=WRITER)
    drain(queue, index, versions, chunker)
    assert chunks_of(index, "rfc-7159") == []
    assert http.get("/health").json()["chunks"] == 266 - 18
