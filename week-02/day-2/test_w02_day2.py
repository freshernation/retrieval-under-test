"""Day 2 — repairing the damage, and measuring whether it helped.

Read the last three tests together, in order. They are the week.
"""

from functools import cache

import pytest

import raglab
from boilerplate import (
    clean,
    collapse_blank_runs,
    front_matter_end,
    reduction,
    rejoin_paragraphs,
    strip_front_matter,
    strip_furniture,
)

CORPUS = raglab.corpus.load()
RAW = {d.id: d.title + "\n" + d.text for d in CORPUS}


@cache
def cleaned() -> dict[str, str]:
    """Lazy, so that an unwritten `clean` fails these tests rather than stopping
    the whole week from collecting."""
    return {d.id: d.title + "\n" + clean(d.text) for d in CORPUS}


# -- stripping ----------------------------------------------------------------


def test_furniture_is_gone():
    out = strip_furniture(CORPUS["rfc-7725"].text)
    assert "\f" not in out
    assert "[Page 1]" not in out
    assert "HTTP-status-451               February 2016" not in out


def test_the_content_survives():
    out = strip_furniture(CORPUS["rfc-7725"].text)
    assert "451" in out and "legal obstacles" in out.lower()


def test_the_unpaginated_document_is_untouched():
    """Nothing to strip, so nothing changes. Your cleaner is a no-op on a tenth
    of the corpus and reports success."""
    assert strip_furniture(CORPUS["rfc-9309"].text) == CORPUS["rfc-9309"].text


# -- front matter -------------------------------------------------------------


def test_the_body_starts_after_the_table_of_contents():
    """`1.  Introduction` appears twice — once in the contents, once as the real
    heading. Taking the first occurrence puts your body start inside the table of
    contents, and every number after that is subtly wrong."""
    lines = CORPUS["rfc-7725"].text.split("\n")
    i = front_matter_end(CORPUS["rfc-7725"].text)
    assert lines[i].startswith("1.")
    assert "Table of Contents" not in "\n".join(lines[i:])


def test_it_works_on_the_odd_one_out():
    assert front_matter_end(CORPUS["rfc-9309"].text) > 0


def test_stripping_front_matter_throws_away_the_abstract():
    """You are deleting something valuable to delete something useless. That is a
    trade, not a cleanup, and it belongs in the loss report as a trade."""
    before = CORPUS["rfc-7725"].text
    after = strip_front_matter(before)
    assert "Abstract" in before and "Abstract" not in after
    assert "Copyright Notice" not in after


# -- whitespace and reflow ----------------------------------------------------


def test_blank_runs_collapse():
    assert collapse_blank_runs("a\n\n\n\n\nb") == "a\n\nb"
    assert collapse_blank_runs("a\n\n\nb", max_run=2) == "a\n\n\nb"


def test_paragraphs_become_single_lines():
    assert rejoin_paragraphs("one\ntwo\n\nthree") == "one two\n\nthree"


def test_stripping_furniture_alone_does_not_heal_the_sentence():
    """The damage outlives the thing that caused it. Delete the footer and the
    header and you are left with the blank lines that padded the bottom of the
    page — so the sentence is still two paragraphs and still retrieves as two
    fragments, neither containing the whole rule."""
    import re

    from boilerplate import heal_page_splits

    stripped = strip_furniture(CORPUS["rfc-3986"].text)
    assert re.search(r"nothing in this\n\s*\n\s*specification", stripped)
    healed = rejoin_paragraphs(heal_page_splits(stripped))
    assert "nothing in this specification" in healed


def test_a_sentence_split_by_a_page_is_a_sentence_again():
    out = clean(CORPUS["rfc-3986"].text)
    assert "Nevertheless, nothing in this specification prevents an application" in out


def test_the_order_of_operations_matters():
    """Rejoining before stripping welds a page footer onto the end of a
    paragraph, where it becomes part of a sentence and is unrecoverable."""
    out = clean(CORPUS["rfc-7725"].text)
    assert "[Page" not in out


# -- what it cost -------------------------------------------------------------


def test_cleaning_removes_between_a_fifth_and_two_fifths_of_the_corpus():
    for doc_id in RAW:
        pct = reduction(RAW[doc_id], cleaned()[doc_id])["pct_removed"]
        assert 15.0 < pct < 40.0


def test_the_shortest_document_loses_the_most():
    """RFC 7725 loses 38.9%; RFC 3986 loses 18.3%. Boilerplate is a fixed cost per
    document, so it is a proportional catastrophe for short ones — and reporting a
    corpus total would have hidden exactly that."""
    short = reduction(RAW["rfc-7725"], cleaned()["rfc-7725"])["pct_removed"]
    long = reduction(RAW["rfc-3986"], cleaned()["rfc-3986"])["pct_removed"]
    assert short == pytest.approx(38.9, abs=0.2)
    assert long == pytest.approx(18.3, abs=0.2)
    assert short > 2 * long


# -- and whether it was worth it ----------------------------------------------
#
# These three are the week. Read them in order and do not skip to the third.


def test_it_changes_nothing_at_k_equals_three():
    """You have just deleted up to 39% of every document. recall@3 and ndcg@3 are
    **identical to four decimal places**, on every query.

    Not nearly identical. Identical. At whole-document granularity, boilerplate
    was never what decided which document matched."""
    import sys
    from pathlib import Path

    sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "week-01" / "day-4"))
    from overlap import rank

    from raglab.metrics import evaluate

    qs = raglab.judgments.load().split("dev")
    after = evaluate({q.id: rank(q.text, cleaned(), 10) for q in qs}, qs, ks=(3, 5))
    before = evaluate({q.id: rank(q.text, RAW, 10) for q in qs}, qs, ks=(3, 5))
    assert after.metrics["recall@3"] == before.metrics["recall@3"]
    assert after.metrics["ndcg@3"] == before.metrics["ndcg@3"]


def test_the_one_thing_that_moves_is_one_query():
    """recall@5 goes 0.852 → 0.963, which looks like a result until you look at
    which queries moved. Exactly one did: r01, from 0.00 to 1.00.

    Nine answerable queries. One moved."""
    import sys
    from pathlib import Path

    sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "week-01" / "day-4"))
    from overlap import rank

    from raglab.metrics import evaluate

    qs = raglab.judgments.load().split("dev")
    after = evaluate({q.id: rank(q.text, cleaned(), 10) for q in qs}, qs, ks=(5,))
    before = evaluate({q.id: rank(q.text, RAW, 10) for q in qs}, qs, ks=(5,))
    moved = [
        q.id
        for q in qs
        if after.per_query[q.id]["recall@5"] != before.per_query[q.id]["recall@5"]
    ]
    assert moved == ["r01"]
    assert before.per_query["r01"]["recall@5"] == 0.0
    assert after.per_query["r01"]["recall@5"] == 1.0


def test_and_the_interval_says_you_measured_nothing():
    """delta +0.111, 95% CI [+0.000, +0.333]. The interval touches zero.

    So: you removed a third of the corpus, threw away every abstract, wrote a
    cleaner with four stages and an order-of-operations trap in it — and by the
    rule in EVALS.md you have **no result**.

    The conclusion is not that cleaning is useless. It is that cleaning is not
    justified *by this measurement*, at whole-document granularity, on nine
    queries. Hold the change. Write it down as unproven. Re-measure in week 4,
    when the unit of retrieval stops being a document and a page of boilerplate
    becomes an entire chunk.

    This is the most important test in week 2, and the discipline it is teaching
    is the one everybody's instinct fights."""
    import sys
    from pathlib import Path

    sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "week-01" / "day-4"))
    from overlap import rank

    from raglab.metrics import bootstrap, evaluate

    qs = raglab.judgments.load().split("dev")
    after = evaluate({q.id: rank(q.text, cleaned(), 10) for q in qs}, qs, ks=(5,))
    before = evaluate({q.id: rank(q.text, RAW, 10) for q in qs}, qs, ks=(5,))
    delta, low, high = bootstrap(after, before, "recall@5")
    assert delta == pytest.approx(0.111, abs=0.001)
    assert low <= 0 <= high
