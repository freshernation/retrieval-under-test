# The fact in the other document

*Week 11 · Day 3 · about 25 minutes*

> By the end of this you can fix the oldest trap in the corpus, and you will know what the
> fix turned out to be.

---

## Sources

| Source | Tier | What it gives you |
|---|---|---|
| [**RFC 8259**](https://www.rfc-editor.org/rfc/rfc8259.html) | 1 | Obsoletes RFC 7159 and reverses it on UTF-8 |
| [**Yao et al.**, *ReAct*](https://arxiv.org/abs/2210.03629) | 1 | Interleaving reasoning and retrieval: the multi-hop framing |
| [**Asai et al.**, *Self-RAG*](https://arxiv.org/abs/2310.11511) | 1 | Retrieval decided and critiqued during generation |

---

## The trap, finally

Week 2 found it. Week 6 watched retrieval walk into it. Week 8 watched the generator cite
it with a perfect faithfulness score. Week 10's attribution walk declared **no station
failed**.

`r05` asks whether JSON must be encoded in UTF-8. RFC 7159 says one thing. RFC 8259
obsoletes it in December 2017 and says the opposite about exactly this — and **RFC 7159 does
not know it has been obsoleted**, because a published RFC is never edited.

So the fact that makes the answer wrong is not in the document the answer came from. No
amount of better ranking reaches it, no chunking reaches it, no prompt reaches it, and no
faithfulness metric can see it, because the answer is faithful. It is the cleanest example
in the course of a failure that lives between documents rather than in one.

A second hop reaches it. Retrieve, notice that a retrieved document has been superseded,
retrieve again inside its successor. That is multi-hop retrieval and today it is eleven
lines with no model in it anywhere.

---

## First, the version everybody writes

`add_hop`: put RFC 8259's chunk in the context **next to** RFC 7159's. Present both, let
the reader judge. It is the humane design, it is what a careful person would do, and you
should run it before writing anything else.

**`citing_superseded` does not move.** Three queries before, three after.

The generator picks sentences by word overlap and the withdrawn document's chunk still
wins — it is longer, it is more on-topic, it was ranked first. Whatever you believe a real
model would do differently, the mechanism on display is general: **supplying the correction
is not the same as removing the error**, and nothing in the pipeline prefers one to the
other. Both chunks are in the context with equal standing.

`replace_hop` — drop the superseded document's chunks, insert the successor's — takes it to
**zero**. The difference is two list comprehensions.

### And one of them has to be about documents

A trap worth meeting. Remove only the stale chunks **present in the context** and the next
chunk of the same withdrawn document moves up into the freed budget. Four queries get
fixed, `r23` goes on citing RFC 7159, and the bug reads as a near miss rather than a
category error.

The unit of supersession is the **document**. The unit you noticed it on was a chunk.
Conflating them produces a fix that works four times out of five, which is the worst
possible score for a correctness fix.

---

## What the hop turned out to be

| strategy | citing superseded | answered | retrievals |
|---|---|---|---|
| baseline | 3 | 0.700 | 20 |
| second hop, replacing | **0** | 0.650 | **25** |
| week 2's `is_current` filter | **0** | 0.650 | 20 |

Identical outcomes. The multi-hop retrieval — trigger detection, successor resolution,
chain following, a second retrieval, a merge — produces exactly the numbers a one-line
metadata filter produces, at **1.25 times the retrievals**.

And the filter was available in week 2, before embeddings, before fusion, before any of
this.

**The agentic win is a metadata join.** That is not a criticism of multi-hop retrieval; it
is what multi-hop retrieval *is* when the relationship being hopped along is already a
field in your metadata. The hop's machinery — notice, resolve, re-retrieve — is a join
performed at query time instead of at ingest time, and a join performed at query time costs
a retrieval and arrives later.

Which gives the question to ask before building one: **which edge am I following, and is it
already a field?**

- If it is a field, filter or join at ingest. One line, no extra retrieval
- If it is derivable from a field, derive it at ingest. Week 2's forty lines bought this
  edge for the whole course
- If it is genuinely not in the data — a semantic relationship, a contradiction nobody
  recorded — then a hop is the only option, and it is worth its cost

Most of the edges people build hops for are in the first two categories. That is the useful
version of this finding, and it survives a real model.

---

## The trigger matters more than the hop

One operational detail with a factor of three in it.

Trigger on the **context** — the chunks that actually made it into the budget — and the hop
fires on **5 of 20** queries. Trigger on a deep shortlist and it fires on **15 of 20**,
because RFC 5785's `/.well-known/` boilerplate appears in almost everyone's top sixty.

Same hop, three times the cost, nothing extra fixed. The condition under which an expensive
stage runs is as much a design decision as the stage, and it is the one that gets written
last and never measured.

---

> **Known** — RFC 8259 obsoletes RFC 7159 and changes its UTF-8 guidance, and a published
> RFC is not edited to record its own obsolescence (`rfc-8259`) · interleaving reasoning
> steps with retrieval is the standard multi-hop formulation (`yao-2023`) · retrieval can be
> decided and critiqued during generation rather than once beforehand (`asai-2023`)
> **Inferred** — that multi-hop retrieval along an edge already present in metadata is a
> query-time join, and is therefore replaceable by an ingest-time one at lower cost. Ours,
> and measured here as identical outcomes at 1.25× the retrievals
> **Inferred** — that supplying a correction is not equivalent to removing the error, because
> both sit in the context with equal standing and nothing in the pipeline ranks truth. Ours
> **Inferred** — that the trigger condition for an expensive stage deserves as much
> measurement as the stage, and usually gets none. Ours
> **Derived** — `add_hop` leaves `citing_superseded` at three while `replace_hop` takes it to
> zero · dropping only the stale chunks present in the context fixes four queries of five,
> because the next chunk of the same document is promoted into the freed budget ·
> triggering on the context fires the hop on 5 of 20 queries against 15 of 20 for a deep
> shortlist
> **Unknown** — how many of the edges production systems build hops for are already fields.
> Every one we have been shown, which is not a sample
