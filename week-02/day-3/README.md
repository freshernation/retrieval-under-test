# Day 3 — Near-duplicates, and what they mean

> **By the end of today** you can find the duplicated documents in a corpus, and say why
> deleting one of them would break a query you have already written.

---

## Read first

- [ ] [**Finding what is repeated**](../../content/week-02/day-3/finding-what-is-repeated.md) — 25 min
- [ ] [**Duplication is not a defect**](../../content/week-02/day-3/duplication-is-not-a-defect.md) — 20 min

---

## Predict first

Two documents in this corpus are near-duplicates of each other, and so are two others.
Both pairs stand in **exactly the same relationship**: the newer obsoletes the older.

Write down: **what similarity threshold would find both pairs and nothing else?**

---

## The lab

`dedupe.py`. Day 2's `clean` is importable.

```python
words(text)              shingles(text, k=5)        jaccard(a, b)
minhash(shingle_set, n=128, seed=0)                 estimate_jaccard(sig_a, sig_b)
near_duplicate_pairs(documents, threshold=0.5)      longest_shared_run(a, b)
```

Use `zlib.crc32` in `minhash`, not Python's `hash()`. Python salts string hashing per
process, so a signature built with `hash()` differs between runs and a deduplication index
built on it silently stops matching after a restart. That is a real bug people ship.

Then run `near_duplicate_pairs` on the raw corpus and on your cleaned corpus from
yesterday, and compare the counts. **That difference is the answer to yesterday's
question**, and it is not the answer anyone expects.

Then `longest_shared_run` on each pair, and read what comes back. Same measurement,
opposite meanings.

```bash
pytest week-02/day-3 -v
```

---

## The written exercise

`week-02/day-3/duplicates.md`, one page.

1. The pairs above 0.05 on the raw corpus and on the cleaned one. Explain the difference in
   two sentences
2. Your predicted threshold from this morning, and why no threshold works
3. **For each of the two supersession pairs, argue for deleting the older document, then
   argue against.** Both arguments, properly, before you conclude. One of them is refuted
   by a query in your own held-out split; find it and name it
4. One paragraph: what would you have to know about the corpus, that similarity cannot
   tell you, to make this decision correctly?

Point 4 is tomorrow.

---

## Deep track

> MinHash estimates 0.500 against an exact 0.547 at 128 permutations. Plot estimation
> error against `n` for n in 16, 64, 128, 512, 2048, averaged over several seeds. Then
> answer the question that actually matters: at what corpus size does exact pairwise
> Jaccard stop being affordable, and is your answer within an order of magnitude of the
> point where MinHash's error stops mattering?

---

## Log

`logs/stuck-log.md` and `logs/signal-log.md`.
