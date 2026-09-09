"""Week 5 milestone — a frozen dense retriever, compared honestly."""

from functools import cache

import numpy as np
import pytest

import raglab
from dense import DenseRetriever, is_comparable, side_by_side
from sections import section_corpus

CORPUS = raglab.corpus.load()
DOCS = {d.id: d.title + "\n" + d.text for d in CORPUS}
DEV = [q for q in raglab.judgments.load().split("dev") if q.answer_spans]


@cache
def fitted():
    chunks = section_corpus(DOCS, 100, 300)
    return chunks, DenseRetriever(dims=192).fit(chunks)


@cache
def lexical_fn():
    import sys
    from pathlib import Path

    root = Path(__file__).resolve().parents[2]
    for day in ("day-3", "day-2", "day-1"):
        sys.path.insert(0, str(root / "week-03" / day))
    from bm25 import search

    from postings import Index

    chunks, _ = fitted()
    index = Index(chunks, stopwords=None)
    return lambda text, k: search(index, text, k)


# -- the retriever ------------------------------------------------------------


def test_it_fits_and_retrieves():
    chunks, retriever = fitted()
    assert retriever.search("how long may a crawler cache robots.txt", 5)
    assert retriever.search("kubernetes helm istio", 5) == []


def test_fit_chains():
    r = DenseRetriever(dims=32)
    assert r.fit({"a": "one two three"}) is r


def test_the_config_records_everything_that_changes_a_vector():
    """Two indexes built over different vocabularies are different spaces. A
    config that does not say so lets you compare them as if they were not."""
    _, retriever = fitted()
    config = retriever.config
    assert config["dims"] == 192
    assert config["n_vocab"] == 4273
    assert config["n_chunks"] == 266
    assert "chunker" in config


def test_dims_cannot_exceed_the_rank():
    small = DenseRetriever(dims=500).fit({"a": "one two", "b": "three four"})
    assert small.dims <= 2


# -- freezing -----------------------------------------------------------------


def test_freezing_produces_something_raglab_can_load(tmp_path):
    """The manifest is the point. Embeddings are a frozen artefact of a model at
    a version, and in six months a matrix with no manifest is a matrix you
    cannot compare with anything."""
    _, retriever = fitted()
    out = retriever.freeze(tmp_path / "s" / "vectors" / "documents")
    assert out.exists() and out.with_suffix(".json").exists()

    loaded = raglab.vectors.load("s", "documents", root=tmp_path)
    assert len(loaded) == 266
    assert loaded.dim == 192
    assert loaded.normalised is True
    assert loaded.ids == retriever.ids


def test_the_vectors_round_trip_exactly(tmp_path):
    _, retriever = fitted()
    retriever.freeze(tmp_path / "s" / "vectors" / "documents")
    loaded = raglab.vectors.load("s", "documents", root=tmp_path)
    assert np.allclose(loaded.matrix, retriever.D)
    assert np.allclose(np.linalg.norm(loaded.matrix, axis=1), 1.0)


def test_a_manifest_out_of_step_is_refused(tmp_path):
    """The check exists because the failure it catches is silent: every
    neighbour you compute is for the wrong document and nothing errors."""
    import json

    _, retriever = fitted()
    retriever.freeze(tmp_path / "s" / "vectors" / "documents")
    path = tmp_path / "s" / "vectors" / "documents.json"
    manifest = json.loads(path.read_text())
    manifest["ids"] = manifest["ids"][:-1]
    path.write_text(json.dumps(manifest))
    with pytest.raises(ValueError, match="out of step"):
        raglab.vectors.load("s", "documents", root=tmp_path)


# -- comparison ---------------------------------------------------------------


def test_the_comparison_is_reported_at_several_k():
    """Because the winner changes with it. A comparison at one k is a claim
    about that k, and reporting it as a claim about the systems is the most
    common error in this literature."""
    chunks, retriever = fitted()
    report = side_by_side(retriever, lexical_fn(), chunks, DEV, ks=(3, 5))
    assert set(report) == {3, 5}
    assert set(report[3]) == {"lexical", "dense", "oracle", "headroom", "tally"}


def test_and_it_shows_the_winner_flipping():
    chunks, retriever = fitted()
    report = side_by_side(retriever, lexical_fn(), chunks, DEV, ks=(3, 5))
    assert report[3]["dense"] > report[3]["lexical"]
    assert report[5]["lexical"] > report[5]["dense"]


def test_the_headroom_is_zero_and_that_is_the_finding():
    """Nine queries, and no complementarity visible at either k. Week 6 is about
    fusion; the case for it is not established here, and the milestone has to
    say so rather than assume it."""
    chunks, retriever = fitted()
    report = side_by_side(retriever, lexical_fn(), chunks, DEV, ks=(3, 5))
    assert report[3]["headroom"] == 0.0
    assert report[5]["headroom"] == 0.0


# -- comparability ------------------------------------------------------------


def test_two_indexes_over_different_chunkings_are_not_comparable():
    """The week's most expensive mistake, caught mechanically. A score
    difference between these is not attributable to anything you changed
    deliberately."""
    a = DenseRetriever(dims=64).fit(section_corpus(DOCS, 100, 300)).config
    b = DenseRetriever(dims=64).fit(section_corpus(DOCS, 60, 150)).config
    assert not is_comparable(a, b)


def test_the_same_corpus_at_different_dimensions_is_comparable():
    chunks = section_corpus(DOCS, 100, 300)
    a = DenseRetriever(dims=64).fit(chunks).config
    b = DenseRetriever(dims=192).fit(chunks).config
    assert is_comparable(a, b)
