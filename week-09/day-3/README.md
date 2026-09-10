# Day 3 — How many queries

> **By the end of today** you can put a number in a plan: how many queries it takes to prove
> the improvement you are hoping for.

---

## Read first

- [ ] [**The number that goes in the plan**](../../content/week-09/day-3/the-number-in-the-plan.md) — 25 min
- [ ] [**Two floors**](../../content/week-09/day-3/two-floors.md) — 20 min

---

## Predict first

You have 19 answerable dev queries.

1. **What is the smallest difference you can detect?**
2. **How many queries would you need to detect 5 points?**

---

## The lab

`power.py`.

```python
paired_differences(a, b)     paired_sd(a, b)        mde(n, sd)
queries_needed(effect, sd)   judge_noise_floor(label_agreement)
detectable(effect, n, sd, label_agreement)          power_table(sd, sizes, effects)
```

`queries_needed` has a **square** in it. Halving the effect you want to detect quadruples
the queries, which is why "we will add a few more" is not a plan.

`power_table` is the planning artefact and it goes in the report **before** the results — a
table showing your experiment could never have detected the effect you are claiming is
embarrassing afterwards and free beforehand.

```bash
pytest week-09/day-3 -v
```

---

## The written exercise

`week-09/day-3/power.md`, one page.

1. Your two predictions and the results
2. The power table: four sizes, three effects
3. **Go back through your reports.** Week 2's cleaning delta, week 6's fusion gains, week 7's
   reranking ceiling. Which of them were above the MDE of the set they were measured on?
4. Your metric is binary, which is why the spread is large. Write two sentences on what a
   graded metric would buy you, and whether that is a reason to prefer nDCG

---

## Deep track

> The MDE formula assumes a normal approximation. Check it: bootstrap the real per-query
> differences at several sample sizes, measure the interval width empirically, and compare
> with the analytic MDE. Report where the approximation is poor, which will be at exactly the
> sample sizes you have.

---

## Log

`logs/stuck-log.md` and `logs/signal-log.md`.
