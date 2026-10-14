# Embedded by which model

*Week 12 · Day 2 · about 25 minutes*

> By the end of this you can say what has to be re-embedded when a document changes, and
> why a chunk added to a dense index is not the chunk a rebuild would have produced.

---

## Sources

| Source | Tier | What it gives you |
|---|---|---|
| [**RFC 8259**](https://www.rfc-editor.org/rfc/rfc8259.html) | 1 | The revised document: it obsoletes RFC 7159 |
| [**FAISS wiki**, Special operations on indexes](https://github.com/facebookresearch/faiss/wiki/Special-operations-on-indexes) | 1 | That vectors can be added to and removed from a built index |

---

## The expensive step

Adding a chunk to yesterday's index cost a tokenisation. Adding one to a dense index costs
an embedding, and at any real scale embedding is the bill.

So the first question on a re-ingest is not "what is in the corpus now". It is **what is
in the corpus now that I have not already embedded.**

---

## Fingerprints

Hash each chunk's text. Keep the hash next to the vector. On re-ingest, hash again and
embed only where the hash is new.

Two details decide whether this works.

**Normalise before hashing, and say what you normalised.** Collapse whitespace, so that
re-wrapping a paragraph is free. Do not lowercase unless your embedding model does —
otherwise you are declaring two texts identical that your model would embed differently.

**Compare by content, not by id.** A chunk id is a position: `rfc-8259#8` is the ninth
chunk of that document. Insert one section near the top and every id after it shifts.
Compare by id and the whole document looks new.

---

## The demonstration: a revised document

RFC 8259 is RFC 7159, revised. Same specification, same structure, a handful of
corrections — including the UTF-8 one that `r05` has been tripping over since week 2.

Chunk both and compare the texts. Of RFC 8259's 21 chunks, **2** are identical to a chunk
of its predecessor.

That is the honest size of the saving. A corrected sentence changes its chunk. A changed
section boundary changes every chunk downstream of it. Fingerprinting a *revised* document
saves almost nothing, and the cases where it saves a great deal — an unchanged document
re-crawled, a corpus re-ingested after a pipeline restart — are the boring ones.

Both are worth knowing before you promise anybody an incremental-update cost.

---

## Folding in

Now the 19 chunks that are new. They need vectors.

In this course the embedding model is the basis week 5 fitted to the corpus. You have two
choices:

- **Refit** the basis on the whole corpus, new documents included. Every vector changes.
- **Fold in**: project the new chunks into the *existing* basis, exactly as a query is
  projected. Nothing already stored changes.

Fold-in is what every production system does, because its model is frozen: a new document
is embedded by the model that embedded the others. Nobody re-embeds a corpus because one
document arrived.

The consequence is in the vocabulary. The two arriving RFCs use **161 terms** the old
basis has never seen. A folded-in chunk is described without any of them. It has a
position in the space, and that position was computed from the words it happens to share
with documents written before it.

---

## Two different retrievers

Fold the two RFCs in, or refit on everything. Compare the top five for the twenty dev
queries.

| | |
|---|---|
| Identical result lists | 5 of 20 |
| Queries where a new document reaches the top 5, refit | 6 |
| Queries where a new document reaches the top 5, folded in | 10 |

A quarter of the lists agree. And the folded-in chunks turn up *more* often than the
refitted ones — they are not hidden by missing vocabulary, they are placed loosely, and
loose placement matches more queries.

**Do not read this as "fold-in is worse".** Measure recall on these twenty queries and the
two are within a few points in either direction. Week 9 worked out how many queries it
takes to detect a difference that size, and it is not twenty.

What the table does say is that they are **different systems**. The eval set you built
describes the refit. The system you will run after the first update is the fold-in. If you
have not re-measured since the corpus changed, your numbers describe a retriever you are
no longer running.

---

> **Known** — RFC 8259 obsoletes RFC 7159 (`rfc-8259`)
> **Inferred** — that a built vector index accepts added and removed vectors without a
> rebuild, which is what makes fold-in the default in practice (`faiss-wiki`)
> **Derived** — 2 of RFC 8259's 21 chunks are textually identical to a chunk of RFC 7159 ·
> the arriving chunks contain 161 terms absent from the old vocabulary · fold-in and refit
> return identical top-fives for 5 of 20 dev queries, and the arriving documents reach the
> top five for 10 queries folded in against 6 refitted
> **Unknown** — whether this gap says anything about a frozen neural embedding model, which
> has no corpus-fitted vocabulary to be missing words from. The direction may transfer. The
> size does not
