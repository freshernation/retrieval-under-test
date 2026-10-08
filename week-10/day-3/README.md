# Day 3 — The field that costs nothing

> **By the end of today** a machine performs the attribution walk you have been doing by
> hand since week 1.

---

## Read first

- [ ] [**The field that costs nothing**](../../content/week-10/day-3/the-field-that-costs-nothing.md) — 25 min
- [ ] [**Attribution by machine**](../../content/week-10/day-3/attribution-by-machine.md) — 20 min

---

## Predict first

Twenty dev queries. Six of them produced confident, wrong answers in week 8.

**Predict the station each of the six failed at.** You do not need the ids — a guess at the
distribution across stations 1 to 6 is enough. Commit to it.

---

## The lab

`tracing.py`.

```python
Span      Trace(query_id).record(name, ms, ids)      .total      .ids(stage)
critical_path(trace)        missing_ids(trace)
attribute(trace, query, chunks, faithful)            attribution_report(stations)
```

`attribute` is nine lines and it is the course's central rule as code: walk 1 → 7, stop at
the first station that failed, never fix downstream of the break.

```bash
pytest week-10/day-3 -v
```

---

## The written exercise

`week-10/day-3/tracing.md`, one page.

1. Your predicted distribution and the measured one
2. **Station 6 is empty, and station 2 is empty.** One paragraph on what you would have
   spent next week doing, and what you will do instead
3. `r05` is attributed `7 none`, is perfectly faithful, and is grounded in a withdrawn
   RFC. Two sentences on why no station failed, and where that failure belongs
4. The fields your trace must carry. For each, one sentence on what dies without it — and
   mark the ones you would lose first if somebody halved your log budget

---

## Deep track

> There is no station 3 branch, because an index failure presents as a retrieval failure
> and the trace cannot tell them apart. Design the evidence that would separate them —
> what would the trace have to record, and what would you have to re-run? Then decide
> whether it is worth it, and write down the decision rather than the design.

---

## Log

`logs/stuck-log.md` and `logs/signal-log.md`.
