"""The ingest, and the report that says what it lost.

Four days of pieces, assembled into one pass over the corpus that produces a
searchable text **and a manifest**. The manifest is the deliverable. Almost no
ingest pipeline in the world produces one, which is why "the answer was not in
the corpus" is so often discovered six months late, by a user.

Everything here composes what you already wrote. `day-1/damage.py`,
`day-2/boilerplate.py`, `day-3/dedupe.py` and `day-4/lineage.py` are importable —
your conftest puts week 2 on the path.

Replace each `raise NotImplementedError` with your own code.
"""

from __future__ import annotations

import sys
from pathlib import Path

_WEEK = Path(__file__).resolve().parents[1]
for _day in ("day-1", "day-2", "day-3", "day-4"):
    sys.path.insert(0, str(_WEEK / _day))


def ingest(documents: dict[str, str]) -> dict[str, str]:
    """Clean every document. Returns id to cleaned text.

    One line, if day 2 went well. It is here so that the manifest and the search
    below are looking at the same text you measured, which sounds obvious and is
    the most common way an ingest report stops describing the index.
    """
    raise NotImplementedError


def manifest(documents: dict[str, str]) -> dict[str, dict]:
    """Per document, everything you learned this week:

        chars_before, chars_after, pct_removed   (day 2)
        furniture, split_paragraphs              (day 1)
        superseded_by                            (day 4, or None)
        near_duplicate_of                        (day 3, or None — highest
                                                  scoring partner at >= 0.5 on
                                                  the *cleaned* text)

    Two rules about this dict, and they are the milestone:

    - **Per document, never a corpus total.** The total hides that the shortest
      document lost 39% and the longest lost 18%, and that difference is the
      finding
    - **Absent facts are `None`, not missing keys.** A consumer that has to use
      `.get()` will eventually stop checking
    """
    raise NotImplementedError


def search(
    query: str, index: dict[str, str], graph: dict[str, str], rank_fn, k: int = 10
) -> list[tuple[str, str | None]]:
    """Retrieve, demote superseded documents, and annotate what is stale.

    Returns `(doc_id, superseded_by_or_None)` pairs. The annotation travels with
    the result rather than being looked up later, because a caller who has to
    remember to check will not, and the failure is silent and confident.
    """
    raise NotImplementedError


def coverage_gaps(manifest_rows: dict[str, dict]) -> list[str]:
    """The sentences your report has to contain, generated from the manifest.

    One string per finding, sorted. Say it plainly, in the form a reader who does
    not know what a shingle is can act on:

    - `"<id>: 39% of the text was removed as boilerplate"` for anything over 30%
    - `"<id>: superseded by <other> and still in the index"`
    - `"<id>: 55% identical to <other>"` for near-duplicates
    - `"<id>: <n> sentences were cut by a page boundary"` for anything over 10

    Generating the prose from the data rather than writing it by hand is the
    difference between a report that stays true and one that was true in March.
    """
    raise NotImplementedError
