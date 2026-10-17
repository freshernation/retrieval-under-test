# Milestone 14 — Guarded, cached, scaled

> **Ship:** one search path that guards the query, answers from a cache that knows who is
> asking and which identifiers they asked about, searches shards with the statistics of
> the whole, and never shows a reader what they may not see.

---

## The brief

### 1. Write `guarded.py`

`guarded_search` and `scale_report`. The order of the five steps is the whole design.

### 2. Measure

The four numbers from this week, on one line each, from `scale_report`.

### 3. Write `REPORT.md`

---

## The rubric

| Station | This week |
|---|---|
| 3 Index | A graph index and shards: both approximate something, and both have a size below which they cost more than they save |
| 4 Retrieve | Statistics shared across shards, and a cache that answers similar questions only when it is the same question |
| 6 Generate | A guard behind the answer as well as in front of the question |
| 7 Measure | Every guardrail with its false-positive rate |

---

## Check it

```bash
pytest week-14/milestone -v
python3 tools/check_evals.py
```
