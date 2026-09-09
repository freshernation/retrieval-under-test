# A metric that cannot see it

*Week 7 · Day 2 · about 20 minutes*

> By the end of this you can tell "this technique did not help" from "my instrument cannot
> detect this technique", which are different findings with opposite consequences.

---

## Read the primary source first

| Source | Tier | What it gives you |
|---|---|---|
| [**Clarke et al., *Novelty and Diversity in Information Retrieval Evaluation***](https://dl.acm.org/doi/10.1145/1390334.1390446) | 1 | α-nDCG and why standard relevance metrics cannot reward novelty |
| [**Carbonell & Goldstein**](https://dl.acm.org/doi/10.1145/290941.291025) | 1 | MMR, and the evaluation problem its authors already had |

---

## The result

Answer recall at k=5, for every diversity setting:

| | |
|---|---|
| baseline | 0.737 |
| MMR λ=0.9 | 0.737 |
| MMR λ=0.7 | 0.737 |
| MMR λ=0.5 | 0.737 |
| dedupe, every threshold | 0.737 |
| MMR λ=0.3 | 0.684 |

Identical, until diversity starts costing relevance and then it falls.

---

## Why, and it is structural

`answer_recall_at_k` asks: **do the top k chunks, together, contain every answer span?**

Consider two windows. One has the answer plus four near-copies of it. The other has the
answer plus four chunks on four different subjects. Both contain the answer, so both score
**1.0**.

The metric is not being insensitive. It is **answering a different question** — presence,
not composition — and it will give the same answer for every arrangement of the other four
slots for as long as the answer is in one of them.

> **A metric that stops at "present" cannot value non-redundancy.**

So this is not evidence that diversity does not help. It is evidence that **this instrument
cannot detect diversity**, which is a completely different finding and has the opposite
consequence: the first says stop working on it, the second says fix the instrument.

---

## What would measure it

**Queries whose answers need several chunks.** If the answer needs a span from two
documents, five chunks from one document cannot answer it and a diverse set can. That makes
diversity visible in the *same* metric.

This corpus contains exactly one such query — `r14`, needing spans from RFC 7159 and RFC
8259 — and it is in the held-out split. So on the dev set, diversity is unmeasurable, and
the actionable output of the day is to write more queries like `r14`.

**Diversity-aware metrics.** α-nDCG and its relatives discount a result for covering an
aspect already covered. They need judgments at the level of *aspects* rather than documents,
which is a large annotation cost and is why almost nobody outside evaluation research uses
them.

**Downstream measurement.** Ask whether the generated answer is better. That needs a
generator and a judge, it is week 8 and week 9, and it is the only one of the three that
measures what you actually care about.

---

## The general habit

When a technique shows no effect, there are three possibilities and they look identical in
the numbers:

1. It does not help
2. It helps in a way the metric cannot see
3. It helps on queries the eval set does not contain

Distinguishing them takes one question: **what would this technique change, and would my
metric respond to that change?** For MMR the answer is "it changes the composition of the
non-answer slots, and my metric ignores them" — which settles it in a minute and settles it
as (2).

Skip that question and you will conclude (1), turn the technique off, and be wrong in a way
nothing will ever correct — because a technique nobody uses generates no evidence.

---

> **Known** — standard relevance metrics do not reward novelty, and diversity-aware metrics
> require aspect-level judgments (`clarke-2008`) · MMR's authors identified the evaluation
> difficulty when proposing it (`carbonell-1998`)
> **Inferred** — that "did not help", "unmeasurable" and "untested by this query set" are
> distinguishable by asking what the technique changes and whether the metric responds.
> Ours
> **Derived** — a metric defined as "the answer is present in the top k" returns the same
> value for every arrangement of the non-answer results, so it is invariant to their
> redundancy
> **Unknown** — whether MMR improves generated-answer quality on this corpus. It is
> measurable from week 8 and it is exactly the experiment this day should motivate
