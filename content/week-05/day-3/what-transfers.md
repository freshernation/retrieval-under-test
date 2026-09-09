# What transfers from LSA to a real model

*Week 5 · Day 3 · about 25 minutes*

> By the end of this you can say which of this week's findings survive contact with a
> trained embedding model, and which do not.

---

## Sources

| Source | Tier | What it gives you |
|---|---|---|
| [**Deerwester et al.**](https://asistdl.onlinelibrary.wiley.com/doi/10.1002/(SICI)1097-4571(199009)41:6%3C391::AID-ASI1%3E3.0.CO;2-9) | 1 | What you built |
| [**Karpukhin et al., *Dense Passage Retrieval***](https://arxiv.org/abs/2004.04906) | 1 | Trained dual encoders for retrieval, and what supervision buys |
| [**MTEB**](https://arxiv.org/abs/2210.07316) | 1 | Modern embedding models compared across tasks, including retrieval |
| [**BEIR**](https://arxiv.org/abs/2104.08663) | 1 | Zero-shot retrieval across eighteen datasets; where dense loses to BM25 |

---

## Be explicit about what you built

**Latent semantic analysis over your own corpus.** 1990, a truncated SVD of a term-chunk
matrix.

**Not** a trained neural encoder. Not fine-tuned. Not fitted on anything except the 266
chunks in front of you.

This course does it that way because weeks 1 to 9 run offline and deterministically — no
API key, no network, no GPU — and because a course whose labs need a paid account is a
course some students cannot take. The cost of that choice is exactly one thing, and this
article is about which one.

---

## What transfers

**The geometry.** Text as points, similarity as angle, cosine over normalised vectors, the
dot-product-on-unit-vectors identity. Identical.

**The dimensionality trade.** Rises, flattens, no elbow, choose on a frontier and not on
variance kept. Identical, and it is the same conversation as chunk size.

**The comparison machinery.** Head-to-head tables, oracle, headroom, families, and the fact
that a winner can flip with `k`. All of it applies unchanged, and it is the most valuable
thing this week produced.

**The ANN mechanics.** Clustering, `nprobe`, ANN recall against brute force, and the
compounding of two recalls. A trained model's vectors go into the same index.

**The failure on exact identifiers.** A rare token contributes almost nothing to a dense
representation of any kind, because it co-occurs with nothing. BEIR finds this for trained
models too — lexical retrieval remains stronger on entity-heavy and exact-match queries, and
it is the reason week 6 exists.

---

## What does not transfer

**One thing, and it is large.**

> **LSA cannot represent a word your corpus has never contained.**

`censorship` has no column, so it has no position, so it contributes nothing. Dense
similarity to `legal reasons` is 0.00 — identical to sparse.

A trained embedding model does not have this problem. It was fitted on far more text than
you have, so it places `censorship` sensibly without ever seeing your documents, and it
brings a notion of similarity that is not derived from your corpus's co-occurrence
statistics.

That is the single biggest practical difference, and it is why "just use an embedding model"
is usually right in production and is not available in a deterministic teaching lab.

---

## What might transfer and we cannot tell

Two results from this week that a trained model would plausibly change, stated as open
rather than settled:

**The vocabulary-gap family tied.** Dense did not win the family it exists for. A trained
model has a much better shot at it — but it might also fail differently, and we cannot
distinguish "LSA is weak" from "these two queries are hard" at n=2.

**Headroom was zero.** Our dense retriever is built from the same lexical statistics as
BM25, so it is not obviously an independent signal. A trained model is a genuinely different
signal and the headroom would plausibly be larger. Plausibly. Nothing here shows it.

Both belong in your report as open questions rather than as conclusions in either direction.

---

## What to do about it in real work

**Use a trained model.** For nearly any production system, a good off-the-shelf embedding
model beats fitting your own decomposition, and it is a lower-effort decision.

**Then apply this week's procedure to it unchanged.** Sweep the dimensions if the model
supports it, build the head-to-head table against BM25, compute the headroom, break it down
by family, and report the k. Every one of those steps is model-agnostic, and skipping them
is what most people do.

**And keep the lexical retriever.** BEIR's finding and yours agree: dense loses on exact
identifiers, and those are a large share of real queries in most domains. You are not
choosing. That is next week.

---

> **Known** — trained dual encoders improve retrieval over unsupervised methods given
> supervision (`dpr-2020`) · dense models underperform BM25 on several datasets, especially
> entity- and exact-match-heavy ones (`beir-2021`) · deployed embedding models are compared
> across tasks at fixed dimensionalities (`mteb-2022`) · LSA is a truncated SVD of a
> term-document matrix (`deerwester-1990`)
> **Inferred** — that the geometry, dimensionality trade, comparison machinery and ANN
> mechanics transfer unchanged while corpus-bounded vocabulary does not. Ours, argued from
> what each technique depends on rather than measured
> **Derived** — a term with no column in the matrix cannot contribute to a projected query,
> so out-of-vocabulary similarity is exactly zero
> **Unknown** — whether the zero headroom measured here would survive a trained model. We
> expect not, and this course cannot test it
