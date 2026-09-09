# Day 1 — The unit of retrieval changes

> **By the end of today** you can chunk a corpus, and you can demonstrate that your
> evaluation is incapable of telling you whether it worked.

---

## Read first

- [ ] [**Why chunk at all**](../../content/week-04/day-1/why-chunk-at-all.md) — 25 min
- [ ] [**The number with no source**](../../content/week-04/day-1/the-number-with-no-source.md) — 25 min

---

## Predict first

You are about to cut ten documents into 137 pieces and retrieve those instead.

1. What will happen to ndcg@3, measured against your existing document-level judgments?
2. Is there any chunk size at which an **answer** could disappear from the corpus entirely?

Write both down. The second one is the day.

---

## The lab

`windows.py`.

```python
split_words(text)                   fixed_windows(text, size, overlap)
chunk_id(doc_id, index)             parent(chunk_id)
chunk_corpus(documents, size, overlap)
to_documents(ranked_chunks, k)      coverage(documents, chunks)
```

`chunk_id` and `parent` look like plumbing and are station 1 surviving into station 2. A
chunk with no route back to its document cannot be cited, cannot be attributed, and cannot
be checked against week 2's supersession graph — all of which you built and would silently
lose here.

Then the last three tests, in order. Do not skip to the third.

```bash
pytest week-04/day-1 -v
```

---

## The written exercise

`week-04/day-1/what-the-metric-cannot-see.md`, one page.

1. Your two predictions and what happened
2. The 200/0 versus 200/25 comparison. State, in your own words, the **two separate**
   failures of the document-level evaluation. They are not the same failure
3. Take the query whose answer was destroyed. Write down every stage of the pipeline that
   could, in principle, have recovered it — and cross off the ones that cannot. You should
   end with none
4. **The uncomfortable one.** You have now made three weeks of decisions using
   document-level judgments. Which of them would you re-examine, and why?

---

## Deep track

> `to_documents` collapses a chunk ranking into a document ranking by first occurrence.
> There are at least three other reasonable rules — highest chunk score, sum of chunk
> scores, count of chunks above a threshold. Implement two, measure whether the
> document-level numbers change, and say what that tells you about how much information
> was in the aggregation choice all along.

---

## Log

`logs/stuck-log.md` and `logs/signal-log.md`.
