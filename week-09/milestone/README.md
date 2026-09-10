# Milestone 9 — The harness, the gate, and the Monday summary

> **Ship:** one runnable thing that measures everything you know how to measure, a gate that
> blocks a regression without crying wolf, and a summary whose first line is a blocker rather
> than a metric.

---

## The brief

### 1. Build the suite

`EvalSuite`: week 8's report card, plus this week's proxies, power and judge sections.

The suite **owns the contexts** — builds them once, hands the same ones to every check. A
harness that rebuilds retrieval per metric can report a faithfulness computed against a
context the generator never saw, and the numbers look completely normal.

### 2. Report the judge with its baseline

Accuracy **and** constant-baseline accuracy. Kappa **and** baseline kappa. Self-agreement.

A judge in a report without those four numbers is a number that cannot be interpreted, and
this week found one whose accuracy matched the baseline exactly.

### 3. State the power before the results

`n`, `sd`, `mde`, and a power table. Then go back through your week 2 to 8 reports and mark
every delta you claimed as **above** or **below** the MDE of the set it was measured on.

That list is uncomfortable and it is the most valuable page in the milestone.

### 4. Build a gate, and measure its false-alarm rate

At most **five** guarded metrics, each with a direction and a tolerance derived from the MDE.

Then run it on repeated runs of an unchanged system and report the false-alarm rate. A gate
you have not measured this way is a gate you are about to mute.

### 5. Write the Monday summary

Ranked, not sorted: blockers first, then what the eval set **cannot** measure, then the
numbers. A summary that opens with a metric is a summary nobody finishes.

### 6. Confirm once on `test`, and write `REPORT.md`

---

## The rubric

| Station | This week |
|---|---|
| 1 Corpus | One sentence: which of your checks would notice a document going out of date? |
| 2 Chunk | One sentence on what your chunk size did to the paired standard deviation |
| 3 Index | One sentence: which serving-time signal would tell you the index had degraded? |
| 4 Retrieve | The proxies, and which of them you would actually instrument |
| 5 Rank | One sentence on what you can detect at your n |
| 6 Generate | The judge, its baseline, and whether you would gate on it |
| 7 Measure | **The week.** The harness, the gate, and the list of things you cannot see |

---

## The bar

- `pytest week-09 -v` green, `tools/check_evals.py` green
- Judge reported with all four baseline numbers
- Power stated **before** the results, with the retrospective MDE audit
- Gate with at most five guarded metrics and a measured false-alarm rate
- Summary ranked, leading with a blocker
- Exactly one `test` run this week
- You survive Friday

---

## What you will want to do and should not

**Report the judge's accuracy alone.** 0.70 looks respectable and is the base rate.

**Gate on everything you measure.** Ten metrics fire spuriously two times in five.

**Set a tight tolerance because it feels rigorous.** Below the MDE it is a coin flip, and the
gate will be switched off by somebody who is right to switch it off.

**Skip the retrospective audit.** Most of this course's deltas were below the MDE of the set
they were measured on. The course said so each time; your report should say so once, in one
place, with the numbers.

**Lead the summary with faithfulness.** It is 1.00 and thirty percent of the answers are
wrong.
