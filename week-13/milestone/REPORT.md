# Milestone 13 report — [your name]

> Fill this in. Every number cites a run id. `tools/check_evals.py` enforces it.

---

## 1 · How a change reaches search

From `POST /documents` to a search that finds it: each step, what can fail at it, and
how you would know.

## 2 · Out of order

Day 1's numbers: wrong final indexes in arrival order, and with versions. One sentence
on why the withdrawal's version must be remembered.

## 3 · What survives a restart

The snapshot, the versions and the queue. What would happen if any one of them were lost.

## 4 · The gate

Your baseline, with its run id, the tolerance and where it came from, and one change it
blocked and one it let through.

**Run:** `run:<id>`

## 5 · Two machines

What breaks the day the API runs on two machines, and what you would change first.
