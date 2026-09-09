# Five results, two documents

*Week 7 · Day 2 · about 25 minutes*

> By the end of this you can measure redundancy in a result set and apply the two standard
> fixes.

---

## Read the primary sources first

| Source | Tier | What it gives you |
|---|---|---|
| [**Carbonell & Goldstein, *The Use of MMR***](https://dl.acm.org/doi/10.1145/290941.291025) | 1 | Maximal marginal relevance, 1998, from the people who proposed it |
| [**Clarke et al., *Novelty and Diversity in IR Evaluation***](https://dl.acm.org/doi/10.1145/1390334.1390446) | 1 | Metrics that can actually see diversity, and why the usual ones cannot |
| [**Broder**](https://www.cs.princeton.edu/courses/archive/spr05/cos598E/bib/broder97resemblance.pdf) | 1 | Set-overlap similarity, from week 2 |

---

## What is in a top-5

Measure it rather than assuming:

| | |
|---|---|
| distinct documents in the top 5 | **2.4** |
| pairs sharing a parent document | **5.68 of 10** |
| mean pairwise word overlap | 0.139 |
| maximum observed pair overlap | **0.948** |

Five results. Two documents. More than half the pairs are two sections of the same RFC, and
somewhere in there is a pair 95% identical by word overlap.

That is not a retrieval failure. It is what you should expect: a document about caching has
several sections about caching, they all match a caching query, and the retriever is right
about every one of them.

It is, however, a **context window mostly spent saying related things twice** — and at
week 4's density of 0.24, you are paying for it.

---

## Deduplication

Walk the ranking and drop any chunk too similar to one already kept.

Conservative: it removes only near-identical text, so it cannot cost an answer unless two
chunks were nearly the same and only one carried the span.

On this corpus it **barely fires**. Redundancy moves from 0.139 to 0.134 at a threshold of
0.8, and 0.5 does no better.

That is worth pausing on, because the instinct is to assume the tool is broken. It is not:

> **A tool that does nothing is telling you your problem is not the one it solves.**

The redundancy here is not near-duplicate chunks. It is *different* sections of one document
being genuinely relevant, which `dedupe` correctly leaves alone.

---

## Maximal marginal relevance

Pick greedily, trading relevance against similarity to what is already selected:

$$\text{value}(d) = \lambda \cdot \text{rel}(d) - (1 - \lambda)\max_{s \in S}\text{sim}(d, s)$$

`lambda = 1` is the identity. Lower values buy diversity.

| lambda | redundancy | distinct docs | answer recall |
|---|---|---|---|
| baseline | 0.139 | 2.37 | 0.737 |
| 0.7 | 0.130 | 2.42 | 0.737 |
| 0.5 | 0.115 | 2.53 | 0.737 |
| 0.3 | **0.091** | **2.89** | **0.684** |

The knob does exactly what it says. Redundancy falls, document coverage rises, and at 0.3 it
starts costing answers.

Note the relevance term: you have an *order*, not comparable scores — week 6's lesson — so
`1 / (rank + 1)` stands in. That is itself a choice, and a different relevance function
would move the trade.

---

## When diversity actually matters

Three situations, and they are worth naming because none of them is "always":

**Multi-part answers.** A question needing facts from two documents. Five chunks from one
document cannot answer it however good they are.

**Ambiguous queries.** `451` could be the status code or the book. A diverse result set
covers both readings; a redundant one commits to whichever the retriever preferred.

**Exploration.** A user who does not know what they are looking for is served by breadth.

And one where it does not: **a single factual lookup with one right answer.** Diversity there
is pure cost, and most of this corpus's queries are that.

Which is why tomorrow's article is not about diversity at all. It is about the fact that
your metric cannot tell any of these situations apart.

---

> **Known** — MMR trades relevance against novelty with a single parameter
> (`carbonell-1998`) · diversity-aware evaluation requires metrics designed for it, distinct
> from standard relevance metrics (`clarke-2008`) · set-overlap similarity is the standard
> cheap comparison (`broder-1997`)
> **Inferred** — that redundancy here is same-document rather than near-duplicate, so
> deduplication is the wrong tool for it. Measured on this corpus; the generalisation is
> ours
> **Derived** — with 2.4 distinct documents in a top-5, at least three of the five chunks
> share a parent with another
> **Unknown** — what fraction of real query traffic benefits from diversity. It depends
> entirely on the query mix, and nobody measures it before enabling MMR
