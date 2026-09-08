"""Day 2 — the inverted index.

The number to carry into tomorrow: this corpus's longest document is more than
fifteen times its shortest.
"""

from functools import cache

import pytest

import raglab
from postings import Index, phrase, search_and, search_or

CORPUS = raglab.corpus.load()
DOCS = {d.id: d.title + "\n" + d.text for d in CORPUS}


@cache
def index() -> Index:
    return Index(DOCS, stopwords=None)


# -- structure ----------------------------------------------------------------


def test_the_index_knows_its_shape():
    idx = index()
    assert idx.n_documents == 10
    assert idx.vocabulary_size == 4273
    assert idx.total_postings() == 9969


def test_postings_carry_positions():
    p = index().postings("429")
    assert set(p) == {"rfc-6585"}
    assert len(p["rfc-6585"]) == 9
    assert all(isinstance(i, int) for i in p["rfc-6585"])


def test_an_unknown_term_is_empty_not_an_error():
    assert index().postings("kubernetes") == {}
    assert index().document_frequency("kubernetes") == 0


def test_term_and_document_frequency_are_different_questions():
    idx = index()
    assert idx.term_frequency("429", "rfc-6585") == 9
    assert idx.document_frequency("429") == 1
    assert idx.document_frequency("status") == 10


# -- lengths ------------------------------------------------------------------


def test_the_length_spread_is_the_argument_for_tomorrow():
    """1,247 tokens to 19,462 — a factor of **fifteen**. Any scorer that adds up
    per-term contributions without dividing by something will hand every query
    to RFC 3986, and week 1's `frequency_score` did exactly that."""
    lengths = index().lengths
    assert lengths["rfc-7725"] == 1247
    assert lengths["rfc-3986"] == 19462
    assert max(lengths.values()) / min(lengths.values()) > 15


def test_the_average_is_between_them_and_describes_neither():
    assert index().average_length == pytest.approx(5277.9, abs=0.1)


# -- boolean ------------------------------------------------------------------


def test_or_reproduces_week_one_exactly():
    """The index made it a lookup instead of a scan. It must not have made it a
    different retriever — "faster" and "different" are things you have to be
    able to tell apart."""
    import sys
    from pathlib import Path

    sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "week-01" / "day-4"))
    from overlap import rank

    for query in ("route 42 detour", "must JSON be encoded in UTF-8", "451"):
        hits = search_or(index(), query)
        ranked = sorted(hits, key=lambda d: (-hits[d], d))[:5]
        assert ranked == rank(query, DOCS, 5)


def test_and_is_precise_and_brittle():
    """Two documents contain all three of `too`, `many` and `requests`."""
    assert search_and(index(), "too many requests") == {"rfc-6585", "rfc-8615"}


def test_one_unusual_word_empties_an_and_query():
    """And the user cannot tell which word did it. This is why boolean search
    lost, and it is worth having built the thing that lost."""
    assert search_and(index(), "too many requests kubernetes") == set()


def test_an_empty_query_returns_nothing_rather_than_everything():
    assert search_and(index(), "") == set()
    assert search_or(index(), "") == {}


# -- phrases ------------------------------------------------------------------


def test_the_phrase_finds_exactly_one():
    """OR ties two documents at three terms each. AND returns both. The phrase
    returns the one whose section is literally called `429 Too Many Requests`.

    This is the sharpest tool in the lexical box."""
    hits = search_or(index(), "too many requests")
    assert hits["rfc-6585"] == hits["rfc-8615"] == 3
    assert search_and(index(), "too many requests") == {"rfc-6585", "rfc-8615"}
    assert phrase(index(), "too many requests") == {"rfc-6585"}


def test_phrases_need_adjacency_in_order():
    assert phrase(index(), "network authentication required") == {"rfc-6585"}
    assert phrase(index(), "required authentication network") == set()


def test_a_phrase_that_is_not_there():
    assert phrase(index(), "rate limiting policy") == set()


def test_every_term_must_share_one_start_position():
    """The trap that caught this course's own reference solution.

    RFC 2324 contains `coffee pot` and it contains `of`. If you check each term
    against the first term's positions independently, `pot of coffee` matches —
    every term found *a* start that worked, and no single start worked for all
    of them. The document does not contain the phrase.

    The bug produces plausible extra results and raises nothing."""
    assert phrase(index(), "coffee pot") == {"rfc-2324"}
    assert phrase(index(), "pot of coffee") == set()


def test_and_the_fragility_that_comes_with_it():
    """`coffee pot` and `coffee pots` are both in the corpus, and the user does
    not know which they need. `pot of tea` is not, and neither is any paraphrase.

    Phrase search requires the user to have used the document's exact wording.
    They usually have not — which is week 5's argument, arriving three weeks
    early and from an unexpected direction."""
    assert phrase(index(), "coffee pots") == {"rfc-2324"}
    assert phrase(index(), "pot of tea") == set()
    assert phrase(index(), "rate limiting policy") == set()
