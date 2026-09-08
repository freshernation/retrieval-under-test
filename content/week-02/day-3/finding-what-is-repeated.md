# Finding what is repeated

*Week 2 · Day 3 · about 25 minutes*

> By the end of this you can find near-duplicates in a corpus you cannot read, and say what
> the similarity score is actually measuring.

---

## Read the primary sources first

| Source | Tier | What it gives you |
|---|---|---|
| [**Broder, *On the resemblance and containment of documents***](https://www.cs.princeton.edu/courses/archive/spr05/cos598E/bib/broder97resemblance.pdf) | 1 | Shingling and MinHash, from the person who invented them, for exactly this problem |
| [**Leskovec, Rajaraman & Ullman, *Mining of Massive Datasets*, ch. 3**](http://www.mmds.org/) | 2 | The textbook treatment, including locality-sensitive hashing |
| [**CCNet**](https://arxiv.org/abs/1911.00359) | 1 | Deduplication as a stage in a real web-scale pipeline, with its effects reported |

---

## Why shingles and not words

Two documents about JSON share almost all their vocabulary whether or not either was
copied from the other. Bag-of-words similarity between RFC 7159 and RFC 8259 would be
enormous, and it would also be enormous between two independently written JSON tutorials.
It is measuring *topic*, and topic is not what you want.

A **shingle** is a contiguous run of k words. Sharing the exact sequence
`json text exchanged between systems that are not part of a closed ecosystem` is not
something two independent authors do. Order turns similarity into evidence.

`k` is a real choice with a real trade-off. Small `k` finds paraphrase and drowns in
coincidence; large `k` finds only verbatim copying and misses a document that was edited.
`k=5` is a common default and, like every common default in this course, it is worth
knowing that it is a default rather than a result.

---

## Jaccard

$$J(A, B) = \frac{|A \cap B|}{|A \cup B|}$$

Shingles in both, over shingles in either. In [0, 1]. Two empty sets are identical.

It has one property worth stating because it surprises people: **it is not containment.**
A one-page summary quoted verbatim inside a hundred-page document has a Jaccard similarity
near zero with it, because the union is enormous. If what you care about is "is this
document's content already present somewhere", Jaccard is the wrong measure and you want
containment — `|A ∩ B| / |A|` — which is asymmetric and which almost nobody reaches for.

---

## MinHash, and why it exists

You will not need MinHash on ten documents. Exact pairwise Jaccard over ten documents is
45 comparisons and runs instantly.

On ten million documents it is fifty trillion comparisons, and each one intersects two sets
of a hundred thousand shingles. That is the problem MinHash solves, and the trick is
genuinely elegant:

Hash every shingle to an integer, and take the **minimum**. The probability that two sets
have the same minimum is **exactly their Jaccard similarity** — because the minimum over
the union is equally likely to be any element of the union, and it is shared precisely when
that element is in the intersection.

One minimum is a coin flip. Do it with 128 independent hash functions and the fraction of
agreements estimates the similarity, with an error around `1/√n`.

So a set of a hundred thousand shingles becomes 128 integers, and comparing two documents
becomes comparing 128 integers. That is the whole idea.

### Two things that bite

**Use a stable hash.** Python's `hash()` on strings is salted per process, so a MinHash
index built in one run does not match signatures computed in the next. Nothing errors —
similarity just becomes zero everywhere, and a deduplication stage silently stops
deduplicating after a restart. Use `zlib.crc32`, or `hashlib`, or anything with a
documented value.

**Know your error.** On this corpus, 128 permutations estimates **0.500** where the exact
answer is **0.547**. That is the price, it is not a bug, and today is the only time you can
see it — at the scale where MinHash is necessary, the exact answer does not exist to
compare against. Measure the error once, while you can, so you know what you are buying.

---

## What the score does not tell you

This is the day's real lesson and the lab makes it unavoidable.

Two pairs in this corpus:

| Pair | Jaccard | Longest verbatim run |
|---|---|---|
| RFC 7159 / RFC 8259 | 0.547 | **222 words** — the specification |
| RFC 5785 / RFC 8615 | 0.204 | 68 words — **the IETF Trust copyright licence** |

Same measurement. Opposite meanings. One pair shares its subject matter; the other shares
its legal boilerplate and almost nothing else.

A similarity score compresses "how much" and discards "what", and acting on the number
without looking at the shared material is how a deduplication stage deletes a document for
having the same footer as another one.

`longest_shared_run` costs twenty lines. Run it on every pair you are about to act on.

---

## What cleaning did to this

The most interesting number in week 2, and it arrives from an unexpected direction.

| | pairs above 0.05 |
|---|---|
| raw corpus | **10** |
| cleaned corpus | **2** |

Eight of the ten "near-duplicate" pairs in the raw corpus were documents that share a
copyright notice, a `Status of This Memo` section and a table-of-contents structure. They
are not similar; they are RFCs.

And the real pair got *sharper* — 0.547 to 0.583 — because the boilerplate was diluting the
union.

So yesterday's cleaning, which could not be justified by any retrieval metric, transformed
this task completely. **The value of a change does not always appear in the task you had in
mind when you made it.** That is not a licence to make unmeasured changes; it is a reason
to measure more than one thing, and to hold a believed-in change rather than abandoning it.

---

## Where this is now

Deduplication is standard in language-model training pipelines, where duplicated training
data is known to hurt, and the tooling is mature and fast.

It is much less standard in retrieval corpora, where the consequences are different and
less studied: duplicated documents split the evidence for a query across several
near-identical results, waste a context window in week 7, and — as tomorrow shows — are
sometimes not duplicates at all but a version history that somebody has to make a decision
about.

---

> **Known** — shingling with MinHash estimates Jaccard similarity, with error falling as
> the square root of the number of permutations (`broder-1997`) · the probability of a
> shared minimum equals the Jaccard similarity (`broder-1997`, `mmds`)
> **Inferred** — that reporting `longest_shared_run` alongside a score prevents most
> mistaken deletions. Ours, from this corpus
> **Derived** — Jaccard is not containment: a short document quoted whole inside a long one
> scores near zero, because the union is dominated by the long document
> **Unknown** — how much duplication hurts retrieval, as distinct from training. The
> training-side evidence is strong and does not transfer automatically
