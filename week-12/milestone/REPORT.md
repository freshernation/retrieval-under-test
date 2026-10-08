# Final report — [your name]

> The last one. `tools/check_evals.py` enforces the run ids; the rest is on you.
>
> **First line is a blocker.** Section 2 comes before section 3. Every number carries its n.

---

## 1 · What you must act on

Ranked. Blockers first, each with the evidence, the station, and the cost of doing nothing.

| # | Blocker | Station | Evidence | Cost of inaction |
|---|---|---|---|---|
| 1 | | | `run:<id>` | |

If the first row is not something a reader would do something about this week, it is not a
blocker.

## 2 · What this evaluation cannot see

Before the numbers. Deliberately.

- **correctness** — unmeasurable since week 1, and still. Say what you measured instead and
  what the gap is
- what else:

For each one, a sentence on what it would cost to see it.

## 3 · The numbers

| Metric | Value | n | MDE of the set | Above the floor | Run |
|---|---|---|---|---|---|
| | | | | | |

No bare numbers. If a number has no n, it does not go in the table.

### 3a · The MDE audit

Every claimed delta, weeks 2 to 11.

| Week | Claim | Delta | n | MDE | Above the floor |
|---|---|---|---|---|---|
| 2 | | | | | |
| … | | | | | |
| 11 | your own agent | | | | |

Count the rows below the floor. State the count in a sentence.

### 3b · The attribution report

| Station | Failures |
|---|---|
| 1 corpus | |
| 2 chunk | |
| 4 retrieve | |
| 5 rank | |
| 6 generate | |
| 7 none | |

One sentence on the empty rows, and what they mean for the backlog.

## 4 · What expires

| Claim | Mark | Why | Re-measure how |
|---|---|---|---|

Counts: **durable** · **re-measure annually** · **expired**

If `expired` is zero, read your fences again.

---

## 5 · The failure library

**Failures I cannot card**, first, with the evidence each would need:

Then the cards. Roughly thirty, each with all six fields:

> the failure · the station · the diagnostic that finds it · the fix · the measured delta ·
> the conditions under which the fix stops working

Deleted this week, with one line each:

## 6 · Clinics

Average: \_\_\_ / 5 across ten, scored by \_\_\_.

Lowest three, and what you reached for instead:

| # | Score | What you reached for | What it was |
|---|---|---|---|

## 7 · The handover

One page, for the person who inherits this. The eval set and what it cannot see; the three
numbers to watch; the gate; **the two empty stations**; the failures with no card; what you
would do with one more week.

## 8 · What I would do with one more week

Ranked, cheapest first. If one of them is *write more queries*, price it.

## 9 · What I got wrong in this course

At least two. One from the first month, one from the last.
