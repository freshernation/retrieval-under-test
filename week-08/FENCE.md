# Week 8 — Concept fence

## Allowed

- Everything from weeks 1 to 7
- **Generation**, via `raglab.generator.SimulatedGenerator` — a stipulated model, not a
  language model
- **Groundedness**: was the answer in the context, measured with week 4's answer spans
- **Citations**: parsing, resolving, presence-in-context, sentence-level attribution
- **Faithfulness**: word-overlap support of a claim by its cited source, and its limits
- **Refusal**: a confidence signal, the four-way outcome table, the frontier
- **Currency at the last station**: week 2's supersession graph applied to citations

## Not yet

**LLM-as-judge, and any model-scored metric.** That is next week, and using one today
would hide the fact that everything measured this week was computed *mechanically*, which
is the property that makes it trustworthy · sample-size analysis and regression gates ·
query rewriting or expansion · agents · caching · production services

---

## The rule that matters most this week

**Every number this week is computed by machinery, not by reading.**

Week 1 claimed you cannot evaluate a RAG system by reading its answers. This is the week
that becomes concrete: the default generator produces twenty fluent, correctly cited
answers, six of which are about questions it could not answer, and **no amount of reading
distinguishes them.**

So you may not grade an answer by looking at it. Every claim in the milestone report cites
a function that produced it.

## The other rule

**The generator is a stipulated model. Assert the direction, never the value.**

`SimulatedGenerator` reproduces the behaviours the week is about — it answers anything,
grounds its wording in the retrieved text, cites, and prefers the top-ranked chunk. It does
not reproduce paraphrase, synthesis or reasoning.

Its faithfulness of 1.00 is a property of a rule-based copier and **not an estimate of what
a real model would score.** Week 7's discipline, unchanged: the comparisons transfer, the
values do not.
