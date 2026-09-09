# Day 1 — A bigger instrument, and the obvious fusion

> **By the end of today** you can say why adding two retrievers' scores together is not
> fusion, and you will have an eval set that can measure what this week is about.

---

## Read first

- [ ] [**Growing an eval set is a new instrument**](../../content/week-06/day-1/a-new-instrument.md) — 20 min
- [ ] [**Two kinds of number**](../../content/week-06/day-1/two-kinds-of-number.md) — 25 min

---

## Predict first

BM25 scores on this corpus run from about 3 to about 33. Cosines run from about 0.2 to
about 0.8.

**What happens if you add them?** One sentence, before the lab.

---

## The lab

`normalise.py`. From today the labs load the extended query set:

```python
queries = raglab.judgments.load(file="queries-extended.yml")
```

```python
min_max(scores)      z_score(scores)      combine(a, b, weight)
ranked(scores, k)    top_gap(scores)
```

Write `top_gap` before `min_max` and use it on a query that retrieves well and one that
retrieves badly. **Min-max maps both to a top score of exactly 1.0**, and what it destroys
is the only signal that would have told you which retriever to trust.

Then the last two tests.

```bash
pytest week-06/day-1 -v
```

---

## The written exercise

`week-06/day-1/scales.md`, one page.

1. Your prediction and the result. Raw-sum fusion is *identical* to lexical alone at every
   k — write the sentence explaining why to somebody who has not seen the score ranges
2. `combine` treats a missing score as 0.0. After min-max, 0.0 is the **worst** result
   rather than "not measured". Give a concrete example from your own run where that
   penalises a chunk unfairly
3. **The instrument.** You now have two query files. Write two sentences on why the old one
   was not edited, and what would have gone wrong if it had been
4. Your week-3 milestone asked for thirty dev queries. How many do you have? If fewer than
   nineteen, say what today's results are worth

---

## Deep track

> `top_gap` is one confidence signal. Design two more that need only the retriever's own
> output — no judgments — and check whether any of them predicts, per query, which of your
> two retrievers got the answer. You are building a router by hand; week 11 does it
> properly, and knowing now whether the signal exists at all is worth a great deal.

---

## Log

`logs/stuck-log.md` and `logs/signal-log.md`.
