# Day 3 — Comparing two retrievers

> **By the end of today** you can produce the honest output of a comparison, which is not a
> winner.

---

## Read first

- [ ] [**Which is better is the wrong question**](../../content/week-05/day-3/the-wrong-question.md) — 25 min
- [ ] [**What transfers from LSA to a real model**](../../content/week-05/day-3/what-transfers.md) — 25 min

---

## Predict first

You have two retrievers with means one point apart.

1. **Which is better?** Commit to an answer.
2. **How many queries would each get that the other misses?** Two numbers.

---

## The lab

`compare.py`.

```python
head_to_head(a_rankings, b_rankings, chunks, queries, k)
tally(table)          recall_of(table, side)      oracle_recall(table)
headroom(table)       by_family(table, queries)   winner_flips(tables)
```

`headroom` is the important one and it is three lines. **Fusion can only recover queries
that one system gets and the other misses**, so if there are none, no technique next week
can help — and you can find that out this afternoon instead.

```bash
pytest week-05/day-3 -v
```

---

## The written exercise

`week-05/day-3/comparison.md`, one page. **This is the milestone's first draft.**

1. Your two predictions and the results
2. The full head-to-head table at k=1, 3, 5, 10. Four tallies, four oracles, four headrooms
3. **The flip.** At k=3 dense wins; at k=5 lexical wins. Write the sentence you would put in
   a report, and make it survive somebody asking "at what k?"
4. Headroom is zero at every k on your dev split. Write a paragraph on what you would need
   in order to establish that fusion is worth trying — and note that week 3's milestone
   already told you to build it

---

## Deep track

> `oracle_recall` assumes a perfect chooser. Build an *imperfect* one: pick the system per
> query using only signals available at query time — query length, whether every term is in
> the vocabulary, the top score's margin over the second. Measure how much of the oracle it
> recovers. This is routing, it is week 11's material, and doing it badly now is the best
> preparation for doing it properly then.

---

## Log

`logs/stuck-log.md` and `logs/signal-log.md`.
