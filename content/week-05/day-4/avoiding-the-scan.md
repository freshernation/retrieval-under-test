# Avoiding the scan

*Week 5 · Day 4 · about 25 minutes*

> By the end of this you can explain what a vector database is doing, and say when it is
> worth having.

---

## Read the primary sources first

| Source | Tier | What it gives you |
|---|---|---|
| [**Malkov & Yashunin, *HNSW***](https://arxiv.org/abs/1603.09320) | 1 | The graph-based index most vector databases actually use |
| [**Jégou, Douze & Schmid, *Product Quantization***](https://ieeexplore.ieee.org/document/5432202) | 1 | Inverted files plus compression — the other half of what FAISS does |
| [**FAISS documentation**](https://faiss.ai/) | 1 | The implementations, and their published trade-offs |

---

## The cost you are avoiding

`neighbours()` is one matrix multiply against every row: exact, simple, and **linear in the
corpus**.

- 266 chunks: instant
- 1 million: a few hundred milliseconds per query, per core
- 100 million: not a query, a batch job

Every vector database exists to break that linearity, and they all do it the same way: **do
not look at everything.**

---

## Inverted file, which is what you built

Cluster the vectors. At query time, find the nearest few cluster centroids and search only
those lists.

`nprobe` is the knob:

| nprobe | ANN recall | comparisons |
|---|---|---|
| 1 | 0.53 | 38 |
| 2 | 0.64 | 53 |
| 4 | 0.87 | 92 |
| 8 | 0.96 | 170 |
| 16 | 1.00 | 282 |

The shape is the useful part: **steep at the bottom.** Going from 1 to 4 probes nearly
doubles recall for two and a half times the work, and 8 to 16 buys four points for 66% more.
That is the same diminishing-returns shape as chunk size and dimensions, and it is chosen
the same way — a frontier, with a requirement.

### The failure mode you can see

Your cluster sizes run from **2 members to 34**. So probing one list examines somewhere
between 2 and 34 vectors depending on where the query lands, and the recall of a single
probe is wildly unpredictable per query.

This is the standard IVF problem and it is why more sophisticated structures exist. Graph
indexes such as HNSW avoid it by navigating a neighbourhood graph rather than partitioning
space, which gives much better recall at the same comparison count and costs more memory
and a slower build. That is the trade, and it is what most vector databases have chosen.

---

## And at this size it is slower

Probing all 16 lists costs **282 comparisons**: the 266 vectors plus the 16 centroids.
Brute force is 266.

**The approximate index is exact and slower than not having one.**

That is not a bug. An ANN structure is a bet that you have enough vectors for the saving to
exceed the overhead — the centroids, the memory, the build time, the recall you gave up —
and at 266 vectors you lose that bet decisively.

Two things follow, and the second is the one to carry into a vendor conversation:

**Build it to know what the service does.** Not to deploy it. A brute-force scan over
100,000 vectors is a few milliseconds and needs no index at all, and a great many systems
have an ANN index they do not need, tuned by nobody, quietly costing recall.

**Ask what corpus size a benchmark used.** A recall-versus-latency curve at a billion
vectors tells you nothing about your two hundred thousand, and the crossover — where an
index starts paying — is exactly the number nobody publishes.

---

## The rest of what a real index does

Beyond structure, in rough order of how much they change the numbers:

- **Quantisation.** Store 8-bit or 1-bit approximations of each dimension. 4–32× less
  memory, a few points of recall. This is where most of the real saving is, and it is the
  same trade as dimensions
- **Reranking the shortlist with exact vectors.** Retrieve 100 approximately, rescore them
  exactly, return 10. Recovers most of the lost recall for very little work, and is what
  every serious deployment does
- **Filtering.** Restricting to a metadata subset interacts badly with partitioned indexes —
  the filter may eliminate everything in the probed lists — and it is a real and
  under-discussed source of silent recall loss. Week 6 meets it properly

---

> **Known** — graph-based indexes such as HNSW give better recall per comparison than
> partition-based ones at higher memory cost (`hnsw-2016`) · inverted files with product
> quantisation are the other standard approach (`pq-2011`, `faiss-docs`)
> **Inferred** — that many deployed systems run ANN indexes at corpus sizes where brute
> force would be adequate. Ours, from the crossover arithmetic and from experience
> **Derived** — an IVF search at full `nprobe` performs `N + n_lists` comparisons, which
> exceeds brute force's `N`, so an exhaustively probed index is strictly slower
> **Unknown** — the corpus size at which an ANN index starts paying for itself in practice.
> It depends on dimensions, hardware and latency budget, and it is exactly the number
> vendor benchmarks do not report
