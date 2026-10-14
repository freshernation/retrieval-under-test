# Milestone 12 report — [your name]

> Fill this in. Every number cites a run id. `tools/check_evals.py` enforces it.

---

## 1 · The system, as the week left it

Three sentences. What changed in the corpus, who reads it, and who can write to it.

## 2 · The release check

`change_report` output, verbatim.

| Metric | Measured | Limit | Where the limit came from |
|---|---|---|---|
| leaks | | none | |
| debt | | | |
| drift | | | |
| poison_answered | | | |
| stale_entries | | | |

**Run:** `run:<id>`

## 3 · Debt and drift

Debt, and drift at depths 1, 5 and 10, on the same line. One sentence on why the first row
is why nobody notices.

Your compaction rule: the trigger, and its cost.

## 4 · Fold-in against refit

Agreement at depth five. Which of the two your week-9 numbers describe, and your rule for
when an eval must be re-run.

## 5 · Readers

| | Short of five | Empty | Leaks |
|---|---|---|---|
| post-filter the top 5 | | | |
| over-fetch, then filter | | | |
| pre-filter | | | |

The cache: leaks with a query-text key, and with a scoped key. What scoping did to the hit
rate, and the traffic assumption that answer rests on.

**Everything else that sits in front of the filter.** A list.

## 6 · The planted document

| | Rate |
|---|---|
| reached the context | |
| reached the answer | |

The three week-8 checks on the poisoned answer, and the question none of them asks.

## 7 · What you fixed, and re-measured

| Metric | Before | After | What you changed |
|---|---|---|---|
| | | | |

`change_report` output after the fixes, verbatim.

## 8 · What you could not fix

At least one. The obvious candidate is a planted document from a source you trust.

## 9 · The failure library

One card minimum.

> the failure · the station · the diagnostic that finds it · the fix · the measured delta ·
> the conditions under which the fix stops working

## 10 · What I could not measure

- whether a real model obeys an instruction in a retrieved chunk
- how far drift grows with debt on a corpus of realistic size
- how long a revoked permission survives in a real deployment's caches
- whether the fold-in gap exists at all for a frozen neural embedding model
