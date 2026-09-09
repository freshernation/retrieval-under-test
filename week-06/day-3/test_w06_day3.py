"""Day 3 — the verdict.

`test_the_family_that_nothing_reaches` is the week's real finding.
"""

from functools import cache

import pytest

import raglab
from dense import DenseRetriever
from fuse import rrf
from sections import section_corpus
from verdict import by_family, oracle, recall, unreachable, verdict

CORPUS = raglab.corpus.load()
DOCS = {d.id: d.title + "\n" + d.text for d in CORPUS}


@cache
def dev():
    return [q for q in raglab.judgments.load(file="queries-extended.yml").split("dev") if q.answer_spans]


@cache
def runs():
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
    inputs = {
        "lexical": {q.id: search(index, q.text, 50) for q in dev()},
        "dense": {q.id: retriever.search(q.text, 50) for q in dev()},
    }
    return chunks, inputs


def fused_at(k: int, c: float):
    _, inputs = runs()
    return {
        q.id: rrf([inputs["lexical"][q.id], inputs["dense"][q.id]], k, c) for q in dev()
    }


# -- the pieces ---------------------------------------------------------------


def test_oracle_takes_any_number_of_inputs():
    """There is no reason to stop at two retrievers and the arithmetic does not
    care."""
    chunks, inputs = runs()
    two = oracle(inputs, chunks, dev(), 3)
    one = oracle({"lexical": inputs["lexical"]}, chunks, dev(), 3)
    assert two >= one


def test_the_verdict_has_the_field_that_decides():
    chunks, inputs = runs()
    v = verdict(fused_at(3, 60), inputs, chunks, dev(), 3)
    assert set(v) == {
        "k",
        "fused",
        "inputs",
        "best_input",
        "beats_all",
        "dilution",
        "oracle",
        "captured",
    }


def test_captured_is_none_when_there_was_nothing_to_capture():
    """A percentage of no headroom is not a number."""
    chunks, inputs = runs()
    same = {"a": inputs["lexical"], "b": inputs["lexical"]}
    v = verdict(inputs["lexical"], same, chunks, dev(), 5)
    assert v["oracle"] == v["inputs"]["a"]
    assert v["captured"] is None


# -- the three verdicts -------------------------------------------------------


def test_at_three_it_beats_everything_and_takes_all_the_headroom():
    chunks, inputs = runs()
    v = verdict(fused_at(3, 60), inputs, chunks, dev(), 3)
    assert v["beats_all"] is True
    assert v["dilution"] == 0.0
    assert v["captured"] == pytest.approx(1.0)


def test_at_five_it_loses_to_its_own_input():
    """**The failure the whole day exists to catch.**

    Fused 0.737, lexical 0.789. `beats_all` is False and `dilution` is 0.053.

    Compare against dense retrieval alone — 0.737 — and fusion looks like a tie.
    Compare against the weaker input on a different k and you can report an
    improvement. Neither is a lie and both are wrong."""
    chunks, inputs = runs()
    v = verdict(fused_at(5, 60), inputs, chunks, dev(), 5)
    assert v["best_input"] == "lexical"
    assert v["beats_all"] is False
    assert v["dilution"] == pytest.approx(0.053, abs=0.005)
    assert v["fused"] >= v["inputs"]["dense"]


def test_at_ten_the_constant_decides():
    """c=10 captures all of the headroom; c=60 — the default everywhere —
    captures none of it and merely ties the better input."""
    chunks, inputs = runs()
    good = verdict(fused_at(10, 10), inputs, chunks, dev(), 10)
    default = verdict(fused_at(10, 60), inputs, chunks, dev(), 10)
    assert good["beats_all"] and good["captured"] == pytest.approx(1.0)
    assert not default["beats_all"] and default["captured"] == 0.0


# -- where it helps and where it cannot ---------------------------------------


def test_fusion_genuinely_wins_a_family():
    """vocabulary-gap at k=10: lexical 0.75, dense 0.75, **fused 1.00**. Two
    retrievers each missing a different query, and the fusion getting both.

    This is complementarity doing exactly what it is supposed to, and it is
    invisible in a mean that moved five points."""
    chunks, inputs = runs()
    table = by_family(fused_at(10, 10), inputs, chunks, dev(), 10)
    gap = table["vocabulary-gap"]
    assert gap["n"] == 4
    assert gap["lexical"] == pytest.approx(0.75)
    assert gap["dense"] == pytest.approx(0.75)
    assert gap["fused"] == pytest.approx(1.0)


def test_the_family_that_nothing_reaches():
    """**The week's real finding.**

    `paraphrase`: lexical 0.33, dense 0.33, fused 0.33 — at k=3, k=5 and k=10,
    at every constant, under every weighting.

    Two of three paraphrase queries are retrieved by **nothing**. The answers are
    in the corpus. No fusion can help, by construction: the oracle already
    excludes them, so every point of headroom you chase is a point that is not
    here.

    Fusion combines what your retrievers found. It cannot conjure what neither
    of them did, and a week spent tuning `c` is a week not spent on the family
    that is actually failing."""
    chunks, inputs = runs()
    for k, c in ((3, 60), (5, 60), (10, 10)):
        table = by_family(fused_at(k, c), inputs, chunks, dev(), k)
        row = table["paraphrase"]
        assert row["n"] == 3
        assert row["lexical"] == row["dense"] == row["fused"]
        assert row["fused"] == pytest.approx(1 / 3, abs=0.001)


def test_and_it_names_the_queries():
    """`r19` — "how do I stop search engines indexing my site" — and `r20` —
    "what part of a web address comes after the hash".

    Neither shares meaningful vocabulary with its answer. The corpus says
    "crawlers" and "access", not "search engines" and "indexing"; it says
    "fragment identifier", not "hash".

    This is the vocabulary gap that week 5 promised dense retrieval would close,
    at the point where it does not. The fix is not a better retriever. It is
    changing the query, and that is week 11."""
    chunks, inputs = runs()
    missing = unreachable(inputs, chunks, dev(), 10)
    assert missing == ["r19", "r20"]
    families = {q.id: q.family for q in dev()}
    assert all(families[q] == "paraphrase" for q in missing)
