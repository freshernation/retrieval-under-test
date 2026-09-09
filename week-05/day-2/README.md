# Day 2 — Changing the axes

> **By the end of today** you can build a dense representation from the corpus, watch the
> vocabulary gap close, and find the exact limit of doing it this way.

---

## Read first

- [ ] [**Factorising a corpus**](../../content/week-05/day-2/factorising-a-corpus.md) — 30 min
- [ ] [**How many dimensions**](../../content/week-05/day-2/how-many-dimensions.md) — 20 min

---

## Predict first

`too many requests` and `rate limiting` are exactly orthogonal in yesterday's space.

**What will their cosine be in 128 dimensions?** A number. And: **will `censorship` be near
`legal reasons`?**

The second question is the one to remember.

---

## The lab

`lsa.py`.

```python
decompose(W)              variance_kept(S, k)         dimensions_for(S, target)
embed_chunks(U, S, k)     embed_query(q, Vt, k)       neighbours(D, ids, q, k)
term_axes(Vt, vocab, axis, n)
```

Use `full_matrices=False`; the full version allocates a 4273×4273 matrix you will never
look at.

Then **print `term_axes` for the first three directions and read them.** They are not
concepts, they are not tidy, and the strongest direction on this corpus is essentially
"is this the cookies RFC". Seeing that is worth more than being told LSA finds topics,
because it does not.

```bash
pytest week-05/day-2 -v
```

---

## The written exercise

`week-05/day-2/axes.md`, one page.

1. Your two predictions and the results
2. `dimensions_for(S, 0.90)` returns 191, out of 266 chunks. What does that ratio tell you
   about how much redundancy there was to exploit? Would you expect it to be higher or
   lower on ten thousand chunks, and why?
3. Read the first three axes. Describe what each one appears to be about, then say why
   "appears to be about" is doing a lot of work in that sentence
4. **The limit.** `censorship` scores 0.00 against `legal reasons` — the same as sparse. In
   two sentences: why, and what a trained embedding model does differently

---

## Deep track

> Remove the largest singular direction entirely — embed with directions 1 to k rather than
> 0 to k — and re-measure. The first direction usually encodes "how long is this document"
> or "which document is this", and dropping it is a known trick. Report whether it helps
> here, and be suspicious of your own result on nine queries.

---

## Log

`logs/stuck-log.md` and `logs/signal-log.md`.
