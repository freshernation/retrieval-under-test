# Factorising a corpus

*Week 5 · Day 2 · about 30 minutes*

> By the end of this you can explain how a matrix factorisation closes the vocabulary gap,
> and where it stops.

---

## Read the primary sources first

| Source | Tier | What it gives you |
|---|---|---|
| [**Deerwester et al., *Indexing by Latent Semantic Analysis***](https://asistdl.onlinelibrary.wiley.com/doi/10.1002/(SICI)1097-4571(199009)41:6%3C391::AID-ASI1%3E3.0.CO;2-9) | 1 | The technique, 1990, from the people who introduced it |
| [**Manning, Raghavan & Schütze**](https://nlp.stanford.edu/IR-book/) ch. 18 | 2 | The linear algebra, and latent semantic indexing as a retrieval method |
| [**Mikolov et al., *word2vec***](https://arxiv.org/abs/1301.3781) | 1 | Where this line of work went, and why co-occurrence is the common ancestor |

---

## The idea

You have a 266 × 4,273 matrix, 97.5% zero, where two texts sharing no term are exactly
orthogonal.

The singular value decomposition factors it:

$$W \approx U \Sigma V^{\top}$$

Each row of `Vᵀ` is a **direction in term space** — a weighted mixture of words. `Σ` says
how much of the matrix each direction accounts for. `U` says where each chunk sits along
them.

Keep the strongest `k` directions and throw the rest away. Now a chunk is `k` numbers rather
than 4,273, and — the part that matters — **the axes are mixtures of co-occurring words
rather than individual words**.

---

## Why that closes the gap

`too many requests` and `rate limiting` never appear in the same sentence. They appear in
the same *section* of RFC 6585, alongside `429`, `Retry-After`, `client` and `server`.

The factorisation has no notion of meaning and does not need one. It is looking for
directions that explain variance, and "the words that show up when this corpus talks about
being sent too much traffic" is such a direction, because those words co-vary across the
266 rows. Both phrases load onto it, so both land in the same region.

Measured, from 0.00 in the sparse space:

| pair | dense cosine |
|---|---|
| `too many requests` / `rate limiting` | **0.73** |
| `cookie expires` / `max age attribute` | 0.61 |
| `crawler` / `robots` | 0.58 |
| `case insensitive` / `uppercase lowercase` | 0.56 |

Nobody supplied a synonym list. **Co-occurrence in your corpus is the entire mechanism**,
and it is the same mechanism underneath word2vec and everything after it — the difference
is what gets fitted and on how much text, not the premise.

---

## Folding in the query

The query was not in the matrix, so it has no row in `U`. It is placed using the term
directions alone: `q @ Vᵀ[:k].T`.

This has a consequence worth stating, because it is the whole of tomorrow's honest half:
**the projection can only use terms that have columns.** A word your corpus never contained
has no column, so it contributes nothing, so the query is placed as though you had not typed
it.

`censorship` is a reasonable word for what RFC 7725 is about. It is not in this corpus. Its
dense similarity to `legal reasons` is **0.00** — the same as sparse, because for this
technique the word does not exist.

---

## Read the axes and be disappointed

Print the top terms on the first few directions. They are not concepts:

```
axis 0: cookie, uri, path, user, agent, attribute
axis 1: cookie, attribute, ietf, agent, user, internet
```

The strongest direction on this corpus is roughly "is this the cookies RFC", because RFC
6265 is the longest document and dominates the variance.

**LSA does not find topics.** It finds directions of variance, and on a small corpus that is
mostly "which document is this". The retrieval improvement is real and the interpretation
people put on it is mostly wishful. The same caution applies to every claim about what a
dimension of a modern embedding "means".

---

## The honest limit here

`dimensions_for(S, 0.90)` returns **191** — out of 266 chunks. Ninety percent of the
variance needs seventy percent of the directions.

There is not much redundancy in ten technical standards on adjacent subjects, and a
technique whose entire premise is exploiting redundancy therefore has little to work with.
That is why the dense retriever tops out at 0.87 against BM25's 0.93, and it is a property
of the corpus rather than a defect in the linear algebra.

A trained embedding model would not be limited this way, for one reason and one reason only:
it was fitted on far more text than you have. Tomorrow's second article separates what that
changes from what it does not.

---

> **Known** — latent semantic analysis factors a term-document matrix and truncates it, and
> was proposed to address vocabulary mismatch (`deerwester-1990`, `mrs-irbook`) ·
> distributional methods including word2vec rest on co-occurrence statistics
> (`mikolov-2013`)
> **Inferred** — that the strongest directions on a small corpus encode document identity
> rather than topic. Observed here; the generalisation is ours
> **Derived** — a term absent from the corpus has no column in the matrix, so it cannot
> contribute to a projected query vector and the query is placed as though it were not typed
> **Unknown** — how much of a modern embedding model's advantage is the training data volume
> versus the architecture. It is heavily studied and not settled, and it matters for whether
> a small-corpus practitioner should fine-tune or not
