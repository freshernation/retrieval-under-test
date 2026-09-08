"""Day 1 — counting what the format did to the text.

The test to read before anything else:
`test_one_document_in_this_corpus_has_no_pages_at_all`. Every assumption you are
about to make about page furniture is false for a tenth of this corpus, and
nothing anywhere announces it.
"""

import pytest

import raglab
from damage import (
    blank_run_lengths,
    furniture_lines,
    is_page_footer,
    is_running_header,
    loss_report,
    page_break_lines,
    repeated_lines,
    split_paragraphs,
)

CORPUS = raglab.corpus.load()
DOCS = {d.id: d.text for d in CORPUS}

FOOTER = "Bray                         Standards Track                    [Page 8]"
HEADER = "RFC 7725                     HTTP-status-451               February 2016"


# -- page furniture -----------------------------------------------------------


def test_form_feeds_are_found():
    assert len(page_break_lines(DOCS["rfc-7725"])) == 5
    assert len(page_break_lines(DOCS["rfc-3986"])) == 61


def test_one_document_in_this_corpus_has_no_pages_at_all():
    """RFC 9309 was published in 2022 under the unpaginated RFC format. It has no
    form feeds, no page footers and no running headers.

    Nine documents from one publisher in one format, and one that is not. Nothing
    in the corpus announces this. Every cleaner you write today will silently do
    nothing to a tenth of your text, and on your own corpus the tenth will not be
    a document you had heard of."""
    assert page_break_lines(DOCS["rfc-9309"]) == []
    assert furniture_lines(DOCS["rfc-9309"]) == []


def test_a_footer_is_recognised():
    assert is_page_footer(FOOTER)
    assert not is_page_footer("   The 429 status code indicates that the user has sent")


def test_a_header_is_recognised():
    assert is_running_header(HEADER)


def test_a_citation_is_not_a_header():
    """`RFC 2119` appears constantly in normal prose. A cleaner that deletes every
    line starting with `RFC` eats real content, and the month is what tells them
    apart."""
    assert not is_running_header("   as described in RFC 2119 and updated by RFC 8174")
    assert not is_running_header("RFC 3986 defines the generic syntax")


def test_furniture_is_about_five_percent_of_a_paginated_document():
    """Not a rounding error. Every one of those lines is a term your retriever
    will match a query against — author surnames, the word `Standards`, page
    numbers, and the document's own title on every single page."""
    for doc_id in ("rfc-3986", "rfc-6265", "rfc-7159", "rfc-8259"):
        report = loss_report({doc_id: DOCS[doc_id]})[doc_id]
        assert 4.5 < report["furniture_pct"] < 6.0


# -- whitespace ---------------------------------------------------------------


def test_long_blank_runs_are_pagination_and_short_ones_are_paragraphs():
    """You cannot tell them apart by looking at one blank line, which is why a
    cleaner that collapses all whitespace destroys the paragraph structure it
    was relying on."""
    runs = blank_run_lengths(DOCS["rfc-7725"])
    assert max(runs) >= 6
    assert runs.count(1) > 10


# -- broken paragraphs --------------------------------------------------------


def test_sentences_cut_by_a_page_break_are_found():
    """RFC 3986 has seventeen. Each one retrieves as two fragments, and neither
    fragment contains the whole rule — a station 1 failure that will present
    itself to you as a station 4 one."""
    assert len(split_paragraphs(DOCS["rfc-3986"])) == 17


def test_a_short_document_may_have_none():
    assert split_paragraphs(DOCS["rfc-7725"]) == []


def test_the_break_is_reported_before_the_furniture():
    lines = DOCS["rfc-3986"].split("\n")
    for i in split_paragraphs(DOCS["rfc-3986"]):
        assert lines[i].strip()
        assert not lines[i].rstrip().endswith(".")


# -- boilerplate --------------------------------------------------------------


def test_boilerplate_is_found_without_being_described():
    """This matters more than it looks. On your own corpus you will not know what
    the boilerplate is, and a line appearing verbatim in most documents is a
    definition that does not require you to."""
    shared = repeated_lines(DOCS, min_documents=3)
    assert "Copyright Notice" in shared and shared["Copyright Notice"] == 10
    assert "Status of This Memo" in shared


def test_raising_the_threshold_shrinks_the_set():
    assert len(repeated_lines(DOCS, 8)) < len(repeated_lines(DOCS, 3))


def test_boilerplate_hurts_the_shortest_document_most():
    """RFC 7725 is four pages, and 39 of its 284 lines are text it shares with
    other documents — about one line in seven. RFC 3986 is 141 KB and shares 7.

    Boilerplate is a fixed cost per document, so it is a proportional catastrophe
    for short ones. Every short document in your corpus is mostly furniture, and
    week 4 is where that turns into a retrieval failure."""
    report = loss_report(DOCS)
    assert report["rfc-7725"]["repeated"] == 39
    assert report["rfc-3986"]["repeated"] == 7
    short = report["rfc-7725"]["repeated"] / report["rfc-7725"]["lines"]
    long = report["rfc-3986"]["repeated"] / report["rfc-3986"]["lines"]
    assert short > 10 * long


def test_the_1998_document_shares_almost_nothing():
    """RFC 2324 is from 1998 and its boilerplate is from a different era of the
    same publisher. Two shared lines out of 564.

    Corpora are heterogeneous across *time* as well as format, and a cleaner
    tuned on the documents you happened to look at first will quietly not work on
    the old ones."""
    assert loss_report(DOCS)["rfc-2324"]["repeated"] == 2


# -- the report ---------------------------------------------------------------


def test_the_report_covers_every_document():
    report = loss_report(DOCS)
    assert set(report) == set(DOCS)
    assert set(report["rfc-7725"]) == {
        "lines",
        "furniture",
        "furniture_pct",
        "split_paragraphs",
        "repeated",
    }


def test_the_report_is_the_deliverable():
    """An ingest reports what it lost. Almost none do, which is why 'the answer
    was not in the corpus' is so often discovered six months late, by a user."""
    report = loss_report(DOCS)
    damaged = sum(1 for r in report.values() if r["furniture"] or r["split_paragraphs"])
    assert damaged == 9
