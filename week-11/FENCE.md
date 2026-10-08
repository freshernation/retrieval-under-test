# Week 11 — Concept fence

## Allowed

- Everything from weeks 1 to 10
- **Query rewriting**: idf-based term dropping, pseudo-relevance feedback, fan-out and
  fusion over variants
- **Routing**: oracle ceilings, headroom, thresholds on a serving-time signal, capture
- **Multi-hop**: triggers, successor resolution over week 2's supersession graph, merge
  and replace
- **Loops**: stopping conditions on serving-time signals, caps, churn, cost multiples
- Real models behind `--live` only, and never as the basis of a comparison against an
  offline run

## Not yet

Nothing. This is the last week with new mechanism in it — week 12 is the report and the
clinics.

---

## The rule that matters most this week

**No rewrite rule derived from a failing query.**

A synonym dictionary built by looking at the queries that failed is the eval set leaking
into the system. It will score beautifully on the set it was built from and generalise to
nothing, and you will not find out, because the only instrument you have is the set it was
built from.

Every rewrite in this week comes from the corpus or from the query alone — idf from the
index, feedback terms from the retrieved chunks. If you want a hand-built mapping, build it
from documents you have never measured against, and say so.

## The other rule

**Compute the ceiling before building the mechanism.**

Week 7 computed the reranking ceiling before the reranker. Week 11 computes the oracle
router before the router. A mechanism whose maximum possible gain you have not calculated
is a mechanism you cannot evaluate — you will be unable to tell *"this does not work"* from
*"there was nothing here"*, and those have opposite responses.

## And the one this week adds

**Cost in retrievals, not only tokens.**

The loop triples the retrievals and leaves the token count exactly where it was. A cost
report denominated in tokens calls it free, and tokens are the number everybody watches.

Report both. They are different resources and this week's stages move them separately.
