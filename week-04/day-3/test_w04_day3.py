"""Day 3 — chunking on the document's own boundaries.

`test_the_same_answers_for_a_quarter_of_the_tokens` is the week's result.
"""

import statistics
from functools import cache

import pytest

import raglab
from sections import heading, pack, section_corpus, section_lengths, split_sections
from spans import broken_by, mean_answer_recall
from windows import chunk_corpus

CORPUS = raglab.corpus.load()
DOCS = {d.id: d.title + "\n" + d.text for d in CORPUS}
QUERIES = raglab.judgments.load()
DEV = QUERIES.split("dev")


@cache
def retrieve(chunks_key: tuple, k: int = 5):
    """(mean answer recall, mean tokens in the top k) for a chunk corpus."""
    import sys
    from pathlib import Path

    root = Path(__file__).resolve().parents[2]
    for day in ("day-3", "day-2", "day-1"):
        sys.path.insert(0, str(root / "week-03" / day))
    from bm25 import search

    from postings import Index

    chunks = dict(chunks_key)
    index = Index(chunks, stopwords=None)
    rankings = {q.id: search(index, q.text, k) for q in DEV}
    scored = [q for q in DEV if q.answer_spans]
    tokens = sum(
        sum(len(chunks[c].split()) for c in rankings[q.id]) for q in scored
    ) / len(scored)
    return mean_answer_recall(rankings, chunks, DEV, k), tokens


def frozen(chunks: dict[str, str]) -> tuple:
    return tuple(sorted(chunks.items()))


# -- headings -----------------------------------------------------------------


def test_a_heading_is_recognised():
    assert heading("2.3.1.  Access Results") == ("2.3.1", "Access Results")
    assert heading("8.  String and Character Issues") == ("8", "String and Character Issues")


def test_indentation_is_what_distinguishes_a_heading_from_prose():
    """RFC body text is indented three spaces and headings are not. That is a
    fact about this format, it is written down nowhere, and you found it by
    reading a document in week 2."""
    assert heading("   2.3.1 is where this is defined") is None


def test_not_everything_starting_with_a_number_is_a_heading():
    assert heading("429 Too Many Requests") is not None  # it is, here
    assert heading("") is None
    assert heading("Abstract") is None


# -- sections -----------------------------------------------------------------


def test_a_section_keeps_its_own_heading():
    """The cheapest useful thing in the file. A chunk beginning `2.4. Caching`
    carries its own topic; a chunk cut at word 400 does not know what it is."""
    secs = split_sections(DOCS["rfc-9309"])
    caching = [b for n, t, b in secs if t.startswith("Caching")]
    assert caching and caching[0].startswith("2.4")


def test_front_matter_is_kept_rather_than_dropped():
    secs = split_sections(DOCS["rfc-7725"])
    assert secs[0][1] == "front matter"
    assert "Abstract" in secs[0][2]


def test_a_document_with_no_headings_is_one_section():
    assert len(split_sections("just some prose with no numbers")) == 1


def test_structure_is_semantically_right_and_dimensionally_useless():
    """286 sections. Median 116 words, minimum 2, maximum 3,547 — a spread of
    more than a thousand times, and seventy-one sections under fifty words.

    This is why `pack` exists, and it is why "chunk on headings" is advice that
    does not survive contact with a document."""
    lengths = section_lengths(DOCS)
    assert len(lengths) == 286
    assert min(lengths) == 2
    assert max(lengths) == 3547
    assert statistics.median(lengths) == pytest.approx(116, abs=2)
    assert sum(1 for x in lengths if x < 50) == 71


# -- packing ------------------------------------------------------------------


def test_small_sections_merge():
    secs = [("1", "a", "one two three"), ("2", "b", "four five six")]
    assert pack(secs, 6, 100) == ["one two three four five six"]


def test_a_large_section_is_split():
    secs = [("1", "a", " ".join(str(i) for i in range(10)))]
    assert pack(secs, 2, 4) == ["0 1 2 3", "4 5 6 7", "8 9"]


def test_an_oversized_section_flushes_the_buffer_first():
    """Appending it to a half-full buffer and then splitting mixes unrelated
    material into the first piece."""
    secs = [("1", "a", "keep me"), ("2", "b", " ".join(str(i) for i in range(6)))]
    assert pack(secs, 2, 3) == ["keep me", "0 1 2", "3 4 5"]


def test_merging_never_overshoots_the_maximum():
    """A 131-word buffer plus a 250-word section is 381 in a corpus configured
    for 300, and nothing complains unless you make it."""
    secs = [("1", "a", "x " * 100), ("2", "b", "y " * 100)]
    assert all(len(c.split()) <= 150 for c in pack(secs, 90, 150))


def test_bad_bounds_are_refused():
    with pytest.raises(ValueError):
        pack([], 0, 10)
    with pytest.raises(ValueError):
        pack([], 100, 10)


def test_packing_normalises_the_spread():
    packed = section_corpus(DOCS, 100, 300)
    lengths = [len(c.split()) for c in packed.values()]
    assert max(lengths) <= 300
    assert statistics.median(lengths) < 300
    assert max(lengths) / max(1, statistics.median(lengths)) < 5


# -- and the result -----------------------------------------------------------


def test_no_configuration_here_destroys_an_answer():
    for lo, hi in ((100, 300), (150, 400), (200, 600)):
        assert broken_by(section_corpus(DOCS, lo, hi), QUERIES) == []


def test_fixed_windows_at_four_hundred_lose_a_fifth_of_the_answers():
    recall, tokens = retrieve(frozen(chunk_corpus(DOCS, 400)))
    assert recall == pytest.approx(0.78, abs=0.02)
    assert tokens == pytest.approx(1926, abs=30)


def test_the_same_answers_for_a_quarter_of_the_tokens():
    """**The week's result.**

    Fixed 800-word windows: every answer retrieved in the top 5, at 3,648 words
    of context.

    Sections packed to 100-300 words: every answer retrieved in the top 5, at
    **984** words of context.

    Identical coverage. Not identical cost — a quarter of it. And fixed windows
    at 400 words, which is the size the internet recommends, lose a fifth of the
    answers outright while still costing twice as much as the sections.

    Note what did **not** improve: this is not better retrieval. It is the same
    answers, cheaper. Chunking is a cost decision, and tomorrow makes that the
    thesis."""
    big_recall, big_tokens = retrieve(frozen(chunk_corpus(DOCS, 800)))
    sec_recall, sec_tokens = retrieve(frozen(section_corpus(DOCS, 100, 300)))

    assert big_recall == 1.0
    assert sec_recall == 1.0
    assert big_tokens == pytest.approx(3648, abs=40)
    assert sec_tokens == pytest.approx(984, abs=30)
    assert sec_tokens < big_tokens / 3
