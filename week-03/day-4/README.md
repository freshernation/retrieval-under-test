# Day 4 — Tuning, and four reasons not to believe it

> **By the end of today** you can tune two parameters, and you can list the four ways your
> tuned number might be worthless.

---

## Read first

- [ ] [**Two numbers, eighteen points**](../../content/week-03/day-4/two-numbers-eighteen-points.md) — 25 min
- [ ] [**How big does an eval set have to be?**](../../content/week-03/day-4/how-big-does-an-eval-set-have-to-be.md) — 25 min

---

## Predict first

`k1=1.2, b=0.75` is the value in most of the literature and most production search
engines.

**Where does it place in a 45-point grid on this corpus?** Write a rank out of 45.

---

## The lab

`tuning.py`. Day 3's `search` is importable.

```python
grid_search(index, queries, metric, k1_values, b_values)
best(results)        spread(results)      rank_of(results, k1, b)
at_edge(k1, b)       looks(results)       moved_queries(index, queries, a, c)
```

`at_edge` is the most important function in the file, and the reason is in the docstring.

Run the grid, then read the four tests named `test_one_…` through `test_four_…` in order.
Then the last one, which is the uncomfortable part of the day.

**The grid runs on `dev`. Only on `dev`.** You will want to check the winner on `test`, and
today is the day that temptation is strongest. The log records it.

```bash
pytest week-03/day-4 -v
```

---

## The written exercise

`week-03/day-4/tuned.md`, one page.

1. Your predicted rank for the defaults, and the actual one
2. **The four warnings**, each in one sentence, with its number: the default's rank, the
   edge effect, the number of looks, and the fraction of queries the gain rides on
3. The optimum is a plateau running to k1 = ∞, which is to say *turn saturation off*.
   Write a paragraph on whether you believe that, what about this corpus might cause it,
   and what evidence would change your mind
4. **The honest one.** The tuned configuration also wins on the held-out split. Does that
   settle it? Answer in a paragraph, and the paragraph must address what you would have
   concluded if it had lost

---

## Deep track

> Repeat the grid search with a *bootstrap* at each point rather than a single score, and
> report the best configuration whose interval excludes every other configuration's. On
> nine queries you will find there is no such configuration, which is the correct answer
> and is worth being able to demonstrate rather than assert.

---

## Log

`logs/stuck-log.md` and `logs/signal-log.md`.
