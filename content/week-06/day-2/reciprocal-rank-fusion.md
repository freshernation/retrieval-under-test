# Reciprocal rank fusion

*Week 6 · Day 2 · about 25 minutes*

> By the end of this you can implement RRF, and say what its constant controls in terms you
> can defend.

---

## Read the primary source first

| Source | Tier | What it gives you |
|---|---|---|
| [**Cormack, Clarke & Buettcher, *Reciprocal Rank Fusion outperforms Condorcet and individual Rank Learning Methods***](https://plg.uwaterloo.ca/~gvcormac/cormacksigir09-rrf.pdf) | 1 | Four pages. The formula, the experiments, and the constant — read all of it |
| [**Manning, Raghavan & Schütze**](https://nlp.stanford.edu/IR-book/) | 2 | Rank aggregation in context |
| [**Elastic and OpenSearch RRF documentation**](https://opensearch.org/docs/latest/) | 1 | The formula as shipped, and the defaults you will inherit |

---

## The formula

$$\text{score}(d) = \sum_{r \in \text{retrievers}} \frac{1}{c + \text{rank}_r(d)}$$

That is all of it. A document's score is the sum of the reciprocals of its positions, with
a constant added to each denominator.

Three properties follow immediately, and they are why it works:

**It never looks at a score.** Positions are on the same scale by construction — first is
first — so there is nothing to normalise and nothing to destroy.

**Absence contributes nothing rather than a penalty.** A document missing from one list
simply gets no term from it. Contrast yesterday's `combine`, where a missing score became
0.0 and actively harmed the document.

**It is monotone and bounded.** A document in both lists always beats the same document in
one, and no single retriever can dominate by having a bigger scale.

---

## What `c` actually controls

The constant is the only knob and it is almost always left at 60. State it as a ratio and
it stops being mysterious:

$$\text{flattening}(c) = \frac{1/(c+1)}{1/(c+10)} = \frac{c+10}{c+1}$$

| c | first place is worth this much more than tenth |
|---|---|
| 1 | **5.5×** |
| 10 | 1.8× |
| 20 | 1.4× |
| 60 | **1.15×** |
| 200 | 1.04× |

So `c` is a statement about **how much you trust a retriever's ordering versus the bare
fact that it returned the document at all.**

Small `c`: position matters, a retriever's top result carries real weight.
Large `c`: position barely matters, and the fusion is close to counting how many retrievers
returned each document.

At `c = 60` first place is worth 15% more than tenth. That is a strong vote for "being
returned is what counts", and the paper chose it on TREC runs in 2009 where the individual
systems' orderings were noisy.

**Your retrievers are not those retrievers.**

---

## What it buys here

| k | lexical | dense | oracle | RRF |
|---|---|---|---|---|
| 3 | 0.684 | 0.684 | 0.737 | **0.737** — all of it |
| 5 | **0.789** | 0.737 | 0.789 | 0.737 — *worse than lexical* |
| 10 | 0.842 | 0.789 | 0.895 | **0.895** at c≤20 · 0.842 at c=60 |

Two of three k values: fusion reaches the oracle exactly, which is the best any combination
could do.

One of three: **fusion is strictly worse than one of its own inputs**, at every constant
and every weighting, including one favouring lexical two to one.

---

## Why fusion can lose

It is worth being clear, because "combining two signals cannot hurt" is a very natural
belief.

At k=5, lexical alone gets fifteen of nineteen queries. Dense gets fourteen, and they are
not the same fourteen — but they overlap heavily. Fusion promotes documents both retrievers
liked, which usually helps and sometimes displaces a document that **one** retriever was
right about and the other had no opinion on.

At k=3 there is room for the disagreements to matter. At k=10 there is room for everything.
At k=5, on this data, the dilution costs more than the complementarity pays.

> **Mixing a weaker signal into a stronger one is not free.** It is a trade, its sign
> depends on k, and the only way to know is to measure against every input.

---

## Weights

RRF extends to weights trivially — multiply each retriever's contribution — and it is worth
noting what the sweep found: at k=5, *every* weighting loses to lexical alone, including
(2, 1). Only (1, 0) — which is to say, not fusing — matches it.

A weight sweep is not a rescue for a fusion that should not happen.

---

> **Known** — RRF combines rankings by summing reciprocal ranks with an additive constant,
> and outperformed the score-combination and learned methods its authors tested
> (`rrf-2009`) · c=60 is the paper's value and the default in deployed implementations
> (`rrf-2009`, `opensearch-docs`)
> **Inferred** — that c is best understood as a first-versus-tenth ratio. Ours, a
> presentation rather than a result
> **Derived** — the flattening ratio is (c+10)/(c+1), so c=60 makes first place worth 1.15
> times tenth
> **Unknown** — whether c=60 is a good default for modern lexical-plus-dense pairs. It was
> chosen for 2009 TREC runs and, as far as we can find, has never been re-derived
