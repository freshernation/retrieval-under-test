"""Changes arrive out of order.

Week 12 changed the index by hand: a delete here, an add there, each one called by
you, in the order you chose. In a running system changes arrive from outside - a
publisher, a sync job, a person clicking "withdraw" - and they arrive through a
queue that promises only that each one is delivered **at least once**. Not once.
Not in order.

So two things are true of every change you receive: you may have seen it before,
and something newer may already have been applied.

The fix is old and boring and it works: every change carries a **version** for its
document, and you apply a change only if it is newer than the last one you applied
for that document. A withdrawal is a version too - forget that, and a late copy of
the original arrives and brings the withdrawn document back.

The queue itself lives on disk, so a crash loses nothing, and a change that cannot
be applied is tried three times and then set aside, so one bad document does not
stop every change behind it.

Replace each `raise NotImplementedError` with your own code.
"""

from __future__ import annotations

from dataclasses import dataclass

UPSERT = "upsert"
WITHDRAW = "withdraw"
MAX_ATTEMPTS = 3


@dataclass(frozen=True)
class Change:
    """One change to one document. `text` is the whole new document for an upsert,
    None for a withdrawal."""

    doc_id: str
    version: int
    action: str
    text: str | None = None


def chunks_of(index, doc_id: str) -> list[str]:
    """The ids of every chunk stored for this document, sorted. A chunk's document
    is `windows.parent(chunk_id)`."""
    raise NotImplementedError


def apply_naive(index, change: Change, chunker) -> str:
    """Apply in whatever order changes arrive. Remove every chunk of the document;
    for an upsert, add `chunker({doc_id: text})`'s chunks. An upsert with no text
    raises ValueError, as does an unknown action. Returns "applied"."""
    raise NotImplementedError


def apply(index, versions: dict[str, int], change: Change, chunker) -> str:
    """The same - unless `change.version` is not newer than `versions[doc_id]`
    (0 if unseen), in which case change nothing and return "stale". After a change
    is applied, record its version - including a withdrawal's."""
    raise NotImplementedError


def snapshot_of(index) -> dict[str, int]:
    """{chunk_id: length} for every live chunk, sorted by id - what you compare to
    say two indexes hold the same thing."""
    raise NotImplementedError


class ChangeQueue:
    """A queue of changes in a SQLite file.

        ChangeQueue(path)              sqlite3.connect(path, isolation_level=None,
                                       check_same_thread=False) - a web server will
                                       call it from more than one thread (day 4)
        .put(change) -> seq            store it as JSON, status "queued"
        .claim() -> (seq, Change) | None
                                       the oldest queued change, now "working"
        .done(seq)                     status "done"
        .fail(seq, error) -> status    one more attempt; "dead" at MAX_ATTEMPTS,
                                       otherwise back to "queued"; keep the error
        .counts() -> {status: n}
    """

    def __init__(self, path: str) -> None:
        raise NotImplementedError

    def put(self, change: Change) -> int:
        raise NotImplementedError

    def claim(self):
        raise NotImplementedError

    def done(self, seq: int) -> None:
        raise NotImplementedError

    def fail(self, seq: int, error: str) -> str:
        raise NotImplementedError

    def counts(self) -> dict[str, int]:
        raise NotImplementedError


def drain(queue: ChangeQueue, index, versions: dict[str, int], chunker) -> dict[str, int]:
    """Claim and apply until the queue is empty. A change that raises is failed,
    not fatal. Returns {"applied": n, "stale": n, "dead": n}."""
    raise NotImplementedError
