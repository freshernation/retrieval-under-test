# How big does an eval set have to be?

*Week 3 · Day 4 · about 25 minutes*

> By the end of this you can compute, exactly, the number of queries your eval set needs —
> and you will know why every interval this week touched zero.

---

## Sources

| Source | Tier | What it gives you |
|---|---|---|
| [**Smucker, Allan & Carterette**](https://dl.acm.org/doi/10.1145/1321440.1321528) | 1 | Which significance tests hold up on retrieval results |
| [**Efron & Tibshirani**](https://www.routledge.com/An-Introduction-to-the-Bootstrap/Efron-Tibshirani/p/book/9780412042317) | 2 | The bootstrap, and what a percentile interval is |
| [**Voorhees, TREC-8 overview**](https://trec.nist.gov/pubs/trec8/papers/overview_8.pdf) | 1 | Topic-set size in a collection built for the purpose: 50 |

---

## The observation

BM25 raised ndcg@3 from 0.651 to 0.805. Nothing got worse. It is the largest clean
improvement in the course.

The 95% interval's lower bound is **exactly zero**.

Not 0.003. Zero. And the exactness is the clue — a noisy estimate does not land on a round
number.

---

## The arithmetic

Nine answerable dev queries. Three improved. **Six were unchanged.**

The paired bootstrap resamples nine per-query differences with replacement, ten thousand
times, and takes the 2.5th percentile. Six of the nine differences are exactly 0.

So consider a resample that happens to draw **only** unchanged queries. Its mean difference
is exactly 0. The probability of that is

$$\left(\frac{6}{9}\right)^{9} = 0.0260$$

**0.0260 > 0.025.** More than 2.5% of resamples score exactly zero, so the 2.5th percentile
*is* zero, and the lower bound of a 95% interval is pinned there.

No improvement, however large, can lift it. You could have tripled ndcg on those three
queries and the interval would still have touched zero.

This is not a subtlety about statistics. It is arithmetic you can do on paper, and it
explains every interval you computed this week — and both of week 2's.

---

## Inverting it

If a fraction *f* of your queries are unchanged by a given change, the interval can only
exclude zero when

$$f^{\,n} < 0.025$$

| unchanged | queries needed |
|---|---|
| 50% | 6 |
| 67% | **10** |
| 75% | 13 |
| 90% | 36 |
| 95% | 72 |

`queries_needed(2/3)` returns **10**.

You have nine.

> **The binding constraint on this week's headline result is one query.** Not a bigger
> corpus, not a better retriever, not a cleverer statistical test. One more query, judged
> by hand, in an afternoon.

---

## Why this is the *floor* and not the answer

Everything above is the *best* case, and it is worth being clear that clearing the floor is
necessary rather than sufficient.

The floor asks only: *can the lower bound possibly be above zero?* It says nothing about
whether it will be. If your change moves three queries by a lot and leaves six alone, you
also need the moves to be large enough and consistent enough — and the smaller the effect,
the more queries you need on top of the floor.

The right way round: the floor is the number below which measurement is **impossible**.
The number at which it becomes *reliable* is larger, depends on effect size, and week 9
computes it properly. Between the two, you are measuring but not yet trusting.

Which is why the usual advice is 50 queries, and why TREC topic sets are 50. That is not a
magic number; it is roughly where a moderate effect becomes detectable at a typical
unchanged rate, and it has been the convention since the 1990s for that reason.

---

## The unchanged fraction is the thing to attack

Here is the part that changes how you build eval sets.

You can lower `n` by lowering `f`, and `f` is under your control. **A query that no change
ever moves contributes nothing to any comparison, forever.**

Four of this week's six unchanged queries were unchanged because they were *already
perfect* — `r03` (`451`), `r04` (418), `r05`, `r09`. Week 1's baseline got them right,
BM25 gets them right, and every retriever you build for the rest of the course will get
them right.

They are not useless: they are regression guards, and if a change ever broke one you would
want to know immediately. But they cannot **detect an improvement**, and an eval set made
mostly of them is an instrument that can only measure damage.

So a good eval set needs both, deliberately:

- **guards** — queries that must not break
- **discriminators** — queries at the edge of what your system can do, which move when
  something changes

And the second kind is the one that decides whether you can measure anything. When you grow
your set tomorrow, the temptation is to write more queries like the ones you have, because
those are the ones you know how to write. The valuable ones are the ones you expect to
fail.

---

## What this means for the milestone

Grow to **30 dev and 15 test**.

At 30, an unchanged fraction of two thirds gives a floor of `(2/3)³⁰ ≈ 5×10⁻⁶`, so the
floor stops binding entirely and the interval starts reflecting the actual effect size —
which is the point.

It is roughly a day of work. It will feel like the least productive day of the course, and
it produces more than the tuning did: the tuning bought seven points you cannot report, and
the queries buy the ability to report anything at all.

---

> **Known** — the paired bootstrap is an appropriate test for IR comparisons
> (`smucker-2007`) · a percentile interval takes empirical quantiles of the resampled
> statistic (`efron-bootstrap`) · TREC topic sets are conventionally around 50
> (`voorhees-trec8`)
> **Inferred** — that eval sets should be built deliberately from guards and
> discriminators, and that the discriminator count is what determines measurability. Ours
> **Derived** — with a fraction f of queries unchanged, a resample of n drawn with
> replacement is all-unchanged with probability f^n; when that exceeds 0.025 the 2.5th
> percentile of the difference distribution is exactly zero
> **Unknown** — the right size for a hand-built eval set in general. It depends on effect
> size, which depends on what you are about to try, which you do not know in advance
