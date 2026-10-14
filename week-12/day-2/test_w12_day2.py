"""Day 2 — the vector side of a change.

`test_folding_in_is_a_different_system_and_recall_cannot_tell_you_so` is the day.
"""

from functools import cache

import numpy as np
import pytest

import raglab
from dense import DenseRetriever
from refresh import Folded, agreement, diff, fingerprint, fold_in, reusable, unseen_terms
from sections import section_corpus
from windows import parent

CORPUS = raglab.corpus.load()
DOCS = {d.id: d.title + "\n" + d.text for d in CORPUS}
ARRIVING = {"rfc-8259", "rfc-8615"}  # the two replacements, published last


@cache
def chunks():
    return section_corpus(DOCS, 100, 300)


@cache
def dev():
    return list(raglab.judgments.load(file="queries-extended.yml").split("dev"))


@cache
def before():
    return {c: t for c, t in chunks().items() if parent(c) not in ARRIVING}


@cache
def arriving():
    return {c: t for c, t in chunks().items() if parent(c) in ARRIVING}


@cache
def stale():
    return DenseRetriever(dims=192).fit(before())


@cache
def refit():
    return DenseRetriever(dims=192).fit(chunks())


def reaches_new(runs):
    return sum(1 for r in runs.values() if any(parent(c) in ARRIVING for c in r))


# -- what changed --------------------------------------------------------------


def test_a_fingerprint_ignores_rewrapping_and_nothing_else():
    assert fingerprint("a  b\n c") == fingerprint(" a b c ")
    assert fingerprint("a b c") != fingerprint("A b c")
    assert fingerprint("a b c") != fingerprint("a b d")
    assert len(fingerprint("x")) == 16


def test_diff_by_id():
    old = {"d#0": "one", "d#1": "two", "d#2": "three"}
    new = {"d#0": "one", "d#1": "two, revised", "d#3": "four"}
    assert diff(old, new) == {
        "added": ["d#3"], "removed": ["d#2"], "changed": ["d#1"], "unchanged": ["d#0"],
    }


def test_two_new_documents_are_thirty_nine_new_chunks():
    result = diff(before(), chunks())
    assert len(result["added"]) == 39
    assert len(result["unchanged"]) == 227
    assert result["changed"] == [] and result["removed"] == []


def test_a_revised_document_is_almost_entirely_a_new_document():
    """**RFC 8259 revises RFC 7159. Two of its twenty-one chunks are reusable.**

    It is the same specification with corrections, and a content fingerprint
    saves two embeddings out of twenty-one. A changed sentence changes its
    chunk; a changed section boundary changes every chunk after it."""
    assert reusable(before(), arriving()) == ["rfc-8259#13", "rfc-8259#8"]
    assert sum(1 for c in arriving() if parent(c) == "rfc-8259") == 21


# -- embedded by which model ---------------------------------------------------


def test_fold_in_uses_the_model_it_was_given():
    retriever = stale()
    vocab, basis = list(retriever.vocab), retriever.Vt.copy()
    rows = fold_in(retriever, list(arriving().values()))
    assert rows.shape == (39, retriever.dims)
    assert np.allclose(np.linalg.norm(rows, axis=1), 1.0)
    assert retriever.vocab == vocab and np.array_equal(retriever.Vt, basis)
    assert fold_in(retriever, []).shape == (0, retriever.dims)


def test_the_old_model_has_no_word_for_161_things():
    """The arriving chunks use 161 terms the old basis never saw. A folded-in
    chunk is described without any of them."""
    missing = unseen_terms(stale(), arriving())
    assert len(missing) == 161
    assert missing == sorted(missing)
    assert unseen_terms(refit(), arriving()) == []


def test_without_an_insert_the_new_documents_do_not_exist():
    runs = {q.id: stale().search(q.text, 5) for q in dev()}
    assert reaches_new(runs) == 0


def test_folded_puts_the_new_chunks_after_the_old():
    folded = Folded(stale(), arriving())
    assert folded.ids[:227] == stale().ids
    assert folded.ids[227:] == sorted(arriving())
    assert folded.D.shape == (266, stale().dims)


def test_folding_in_is_a_different_system_and_recall_cannot_tell_you_so():
    """**Five of twenty result lists are the same as a refit's.**

    Fold the two new RFCs into the old model, or refit the model on everything:
    the top five agree for a quarter of the queries. The folded-in chunks also
    reach the top five for ten queries, against six after a refit.

    Neither is the right answer. The refit is the system week 5 built; the
    fold-in is the system you will run, because nobody re-embeds a corpus when
    one document arrives. They are two different retrievers, and twenty queries
    cannot say which is better - week 9 worked out how many it would take."""
    folded = Folded(stale(), arriving())
    a = {q.id: refit().search(q.text, 5) for q in dev()}
    b = {q.id: folded.search(q.text, 5) for q in dev()}
    assert agreement(a, b) == 0.25
    assert reaches_new(a) == 6
    assert reaches_new(b) == 10


def test_agreement():
    assert agreement({"q1": ["a"], "q2": ["b"]}, {"q1": ["a"], "q2": ["c"]}) == 0.5
    assert agreement({"q1": ["a", "b"]}, {"q1": ["b", "a"]}) == 0.0
    assert agreement({}, {}) == 0.0


def test_a_query_with_no_known_words_returns_nothing():
    assert Folded(stale(), arriving()).search("zzzz qqqq", 5) == []
