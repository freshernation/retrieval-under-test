# What a reranker is

*Week 7 · Day 1 · about 25 minutes*

> By the end of this you can say what reranking can and cannot do, and compute its ceiling
> before writing one.

---

## Read the primary sources first

| Source | Tier | What it gives you |
|---|---|---|
| [**Nogueira & Cho, *Passage Re-ranking with BERT***](https://arxiv.org/abs/1901.04085) | 1 | The cross-encoder reranker, and the size of the gain it reported |
| [**Liu, *Learning to Rank for Information Retrieval***](https://link.springer.com/book/10.1007/978-3-642-14267-3) | 2 | The feature-based tradition a cross-encoder replaced |
| [**BEIR**](https://arxiv.org/abs/2104.08663) | 1 | Reranked pipelines against single-stage retrieval, across datasets |

---

## The architecture

Retrieval must be able to score every chunk in the corpus, so it embeds or indexes each one
**before it has seen the query**. That constraint is what makes it fast and what limits it:
a chunk's representation cannot depend on what is being asked.

A reranker is freed from that constraint because it only looks at `n` candidates. It can
read the query and the chunk **together**, which is a strictly richer thing to do.

```
retrieval:  score(chunk)          → cheap, over everything, query-blind representation
reranking:  score(query, chunk)   → expensive, over n, query-aware
```

That is the whole idea, and it is why a cross-encoder can beat a bi-encoder: it is not a
better model applied to the same problem, it is a model allowed to see more.

---

## The ceiling, and compute it first

Reranking **reorders**. It cannot introduce a chunk retrieval did not return.

$$\text{best possible recall at any } k \;=\; \text{recall at the shortlist depth}$$

Three lines, no model, and it tells you whether the rest of the day is worth doing.

On this corpus:

| | |
|---|---|
| answer recall at k=5 | 0.737 |
| answer recall over a 10-deep shortlist | **0.895** |
| available to a perfect reranker | **16 points** |
| at depth 20, 50 | still 0.895 |

Two things to take from that table.

**There is genuinely something to win.** Sixteen points is a large gain and this is the
honest case for the week.

**A deeper shortlist buys nothing past ten.** Which also caps what you should pay for: a
reranker over fifty candidates costs five times a reranker over ten and has the same
ceiling.

---

## What it costs

A cross-encoder scores every candidate individually, so cost is linear in shortlist depth
and each score is a full model call over query plus chunk. That is typically **one to two
orders of magnitude** more compute per query than the retrieval that produced the shortlist.

Which makes shortlist depth the whole engineering decision, and it is answerable from the
ceiling curve rather than by taste: depth 10 here, because depth 50 costs five times as much
for the same ceiling.

---

## Why yours will be a feature reranker

There is no model in this course, so you build the other kind: score `(query, chunk)` pairs
with hand-written features — idf-weighted term coverage, exact phrase presence, position of
the first match.

This is learning-to-rank, which was the state of the art for roughly fifteen years and which
cross-encoders replaced. It is a real technique, it is still used where a model is too
expensive, and today it will lose.

The reason it loses is the next article, and it is more interesting than "neural is better".

---

## The comparison people forget

A reranker is assumed to help. The comparison that matters is against **the un-reranked
shortlist**, at the same k, and it is skipped constantly — for the same reason week 6's
fusion was compared against the wrong input.

If you take one habit from this week: **`ceiling` first, un-reranked baseline second, and
only then a reranker.**

---

> **Known** — cross-encoders score query and passage jointly and improved over single-stage
> retrieval on the benchmarks their authors reported (`nogueira-2019`) · feature-based
> learning-to-rank preceded them (`liu-ltr`) · reranked pipelines improve over single-stage
> retrieval on several BEIR datasets (`beir-2021`)
> **Inferred** — that shortlist depth should be chosen from the ceiling curve rather than by
> convention. Ours, and it follows from the ceiling being flat past ten here
> **Derived** — reranking cannot introduce a chunk the shortlist omitted, so recall at the
> shortlist depth bounds any reranked result at any k
> **Unknown** — the cost-per-point of a cross-encoder in a given production setting. It is
> reported as latency by vendors and almost never as points of end-to-end answer recall
