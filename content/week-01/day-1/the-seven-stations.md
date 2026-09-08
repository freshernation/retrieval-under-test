# The seven stations

*Week 1 · Day 1 · about 25 minutes*

> By the end of this you can take a bad answer and attribute it to exactly one stage,
> and say why fixing anything downstream of that stage is wasted work.

---

## A note on where this comes from

**The seven stations are ours.** They are not from a paper, they are not standard
vocabulary, and nobody outside this course calls them this. Say "a station 4 failure" in
an interview and you will get a blank look — say "the document was never in the candidate
set" and you will not.

What they are is *an order to walk in*. The individual stages are entirely conventional;
the contribution, such as it is, is insisting that diagnosis starts at the corpus and moves
forward, and that you stop at the first break.

The course applies its own evidence rule to itself: this framing is Tier 3, it is us, and
you should argue with it.

---

## The seven

| Station | Produces | The failure it prevents |
|---|---|---|
| **1 Corpus** | what is in scope, what was dropped, where each document came from | answering from a corpus that never contained the answer |
| **2 Chunk** | the retrieval unit, and the reason it is that size | a chunk that can be found but cannot be answered from |
| **3 Index** | the representations — lexical, dense, structured | one representation asked to do every job |
| **4 Retrieve** | the candidate set, the filters, the fusion | tuning the ranker when the answer was never in the candidates |
| **5 Rank** | the final order, deduplicated, inside a context budget | right documents, wrong order, truncated away |
| **6 Generate** | a grounded answer, its citations, and its refusals | a fluent answer the sources do not support |
| **7 Measure** | the eval set, the metric, the run record, the gate | "it feels better" |

Each station's output is the next one's input. That is the only reason the order is
meaningful, and it is enough.

---

## The rule

> **Attribute the failure to exactly one station before you change anything. Walk 1 → 7,
> stop at the first station that failed, and never fix downstream of the break.**

"Exactly one" is doing real work. A bad answer usually has several things wrong with it,
and if you are allowed to name three you will name three, change three things, measure
once, and learn nothing. Naming one forces the question *which of these is upstream*, and
upstream is where the fix belongs.

### Worked example

**Query:** "what does ROCC stand for". **Answer:** a plausible paragraph describing an
operational body, not containing the words "Rail Operations Control Centre".

Walk it:

1. **Corpus** — is the glossary in the corpus? Yes. *Not station 1.*
2. **Chunk** — did the glossary survive chunking as a findable unit, or is it eleven
   one-line entries split across three chunks with no context? Check. Suppose it survived.
3. **Index** — is "ROCC" in the index as a token at all, or did a tokeniser lowercase and
   split it into something else? Check. Suppose it is there.
4. **Retrieve** — is the glossary in the top 50 candidates? **No.** *Stop here.*

Station 4. Every other observation about this answer is now irrelevant. The prose was
plausible; that is not a finding, that is what generators do with whatever they are given.
The citation was wrong; of course it was. There is exactly one thing to fix.

And notice what the natural fix would have been for somebody who did not walk it: rewrite
the prompt to say "if you do not know, say so". That change would make this answer *less
wrong* and it would not put the glossary in the candidate set, so the system still cannot
answer the question. This is the trap, and it is set at station 6 because station 6 is the
part you can see.

---

## Which metric belongs to which station

This is most of the diagnostic, and it is why the stations are numbered.

| Symptom | Station | Metric that shows it |
|---|---|---|
| The answer is not in the corpus at all | 1 | none — this is a coverage question, answered by looking |
| Retrieved passage is boilerplate, or half a sentence | 2 | low nDCG with human-obvious relevance; usually found by eye |
| Exact terms fail, paraphrases work (or the reverse) | 3 | per-query recall split by query family |
| Recall@50 is low | 4 | **recall@k** |
| Recall@50 is high, recall@5 is low | 5 | **nDCG@k**, with recall already high |
| Retrieval is right, the answer is not supported by it | 6 | **faithfulness** (week 8) |
| You cannot answer any of the above | 7 | you have no eval set. Start there |

**Recall high and nDCG low is the single most useful pair in this course.** It says: you
found the right documents and put them in the wrong order. That is a ranking problem, and
it is a completely different afternoon from a retrieval problem.

---

## Station 7 is not last

It is numbered seven because measurement is what you do *about* the other six, and it is
placed last because that is where people put it. In practice it comes first — week 1 is
station 7, and nothing else, for five days.

A system with no station 7 has no other stations either, in the sense that matters: you
cannot attribute a failure you cannot detect, and you cannot detect a failure you only see
in the six examples you happened to try.

---

## The order is the whole idea

There is nothing clever in this article. Corpus, chunk, index, retrieve, rank, generate is
just the pipeline, written down, which anybody could do.

What is not obvious — what people with a decade of experience get wrong weekly — is
**starting at the beginning when something breaks**. The instinct is to start where the
symptom is. The symptom is always at the end, because the end is the part that talks.

---

> **Known** — nothing in this article is a claim about the world requiring a source; the
> pipeline stages are conventional and uncontroversial
> **Inferred** — that attributing to exactly one station produces better debugging than
> naming several is our teaching experience, not a measured result
> **Derived** — a fix applied downstream of a break cannot repair the break, because the
> broken stage's output is the fixed stage's input
> **Unknown** — whether this ordering is the best diagnostic ordering. We know of no work
> comparing diagnostic procedures for retrieval systems
