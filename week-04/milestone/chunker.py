"""The chunker, chosen on a frontier rather than picked from a blog post.

Four days assembled into one configurable object and one decision procedure.

Replace each `raise NotImplementedError` with your own code.
"""

from __future__ import annotations

import sys
from pathlib import Path

_WEEK = Path(__file__).resolve().parents[1]
for _day in ("day-1", "day-2", "day-3", "day-4"):
    sys.path.insert(0, str(_WEEK / _day))


class Chunker:
    """One strategy, one config, one `chunk()`.

    Strategies: `"whole"`, `"fixed"` (`size`, `overlap`), `"sections"`
    (`min_words`, `max_words`).

    As in week 3, the config dict is complete rather than partial, because
    `raglab.runs.record` hashes it and a config that omits what it did not set
    cannot be compared with another one. Store the strategy's own parameters
    **and the strategy name**, so that two configs with the same numbers and
    different strategies do not collide.
    """

    def __init__(self, strategy: str = "sections", **config) -> None:
        raise NotImplementedError

    @property
    def config(self) -> dict:
        raise NotImplementedError

    def chunk(self, documents: dict[str, str]) -> dict[str, str]:
        """Chunk id → text. `"whole"` returns the documents unchanged, keyed by
        document id — so that "do not chunk at all" is a configuration on the
        same frontier as everything else, rather than a special case you forget
        to compare against."""
        raise NotImplementedError


def audit(chunks: dict[str, str], queries, documents: dict[str, str] | None = None) -> dict:
    """Everything you must check about a chunking **before** running retrieval:

        n_chunks, min_words, median_words, max_words
        broken       query ids whose answer spans this chunking destroyed
        orphans      chunk ids with no parent among `documents`, when given
        empty        chunk ids with no words

    `broken` is the one that matters and it costs no retrieval at all. A span
    absent from every chunk is not a ranking problem or a recall problem — the
    answer has left the index, and nothing downstream can put it back.

    Run this on every candidate configuration before you measure any of them.
    """
    raise NotImplementedError


def frontier(chunkers: dict[str, "Chunker"], documents, queries, rank_fn, ks=(1, 3, 5, 10)):
    """Measure every chunker at every k and return the non-dominated points,
    cheapest first.

    Returns `(points, frontier)` — all of them and the frontier — because the
    report needs both. A frontier with the dominated points hidden looks like a
    set of good options rather than a set of options.
    """
    raise NotImplementedError


def decide(points, target: float, budget: float | None = None):
    """The cheapest point reaching `target` recall within `budget` words, or None.

    Two numbers from outside the system, and neither is a retrieval question:

    - `target` — how often it is acceptable for the answer not to be in the
      context at all
    - `budget` — how much context you are willing to pay for

    If nothing meets both, return None rather than the nearest thing. A
    chunker that quietly returns something not meeting the requirement is worse
    than one that refuses, because the refusal is a conversation with whoever
    set the requirement and the silent near-miss is not.
    """
    raise NotImplementedError
