# Week 2 — Concept fence

## Allowed

- Everything from week 1
- **The corpus as an object of study**: reading the raw text, page furniture, form
  feeds, running headers, front matter, boilerplate, blank-run structure
- **Extraction damage**: sentences split across a page boundary, structure the format
  destroyed, what an abstract is worth
- **Near-duplicates**: shingles, Jaccard, MinHash signatures, thresholds, and what a
  similarity score cannot tell you
- **Provenance and lineage**: parsing a metadata header, supersession, currency,
  annotating and demoting a result
- **Loss reporting**: per-document manifests, generated prose, coverage gaps

## Not yet

Chunking of any kind — you are still retrieving whole documents · BM25, IDF, term
weighting, saturation, length normalisation · stemming, lemmatisation, stopwords ·
inverted indexes · embeddings, vectors, cosine similarity, ANN · hybrid retrieval and
fusion · reranking · query expansion or rewriting · language models, for anything ·
prompts · agents · caching

---

## The rule that matters most this week

**You may not change the retriever.**

Not the scoring, not the tokeniser, not `k`. Week 1's forty lines are frozen, exactly as
you left them, all week.

This is a hard rule with a soft reason: every instinct you have when a result is bad
points at the retriever, and while that instinct is available to you, you will never
seriously investigate the corpus. Take the instinct away for five days and you will find
things you would not otherwise have looked for — a third of your text is furniture, two
of your documents are obsolete, seventeen sentences are cut in half, and one document is
in a completely different format from the other nine.

None of that is fixable at station 4. All of it changes what station 4 can possibly do.

## The other rule

**Every change this week ships with the number that says whether it helped — including
when the answer is no.**

You are going to make two substantial changes this week and neither of them will produce
a confidence interval that excludes zero. That is not a failure of the week; it is the
week. What you do about a change you believe in and cannot prove is the thing being
taught, and `week-02/day-4/test_w02_day4.py` ends by making the distinction you will need.
