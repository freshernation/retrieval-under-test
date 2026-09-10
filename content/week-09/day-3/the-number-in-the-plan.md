# The number that goes in the plan

*Week 9 · Day 3 · about 25 minutes*

> By the end of this you can say, before running an experiment, whether it could possibly
> answer your question.

---

## Read the primary sources first

| Source | Tier | What it gives you |
|---|---|---|
| [**Cohen, *Statistical Power Analysis***](https://doi.org/10.4324/9780203771587) | 2 | Power analysis, and the argument that it belongs before the experiment |
| [**Smucker, Allan & Carterette**](https://dl.acm.org/doi/10.1145/1321440.1321528) | 1 | Which tests hold up on retrieval results |
| [**Voorhees, TREC-8**](https://trec.nist.gov/pubs/trec8/papers/overview_8.pdf) | 1 | Topic-set size in a collection built for the purpose: 50 |

---

## Week 3's floor was necessary and not sufficient

Week 3 found that with six of nine queries unchanged, the bootstrap's lower bound was pinned
at zero — `(6/9)⁹ = 0.026`, just over 0.025 — so **no improvement, however large, could be
confirmed.**

That said when measurement is *impossible*. It did not say when it is *reliable*, and the
gap between those two is where most experiments live.

---

## The sufficient version

Paired differences, their standard deviation, and one formula:

$$\text{MDE} = \frac{z \cdot \text{sd}}{\sqrt{n}}$$

The smallest difference a comparison at this size can distinguish from zero.

On this corpus, comparing fusion against lexical at k=5:

| | |
|---|---|
| n | 19 |
| paired sd | **0.223** |
| **minimum detectable effect** | **0.1003** |

Even a ten-point difference is fractionally below the line.

---

## The square

Invert it and the cost of precision becomes visible:

$$n = \left(\frac{z \cdot \text{sd}}{\text{effect}}\right)^2$$

| detect | queries |
|---|---|
| 10 points | 20 |
| 5 points | **77** |
| 2 points | **479** |

**Halving the effect quadruples the queries.** Which means "we will add a few more queries"
is not a plan, and a 2-point improvement is genuinely expensive to prove rather than merely
tedious to prove.

It also reframes what a small improvement is worth. If proving a 2-point gain costs 479
hand-judged queries, and you have 19, then either the gain is large enough to see or the
work is labelling rather than modelling. That is a resourcing conversation and it should
happen before the modelling, not after.

---

## Why the spread is so large

`sd = 0.223` is high for a quantity bounded in [0, 1], and the reason is the metric.

Answer recall is **binary per query**: 0 or 1. So per-query differences are −1, 0 or +1, and
the spread is near the maximum a bounded quantity can have.

A graded metric — nDCG, or a partial-credit answer score — has smaller per-query differences
and therefore a smaller sd, and therefore needs fewer queries for the same MDE.

**That is an argument for nDCG that has nothing to do with which metric is more meaningful.**
It is worth knowing, and it is worth not letting it decide alone: a graded metric that
measures the wrong thing precisely is not an improvement.

---

## The habit

Compute the MDE **before** the experiment.

If the effect you are hoping for is smaller than it, the experiment cannot answer your
question. Running it anyway costs a week and produces a number, and the number will be
quoted, because a number in a report is a number in a report.

`power_table` is the artefact: sizes down the side, effects across the top, detectable or
not in the cells. It goes in the report *before* the results, where it is free. Afterwards it
is a retraction.

---

## And the audit

Go back through this course:

| week | claimed | MDE at that n |
|---|---|---|
| 2 cleaning | 0.111 | 0.100 |
| 6 fusion | 0.053 | 0.100 |
| 7 reranking ceiling | 0.158 | 0.100 |

Week 6's fusion gain — the whole week's headline — was **never distinguishable from zero**.

The course said so at the time, every time, by reporting the interval alongside the delta.
That is the entire reason this table is a summary rather than a confession, and it is what
the discipline was for.

---

> **Known** — power analysis belongs before an experiment, and required sample size scales
> with the inverse square of the effect (`cohen-1988`) · paired testing is appropriate for
> retrieval comparisons (`smucker-2007`) · evaluation collections conventionally use around
> fifty topics (`voorhees-trec8`)
> **Inferred** — that a graded metric requires fewer queries than a binary one at equal MDE,
> because per-query differences are smaller. Ours, from the sd of a binary difference
> **Derived** — with sd 0.223 and z 1.96, detecting 0.05 requires 77 queries and detecting
> 0.02 requires 479
> **Unknown** — how many published RAG improvements are below the MDE of the sets they were
> measured on. The sample sizes are usually reported; the standard deviations are not
