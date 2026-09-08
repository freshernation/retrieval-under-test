# Week 1 — Measure before you build

> **Destination**
> Have a labelled eval set you wrote yourself, a metric you implemented yourself, a
> baseline number on the board, and be able to say how much of that number is real.

By Friday you will have written about forty relevance judgments by hand and a retriever
so simple it is almost an insult. The retriever will score badly. That number is the most
valuable thing you produce this week, because every week after this one is measured
against it.

---

## The week

| Day | Folder | What you'll be able to do |
|---|---|---|
| Mon | `day-1/` | Attribute a bad answer to exactly one of the seven stations |
| Tue | `day-2/` | Write relevance judgments, and measure how much you disagree with yourself |
| Wed | `day-3/` | Implement recall, nDCG and MRR, and say what each one hides |
| Thu | `day-4/` | Build a retriever in forty lines and get a number for it |
| Fri | `milestone/` | Ship the eval set and the baseline, then defend both |

Each day folder has its own `README.md`. Start there, every time.

---

## How a day goes

1. **Read** the day's README. All of it, before writing anything.
2. **Read the linked articles.** Not summaries of them.
3. **Predict before you run.** Every lab has a *Predict first* block. Write your guess
   down. The gap between your guess and the number is the lesson, and it does not exist
   if you skip this.
4. **Write** the exercises, in order — they build.
5. **Test** with `pytest week-01/day-N -v`.
6. **Log** what stuck you in `logs/stuck-log.md`, and your five numbers in
   `logs/signal-log.md`.
7. **Commit and push.** Every day.

Day 1 has no tests. That is deliberate and it is explained there.

---

## What is different about this course

In a programming course the tests tell you whether you are right. Here they mostly cannot.
`pytest` can check that your nDCG matches the definition. It cannot check whether the
thing you measured was worth measuring, and it certainly cannot check whether your
judgments describe what a user wants.

| | Checks | Automatic |
|---|---|---|
| `pytest week-01` | the metric implementations | yes |
| The milestone rubric | that all seven stations were run, and the numbers are real | partly |
| **Friday's clinic** | whether you can find the failure under attack | no |

The third one is the real one.

---

## Milestone

An eval set of your own — twelve new queries over the shipped corpus, judged by hand — a
self-agreement number, and the day-4 baseline scored against it. Spec in
`milestone/README.md`. It must pass its tests **and** survive Friday's clinic, which is a
different and harder bar.

---

## What this week is not about

Building a retrieval system. Vector databases. Anything in the "not yet" column of
[`FENCE.md`](FENCE.md).

You will finish this week with a system that is worse than a search box from 1998, and
that is correct. A bad retriever whose failures you can enumerate beats a good one you
cannot measure, and it is not close — the second kind stops improving the moment it stops
being obviously broken, which is usually about a week after launch.
