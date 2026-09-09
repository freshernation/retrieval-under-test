"""Day 4 — filters, and where you put them."""

from functools import cache

import pytest

import raglab
from filters import (
    chunk_metadata,
    current_only,
    post_filter,
    pre_filter,
    published_since,
    shortfall,
    survival,
)
from sections import section_corpus
from spans import answer_recall_at_k

CORPUS = raglab.corpus.load()
DOCS = {d.id: d.title + "\n" + d.text for d in CORPUS}


@cache
def dev():
    return [q for q in raglab.judgments.load(file="queries-extended.yml").split("dev") if q.answer_spans]


@cache
def setup():
    import sys
    from pathlib import Path

    root = Path(__file__).resolve().parents[2]
    for day in ("day-3", "day-2", "day-1"):
        sys.path.insert(0, str(root / "week-03" / day))
    from bm25 import search

    from postings import Index

    chunks = section_corpus(DOCS, 100, 300)
    index = Index(chunks, stopwords=None)
    meta = chunk_metadata(chunks, CORPUS)
    return chunks, meta, lambda text, depth: search(index, text, depth)


# -- metadata -----------------------------------------------------------------


def test_every_chunk_reaches_its_document():
    """Week 4 insisted a chunk carry its parent in its id. This is why: a filter
    on document metadata is impossible over chunks that cannot name where they
    came from."""
    chunks, meta, _ = setup()
    assert set(meta) == set(chunks)
    assert all(row["doc"] in DOCS for row in meta.values())


def test_the_supersession_graph_survives_chunking():
    chunks, meta, _ = setup()
    stale = {c for c, row in meta.items() if not row["current"]}
    assert stale
    assert {meta[c]["doc"] for c in stale} == {"rfc-7159", "rfc-5785"}


def test_missing_metadata_fails_a_date_filter():
    """A document with no date is not known to satisfy a date filter. That is a
    choice, it is the safe one, and on a real corpus the undated fraction is
    rarely small."""
    predicate = published_since({"x": {"year": None}}, 2015)
    assert predicate("x") is False
    assert predicate("never-seen") is False


# -- the two placements -------------------------------------------------------


def test_post_filter_can_leave_you_short():
    assert post_filter(["a", "b", "c"], lambda c: c == "a", 5) == ["a"]
    assert shortfall(["a"], 5) == 4
    assert shortfall(["a", "b", "c", "d", "e"], 5) == 0


def test_pre_filter_restricts_the_corpus():
    chunks, meta, _ = setup()
    kept = pre_filter(chunks, current_only(meta))
    assert len(kept) == 238
    assert len(kept) < len(chunks)


def test_they_agree_on_recall_when_the_shortlist_is_deep():
    """This is the reassuring result and it is conditional. With 50 candidates
    and a filter keeping 89% of the corpus, post-filtering loses nothing."""
    import sys
    from pathlib import Path

    root = Path(__file__).resolve().parents[2]
    for day in ("day-2", "day-1"):
        sys.path.insert(0, str(root / "week-03" / day))
    from bm25 import search

    from postings import Index

    chunks, meta, lexical = setup()
    predicate = current_only(meta)
    kept = pre_filter(chunks, predicate)
    pre_index = Index(kept, stopwords=None)

    post = sum(
        answer_recall_at_k(post_filter(lexical(q.text, 50), predicate, 5), chunks, q, 5)
        for q in dev()
    ) / len(dev())
    pre = sum(
        answer_recall_at_k(search(pre_index, q.text, 5), kept, q, 5) for q in dev()
    ) / len(dev())
    assert post == pre == pytest.approx(0.789, abs=0.005)


# -- where they come apart ----------------------------------------------------


def test_a_shallow_shortlist_starves_the_post_filter():
    """**The ANN case.** Ask for 5 from a shortlist of 5 and a filter that drops
    one in ten leaves you with 4.5 on average. Deepen the shortlist and the
    shortfall vanishes.

    With an approximate index you cannot simply deepen it — the candidates are
    not the true top-n either — so a post-filter over ANN results loses recall
    twice, and neither loss is reported by anything."""
    chunks, meta, lexical = setup()
    predicate = current_only(meta)
    shallow = [shortfall(post_filter(lexical(q.text, 5), predicate, 5), 5) for q in dev()]
    deep = [shortfall(post_filter(lexical(q.text, 50), predicate, 5), 5) for q in dev()]
    assert sum(shallow) / len(shallow) > 5 * (sum(deep) / len(deep))


def test_a_selective_filter_returns_nothing_for_some_queries():
    """`published_since(2015)` keeps 63 of 266 chunks. Mean shortfall is 0.63
    and the **maximum is 5** — at least one query, given fifty candidates,
    has no result at all that satisfies the filter."""
    chunks, meta, lexical = setup()
    predicate = published_since(meta, 2015)
    assert sum(1 for c in chunks if predicate(c)) == 63
    shortfalls = [shortfall(post_filter(lexical(q.text, 50), predicate, 5), 5) for q in dev()]
    assert max(shortfalls) == 5
    assert sum(shortfalls) / len(shortfalls) == pytest.approx(0.63, abs=0.05)


def test_survival_tells_you_how_deep_to_go():
    """If 10% survive, a post-filter for the top 5 needs roughly 50 candidates.
    That is the calculation nobody does, and it is one line."""
    chunks, meta, lexical = setup()
    strict = published_since(meta, 2015)
    loose = current_only(meta)
    rates = [survival(lexical(q.text, 20), strict, 20) for q in dev()]
    assert sum(rates) / len(rates) < 0.5
    assert survival(lexical(dev()[0].text, 20), loose, 20) > 0.8


# -- and the honest reading ---------------------------------------------------


def test_the_recall_a_filter_costs_is_not_a_bug():
    """`published_since(2015)` takes answer recall from 0.789 to 0.316.

    That is not a defect. Most of the answers are in documents published before
    2015, and the user asked not to see them. The filter did exactly what it was
    told.

    What would be a defect is reporting 0.316 as retrieval quality. **A filtered
    system must be measured against what the filter allows**, not against the
    unfiltered corpus, or you will spend a quarter trying to fix a requirement."""
    chunks, meta, lexical = setup()
    predicate = published_since(meta, 2015)
    filtered = sum(
        answer_recall_at_k(post_filter(lexical(q.text, 50), predicate, 5), chunks, q, 5)
        for q in dev()
    ) / len(dev())
    unfiltered = sum(
        answer_recall_at_k(lexical(q.text, 5), chunks, q, 5) for q in dev()
    ) / len(dev())
    assert filtered == pytest.approx(0.316, abs=0.01)
    assert unfiltered == pytest.approx(0.789, abs=0.01)
