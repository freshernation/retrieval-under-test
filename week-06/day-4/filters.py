"""Filters, and where you put them.

Week 2 built a supersession graph and demoted stale results. Today it becomes a
**filter**, and filtering turns out to be a place where the order of operations
changes the answer.

Two options, and every retrieval system picks one whether or not anybody
decided:

    pre-filter   restrict the corpus, then retrieve from what is left
    post-filter  retrieve, then drop what fails the predicate

They give the same results when your shortlist is deep. They come apart when it
is not — and with an approximate index it is never as deep as you think.

`day-4/lineage.py` from week 2 and `day-1/windows.py` from week 4 are importable.

Replace each `raise NotImplementedError` with your own code.
"""

from __future__ import annotations

from lineage import supersession
from windows import parent


def chunk_metadata(chunks: dict[str, str], corpus) -> dict[str, dict]:
    """Chunk id → `doc`, `year`, `rfc`, `superseded_by`, `current`.

    Every field comes from the **document**, reached through `parent()`. This is
    why week 4 insisted a chunk carry its parent in its id: a filter on document
    metadata is impossible over chunks that cannot name where they came from,
    and by the time you notice, re-chunking is the only fix.
    """
    raise NotImplementedError


def current_only(meta: dict[str, dict]):
    """A predicate accepting chunks from documents nothing supersedes.

    Week 2's graph, four weeks later, as one line. Note that it is now a *hard*
    filter where week 2 used a soft demotion — and that the two are different
    products: demotion keeps the obsolete document available for "what changed",
    and this removes it.
    """
    raise NotImplementedError


def published_since(meta: dict[str, dict], year: int):
    """A predicate accepting chunks from documents published in `year` or later.

    Missing metadata fails the predicate. That is a choice and it is the safe
    one — a document with no date is not known to satisfy a date filter — and it
    is worth knowing you made it, because on a real corpus the undated fraction
    is rarely small.
    """
    raise NotImplementedError


def post_filter(ranked: list[str], predicate, k: int) -> list[str]:
    """Filter a ranking, then take `k`.

    Cheap and it has one failure mode: **you can end up with fewer than `k`
    results, or none at all**, and the shallower your shortlist the more often.
    """
    raise NotImplementedError


def pre_filter(chunks: dict[str, str], predicate) -> dict[str, str]:
    """Restrict the corpus before retrieval.

    Always returns `k` results if `k` survive the filter, and costs you an index
    per filter — or a rebuild per query, which is worse. Fine for a handful of
    known filters, impossible for arbitrary ones.
    """
    raise NotImplementedError


def shortfall(results: list[str], k: int) -> int:
    """How many short of `k` you came. **Report this.**

    A retrieval system that silently returns three results when asked for five
    looks identical to one that found three good ones, and the difference is
    entirely the difference between a working system and a broken filter.
    """
    raise NotImplementedError


def survival(ranked: list[str], predicate, depth: int) -> float:
    """Fraction of the top `depth` that passes the predicate.

    The number that tells you how deep a shortlist you need. If 10% survive, a
    post-filter for the top 5 needs roughly 50 candidates — and if you are
    retrieving those 50 from an approximate index, they are not the true top 50.
    """
    raise NotImplementedError
