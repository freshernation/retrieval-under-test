# Day 4 — The loop

> **By the end of today** you can tell a loop's progress from its motion, and you can price
> the difference.

> **Deep track** — the whole week.

---

## Read first

- [ ] [**Three things, none of them the model**](../../content/week-11/day-4/none-of-them-the-model.md) — 25 min
- [ ] [**Churn is not progress**](../../content/week-11/day-4/churn-is-not-progress.md) — 20 min

---

## Predict first

A loop that retrieves, checks its confidence, rewrites and tries again, capped at three
iterations.

**Draw the histogram you expect** — how many queries stop at 1, 2 and 3 iterations. Commit
to it before the lab.

---

## The lab

`loop.py`.

```python
Run(query_id, context, retrievals, confidences, shortlists)   .iterations   .capped(max)
Loop(shortlist, build_context, rewrite, stop_at, max_iters).run(query_id, query_text)
histogram(runs)      cost_multiple(runs)      churn(run)
loop_report(runs, answered, max_iters)
```

Two details decide whether the loop is honest. Score the **original** query against each
context, not the rewritten one — otherwise the loop grades its own homework. And keep the
**best** context, not the last; the last is the one that failed to clear the bar.

```bash
pytest week-11/day-4 -v
```

---

## The written exercise

`week-11/day-4/loop.md`, one page.

1. Your predicted histogram and the measured one. Note the empty column
2. The answered rate at each of three stopping thresholds, next to the cost multiple
3. **`churn` counts 24 of 24.** Write the two sentences explaining why a no-progress
   detector based on *the candidate set changed* would never fire
4. `r10`'s confidence falls from 0.44 to 0.11 across twelve iterations. One paragraph on
   what, in this loop, could have noticed — and the honest answer about what you would have
   to add

---

## Deep track

> The loop's iteration count predicts answerability at strength 0.786, which clears week
> 9's floor and is the only thing the loop produced. Week 9 found two free signals at 0.83.
> Combine the iteration count with retrieval confidence, measure the combined AUC, and then
> apply the week-9 arithmetic: is the combination's gain over the best single signal larger
> than this set can resolve? Answer before deciding whether 2.2× is worth paying for a
> diagnostic.

---

## Log

`logs/stuck-log.md` and `logs/signal-log.md`.
