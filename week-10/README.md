# Week 10 — Production

> **Destination**
> Put the pipeline behind a service boundary — budgeted, cached, traced and priced —
> and discover that none of it made the system any better.

Nine weeks measured quality. Nothing measured time, and a retrieval system that is right
in four seconds is a system nobody uses. This is also the week the course stops being
able to pretend that a number is free.

---

## The week

| Day | Folder | What you'll be able to do |
|---|---|---|
| Mon | `day-1/` | Budget a pipeline per stage, and count work instead of seconds |
| Tue | `day-2/` | Measure a cache honestly, including what it is serving |
| Wed | `day-3/` | Attribute a failure to one station from a trace, by machine |
| Thu | `day-4/` | Find the spend that buys nothing |
| Fri | `milestone/` | Ship the service, its contract, and its refusal |

---

## Five findings

**The mean is 423 and the spread is 269-fold.** A one-word query touches 4 postings; a
seven-word question touches 1,075. Both arrive at the same endpoint with the same
timeout, and capacity sized on the average request is **96% short** of the 95th
percentile. Meanwhile dense search costs 266 comparisons for every query ever asked —
which is either its best property or its worst.

**Cost tells you nothing about quality.** Week 9's AUC, run over a new signal: does an
expensive query predict a failed one? **0.417**, strength 0.583. Chance. You cannot
triage by cost and you cannot spend your way to an answer.

**The same cache scores 0.19 or 0.79.** One cache, capacity five, three guesses about
traffic. Four-fold, from a number typed into a simulator. And the eval set cannot settle
it: twenty-six queries, twenty-six distinct, hit rate zero. **An eval set is built to have
no duplicates**, so the instrument nine weeks went into is structurally unable to measure
this.

**Nothing failed at station 6.**

| station | queries |
|---|---|
| 1 corpus | 1 |
| 2 chunk | **0** |
| 4 retrieve | 2 |
| 5 rank | 3 |
| 6 generate | **0** |
| 7 none | 14 |

Six failures, five of them the candidate set, none of them the prompt — and the chunker,
the other thing people rewrite, is also clean. A trace carrying the chosen **ids** lets a
machine do the walk the course has been teaching by hand since week 1.

**One budget step costs 58% more and buys nothing.** 800 words to 1,200: tokens per query
885 → 1,403, answered rate 0.70 → 0.70. Not an optimisation opportunity — a setting that
should be turned down, invisible on any dashboard, and the easiest win in a production RAG
system.

---

## The milestone's own verdict

The service meets every SLO, exceeds no budget, and `ship_check` refuses anyway — on the
six failures the attribution found.

Nothing broke this week. The pipeline is exactly as good as it was on Friday of week 8; it
is now fast, cached, traced and priced. **Packaging is not improvement**, and a service
report that could not say so would be worse than no service report.

---

## `--live`

This is the week the course admits what it has been simulating. `SETUP.md` gains a
`--live` section: real services, a real model, real prices. The first thing to do with a
real model is re-run weeks 8 and 9 and find out which comparisons survive.

Some will not. That is the experiment, not a disappointment.

---

## Milestone

A service with a contract, and a report that refuses to ship it. Spec in
`milestone/README.md`.
