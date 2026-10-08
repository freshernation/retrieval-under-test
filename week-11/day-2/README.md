# Day 2 — Routing

> **By the end of today** you can compute what routing could buy before you build a router,
> and you will have found out what captures it.

> **Deep track** — the whole week.

---

## Read first

- [ ] [**The ceiling comes first**](../../content/week-11/day-2/the-ceiling-comes-first.md) — 25 min
- [ ] [**A proxy is validated for one decision**](../../content/week-11/day-2/one-decision-at-a-time.md) — 20 min

---

## Predict first

Day 1's rewrite gained two queries and lost three.

**How much is available to a perfect router?** A number. Then: **will retrieval confidence
capture it?** Week 9 measured that signal at AUC 0.83 for a different question.

---

## The lab

`route.py`.

```python
oracle_best(outcomes)      headroom(baseline, oracle)      route(signal, threshold)
apply_routes(routes, outcomes)                             capture(baseline, routed, oracle)
sweep(signal, outcomes, thresholds)
```

Build `oracle_best` **first**, before the router. Week 7 computed the reranking ceiling
before the reranker for the same reason: you have to be able to tell *"this does not work"*
from *"there was nothing here"*.

```bash
pytest week-11/day-2 -v
```

---

## The written exercise

`week-11/day-2/route.md`, one page.

1. Your two predictions and the measured answers
2. The threshold sweep, as a table, with `capture` in a column. Note the four thresholds
   where it is negative
3. **The same signal scores 0.83 on one question and 0.667 on another.** Two sentences on
   why that is not a flaw in week 9's measurement
4. **The family router captures 100%.** Write the paragraph explaining why you are not
   shipping it, and then the one listing what you would have to build to approximate it

---

## Deep track

> The decisive queries are five: two the rewrite gains, three it loses. Everything else is
> invariant to the route. Compute the MDE for n=5, then design the smallest extension to
> the eval set that would make a router's gain detectable — how many queries, and in which
> families. Week 9 priced five points at 77 queries for a mean; price this one.

---

## Log

`logs/stuck-log.md` and `logs/signal-log.md`.
