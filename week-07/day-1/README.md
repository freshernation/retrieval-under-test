# Day 1 — Reranking

> **By the end of today** you can compute what a reranker could possibly buy, and you will
> have built one that buys none of it.

---

## Read first

- [ ] [**What a reranker is**](../../content/week-07/day-1/what-a-reranker-is.md) — 25 min
- [ ] [**Better, not merely different**](../../content/week-07/day-1/better-not-different.md) — 25 min

---

## Predict first

Answer recall at k=5 is 0.737. Over a ten-deep shortlist it is 0.895.

1. **How much can a perfect reranker gain?**
2. **How much will yours gain?** Commit to a number.

---

## The lab

`rerank.py`.

```python
document_frequencies(chunks)   idf(term, df, n)   features(query, text, df, n)
feature_score(...)             prior(shortlist)   rerank(query, shortlist, ..., alpha)
ceiling(shortlist, chunks, query, depth)
```

Write `ceiling` **first**. It is three lines and it tells you whether the rest of the day is
worth doing — if the shortlist's recall equals your recall at k, reordering cannot help and
you can stop.

Then sweep `alpha` from 0 to 1 and read the whole curve, not the best point.

```bash
pytest week-07/day-1 -v
```

---

## The written exercise

`week-07/day-1/rerank.md`, one page.

1. Your two predictions and the results
2. The alpha sweep, all six values, at k=1, 3 and 5
3. **Why it loses.** Three features against BM25 plus RRF. Write the paragraph — it is about
   what a relevance model is and where one comes from, not about your code
4. The ceiling is sixteen points and nothing you wrote touched it. Name three things that
   might, and say what evidence would tell you which to try

---

## Deep track

> Fit the feature weights instead of guessing them: hold out half your dev queries, grid or
> gradient-fit the three weights on the other half, and evaluate. You are doing
> learning-to-rank with three features and ten training queries. Report what you get, and
> then say what the sample size means for the result.

---

## Log

`logs/stuck-log.md` and `logs/signal-log.md`.
