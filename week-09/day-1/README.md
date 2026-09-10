# Day 1 — What you cannot measure once it is running

> **By the end of today** you can list the metrics that need ground truth, and you will have
> found two serving-time signals that predict one of them.

---

## Read first

- [ ] [**The serving-time gap**](../../content/week-09/day-1/the-serving-time-gap.md) — 25 min
- [ ] [**Available is not informative**](../../content/week-09/day-1/available-is-not-informative.md) — 20 min

---

## Predict first

Four signals available on every request: retrieval confidence, distinct documents in the
context, answer length, citation count.

**Rank them by how well they predict whether the answer was in the context.** Commit to an
order.

---

## The lab

`proxies.py`.

```python
availability()      needs_ground_truth(metrics)      auc(good, bad)
separation_strength(value)                            proxy_report(signals, truth)
useful_proxies(report, floor)
```

Write `availability()` **by hand**, from week 8's report card. Five minutes, and the test to
apply to each metric is: *could I compute this for a query I have never seen, right now, with
no human involved?*

Then `auc`, which asks "does this signal predict that outcome" without picking a threshold —
because picking a threshold first is how a useful signal gets discarded for scoring badly at
a cutoff nobody chose.

```bash
pytest week-09/day-1 -v
```

---

## The written exercise

`week-09/day-1/proxies.md`, one page.

1. Your predicted ranking and the actual one
2. The offline-only list. For each, write one sentence on what you would do if a user
   reported a bad answer and you could not compute it
3. **Distinct documents scores AUC 0.17.** Explain in two sentences why it is *inversely*
   predictive, and why nobody instruments it
4. Answer length and citation count are indistinguishable from chance and are exactly what a
   dashboard tracks. Write the paragraph you would send to whoever owns your dashboard

---

## Deep track

> Build a combined proxy — a simple weighted score over the two useful signals — and measure
> its AUC. Then check whether it beats the best single one by more than the week-3 floor
> allows you to claim. This is the routing signal week 11 needs, and finding out now whether
> combination helps is worth a great deal.

---

## Log

`logs/stuck-log.md` and `logs/signal-log.md`.
