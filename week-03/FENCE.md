# Week 3 — Concept fence

## Allowed

- Everything from weeks 1 and 2
- **The fence on the retriever is lifted.** You may change tokenisation, scoring, and `k`
- **Analysis**: tokenisation, case folding, stopword lists, suffix stemming, keeping
  identifiers and compounds
- **The inverted index**: postings lists, positions, term frequency, document frequency,
  document length, boolean AND/OR, phrase search
- **BM25**: inverse document frequency, term-frequency saturation, length normalisation,
  k1 and b
- **Tuning**: grid search on `dev`, the spread across a grid, edge effects, the
  multiple-comparisons count
- **Sizing the eval set**: the unchanged fraction, the bootstrap floor, how many queries a
  result needs

## Not yet

Chunking of any kind — you are still retrieving whole documents · embeddings, vectors,
cosine similarity, ANN, vector databases · hybrid retrieval, score normalisation, fusion ·
reranking and cross-encoders · query expansion, rewriting, synonyms, or any thesaurus ·
language models, for anything · prompts · agents · caching

---

## The rule that matters most this week

**One change per run.**

You have four days of knobs and you may turn exactly one at a time. Analyzer options, k1,
b, k — each gets its own run id, its own delta, its own interval, its own `worse_than`.

The reason is not tidiness. Two of this week's changes move the metric in *opposite*
directions — removing stopwords makes recall worse, BM25 makes it much better — and a
student who turns both knobs at once sees a net improvement and concludes that stopword
removal helped. They will believe that for years. There is no later measurement that
corrects it, because nobody re-tests a thing they already believe.

Last week you could not change the retriever at all. This week you can change one thing at
a time. Week 4 lifts that too.

## The other rule

**`test` is read once. It was already the rule and this is the week it gets hard.**

You are about to run a forty-five-configuration grid search, and the winner will be a
number you chose *because* it won. The temptation to check it on `test`, adjust, and check
again is the strongest it will be all course — and the log records every read.
