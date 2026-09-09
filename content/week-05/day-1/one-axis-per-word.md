# One axis per word

*Week 5 · Day 1 · about 25 minutes*

> By the end of this you can say what a vector space model is, and prove that the
> vocabulary gap is a property of its axes rather than a tuning failure.

---

## Read the primary sources first

| Source | Tier | What it gives you |
|---|---|---|
| [**Salton, Wong & Yang, *A Vector Space Model for Automatic Indexing***](https://dl.acm.org/doi/10.1145/361219.361220) | 1 | The original, 1975. Documents as points, similarity as an angle |
| [**Manning, Raghavan & Schütze**](https://nlp.stanford.edu/IR-book/) ch. 6 | 2 | The textbook treatment, including tf-idf weighting and cosine |
| [**Furnas et al., *The vocabulary problem***](https://dl.acm.org/doi/10.1145/32206.32212) | 1 | Why two people rarely choose the same word — the measurement behind the whole week |

---

## The construction

Take every distinct term in the corpus and call it a dimension. This corpus has 4,273, so
every chunk is a point in 4,273-dimensional space, and its coordinate on the `429` axis is
how often it says `429`, weighted.

That is the whole idea, and it is fifty years old.

It buys two things immediately. Similarity becomes **geometry**, so all of linear algebra
is available — one matrix multiply scores a query against every chunk at once, which is why
this representation survived. And a query is just another point, so query and document are
finally the same kind of object.

---

## Weighting, and what has and has not changed

Raw counts would let a chunk win by saying `the` five hundred times, so weight as before:
`log(1 + tf) × idf`. Week 3's saturation and week 3's idf, in the simplest forms that have
them.

One thing has quietly changed and it is worth noticing. Your idf is now computed over
**chunks**, not documents. `429` was in 1 document of 10; it is now in a handful of 266
chunks, so its idf went **up**.

> **Chunking changed your scoring function without touching your scoring function.**

That is not a bug and it is not neutral. Every statistic BM25 depends on — df, average
length, N — is a property of the unit you index, and changing the unit changes all of them
at once. A week-3 tuning of `k1` and `b` is, strictly, no longer valid.

---

## Cosine handles the length problem for free

The dot product grows with vector length, so a long chunk beats a short one for having more
of everything. Divide by both lengths and you have the cosine of the angle: **direction
only** — which terms, in what proportion.

Which is week 3's length normalisation arriving from a completely different direction, and
with a real difference. `b` is a *parameter*: you chose 0.75, you could have chosen 0.4, and
week 3 spent a day on which. Cosine is not a parameter. It is full normalisation, always,
and you cannot dial it back without leaving the geometry.

Neither is better. It is a genuine loss of control that buys a genuine simplification, and
knowing which you have is the point.

---

## And now the problem

Compute the sparsity of your matrix. **97.5% of it is zero.**

Every chunk uses about a hundred of four thousand axes, so almost every pair of chunks is
*exactly* orthogonal — not nearly, exactly — because they share no term at all.

Sit with what that means. Cosine similarity between two texts sharing no word is **0.00**,
and 0.00 is the same number you get for two texts about completely unrelated things. The
representation cannot distinguish "unrelated" from "related, differently worded".

- `31-day pass` and `monthly pass`: **0.00**
- `too many requests` and `rate limiting`: **0.00**
- `crawler` and `robots`: **0.00**

Furnas's number from week 3 says this is the normal case, not the edge case: two people
choose the same word for the same thing 10–20% of the time.

> **The vocabulary gap is not a tuning failure. It is a property of the axes.** One axis per
> word means words are the only thing that can be similar, and no weighting scheme changes
> what the axes are.

That is why today's retriever — a perfectly respectable tf-idf vector space model — scores
0.87 against BM25's 0.93 and cannot be fixed by trying harder. Tomorrow changes the axes,
which is the only move available.

---

> **Known** — the vector space model represents documents as weighted term vectors compared
> by cosine (`salton-1975`, `mrs-irbook`) · spontaneous vocabulary agreement between two
> people is 10–20% (`furnas-1987`)
> **Inferred** — that cosine and BM25's `b` are the same idea with different control
> surfaces. Ours, and it is a framing rather than a result
> **Derived** — two texts sharing no term have a term-vector cosine of exactly zero,
> identically to two unrelated texts, so this representation cannot distinguish them
> **Unknown** — how much of real query traffic falls in the vocabulary gap. It depends
> entirely on whether users share vocabulary with the corpus's authors, which nobody
> measures before building
