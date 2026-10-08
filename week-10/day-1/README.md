# Day 1 — The mean is not the number

> **By the end of today** you can budget a pipeline per stage, in a unit that means the
> same thing on somebody else's machine.

---

## Read first

- [ ] [**The mean is not the number**](../../content/week-10/day-1/the-mean-is-not-the-number.md) — 25 min
- [ ] [**Count the work, not the seconds**](../../content/week-10/day-1/count-the-work-not-the-seconds.md) — 20 min

---

## Predict first

Two questions. Commit to both.

1. **How much more does the most expensive query in your eval set cost than the
   cheapest?** Write a factor down.
2. **Do expensive queries fail more often than cheap ones?** Yes or no.

---

## The lab

`latency.py`.

```python
work(index, query_text)        constant_work(n_chunks)      percentile(values, p)
spread(values)                 under_provision(values, p)
budget_report(measured, budget)              exceeds(report)
```

`work` is the whole idea: the sum of the document frequencies of the query's distinct
terms. It is what an inverted index actually does, it is identical on every machine, and it
is three lines.

```bash
pytest week-10/day-1 -v
```

Time the stages with a stopwatch too — you need to know your own slow stage. Just do not
put the number in the report.

---

## The written exercise

`week-10/day-1/latency.md`, one page.

1. Your two predictions and the measured answers
2. A per-stage budget for your pipeline, in work units, with one sentence per stage saying
   where the number came from. A stage with no budget is on this list too, with a reason
3. **Cost AUC is 0.417.** Write the two sentences you would say to somebody proposing to
   route expensive queries to a cheaper pipeline
4. The by-family cost table *looks* like a trend and the median split refutes it. Explain
   in three sentences why you believe the split and not the table

---

## Deep track

> `work` counts postings touched, which assumes the index is consulted once per distinct
> term and the whole postings list is read. Neither is quite true: a real engine skips
> blocks, and WAND-style pruning can stop early. Read the Lucene scoring docs, then write
> down what your count over-estimates and by roughly how much — and whether the
> over-estimate is uniform across queries. If it is not, your budget is wrong in a way
> that depends on the query.

---

## Log

`logs/stuck-log.md` and `logs/signal-log.md`.
