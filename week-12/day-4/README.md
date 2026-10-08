# Day 4 — What expires

> **By the end of today** every claim in your report is marked durable, re-measure
> annually, or already expired — and you can defend each mark.

**No lab.**

---

## Read first

- [ ] [**What expires and what does not**](../../content/week-12/day-4/what-expires.md) — 25 min
- [ ] [**The handover**](../../content/week-12/day-4/the-handover.md) — 20 min

---

## Predict first

**Which of your findings expires first?** Name one, and say what would have to change for it
to become false.

---

## The work

### 1 · Mark every claim

Three marks and no fourth:

| mark | means |
|---|---|
| **durable** | about information retrieval. True in ten years |
| **re-measure annually** | about your corpus, your traffic, or your costs. Will drift |
| **expired** | about a model version, a price, or a library API. Already stale |

A claim you cannot mark is a claim you do not understand well enough to have written.

### 2 · The re-measurement list

For every *re-measure annually* claim: the command, the eval set, and the number to compare
against. If it takes more than a paragraph, nobody will do it, and an unmeasurable
commitment is worse than none because it reads as a plan.

### 3 · The handover note

One page, for the person who inherits this system when you do not work here.

- what the eval set is, how it was built, and what it cannot see
- the three numbers to watch and the gate that guards them
- **the two empty stations**, so they do not spend a month on the prompt
- the failures with no card, so they are not surprised by them
- what you would do with one more week

---

## The written exercise

`week-12/day-4/expiry.md`.

1. Your predicted first-to-expire and your considered answer
2. The full marked claim list. Count each mark — if nothing is *expired*, you have not
   looked
3. The re-measurement list, with commands
4. The handover note

---

## Deep track

> Go back to week 1's reading list and check every source: is the URL live, has the
> document been superseded, has the number you quoted changed? That is nine weeks of
> evidence rot measured rather than assumed. Week 10 found a source that went unreachable
> *between* being read and being checked, and that is the point — `tools/check_sources.py
> --check-urls` is the course's own answer and it only checks that a URL resolves.

---

## Log

`logs/stuck-log.md` and `logs/signal-log.md`.
