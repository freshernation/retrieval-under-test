# Day 3 — The verdict

> **By the end of today** you can deliver a fusion result that survives someone asking
> "compared to what?", and you can name the failure fusion cannot reach.

---

## Read first

- [ ] [**Compared to what**](../../content/week-06/day-3/compared-to-what.md) — 25 min
- [ ] [**What fusion cannot conjure**](../../content/week-06/day-3/what-fusion-cannot-conjure.md) — 25 min

---

## Predict first

Your fusion beats dense retrieval at k=5.

**Is that an improvement?** Answer before the lab, and commit.

---

## The lab

`verdict.py`.

```python
recall(rankings, chunks, queries, k)      oracle(inputs, chunks, queries, k)
verdict(fused, inputs, chunks, queries, k)
by_family(fused, inputs, chunks, queries, k)
unreachable(inputs, chunks, queries, k)
```

`beats_all` is **strictly greater than every input**. `captured` is `None` when there was
no headroom, because a percentage of nothing is not a number.

Then `unreachable`, which is six lines and is the most important list in the week.

```bash
pytest week-06/day-3 -v
```

---

## The written exercise

`week-06/day-3/verdict.md`, one page. **This is the milestone's first draft.**

1. Your prediction, and the k=5 verdict: `beats_all` False, `dilution` 0.053
2. The three verdicts at k = 3, 5, 10 in a single table, with `dilution` and `captured`
3. **The family table.** One family is at 0.33 for every system at every k. Name it, name
   the two queries, and explain in two sentences why no fusion can help
4. Given that, write the one-paragraph recommendation you would give a team: what should
   they do next, and what should they *not* spend the next sprint on?

---

## Deep track

> `unreachable` gives you the queries nothing retrieves. For each, find where the answer
> actually is and work out what would have had to be different — a different chunking, a
> different analyzer, an expanded query, a different corpus. Then rank those four
> interventions by expected cost. You have just done, informally, what week 11 does with a
> model, and doing it by hand first is the point.

---

## Log

`logs/stuck-log.md` and `logs/signal-log.md`.
