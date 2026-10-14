"""The release check for a system that changes.

Week 10's `ship_check` asked whether the service was fast enough. This one asks
whether it is still the system you measured, after a week of the corpus moving,
readers differing, and one document that should not be there.

Five numbers, all of which you produced this week:

    debt              day 1 - tombstoned documents over stored documents
    drift             day 1 - the fraction of queries whose results differ
                      from a rebuilt index
    stale_entries     day 3 - the fraction of cache entries built on a
                      document that has since changed or been revoked
    poison_answered   day 4 - the fraction of planted chunks that reached an
                      answer
    leaks             day 3 - how many results a reader was shown that they
                      may not read

Four of them have a limit you choose. One does not.

Replace each `raise NotImplementedError` with your own code.
"""

from __future__ import annotations

AT_MOST = ("debt", "drift", "poison_answered", "stale_entries")
ZERO = ("leaks",)


def release_check(measured: dict, limits: dict) -> dict:
    """Returns `{"ship": bool, "failures": [...]}`.

    - `leaks` must be exactly 0. **It takes no limit**: passing one in `limits`
      is a `ValueError`. A system with a leak budget has decided how many
      people may read what they should not.
    - Every metric in `AT_MOST` needs a limit: a missing one is a `ValueError`.
      Week 10's rule - an SLO target has no default.
    - A metric that was **not measured** fails. Missing from `measured`, or
      `None`, is a failure and never a pass.
    - `failures` lists `leaks` first if it failed, then the `AT_MOST` metrics
      in the order above. A value equal to its limit passes.
    """
    raise NotImplementedError


def change_report(measured: dict, limits: dict) -> str:
    """One line per metric, then the verdict:

        leaks 0 (must be 0) PASS
        debt 0.105 <= 0.200 PASS
        drift 0.400 <= 0.100 FAIL
        poison_answered 1.000 <= 0.000 FAIL
        stale_entries not measured <= 0.050 FAIL
        DO NOT SHIP: drift, poison_answered, stale_entries

    `leaks` first, then `AT_MOST` in order. Three decimal places for the
    fractions and their limits; `leaks` as it was given. The last line is
    `SHIP`, or `DO NOT SHIP: ` and the failures joined with `, `.
    """
    raise NotImplementedError
