# Day 1 — Rewriting the query

> **By the end of today** you can rewrite a query three ways, and you will know what each
> one does to each query family.

> **Deep track** — the whole week.

---

## Read first

- [ ] [**The technique aimed at the failure**](../../content/week-11/day-1/aimed-at-the-failure.md) — 25 min
- [ ] [**Query drift**](../../content/week-11/day-1/query-drift.md) — 20 min

---

## Predict first

Week 10's attribution named two station-4 failures: `r19` and `r20`, both paraphrases, both
flagged by week 6 as retrieved by nothing.

**Will query rewriting fix them?** Yes or no, in writing. Then: **which query family will
rewriting hurt most?**

---

## The lab

`rewrite.py`.

```python
term_idf(index, term)            drop_low_idf(index, query_text, keep)
prf_terms(index, chunks, shortlist, query_text, n)
expand(query_text, terms)        variants(index, chunks, query_text, shortlist)
rewrite_report(before, after)
```

**The rule, and it is the integrity of the day:** no rewrite rule derived from a failing
query. A synonym dictionary built by looking at what failed is the eval set leaking into
the system, it will score beautifully, and you will never find out. Everything here comes
from the index or from the query.

```bash
pytest week-11/day-1 -v
```

---

## The written exercise

`week-11/day-1/rewrite.md`, one page.

1. Your two predictions, and the measured answers
2. The per-family table for the expansion. Two families up, three down, one unchanged
3. **The net delta is -0.05 and it is the least useful number in the report.** Write the
   paragraph you would send to somebody who had quoted it
4. `r19`'s feedback terms are `web accessed their sites rec`. Explain in three sentences
   why pseudo-relevance feedback cannot fix a query it did not already half-answer

---

## Deep track

> `prf_terms` ranks by `count × idf` over the top three chunks. Both numbers are choices.
> Sweep the feedback depth (1, 3, 5, 10) and the term count (2, 5, 10), report the grid, and
> then apply week 9's arithmetic: with 20 queries and an MDE of 0.1003, how many cells of
> that grid are distinguishable from each other? The answer is a number and it is small.

---

## Log

`logs/stuck-log.md` and `logs/signal-log.md`.
