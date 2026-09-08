"""Day 4 — provenance, and the fix that the metrics cannot justify.

Read the last two tests together. They are the most careful thing in week 2.
"""

import sys
from functools import cache
from pathlib import Path

import pytest

import raglab
from lineage import (
    annotate,
    current_version,
    demote_superseded,
    is_current,
    parse_header,
    supersession,
)

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "week-01" / "day-4"))
from overlap import rank  # noqa: E402

CORPUS = raglab.corpus.load()
RAW = {d.id: d.text for d in CORPUS}
FULL = {d.id: d.title + "\n" + d.text for d in CORPUS}


@cache
def graph() -> dict[str, str]:
    """Lazy, so an unwritten `supersession` fails these tests individually."""
    return supersession(RAW)


# -- parsing ------------------------------------------------------------------


def test_the_obvious_case():
    h = parse_header(RAW["rfc-8259"])
    assert h["rfc"] == 8259
    assert h["obsoletes"] == [7159]
    assert h["updates"] == []
    assert h["category"] == "Standards Track"
    assert h["date"] == "December 2017" and h["year"] == 2017


def test_a_document_with_both_relationships():
    h = parse_header(RAW["rfc-8615"])
    assert h["obsoletes"] == [5785] and h["updates"] == [7230, 7595]


def test_the_category_stops_at_the_author_column():
    """`Category: Standards Track       G. Illyes` is a category of "Standards
    Track". Two or more spaces is the column separator, and a lazy `.+$` puts an
    author's name inside your category field for one document in ten."""
    assert parse_header(RAW["rfc-9309"])["category"] == "Standards Track"


def test_the_header_window_must_survive_the_busiest_document():
    """RFC 3986 carries STD, Updates *and* Obsoletes, which pushes its date down
    to line 12. A twelve-line window works on nine documents and loses the date
    on the one with the most metadata."""
    h = parse_header(RAW["rfc-3986"])
    assert h["obsoletes"] == [2732, 2396, 1808]
    assert h["updates"] == [1738]
    assert h["year"] == 2005


def test_the_byte_order_mark_does_not_break_it():
    assert parse_header(RAW["rfc-9309"])["rfc"] == 9309


def test_a_day_first_date_still_parses():
    """RFC 2324 dates itself `1 April 1998`. Everything else uses `Month YYYY`."""
    h = parse_header(RAW["rfc-2324"])
    assert h["year"] == 1998 and h["category"] == "Informational"


def test_absence_is_represented_as_absence():
    h = parse_header(RAW["rfc-7725"])
    assert h["obsoletes"] == [] and h["updates"] == []


# -- the graph ----------------------------------------------------------------


def test_both_supersessions_are_found():
    """The two pairs day 3 could not separate by similarity — 0.547 and 0.185 —
    are here, exactly and unambiguously, because somebody wrote them down."""
    assert graph() == {"rfc-7159": "rfc-8259", "rfc-5785": "rfc-8615"}


def test_it_is_built_from_the_newer_document():
    """RFC 7159 will never mention RFC 8259; an RFC is never edited after
    publication. The fact that makes 7159's answer wrong is in 8259."""
    assert "8259" not in RAW["rfc-7159"]
    assert "Obsoletes: 7159" in RAW["rfc-8259"]


def test_documents_you_do_not_have_are_ignored():
    """RFC 7159 obsoletes 4627 and 7158, neither of which is in the corpus. A
    KeyError here would be a crash caused entirely by a document being absent."""
    assert parse_header(RAW["rfc-7159"])["obsoletes"] == [4627, 7158]
    assert "rfc-4627" not in graph() and "rfc-7158" not in graph()


def test_current_and_superseded():
    assert is_current("rfc-8259", graph())
    assert not is_current("rfc-7159", graph())


def test_chains_are_followed_to_the_end():
    chain = {"a": "b", "b": "c"}
    assert current_version("a", chain) == "c"
    assert current_version("c", chain) == "c"


def test_a_cycle_raises_rather_than_hanging():
    with pytest.raises(ValueError):
        current_version("a", {"a": "b", "b": "a"})


# -- using it -----------------------------------------------------------------


def test_annotation_marks_what_is_stale():
    assert annotate(["rfc-7159", "rfc-8259"], graph()) == [
        ("rfc-7159", "rfc-8259"),
        ("rfc-8259", None),
    ]


def test_demotion_moves_stale_results_down_without_dropping_them():
    assert demote_superseded(["rfc-7159", "rfc-2324", "rfc-8259"], graph()) == [
        "rfc-2324",
        "rfc-8259",
        "rfc-7159",
    ]


def test_the_obsolete_json_spec_stops_outranking_the_current_one():
    """The week's headline. For `must JSON be encoded in UTF-8`, the week-1
    baseline returns RFC 7159 — the obsolete one, which says UTF-16 is fine —
    **above** RFC 8259. Demotion fixes it, and nothing in the text could have."""
    q = raglab.judgments.load().by_id("r05")
    before = rank(q.text, FULL, 10)
    assert before[0] == "rfc-7159"
    assert demote_superseded(before, graph())[0] == "rfc-8259"


# -- and whether the numbers agree --------------------------------------------


def test_nothing_gets_worse():
    """Necessary, and it is the part people skip. Every query is checked, not the
    mean — a change that helps on average while breaking one class of question is
    the most common way a retrieval system quietly gets worse for the people who
    depend on it most."""
    from raglab.metrics import evaluate

    qs = raglab.judgments.load().split("dev")
    before = evaluate({q.id: rank(q.text, FULL, 10) for q in qs}, qs, ks=(3,))
    after = evaluate(
        {q.id: demote_superseded(rank(q.text, FULL, 10), graph()) for q in qs}, qs, ks=(3,)
    )
    assert after.worse_than(before, "ndcg@3") == []
    assert after.per_query["r05"]["ndcg@3"] > before.per_query["r05"]["ndcg@3"]


def test_and_the_interval_still_will_not_confirm_it():
    """ndcg@3 goes 0.651 → 0.720. The interval is [+0.000, +0.125]. It touches
    zero, so by the letter of rule 1 you have not measured an improvement — for
    the second time this week.

    **Ship it anyway, and be able to say why.** This is not a tuning change
    chasing a metric. It is a *correctness* fix: returning a specification that
    was withdrawn in 2017 is wrong on nine queries and on nine million, and it
    would still be wrong if the eval set contained no query that noticed.

    The measurement's job here is not to justify the change. It is to prove the
    change cost nothing — `test_nothing_gets_worse` above — which is the question
    an interval on nine queries can actually answer.

    Know which kind of change you are making. A tuning change with no delta is
    superstition; a correctness fix with no delta is a correctness fix on an eval
    set too small to see it. Saying which, out loud, in the report, is the
    difference between discipline and ritual."""
    from raglab.metrics import bootstrap, evaluate

    qs = raglab.judgments.load().split("dev")
    before = evaluate({q.id: rank(q.text, FULL, 10) for q in qs}, qs, ks=(3,))
    after = evaluate(
        {q.id: demote_superseded(rank(q.text, FULL, 10), graph()) for q in qs}, qs, ks=(3,)
    )
    delta, low, high = bootstrap(after, before, "ndcg@3")
    assert delta > 0
    assert low <= 0 <= high
