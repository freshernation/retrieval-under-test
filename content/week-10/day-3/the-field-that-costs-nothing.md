# The field that costs nothing

*Week 10 · Day 3 · about 25 minutes*

> By the end of this you can explain why a trace of durations is the small half of tracing,
> and what the other half costs.

---

## Sources

| Source | Tier | What it gives you |
|---|---|---|
| [**Sigelman et al.**, *Dapper*](https://research.google/pubs/pub36356/) | 1 | Distributed tracing as built and operated, including what they sampled away |
| [**OpenTelemetry**, trace specification](https://opentelemetry.io/docs/specs/otel/trace/api/) | 1 | Spans, attributes, and the vendor-neutral data model |
| [**Google SRE Book**, ch. 6](https://sre.google/sre-book/monitoring-distributed-systems/) | 1 | What observability is for |

---

## What tracing is sold as

Spans, a waterfall diagram, find the slow one. That is real and it is the smaller half.

A duration tells you which stage was **slow**. It cannot tell you which stage was
**wrong**, and in a retrieval system almost every incident is the second kind. *"The answer
cited the wrong document"* has no slow stage in it anywhere.

---

## What it is actually for here

This course's central rule, since week 1: **attribute the failure to exactly one station
before you change anything.** Walk 1 → 7, stop at the first station that failed, never fix
downstream of the break.

Doing that by hand means reproducing the request — rebuilding the shortlist, repacking the
context, re-running the generator. Which is fine in a lab and impossible in an incident,
because the corpus has been re-ingested since, the index has been rebuilt, and the model
version has moved. **The thing you re-run is not the thing that failed.**

Unless the trace recorded the ids.

```python
trace.record("shortlist", ms, shortlist_ids)
trace.record("context", ms, tuple(context))
```

Two lists of about ten short strings per request. With them, the walk is nine lines of code
over a record you already have, performed after the fact, on an incident nobody can
reproduce. Without them, you have a waterfall.

---

## The two layers of a trace

Worth separating explicitly, because week 9 set this up.

**Serving-time fields** — durations, ids, scores, token counts. Available on every request,
no ground truth needed, cheap.

**Eval-set fields** — which station failed, whether the answer was available, whether it
was right. These need judgments, so they cannot be computed live.

Attribution needs both. Which means **attribution runs in CI against the eval set, not in
production** — and the only reason it can run at all is that the serving-time layer kept the
ids. The ids are the bridge between the request that happened and the judgments you have.

That is the shape of the answer to week 9's serving-time gap. Not a proxy for the metric you
cannot compute, but a *record* complete enough that you can compute it later, on the queries
you have labels for.

---

## What gets dropped, and when

Dapper is honest about this and the honesty is the useful part: they sampled aggressively,
because full-fidelity tracing at Google's volume was not affordable. Sampling is the right
answer at that scale.

But notice *what* is usually dropped first when a log budget gets trimmed. Not the
durations — those are small numbers and they feed the dashboard somebody is watching. The
**attributes**. The ids. The lists. They are the biggest field in the span and the one with
no graph pointing at it.

So the field that costs almost nothing in absolute terms is the field that looks expensive
relative to a trace carrying nothing else, and it is the one that dies. Then six months
later nobody can explain an incident, and the conclusion drawn is that tracing did not
help.

If you have to cut: keep the ids for a short retention window and the durations for a long
one. Ids answer *why*, and you only need them while the question is live.

---

## The total is not the latency

One more honest caveat, since the code is three lines.

`trace.total` is the sum of the spans. A request's latency is wall-clock from arrival to
response, which includes **the gaps between spans** — queueing, connection acquisition,
serialisation, the scheduler.

A system whose span total is 40ms and whose p95 latency is 400ms is a system with a queue,
and the trace as written cannot see it. Report both, and when they disagree, the gap is the
finding.

---

> **Known** — distributed tracing records a span tree per request with attributes attached,
> and production deployments sample rather than keep everything
> (`sigelman-2010`, `otel-spec`) · a span carries typed attributes as part of the data model
> (`otel-spec`)
> **Inferred** — that the ids chosen by each stage are the highest-value field in a
> retrieval trace, because they are what makes post-hoc attribution possible without
> reproducing a request that can no longer be reproduced. Ours
> **Inferred** — that attributes are the first field cut when log volume is trimmed, since
> they are the largest and the least watched. Ours, from practice rather than from a study
> **Derived** — a sum of spans excludes inter-span time, so a span total below the measured
> request latency indicates queueing or acquisition the trace does not instrument
> **Unknown** — what fraction of production RAG traces record retrieved ids. Every
> observability vendor's RAG example we have read traces durations and token counts
