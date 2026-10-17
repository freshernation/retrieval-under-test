# Day 3 — A graph index, by hand

> **By the end of today** you have built an HNSW index and can say, with a number, the
> size below which it costs more than reading everything.

---

## Read first

- [ ] [**The graph and the scan**](../../content/week-14/day-3/the-graph-and-the-scan.md) — 25 min

---

## Predict first

266 chunks. To find the same top ten as a scan, 99 times in 100.

**How many distances does the graph compute per query?**

---

## The lab

`hnsw.py`.

```python
HNSW(M, ef_construction, seed)  .random_level  .search_layer  .add  .search  .distances
build(ids, D, M, ef_construction, seed)   brute_force(ids, D, q, k)   recall(approx, exact)
```

```bash
pytest week-14/day-3 -v
```

---

## The written exercise

`week-14/day-3/hnsw.md`, one page.

1. Your prediction, and the answer
2. Recall against distances per query, for four values of `ef`, as a table
3. Why does asking for perfect recall cost more than the scan?
4. At what corpus size would you switch from a scan? Say how you would decide
