"""Week 2 milestone — the ingest, and the report that says what it lost."""

import sys
from functools import cache
from pathlib import Path

import pytest

import raglab
from ingest import coverage_gaps, ingest, manifest, search

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "week-01" / "day-4"))
from overlap import rank  # noqa: E402

CORPUS = raglab.corpus.load()
RAW = {d.id: d.text for d in CORPUS}


@cache
def rows() -> dict[str, dict]:
    """Lazy, so an unwritten `manifest` fails these tests individually rather
    than stopping the week from collecting."""
    return manifest(RAW)


def test_every_document_is_ingested():
    out = ingest(RAW)
    assert set(out) == set(RAW)
    assert all(len(v) < len(RAW[k]) for k, v in out.items())


def test_the_manifest_covers_every_document_with_every_field():
    assert set(rows()) == set(RAW)
    assert set(rows()["rfc-7725"]) == {
        "chars_before",
        "chars_after",
        "pct_removed",
        "furniture",
        "split_paragraphs",
        "superseded_by",
        "near_duplicate_of",
    }


def test_absent_facts_are_none_rather_than_missing():
    """A consumer that has to use `.get()` will eventually stop checking."""
    assert rows()["rfc-7725"]["superseded_by"] is None
    assert rows()["rfc-7725"]["near_duplicate_of"] is None


def test_the_manifest_knows_what_is_stale():
    assert rows()["rfc-7159"]["superseded_by"] == "rfc-8259"
    assert rows()["rfc-5785"]["superseded_by"] == "rfc-8615"
    assert rows()["rfc-8259"]["superseded_by"] is None


def test_the_manifest_knows_what_is_duplicated():
    assert rows()["rfc-7159"]["near_duplicate_of"] == "rfc-8259"
    assert rows()["rfc-8259"]["near_duplicate_of"] == "rfc-7159"


def test_the_well_known_pair_is_not_flagged_as_duplicate_at_this_threshold():
    """0.185, well under 0.5. Same relationship as the JSON pair, and similarity
    cannot see it — which is why `superseded_by` is a separate column and not
    derived from `near_duplicate_of`."""
    assert rows()["rfc-5785"]["near_duplicate_of"] is None
    assert rows()["rfc-5785"]["superseded_by"] == "rfc-8615"


def test_per_document_not_a_total():
    """The corpus total would say "27% removed" and hide the whole finding."""
    assert rows()["rfc-7725"]["pct_removed"] == pytest.approx(39.1, abs=0.2)
    assert rows()["rfc-3986"]["pct_removed"] == pytest.approx(18.3, abs=0.2)


# -- search -------------------------------------------------------------------


def test_search_demotes_and_annotates():
    index = ingest(RAW)
    from lineage import supersession

    graph = supersession(RAW)
    results = search("must JSON be encoded in UTF-8", index, graph, rank, k=5)
    assert results[0] == ("rfc-8259", None)
    assert ("rfc-7159", "rfc-8259") in results


def test_the_annotation_travels_with_the_result():
    """A caller who has to remember to look up staleness will not, and the
    failure is silent and confident."""
    index = ingest(RAW)
    from lineage import supersession

    for doc_id, stale in search("JSON", index, supersession(RAW), rank, k=10):
        assert stale is None or isinstance(stale, str)


# -- the report ---------------------------------------------------------------


def test_the_gaps_are_generated_from_the_data():
    """Prose written by hand was true in March. Prose generated from the manifest
    is true now."""
    gaps = coverage_gaps(rows())
    assert any("superseded by rfc-8259" in g for g in gaps)
    assert any("rfc-7725" in g and "boilerplate" in g for g in gaps)
    assert any("rfc-3986" in g and "cut by a page boundary" in g for g in gaps)
    assert gaps == sorted(gaps)


def test_a_clean_corpus_reports_nothing():
    quiet = {
        "a": {
            "chars_before": 100,
            "chars_after": 95,
            "pct_removed": 5.0,
            "furniture": 0,
            "split_paragraphs": 0,
            "superseded_by": None,
            "near_duplicate_of": None,
        }
    }
    assert coverage_gaps(quiet) == []
