# Semantically right, dimensionally useless

*Week 4 · Day 3 · about 20 minutes*

> By the end of this you can say why "chunk on headings" is advice that does not survive
> contact with a document, and what to do about it.

---

## Sources

| Source | Tier | What it gives you |
|---|---|---|
| — | — | No primary source. The packing rules below are ours |
| [**RFC 7322**](https://www.rfc-editor.org/rfc/rfc7322.txt) | 1 | The section conventions producing the distribution measured here |

---

## The distribution

Split this corpus on its headings and you get **286 sections**:

| | words |
|---|---|
| shortest | **2** |
| median | 116 |
| longest | **3,547** |

Seventy-one sections are under fifty words. Five are over eight hundred.

A spread of more than **a thousand times**, from a structure that is entirely correct.
Section 4 really is one idea and section 2.3.1.2 really is another; one of them is a
sentence and the other is fifteen pages.

> **Structure tells you where the boundaries are. It tells you nothing about size.**

Both failure modes are real. A two-word chunk consisting of a heading matches on that
heading and delivers nothing to a context window. A 3,547-word chunk is a fifth of your
budget in one result, and week 7 will show it is worse than that.

---

## Packing

Merge consecutive sections until they reach a floor; split any single section that exceeds
a ceiling.

Three rules, and the ordering of the flushes is where the bugs are:

**A section over the ceiling flushes the buffer first, then splits.** Appending a
3,547-word section to a half-full buffer and *then* splitting mixes unrelated material into
the first piece, and that piece is now a chunk about two things — which is precisely what
structure-aware chunking was supposed to avoid.

**A section that would push the buffer past the ceiling also flushes first.** Without this,
the ceiling is an aspiration rather than an invariant: a 131-word buffer plus a 250-word
section is 381 in a corpus configured for 300, and nothing complains. Ours did, until a test
caught it.

**Merging is only ever of consecutive sections**, so a chunk is always a contiguous span of
one document — which keeps `parent()` meaningful and keeps citation honest.

---

## The compromise you are making

Merging adjacent sections is a real cost and it should be named rather than waved past.

Section 4 and section 5 are *different topics*. A chunk containing both is less focused
than either, and its retrieval behaviour is a blend: it matches queries about both, ranks
below a dedicated chunk for either, and spends context on the half you did not want.

You are trading that against a two-word chunk that retrieves for nothing.

There is no principled place to draw that line, which is the same shape as everything else
in this week. What you can do is **measure both ends** and let the frontier decide, which is
tomorrow.

---

## The result

Sections packed to 100–300 words: **every answer in the top 5, for 984 words of context.**

Fixed 800-word windows: every answer in the top 5, for **3,648**.

Fixed 400-word windows — the recommended size — 78% of answers, for 1,926.

Identical coverage at a quarter of the cost, and the middle row loses a fifth of the
answers while costing twice as much as the winner.

Notice again what did *not* happen: structure-aware chunking did not retrieve an answer that
whole documents missed. **It is the same answers, cheaper.** That is the whole value, it is
a large value, and describing it as improved retrieval would be false.

---

## Why the sizes are what they are

`100–300` was not derived. It was measured against alternatives on the frontier, and the
honest statement is: on this corpus, with these queries, with BM25, at k=5, it is the
cheapest configuration reaching full coverage.

Change the retriever and it moves. Change the query length and it moves. Add ten thousand
documents and it moves.

**The number is not the deliverable. The procedure is** — audit, measure both axes, plot the
frontier, choose with a requirement — and that is what transfers to a corpus nobody has
written about.

---

> **Known** — RFC section conventions produce the measured distribution (`rfc7322`)
> **Inferred** — that structure gives correct boundaries and no size guarantee, so packing
> is required rather than optional. Ours, and the distribution above is the evidence
> **Derived** — merging without a ceiling check can exceed the ceiling by up to one
> section's length, so the ceiling is only an invariant if the check happens before the
> append
> **Unknown** — whether merging adjacent sections costs retrieval quality in a way that
> matters. It clearly costs focus; whether that shows up in a metric on a larger corpus we
> cannot say from ten documents
