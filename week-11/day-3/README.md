# Day 3 — The second hop

> **By the end of today** you can fix the corpus's oldest trap, and you will know what the
> fix actually is.

> **Deep track** — the whole week.

---

## Read first

- [ ] [**The fact in the other document**](../../content/week-11/day-3/the-fact-in-the-other-document.md) — 25 min
- [ ] [**Superseded is not wrong**](../../content/week-11/day-3/superseded-is-not-wrong.md) — 20 min

---

## Predict first

Week 8's `r05` cites RFC 7159 — withdrawn in December 2017 — with faithfulness 1.00.

**Will adding RFC 8259's chunk to the context stop it?** Yes or no. Then: **what will the
hop cost, in retrievals?**

---

## The lab

`hop.py`.

```python
stale_in(context, graph)      successors(chunk_ids, graph)      follow(deeper, docs, limit)
add_hop(shortlist, extra)     replace_hop(shortlist, stale, extra)
hop_report(superseded, answered, retrievals)
```

Write `add_hop` and run it **before** you write `replace_hop`. The version that presents
both documents and lets the reader judge is the humane design and it is the one everybody
writes first, and finding out what it does is worth more than being told.

```bash
pytest week-11/day-3 -v
```

---

## The written exercise

`week-11/day-3/hop.md`, one page.

1. Your two predictions and the measured answers
2. The comparison table: baseline, hop, and week 2's `is_current` filter. Then one
   paragraph on what your multi-hop retrieval turned out to be
3. **The fix breaks `r07`.** Explain the difference between `r05` and `r07` in three
   sentences, then write the rule you would ship that handles both — or state that you
   cannot, and why
4. Dropping only the stale chunk you noticed promotes the next chunk of the same withdrawn
   document. One sentence on why that bug looks like a near miss

---

## Deep track

> The supersession edge was in the metadata. Name three edges in *your own* corpus that
> are not — a thing that supersedes, contradicts, requires or amends another thing — and for
> each one, say what it would cost to make it a field. Then decide which of the three is
> worth a hop and which is worth an ingest change. The second list should be longer.

---

## Log

`logs/stuck-log.md` and `logs/signal-log.md`.
