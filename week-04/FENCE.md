# Week 4 — Concept fence

## Allowed

- Everything from weeks 1 to 3
- **Chunking**: fixed windows, overlap, structure-aware splitting on headings, packing
  small sections together and splitting large ones, chunk identity and parentage
- **Answer spans**: verbatim ground truth at chunk granularity, span survival, answer
  recall at k
- **Cost**: context words at k, the coverage/cost frontier, Pareto domination, choosing a
  point on a frontier
- Retrieval over chunks with week 3's BM25, and folding chunk rankings up to documents

## Not yet

Embeddings, vectors, cosine similarity, ANN, vector databases · semantic or
model-assisted chunking of any kind · hybrid retrieval and fusion · reranking ·
query expansion or rewriting · parent-document retrieval and context stitching —
that is week 7, and doing it now hides what chunking costs · summarising or rewriting a
chunk before indexing it · language models, for anything · agents · caching

---

## The rule that matters most this week

**No chunking decision without the cost number next to it.**

Every configuration you report carries **two** numbers: what fraction of answers reach the
context, and how many words that context is. Not one. A chunk size quoted with an nDCG and
no cost is the shape of every chunking recommendation on the internet, and it is
unactionable — the whole decision is a trade between those two axes.

This is the first week where the honest presentation of a result is a **frontier** rather
than a number, and the report is graded on that.

## The other rule

**Run the span audit before you run any retrieval.**

`broken_by` takes one pass over the chunk texts. No index, no queries executed, no model. It
catches the failure nothing downstream can repair — an answer split by a boundary is not in
the index at any k, and no ranker, reranker, prompt or model will ever put it back.

You will be tempted to skip it because it is not a measurement of anything working. That is
exactly why it is cheap and exactly why nobody does it.
