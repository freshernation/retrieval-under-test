"""Day 3 — comparing two retrievers.

`test_the_winner_depends_on_k` is the day.
"""

from functools import cache

import pytest

import raglab
from compare import (
    A_ONLY,
    B_ONLY,
    BOTH,
    NEITHER,
    by_family,
    head_to_head,
    headroom,
    oracle_recall,
    recall_of,
    tally,
    winner_flips,
)
from lsa import decompose, embed_chunks, embed_query, neighbours
from sections import section_corpus
from similarity import build_vocabulary, count_matrix, idf_weights, l2_normalise, query_vector, weight

CORPUS = raglab.corpus.load()
DOCS = {d.id: d.title + "\n" + d.text for d in CORPUS}
DEV = [q for q in raglab.judgments.load().split("dev") if q.answer_spans]
DIMS = 192


@cache
def systems():
    import sys
    from pathlib import Path

    root = Path(__file__).resolve().parents[2]
    for day in ("day-3", "day-2", "day-1"):
        sys.path.insert(0, str(root / "week-03" / day))
    from bm25 import search

    from postings import Index

    chunks = section_corpus(DOCS, 100, 300)
    ids, vocab = build_vocabulary(chunks)
    X = count_matrix(chunks, ids, vocab)
    idf = idf_weights(X)
    U, S, Vt = decompose(l2_normalise(weight(X, idf)))
    D = embed_chunks(U, S, DIMS)
    index = Index(chunks, stopwords=None)

    def lexical(text, k):
        return search(index, text, k)

    def dense(text, k):
        return neighbours(D, ids, embed_query(query_vector(text, vocab, idf), Vt, DIMS), k)

    return chunks, lexical, dense


@cache
def table_at(k: int):
    chunks, lexical, dense = systems()
    return head_to_head(
        {q.id: lexical(q.text, k) for q in DEV},
        {q.id: dense(q.text, k) for q in DEV},
        chunks,
        DEV,
        k,
    )


# -- the table ----------------------------------------------------------------


def test_every_answerable_query_gets_a_verdict():
    table = table_at(5)
    assert set(table) == {q.id for q in DEV}
    assert set(table.values()) <= {BOTH, A_ONLY, B_ONLY, NEITHER}


def test_unanswerable_queries_are_skipped():
    chunks, lexical, dense = systems()
    everything = raglab.judgments.load().split("dev")
    table = head_to_head({}, {}, chunks, everything, 5)
    assert "r10" not in table


def test_the_tally_includes_its_zeros():
    """`"b only": 0` is a finding. A dict that omits it makes the reader do the
    subtraction, and readers do not."""
    counts = tally(table_at(5))
    assert set(counts) == {BOTH, A_ONLY, B_ONLY, NEITHER}
    assert counts[B_ONLY] == 0


def test_recall_is_recoverable_from_the_table():
    table = table_at(5)
    assert recall_of(table, "a") == pytest.approx(1.0)
    assert recall_of(table, "b") == pytest.approx(0.889, abs=0.02)


# -- the ceiling --------------------------------------------------------------


def test_the_oracle_is_what_fusion_could_reach():
    """Every query either system gets. If it equals the better system, the two
    are redundant and no amount of clever combining helps — which is exactly
    what the next test finds."""
    assert oracle_recall(table_at(3)) == pytest.approx(0.889, abs=0.02)
    assert oracle_recall(table_at(5)) == pytest.approx(1.0)
    assert tally(table_at(3))[A_ONLY] == 0
    assert tally(table_at(3))[B_ONLY] == 1


def test_there_is_no_headroom_at_all_on_nine_queries():
    """**Not the result anyone wants, and it is the honest one.**

    At k=3 the oracle is 0.89 and dense alone is 0.89 — dense gets every query
    lexical gets, plus one. At k=5 the oracle is 1.00 and lexical alone is 1.00.

    Headroom is **zero at both**. On this split, the two systems are redundant:
    whichever is ahead already contains the other, and no fusion however clever
    can add anything.

    Week 6 is about fusion. The case for it is not established here, and the
    reason is not that fusion does not work — it is that nine queries cannot
    show complementarity that involves one or two queries in each direction.
    Your week-3 milestone asked you to grow the eval set to thirty. This is what
    it was for, and week 6 will not be measurable without it."""
    assert headroom(table_at(3)) == 0.0
    assert headroom(table_at(5)) == 0.0
    assert oracle_recall(table_at(3)) == pytest.approx(recall_of(table_at(3), "b"))
    assert oracle_recall(table_at(5)) == pytest.approx(recall_of(table_at(5), "a"))


def test_zero_headroom_means_redundant():
    assert headroom({"q1": BOTH, "q2": A_ONLY}) == 0.0
    assert headroom({"q1": A_ONLY, "q2": B_ONLY}) == 0.5


# -- families -----------------------------------------------------------------


def test_the_family_table_reports_n_and_n_is_embarrassing():
    """Most families have one or two queries on this split. The table is
    suggestive and it is not evidence, and reporting `n` is what stops everyone
    forgetting that."""
    families = by_family(table_at(3), DEV)
    assert all("n" in row for row in families.values())
    assert max(row["n"] for row in families.values()) <= 2


def test_the_families_disagree_even_so():
    """On `superseded` queries dense gets both and lexical gets one. On
    `vocabulary-gap` they tie at half — which is the family dense was supposed to
    win, and it does not.

    Two queries each. Do not build anything on this. Do notice that the two
    systems are not the same system with different accuracy."""
    families = by_family(table_at(3), DEV)
    assert families["superseded"]["b"] > families["superseded"]["a"]
    assert families["vocabulary-gap"]["a"] == families["vocabulary-gap"]["b"]


# -- and the day --------------------------------------------------------------


def test_the_winner_depends_on_k():
    """**The day.**

    At k=3 dense scores 0.89 and lexical 0.78. At k=5 lexical scores 1.00 and
    dense 0.89.

    Same two systems, same corpus, same queries, opposite conclusions —
    separated by a parameter that is a property of neither of them.

    You do not have a better retriever. You have two retrievers and a knob, and
    any sentence of the form "dense beats BM25" is incomplete without the k it
    was measured at, the corpus it was measured on, and the n it was measured
    over. Almost every such sentence you will read omits all three."""
    tables = {k: table_at(k) for k in (3, 5)}
    assert recall_of(tables[3], "b") > recall_of(tables[3], "a")
    assert recall_of(tables[5], "a") > recall_of(tables[5], "b")
    assert winner_flips(tables)


def test_and_nine_queries_cannot_settle_it():
    """Week 3's floor arithmetic, still binding. One query is eleven points of
    the mean, and both differences above are exactly one query.

    The honest output of today is not a winner. It is a table showing where they
    disagree, a ceiling saying what combining them could reach, and a number
    saying how little either claim is worth."""
    assert len(DEV) == 9
    assert abs(recall_of(table_at(3), "a") - recall_of(table_at(3), "b")) == pytest.approx(
        1 / 9, abs=0.01
    )
