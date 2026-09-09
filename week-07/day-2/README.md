# Day 2 — Redundancy

> **By the end of today** you can measure how much of a result set repeats itself, and you
> can explain why your metric does not care.

---

## Read first

- [ ] [**Five results, two documents**](../../content/week-07/day-2/five-results-two-documents.md) — 25 min
- [ ] [**A metric that cannot see it**](../../content/week-07/day-2/a-metric-that-cannot-see-it.md) — 20 min

---

## Predict first

Your top-5 contains **2.4 distinct documents** on average.

**What will MMR do to answer recall?** A number and a sign.

---

## The lab

`diversity.py`.

```python
similarity(a, b)          redundancy(ranked, chunks, k)     same_document_pairs(ranked, k)
distinct_documents(ranked, k)
dedupe(ranked, chunks, threshold)                            mmr(ranked, chunks, k, lam)
```

Run `dedupe` and notice how little it removes. **A tool that does nothing is not broken** —
it is telling you your problem is not the one it solves, and here the redundancy is
different sections of one document rather than near-identical chunks.

Then MMR, and then the last two tests.

```bash
pytest week-07/day-2 -v
```

---

## The written exercise

`week-07/day-2/redundancy.md`, one page.

1. Your prediction and the result
2. Redundancy, same-document pairs and distinct documents at the baseline and at three MMR
   settings. Six numbers, and the recall next to each
3. **The uncomfortable paragraph.** Answer recall is identical for every diversity setting
   that does not also hurt. Explain why, in terms of what the metric asks
4. Write **two** queries for your own set whose answers need chunks from different
   documents. That is what would make this measurable, and it is the actionable output of
   the day

---

## Deep track

> Redundancy at the *chunk* level barely exists here; at the *document* level it is
> everywhere. Build a metric that captures what you actually mind — perhaps distinct
> documents per unit of context — and check whether any diversity setting improves it
> without costing recall. Then say whether the metric you invented is one you would defend.

---

## Log

`logs/stuck-log.md` and `logs/signal-log.md`.
