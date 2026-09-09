# Day 1 — Text as geometry

> **By the end of today** you can put text in a vector space, and prove that the
> vocabulary gap is a property of that space rather than a tuning failure.

---

## Read first

- [ ] [**One axis per word**](../../content/week-05/day-1/one-axis-per-word.md) — 25 min
- [ ] [**Cosine, and why not the dot product**](../../content/week-05/day-1/cosine.md) — 20 min

---

## Predict first

Two chunks about rate limiting, one using the phrase `too many requests` and one using
`rate limiting`, sharing no other content words.

**What is their cosine similarity in a one-axis-per-word space?** Write a number.

---

## The lab

`similarity.py`. Week 3's `analyze` and week 4's `section_corpus` are importable.

```python
build_vocabulary(chunks)     count_matrix(chunks, ids, vocab)     idf_weights(X)
weight(X, idf)               l2_normalise(v)                      cosine(a, b)
query_vector(query, vocab, idf)                                   nearest(matrix, ids, q, k)
sparsity(matrix)
```

Build the term-position lookup **once**, outside the loop. `vocab.index(term)` inside a
double loop is a linear scan of four thousand strings per token, and it turns a
one-second lab into a five-minute one.

Then the last two tests, which are the day.

```bash
pytest week-05/day-1 -v
```

---

## The written exercise

`week-05/day-1/geometry.md`, one page.

1. Your predicted cosine and the actual one
2. The matrix is 266 × 4,273 and **97.5% zero**. Compute how many bytes that is dense, and
   how many the non-zero entries would need. Then say why nobody stores it dense
3. `cosine` and week 3's `b` are both length normalisation. Write a paragraph on how they
   differ — one is a parameter and one is not, and that is a real design difference
4. **The one that matters.** State, in one sentence, why no weighting scheme can bridge
   `31-day` and `monthly` in this representation. Then predict what would have to change

---

## Deep track

> The idf here is computed over chunks; week 3's was over documents. Compute both for the
> whole vocabulary and plot one against the other. Find the terms that moved most, explain
> why, and say which of the two is the right denominator — the question is not rhetorical
> and the answer depends on what you think a "document" is.

---

## Log

`logs/stuck-log.md` and `logs/signal-log.md`.
