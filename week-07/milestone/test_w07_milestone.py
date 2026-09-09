"""Week 7 milestone — the context assembler."""

from functools import cache

import pytest

import raglab
from context import ContextAssembler, compare, regressions
from dense import DenseRetriever
from fuse import rrf
from sections import section_corpus

CORPUS = raglab.corpus.load()
DOCS = {d.id: d.title + "\n" + d.text for d in CORPUS}


@cache
def dev():
    return [q for q in raglab.judgments.load(file="queries-extended.yml").split("dev") if q.answer_spans]


@cache
def parts():
    import sys
    from pathlib import Path

    root = Path(__file__).resolve().parents[2]
    for day in ("day-3", "day-2", "day-1"):
        sys.path.insert(0, str(root / "week-03" / day))
    from bm25 import search

    from postings import Index

    chunks = section_corpus(DOCS, 100, 300)
    index = Index(chunks, stopwords=None)
    retriever = DenseRetriever(dims=192).fit(chunks)

    def retrieve(text, depth):
        return rrf([search(index, text, 60), retriever.search(text, 60)], depth, 10)

    return chunks, retrieve


def make(**kwargs):
    chunks, retrieve = parts()
    return ContextAssembler(retrieve, chunks, **kwargs)


# -- the assembler ------------------------------------------------------------


def test_every_stage_is_off_by_default():
    """A pipeline whose stages default to on is a pipeline nobody measured."""
    config = make().config
    assert config["rerank_alpha"] is None
    assert config["mmr_lambda"] is None
    assert config["dedupe_threshold"] is None
    assert config["order"] == "rank"


def test_the_config_distinguishes_two_assemblers():
    from raglab.runs import config_hash

    assert config_hash(make().config) != config_hash(make(budget=400).config)
    assert config_hash(make().config) != config_hash(make(order="ends").config)


def test_an_unknown_ordering_is_refused():
    with pytest.raises(ValueError):
        make(order="semantic")


def test_it_builds_something_a_generator_could_receive():
    built = make().build(dev()[0])
    assert isinstance(built["text"], str) and built["text"]
    assert built["words"] <= 800
    for chunk_id in built["chunks"]:
        assert f"[{chunk_id}]" in built["text"]


def test_the_budget_is_respected_with_and_without_truncation():
    for truncate in (False, True):
        for q in dev():
            assert make(budget=500, truncate=truncate).build(q)["words"] <= 500


def test_ordering_changes_the_window_not_its_contents():
    q = dev()[0]
    a = make(order="rank").build(q)
    b = make(order="ends").build(q)
    assert sorted(a["chunks"]) == sorted(b["chunks"])
    assert a["chunks"] != b["chunks"] or len(a["chunks"]) < 3


def test_build_reports_what_production_cannot_compute():
    """`answered` and `density` need the query's answer spans, which do not
    exist at serving time. These are evaluation-time numbers and the report must
    say so rather than implying the pipeline monitors itself."""
    q = dev()[0]
    built = make().build(q)
    assert set(built) == {"text", "chunks", "words", "answered", "density", "positions"}
    assert q.answer_spans


# -- comparing configurations -------------------------------------------------


def test_compare_reports_all_three_numbers():
    """A configuration answering as often for fewer words is strictly better;
    one answering more often for more words is a point on a frontier."""
    table = compare({"default": make(), "small": make(budget=400)}, dev()[:6])
    assert set(table["default"]) == {"answered", "density", "words"}
    assert table["small"]["words"] < table["default"]["words"]


def test_the_defaults_beat_the_full_pipeline():
    """**The milestone.**

    Turn on reranking, deduplication and MMR — every technique this week taught
    — and the assembled context answers **no more often** than the plain one,
    for the same budget.

    Two of the three stages were measured this week and found to cost more than
    they bought on this corpus. Building them was worth it; switching them on
    would not be."""
    plain = make()
    everything = make(rerank_alpha=0.5, mmr_lambda=0.5, dedupe_threshold=0.8)
    table = compare({"plain": plain, "everything": everything}, dev())
    assert table["everything"]["answered"] <= table["plain"]["answered"]


def test_regressions_name_the_queries():
    """Week 6's rule, one stage later: a change that raises the mean while
    breaking a query is a trade, and a trade needs naming."""
    plain = make()
    aggressive = make(mmr_lambda=0.2, budget=400)
    lost = regressions(None, None, dev(), plain, aggressive)
    assert isinstance(lost, list)
    assert all(isinstance(q, str) for q in lost)
    assert lost == sorted(lost)


def test_a_smaller_budget_costs_answers():
    table = compare({"800": make(), "300": make(budget=300)}, dev())
    assert table["300"]["answered"] < table["800"]["answered"]
    assert table["300"]["density"] > table["800"]["density"]
