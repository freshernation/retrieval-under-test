# The graph and the scan

*Week 14 · Day 3 · about 25 minutes*

> By the end of this you can explain how a navigable small-world graph finds near
> neighbours, and why on a small corpus it does more work than reading everything.

---

## Sources

| Source | Tier | What it gives you |
|---|---|---|
| [**Malkov & Yashunin**, Efficient and robust approximate nearest neighbor search using HNSW graphs](https://arxiv.org/abs/1603.09320) | 1 | The algorithm: layers, greedy search, `M` and `ef` |
| [**FAISS wiki**, Indexing 1M vectors](https://github.com/facebookresearch/faiss/wiki/Indexing-1M-vectors) | 1 | What these indexes are for: corpora where a scan is the expensive part |

---

## Week 5's index, and the one everybody uses

Week 5 built an approximate index by clustering: put every vector in its nearest cluster,
and at query time look only in the few clusters nearest the query. It is simple, and its
recall falls off sharply when an answer sits near a cluster boundary.

The index inside most vector databases is a graph instead. **HNSW** — hierarchical
navigable small world — links each vector to a handful of its nearest neighbours. Search
starts somewhere and walks: from the current node, move to whichever neighbour is closer to
the query, and keep going until no neighbour is. To make the walk fast, there are layers.
Each vector appears on the bottom layer; a few also appear on the one above, fewer still
above that. The top layers have long links and few nodes; a search starts there, crosses
the space in a few steps, and drops a layer each time it gets stuck.

Two numbers control it. **M** is how many neighbours each node keeps (twice that on the
bottom layer). **ef** is how many candidates the search keeps while it walks: wider is
slower and finds more.

---

## The cost is distances

Wall-clock time on a laptop is mostly noise. The honest cost of a vector search is how many
distances it computes. A scan computes one per vector: 266 here, every query.

The graph, measured, with `M = 8`:

| ef | recall@10 | distances per query |
|---|---|---|
| 10 | 0.754 | 98 |
| 32 | 0.888 | 179 |
| 64 | 0.992 | **241** |
| 128 | 1.000 | 274 |

To agree with the scan ninety-nine times in a hundred, the graph reads **91%** of what the
scan reads, and gets the rest wrong some of the time. Asked for perfect recall, it reads
**more** than the scan — it visits nodes more than once on its way through the layers.

---

## Where it pays

Build the same graph over 2,000 random vectors and it reaches 0.978 recall reading about a
third of them. The overhead is roughly fixed and the scan grows with the corpus; somewhere
between a few hundred and a few thousand vectors the lines cross, and from there the graph
pulls away. At a million vectors it is not a choice.

At 266 it is a choice, and the right one is the scan. The point of building the graph by
hand is not that this corpus needs it; it is that you can now say, with a measurement, at
what size yours will.
