"""Day 4 — approximate search.

The last two tests are the ones to carry out of the week.
"""

from functools import cache

import numpy as np
import pytest

import raglab
from ann import IVF, ann_recall, brute_force, build_ivf, kmeans, search_ivf
from lsa import decompose, embed_chunks, embed_query
from sections import section_corpus
from similarity import build_vocabulary, count_matrix, idf_weights, l2_normalise, query_vector, weight
from spans import answer_recall_at_k

CORPUS = raglab.corpus.load()
DOCS = {d.id: d.title + "\n" + d.text for d in CORPUS}
DEV = [q for q in raglab.judgments.load().split("dev") if q.answer_spans]
DIMS = 192


@cache
def space():
    chunks = section_corpus(DOCS, 100, 300)
    ids, vocab = build_vocabulary(chunks)
    X = count_matrix(chunks, ids, vocab)
    idf = idf_weights(X)
    U, S, Vt = decompose(l2_normalise(weight(X, idf)))
    return chunks, ids, vocab, idf, Vt, embed_chunks(U, S, DIMS)


@cache
def index16():
    _, ids, _, _, _, D = space()
    return build_ivf(D, ids, 16, 0)


def qvec(text: str):
    _, _, vocab, idf, Vt, _ = space()
    return embed_query(query_vector(text, vocab, idf), Vt, DIMS)


@cache
def sweep(nprobe: int):
    chunks, ids, _, _, _, D = space()
    ivf = index16()
    recalls, comparisons, answers = [], [], 0.0
    for q in DEV:
        v = qvec(q.text)
        exact = brute_force(D, ids, v, 5)
        approx = search_ivf(ivf, v, 5, nprobe)
        recalls.append(ann_recall(approx, exact))
        comparisons.append(ivf.comparisons)
        answers += answer_recall_at_k(approx, chunks, q, 5)
    return float(np.mean(recalls)), float(np.mean(comparisons)), answers / len(DEV)


# -- clustering ---------------------------------------------------------------


def test_clustering_is_identical_on_every_run():
    """An index that reshuffles between builds makes two runs of the same
    configuration disagree, and you will spend a day on it."""
    _, _, _, _, _, D = space()
    a, _ = kmeans(D, 8, seed=0)
    b, _ = kmeans(D, 8, seed=0)
    assert np.allclose(a, b)


def test_a_different_seed_gives_a_different_clustering():
    _, _, _, _, _, D = space()
    a, _ = kmeans(D, 8, seed=0)
    b, _ = kmeans(D, 8, seed=1)
    assert not np.allclose(a, b)


def test_centroids_stay_on_the_sphere():
    _, _, _, _, _, D = space()
    centroids, _ = kmeans(D, 8, seed=0)
    assert np.allclose(np.linalg.norm(centroids, axis=1), 1.0)


def test_every_row_lands_somewhere_and_every_list_exists():
    """A cluster that won no members still exists and still gets probed. A
    KeyError on a rare probe order is a delightful bug to find in production."""
    ivf = index16()
    assert ivf.n_lists == 16
    assert set(ivf.lists) == set(range(16))
    assert sum(len(v) for v in ivf.lists.values()) == len(ivf.ids)


def test_the_clusters_are_wildly_uneven():
    """From 2 members to 34. Real IVF indexes have this problem, it is why
    probing one list is unpredictable, and it is what more sophisticated
    structures are for."""
    sizes = sorted(len(v) for v in index16().lists.values())
    assert sizes[0] <= 3 and sizes[-1] >= 30


# -- searching ----------------------------------------------------------------


def test_probing_everything_is_exact():
    chunks, ids, _, _, _, D = space()
    v = qvec("how long may a crawler cache robots.txt")
    assert search_ivf(index16(), v, 5, nprobe=16) == brute_force(D, ids, v, 5)


def test_an_empty_query_returns_nothing():
    assert search_ivf(index16(), np.zeros(DIMS), 5, 4) == []


def test_nprobe_is_at_least_one():
    """A search that probes nothing returns nothing and looks like a broken index
    rather than a misconfigured one."""
    v = qvec("robots.txt")
    assert search_ivf(index16(), v, 5, nprobe=0) != []


# -- the trade ----------------------------------------------------------------


def test_more_probes_means_more_recall_and_more_work():
    """0.53 recall for 38 comparisons; 0.96 for 170. The knob does what it says
    and the curve is steep at the bottom, which is the useful part."""
    r1, c1, _ = sweep(1)
    r4, c4, _ = sweep(4)
    r8, c8, _ = sweep(8)
    assert r1 == pytest.approx(0.53, abs=0.06)
    assert r4 == pytest.approx(0.87, abs=0.06)
    assert r8 == pytest.approx(0.96, abs=0.04)
    assert c1 < c4 < c8


def test_ann_recall_is_agreement_with_brute_force_not_relevance():
    """It is a property of the *index* — did it find what an exhaustive scan
    would have found — and it says nothing about whether those vectors were the
    right answer. An index can have ANN recall 1.0 and retrieve nothing useful."""
    assert ann_recall(["a", "b"], ["a", "b"]) == 1.0
    assert ann_recall(["a", "z"], ["a", "b"]) == 0.5
    assert ann_recall([], []) == 1.0


# -- and the two things to carry out ------------------------------------------


def test_the_error_compounds_and_nobody_reports_it_that_way():
    """**The lesson.**

    At nprobe=1 the index has ANN recall **0.53** — it finds about half of what
    brute force would. That is a number a vector database would report, and on
    its own it sounds like a tuning detail.

    What the user experiences is **answer recall falling from 0.89 to 0.78**.
    One in nine queries where the answer was in the corpus, was in the top 5 of
    an exact search, and did not reach the context because of an index setting.

    Two different recalls. The index's is reported by the vendor; the user's is
    the one that matters; and they are multiplied together rather than chosen
    between. A 95%-recall index on top of a 90%-recall retriever is not 90%."""
    _, _, exact_answers = sweep(16)
    _, _, sloppy_answers = sweep(1)
    r1, _, _ = sweep(1)

    assert r1 < 0.6
    assert exact_answers == pytest.approx(0.889, abs=0.02)
    assert sloppy_answers == pytest.approx(0.778, abs=0.02)
    assert sloppy_answers < exact_answers


def test_at_this_size_the_index_is_slower_than_not_having_one():
    """266 vectors. Probing all 16 lists costs 282 comparisons — the 266 vectors
    **plus** 16 centroids — against brute force's 266.

    The approximate index is exact and slower. That is not a bug: an ANN
    structure is a bet that you have enough vectors for the saving to exceed the
    overhead, and at this scale you do not.

    Build it to know what the service does. Do not deploy it because it sounds
    sophisticated, and ask what a vendor's benchmark corpus size was."""
    _, comparisons, _ = sweep(16)
    _, ids, _, _, _, _ = space()
    assert comparisons > len(ids)
    assert comparisons == pytest.approx(len(ids) + 16, abs=1)
