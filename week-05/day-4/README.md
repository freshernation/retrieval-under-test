# Day 4 — Not looking at everything

> **By the end of today** you can build an approximate index, and you can explain why its
> reported recall is not the recall your users experience.

---

## Read first

- [ ] [**Avoiding the scan**](../../content/week-05/day-4/avoiding-the-scan.md) — 25 min
- [ ] [**Two recalls, multiplied**](../../content/week-05/day-4/two-recalls.md) — 20 min

---

## Predict first

An approximate index with **ANN recall 0.53** — it finds about half of what an exhaustive
search would.

**What happens to answer recall?** Your dense retriever is at 0.89. Write a number.

---

## The lab

`ann.py`.

```python
kmeans(D, n_clusters, seed)      IVF          build_ivf(D, ids, n_clusters, seed)
brute_force(D, ids, q, k)        search_ivf(ivf, q, k, nprobe)
ann_recall(approx, exact)
```

Seed the clustering. An index that reshuffles between builds makes two runs of the same
configuration disagree, and you will spend a day on it.

Count the **centroid** comparisons as well as the vector ones. Leaving them out is how an
index reports a saving it did not make — and today's last test shows this index doing more
work than brute force.

```bash
pytest week-05/day-4 -v
```

---

## The written exercise

`week-05/day-4/approximate.md`, one page.

1. Your predicted answer recall at ANN recall 0.53, and the real one
2. The full sweep: nprobe against ANN recall, comparisons, and answer recall
3. **The compounding.** Write the two-sentence explanation you would give someone who says
   "our vector database has 95% recall, so we're fine"
4. Cluster sizes here run from 2 to 34. Explain why that makes probing one list
   unpredictable, and name what a more sophisticated index does about it

---

## Deep track

> Implement a second structure — a random-projection LSH index, or a small navigable-graph
> search — and put both on the same axes as Thursday's frontier: ANN recall against
> comparisons. Then answer the question the frontier makes obvious: at 266 vectors, is
> either of them worth having?

---

## Log

`logs/stuck-log.md` and `logs/signal-log.md`.
