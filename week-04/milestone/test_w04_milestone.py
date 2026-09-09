"""Week 4 milestone — choosing a chunker on evidence.

`test_the_decision_needs_two_numbers_you_cannot_measure` is the one to read.
"""

from functools import cache

import pytest

import raglab
from chunker import Chunker, audit, decide, frontier

CORPUS = raglab.corpus.load()
DOCS = {d.id: d.title + "\n" + d.text for d in CORPUS}
QUERIES = raglab.judgments.load()
DEV = QUERIES.split("dev")

CHUNKERS = {
    "whole documents": Chunker("whole"),
    "fixed 400": Chunker("fixed", size=400, overlap=0),
    "fixed 200/25": Chunker("fixed", size=200, overlap=25),
    "sections 100-300": Chunker("sections", min_words=100, max_words=300),
    "sections 60-150": Chunker("sections", min_words=60, max_words=150),
}


def bm25_rank(query: str, chunks: dict[str, str], k: int) -> list[str]:
    import sys
    from pathlib import Path

    root = Path(__file__).resolve().parents[2]
    for day in ("day-3", "day-2", "day-1"):
        sys.path.insert(0, str(root / "week-03" / day))
    from bm25 import search

    from postings import Index

    return search(_index(tuple(sorted(chunks.items()))), query, k)


@cache
def _index(frozen: tuple):
    import sys
    from pathlib import Path

    root = Path(__file__).resolve().parents[2]
    for day in ("day-2", "day-1"):
        sys.path.insert(0, str(root / "week-03" / day))
    from postings import Index

    return Index(dict(frozen), stopwords=None)


@cache
def measured():
    return frontier(CHUNKERS, DOCS, DEV, bm25_rank)


# -- the chunker --------------------------------------------------------------


def test_not_chunking_is_a_configuration_not_a_special_case():
    """So that "leave the documents alone" sits on the same frontier as
    everything else, rather than being the baseline you forget to compare
    against."""
    whole = Chunker("whole").chunk(DOCS)
    assert whole == DOCS


def test_the_config_records_the_strategy():
    """Two configs with the same numbers and different strategies must not
    collide in the run ledger."""
    from raglab.runs import config_hash

    a = Chunker("fixed", size=300).config
    b = Chunker("sections", min_words=100, max_words=300).config
    assert a["strategy"] == "fixed" and b["strategy"] == "sections"
    assert config_hash(a) != config_hash(b)


def test_the_config_is_complete():
    assert Chunker("fixed").config == {"strategy": "fixed", "size": 400, "overlap": 0}


def test_an_unknown_strategy_is_refused():
    with pytest.raises(ValueError):
        Chunker("semantic")


# -- the audit ----------------------------------------------------------------


def test_the_audit_reports_the_shape():
    report = audit(Chunker("sections", min_words=100, max_words=300).chunk(DOCS), QUERIES)
    assert report["n_chunks"] == 266
    assert report["max_words"] <= 300
    assert report["empty"] == []


def test_the_audit_finds_a_destroyed_answer_without_retrieving_anything():
    """No index, no queries executed, no model. One pass over the chunk texts,
    and it catches the failure that no downstream stage can repair."""
    report = audit(Chunker("fixed", size=200, overlap=0).chunk(DOCS), QUERIES)
    assert report["broken"] == ["r15"]


def test_and_says_nothing_when_there_is_nothing_to_say():
    report = audit(Chunker("sections", min_words=100, max_words=300).chunk(DOCS), QUERIES)
    assert report["broken"] == []


def test_orphans_are_found_when_documents_are_given():
    chunks = {"rfc-7725#0": "text", "ghost#0": "text"}
    assert audit(chunks, QUERIES, DOCS)["orphans"] == ["ghost#0"]
    assert audit(chunks, QUERIES)["orphans"] == []


# -- the frontier -------------------------------------------------------------


def test_the_frontier_discards_most_of_the_options():
    points, front = measured()
    assert len(points) == len(CHUNKERS) * 4
    assert len(front) < len(points) / 3


def test_both_are_returned_because_the_report_needs_both():
    """A frontier with the dominated points hidden looks like a set of good
    options rather than a set of options."""
    points, front = measured()
    assert set(front) <= set(points)


def test_the_recommended_size_is_dominated():
    _, front = measured()
    assert "fixed 400" not in {p.name for p in front}


# -- the decision -------------------------------------------------------------


def test_a_requirement_that_cannot_be_met_returns_nothing():
    """Not the nearest thing. A refusal is a conversation with whoever set the
    requirement; a silent near-miss is not."""
    points, _ = measured()
    assert decide(points, target=1.0, budget=100) is None
    assert decide(points, target=1.01) is None


def test_the_decision_needs_two_numbers_you_cannot_measure():
    """**The milestone.**

    At `target=1.0` the answer is `sections 100-300` at k=5, for 984 words.
    At `target=0.75` it is a much smaller chunker for 359 — a third of the cost,
    and one query in four where the answer is not in the context at all.

    Neither number is a retrieval question. How often it is acceptable to miss
    entirely, and how much context you will pay for, come from outside the
    system — and if you do not choose them deliberately, your chunk size chooses
    them for you and nobody finds out which values it picked."""
    points, _ = measured()
    strict = decide(points, target=1.0)
    relaxed = decide(points, target=0.75)

    assert strict.name == "sections 100-300" and strict.k == 5
    assert strict.tokens == pytest.approx(984, abs=30)
    assert relaxed.tokens < strict.tokens / 2
    assert relaxed.recall < 1.0


def test_a_budget_changes_the_answer():
    points, _ = measured()
    assert decide(points, target=0.75, budget=2000).tokens <= 2000
    generous = decide(points, target=0.75, budget=100_000)
    tight = decide(points, target=0.75, budget=400)
    assert tight.tokens <= generous.tokens
