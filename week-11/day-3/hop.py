"""The second hop: retrieve, read what you got, retrieve again.

This is the corpus's set piece, and the course has been walking towards it since
week 2.

RFC 7159 says one thing about UTF-8. RFC 8259 obsoletes it in December 2017 and
says the opposite. The fact that makes the answer wrong **is not in the document
the answer came from** — so no amount of better ranking, better chunking or
better prompting can reach it, and week 8 watched the generator cite the
withdrawn document with a perfect faithfulness score.

A second hop can reach it. Retrieve, notice that a retrieved document has been
superseded, then retrieve again inside its successor. That is multi-hop
retrieval, and today it is eleven lines with no model in it anywhere.

Which is the finding you should be watching for.

Replace each `raise NotImplementedError` with your own code.
"""

from __future__ import annotations


def stale_in(context, graph: dict[str, str]) -> list[str]:
    """The chunk ids in `context` whose **document** has been superseded, sorted.

    `graph` is week 2's supersession map, built by parsing `Obsoletes:` out of
    the headers. It cost forty lines in week 2 and nothing since.
    """
    raise NotImplementedError


def successors(chunk_ids, graph: dict[str, str]) -> list[str]:
    """The current document ids for those chunks, sorted, following the chain to
    its end with week 2's `current_version`.

    Chains, not edges: a document can be obsoleted by a document that is itself
    obsoleted, and a one-step hop lands on another withdrawn specification.
    """
    raise NotImplementedError


def follow(deeper, docs, limit: int) -> list[str]:
    """The best `limit` chunks in `deeper` that belong to `docs`.

    `deeper` is a **deeper shortlist for the same query** — the second hop is
    another retrieval, and this is where its cost comes from. Reuse the ranking
    you already have rather than issuing a fresh query: you are not asking a new
    question, you are asking the same one of a narrower set.
    """
    raise NotImplementedError


def add_hop(shortlist, extra) -> list[str]:
    """`extra` first, then the original shortlist. The superseding document's
    evidence is now in the context alongside the superseded document's.

    This is the version everybody writes, and you should run it before you write
    the next one.
    """
    raise NotImplementedError


def replace_hop(shortlist, stale, extra) -> list[str]:
    """`extra` first, then the shortlist with **every chunk of every superseded
    document** removed — not merely the stale chunks you happened to notice.

    Removing one chunk promotes the next chunk of the same withdrawn document
    into the budget, and the citation comes back. The unit of supersession is the
    document; the unit you noticed it on was a chunk; and conflating the two
    produces a fix that works on four queries out of five.

    The difference between this and `add_hop` is two list comprehensions, and it
    is the difference between fixing the failure and not.
    """
    raise NotImplementedError


def hop_report(superseded: dict[str, list[str]], answered: dict[str, bool], retrievals: int) -> dict:
    """`citing_superseded` (sorted ids), `answered`, `retrievals`.

    All three, because this day's two interesting results are a metric going to
    zero and a different metric going down with it, and a report carrying one of
    them would be an advertisement.
    """
    raise NotImplementedError
