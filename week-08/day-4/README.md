# Day 4 — Refusal

> **By the end of today** you can make a system decline to answer, and you can price the
> decision rather than guessing at it.

---

## Read first

- [ ] [**Refusal has to be designed**](../../content/week-08/day-4/refusal-has-to-be-designed.md) — 25 min
- [ ] [**Whose decision is this**](../../content/week-08/day-4/whose-decision-is-this.md) — 20 min

---

## Predict first

You are about to add a confidence threshold below which the system declines.

**How many correct answers will you lose to remove the first wrong one?**

---

## The lab

`refuse.py`.

```python
confidence(query_text, context)     has_answer(query, context)     outcome(query, context, answer)
outcomes(answers, queries, contexts)
frontier(queries, contexts, thresholds)                            free_threshold(points)
separation(queries, contexts)
```

`confidence` uses **only what you would have at serving time**. Everything else measured
this week needs answer spans, and in production there are none — that asymmetry is the whole
difficulty of refusal.

The four-way table is the point. Counting refusals tells you nothing: refusing everything
and refusing nothing both produce a single number.

```bash
pytest week-08/day-4 -v
```

---

## The written exercise

`week-08/day-4/refusal.md`, one page.

1. Your prediction and the answer — which is **zero**, up to a threshold of 0.55
2. The full frontier: eight thresholds, four counts each. Mark the free region and the point
   where the exchange rate turns
3. **The overlap.** Minimum confidence when the answer was present: 0.56. Maximum when it was
   absent: 0.78. Write the paragraph explaining why no threshold separates them, and what
   that means for anyone promising a system that "knows when it does not know"
4. Choose a threshold, and justify it with a sentence about **consequences** rather than
   about the metric. Then name the person who should actually be making that choice

---

## Deep track

> The overlap is a property of *this* signal. Build a better one from what is available at
> serving time — the retriever's score margin, the number of distinct documents in the
> context, the fraction of query terms unmatched — and measure whether any of them separates
> the two populations. This is week 11's routing problem, and finding out now whether the
> signal exists at all is worth a great deal.

---

## Log

`logs/stuck-log.md` and `logs/signal-log.md`.
