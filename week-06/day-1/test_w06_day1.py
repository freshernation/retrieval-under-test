"""Day 1 — the eval set grows, and the obvious fusion fails.

`test_adding_the_scores_is_just_bm25` is the day.
"""

from functools import cache

import pytest

import raglab
from dense import DenseRetriever
from normalise import combine, min_max, ranked, top_gap, z_score
from sections import section_corpus
from spans import answer_recall_at_k

CORPUS = raglab.corpus.load()
DOCS = {d.id: d.title + "\n" + d.text for d in CORPUS}


@cache
def dev():
    qs = raglab.judgments.load(file="queries-extended.yml").split("dev")
    return [q for q in qs if q.answer_spans]


@cache
def systems():
    import sys
    from pathlib import Path

    root = Path(__file__).resolve().parents[2]
    for day in ("day-3", "day-2", "day-1"):
        sys.path.insert(0, str(root / "week-03" / day))
    from bm25 import score, search

    from postings import Index

    chunks = section_corpus(DOCS, 100, 300)
    index = Index(chunks, stopwords=None)
    retriever = DenseRetriever(dims=192).fit(chunks)

    def lexical(text, depth=50):
        return {c: score(index, text, c) for c in search(index, text, depth)}

    def dense(text, depth=50):
        return _cosine_scores(retriever, text, depth)

    return chunks, lexical, dense


def _cosine_scores(retriever, text, depth):
    from lsa import embed_query
    from similarity import query_vector

    q = embed_query(query_vector(text, retriever.vocab, retriever.idf), retriever.Vt, retriever.dims)
    scores = retriever.D @ q
    order = sorted(range(len(scores)), key=lambda i: -scores[i])[:depth]
    return {retriever.ids[i]: float(scores[i]) for i in order}


def measure(rank_fn, k):
    chunks, _, _ = systems()
    return sum(answer_recall_at_k(rank_fn(q.text, k), chunks, q, k) for q in dev()) / len(dev())


# -- the instrument -----------------------------------------------------------


def test_the_extended_set_is_bigger_and_the_old_one_is_untouched():
    """An eval set that grows is a new instrument, not a corrected one. Numbers
    taken with the two are not comparable, and keeping both files is what makes
    that visible instead of silent."""
    old = raglab.judgments.load()
    new = raglab.judgments.load(file="queries-extended.yml")
    assert len(old) == 16 and len(new) == 26
    assert {q.id for q in old} < {q.id for q in new}
    assert len(old.split("test")) == len(new.split("test")) == 6


def test_nineteen_answerable_dev_queries():
    assert len(dev()) == 19


def test_the_new_queries_are_the_shapes_that_separate_the_two_retrievers():
    new = {q.id: q.family for q in raglab.judgments.load(file="queries-extended.yml")}
    added = {q: f for q, f in new.items() if q >= "r17"}
    assert added["r17"] == "identifier"
    assert added["r19"] == "paraphrase"
    assert added["r21"] == "vocabulary-gap"


# -- normalisation ------------------------------------------------------------


def test_min_max_rescales():
    assert min_max({"a": 10.0, "b": 5.0, "c": 0.0}) == {"a": 1.0, "b": 0.5, "c": 0.0}


def test_a_single_result_is_not_ranked_last():
    """Returning 0.0 for a constant set would silently rank a sole exact match
    bottom."""
    assert min_max({"a": 7.0}) == {"a": 1.0}
    assert min_max({"a": 3.0, "b": 3.0}) == {"a": 1.0, "b": 1.0}


def test_z_score_is_centred():
    out = z_score({"a": 1.0, "b": 2.0, "c": 3.0})
    assert out["b"] == pytest.approx(0.0)
    assert out["a"] == -out["c"]


def test_a_constant_set_has_no_shape():
    assert z_score({"a": 5.0, "b": 5.0}) == {"a": 0.0, "b": 0.0}
    assert z_score({}) == {}


def test_combine_treats_missing_as_zero_and_that_is_an_assumption():
    """Absent from the top 50 is not "scored zero", it is "not measured". After
    min-max, 0.0 is the *worst* result rather than no result, so a chunk one
    retriever never saw is actively penalised."""
    out = combine({"a": 1.0}, {"b": 1.0})
    assert out == {"a": 0.5, "b": 0.5}


def test_a_bad_weight_is_refused():
    with pytest.raises(ValueError):
        combine({}, {}, weight=1.5)


# -- the confidence signal min-max destroys -----------------------------------


def test_top_gap_measures_separation():
    assert top_gap({"a": 10.0, "b": 5.0}) == pytest.approx(0.5)
    assert top_gap({"a": 10.0, "b": 9.9}) == pytest.approx(0.01)
    assert top_gap({"a": 1.0}) == 0.0


def test_min_max_makes_a_confident_and_a_hopeless_query_identical():
    """`r01` retrieves with a top score of 24.7 and a 14% gap to the runner-up.
    `r19` retrieves with a top score of 16.3 and a 2% gap — it could barely
    separate its candidates.

    After min-max both have a top score of exactly 1.0. The information that one
    retriever was confident and the other was guessing is gone, and it is
    precisely the information a fusion rule would want."""
    _, lexical, _ = systems()
    strong = lexical("what status code should I return when a client sends too many requests", 5)
    weak = lexical("how do I stop search engines indexing my site", 5)

    assert top_gap(strong) > 5 * top_gap(weak)
    assert max(min_max(strong).values()) == max(min_max(weak).values()) == 1.0


# -- and the day --------------------------------------------------------------


def test_the_two_score_scales_are_not_comparable():
    """BM25 is unbounded and query-dependent — 3.2 to 33.2 across this dev split.
    Cosine is bounded in [-1, 1] and in practice sits between 0.2 and 0.8.

    They are not the same kind of number. One is a sum of per-term evidence; the
    other is an angle."""
    _, lexical, dense = systems()
    lex_all = [v for q in dev() for v in lexical(q.text, 10).values()]
    dense_all = [v for q in dev() for v in dense(q.text, 10).values()]
    assert max(lex_all) > 30 and min(lex_all) < 4
    assert max(dense_all) <= 1.0


def test_adding_the_scores_is_just_bm25():
    """**The day.**

    Sum the raw scores and the fused ranking is **identical to lexical alone at
    every k** — 0.684, 0.789, 0.842. Not similar: identical.

    BM25's scale swamps cosine's entirely, so "combining" the two is a very
    elaborate way of using one of them. It runs, it produces a ranking, it looks
    like a hybrid retriever, and it has no dense component in it whatsoever.

    Nothing errors. This is the most common hybrid-retrieval bug there is."""
    _, lexical, dense = systems()

    def summed(text, k):
        return ranked(combine(lexical(text), dense(text)), k)

    def lex_only(text, k):
        return ranked(lexical(text), k)

    for k in (3, 5, 10):
        assert measure(summed, k) == measure(lex_only, k)


def test_and_normalising_first_does_not_reliably_help_either():
    """min-max fusion is *worse* than lexical alone at k=5 and better at k=10.
    Two adjacent values of k, opposite verdicts, on nineteen queries.

    Score normalisation is not the answer. Tomorrow's is a method that never
    looks at a score at all."""
    _, lexical, dense = systems()

    def mm(text, k):
        return ranked(combine(min_max(lexical(text)), min_max(dense(text))), k)

    def lex_only(text, k):
        return ranked(lexical(text), k)

    assert measure(mm, 5) < measure(lex_only, 5)
    assert measure(mm, 10) > measure(lex_only, 10)
