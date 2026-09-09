# Week 6 — Hybrid, and what fusion can and cannot do

> **Destination**
> Combine two retrievers, prove the combination beats both of them, and know exactly which
> failures it cannot touch.

Week 5 ended at a wall: the headroom between lexical and dense retrieval was **zero at
every k** on nine dev queries, so there was no measurable case for this week at all.

That was not a property of the retrievers. It was the eval set, and the first thing this
week does is fix it.

---

## The week

| Day | Folder | What you'll be able to do |
|---|---|---|
| Mon | `day-1/` | Grow the instrument, and watch score-based fusion turn into BM25 |
| Tue | `day-2/` | Fuse by rank, and find out what the paper's constant costs |
| Wed | `day-3/` | Deliver a verdict, including the one where fusion loses |
| Thu | `day-4/` | Filter, and find out that where you put it changes the answer |
| Fri | `milestone/` | Ship — or refuse to ship — a hybrid retriever |

---

## The instrument grows, and the old one is kept

`data/gold/rfc/queries-extended.yml`: the sixteen queries you have plus **ten more dev
queries**, chosen to stress the two retrievers in opposite directions — bare identifiers,
and paraphrases sharing almost no vocabulary with the corpus.

The old file is **not edited**. An eval set that grows is a *new instrument*, not a
corrected one, and results taken with the two are not comparable. Weeks 1 to 5 keep the set
they measured against, and keeping both files is what makes that visible rather than
silent.

With nineteen answerable dev queries the headroom is no longer zero.

---

## Three verdicts from one technique

| k | lexical | dense | fused | verdict |
|---|---|---|---|---|
| 3 | 0.684 | 0.684 | **0.737** | beats both, captures **all** the headroom |
| 5 | **0.789** | 0.737 | 0.737 | **worse than lexical alone**, at every c and every weighting |
| 10 | 0.842 | 0.789 | **0.895** at c=10 · 0.842 at c=60 | the constant decides everything |

**Fusion is not free.** Mixing a weaker signal into a stronger one dilutes it, and a fused
ranking that beats *one* input is a worse version of the other.

And the default constant matters as much as the method: at k=10, `c = 60` — the value in
the original paper and in every implementation — captures **none** of the available
headroom.

---

## The finding that outranks all of it

Break the result down by query family and one row does not move:

| family | n | lexical | dense | fused |
|---|---|---|---|---|
| identifier | 4 | 1.00 | 1.00 | 1.00 |
| vocabulary-gap | 4 | 0.75 | 0.75 | **1.00** |
| **paraphrase** | 3 | **0.33** | **0.33** | **0.33** |

At k=3, k=5 and k=10. At every constant. Under every weighting.

Two queries — *"how do I stop search engines indexing my site"* and *"what part of a web
address comes after the hash"* — are retrieved by **nothing**. The answers are in the
corpus.

> **Fusion combines what your retrievers found. It cannot conjure what neither of them
> did.** Every point of headroom you chase is a point that is not here, and a week spent
> tuning `c` is a week not spent on the family that is actually failing.

The fix is not a better retriever. It is changing the query, and that is week 11.

---

## Milestone

A hybrid retriever with a gate that refuses to ship it when it loses. Spec in
`milestone/README.md`.
