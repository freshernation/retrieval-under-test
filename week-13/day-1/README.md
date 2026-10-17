# Day 1 — Changes arrive out of order

> **By the end of today** you can apply a stream of changes delivered at least once, in
> any order, and end with the right index — and say how often you would not have.

---

## Read first

- [ ] [**At least once, in any order**](../../content/week-13/day-1/at-least-once-in-any-order.md) — 25 min

---

## Predict first

Ten RFCs published, then two withdrawn and one revised. The thirteen changes are shuffled,
and two of them delivered twice.

**Applied in the order they arrive, in how many of twenty shuffles is the final index
wrong?** Write a number down.

---

## The lab

`ingestqueue.py`.

```python
Change(doc_id, version, action, text=None)
chunks_of(index, doc_id)
apply_naive(index, change, chunker)          apply(index, versions, change, chunker)
snapshot_of(index)
ChangeQueue(path)  .put  .claim  .done  .fail  .counts
drain(queue, index, versions, chunker)
```

```bash
pytest week-13/day-1 -v
```

---

## The written exercise

`week-13/day-1/ingestqueue.md`, one page.

1. Your prediction, and the answer
2. Find one shuffle where the naive index is wrong and say exactly which change undid which
3. Why does a withdrawal's version have to be remembered? Give the delivery order that
   proves it
4. A change has failed three times and is dead. Who finds out, and how?
