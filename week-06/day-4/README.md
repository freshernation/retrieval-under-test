# Day 4 — Filters, and where you put them

> **By the end of today** you can filter a retrieval result without silently losing recall,
> and you can say why an approximate index makes that harder.

---

## Read first

- [ ] [**Before or after**](../../content/week-06/day-4/before-or-after.md) — 25 min
- [ ] [**A filter is a requirement, not a defect**](../../content/week-06/day-4/a-filter-is-a-requirement.md) — 20 min

---

## Predict first

You filter to documents published since 2015. That keeps 63 of your 266 chunks.

1. **What happens to answer recall?**
2. **How many of your nineteen queries return fewer than five results?**

---

## The lab

`filters.py`. Week 2's `lineage.py` and week 4's `windows.py` are importable — week 2's
supersession graph finally becomes an operational filter.

```python
chunk_metadata(chunks, corpus)     current_only(meta)     published_since(meta, year)
post_filter(ranked, predicate, k)  pre_filter(chunks, predicate)
shortfall(results, k)              survival(ranked, predicate, depth)
```

`shortfall` is the one to report. A system that silently returns three results when asked
for five looks exactly like one that found three good ones.

```bash
pytest week-06/day-4 -v
```

---

## The written exercise

`week-06/day-4/filters.md`, one page.

1. Your two predictions and the results
2. Pre- and post-filtering agree on recall here. State the **condition** under which that
   holds, and then say what breaks it
3. **The ANN interaction.** Week 5's index returns an approximate top-n. Explain, in a
   paragraph, why post-filtering over approximate candidates loses recall twice and why
   neither loss is reported by anything
4. Week 2 *demoted* superseded documents; today you *filtered* them. Name a query in your
   own set where those two choices give different answers, and say which is right

---

## Deep track

> Implement a third placement: filter-aware retrieval, where the predicate is pushed into
> the scoring loop so that failing chunks are never scored. Measure all three for both
> recall and work done. Then say which of the three a vector database can actually offer
> you, and why.

---

## Log

`logs/stuck-log.md` and `logs/signal-log.md`.
