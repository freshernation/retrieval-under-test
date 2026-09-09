# Week 7 — Ranking and the context budget

> **Destination**
> Turn a ranking into a context window: the right size, without redundancy, arranged
> deliberately — and know which of those three you can actually measure.

Six weeks have produced an ordered list. A generator does not consume an ordered list. It
consumes a **string of a certain size**, and everything between the two is this week.

---

## The week

| Day | Folder | What you'll be able to do |
|---|---|---|
| Mon | `day-1/` | Build a reranker, and find out it loses |
| Tue | `day-2/` | Measure redundancy, and find your metric cannot see it |
| Wed | `day-3/` | Replace `k` with a budget, and see what you are paying for |
| Thu | `day-4/` | Order the window, using a model you cannot check |
| Fri | `milestone/` | Ship a context assembler whose stages are off by default |

---

## Three negative results, and they are the content

**Reranking loses.** There is a genuine sixteen-point ceiling — answer recall at k=5 is
0.737 and over a ten-deep shortlist it is 0.895 — and a reranker built from three sensible
features captures **none** of it. Every blend weight is worse than or equal to doing
nothing, and the best `alpha` is the identity.

A reranker is not a stage you add. It is a **claim that you have a better model of relevance
than your retriever**, and three features you invented on Monday are not that.

**Diversity is unmeasurable here.** The top-5 contains 2.4 distinct documents and 57% of its
pairs share a parent. MMR fixes that — and answer recall is **identical** for every setting
that does not also hurt. A metric that asks "is the answer present" is structurally
indifferent to whether the other four chunks repeat each other, and the one query in this
corpus that could measure it is in the held-out split.

Unmeasurable is not unimportant. Reporting the first as the second is how a useful technique
gets abandoned.

**Position cannot be measured at all.** Not without a generator. Day 4 builds a stipulated
model, compares orderings under it, and refuses to quote a number.

---

## The one positive result

`k` was never a budget.

| budget | answered | density |
|---|---|---|
| 200 | 0.263 | 0.263 |
| 400 | 0.474 | 0.309 |
| 800 | 0.737 | 0.237 |
| 2000 | 0.789 | **0.098** |

Answered rises and flattens. **Density falls throughout.** At 2,000 words, nine tenths of
what you are paying for is not carrying the answer — and week 8 will show that the extra
1,200 words are not free in a second way.

Week 4 said chunking is a cost decision. This is the same frontier one stage later, on the
axis the generator actually charges for.

---

## Milestone

A context assembler with every stage **off by default**, and the measurements that justify
turning each one on — or not. Spec in `milestone/README.md`.
