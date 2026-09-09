# Two recalls, multiplied

*Week 5 · Day 4 · about 20 minutes*

> By the end of this you can explain why a 95%-recall vector index does not give you a
> 95%-as-good system.

---

## Sources

| Source | Tier | What it gives you |
|---|---|---|
| [**Malkov & Yashunin**](https://arxiv.org/abs/1603.09320) | 1 | ANN recall as the field defines it: agreement with exhaustive search |
| [**FAISS documentation**](https://faiss.ai/) | 1 | Recall@k reported the same way, as an index property |

---

## They are different quantities

**ANN recall** — of the top k an exhaustive scan would return, how many did the index find?
A property of the **index**. Reported by every vector database.

**Answer recall** — did the answer reach the context window? A property of the **system**.
What the user experiences. Reported by nobody.

They are not the same number, they are not comparable, and — the part that matters —
**they are multiplied, not chosen between.**

---

## The measurement

On this corpus, at `nprobe = 1`:

| | |
|---|---|
| ANN recall@5 | **0.53** |
| Answer recall@5, exact search | 0.89 |
| Answer recall@5, this index | **0.78** |

An index finding "about half" of what brute force finds costs **eleven points of answer
recall** — one query in nine where the answer was in the corpus, was in the top 5 of an
exact search, and did not reach the context because of a configuration setting.

Notice how the losses relate. ANN recall of 0.53 does not become answer recall of
`0.89 × 0.53 = 0.47`, because the true nearest neighbours are not equally important — losing
the fifth-ranked chunk usually costs nothing and losing the first usually costs everything.
So the compounding is **real but not multiplicative**, and its size depends on your data.

Which means you cannot compute it. You have to measure it, end to end, on your own eval set.

---

## The sentence to have ready

> "Our vector database has 95% recall, so we're fine."

Two sentences back:

**That is 95% agreement with an exhaustive scan over the same vectors. It says nothing about
whether those vectors were the right answer, and it is a ceiling on your retrieval rather
than a floor.**

**And it composes with everything else that loses recall — the chunking that dropped an
answer, the embedding that blurred an identifier, the k that was too small — so the only
number worth quoting is the end-to-end one.**

---

## Where the losses accumulate

By week 5 you have seen five, and each has its own metric that looks fine on its own:

| stage | what is lost | week |
|---|---|---|
| corpus | a table the extractor flattened | 2 |
| chunking | an answer split by a boundary | 4 |
| indexing | an identifier blurred into a dense space | 5 |
| ANN | a true neighbour never examined | 5 |
| k | a chunk ranked sixth | 4 |

**Every one has a metric that can look excellent while the system fails.** That is the
argument for the answer-span metric and for measuring end to end: it is the only number that
composes, because it is defined on the outcome rather than on a stage.

This is the seven stations arriving as arithmetic. A per-station number tells you *where* a
failure is. Only the end-to-end number tells you *how much* there is.

---

## What to do

**Measure end to end.** Answer recall of the whole pipeline, at the k you will actually use,
on your own queries.

**Then attribute.** When it drops, walk the stations and find which one moved. That is what
per-stage metrics are for — diagnosis, not reporting.

**Never quote a stage metric as a system claim.** "95% recall" as a description of a
retrieval system is either a category error or marketing, and after this week you can say
which in a meeting.

---

> **Known** — ANN recall is defined as agreement with exhaustive search over the same
> vectors (`hnsw-2016`, `faiss-docs`)
> **Inferred** — that stage metrics compose in a way that makes each individually
> uninformative about the system. Ours; it is the seven-stations framing applied to
> measurement
> **Derived** — an index that omits some true neighbours can only reduce the answer recall
> of an otherwise unchanged pipeline, so ANN recall bounds system recall from above
> **Unknown** — how much answer recall a typical production ANN configuration costs. It is
> measurable in an afternoon with an answer-span eval set, and we have never seen it reported
