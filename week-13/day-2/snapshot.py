"""An index that survives a restart.

Every index so far lived as long as the Python process that built it. A service
that rebuilds its index on every start is a service that is down for as long as
indexing takes - and that is building from whichever corpus it can see at that
moment, which may not be the one you measured.

So the index is written to disk, and read back. Two things make this harder than
`json.dump`.

- **A half-written file is worse than no file.** A crash in the middle of a save
  must leave the previous snapshot intact. Write to a temporary file, then
  replace the old one in one step (`os.replace` is atomic on the same disk).
- **An index is only meaningful with the analyzer that built it.** Load an index
  built without stopwords into a service that removes them from queries, and every
  query is scored against terms it no longer contains. Nothing errors. So the
  snapshot carries a manifest, and loading refuses a mismatch.

Replace each `raise NotImplementedError` with your own code.
"""

from __future__ import annotations

FORMAT = 1


class SnapshotMismatch(Exception):
    """The snapshot cannot be used as asked - and saying so is the whole point."""


def fingerprint(index) -> str:
    """sha256 hex of json.dumps({"lengths": sorted(index.lengths.items()),
    "dead": sorted(index.dead)}). Two indexes with the same stored chunks, lengths
    and tombstones have the same fingerprint."""
    raise NotImplementedError


def manifest(index) -> dict:
    """{"format": FORMAT, "options": index.options, "n_documents": index.n_documents,
    "fingerprint": fingerprint(index)}"""
    raise NotImplementedError


def save(index, path, writer=None) -> None:
    """Write {"manifest", "lengths", "dead" (sorted), "postings": {term: {chunk:
    positions}}} as JSON, through `writer(body, handle)` (json.dump if None), to
    `<path>.tmp` - then os.replace it onto `path`. If `writer` raises, the old
    file at `path` must be untouched. (LiveIndex keeps its postings in
    `index._postings`; reading a private attribute of your own week 12 class is
    allowed here.)"""
    raise NotImplementedError


def load(path, **options):
    """Read a snapshot back into a LiveIndex - postings, lengths, tombstones, and
    the per-chunk term sets `remove` needs. Raise SnapshotMismatch if the format is
    not FORMAT, if `options` are not the options it was built with, or if the
    rebuilt index's fingerprint is not the manifest's."""
    raise NotImplementedError
