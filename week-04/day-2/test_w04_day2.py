"""Day 2 — answer spans, and the failure they make visible.

`test_the_metric_finally_sees_it` is the pair to yesterday's last test.
"""

from functools import cache

import pytest

import raglab
from spans import (
    answer_recall_at_k,
    broken_by,
    carrying_chunks,
    mean_answer_recall,
    smallest_overlap_that_saves,
    survives,
)
from windows import chunk_corpus

CORPUS = raglab.corpus.load()
DOCS = {d.id: d.title + "\n" + d.text for d in CORPUS}
QUERIES = raglab.judgments.load()
DEV = QUERIES.split("dev")


@cache
def chunked(size: int, overlap: int = 0):
    return chunk_corpus(DOCS, size, overlap)


# -- the spans themselves -----------------------------------------------------


def test_every_answerable_query_has_a_span_and_it_is_in_the_corpus():
    """Fifteen of sixteen. The sixteenth is `r10`, which is unanswerable and has
    nothing to point at."""
    whole = {d.id: d.title + "\n" + d.text for d in CORPUS}
    for q in QUERIES:
        if q.unanswerable:
            assert q.answer_spans == ()
            continue
        assert q.answer_spans
        found = set()
        for text in whole.values():
            found |= q.spans_in(text)
        assert found == set(q.answer_spans), q.id


def test_a_span_is_matched_after_collapsing_whitespace():
    """Chunking splits on whitespace and rejoins with single spaces, so a span
    must survive that. Nothing else is normalised — a quotation that needed
    adjusting to match is not evidence."""
    q = QUERIES.by_id("r05")
    assert q.spans_in("blah   MUST  be\n encoded    using UTF-8 blah") == set(q.answer_spans)
    assert q.spans_in("must be encoded using utf-8") == set()


def test_one_span_still_carries_week_two_damage():
    """`r11`'s span is `Although schemes are case- insensitive` — hyphenated
    across a line break in RFC 3986, and still hyphenated after extraction.

    A user searching for `case-insensitive` does not match it. Week 2's
    substitution damage, unrepaired, now load-bearing in the ground truth."""
    assert "case- insensitive" in QUERIES.by_id("r11").answer_spans[0]


def test_a_query_needing_two_documents_has_two_spans():
    r14 = QUERIES.by_id("r14")
    assert len(r14.answer_spans) == 2
    both = [DOCS["rfc-8259"], DOCS["rfc-7159"]]
    assert r14.is_answered_by(both)
    assert not r14.is_answered_by([DOCS["rfc-8259"]])


# -- survival -----------------------------------------------------------------


def test_carrying_chunks_finds_where_the_answer_lives():
    carriers = carrying_chunks(chunked(400), QUERIES.by_id("r05"))
    assert len(carriers) == 1
    assert next(iter(carriers)).startswith("rfc-8259#")


def test_overlap_duplicates_a_span_and_that_is_its_cost():
    q = QUERIES.by_id("r01")
    assert len(carrying_chunks(chunked(400, 200), q)) >= len(
        carrying_chunks(chunked(400), q)
    )


def test_an_unanswerable_query_does_not_survive_and_that_is_deliberate():
    """Slightly rude, and correct: it has nothing to survive, and counting it as
    a success would put it in your numerator."""
    assert survives(chunked(400), QUERIES.by_id("r10")) is False


def test_generous_chunking_breaks_nothing():
    assert broken_by(chunked(800), QUERIES) == []
    assert broken_by(chunked(400), QUERIES) == []


def test_two_hundred_words_with_no_overlap_destroys_an_answer():
    """One query. No index, no ranking, no model — a single pass over the chunk
    texts finds it, in under a second, before any retrieval happens."""
    assert broken_by(chunked(200), QUERIES) == ["r15"]


def test_and_sixty_word_chunks_destroy_a_different_one():
    assert broken_by(chunked(60), QUERIES) == ["r13"]


def test_overlap_repairs_both():
    assert broken_by(chunked(200, 25), QUERIES) == []
    assert broken_by(chunked(60, 15), QUERIES) == []


def test_the_smallest_overlap_that_saves_it_is_computable():
    """Overlap is usually chosen by folklore — "10% is standard". It is a
    function of your longest span and your chunk size, and you can just work it
    out."""
    r15 = QUERIES.by_id("r15")
    smallest = smallest_overlap_that_saves(DOCS, r15, 200, limit=40)
    assert smallest is not None and 0 < smallest <= 25
    assert survives(chunk_corpus(DOCS, 200, smallest), r15)
    assert not survives(chunk_corpus(DOCS, 200, smallest - 1), r15)


# -- the metric ---------------------------------------------------------------


def test_answer_recall_needs_every_span():
    r14 = QUERIES.by_id("r14")
    chunks = {"a": DOCS["rfc-8259"], "b": DOCS["rfc-7159"], "c": DOCS["rfc-3986"]}
    assert answer_recall_at_k(["a", "b"], chunks, r14, 2) == 1.0
    assert answer_recall_at_k(["a", "c"], chunks, r14, 2) == 0.0


def test_it_is_binary_because_a_context_window_is():
    """No partial credit for nearly. The window either contains the answer or it
    does not."""
    q = QUERIES.by_id("r05")
    chunks = {"hit": DOCS["rfc-8259"], "miss": DOCS["rfc-3986"]}
    assert answer_recall_at_k(["hit"], chunks, q, 1) == 1.0
    assert answer_recall_at_k(["miss"], chunks, q, 1) == 0.0


def test_k_is_respected():
    q = QUERIES.by_id("r05")
    chunks = {"miss": DOCS["rfc-3986"], "hit": DOCS["rfc-8259"]}
    assert answer_recall_at_k(["miss", "hit"], chunks, q, 1) == 0.0
    assert answer_recall_at_k(["miss", "hit"], chunks, q, 2) == 1.0


def test_unanswerable_queries_are_excluded_from_the_mean():
    """Not scored zero. An unanswerable query cannot fail to have its answer
    retrieved, and putting it in the denominator caps your metric below 1."""
    chunks = chunked(400)
    perfect = {q.id: [] for q in DEV}
    assert mean_answer_recall(perfect, chunks, DEV, 5) == 0.0
    assert len([q for q in DEV if q.answer_spans]) == 9


# -- and the pair to yesterday ------------------------------------------------


def test_the_metric_finally_sees_it():
    """Yesterday: 200/0 versus 200/25 scored 0.834 against 0.779 at document
    level, so the configuration that **destroys an answer** looked better.

    At span granularity, on the split that contains the destroyed query, the
    same comparison is 0.0 against 1.0. Not a fifth of a point — the answer is
    either in the index or it is not.

    The change was not in the retriever. It was in what you were willing to
    call a measurement."""
    r15 = QUERIES.by_id("r15")
    assert not survives(chunked(200), r15)
    assert survives(chunked(200, 25), r15)

    test_split = QUERIES.split("test")
    assert "r15" in {q.id for q in test_split}

    ranked = {"r15": list(carrying_chunks(chunked(200, 25), r15))}
    assert answer_recall_at_k(ranked["r15"], chunked(200, 25), r15, 5) == 1.0
    assert answer_recall_at_k([], chunked(200), r15, 5) == 0.0
