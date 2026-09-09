# Day 2 — Ground truth at the right granularity

> **By the end of today** you can detect a destroyed answer without running any retrieval,
> and you can compute how much overlap you actually need.

---

## Read first

- [ ] [**An eval set is a model of the thing you measure**](../../content/week-04/day-2/an-eval-set-is-a-model.md) — 25 min
- [ ] [**Overlap, and how much is enough**](../../content/week-04/day-2/overlap.md) — 20 min

---

## Read the spans first

```bash
python3 -c "
import raglab
for q in raglab.judgments.load():
    print(q.id, q.answer_spans or '(unanswerable)')"
```

Fifteen spans, written by hand, verbatim from the corpus. **Read all of them and disagree
with at least one.** A span that is too long makes chunking look worse than it is; one that
is too short makes it look better. Yours will need the same argument.

Notice `r11`'s: `Although schemes are case- insensitive`, hyphenated across a line break in
RFC 3986 and still hyphenated after extraction. Week 2's damage, unrepaired, now
load-bearing in the ground truth.

---

## Predict first

At 200 words with no overlap, one query's answer is destroyed. **What is the smallest
overlap that saves it?** A number, before you compute it.

---

## The lab

`spans.py`. Day 1's `chunk_corpus` is importable.

```python
carrying_chunks(chunks, query)      survives(chunks, query)
broken_by(chunks, queries)          answer_recall_at_k(ranked, chunks, query, k)
mean_answer_recall(rankings, chunks, queries, k)
smallest_overlap_that_saves(documents, query, size)
```

`broken_by` is the important one and it is six lines. **It needs no index, no queries
executed, and no model** — one pass over the chunk texts, catching the one failure nothing
downstream can repair.

```bash
pytest week-04/day-2 -v
```

---

## The written exercise

`week-04/day-2/spans.md`, one page.

1. The span you disagree with, and what you would write instead. Then: does your version
   change any result from today?
2. Your predicted overlap and the computed one
3. `answer_recall_at_k` is **binary per query** — the context either contains the answer or
   it does not. Argue against that design for a paragraph, properly, then say whether you
   are convinced
4. **Add answer spans to four of your own queries.** Then run `broken_by` over your week-3
   configuration and report what you find. If it is nothing, say what that does and does
   not prove

---

## Deep track

> Answer spans are one form of finer-grained ground truth and they have a specific
> weakness: they reward a chunk for *containing* the string, not for being usable. Construct
> a chunk from this corpus that contains a span and would still produce a wrong answer, and
> say what a better ground truth would have to record.

---

## Log

`logs/stuck-log.md` and `logs/signal-log.md`.
