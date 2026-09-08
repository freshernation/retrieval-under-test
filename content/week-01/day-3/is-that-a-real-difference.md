# Is that a real difference?

*Week 1 · Day 3 · about 25 minutes*

> By the end of this you can look at "recall went from 0.61 to 0.64" and say whether
> anything happened.

---

## Sources

| Source | Tier | What it gives you |
|---|---|---|
| [**Efron & Tibshirani, *An Introduction to the Bootstrap***](https://www.routledge.com/An-Introduction-to-the-Bootstrap/Efron-Tibshirani/p/book/9780412042317) | 2 | The method, from the people who invented it |
| [**Smucker, Allan & Carterette, *A comparison of statistical significance tests for IR***](https://dl.acm.org/doi/10.1145/1321440.1321528) | 1 | Which test to use on retrieval results, tested on retrieval results |
| [**TREC overview papers**](https://trec.nist.gov/pubs.html) | 1 | The convention of paired testing over shared query sets |

---

## The problem, concretely

You change your chunker. Recall@10 on `dev` goes from 0.61 to 0.64.

Was that the chunker?

You have 96 queries. The change moved four of them from 0 to 1 and moved one from 1 to 0.
The mean shifted by three points on the strength of **five queries**, and if you had
happened to write five different queries in week 2, the number might have gone the other
way.

That is not a hypothetical objection. It is the normal situation with a hand-built eval
set, and it is why almost every improvement reported in almost every RAG blog post is
unverifiable — not wrong, unverifiable, which is a different and more annoying thing.

---

## Pair first, then resample

**Pairing.** The same queries are hard for both systems. Query 7 is hard because it is
badly worded, not because of your chunker, and that difficulty is present in both numbers.
So take the difference *per query* first, and analyse the differences. This removes the
shared variance and it is the single largest improvement you can make to a small-sample
comparison.

**Resampling.** You have one sample of 96 differences and you want to know how much the
mean would wobble if you had drawn a different 96. The bootstrap answers this by drawing,
with replacement, from the differences you have — ten thousand times — and looking at the
spread of the resulting means.

That spread is your confidence interval. The rule is one line:

> **If the interval contains zero, you did not measure an improvement.**

Not "the improvement was small". Not "it was probably real but underpowered". You have a
result consistent with no change, and the honest sentence is *"not distinguishable from no
change at n=96"*.

---

## What eight queries buys you

Almost nothing, and it is important to feel this in week 1 rather than discovering it in
week 6.

With eight queries, one query is 12.5% of the mean. A single query flipping produces a
12-point swing. The bootstrap interval on eight queries is enormous, and essentially every
change you make this week and next will be indistinguishable from noise.

That is not a reason to skip the interval. It is the reason to compute it: **it tells you
what your instrument can resolve**, and an instrument that cannot resolve a 5-point change
should not be used to justify a decision that hangs on 5 points. Compute it, read it, and
let it tell you your eval set is too small — which it is, and which is why it grows.

---

## Seed it

`random.Random(0)`. Always.

A confidence interval that moves when you rerun it teaches exactly the wrong lesson about
what confidence means, and it makes two runs of the same configuration disagree, which
makes your run ledger useless. Determinism is not fastidiousness. It is what makes the
comparison a comparison.

---

## What the interval does not cover

The bootstrap quantifies **sampling error over your queries, given your judgments**. It is
silent about everything else, and the everything else is larger:

- **Your judgments might be wrong.** The bootstrap assumes them. Your kappa from yesterday
  is the honest bound here, and it is not in the interval
- **Your queries might not be the queries users ask.** The biggest error in every
  production retrieval system, entirely outside this analysis, and not fixable with
  statistics
- **You might have run twenty configurations and reported the best.** Twenty comparisons at
  95% gives you one spurious "significant" result on average, for free. If you tried twenty
  things, say so — the number of things you tried is part of the result
- **The corpus is a sample too**, and nothing here resamples documents

An interval is a floor on your uncertainty, never a ceiling. Report it and stay suspicious.

---

## What to write down

Three numbers, every time, and the sentence is short:

> recall@10 rose from 0.61 to 0.64 on `dev` (`run:...` vs `run:...`), +0.03
> [95% CI −0.01, 0.07], n=96. **Not distinguishable from no change.** Five queries moved:
> four up, one down.

The last sentence is the one that stops you shipping. It is also the one nobody writes.

---

> **Known** — the paired bootstrap and randomisation tests are appropriate for IR
> comparisons and standard tests are not always (`smucker-2007`) · the bootstrap estimates
> sampling distributions by resampling (`efron-bootstrap`)
> **Inferred** — that on a hand-built set of a few dozen queries most reported RAG
> improvements would not survive an interval. This follows from the sample sizes involved;
> we know of no survey that has checked
> **Derived** — with n queries, one query flipping moves the mean by 1/n, so at n=8 a single
> query is 12.5% of the result
> **Unknown** — how to fold judgment uncertainty into the interval. It is not standard
> practice and the two sources of error are usually reported separately, or not at all
