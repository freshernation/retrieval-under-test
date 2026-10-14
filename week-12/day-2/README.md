# Day 2 — Embedded by which model

> **By the end of today** you can say what a re-ingest has to embed again, and why the
> chunk you add to a dense index is not the chunk a rebuild would have made.

---

## Read first

- [ ] [**Embedded by which model**](../../content/week-12/day-2/embedded-by-which-model.md) — 25 min

---

## Predict first

RFC 8259 is a revision of RFC 7159: the same specification, with corrections. You
fingerprint every chunk of both.

**How many of RFC 8259's 21 chunks can reuse an embedding you already have?**

---

## The lab

`refresh.py`.

```python
fingerprint(text)            diff(old, new)            reusable(old, new)
unseen_terms(retriever, chunks)                        fold_in(retriever, texts)
Folded(retriever, new_chunks).search(query, k)         agreement(a, b)
```

The setting is the corpus as it stood before its two newest documents, RFC 8259 and RFC
8615, and then their arrival. `fold_in` embeds a chunk exactly as week 5 embeds a query —
which is the point: the new chunk gets the old model.

```bash
pytest week-12/day-2 -v
```

---

## The written exercise

`week-12/day-2/refresh.md`, one page.

1. Your prediction and the answer. Then: name a kind of corpus change where fingerprinting
   saves nearly everything
2. `diff` says 39 chunks were added and `reusable` says 2 of them were not really new.
   Which of the two would you bill an embedding budget from, and why are they different
   questions?
3. 161 terms the old basis has never seen. Pick three from `unseen_terms` and say what a
   query using one of them can and cannot match
4. **Five of twenty lists agree.** State what you may and may not conclude, using week 9's
   arithmetic on how many queries a difference needs
5. The system you evaluated in week 9 and the system running after the first update are
   two retrievers. Write the rule for when an eval has to be re-run

---

## Deep track

> Do the same for the approximate index. Build week 5's IVF on the old vectors, insert the
> new ones into the nearest existing list without moving a centroid, and compare ANN recall
> against an index clustered on everything, at `nprobe` 1, 2 and 4 and at 8 and 16
> clusters. The result is not the one the textbook predicts, and the list sizes say why.

---

## Log

`logs/stuck-log.md` and `logs/signal-log.md`.
