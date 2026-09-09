# Day 3 — The window is a budget

> **By the end of today** you can size a context window deliberately, and you will know
> what fraction of it is doing any work.

---

## Read first

- [ ] [**k was never a budget**](../../content/week-07/day-3/k-was-never-a-budget.md) — 25 min
- [ ] [**Answer density**](../../content/week-07/day-3/answer-density.md) — 20 min

---

## Predict first

1. **How many words is `k = 5` on your corpus?** A range, not a number.
2. At a budget of 800 words, **what fraction sits in an answer-bearing chunk?**

---

## The lab

`window.py`.

```python
word_count(text)     truncate_to(text, words)     pack(ranked, chunks, budget, truncate)
used_words(texts)    answer_density(texts, query) answered(texts, query)
budget_curve(ranked, chunks, query, budgets, truncate)
```

`pack` **stops** at the first chunk that does not fit — it does not skip ahead to a smaller
one. Skipping silently reorders the window by size, so it no longer reflects the ranking you
spent six weeks building.

Then the truncation pair: it *helps* at a tight budget, and it can destroy an answer span.
Both are true and both are tests.

```bash
pytest week-07/day-3 -v
```

---

## The written exercise

`week-07/day-3/budget.md`, one page.

1. Your two predictions and the results
2. The full budget curve, with and without truncation. Eight rows, three columns
3. **Truncation.** It nearly doubles `answered` at 200 words and it can cut an answer span
   in half. State the rule you would adopt, and the condition under which you would change it
4. Density falls from 0.31 at 400 words to 0.10 at 2,000. Write the sentence you would put
   in front of somebody paying for those tokens

---

## Deep track

> `answer_density` counts a chunk carrying the span as entirely useful, which it is not.
> Build a tighter bound — the words within some distance of the span, say — and recompute
> the curve. Then say what the gap between the two numbers represents, and which one you
> would report.

---

## Log

`logs/stuck-log.md` and `logs/signal-log.md`.
