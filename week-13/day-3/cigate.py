"""The gate runs itself.

Week 9 built a gate: rules, a direction, a tolerance, a verdict. Then it sat in a
library and ran when somebody remembered to run it - which is to say, before the
changes people were proud of, and not before the ones they were not.

Today it runs on every pull request, with no one deciding to run it, and the
interesting part is everything around the arithmetic:

- **The baseline is a file in the repository**, so changing what "good" means is a
  change somebody reviews - with a reason written next to it.
- **CI never writes the baseline.** A gate that accepts its own new numbers is a
  gate that can be talked into anything. Accepting is a person, on purpose.
- **The tolerance is chosen in advance**, from week 9's noise floor. On nineteen
  queries a zero-tolerance gate fires on one query changing its mind.

Replace each `raise NotImplementedError` with your own code.
"""

from __future__ import annotations

from gate import HIGHER, Rule

RULES = [Rule("mrr", HIGHER, 0.08), Rule("recall@3", HIGHER, 0.08)]


def measure(rank, queries) -> dict:
    """`rank(text)` returns ranked document ids. Score it with
    raglab.metrics.evaluate(..., ks=(1, 3)) and return
    {"mrr": <4 places>, "recall@3": <4 places>, "n": <answerable queries>}."""
    raise NotImplementedError


def read_baseline(path) -> dict | None:
    """The baseline file's JSON - {"metrics": {...}, "reason": "..."} - or None if
    there is no file."""
    raise NotImplementedError


def write_baseline(path, metrics: dict, reason: str) -> None:
    """Write {"metrics": metrics, "reason": <reason, stripped>} as JSON. An empty
    reason raises ValueError: nobody gets to move the goalposts silently."""
    raise NotImplementedError


def decide(baseline: dict, candidate: dict, rules=RULES) -> dict:
    """week 9's Gate(rules).check(baseline, candidate), plus "improved": the
    metrics, in rule order, where the candidate beats the baseline by MORE than the
    rule's tolerance. Inside the tolerance is not an improvement; it is noise."""
    raise NotImplementedError


def run(rank, queries, baseline_path, rules=RULES, accept: str | None = None, say=print) -> int:
    """What CI runs. Measure the candidate, then:

        no baseline file      with `accept`: write it, return 0
                              without: say so, return 2
        otherwise             decide; say the baseline, the candidate, each
                              failure ("REGRESSION ...") and each improvement;
                              if it passed and `accept` was given, write the
                              candidate as the new baseline with that reason.
                              Return 0 if it passed, 1 if not.

    A failed run never writes the baseline, whatever `accept` says."""
    raise NotImplementedError
