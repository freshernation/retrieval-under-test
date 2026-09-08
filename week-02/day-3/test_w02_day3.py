"""Day 3 — near-duplicates, and what they mean.

Read `test_similarity_cannot_find_the_second_supersession` and
`test_deleting_either_one_is_wrong` together. They are why tomorrow exists.
"""

import sys
from functools import cache
from pathlib import Path

import pytest

import raglab
from dedupe import (
    estimate_jaccard,
    jaccard,
    longest_shared_run,
    minhash,
    near_duplicate_pairs,
    shingles,
    words,
)

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "day-2"))
from boilerplate import clean  # noqa: E402

CORPUS = raglab.corpus.load()
RAW = {d.id: d.text for d in CORPUS}


@cache
def cleaned() -> dict[str, str]:
    """Lazy — day 2's `clean` may not be written yet, and that should fail these
    tests rather than stop the week from collecting."""
    return {d.id: clean(d.text) for d in CORPUS}


# -- shingles -----------------------------------------------------------------


def test_shingles_are_contiguous_word_runs():
    assert shingles("a b c d", k=3) == {("a", "b", "c"), ("b", "c", "d")}


def test_a_short_document_is_one_shingle():
    assert shingles("a b", k=5) == {("a", "b")}
    assert shingles("", k=5) == set()


def test_order_is_what_makes_it_evidence():
    """Two documents about JSON share most of their vocabulary whether or not
    either was copied. Only a shared *sequence* is evidence of copying."""
    a, b = "the cat sat on the mat", "the mat sat on the cat"
    assert set(words(a)) == set(words(b))
    assert jaccard(shingles(a, 3), shingles(b, 3)) < 0.5


# -- jaccard ------------------------------------------------------------------


def test_jaccard_basics():
    assert jaccard({1, 2}, {1, 2}) == 1.0
    assert jaccard({1, 2}, {3, 4}) == 0.0
    assert jaccard({1, 2}, {2, 3}) == pytest.approx(1 / 3)
    assert jaccard(set(), set()) == 1.0


def test_the_json_pair_is_more_than_half_identical():
    """RFC 7159 and RFC 8259. Same title, same editor, three years apart."""
    score = jaccard(shingles(RAW["rfc-7159"]), shingles(RAW["rfc-8259"]))
    assert score == pytest.approx(0.547, abs=0.005)


# -- minhash ------------------------------------------------------------------


def test_the_signature_estimates_the_real_thing():
    a, b = shingles(RAW["rfc-7159"]), shingles(RAW["rfc-8259"])
    assert estimate_jaccard(minhash(a), minhash(b)) == pytest.approx(jaccard(a, b), abs=0.06)


def test_the_estimate_is_wrong_and_you_should_know_by_how_much():
    """0.500 estimated against 0.547 exact, with 128 permutations. That error is
    not a bug, it is the price, and the only time you can see it is now — on ten
    million documents the exact answer does not exist to compare against."""
    a, b = shingles(RAW["rfc-7159"]), shingles(RAW["rfc-8259"])
    assert estimate_jaccard(minhash(a, 128, seed=0), minhash(b, 128, seed=0)) == pytest.approx(
        0.5, abs=0.01
    )


def test_signatures_are_stable_across_runs():
    """`zlib.crc32`, not `hash()`. Python salts string hashing per process, so a
    signature built with `hash()` differs between runs, and a deduplication
    index built on it silently stops matching after a restart."""
    s = shingles(RAW["rfc-7725"])
    assert minhash(s, 64, seed=1) == minhash(s, 64, seed=1)


def test_mismatched_signatures_are_refused():
    with pytest.raises(ValueError):
        estimate_jaccard([1, 2, 3], [1, 2])


# -- what cleaning did --------------------------------------------------------


def test_the_raw_corpus_has_ten_pairs_above_five_percent():
    assert len(near_duplicate_pairs(RAW, threshold=0.05)) == 10


def test_the_cleaned_corpus_has_two():
    """**This is what yesterday bought you.** Cleaning did not move recall by a
    measurable amount. It removed eight spurious near-duplicate pairs and made
    the real one sharper — because on the raw text the "similarity" between
    unrelated RFCs was mostly the copyright licence they all carry.

    The value of a change does not always show up in the task you were thinking
    about when you made it. That is not a licence to make unmeasured changes; it
    is a reason to measure more than one thing."""
    pairs = near_duplicate_pairs(cleaned(), threshold=0.05)
    assert len(pairs) == 2
    assert {(a, b) for _, a, b in pairs} == {
        ("rfc-7159", "rfc-8259"),
        ("rfc-5785", "rfc-8615"),
    }


def test_the_real_pair_gets_sharper_and_the_spurious_ones_collapse():
    raw_spurious = jaccard(shingles(RAW["rfc-6585"]), shingles(RAW["rfc-7725"]))
    clean_spurious = jaccard(shingles(cleaned()["rfc-6585"]), shingles(cleaned()["rfc-7725"]))
    assert raw_spurious > 3 * clean_spurious

    assert jaccard(shingles(cleaned()["rfc-7159"]), shingles(cleaned()["rfc-8259"])) > jaccard(
        shingles(RAW["rfc-7159"]), shingles(RAW["rfc-8259"])
    )


# -- what is actually shared --------------------------------------------------


def test_the_json_pair_shares_the_specification():
    """222 words verbatim, and they are the specification."""
    run = longest_shared_run(RAW["rfc-7159"], RAW["rfc-8259"])
    assert len(run) == 222
    assert "json" in run and "interoperable" in run


def test_the_other_pair_shares_the_copyright_notice():
    """68 words, and they are the IETF Trust licence. Same measurement, opposite
    meaning. A similarity score that cannot tell a specification from a legal
    boilerplate is a number you must not act on without looking."""
    run = longest_shared_run(RAW["rfc-5785"], RAW["rfc-8615"])
    assert "trustee" in run and "license" in run
    assert "well" not in run


# -- and what it all means ----------------------------------------------------


def test_similarity_cannot_find_the_second_supersession():
    """Both pairs are supersessions. RFC 8259 obsoletes 7159; RFC 8615 obsoletes
    5785. Exactly the same relationship.

    Their similarities are 0.547 and 0.185. **There is no threshold that catches
    both and nothing else.** Set it at 0.5 and you miss half your supersessions;
    set it at 0.15 and on a real corpus you drown.

    Near-duplicate detection is not a supersession detector and cannot be made
    into one, because the relationship is not a fact about the text. It is
    metadata, and tomorrow is about going and getting it."""
    strict = {(a, b) for _, a, b in near_duplicate_pairs(cleaned(), threshold=0.5)}
    assert ("rfc-5785", "rfc-8615") not in strict
    assert ("rfc-7159", "rfc-8259") in strict


def test_deleting_either_one_is_wrong():
    """The reflex when you find a 55% duplicate is to drop one. Both directions
    are wrong here, and for different reasons.

    Drop RFC 7159 and you lose the ability to answer "what changed" — query r14
    in the test split needs both, and neither document contains the comparison.
    Drop RFC 8259 and your corpus now confidently returns the obsolete rule.

    Deduplication is a decision about *what the corpus is for*, and it is a
    station 1 decision. It is not a cleanup step."""
    qs = raglab.judgments.load().split("test")
    r14 = qs.by_id("r14")
    assert r14.judgments["rfc-7159"] == 2 and r14.judgments["rfc-8259"] == 2
    assert len(r14.relevant) == 2
