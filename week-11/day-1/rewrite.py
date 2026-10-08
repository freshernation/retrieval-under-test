"""Rewriting the query: the tool aimed at the failure week 10 found.

Week 10's attribution report named six failures. Two of them are station 4 — the
shortlist never contained the answer — and both are `paraphrase` queries that
week 6 independently flagged as retrieved by nothing. *"How do I stop search
engines indexing my site"* against a corpus that says `crawler`, `disallow` and
`access`.

Query rewriting is the technique pointed exactly at that. So this is the honest
test of it, on a failure identified before the technique was chosen rather than
after.

**One rule, and it is the whole integrity of the day.** You may not write a
synonym dictionary by looking at the failing queries. A rewrite rule built from
the failures is the eval set leaking into the system, and it will score
beautifully and generalise to nothing. Every rewrite here is derived from the
corpus or from the query alone.

Replace each `raise NotImplementedError` with your own code.
"""

from __future__ import annotations


def term_idf(index, term: str) -> float:
    """BM25's idf, from week 3. Rare terms carry the query; common ones dilute it."""
    raise NotImplementedError


def drop_low_idf(index, query_text: str, keep: float = 0.5) -> str:
    """Keep the `keep` fraction of distinct terms with the highest idf, in their
    original order.

    The cheapest rewrite there is: *"how do I stop search engines indexing my
    site"* loses `how`, `do`, `i`, `site`. No dictionary, no model, no
    assumptions — and the terms it drops are the ones contributing least to the
    score already, which is a reason to expect it to do very little.
    """
    raise NotImplementedError


def prf_terms(index, chunks: dict[str, str], shortlist, query_text: str = "", n: int = 5) -> list[str]:
    """Pseudo-relevance feedback: the top `n` terms of the shortlist's chunks,
    ranked by `count × idf`, excluding anything already in `query_text`.

    The exclusion matters. Without it the list is dominated by the query's own
    terms, the expansion adds almost nothing, and the technique appears to be
    harmless — which is a worse outcome than finding out what it does.

    The idea is decades old and it is sound: the documents you retrieved are
    probably about the right thing, so their vocabulary is probably useful.

    The failure mode is in the premise. If the first retrieval was wrong, the
    feedback terms come from the wrong documents, and the second retrieval is
    *more confidently* wrong. That is called query drift, and you will watch it
    happen to the two queries this day was aimed at.
    """
    raise NotImplementedError


def expand(query_text: str, terms) -> str:
    """The query with `terms` appended. Append rather than replace: a rewrite that
    discards the user's words is a rewrite that can lose an exact identifier,
    and week 5 measured what exact identifiers are worth here."""
    raise NotImplementedError


def variants(index, chunks: dict[str, str], query_text: str, shortlist) -> list[str]:
    """The original, the dropped version, and the expanded version — in that
    order, original first.

    Original first is not cosmetic. Week 6's RRF rewards agreement across input
    rankings, and a fan-out whose variants all drift together agrees loudly about
    the wrong documents.
    """
    raise NotImplementedError


def rewrite_report(answered_before: dict[str, bool], answered_after: dict[str, bool]) -> dict:
    """`gained`, `lost`, `before`, `after`, `delta`.

    `gained` and `lost` as sorted id lists, not counts. A net delta of -0.05
    hides two queries fixed and three broken, and those are different facts
    about the rewrite — one says what it is for, the other says what it costs.
    """
    raise NotImplementedError
