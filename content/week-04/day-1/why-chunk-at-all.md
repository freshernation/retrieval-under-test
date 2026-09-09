# Why chunk at all

*Week 4 · Day 1 · about 25 minutes*

> By the end of this you can say what chunking is for, and it is not what you think.

---

## Sources

| Source | Tier | What it gives you |
|---|---|---|
| [**Lewis et al., *Retrieval-Augmented Generation***](https://arxiv.org/abs/2005.11401) | 1 | The original architecture, which retrieves passages rather than documents, and does not say why |
| [**Robertson & Zaragoza**](https://www.staff.city.ac.uk/~sbrp622/papers/foundations_bm25_review.pdf) §3.2 | 1 | Length normalisation — the retrieval model's own answer to "documents are different sizes" |
| [**Liu et al., *Lost in the Middle***](https://arxiv.org/abs/2307.03172) | 1 | What a long context does to a model's use of it. Week 7's material, and the reason cost is not only money |

> **There is no primary source for how to chunk.** That is not an oversight in this table;
> it is the subject of tomorrow's second article and the defining fact about this week.

---

## The three reasons people give

**"Smaller chunks are more precise."** The idea being that a 400-word passage about
caching is a better match for a caching question than a 20,000-word document that mentions
caching once.

There is something to this and it is smaller than it sounds, because BM25 already has an
answer: length normalisation. Week 3's `b` parameter exists precisely to stop long
documents winning by having more chances to match. The retrieval model was handling this
before you chunked anything.

**"The model needs focused context."** True, and it is week 7's material rather than
week 4's — a model's use of long context degrades in measurable ways, and the degradation
is about position and quantity rather than about document boundaries.

**"It fits in the window."** This is the real one, and it is so mundane that it gets
mentioned last.

---

## What the measurement says

Retrieve whole documents from this corpus, take the top 3, and **every answer in the eval
set is in there.** Perfect coverage, with no chunking at all, using a retriever you have had
since Wednesday of week 3.

The context that produces is **22,943 words**.

Now chunk into sections of 100–300 words and take the top 5: still every answer, and
**984 words**.

Twenty-three times less. Identical coverage.

And across three days of measurement, **no chunking configuration retrieved an answer that
whole documents missed.** Several lost answers. None gained one.

> **Chunking is a cost decision.** You do it because 22,943 words is a bill you cannot pay
> — in tokens, in latency, and in a generator's attention. Not because it finds more.

---

## Why this is worth being pedantic about

Because the framing decides what you measure, and the wrong framing produces work that
cannot be evaluated.

If chunking is a *quality* improvement, you tune chunk size against nDCG, watch it wobble
by two points on a small eval set, and pick a winner from noise. That is what almost every
chunk-size table on the internet is.

If chunking is a *cost* decision, the question becomes: **how little context can I spend
and still have the answer in it?** That has two axes, an explicit requirement, and a
frontier — and it produces a decision you can defend to somebody who is paying for the
tokens.

It also tells you when to stop. There is no optimal chunk size to find, so there is no
search to run for ever. There is a frontier, you pick a point on it, and you go and do
something else.

---

## The three costs, and only one is money

**Tokens.** The obvious one. Twenty-three times the context is twenty-three times the
input cost, per query, for ever.

**Latency.** Long contexts are slower to transmit and slower to process, and this is the
one users notice.

**Attention.** The one that is not obvious and matters most. A model's ability to use
information in a long context is not uniform — material in the middle of a long window is
used less reliably than material at either end. So a 22,943-word context is not merely
expensive; it is *worse* than a good 984-word one, even though it contains strictly more.

That last point is week 7's, and it inverts the naive view completely: more context is not
weakly better and then expensive. It is expensive **and** can be actively worse.

---

## What you are trading against

Chunking is not free, and today's lab is about the cost that has nothing to do with
tokens.

Every chunk boundary is a place where something might be cut in half. A rule stated in one
sentence, split across two chunks, is present in neither — and it is then **absent from the
index at any k**, unrecoverable by any downstream stage. The answer is in the corpus and
your system cannot reach it.

That is the trade: fewer tokens against a risk of destroying an answer. It is a real trade
with a real failure mode, and today ends by demonstrating that **your current evaluation
cannot see either side of it.**

---

> **Known** — the original RAG architecture retrieves passages rather than whole documents
> (`rag-2020`) · length normalisation in the retrieval model already addresses documents of
> differing size (`bm25-foundations`) · a model's use of information in a long context
> varies with position (`lost-in-the-middle`)
> **Inferred** — that chunking is a cost decision rather than a quality improvement. Ours,
> and this week is the measurement behind it. It is a claim about this corpus that we expect
> to generalise and cannot demonstrate that it does
> **Derived** — if a configuration never retrieves an answer that a coarser one missed, its
> value cannot be in coverage, so it must be in cost
> **Unknown** — whether whole-document retrieval would still be perfect on a corpus of ten
> thousand documents. Almost certainly not, and the point at which it stops being is not
> something we can measure with ten
