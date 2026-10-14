"""The vector side of a change: what to embed again, and with what.

Yesterday's index was lexical, and a new document simply joined it. A dense
index has a model behind it, and that raises two questions a posting list never
asks.

**What actually changed?** Embedding is the expensive step, so you embed only
what is new. That needs a fingerprint of each chunk's content.

**Embedded by which model?** In this course the "model" is the basis week 5
fitted to the corpus. A new chunk can be projected into the old basis - *folded
in* - without refitting. That is what every production system does with a frozen
embedding model, and it means the new chunk is described using only the
vocabulary the model already had.

Replace each `raise NotImplementedError` with your own code.
"""

from __future__ import annotations

import numpy as np


def fingerprint(text: str) -> str:
    """The first 16 hex characters of the SHA-256 of the text, with every run of
    whitespace collapsed to one space and the ends stripped.

    Collapsing whitespace is a decision: re-wrapping a paragraph should not cost
    you an embedding. Lowercasing would be a second decision, and is not made
    here.
    """
    raise NotImplementedError


def diff(old: dict[str, str], new: dict[str, str]) -> dict[str, list[str]]:
    """Compare two chunk sets **by id**. Four sorted lists of chunk ids:

        added       in `new` and not in `old`
        removed     in `old` and not in `new`
        changed     in both, with different fingerprints
        unchanged   in both, with the same fingerprint
    """
    raise NotImplementedError


def reusable(old: dict[str, str], new: dict[str, str]) -> list[str]:
    """The ids in `new`, sorted, whose **text** already exists somewhere in
    `old` under any id.

    `diff` asks whether an id is new. This asks whether the content is, which
    is the question an embedding bill depends on.
    """
    raise NotImplementedError


def unseen_terms(retriever, chunks: dict[str, str]) -> list[str]:
    """The terms in `chunks`, sorted, that are not in `retriever.vocab`.

    Use week 5's `build_vocabulary`. These are the words a folded-in chunk
    cannot be described with: the model has no axis for them.
    """
    raise NotImplementedError


def fold_in(retriever, texts: list[str]) -> np.ndarray:
    """Embed `texts` with the retriever's **existing** vocabulary, idf and
    basis - exactly as it embeds a query - and L2-normalise each row.

    One row per text, `retriever.dims` columns. No texts gives a 0-row array of
    that width. Nothing about the retriever changes.
    """
    raise NotImplementedError


class Folded:
    """A fitted retriever plus chunks folded into it afterwards.

    `ids` is the retriever's ids followed by the new ids in sorted order, and
    `D` is the matching matrix. `search` scores a query against all of it, with
    the same tie-break as week 5: higher score first, then earlier row.
    """

    def __init__(self, retriever, new_chunks: dict[str, str]) -> None:
        raise NotImplementedError

    def search(self, query: str, k: int = 5) -> list[str]:
        raise NotImplementedError


def agreement(a: dict[str, list[str]], b: dict[str, list[str]]) -> float:
    """The fraction of `a`'s queries whose result list is identical in `b`.
    0.0 when `a` is empty."""
    raise NotImplementedError
