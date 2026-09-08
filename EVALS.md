# The measurement doctrine

Rule 1 in full: **no change without a measured delta**. This page says what counts as a
measurement, why the rule is stricter here than anywhere you have worked, and how it is
machine-checked.

---

## Why this exists

Retrieval is the field where intuition is worst. Ten reasonable engineers given the same
corpus will disagree about chunk size, they will each try their own, each will look at
five queries, and each will conclude they were right. All ten cannot be. The failure is
not that they lack taste — it is that a change to a retrieval system moves some queries
up and other queries down, and no amount of looking at examples tells you which effect
was larger.

**So the only honest claim is a claim with an aggregate number and a split attached.**

This is unusual to enforce. Most RAG writing, including most vendor writing, reports
improvements with no baseline, no eval set, no confidence interval, and no statement of
which queries got worse. Once you can see that, you cannot unsee it, and that is worth
more than any technique in this course.

---

## The four rules

**1. Every claim of improvement names a run — or, for a correctness fix, a measurement
showing it cost nothing.**

Say which kind of change you are making, in the report, every time.

A **tuning change** adjusts a parameter or heuristic to make the system score better —
chunk size, `k`, a fusion weight, a threshold. Its only justification is the number, so a
tuning change with no delta is superstition. Hold it.

A **correctness fix** repairs something wrong independent of any measurement: returning a
specification withdrawn in 2017 is wrong whether or not your eval set contains a query
that notices. The defect justifies the change; the measurement's job is to prove it cost
nothing, which is a question `Evaluation.worse_than` can answer on nine queries where an
interval cannot.

Three guards, so this is not a loophole: a correctness fix must name the defect **without
mentioning your metric**; `worse_than` must be empty; and the defect must be one a user
would recognise. "The obsolete spec outranks the current one" passes. "Chunks are not
aligned to section boundaries" does not — that is a hypothesis about retrieval quality,
which is a tuning change wearing a coat.

> *Amended 2026-09-09, while building week 2.* The rule as originally written would have
> forced the wrong answer twice in five days: it would have shipped a cleaning change on a
> +0.100 that was one query out of nine, and held a fix that stopped a withdrawn
> specification outranking its replacement. A rule that cannot be amended when it turns
> out to be incomplete is being recited rather than applied. See
> [`content/week-02/day-2/the-change-you-cannot-prove.md`](content/week-02/day-2/the-change-you-cannot-prove.md).

---

**Every claim of improvement names a run.**

In a milestone document, this is not acceptable:

> Switching to 400-token chunks with 50-token overlap improved retrieval.

This is:

> Switching to 400-token chunks with 50-token overlap raised recall@10 from 0.61 to 0.68
> on `dev` (`run:2026-09-08-a41c` vs `run:2026-09-08-9d02`, n=96, +0.07 [95% CI
> 0.02, 0.11]). Confirmed once on `test`: 0.66 (`run:2026-09-08-e7b1`). Eleven queries
> got worse; nine of them are the acronym queries, which is card F-014.

### The citation form is fixed

`tools/check_evals.py` does not guess at prose — a checker that guesses is a checker you
learn to write around. Every number that is checked is written like this:

```
recall@10 0.68 (run:2026-09-08-a41c)
```

metric, value, run id, in that order. Anything else in the sentence is yours. The checker
reads the ledger and fails when the number in prose disagrees with the run it names, when
the run does not exist, or when the run has no such metric.

**2. Name the split, and touch `test` once.**

`dev` is for tuning. `test` is for confirming, once per milestone. Every read of `test`
is recorded automatically by `raglab.runs`, and a milestone reporting `test` numbers from
more than one run that week fails the check.

You will want to bend this in about week 4, when your `test` number comes back worse than
`dev` and you are sure one more try would fix it. That feeling is the entire reason the
rule exists.

**3. Report what got worse.**

Every delta comes with the count of queries that regressed, and at least one of them
looked at by eye. An aggregate that improved while a class of queries collapsed is the
most common way a retrieval system gets quietly worse for the people who depend on it
most — and it is invisible in the mean.

**4. State the size of the thing you are claiming.**

`n`, and a confidence interval from `raglab.metrics.bootstrap`. On 96 queries, a
0.02 difference in recall@10 is noise, and week 9 makes you prove that to yourself. Until
then, the rule is mechanical: report the interval, and if it crosses zero, say the result
is not distinguishable from no change.

---

## What a run is

A run is one evaluation of one configuration against one split, recorded automatically:

```yaml
# runs/2026-09-08-a41c.yml
id: 2026-09-08-a41c
created: 2026-09-08T14:22:07
split: dev
n: 96
config_hash: 4f1a9c2b
config:
  retriever: bm25
  k1: 1.2
  b: 0.75
  chunker: fixed
  chunk_tokens: 400
  overlap_tokens: 50
metrics:
  recall@10: 0.6771
  ndcg@10: 0.4413
  mrr: 0.5120
regressions_vs: 2026-09-08-9d02
queries_worse: 11
```

You do not write these. `raglab.runs.record()` writes them when you evaluate, which is
deliberate: a ledger you have to maintain by hand is a ledger with gaps exactly where the
embarrassing results were.

---

## The metrics, and when each one lies

| Metric | Answers | Lies when |
|---|---|---|
| **recall@k** | is the answer anywhere in the candidates | k is large enough to hide a bad ranker |
| **nDCG@k** | is it near the top, weighted by how relevant | your judgments are binary — then it is just a fancier MRR |
| **MRR** | how far down is the *first* good result | the question needs several documents |
| **precision@k** | how much of what you returned was useful | most queries have fewer than k relevant documents, so it is capped below 1 and comparisons across queries mislead |
| **faithfulness** | does the answer follow from the retrieved text | week 8. It is judged by a model, and week 9 is about how much to trust that |
| **answer correctness** | is it right | almost never measurable without people. Say so |

**The station tells you which metric.** A station-4 failure is a recall failure; a
station-5 failure is an nDCG failure with recall already high; a station-6 failure shows
as low faithfulness with nDCG fine. This is most of the diagnostic, and it is why the
stations are numbered.

---

## Judgments

A relevance judgment is a human saying *this document answers this query*. The gold corpus
has them — [ten RFCs, sixteen queries, every grade written by reading the document and
falsifiable by you in fifteen seconds](data/gold/rfc/README.md). Your own corpus needs its
own, and week 2 is when you find out how long that takes.

- **Graded, not binary.** 0 irrelevant · 1 related · 2 answers it · 3 answers it
  completely and alone. nDCG needs the grades; recall collapses them to `>= 2`
- **Judge the document, not the system.** Never label by looking at what your retriever
  returned. That is how an eval set quietly becomes a description of the system it was
  supposed to test — the most expensive mistake in this course, and it is unrecoverable
- **Label a query before you run it.** Write down what you expect to be relevant, then
  search. The gap is the lesson
- **Mark the unanswerable ones.** A query the corpus genuinely cannot answer has no
  relevant document *on purpose*. Flag it `unanswerable: true` — it then stays out of every
  retrieval mean, because such a query still earns a non-zero nDCG for confidently
  returning something, which is the exact behaviour it was added to detect. What it
  actually measures is refusal, and that needs a generator: week 8
- **Measure your own disagreement.** Re-label 20 queries a week later without looking.
  If you disagree with yourself 15% of the time, no measured difference below 15% means
  anything, and now you know the floor

---

## What this doctrine cannot do

It cannot tell you whether the queries in your eval set are the queries people will
actually ask. That is the largest source of error in every retrieval system in
production, it is not fixable with statistics, and it is why week 12 is about the
report and the review rather than about a number.

An eval set is a model of your users. Say what it is a model *of*, and where you know it
is wrong, in the first paragraph of every report you write.
