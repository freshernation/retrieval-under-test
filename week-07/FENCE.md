# Week 7 — Concept fence

## Allowed

- Everything from weeks 1 to 6
- **Reranking**: feature-based scoring over a shortlist, blending with the retriever's
  prior, and the ceiling a shortlist imposes
- **Diversity**: pairwise similarity within a result set, deduplication, maximal marginal
  relevance
- **Budgets**: packing a word budget, truncation, answer density, the budget/answered
  frontier
- **Order**: rank order, document order, ends-first, and a **stipulated** positional model
- **Assembly**: labelled chunks, the string a generator would receive

## Not yet

Language models, for anything — including as a reranker, which is what a cross-encoder is ·
prompts · generation, grounding, citation or refusal · query rewriting and expansion ·
agents · caching

---

## The rule that matters most this week

**A stipulated model's values are never asserted, only its direction.**

Day 4 needs a positional weighting and there is no generator here to measure one. So it
uses a parabola whose *shape* comes from the literature and whose *numbers* come from
nowhere.

Every test about it compares two orderings and checks that the comparison survives changing
the parameter. **None of them asserts a score**, and the report may not quote one. A number
produced by a model you cannot check is a number that will be quoted back at you as
evidence within a month.

## The other rule

**Every stage you add must be compared against not having it.**

Reranking, deduplication and MMR are all techniques that are assumed to help. This week two
of the three cost more than they buy on this corpus, and the only reason you know is that
the milestone's default configuration has **every stage off**.
