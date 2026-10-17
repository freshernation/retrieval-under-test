"""Day 2 — a cache that answers similar questions.

`test_section_three_point_two_is_served_the_answer_to_three_point_four` is the day.
"""

from functools import cache

import raglab
from dense import DenseRetriever
from sections import section_corpus
from semcache import SemanticCache, embedder, identifiers, sweep

CORPUS = raglab.corpus.load()
DOCS = {d.id: d.title + "\n" + d.text for d in CORPUS}

# The same question, asked another way. A cache should answer the second from the first.
PARAPHRASES = [
    ("what status code should I return when a client sends too many requests",
     "which status code tells a client it sent too many requests"),
    ("how do I tell a client to slow down", "how can a server ask a client to slow down"),
    ("what does the 418 status code mean", "what is the meaning of status code 418"),
    ("must JSON be encoded in UTF-8", "does JSON have to be encoded as UTF-8"),
    ("what does ABNF stand for", "what is ABNF short for"),
    ("how do cookies expire", "when does a cookie expire"),
    ("what is a well-known URI", "what are well-known URIs for"),
    ("how does robots.txt work", "how do robots.txt files work"),
    ("what characters are allowed in a URI", "which characters may appear in a URI"),
    ("can a cookie be shared across subdomains", "are cookies shared between subdomains"),
]
# A different question that looks the same. A cache must never answer the second from the first.
NEAR_MISSES = [
    ("what does the 418 status code mean", "what does the 451 status code mean"),
    ("what does the 429 status code mean", "what does the 451 status code mean"),
    ("what does RFC 7159 say about duplicate names", "what does RFC 8259 say about duplicate names"),
    ("what does the 428 status code mean", "what does the 431 status code mean"),
    ("is 418 a real status code", "is 451 a real status code"),
    ("what changed in RFC 8615", "what changed in RFC 5785"),
    ("what does section 3.2 of RFC 3986 define", "what does section 3.4 of RFC 3986 define"),
    ("what does the 511 status code mean", "what does the 429 status code mean"),
    ("cookies in RFC 6265", "cookies in RFC 2965"),
    ("what is the max-age attribute", "what is the expires attribute"),
]
THRESHOLDS = (0.8, 0.9, 0.95, 0.98)


@cache
def embed():
    return embedder(DenseRetriever(dims=192).fit(section_corpus(DOCS, 100, 300)))


def test_identifiers():
    assert identifiers("what does section 3.2 of RFC 3986 define") == {"3.2", "3986"}
    assert identifiers("what does ABNF stand for") == frozenset()
    assert all(identifiers(a) == identifiers(b) for a, b in PARAPHRASES)


def test_an_embedding_is_a_unit_vector():
    import numpy as np
    assert abs(float(np.linalg.norm(embed()("what does the 418 status code mean"))) - 1.0) < 1e-9


def test_without_the_guard_no_threshold_is_safe():
    """Every threshold that answers a paraphrase also answers a near miss."""
    hits = sweep(PARAPHRASES, embed(), THRESHOLDS, guard_identifiers=False)
    wrong = sweep(NEAR_MISSES, embed(), THRESHOLDS, guard_identifiers=False)
    assert hits == {0.8: 5, 0.9: 2, 0.95: 1, 0.98: 0}
    assert wrong == {0.8: 2, 0.9: 1, 0.95: 1, 0.98: 1}


def test_section_three_point_two_is_served_the_answer_to_three_point_four():
    """The two questions score 0.981 - higher than nine of the ten paraphrases."""
    e = embed()
    a, b = NEAR_MISSES[6]
    score = float(e(a) @ e(b))
    assert round(score, 3) == 0.981
    assert sum(float(e(x) @ e(y)) > score for x, y in PARAPHRASES) == 0


def test_with_the_guard_the_hits_stay_and_the_wrong_answers_go():
    assert sweep(PARAPHRASES, embed(), THRESHOLDS, guard_identifiers=True) == {0.8: 5, 0.9: 2, 0.95: 1, 0.98: 0}
    assert sweep(NEAR_MISSES, embed(), THRESHOLDS, guard_identifiers=True) == {0.8: 0, 0.9: 0, 0.95: 0, 0.98: 0}


def test_another_reader_is_another_cache():
    store = SemanticCache(embed(), 0.8)
    store.put("what does the 418 status code mean", {"staff"}, ["rfc-2324#1"])
    assert store.get("what does the 418 status code mean", set()) is None
    value, score = store.get("what does the 418 status code mean", {"staff"})
    assert value == ["rfc-2324#1"] and score > 0.999


def test_the_best_entry_wins():
    store = SemanticCache(embed(), 0.5)
    store.put("how do cookies expire", set(), "far")
    store.put("when does a cookie expire", set(), "near")
    assert store.get("when does a cookie expire", set())[0] == "near"
