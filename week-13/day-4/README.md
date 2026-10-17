# Day 4 — A service with a door

> **By the end of today** other people search the index over HTTP, each seeing only what
> their key may read, and writers change it through the queue — with an honest answer
> about when their change is live.

---

## Read first

- [ ] [**Accepted is not done**](../../content/week-13/day-4/accepted-is-not-done.md) — 20 min

---

## Predict first

A writer posts RFC 9309 and gets `202 Accepted`. A reader searches for "robots exclusion
protocol" straight away.

**Is RFC 9309 in the results?** What would tell the writer when it will be?

---

## The lab

`searchapi.py`.

```python
caller_for(header, keys)
create_app(index, acl, keys, queue, versions)
    GET /health     POST /search     POST /documents
```

```bash
pytest week-13/day-4 -v
```

---

## The written exercise

`week-13/day-4/searchapi.md`, one page.

1. Your prediction, and the answer
2. Why `/search` filters the top 60 and then takes k, rather than taking k and filtering
3. The writer wants to know when their document is live. Design the smallest change that
   tells them
4. Every key here is in a file. Say where it should be, and what changes when one leaks
