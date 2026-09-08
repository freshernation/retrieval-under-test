# Week 1 — Concept fence

## Allowed

- **The seven stations**: corpus, chunk, index, retrieve, rank, generate, measure — and
  attributing a failure to exactly one of them
- **Relevance judgments**: the four grades, what a query is, what a `qrels` file is,
  self-agreement, the difference between judging a document and judging a system
- **Splits**: dev and test, why they exist, what overfitting an eval set looks like
- **Metrics**: recall@k, precision@k, MRR, DCG and nDCG, computed by hand
- **Confidence**: the paired bootstrap, reading an interval, "not distinguishable from no
  change"
- **A retriever, in the plainest possible form**: split text on whitespace, count how many
  query words a document contains, sort by that count
- **Evidence tiers**: the four tiers, dates, conflicted sources, the claims ledger

## Not yet

BM25 and any weighting scheme · inverse document frequency · stemming, lemmatisation,
stopword lists · inverted indexes and postings · chunking of any kind · embeddings,
vectors, cosine similarity, ANN, vector databases · hybrid retrieval and fusion ·
reranking and cross-encoders · query expansion or rewriting · language models of any kind,
for anything, including writing your queries · prompts · agents · caching · anything with
a vendor's name on it

---

## The rule that matters most this week

**You may not use a language model to write, grade, or check a relevance judgment.**

Not for the obvious ones. Not for a first pass you will review. Not for "just checking
mine".

An eval set written by a model is a measurement of that model's opinion. Every number you
compute against it afterwards is precise, reproducible, and about nothing — and the
failure is undetectable, by you or anyone else, forever. There is no later point in this
course where you find out.

`ai/annotator.md` is the role that exists to help you here, and it is written to refuse
this specific request. Read why it refuses. That paragraph is the most important thing in
the `ai/` folder.

## The other rule

**No retriever before the eval set exists.**

You will want to build something on Monday. Everyone does. Building first means your eval
set gets written by looking at what your retriever returned, which is how an eval set
quietly becomes a description of the system it was supposed to test.

Order matters here in a way it does not later: **judgments, then metrics, then the
baseline.** Monday to Friday, in that order, on purpose.
