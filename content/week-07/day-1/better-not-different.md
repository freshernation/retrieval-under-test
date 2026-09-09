# Better, not merely different

*Week 7 · Day 1 · about 25 minutes*

> By the end of this you can say why a sensible reranker made things worse, and what that
> implies about adding a stage to a pipeline.

---

## Sources

| Source | Tier | What it gives you |
|---|---|---|
| [**Nogueira & Cho**](https://arxiv.org/abs/1901.04085) | 1 | What supervision a cross-encoder is trained with |
| [**Robertson & Zaragoza**](https://www.staff.city.ac.uk/~sbrp622/papers/foundations_bm25_review.pdf) | 1 | What BM25 already encodes, derived rather than guessed |
| [**Lin, *The neural hype***](https://sigir.org/wp-content/uploads/2019/01/p040.pdf) | 1 | Comparing a new stage against a properly tuned baseline |

---

## The result

Sweep `alpha` from "features only" to "retriever only", at k=3:

| alpha | 0.0 | 0.3 | 0.5 | 0.7 | 0.9 | 1.0 |
|---|---|---|---|---|---|---|
| answer recall | 0.474 | 0.579 | 0.579 | 0.579 | 0.737 | **0.737** |

Monotone. The maximum is at `alpha = 1.0`, which is **the identity** — the retriever's
order, untouched.

Every amount of this reranker makes things worse or leaves them alone, with a sixteen-point
ceiling sitting right there.

---

## Why

Not because the features are silly. Idf-weighted coverage, phrase presence and early
mention are reasonable, and they are roughly what a 2010 learning-to-rank system used.

Because of what they are being compared against.

**BM25 is not a heuristic.** It is a derivation from a probabilistic model of relevance,
refined over three decades, with term saturation and length normalisation in it for reasons
that were argued about in print. **RRF is four pages of the same kind of care.** Between
them they are a *tuned, principled, and remarkably strong* model of relevance.

Three features written on a Monday are not a better model. They are a **different** one,
and different is not the bar.

> A reranker is not a stage you add. It is a **claim that you have a better model of
> relevance than your retriever**, and the claim needs evidence.

---

## Why a cross-encoder is different

Not because it is neural. Because of two things a hand-built reranker cannot have:

**It sees the pair.** `score(query, chunk)` with full attention between them — it can
represent "this chunk answers *this* question" rather than "this chunk contains these
terms". No feature you write by hand approximates that.

**It was trained on supervision you do not have.** Hundreds of thousands of human relevance
judgments. Your `coverage` weight of 1.0 and `phrase` weight of 0.5 were chosen by you, in a
minute, from nothing. Theirs were fitted.

So the honest summary is not "neural beats features". It is: **a reranker wins when it
encodes more evidence about relevance than the retriever does**, and the two ways to get
more evidence are a richer view of the pair and more supervision. A hand-built feature
reranker has neither.

---

## What to do about the ceiling

Sixteen points, untouched. Three plausible routes, in the order this course would try them:

**Rerank with a trained cross-encoder.** Most likely to work, and the thing to measure the
same way you measured this one.

**Fit the weights instead of guessing.** Deep track. With nineteen dev queries the fit will
overfit, and knowing that in advance is the exercise.

**Improve retrieval instead.** The ceiling is the *shortlist's* recall — raise that and the
ceiling rises. This is unfashionable and it is often the cheapest option, and week 6's
`unreachable` says exactly where it would pay.

---

## The rule this generalises to

Every stage in a RAG pipeline is assumed to help: chunking, reranking, deduplication, query
expansion, an agent loop. Each is a claim about improving on what came before, and each is
checkable in an afternoon against the configuration without it.

This week's milestone therefore defaults **every optional stage to off**, and requires a
measurement to turn one on. That is not scepticism for its own sake — it is the only way to
end up with a pipeline whose parts you can each justify, which is the difference between a
system and an accumulation.

---

> **Known** — cross-encoders are trained on large collections of human relevance judgments
> and score query and passage jointly (`nogueira-2019`) · BM25 derives from a probabilistic
> relevance model rather than being assembled from heuristics (`bm25-foundations`) ·
> improvements should be measured against a properly tuned baseline (`lin-neural-hype`)
> **Inferred** — that a reranker helps only when it encodes more evidence about relevance
> than the retriever, via a richer view of the pair or more supervision. Ours, and this
> day's negative result is the evidence for it
> **Derived** — if the best blend weight is the identity, the reranker's contribution at
> every other weight is negative
> **Unknown** — how much of the published cross-encoder gain survives against a *tuned*
> hybrid baseline rather than a single-stage one. Lin's question, unanswered for rerankers
