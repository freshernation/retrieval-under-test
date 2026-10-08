# Day 2 — A hit rate is a claim about traffic

> **By the end of today** you can measure a cache honestly, which includes saying which
> number you assumed and what the cache is serving.

---

## Read first

- [ ] [**A hit rate is a claim about traffic**](../../content/week-10/day-2/a-hit-rate-is-a-claim-about-traffic.md) — 25 min
- [ ] [**The cached answer that outlives its correction**](../../content/week-10/day-2/the-cached-answer-that-outlives-its-correction.md) — 20 min

---

## Predict first

**Run a cache over your eval set and write down the hit rate you expect.**

Do this before the lab. It takes thirty seconds and the answer reframes the day.

---

## The lab

`caching.py`.

```python
cache_key(query_text)      distinct(texts)        LRU(capacity)
stream(ids, n, skew)       work_saved(hit_ids, costs)
replay(requests, costs, capacity)                 staleness(cached, fresh)
```

`LRU` is forty lines and it is what the service in front of your retriever is doing. Write
it rather than importing one — the FIFO-pretending-to-be-an-LRU bug is the one you will
meet in somebody else's code, and you will only recognise it if you have written the
correct version once.

```bash
pytest week-10/day-2 -v
```

---

## The written exercise

`week-10/day-2/caching.md`, one page.

1. Your predicted hit rate on the eval set, and why it is zero
2. The three hit rates from the three skews, each labelled with the assumption that
   produced it. Then: **one counter you could add to a real system that would settle it**,
   and what it costs
3. Hit rate 0.50 saves 18% or 82% of the work depending on *which* half you cache. Write the
   paragraph explaining to somebody why their hit-rate target is the wrong target
4. **The staleness page.** `r05`, served from a pre-8259 cache, grounded entirely in a
   withdrawn RFC. Write the invalidation rule you would actually ship, and the thing it
   still would not catch

---

## Deep track

> An overlap-based staleness check scored 0.833 and missed the only chunk that mattered.
> Design a check that would have caught it, measure it on the whole dev set, and report its
> false-alarm rate on a corpus that did not change. Week 9's gate arithmetic applies
> unchanged — and if your check fires on a third of unchanged rebuilds, it will be switched
> off, and you will be the one who switches it off.

---

## Log

`logs/stuck-log.md` and `logs/signal-log.md`.
