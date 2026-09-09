# "Which is better" is the wrong question

*Week 5 · Day 3 · about 25 minutes*

> By the end of this you can produce the honest output of a comparison, which is a table
> and two numbers rather than a winner.

---

## Sources

| Source | Tier | What it gives you |
|---|---|---|
| [**BEIR**](https://arxiv.org/abs/2104.08663) | 1 | Eighteen datasets; lexical and dense trade places depending on the dataset |
| [**Lin, *The neural hype***](https://sigir.org/wp-content/uploads/2019/01/p040.pdf) | 1 | What happens when a field answers this question carelessly |
| [**Smucker, Allan & Carterette**](https://dl.acm.org/doi/10.1145/1321440.1321528) | 1 | What it takes to establish that one system beats another |

---

## The measurement

Two retrievers, same chunks, same queries, same metric:

| k | lexical | dense |
|---|---|---|
| 1 | 0.33 | 0.33 |
| **3** | 0.78 | **0.89** |
| **5** | **1.00** | 0.89 |
| 10 | 0.89 | 0.89 |

At k=3 dense wins. At k=5 lexical wins.

Same systems. Same corpus. Same queries. **Opposite conclusions, separated by a parameter
that is a property of neither of them.**

Any sentence of the form "dense beats BM25" is therefore incomplete without the k, and
almost every such sentence you will read this year omits it — along with the corpus and the
n.

---

## What to produce instead

**The head-to-head table.** For each query: both, lexical only, dense only, neither. Two
systems scoring 0.80 can agree on every query or disagree on every query, and the mean
cannot tell those apart, although they are completely different situations.

**The oracle**, which is every query either system gets. This is the **ceiling on fusion** —
combining them cannot exceed it however cleverly you do it.

**The headroom**, `oracle − max(a, b)`. If it is zero, the two systems are redundant on your
data and next week's whole subject cannot help you.

On this corpus, at nine dev queries:

| k | lexical | dense | oracle | **headroom** |
|---|---|---|---|---|
| 3 | 0.78 | 0.89 | 0.89 | **0.00** |
| 5 | 1.00 | 0.89 | 1.00 | **0.00** |

**Zero at both.** Whichever system is ahead already gets everything the other gets.

---

## Sitting with a negative result

That is not the result anybody wants going into a week on hybrid retrieval, and the right
response is not to reach for fusion anyway.

Two honest readings, and both are worth holding:

**Nine queries cannot show this.** Complementarity involving one or two queries in each
direction is invisible at n=9 — it is week 3's floor arithmetic again, and week 3's
milestone asked you to grow the eval set to thirty for exactly this kind of question. If you
did not, this is the cost, arriving on schedule.

**Or these two systems really are redundant here.** Ten technical documents, heavy shared
vocabulary, and an LSA space learned from that same small corpus — dense retrieval here is
built from the lexical statistics, so it is not obvious it *should* be independent. On a
corpus with genuine paraphrase and a trained model, the story is different, and that
difference is a claim we cannot test from inside this week.

What you must not do is conclude fusion works because everyone says so. **You have a
measurement that says it cannot help on your data, and the correct next step is a better
measurement rather than a better technique.**

---

## The family table, and its warning

Grouping by query shape is more stable than the mean, because it aggregates over the thing
that actually varies:

| family | n | lexical | dense |
|---|---|---|---|
| superseded | 2 | 0.50 | **1.00** |
| vocabulary-gap | 2 | 0.50 | 0.50 |
| identifier | 2 | 1.00 | 1.00 |
| acronym | 1 | 1.00 | 1.00 |
| plain | 2 | 1.00 | 1.00 |

Two things, in order of importance.

**Report `n`.** Every row is one or two queries. This table is suggestive and it is not
evidence, and a table without `n` invites everyone to forget that.

**The vocabulary-gap row ties.** That is the family dense retrieval exists for, and it does
not win it. Whatever else is going on, "dense fixes paraphrase" is not what this measurement
says.

---

## Why this is the hardest thing in the course so far

Improving one system is easy to know you have done: the number goes up on a held-out split.

Comparing two systems requires establishing that a difference is real, at a sample size
where one query is eleven points of the mean, when the ranking depends on a parameter, on a
corpus that is a sample of one.

**Most published RAG comparisons are doing this and not saying so.** Not through bad faith —
because the honest version's output is a table and a shrug, and a table and a shrug does not
make a blog post.

---

> **Known** — lexical and dense retrieval trade places depending on the dataset
> (`beir-2021`) · establishing that one retrieval system beats another requires paired
> testing at adequate sample size (`smucker-2007`) · careless comparison inflated a
> substantial share of published IR results (`lin-neural-hype`)
> **Inferred** — that headroom is the right thing to measure before attempting fusion.
> Ours; it follows from fusion's ceiling being the oracle
> **Derived** — fusion cannot exceed the oracle, so zero headroom means no fusion technique
> can improve on the better single system
> **Unknown** — whether the zero headroom here is a property of this corpus or of the sample
> size. We cannot distinguish them at n=9, and saying which is the honest report
