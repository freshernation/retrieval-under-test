"""A service with a door.

Everything so far has been called by you, from Python, with every document visible.
A service is called by other people, over HTTP, each of whom may see some
documents and not others, and some of whom may change the corpus.

So three routes and two kinds of key:

    POST /search      any key; results filtered by what that key's groups may read
                      (week 12's `reader` - fail closed)
    POST /documents   a writer key only; the change goes on day 1's queue and the
                      answer is 202 Accepted - queued, not done
    GET  /health      no key; how much is indexed, the debt, and how many changes
                      are queued or dead

The 202 is the part people get wrong. A document you were told was "accepted" is not
searchable until a worker has drained the queue. That gap is the price of not
indexing inside the request, and /health is how you see it.

Replace each `raise NotImplementedError` with your own code.
"""

from __future__ import annotations

from pydantic import BaseModel, Field


class SearchIn(BaseModel):
    query: str = Field(min_length=1, max_length=500)
    k: int = Field(default=5, ge=1, le=20)


class DocumentIn(BaseModel):
    doc_id: str = Field(min_length=1)
    version: int = Field(ge=1)
    text: str | None = None
    withdraw: bool = False


def caller_for(header: str, keys: dict[str, dict]):
    """keys maps an API key to {"name", "groups": set, "writer": bool}. Return the
    caller for a header of "Bearer <key>", or None. Compare with
    secrets.compare_digest, against every key."""
    raise NotImplementedError


def create_app(index, acl: dict, keys: dict[str, dict], queue, versions: dict):
    """A FastAPI app over a LiveIndex, the corpus ACL, the keys, day 1's queue and
    its versions.

        GET  /health     {"status": "ok", "chunks": <live chunks>, "debt": <4 places>,
                          "queued": n, "dead": n}
        POST /search     SearchIn; 401 without a key. BM25 top 60 (week 3's search),
                         keep what reader(acl, caller groups) allows, first k:
                         {"results": [chunk ids]}
        POST /documents  DocumentIn; 401 without a key, 403 for a key that is not a
                         writer, 422 for an upsert with no text. Otherwise put a
                         Change on the queue and answer 202 {"seq": n, "status": "queued"}
    """
    raise NotImplementedError
