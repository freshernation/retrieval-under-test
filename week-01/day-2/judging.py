"""Relevance judgments, and the arithmetic of disagreeing with yourself.

A judgment is a person saying *this document answers this query*. Everything
downstream — every metric, every comparison, every claim you make for the rest of
this course — is a function of these numbers, which makes this the highest-leverage
and least glamorous file in the repository.

Grades:

    0  irrelevant
    1  related, but does not answer it
    2  answers it
    3  answers it completely, on its own

Replace each `raise NotImplementedError` with your own code.
"""

from __future__ import annotations

from collections import Counter

VALID_GRADES = (0, 1, 2, 3)
RELEVANT_AT = 2


def parse_grade(value: object) -> int:
    """Coerce a judgment to a grade, or raise ValueError.

    Accept an int in 0..3, or a string of one. Reject everything else —
    including `True`, `2.5`, and `"2 "` with a space. Being strict here is
    cheap; a `qrels` file with one bad row silently scores that query zero for
    every system you will ever compare.
    """
    raise NotImplementedError


def relevant_set(judgments: dict[str, int], threshold: int = RELEVANT_AT) -> set[str]:
    """The document ids at or above `threshold`.

    This is where graded judgments become binary, and it is a lossy step you
    should be able to justify: recall does not know the difference between a
    document that answers the question completely and one that barely clears
    the bar.
    """
    raise NotImplementedError


def agreement(a: dict[str, int], b: dict[str, int]) -> float:
    """Fraction of commonly-judged documents where two judges gave the same grade.

    Judge only the overlap: a document one of you never looked at is not a
    disagreement, it is a gap. Returns 1.0 when there is no overlap, on the
    grounds that no evidence of disagreement is not evidence of disagreement —
    and `overlap_size` exists so you can tell the two apart.
    """
    raise NotImplementedError


def overlap_size(a: dict[str, int], b: dict[str, int]) -> int:
    """How many documents both judges graded. Always report this next to any
    agreement number; 100% agreement on three documents is not a finding."""
    raise NotImplementedError


def binary_disagreements(
    a: dict[str, int], b: dict[str, int], threshold: int = RELEVANT_AT
) -> list[str]:
    """Documents where the two judges land on opposite sides of `threshold`.

    Sorted, for stable tests. These are the disagreements that actually change a
    recall number — a 2-versus-3 argument changes nDCG slightly and recall not
    at all, while a 1-versus-2 changes everything, which is why the 1/2 line is
    where all the annotation guidance in the world is aimed.
    """
    raise NotImplementedError


def cohens_kappa(a: dict[str, int], b: dict[str, int]) -> float:
    """Agreement corrected for the agreement you would get by chance.

        kappa = (p_observed - p_chance) / (1 - p_chance)

    where `p_chance` is the probability two judges agree if each draws
    independently from their own observed grade distribution.

    Why bother: if 90% of everything you judge is a 0, two judges who label
    everything 0 agree 90% of the time and have told you nothing. Kappa says 0
    for that, correctly.

    Return 1.0 when `p_chance` is 1.0 — every judgment identical on both sides
    leaves nothing to correct for, and the formula divides by zero.
    """
    raise NotImplementedError


def pool(rankings: list[list[str]], depth: int = 10) -> list[str]:
    """The set of documents worth judging, from several systems' rankings.

    Take the top `depth` from each list and union them, preserving first-seen
    order across the lists in the order given. This is *pooling*, and it is how
    TREC has built judgment sets since 1992: you cannot judge a whole corpus, so
    you judge everything that any credible system ranked highly.

    It has a known and permanent bias — a document no system in the pool ever
    ranked highly is graded 0 forever, including for a future system that finds
    it. Knowing that this bias exists in every retrieval benchmark you will ever
    read is worth more than the function.
    """
    raise NotImplementedError


def smells(judgments_by_query: dict[str, dict[str, int]], corpus_ids: set[str]) -> list[str]:
    """Everything wrong with an eval set that a machine can see.

    Return one string per problem, sorted, empty when the set is sound. Detect:

    - a query with no document graded >= 2 — unanswerable, and it drags every
      mean down for reasons that have nothing to do with the retriever
    - a query where every judged document is relevant — you labelled only what
      you already believed, so the query cannot punish a bad result. **This is
      the one that ruins eval sets and it is invisible in the metrics**
    - a judgment for a document id that is not in the corpus
    - a query with fewer than 3 judgments — too thin to mean anything

    Prefix each message with the query id, so they sort usefully.
    """
    raise NotImplementedError
