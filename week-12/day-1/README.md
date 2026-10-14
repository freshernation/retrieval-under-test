# Day 1 — The dead still vote

> **By the end of today** you can take a document out of an index two ways, and say what
> the cheap one costs with a number.

---

## Read first

- [ ] [**The dead still vote**](../../content/week-12/day-1/the-dead-still-vote.md) — 25 min

---

## Predict first

Two RFCs in the corpus have been obsoleted. You mark their 28 chunks as deleted and filter
them out of every result.

**For how many of the twenty dev queries is the top ten now different from the top ten of
an index built without those chunks?** Write a number down.

---

## The lab

`liveindex.py`.

```python
LiveIndex(documents, **options)
    .add(doc_id, text)      .remove(doc_id)      .tombstone(doc_id)      .compact()
    .doc_ids   .lengths   .dead   .debt   .n_documents   .average_length
    .postings(term)   .term_frequency(term, doc_id)   .document_frequency(term)

drift(index, reference, queries, k, search)
```

`LiveIndex` reads like week 3's `Index`, so week 3's `search` runs on it unchanged. Do not
subclass `Index` — it was built to be built once, and the thing it does not keep is the
thing `remove` needs.

```bash
pytest week-12/day-1 -v
```

---

## The written exercise

`week-12/day-1/liveindex.md`, one page.

1. Your prediction, and the answer at depths 1, 5 and 10
2. `json` has document frequency 32 in one index and 16 in the other. Work out what that
   does to its idf, and say which way it moves the score of a live chunk about JSON
3. **No top result changed.** Write the paragraph you would send to somebody who checked
   three queries by eye after the delete and reported that everything was fine
4. Debt is 0.105 and drift at depth ten is 0.40. Name a deletion that would give high debt
   and almost no drift, and one that would give the opposite
5. Your compaction rule: the trigger, and what it costs when it fires

---

## Deep track

> Tombstone chunks one document at a time, in three different orders, and plot drift
> against debt for each. If the curves differ — they will — say what property of a document
> predicts how much damage its tombstone does. Then propose a number better than debt for
> the dashboard, and say what it costs to compute.

---

## Log

`logs/stuck-log.md` and `logs/signal-log.md`.
