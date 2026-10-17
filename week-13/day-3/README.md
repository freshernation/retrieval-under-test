# Day 3 — The gate runs itself

> **By the end of today** the gate runs on every pull request, the baseline is a file
> only a person can change, and you can defend letting a change through that lost a query.

---

## Read first

- [ ] [**The gate nobody has to remember**](../../content/week-13/day-3/the-gate-nobody-has-to-remember.md) — 20 min

---

## Predict first

`k1 = 2.0` against the baseline, on the nineteen answerable dev queries.

**Does a gate with zero tolerance pass it? Does one with week 9's tolerance?**

---

## The lab

`cigate.py`, and `retrieval-gate.yml`. `run_gate.py` is given.

```python
RULES
measure(rank, queries)     read_baseline(path)     write_baseline(path, metrics, reason)
decide(baseline, candidate, rules)
run(rank, queries, baseline_path, rules, accept=None, say=print)
```

```bash
pytest week-13/day-3 -v
python3 week-13/day-3/run_gate.py --accept "first baseline"
```

Then copy the workflow to `.github/workflows/retrieval-gate.yml` and open a pull request.

---

## The written exercise

`week-13/day-3/cigate.md`, one page.

1. Your prediction, and the answers
2. Where your tolerance came from, with the week 9 number
3. Why CI must never pass `--accept`. Describe the first week of a team where it does
4. The gate passed `k1 = 2.0`. Would you merge it? Say what else you would want to know
