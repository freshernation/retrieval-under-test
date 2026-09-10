"""Day 3 — how many queries.

`test_five_points_costs_seventy_seven_queries` is the day.
"""

from functools import cache

import pytest

import raglab
from dense import DenseRetriever
from fuse import rrf
from power import (
    detectable,
    judge_noise_floor,
    mde,
    paired_differences,
    paired_sd,
    power_table,
    queries_needed,
)
from sections import section_corpus
from spans import answer_recall_at_k

CORPUS = raglab.corpus.load()
DOCS = {d.id: d.title + "\n" + d.text for d in CORPUS}


@cache
def dev():
    return [q for q in raglab.judgments.load(file="queries-extended.yml").split("dev") if q.answer_spans]


@cache
def scores():
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
    lexical = {q.id: search(index, q.text, 60) for q in dev()}
    dense = {q.id: retriever.search(q.text, 60) for q in dev()}
    fused = {
        q.id: answer_recall_at_k(rrf([lexical[q.id], dense[q.id]], 5, 10), chunks, q, 5)
        for q in dev()
    }
    plain = {q.id: answer_recall_at_k(lexical[q.id][:5], chunks, q, 5) for q in dev()}
    return fused, plain


# -- the spread ---------------------------------------------------------------


def test_pairing_is_week_threes_reason():
    a, b = scores()
    diffs = paired_differences(a, b)
    assert len(diffs) == 19
    assert all(-1.0 <= d <= 1.0 for d in diffs)


def test_a_binary_metric_has_a_large_spread():
    """A per-query score of 0 or 1 gives differences of −1, 0 or +1, and the
    spread is close to the maximum a bounded quantity can have. **Graded metrics
    need fewer queries than binary ones** — an argument for nDCG that has nothing
    to do with which is more meaningful."""
    a, b = scores()
    assert paired_sd(a, b) == pytest.approx(0.223, abs=0.02)


def test_no_spread_needs_no_queries():
    same = {"a": 1.0, "b": 1.0}
    assert paired_sd(same, same) == 0.0
    assert queries_needed(0.05, 0.0) == 1


# -- the two numbers ----------------------------------------------------------


def test_nineteen_queries_detects_ten_points_and_not_quite():
    """The minimum detectable effect at n=19 is **0.1003** — so even a ten-point
    difference is fractionally below the line.

    Everything you have measured smaller than that, and most of this course's
    deltas are smaller than that, was never distinguishable from zero."""
    a, b = scores()
    floor = mde(19, paired_sd(a, b))
    assert floor == pytest.approx(0.100, abs=0.005)
    assert floor > 0.10


def test_five_points_costs_seventy_seven_queries():
    """**The day.**

    | detect | queries |
    |---|---|
    | 10 points | 20 |
    | 5 points | **77** |
    | 2 points | **479** |

    Note the square. Halving the effect **quadruples** the queries — so "we will
    add a few more queries" is not a plan, and a 2-point improvement is
    genuinely expensive to prove rather than merely tedious.

    Week 3 told you to grow the set to thirty. Thirty detects eight points."""
    a, b = scores()
    sd = paired_sd(a, b)
    assert queries_needed(0.10, sd) == 20
    assert queries_needed(0.05, sd) == 77
    assert queries_needed(0.02, sd) == 479
    assert queries_needed(0.05, sd) > 3 * queries_needed(0.10, sd)


def test_a_bad_effect_is_refused():
    with pytest.raises(ValueError):
        queries_needed(0.0, 0.2)
    with pytest.raises(ValueError):
        mde(0, 0.2)


# -- the floor more queries cannot fix ----------------------------------------


def test_a_noisy_judge_sets_a_floor_no_sample_size_lowers():
    """If a judge disagrees with itself on 10% of cases, a 5-point difference is
    inside its own noise **at any n**. The disagreement is not sampling error;
    it is the instrument."""
    assert judge_noise_floor(0.90) == pytest.approx(0.10)
    assert judge_noise_floor(1.0) == 0.0
    with pytest.raises(ValueError):
        judge_noise_floor(1.5)


def test_both_floors_bind_and_the_larger_wins():
    """Adding queries fixes one and does nothing to the other."""
    a, b = scores()
    sd = paired_sd(a, b)
    assert detectable(0.05, 1000, sd, label_agreement=1.0) is True
    assert detectable(0.05, 1000, sd, label_agreement=0.90) is False
    assert detectable(0.05, 19, sd, label_agreement=1.0) is False


# -- the planning artefact ----------------------------------------------------


def test_the_table_goes_in_the_report_before_the_results():
    """A table showing your experiment could never have detected the effect you
    are claiming is embarrassing afterwards and free beforehand."""
    a, b = scores()
    table = power_table(paired_sd(a, b), (19, 50, 100, 500), (0.02, 0.05, 0.15))
    assert table[19][0.15] is True
    assert table[19][0.05] is False
    assert table[100][0.05] is True
    assert table[500][0.02] is True
    assert 0.02 not in table[19] or table[19][0.02] is False


def test_and_it_indicts_most_of_this_course():
    """Week 2's cleaning delta was 0.111. Week 6's fusion gains were 0.053. Week
    7's reranking ceiling was 0.158.

    At n=19 the minimum detectable effect is 0.100. Two of those three were
    never measurable, and the course said so at the time each was measured —
    which is the only reason this table is a summary rather than a retraction."""
    a, b = scores()
    floor = mde(19, paired_sd(a, b))
    assert 0.053 < floor
    assert 0.111 > floor
    assert 0.158 > floor
