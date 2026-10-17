# Day 4 — Shards, and the statistics they split

> **By the end of today** you can split the index into shards, search them in parallel,
> and get back exactly the whole index's ranking.

---

## Read first

- [ ] [**Every shard thinks it is the corpus**](../../content/week-14/day-4/every-shard-thinks-it-is-the-corpus.md) — 20 min

---

## Predict first

Four shards, each scoring with its own document counts and lengths.

**For how many of the 26 queries does the merged top ten differ from the whole index's?**

---

## The lab

`shards.py`.

```python
shard_of(chunk_id, n)   split(chunks, n)   build_shards(chunks, n, **options)
global_stats(shards, terms)   score_shard(shard, terms, stats)
scatter_gather(shards, query, k, shared=True)
```

```bash
pytest week-14/day-4 -v
```

---

## The written exercise

`week-14/day-4/shards.md`, one page.

1. Your prediction, and the answer
2. Pick one query and one chunk. Show its idf in its shard and in the whole index
3. Shared statistics cost a round trip. When would you pay it, and when not?
4. Week 12's tombstones and today's shards: say in two sentences why they are one lesson
