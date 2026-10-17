# Every shard thinks it is the corpus

*Week 14 · Day 4 · about 20 minutes*

> By the end of this you can explain why splitting a BM25 index into shards changes its
> rankings, and the one extra step that changes them back.

---

## Sources

| Source | Tier | What it gives you |
|---|---|---|
| [**Elasticsearch reference**, Search API — `search_type`](https://www.elastic.co/guide/en/elasticsearch/reference/current/search-search.html) | 1 | `dfs_query_then_fetch`: gather term statistics from every shard before scoring |
| [**Elastic blog**, Practical BM25 part 1: how shards affect relevance scoring](https://www.elastic.co/blog/practical-bm25-part-1-how-shards-affect-relevance-scoring-in-elasticsearch) | 2 | The same finding, in the engine most people run |

---

## Scatter, gather

When an index outgrows one machine it is split. Each chunk goes to a shard by a hash of its
id, so every machine agrees where it lives; each shard is an ordinary index over its part;
a query is sent to every shard, each returns its top results with their scores, and the
results are merged by score.

It is how every large search system scales, and each shard does its job correctly.

---

## The statistics are split too

BM25 does not score a chunk on its own. It scores it relative to the corpus: how many
chunks contain the term — rarer terms count for more — how many chunks there are, and how
long a chunk is compared with the average.

A shard knows only its own chunks. A term that is rare across the corpus may be common in
one shard and absent from another; the average length differs shard to shard. So the same
chunk with the same words gets a different score depending on which shard it landed in and
who else landed there. The merge then compares scores computed on four different scales.

Measured with four shards: **25 of 26** top tens differ from the whole index's, and **5**
top results.

---

## Week 12, the other way round

Week 12's tombstones were dead chunks still voting in the statistics: the index's counts
described a corpus that was not the one being searched. Here every shard's counts describe
a corpus that is not the one being searched either — a quarter of it. Same mechanism, same
silence: every result is a real, relevant chunk, and nothing errors.

---

## Share the statistics

The fix is to give every shard the statistics of the whole. First ask each shard for its
document frequencies for the query's terms, its chunk count and its total length; add them
up; then send those totals back with the query and let every shard score with them.

That is one more round trip per query. In return, **none** of the 26 top tens differ, with
two shards, four or eight. The search engine most people run offers exactly this as an
option, off by default, because the round trip costs latency. Whether to pay it is a real
decision — and it is the decision between a sharded index and a different retriever.
