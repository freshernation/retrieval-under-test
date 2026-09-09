"""A dense retriever, frozen, and compared honestly.

Four days assembled, plus the step nobody does: **writing the vectors down with
a manifest that says what made them.**

Replace each `raise NotImplementedError` with your own code.
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np


class DenseRetriever:
    """Fit on a chunk corpus, then search it.

    The config must record **everything that changes a vector**: the number of
    dimensions, the analyzer options, the chunker that produced the chunks, and
    the size of the vocabulary. Two indexes built with different vocabularies
    are different spaces, and a config that does not say so lets you compare
    them as though they were the same.
    """

    def __init__(self, dims: int = 192, **config) -> None:
        raise NotImplementedError

    def fit(self, chunks: dict[str, str]) -> "DenseRetriever":
        """Build the vocabulary, the weighted matrix, the factorisation, and the
        chunk embeddings. Returns self, so it chains."""
        raise NotImplementedError

    @property
    def config(self) -> dict:
        """Complete, hashable, and including `n_vocab` and `n_chunks`."""
        raise NotImplementedError

    def search(self, query: str, k: int = 5) -> list[str]:
        """Ranked chunk ids. `[]` for a query with no known terms."""
        raise NotImplementedError

    def freeze(self, path: Path) -> Path:
        """Write `<path>.npy` and `<path>.json` in `raglab.vectors`' format.

        The manifest carries `ids`, `model`, `dim`, `normalised` and `created`.
        `raglab.vectors.load` refuses a manifest whose id count disagrees with
        the matrix, and that check exists because **the failure it catches is
        silent**: every neighbour you compute is for the wrong document, and
        nothing errors.

        Embeddings are a frozen artefact of a model at a version. Write down
        which one, or in six months you will have a matrix and no way to know
        what can be compared with it.
        """
        raise NotImplementedError


def side_by_side(dense: DenseRetriever, lexical, chunks, queries, ks=(1, 3, 5, 10)) -> dict:
    """The comparison the report needs, at several k:

        per k: dense recall, lexical recall, oracle, headroom, and the tally

    Several k, because week 5 found that **the winner changes with it**. A
    comparison at one k is a claim about that k, and reporting it as a claim
    about the systems is the most common error in this literature.
    """
    raise NotImplementedError


def is_comparable(a: dict, b: dict) -> bool:
    """Whether two configs describe indexes that can be compared at all.

    They cannot if they were built over different chunkings or different
    vocabularies — those are different spaces and different corpora, and a
    difference in score is then not attributable to anything you changed
    deliberately.

    Cheap, mechanical, and it catches the week's most expensive mistake.
    """
    raise NotImplementedError
