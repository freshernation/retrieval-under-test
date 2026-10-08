# Milestone 10 report — [your name]

> Fill this in. Every number cites a run id. `tools/check_evals.py` enforces it, and the
> fence forbids a price in a result.

---

## 1 · What this service promises

Three sentences. What it answers, what it refuses, and what it does not claim to know.

## 2 · The contract

| Term | Value | Where the number came from |
|---|---|---|
| work p50 | | |
| work p95 | | |
| n | | |
| tokens per query | | |
| cache | on / off, capacity | |
| traffic assumed | skew = | |

**Run:** `run:<id>`

Every performance figure above is a work count. If any of them is a clock reading, say
which machine.

## 3 · The budget, per stage

| Stage | Budget | Measured | Within | Provenance of the budget |
|---|---|---|---|---|
| | | | | |

Unbudgeted stages, and why:

## 4 · The tail

p50, p95, p99, and n. One sentence on how many requests your p95 represents.

## 5 · The attribution report

| Station | Failures | Queries |
|---|---|---|
| 1 corpus | | |
| 2 chunk | | |
| 4 retrieve | | |
| 5 rank | | |
| 6 generate | | |
| 7 none | | |

**The two empty stations.** One paragraph: what were you going to work on next, and what
are you going to work on instead?

**Station 7 is not a clean bill of health.** Name one query attributed `7 none` whose
answer is wrong, and say where that failure belongs.

## 6 · The cache

Hit rate, and the traffic distribution that produced it — on the same line.

Work saved, which is not the hit rate.

**Staleness.** What your cache would serve after a document changed, and the rule you would
ship. Then the thing that rule still would not catch.

## 7 · Cost

| Budget | Tokens/query | Answered | Tokens/answer |
|---|---|---|---|
| | | | |

Marginal cost per additional answered query, per step. `waste`:

The setting you turned down, and the number that justified it.

If you quote a monthly figure, the rate you assumed goes on the same line as the figure.

## 8 · The refusal

`ship_check` output, verbatim. Then one paragraph: every SLO is met and the service does
not ship. Say why that is the correct outcome.

## 9 · What this week improved

Be honest. The expected answer is *nothing measurable*, and the reason is that packaging
is not improvement.

## 10 · The failure library

One card minimum. The cached withdrawn RFC is the obvious candidate.

> the failure · the station · the diagnostic that finds it · the fix · the measured delta ·
> the conditions under which the fix stops working

## 11 · What I could not measure

- user-visible latency, because this course counts work and not seconds
- the real traffic distribution, which decides the cache's entire value
- whether an index failure is distinguishable from a retrieval one
- the price of anything, next year
