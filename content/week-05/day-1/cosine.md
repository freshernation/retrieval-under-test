# Cosine, and why not the dot product

*Week 5 · Day 1 · about 20 minutes*

> By the end of this you can say what each similarity measure ignores, and why the answer
> to "which is best" is "which do you want to ignore".

---

## Sources

| Source | Tier | What it gives you |
|---|---|---|
| [**Manning, Raghavan & Schütze**](https://nlp.stanford.edu/IR-book/) ch. 6 | 2 | Length normalisation and cosine, with the derivation |
| [**Salton, Wong & Yang**](https://dl.acm.org/doi/10.1145/361219.361220) | 1 | Similarity as an angle, from 1975 |

---

## Three measures, one difference

| measure | formula | ignores |
|---|---|---|
| dot product | `a · b` | nothing |
| cosine | `a · b / (‖a‖‖b‖)` | **length** |
| Euclidean distance | `‖a − b‖` | nothing, and it is dominated by length |

Cosine is the dot product with length divided out. That is the whole distinction, and it is
the right one for text for a specific reason: **length is mostly an artefact of how much
somebody wrote**, not of what they wrote about. A three-page section on caching and a
paragraph on caching are about the same thing, and the dot product prefers the section for
having more of everything.

Euclidean distance is worse than either for text — the distance between two documents is
dominated by their difference in length, so a short relevant chunk is "far" from a long
relevant one.

---

## The trick worth knowing

**On unit-length vectors, all three agree.**

If `‖a‖ = ‖b‖ = 1`, then `a · b` is the cosine, and `‖a − b‖² = 2 − 2(a · b)`, so ranking by
Euclidean distance and ranking by cosine give the same order.

This is why every vector index normalises on write and then uses the dot product: it is one
multiply-accumulate per dimension with no division, it runs on hardware built for it, and it
is exactly cosine. When a vector database says it supports "inner product" and "cosine" as
separate metrics, the difference is whether it normalises for you.

The practical consequence is a real bug class: **store unnormalised vectors, query with
"inner product", and you have silently ranked by length.** It returns plausible results,
they are systematically biased towards long chunks, and nothing errors. This is why
`raglab.vectors`' manifest carries a `normalised` flag.

---

## What cosine ignores that you might want

Being clear about the cost, because the loss is real.

**Magnitude as confidence.** A chunk mentioning `429` twenty times and one mentioning it
once point in similar directions. Cosine says they are similar; a user looking for the
authoritative treatment would disagree. BM25's saturation makes exactly this judgment and
cosine gives it up.

**Length as information.** A one-sentence chunk and a three-page chunk on the same subject
are not equally useful for a context window, and cosine cannot tell them apart. Week 7
brings length back as an explicit budget.

**Absolute scores.** Cosine is in [−1, 1] and comparable *within* one query. It is not
comparable across queries, and it is not a probability. `0.8` means nothing on its own —
week 6 opens with this, because it is the reason you cannot simply add a cosine to a BM25
score.

---

## The zero vector

A query whose every term is unknown produces the zero vector, which has no direction, so
cosine is undefined.

Return 0.0 and return no results. The alternatives are worse in instructive ways: `nan`
propagates through a matrix multiply and poisons every score in the batch, and returning
the arbitrary first `k` rows gives the user confident irrelevant results for a query the
system genuinely cannot process.

That last one is the shape of every hallucination in week 8, arriving early and in linear
algebra.

---

> **Known** — cosine is the dot product with length normalised out (`mrs-irbook`,
> `salton-1975`) · on unit vectors, cosine and Euclidean ranking coincide (`mrs-irbook`)
> **Inferred** — that magnitude-as-confidence is a real loss rather than a curiosity. Ours,
> from the contrast with BM25's saturation
> **Derived** — for unit vectors, `‖a − b‖² = 2 − 2(a·b)`, so minimising distance is
> maximising cosine and the two rankings are identical
> **Unknown** — how often production systems query unnormalised vectors with an inner-product
> metric. It is silent, it biases towards long chunks, and we know of no way to detect it
> from outside
