"""Let the day's tests import this day's module, and the earlier weeks' labs.

Week 8 builds on your own weeks 2 to 7 code — the supersession graph,
the analyzer, the index, BM25, the section chunker, the answer-span metric, the
dense retriever, the hybrid fusion and the context assembler. Those directories go on
the path here rather than in each test file, so that a missing import is a
missing *lab* rather than a missing line of plumbing.

Lab module names are unique across the whole course, which is what makes this
safe; `tests/test_repo.py` enforces it.
"""

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]

sys.path.insert(0, str(ROOT))
for week, days in (("week-02", ("day-1", "day-2", "day-3", "day-4")),
    ("week-03", ("day-1", "day-2", "day-3")),
    ("week-04", ("day-1", "day-2", "day-3", "day-4")),
    ("week-05", ("day-1", "day-2", "day-3", "day-4", "milestone")),
    ("week-06", ("day-1", "day-2", "day-3", "day-4", "milestone")),
    ("week-07", ("day-1", "day-2", "day-3", "day-4", "milestone")),):
    for day in days:
        sys.path.insert(0, str(ROOT / week / day))
sys.path.insert(0, str(HERE))
