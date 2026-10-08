# Week 10 — Concept fence

## Allowed

- Everything from weeks 1 to 9
- **Work counting**: postings touched, comparisons made, tokens consumed
- **Latency**: per-stage spans, nearest-rank percentiles, per-stage budgets
- **Caching**: keys and normalisation, LRU, hit rate, work saved, staleness
- **Tracing**: spans with ids, critical path, machine attribution to one station
- **Cost**: token counts, budget curves, marginal cost per answer, a price passed in
- Real services and a real model **only** behind `--live`, and never as the basis of a
  reported comparison against an offline run

## Not yet

Agentic retrieval, query rewriting, routing, multi-hop · anything that changes what the
system *retrieves*. This week packages; next week changes.

---

## The rule that matters most this week

**Count the work. Time the clock. Report the work.**

A stopwatch measures this implementation on this laptop with this much free memory. It is
the right tool for finding your own slow stage and the wrong one for any number that
leaves the room.

Postings touched, comparisons made and tokens consumed are properties of the pipeline.
They are identical on every machine, they are comparable between two designs, and they are
what a budget should be written in. Seconds go in the logs.

## The other rule

**No price in a result.**

A price per thousand tokens is the fastest-ageing number in this repository — it has fallen
by more than an order of magnitude over the life of this technology and it will have moved
again before you teach this.

So `price()` takes the rate as an argument and has no default, token counts are the measured
quantity, and a milestone that reports a monthly figure must report the rate it assumed, on
the same line.

## And the one carried forward

**A cache is part of the system, not a layer over it.**

It changes what the system *says*, not only how fast it says it. It goes in the config, it
goes in the run id, and a cached run may not be compared against an uncached one.
