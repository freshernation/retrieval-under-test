# Two kinds of number

*Week 6 · Day 1 · about 25 minutes*

> By the end of this you can say why adding a BM25 score to a cosine is not fusion, and
> what every fix for it costs.

---

## Sources

| Source | Tier | What it gives you |
|---|---|---|
| [**Robertson & Zaragoza**](https://www.staff.city.ac.uk/~sbrp622/papers/foundations_bm25_review.pdf) §3 | 1 | What a BM25 score is: a sum of per-term evidence, unbounded |
| [**Manning, Raghavan & Schütze**](https://nlp.stanford.edu/IR-book/) ch. 6 | 2 | What a cosine is: an angle, bounded in [−1, 1] |
| [**Cormack, Clarke & Buettcher**](https://plg.uwaterloo.ca/~gvcormac/cormacksigir09-rrf.pdf) | 1 | The paper that gave up on making them comparable, and what it did instead |

---

## They are not the same kind of number

**A BM25 score** is a sum of per-term contributions. Unbounded above. Grows with query
length — a ten-word query scores higher than a two-word one against the same document, for
no reason connected to relevance. On this corpus's dev split it runs from **3.2 to 33.2**.

**A cosine** is an angle. Bounded in [−1, 1]. Does not grow with query length. Here it sits
between **0.2 and 0.8**.

Add them and the sum is `24.66 + 0.68`. The cosine is 2.7% of the total. Add them across
every query and you get a ranking that is **identical** to BM25 alone — not similar,
identical, at k=3, 5 and 10.

> You built a hybrid retriever with no dense component in it. It runs, it produces a
> ranking, and nothing errors.

This is the most common hybrid-retrieval bug there is, and it is invisible unless you
compare the fused ranking against each input — which is Wednesday.

---

## The fixes, and what each destroys

### Min-max, per query

Rescale each retriever's scores to [0, 1] within the query.

**What it destroys:** every query's top result becomes exactly **1.0**. A query where BM25
scored 24.7 with a 14% gap to the runner-up, and one where it scored 16.3 with a 2% gap,
are now identical at the top.

That gap was the only signal you had about how confident the retriever was. Min-max is the
one operation guaranteed to remove it, and it removes it from precisely the input a fusion
rule would want.

It is also **unstable at the bottom**: the lowest-scoring candidate in your shortlist
becomes 0.0, so the normalisation depends on how deep you cut. Change the depth and every
score changes.

### Z-score, per query

Standardise to mean 0, standard deviation 1.

Better in one way — the *shape* of the distribution survives. And it assumes the scores are
roughly symmetric around a mean, which retrieval scores are not: a handful of good matches
and a long tail of near-zeros. Standardising a skewed distribution puts the interesting
part in a narrow band and the tail everywhere.

### Both share a defect

`combine` treats a document missing from one retriever's shortlist as scoring **0.0**.

After normalisation, 0.0 is not "not measured" — it is the *worst possible result*. So a
chunk that one retriever ranked second and the other never saw is penalised as though the
second retriever had examined it and rejected it.

On a shortlist of 50 from a corpus of 266, most documents are missing from most lists. The
assumption is doing enormous work and it is wrong.

---

## Measured

| | k=3 | k=5 | k=10 |
|---|---|---|---|
| lexical alone | 0.684 | **0.789** | 0.842 |
| raw sum | 0.684 | 0.789 | 0.842 |
| min-max | 0.684 | 0.737 | 0.895 |
| z-score | 0.684 | 0.737 | 0.895 |

Raw sum is BM25 wearing a hat. Min-max and z-score are **worse at k=5 and better at k=10** —
two adjacent values, opposite verdicts, on nineteen queries.

None of this is a technique. It is a set of ways to make two incompatible numbers look
compatible, each with its own failure, none of them reliably better than using one
retriever.

---

## The move that follows

The 2009 RRF paper's contribution is mostly the decision to stop trying.

**Do not look at the scores.** Use only positions, which every retriever produces on the
same scale by construction: first is first, and it means the same thing on both sides
without any normalisation at all.

That gives up real information — a retriever that is *very* confident about its top result
and one that is barely separating its candidates produce the same rank 1. Tomorrow is
whether that trade is worth it, and the answer on this corpus is: at two values of k out of
three.

---

> **Known** — BM25 scores are unbounded sums of per-term contributions (`bm25-foundations`)
> · cosine is bounded in [−1, 1] (`mrs-irbook`) · RRF uses only ranks and outperformed the
> score-combination methods its authors tested (`rrf-2009`)
> **Inferred** — that min-max's destruction of the top-gap signal is its most important
> defect. Ours; the alternatives are enumerated above
> **Derived** — summing scores whose scales differ by an order of magnitude produces a
> ranking determined by the larger-scaled input alone
> **Unknown** — whether a well-designed score-aware fusion beats RRF on modern retrievers.
> The 2009 result is old, the retrievers have changed, and we have not seen it re-run
