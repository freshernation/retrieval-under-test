"""Week 1 milestone — the plumbing, and the audit.

The test to read: `test_unjudged_documents_in_the_top_k_are_found`. Those
documents scored zero in every metric you computed, and some of them were right.
"""

from pathlib import Path

import pytest

import raglab
from baseline import judged_coverage, read_queries, search_all, unjudged_in_top_k

SAMPLE = Path(raglab.corpus.DATA_ROOT) / "sample" / "queries.yml"
CORPUS = raglab.corpus.load("sample")
DOCS = {d.id: d.title + "\n" + d.text for d in CORPUS}


def fake_rank(query: str, documents: dict[str, str], k: int = 10) -> list[str]:
    """A deterministic stand-in, so these tests do not depend on day 4."""
    return sorted(documents)[:k]


# -- read_queries -------------------------------------------------------------


def test_it_reads_a_query_file():
    qs = read_queries(SAMPLE)
    assert len(qs) == 12
    assert qs.by_id("q07").text == "what does ROCC stand for"
    assert qs.by_id("q07").judgments["mrta-030"] == 3


def test_splits_survive_the_round_trip():
    qs = read_queries(SAMPLE)
    assert len(qs.split("dev")) == 8 and len(qs.split("test")) == 4


def test_a_bad_grade_is_refused_at_load_time(tmp_path: Path):
    bad = tmp_path / "q.yml"
    bad.write_text("queries:\n  - id: q1\n    text: t\n    split: dev\n    judgments: {a: 7}\n")
    with pytest.raises(ValueError):
        read_queries(bad)


def test_a_bad_split_is_refused(tmp_path: Path):
    bad = tmp_path / "q.yml"
    bad.write_text("queries:\n  - id: q1\n    text: t\n    split: train\n    judgments: {a: 2}\n")
    with pytest.raises(ValueError):
        read_queries(bad)


def test_a_duplicate_query_id_is_refused(tmp_path: Path):
    bad = tmp_path / "q.yml"
    bad.write_text(
        "queries:\n"
        "  - {id: q1, text: t, split: dev, judgments: {a: 2}}\n"
        "  - {id: q1, text: u, split: dev, judgments: {b: 2}}\n"
    )
    with pytest.raises(ValueError):
        read_queries(bad)


# -- search_all ---------------------------------------------------------------


def test_every_query_gets_a_ranking():
    qs = read_queries(SAMPLE).split("dev")
    rankings = search_all(qs, DOCS, fake_rank, k=5)
    assert set(rankings) == {q.id for q in qs}
    assert all(len(r) == 5 for r in rankings.values())


def test_the_rank_function_is_passed_in_not_imported():
    """So that week 3 can hand this the same thing with a different scorer."""
    qs = read_queries(SAMPLE).split("dev")
    called: list[str] = []

    def spy(query, documents, k=10):
        called.append(query)
        return []

    search_all(qs, DOCS, spy, k=3)
    assert len(called) == 8


# -- the audit ----------------------------------------------------------------


def test_unjudged_documents_in_the_top_k_are_found():
    """`fake_rank` returns mrta-001 through mrta-005 for everything. For q07 —
    `what does ROCC stand for` — the shipped set judged four documents, only one
    of which is among those five. The other four scored zero, silently."""
    qs = read_queries(SAMPLE).split("dev")
    rankings = search_all(qs, DOCS, fake_rank, k=5)
    unjudged = unjudged_in_top_k(rankings, qs, k=5)
    assert unjudged["q07"] == ["mrta-001", "mrta-002", "mrta-003", "mrta-004", "mrta-005"]


def test_queries_with_nothing_unjudged_are_left_out():
    qs = read_queries(SAMPLE).split("dev")
    perfect = {q.id: sorted(q.judgments) for q in qs}
    assert unjudged_in_top_k(perfect, qs, k=10) == {}


def test_the_audit_respects_k():
    qs = read_queries(SAMPLE).split("dev")
    rankings = search_all(qs, DOCS, fake_rank, k=5)
    assert len(unjudged_in_top_k(rankings, qs, k=2)["q07"]) <= 2


def test_rank_order_is_preserved_so_you_judge_the_top_one_first():
    qs = read_queries(SAMPLE).split("dev")
    rankings = {"q07": ["mrta-005", "mrta-001"]}
    assert unjudged_in_top_k(rankings, qs.split("dev"), k=10)["q07"] == [
        "mrta-005",
        "mrta-001",
    ]


# -- coverage -----------------------------------------------------------------


def test_coverage_counts_documents_judged_by_any_query():
    qs = read_queries(SAMPLE)
    coverage = judged_coverage(qs, set(CORPUS.ids))
    assert 0.0 < coverage < 1.0


def test_even_a_thorough_set_leaves_documents_nobody_has_ever_looked_at():
    """Twelve queries, forty-four judgments, thirty documents — 87% coverage,
    which sounds excellent and is an artefact of the corpus being tiny.

    Four documents have never been looked at by anyone. On this corpus that is a
    curiosity. Scale the same twelve queries to a corpus of a million and the
    number is 0.004%, and every claim you make rests on it. State your own
    coverage in the report and be uncomfortable about it."""
    qs = read_queries(SAMPLE)
    coverage = judged_coverage(qs, set(CORPUS.ids))
    assert coverage == pytest.approx(26 / 30)
    judged = {d for q in qs for d in q.judgments}
    assert sorted(set(CORPUS.ids) - judged) == [
        "mrta-011",
        "mrta-017",
        "mrta-019",
        "mrta-025",
    ]


def test_an_empty_corpus_is_zero_not_a_crash():
    assert judged_coverage(read_queries(SAMPLE), set()) == 0.0
