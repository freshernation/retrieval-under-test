# Day 3 — BM25

> **By the end of today** you have the strongest lexical retriever there is, and you know
> which of week 1's four defects it does not touch.

---

## Read first

- [ ] [**Three ideas and one formula**](../../content/week-03/day-3/three-ideas-and-one-formula.md) — 30 min · sources: [Robertson & Zaragoza §3](https://www.staff.city.ac.uk/~sbrp622/papers/foundations_bm25_review.pdf)
- [ ] [**What BM25 still cannot do**](../../content/week-03/day-3/what-bm25-cannot-do.md) — 20 min

---

## Predict first

Week 1's baseline gets ndcg@3 of 0.651 on `dev`.

**What will BM25 get?** One number. And: **how many of the nine answerable queries will
improve?**

The second number is the interesting one and almost nobody guesses it correctly.

---

## The lab

`bm25.py`. Day 2's `Index` is importable.

```python
idf(document_frequency, n_documents)      saturate(tf, k1)
length_norm(doc_length, average_length, b)
score_term(tf, df, n, doc_length, avg_length, k1, b)
score(index, query, doc_id, k1, b)        search(index, query, k, k1, b)
```

Write `idf` first and print it for `status` and `429`. **0.047 against 1.992** — forty
times the weight, derived from the corpus rather than guessed by a list. That is Monday's
stopword problem solved properly, and it is one logarithm.

Then `score_term`, and get the normalisation in the right place: **in the denominator,
multiplied by k1**, not applied to the whole term. Getting this wrong still produces a
working retriever with slightly wrong behaviour, which is the worst kind of bug.

```bash
pytest week-03/day-3 -v
```

---

## The written exercise

`week-03/day-3/what-moved.md`, one page.

1. Your two predictions and the results
2. **The three queries that improved, and why each one did.** Use `explain()` from week 1
   and `idf` from today. Each has a different reason
3. **The six that did not.** Four of them were already perfect. Two were not, and are still
   not. Name them and say what is wrong — the answer is not in this week
4. In week 1 you named four defects and ranked them by expected cost. BM25 fixes three.
   Which one survives, and has your ranking changed?

Question 4 is week 5's motivation and you should write it down now, while it is still your
own observation rather than something you were told.

---

## Deep track

> BM25 sums per-term scores independently — a bag of words with weights. Construct a query
> against this corpus where that independence assumption is clearly wrong, run it, and
> describe what a scorer that knew about term dependence would have to do differently.
> Then find out what the standard answer to this is called and who proposed it.

---

## Log

`logs/stuck-log.md` and `logs/signal-log.md`.
