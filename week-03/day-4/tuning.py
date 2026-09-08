"""Tuning k1 and b — and learning to distrust the result.

Two numbers. On this corpus they move ndcg@3 by eighteen points, which makes
tuning the highest-leverage hour of the week and the easiest place to fool
yourself in the whole course.

Everything today is a **tuning change** in the sense of `EVALS.md`: there is no
argument for k1=2.4 except the number. So the number has to be good, and most of
this lab is about the ways it is not.

`day-3/bm25.py` is importable.

Replace each `raise NotImplementedError` with your own code.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "day-3"))
from bm25 import search  # noqa: E402

from raglab.metrics import evaluate  # noqa: E402

K1_GRID = (0.0, 0.3, 0.6, 0.9, 1.2, 1.5, 1.8, 2.1, 2.4)
B_GRID = (0.0, 0.25, 0.5, 0.75, 1.0)


def grid_search(index, queries, metric="ndcg@3", k1_values=K1_GRID, b_values=B_GRID, k=10):
    """Every (k1, b) pair, scored, best first.

    Return `(score, k1, b)` triples with the score rounded to 4 decimals, sorted
    by score descending and then by k1 and b ascending — so that ties resolve to
    the *smaller* parameters. That is a real choice: on a plateau the smallest
    values are the least extreme and the most likely to survive contact with
    other data.

    Run it on `dev`. Only ever on `dev`.
    """
    raise NotImplementedError


def best(results):
    """The top triple."""
    raise NotImplementedError


def spread(results) -> tuple[float, float]:
    """`(worst, best)` score across the grid.

    Report this next to any tuned number. A grid whose scores span 0.71 to 0.89
    is telling you the parameters matter; one that spans 0.882 to 0.886 is
    telling you to stop tuning and go and do something else.
    """
    raise NotImplementedError


def rank_of(results, k1: float, b: float) -> int:
    """Where a specific configuration placed, 1-based. Raises KeyError if it was
    not in the grid.

    Use it on the defaults. `k1=1.2, b=0.75` is the value in most of the
    literature and in most search engines, and on this corpus it comes **38th
    out of 45**. Conventions are conventions.
    """
    raise NotImplementedError


def at_edge(k1: float, b: float, k1_values=K1_GRID, b_values=B_GRID) -> bool:
    """Whether the chosen configuration sits on the boundary of the grid.

    **This is the most important function in the file.** A grid search that
    returns an edge value has not found an optimum — it has found the edge of
    your grid, and the real optimum is somewhere you did not look.

    Today's is at the edge, and widening the grid shows the score still rising
    at k1=4 and then flat for ever. A plateau extending to infinity means the
    tuner is asking you to set k1 to infinity, which is to say: **turn term
    saturation off entirely.** That is a substantive claim about your corpus,
    it disagrees with thirty years of practice, and it deserves to be
    investigated rather than shipped.
    """
    raise NotImplementedError


def looks(results) -> int:
    """How many configurations you evaluated.

    The multiple-comparisons count, and it belongs in the report. Forty-five
    looks at nine queries at a 95% confidence level means you should expect
    roughly two configurations to look significantly better than they are, for
    free, from noise alone.
    """
    raise NotImplementedError


def moved_queries(index, queries, a, c, metric="ndcg@3", k=10):
    """Query ids whose score differs between configurations `a` and `c`, each a
    `(k1, b)` pair. Sorted.

    Run this on your tuned configuration against the default before you believe
    anything. If a seven-point improvement rides on three queries out of nine,
    what you have tuned is those three queries.
    """
    raise NotImplementedError
