"""Day 4 — position, and a model we cannot check.

Every assertion about the stipulated model is about direction. None is about a
value. Read `test_the_numbers_here_are_not_measurements` last.
"""

from functools import cache

import pytest

import raglab
from dense import DenseRetriever
from fuse import rrf
from order import (
    answer_positions,
    assemble,
    attention_weight,
    ends_first,
    expected_use,
    order_by_document,
    order_by_rank,
)
from sections import section_corpus
from window import pack

CORPUS = raglab.corpus.load()
DOCS = {d.id: d.title + "\n" + d.text for d in CORPUS}


@cache
def dev():
    return [q for q in raglab.judgments.load(file="queries-extended.yml").split("dev") if q.answer_spans]


@cache
def setup():
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
    packed = {}
    for q in dev():
        shortlist = rrf([search(index, q.text, 60), retriever.search(q.text, 60)], 60, 10)
        packed[q.id] = pack(shortlist, chunks, 800)
    return chunks, packed


def mean_use(order_fn):
    chunks, packed = setup()
    return sum(
        expected_use(order_fn(packed[q.id][0]), chunks, q) for q in dev()
    ) / len(dev())


# -- the orderings ------------------------------------------------------------


def test_rank_order_is_the_identity():
    assert order_by_rank(["c", "a", "b"]) == ["c", "a", "b"]


def test_document_order_restores_reading_order():
    """Two consecutive sections of one RFC read as an argument. The same two
    interleaved with a third document read as three fragments."""
    assert order_by_document(["b#3", "a#10", "a#2"]) == ["a#2", "a#10", "b#3"]


def test_ends_first_puts_rank_one_first_and_rank_two_last():
    assert ends_first(["1", "2", "3", "4", "5"]) == ["1", "3", "5", "4", "2"]


def test_every_ordering_is_a_permutation():
    chunks, packed = setup()
    for q in dev():
        selected = packed[q.id][0]
        for fn in (order_by_rank, order_by_document, ends_first):
            assert sorted(fn(selected)) == sorted(selected)


# -- the stipulated model -----------------------------------------------------


def test_it_is_symmetric_and_dips_in_the_middle():
    weights = [attention_weight(i, 5) for i in range(5)]
    assert weights[0] == weights[-1] == 1.0
    assert weights[2] == min(weights)
    assert weights == weights[::-1]


def test_the_dip_parameter_controls_the_depth():
    shallow = attention_weight(2, 5, dip=0.9)
    deep = attention_weight(2, 5, dip=0.1)
    assert shallow > deep


def test_a_single_chunk_window_has_no_middle():
    assert attention_weight(0, 1) == 1.0


def test_bad_parameters_are_refused():
    with pytest.raises(ValueError):
        attention_weight(0, 0)
    with pytest.raises(ValueError):
        attention_weight(0, 5, dip=1.5)


# -- what is measured, as opposed to stipulated -------------------------------


def test_answer_positions_are_measured():
    """This one is real. On this corpus the first answer-bearing chunk sits
    roughly a third of the way into the window — which is the region the
    stipulated model penalises most, and is the reason the question is worth
    asking at all."""
    chunks, packed = setup()
    fractions = []
    for q in dev():
        order = order_by_rank(packed[q.id][0])
        hits = answer_positions(order, chunks, q)
        if hits and len(order) > 1:
            fractions.append(min(hits) / (len(order) - 1))
    assert fractions
    assert 0.2 < sum(fractions) / len(fractions) < 0.5


def test_a_window_with_no_answer_scores_zero():
    chunks, _ = setup()
    q = dev()[0]
    assert expected_use(["nothing"], {"nothing": "unrelated text"}, q) == 0.0


# -- and the discipline -------------------------------------------------------


def test_the_orderings_rank_in_this_direction():
    """Under the stipulated model: ends-first > rank > document.

    That ordering is what this comparison is for. It follows from the model's
    shape — ends-first puts the best results where the model says attention is
    highest, and document order ignores rank entirely — so it is closer to a
    consequence of the assumption than to a finding."""
    assert mean_use(ends_first) > mean_use(order_by_rank) > mean_use(order_by_document)


def test_the_numbers_here_are_not_measurements():
    """**The day.**

    `expected_use` returns something like 0.69 for ends-first and 0.67 for rank
    order. Those numbers are **meaningless**. They are a parabola we invented,
    evaluated at positions we measured, and the parabola's only justification is
    that the literature reports a U-shape for some models on some tasks.

    Change `dip` and every number changes while the ordering does not. That is
    the property that makes the comparison usable and the values not.

    So: report the **ordering** of strategies and the sensitivity of that
    ordering to `dip`. Never report the score. And in week 8, when there is a
    generator, measure it properly and find out whether any of today's ordering
    survives — which it may not."""
    orderings = []
    for dip in (0.2, 0.5, 0.8):
        chunks, packed = setup()
        scores = {
            name: sum(expected_use(fn(packed[q.id][0]), chunks, q, dip) for q in dev())
            for name, fn in (
                ("ends", ends_first),
                ("rank", order_by_rank),
                ("document", order_by_document),
            )
        }
        orderings.append(tuple(sorted(scores, key=lambda n: -scores[n])))
    assert len(set(orderings)) == 1


# -- assembly -----------------------------------------------------------------


def test_the_context_labels_every_chunk():
    """Week 8 asks the generator to cite, and it can only cite what it can name.
    A context of unlabelled prose makes attribution impossible for the model and
    unverifiable for you."""
    chunks, packed = setup()
    q = dev()[0]
    selected, texts = packed[q.id]
    context = assemble(order_by_rank(selected), texts)
    for chunk_id in selected:
        assert f"[{chunk_id}]" in context


def test_assembly_uses_the_packed_text_not_the_original():
    """Truncated chunks must appear truncated. Assembling from `chunks` instead
    of the packed texts silently blows the budget you spent yesterday
    computing."""
    order = ["a"]
    texts = {"a": "short"}
    assert assemble(order, texts) == "[a]\nshort"
    assert assemble(["a", "missing"], texts) == "[a]\nshort"
