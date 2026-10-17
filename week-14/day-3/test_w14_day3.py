"""Day 3 — a graph index, and the size at which it is worth it.

`test_on_this_corpus_the_graph_reads_nine_tenths_of_it` is the day.
"""

from functools import cache

import numpy as np

import raglab
from dense import DenseRetriever
from hnsw import HNSW, brute_force, build, recall
from sections import section_corpus
from semcache import embedder

CORPUS = raglab.corpus.load()
DOCS = {d.id: d.title + "\n" + d.text for d in CORPUS}


@cache
def dense():
    return DenseRetriever(dims=192).fit(section_corpus(DOCS, 100, 300))


@cache
def vectors():
    D = dense().D
    return D / np.linalg.norm(D, axis=1, keepdims=True)


@cache
def queries():
    j = raglab.judgments.load(file="queries-extended.yml")
    e = embedder(dense())
    return [e(q.text) for q in list(j.split("dev")) + list(j.split("test"))]


@cache
def graph(M):
    return build(dense().ids, vectors(), M=M, ef_construction=64)


def measured(g, ids, D, Q, ef):
    g.distances = 0
    recalls = [recall(g.search(q, 10, ef), brute_force(ids, D, q, 10)) for q in Q]
    return round(sum(recalls) / len(recalls), 3), round(g.distances / len(Q), 1)


def test_recall_and_brute_force():
    assert recall(["a", "b"], ["b", "c"]) == 0.5 and recall([], []) == 1.0
    D = np.eye(3)
    assert brute_force(["x", "y", "z"], D, np.array([0.0, 1.0, 0.0]), 2) == ["y", "x"]


def test_levels_thin_out():
    sizes = [len(layer) for layer in graph(8).layers]
    assert sizes[0] == 266 and all(a > b for a, b in zip(sizes, sizes[1:]))


def test_every_distance_is_counted():
    g = HNSW(M=4)
    g.add("a", np.array([1.0, 0.0]))
    g.distances = 0
    g.distance(np.array([1.0, 0.0]), 0)
    assert g.distances == 1


def test_wider_search_finds_more():
    found = [measured(graph(8), dense().ids, vectors(), queries(), ef)[0] for ef in (10, 32, 64, 128)]
    assert found == [0.754, 0.888, 0.992, 1.0]


def test_on_this_corpus_the_graph_reads_nine_tenths_of_it():
    """To match brute force at 0.99 recall@10, the graph computes 241 distances per
    query - 91% of the 266 a brute-force scan computes. Asked for perfect recall, it
    computes more than the scan."""
    assert measured(graph(8), dense().ids, vectors(), queries(), 64) == (0.992, 241.0)
    assert measured(graph(8), dense().ids, vectors(), queries(), 128) == (1.0, 274.3)


def test_at_two_thousand_vectors_it_reads_a_third():
    rng = np.random.default_rng(0)
    D = rng.normal(size=(2000, 32))
    D /= np.linalg.norm(D, axis=1, keepdims=True)
    Q = rng.normal(size=(50, 32))
    Q /= np.linalg.norm(Q, axis=1, keepdims=True)
    ids = [str(i) for i in range(2000)]
    g = build(ids, D, M=16, ef_construction=64)
    assert measured(g, ids, D, list(Q), 32) == (0.978, 689.5), (
        "At 2,000 vectors the same graph reaches 0.978 reading about a third of them."
    )
