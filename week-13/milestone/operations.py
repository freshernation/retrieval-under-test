"""Milestone 13 — the service, operated.

Days 1 to 4 built a queue, a snapshot, a gate and a door. Today they become one
thing that starts, takes changes, survives a restart, and can say whether it is
ready.

The part that is easy to miss: **the versions are part of the index's state.**
Restart with the snapshot but without the versions and every change the queue
redelivers looks new - including the late copy of a document you withdrew.

Replace each `raise NotImplementedError` with your own code.
"""

from __future__ import annotations


def save_versions(path, versions: dict) -> None:
    """JSON of the versions, sorted by document id, written to `<path>.tmp` and
    os.replace'd onto `path` - day 2's rule for anything a crash must not half-write."""
    raise NotImplementedError


def boot(snapshot_path, versions_path, queue_path, documents: dict, chunker, **options) -> dict:
    """Start the service's state.

    A snapshot at `snapshot_path`: load it (day 2, with these options) and the
    versions file beside it; source "snapshot".
    No snapshot: build a LiveIndex from chunker(documents) with these options, every
    document at version 1, save both; source "built".

    Return {"index", "versions", "queue": ChangeQueue(queue_path), "source",
            "snapshot": <path as str>, "versions_path": <path as str>}."""
    raise NotImplementedError


def work_once(state: dict, chunker) -> dict:
    """Drain the queue (day 1). If anything was applied, save the snapshot and the
    versions. Return the tally."""
    raise NotImplementedError


def create_service(state: dict, acl: dict, keys: dict):
    """Day 4's app over this state."""
    raise NotImplementedError


def operations_check(state: dict, max_queued: int = 0) -> dict:
    """Is it ready to take traffic?

        {"ready": bool, "problems": [...], "debt": <4 places>}

    Problems, in this order: "<n> change(s) could not be applied" for any dead
    change; "<n> change(s) waiting" if more than `max_queued` are queued."""
    raise NotImplementedError
