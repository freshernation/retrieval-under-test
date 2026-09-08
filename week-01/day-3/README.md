# Day 3 — The metrics, and what each one hides

> **By the end of today** you can implement recall, nDCG, MRR and average precision from
> the definitions, and say what each of them cannot see.

---

## Read first

- [ ] [**The metrics**](../../content/week-01/day-3/the-metrics.md) — 30 min · sources: [Järvelin & Kekäläinen on nDCG](https://dl.acm.org/doi/10.1145/582415.582418), [TREC](https://trec.nist.gov/pubs.html)
- [ ] [**Is that a real difference?**](../../content/week-01/day-3/is-that-a-real-difference.md) — 25 min

---

## Predict first

A retriever returns the three relevant documents for a query in positions 8, 9 and 10 out
of 10. Another returns them in positions 1, 2 and 3.

Write down, before the lab: **which metrics distinguish these two systems, and which give
them identical scores?** There are four metrics in the lab. Name them in two lists.

---

## The lab

`scoring.py`.

```python
grade(judgments, doc_id)              recall_at_k(ranked, judgments, k)
precision_at_k(ranked, judgments, k)  reciprocal_rank(ranked, judgments)
dcg_at_k(...)                         ndcg_at_k(...)
average_precision(ranked, judgments)  mean_over_queries(metric, rankings, judgments)
paired_bootstrap(scores_a, scores_b)
```

`raglab.metrics` already contains every one of these and you are writing them anyway. A
metric you have not implemented is a metric you will quote without knowing what it hides,
and each of these hides something specific and expensive.

From tomorrow, use `raglab.metrics`. It is the definition of record, and a milestone that
disagrees with it is wrong rather than interestingly different.

Read `test_precision_at_ten_is_capped_by_the_judgments` before you write
`precision_at_k`. Then write `paired_bootstrap` last and run
`test_a_one_query_win_on_eight_queries_is_not_a_result`.

```bash
pytest week-01/day-3 -v
```

---

## The written exercise

`week-01/day-3/metrics-choice.md`, half a page.

For each situation, name the metric you would report and the one you would refuse to
report, with one sentence each:

1. A support search box. The user reads the first result and nothing else
2. A legal discovery tool. Missing one relevant document is the failure that matters
3. A RAG pipeline that puts the top 5 chunks in a context window
4. A comparison of two rerankers, where both were given the same candidates

Then one paragraph: **which of these four would be badly served by every metric in
today's lab, and what would you actually need?**

---

## Deep track

> Implement `ndcg_at_k` with the *linear* gain `g` instead of `2**g - 1`, run both over
> the sample corpus, and say which ranking decisions change. Then find out which of the
> two the tools you have used report, and whether they say.

---

## Log

`logs/stuck-log.md` and `logs/signal-log.md`.
