# The cached answer that outlives its correction

*Week 10 · Day 2 · about 20 minutes*

> By the end of this you can explain why a cache is part of the system rather than a layer
> over it, and why an overlap-based staleness check passes the case that matters.

---

## Sources

| Source | Tier | What it gives you |
|---|---|---|
| [**RFC 9111**, HTTP Caching](https://www.rfc-editor.org/rfc/rfc9111.html) | 1 | Freshness lifetime, staleness, and revalidation as a specified mechanism |
| [**RFC 8259**](https://www.rfc-editor.org/rfc/rfc8259.html) | 1 | The document that obsoletes 7159 and reverses its UTF-8 guidance |
| [**Google SRE Book**, ch. 6](https://sre.google/sre-book/monitoring-distributed-systems/) | 1 | Indicator versus diagnostic |

---

## The demonstration

`r05` asks whether JSON must be encoded in UTF-8.

RFC 7159 says one thing. RFC 8259 obsoletes it in December 2017 and says the opposite about
exactly this. Week 2 found the trap; week 6 watched retrieval walk into it; week 8 watched
the generator cite the withdrawn document with a perfect support score.

Now serve `r05` from a corpus that predates 8259, and cache it.

| | context |
|---|---|
| pre-8259, cached | `rfc-7159#10`, `rfc-3986#37`, `rfc-7159#11`, `rfc-9309#8`, `rfc-9309#10`, `rfc-7159#3` |
| current, fresh | `rfc-7159#10`, **`rfc-8259#12`**, `rfc-3986#37`, `rfc-9309#8`, `rfc-7159#11`, `rfc-9309#10` |

The fresh build puts the correcting document at rank two. The cached one is grounded
entirely in the withdrawn RFC, and it will be, for as long as the entry lives — which, with
no invalidation rule, is forever.

The cache reports a **hit**. Nothing in the system disagrees. Faithfulness is 1.00, every
citation resolves, and the attribution walk says station 7: nothing failed.

---

## Why this makes the cache part of the system

A cache is usually reasoned about as a performance layer — same answers, sooner. That
framing is false the moment the thing being cached was derived from a corpus that can
change, which is every RAG system.

What the cache actually does is **freeze a retrieval decision made against a corpus
snapshot** and keep serving it after the snapshot has moved. The answers are not the same
answers sooner; they are older answers, and nothing in the response says so.

Which is why the cache belongs in the config and in the run id, and why a cached run may
not be compared against an uncached one. Two systems that differ in what they say are two
systems. Week 7's rule — every optional stage defaults to off — applies here for a stronger
reason than usual.

HTTP worked this out decades ago and wrote it down. RFC 9111 does not treat freshness as an
operational detail: it gives staleness a definition, a lifetime and a revalidation
mechanism, because a cache without those is a correctness bug with a latency benefit.

---

## The check that passes

So write a staleness check. Compare the cached context against one rebuilt now.

**Overlap: 0.833.** Five of the six chunks are still the right ones.

A threshold anywhere sensible passes that. And the one chunk that changed is the answer.

This is the same blindness three times over now:

- week 7 — answer recall asks whether the answer is present and is indifferent to the other
  four slots
- week 9 — faithfulness relates the answer to the context and cannot see the world
- week 10 — an overlap score relates two contexts and cannot see which member mattered

**An aggregate over a set cannot tell you which element of the set was load-bearing.** That
is not a defect in any one metric; it is what aggregation is. The response is not a better
aggregate. It is a check aimed at the specific thing: *did any document in my corpus change
its supersession status, and does any cached entry cite the superseded side?* That is a
metadata query, it is cheap, and it is narrow on purpose.

---

## What to actually ship

Three rules, in increasing order of what they cost you.

1. **Version the key.** Include a corpus-version hash in the cache key. A corpus rebuild
   invalidates everything, which is blunt, correct, and costs you the whole cache on every
   ingest.
2. **Invalidate by document.** Keep the chunk ids per entry — you have them, day 3 insists
   on them — and drop entries touching a changed document. Precise, and it needs the ids.
3. **Never cache a query that touched a superseded document.** Narrow, aimed at this exact
   failure, and it still misses the next one.

And then write down what none of them catch: a document that should have been superseded
and was not. There is no mechanism for that, because it is a corpus problem, and station 1
is the quiet station this week for exactly this reason.

---

> **Known** — RFC 9111 specifies freshness lifetime, staleness and revalidation as required
> mechanisms rather than conventions (`rfc-9111`) · RFC 8259 obsoletes RFC 7159 and changes
> its guidance on UTF-8 encoding (`rfc-8259`) · an indicator triggers work and a diagnostic
> explains it (`sre-book`)
> **Inferred** — that a cache over a mutable corpus changes what the system says and
> therefore belongs in the config and the run id. Ours, following week 7's default-off rule
> **Inferred** — that an aggregate over a context cannot identify which member was
> load-bearing, which is the same limitation as week 7's answer recall and week 9's
> faithfulness. Ours, and the third instance is what makes it a pattern
> **Derived** — a cached pre-8259 context for `r05` contains no chunk from the correcting
> document while a fresh one ranks it second, so the cached answer is grounded wholly in a
> withdrawn specification · an overlap check over those two contexts scores 0.833, above any
> plausible threshold
> **Unknown** — how long a typical production RAG cache entry lives, and whether any ships
> a supersession-aware invalidation rule. We have not seen one
