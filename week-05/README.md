# Week 5 — Embeddings, and what they are actually better at

> **Destination**
> Build a dense retriever from scratch, measure it against four weeks of lexical work, and
> be able to say precisely what each one is for.

You have waited four weeks for this and the fence has been holding you back on purpose.
Here is the thing worth knowing before Monday: **it is not an upgrade.**

Dense retrieval does not beat BM25 on this corpus. It wins some queries BM25 loses, loses
some BM25 wins, and which of them has the higher mean depends on a parameter that is a
property of neither.

---

## The week

| Day | Folder | What you'll be able to do |
|---|---|---|
| Mon | `day-1/` | Turn text into geometry, and prove the vocabulary gap is structural |
| Tue | `day-2/` | Change the axes, close the gap — and find the limit of doing it this way |
| Wed | `day-3/` | Compare two retrievers properly, and find out you cannot |
| Thu | `day-4/` | Build an approximate index, and see the error compound |
| Fri | `milestone/` | Ship a frozen dense retriever and an honest comparison |

---

## What this course uses for vectors, and why

There is no model here. Weeks 1 to 9 run **offline and deterministically** — no API key, no
network, no GPU — because a test whose result depends on a model's sampling is not a test,
and a course whose labs need a paid account is a course some students cannot take.

So the dense representation you build is computed from the corpus itself, by linear
algebra: **latent semantic analysis**, which is the direct ancestor of everything the field
now calls an embedding. Day 3's second article says exactly which of the week's findings
transfer to a trained model and which do not — because one of them does not, and it matters.

What transfers: the geometry, cosine similarity, the dimensionality trade, the
complementarity with lexical retrieval, the ANN mechanics, and every mistake in the
comparison. What does not: LSA cannot represent a word your corpus has never contained.

---

## Four findings, in order of how uncomfortable they are

**The vocabulary gap is structural.** In a one-axis-per-word space, two texts sharing no
term are *exactly* orthogonal — not nearly, exactly — however related they are. No
weighting scheme repairs that. It is a property of the axes.

**Changing the axes closes it.** `too many requests` and `rate limiting` go from cosine
0.00 to **0.73**, with nobody telling the system anything about synonyms. And a word your
corpus has never seen still scores 0.00, because this technique learns its axes from your
corpus and only from your corpus.

**You cannot say which retriever is better.** At k=3 dense scores 0.89 and lexical 0.78. At
k=5 lexical scores 1.00 and dense 0.89. Same systems, same corpus, same queries, opposite
conclusions. And the headroom for combining them is **zero at both** — on nine queries, the
complementarity everyone assumes is there is not visible.

**Approximation costs more than it says.** An index with ANN recall 0.53 — a number a
vendor reports — turns 0.89 answer recall into 0.78. Two different recalls, multiplied
together rather than chosen between, and only one of them is ever quoted.

---

## Milestone

A frozen dense retriever with a manifest, and a comparison honest enough to say it did not
settle anything. Spec in `milestone/README.md`.

---

## What this week is not about

Whether embeddings are better than keyword search. That question has no answer, and this
week is largely about learning to notice that it has no answer.

What it has instead: two systems, a table of where they disagree, and a number saying how
much a perfect combination of them could win. That number is next week's subject, and this
week's job is to find out whether it is worth spending a week on.
