# Week 5 — Concept fence

## Allowed

- Everything from weeks 1 to 4
- **Vector space**: term-document matrices, tf-idf weighting, L2 normalisation, cosine
  similarity, sparsity
- **Dimensionality reduction**: the singular value decomposition, truncation, variance
  kept, projecting a query into a reduced space
- **Comparison**: head-to-head tables, oracle recall, headroom, query families, and the
  fact that a winner can depend on `k`
- **Approximate search**: k-means clustering, inverted-file indexes, `nprobe`, ANN recall
  against brute force, comparison counts
- Freezing vectors with a manifest

## Not yet

**Fusion of any kind.** No combining lexical and dense scores, no reciprocal rank fusion,
no weighted sums, no "just take the union". You will want to on Wednesday afternoon and it
is next week · reranking and cross-encoders · query expansion or rewriting · language
models, for anything, including generating embeddings · prompts · agents · caching

---

## The rule that matters most this week

**No fusion until you have measured the headroom.**

Combining two retrievers is the obvious move and it is next week's whole subject. The
reason it waits is that fusion can only ever recover queries that **one system gets and the
other misses** — so if there are none of those, no fusion technique whatever can help, and
you can find that out in an afternoon before spending a week on it.

Wednesday's `headroom()` is that measurement, and on this corpus at nine queries the answer
is **zero at every k**. Sit with that rather than reaching for the technique anyway.

## The other rule

**Every comparison names its k.**

The winner flips between k=3 and k=5 on this corpus. Any sentence of the form "dense beats
BM25" is incomplete without the k, the corpus, and the n — and almost every such sentence
you will read this year omits all three.
