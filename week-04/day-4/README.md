# Day 4 — The frontier

> **By the end of today** you can present a chunking decision the way it should be
> presented — two axes, a frontier, and a requirement from outside the system.

---

## Read first

- [ ] [**Chunking is a cost decision**](../../content/week-04/day-4/chunking-is-a-cost-decision.md) — 25 min
- [ ] [**Choosing on a frontier**](../../content/week-04/day-4/choosing-on-a-frontier.md) — 25 min

---

## Predict first

Whole documents — no chunking at all — retrieve **every** answer in the top 3.

So: **what is chunking for?** One sentence, before you read the articles. Most people write
something about precision or relevance. Keep the paper.

---

## The lab

`budget.py`.

```python
Point(name, k, recall, tokens)      Point.dominates(other)
context_cost(ranked, chunks, k)     measure(chunks, queries, rank_fn, name, k)
pareto(points)                      cheapest_meeting(points, target)
savings(a, b)
```

`dominates` must return False for a point against itself. Get it wrong and `pareto` returns
an empty frontier, which looks like a data problem and is not.

Then `test_the_thesis`, and check it against what you wrote this morning.

```bash
pytest week-04/day-4 -v
```

---

## The written exercise

`week-04/day-4/frontier.md`, one page. **This is the milestone's first draft.**

1. Your one-sentence answer to "what is chunking for", from this morning, and your answer
   now
2. The full table: every configuration at every k, with both numbers. Then the frontier,
   with the dominated points still visible and marked as dominated
3. `fixed 400` — the size the internet recommends — is dominated at every k. State by what,
   and by how much
4. **The two numbers from outside.** Pick a target coverage and a context budget, justify
   each in one sentence in terms of consequences rather than preferences, and name the
   configuration they select. Then change the target to 0.75 and say what you would be
   agreeing to

---

## Deep track

> Everything today assumes the frontier is stable. It is measured on nine queries. Bootstrap
> the frontier: resample the queries, recompute it, and see how often each point is on it.
> Report the frontier as a set of points with membership probabilities, and then say whether
> that changes the decision you made.

---

## Log

`logs/stuck-log.md` and `logs/signal-log.md`.
