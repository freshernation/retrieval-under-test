# Day 1 — What a RAG answer actually is

> **By the end of today** you can look at a wrong answer and say which of seven stages
> produced it, without touching the system.

---

## Read first

- [ ] [**What a RAG answer actually is**](../../content/week-01/day-1/what-a-rag-answer-is.md) — 20 min
- [ ] [**The seven stations**](../../content/week-01/day-1/the-seven-stations.md) — 25 min

---

## There are no tests today

Deliberately. Today's work is a judgment about a failure, and there is nothing assertable
about it — a green test on day 1 would teach you that green means good, which is the
single belief this course exists to remove.

Tomorrow has tests. Today has a worksheet and it is marked by a person.

---

## The exercise

`NOTES.md` in this folder, prefilled with **eight bad answers** from a system built over
the sample corpus. For each one:

1. Name the station that failed — **exactly one**, the first one in order 1 → 7
2. Say what you would look at to confirm it, before changing anything
3. Say what a person who had not read this course would have changed instead

The third column is the point of the exercise. Six of the eight have an obvious wrong fix
that a competent engineer would reach for, and five of those wrong fixes are at station 6.

Take an hour. Do not look at the sample corpus first — you are practising the diagnosis
you make when somebody hands you a broken system, and you never get to read the corpus
first in real life either.

Then read the corpus, and go back and change your answers. Note which ones you changed.

---

## Predict first

Before you start: **which station do you think produces the most failures in production
RAG systems?** Write your guess and one sentence on why.

Come back to it in week 8.

---

## The thing worth arguing with

The stations are ours. They are not from a paper and they are not standard vocabulary —
nobody else calls them this, and if you say "a station 4 failure" in an interview you will
get a blank look. What they are is an *order to walk in*, and the value is almost entirely
in the walking rather than in the names.

Argue with the ordering if you like. The one thing that is not negotiable is that a
diagnosis starts at the corpus and moves forward, because every station's output is the
next one's input, and fixing a stage downstream of the break is how you spend three weeks
tuning a reranker over documents that were never ingested.

---

## Log

`logs/stuck-log.md` and `logs/signal-log.md`. Start both today even though there is little
to write — a log begun on day 4 is a log with a hole in it where week 1 was.
