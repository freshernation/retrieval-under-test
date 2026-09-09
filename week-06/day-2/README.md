# Day 2 — Fusing by rank

> **By the end of today** you can implement reciprocal rank fusion, and you can say what
> its constant actually controls.

---

## Read first

- [ ] [**Reciprocal rank fusion**](../../content/week-06/day-2/reciprocal-rank-fusion.md) — 25 min · source: [Cormack, Clarke & Buettcher 2009](https://plg.uwaterloo.ca/~gvcormac/cormacksigir09-rrf.pdf)
- [ ] [**Another default from somebody else's corpus**](../../content/week-06/day-2/another-default.md) — 20 min

---

## Predict first

RRF's constant `c` defaults to 60 everywhere, from a 2009 paper.

**What does `c` control?** And: **at c = 60, how many times more does first place count
than tenth?** A number.

---

## The lab

`fuse.py`.

```python
ranks(ranking, depth)        rrf(rankings, k, c, weights, depth)
rrf_scores(...)              contribution(position, c)       flattening(c, positions)
```

Ranks are **1-based**. Zero-based first place gives it the same weight as `c` alone, which
shifts every score and is invisible in the output.

Write `flattening` early — it turns `c` from a magic number into a ratio you can state, and
the answer to this morning's second question is **1.15**.

```bash
pytest week-06/day-2 -v
```

---

## The written exercise

`week-06/day-2/fusion.md`, one page.

1. Your two predictions and the answers
2. The full sweep: `c` in 1, 10, 20, 60, 200 against k in 3, 5, 10. Twelve numbers, and the
   oracle next to each column
3. **At k=5 every fusion loses to lexical alone** — every constant, every weighting,
   including one favouring lexical two to one. Write the paragraph explaining why mixing a
   weaker signal into a stronger one is not free
4. At k=10, `c = 60` captures none of the headroom and `c = 10` captures all of it. What
   would you have concluded if you had used the default and not swept?

---

## Deep track

> RRF ignores scores entirely, which is its strength and obviously discards information.
> Implement one score-aware fusion that is not naive — rank-biased score normalisation, or
> a weighted combination of per-query z-scores — and put it on the same table. Report
> whether the extra information bought anything, and be suspicious of a win on nineteen
> queries.

---

## Log

`logs/stuck-log.md` and `logs/signal-log.md`.
