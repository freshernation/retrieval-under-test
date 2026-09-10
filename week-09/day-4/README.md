# Day 4 — The gate

> **By the end of today** you can stop a regression automatically, without building something
> that gets muted within a fortnight.

---

## Read first

- [ ] [**A gate that gets kept**](../../content/week-09/day-4/a-gate-that-gets-kept.md) — 25 min
- [ ] [**Guard few things**](../../content/week-09/day-4/guard-few-things.md) — 20 min

---

## Predict first

A gate guards ten metrics. Each fires spuriously 5% of the time on an unchanged system.

**How often does the gate fire on an unchanged system?**

---

## The lab

`gate.py`.

```python
Rule(metric, direction, tolerance)     Gate(rules).check(baseline, candidate)
false_alarm_rate(gate, runs)           compound_alarm_rate(per_metric_rate, metrics)
tolerance_from_mde(mde_value)
```

**Direction is per metric.** `confidently_wrong` and `unresolvable` are metrics you want to
fall, and a gate assuming higher-is-better everywhere waves through a system that doubled its
wrong answers.

`check` reports `checked` as well as the verdict. A gate that silently skips a missing metric
**passes**, and the most common cause of a gate passing is that it stopped running.

```bash
pytest week-09/day-4 -v
```

---

## The written exercise

`week-09/day-4/gate.md`, one page.

1. Your prediction and the answer — 40%
2. Your gate: which metrics, which directions, which tolerances, and where each tolerance
   came from
3. **The false-alarm rate** of your gate, measured on repeated runs of an unchanged system.
   If it is above 5%, say what you will do about it
4. Name the metrics you deliberately did **not** guard, and why reporting is the right
   treatment for each

---

## Deep track

> A gate on a mean is one design. Build a second that gates on **per-query regressions** —
> block if any query that previously succeeded now fails — and compare their false-alarm
> rates and their sensitivity. One of them catches a change that helps on average and breaks
> a class of query, which is the failure `EVALS.md` has warned about since week 1.

---

## Log

`logs/stuck-log.md` and `logs/signal-log.md`.
