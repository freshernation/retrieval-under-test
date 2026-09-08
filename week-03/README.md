# Week 3 — Lexical retrieval, properly

> **Destination**
> Replace week 1's forty lines with the strongest lexical retriever there is, measure
> exactly how much it bought, and find out that your eval set is now the limiting factor.

The fence lifts. For two weeks you have been forbidden from touching the retriever, and
this week you rebuild it from the tokeniser up.

Three of the four defects you named in week 1 are repaired by about forty lines of
arithmetic that was fully understood by 1994. The fourth is not touched, and will not be
until week 5.

---

## The week

| Day | Folder | What you'll be able to do |
|---|---|---|
| Mon | `day-1/` | Build an analyzer, and find out that the classic improvements do not help |
| Tue | `day-2/` | Build an inverted index, and phrase search on top of it |
| Wed | `day-3/` | Build BM25, and watch three queries fix themselves |
| Thu | `day-4/` | Tune k1 and b, and find four reasons not to trust the result |
| Fri | `milestone/` | Ship the retriever, grow the eval set, then defend both |

---

## Monday's result is negative, and you should know that in advance

Removing stopwords makes recall **worse**. Stemming makes nDCG worse and breaks two
queries outright. Neither is a mistake in your code.

Both are crude approximations applied *before any evidence is available*: a stopword list
guesses that a term carries no information, and a stemmer guesses that two strings mean
the same thing. The one change on Monday that helps is the only one that **adds**
information rather than discarding it.

Then on Wednesday, one logarithm does properly what the stopword list was approximating.
`status` appears in all ten documents and scores 0.047; `429` appears in one and scores
1.992 — forty times the weight, derived from the corpus rather than guessed in advance.

**You cannot fix a scoring problem in the tokeniser.** That is the week's first half.

---

## The number you cannot escape

BM25 raises ndcg@3 from 0.651 to 0.805 and breaks nothing. It is the largest clean
improvement in the course.

The 95% interval's lower bound is **exactly zero**.

Not nearly zero — zero, and for a reason that is arithmetic rather than bad luck. Three of
your nine answerable dev queries improved and six were unchanged, so a bootstrap resample
that draws only unchanged queries has a delta of exactly 0. That happens with probability
`(6/9)⁹ = 0.0260`, which is just over the 0.025 that pins the 2.5th percentile.

At the same rate, **ten** answerable queries would have cleared it: `(2/3)¹⁰ = 0.0173`.

One more query. Judged by hand. In an afternoon.

> **The binding constraint on this week's result is not the retriever, the corpus, or the
> statistics. It is the size of your eval set** — and it took until week 3 to find that
> out, because you needed a retriever good enough to make the instrument the limitation.

That is what the milestone is for, and why it arrives now.

---

## Milestone

A tuned BM25 retriever, and an eval set grown to the size that can actually measure it.
Spec in `milestone/README.md`.

---

## What this week is not about

Beating a benchmark. Finding the best k1.

`k1=1.2, b=0.75` is the value in most of the literature and most search engines, and on
this corpus it places **38th out of 45**. That is not a scandal — those defaults were
chosen on collections of news articles and this is ten RFCs — and the lesson is not that
the convention is wrong. It is that you cannot know whether yours is any good without
doing the work, and that once you have done it, the answer is about your corpus and
transfers to nobody else's.
