# The step that buys nothing

*Week 10 · Day 4 · about 25 minutes*

> By the end of this you can find the spend in your pipeline that purchases no answers, and
> explain why no dashboard would have shown it to you.

---

## Sources

| Source | Tier | What it gives you |
|---|---|---|
| [**Liu et al.**, *Lost in the Middle*](https://doi.org/10.1162/tacl_a_00638) | 1 | Longer contexts are not monotonically better for the model that reads them |
| [**Google SRE Book**, ch. 6](https://sre.google/sre-book/monitoring-distributed-systems/) | 1 | Indicator versus diagnostic |

> There is **no primary source** for "how large should the retrieved context be". It is the
> same gap week 4 found for chunk size, one station along, and it is why this day measures
> rather than cites.

---

## The curve

Twenty dev queries, the same pipeline, one dial — week 7's word budget:

| budget | tokens/query | answered | tokens/answer |
|---|---|---|---|
| 200 | 93 | 0.20 | 372 |
| 400 | 375 | 0.50 | 834 |
| 800 | 885 | 0.70 | 1,264 |
| **1200** | **1,403** | **0.70** | 2,004 |
| 2000 | 2,445 | 0.80 | 3,260 |
| 4000 | 4,922 | 0.85 | 5,791 |

Look at 800 → 1,200.

**Tokens per query: 885 → 1,403.** Fifty-eight per cent more spend, on every request, for
as long as the setting stays where it is.

**Answered rate: 0.70 → 0.70.** Not a small gain. None.

This is not an optimisation opportunity. It is a setting that should be turned down, and
turning it down is free.

---

## Why nothing would have told you

Go through what a dashboard would have shown across that step.

| signal | 800 | 1200 |
|---|---|---|
| faithfulness | 1.00 | 1.00 |
| citations resolved | all | all |
| answer length | shorter | **longer** |
| latency | lower | slightly higher |
| answered rate | 0.70 | 0.70 — **and not computable live** |

The only signal that moved in a *bad* direction is latency, slightly, and the only signal
that would have revealed the truth is the one week 9 proved you cannot compute at serving
time. Meanwhile answer length went up, and week 9 measured answer length at AUC 0.45 —
chance — while also measuring that a padded answer scores **higher** on word-overlap
faithfulness.

So the 1,200-word setting makes the system cost 58% more, look slightly better on two
dashboard metrics, and answer no more questions. Everything about the observable surface
says it is fine or better.

That is the mechanism behind every over-provisioned RAG pipeline you will meet. Nobody
chose it. Somebody raised a number, nothing got worse, and nothing could have got better.

---

## Why the average cannot find it

The seductive summary is `tokens_per_answered` — cost per answer, which sounds exactly like
the right unit.

It climbs smoothly: 372, 834, 1,264, 2,004, 3,260, 5,791. No cliff. No signal. It rises
monotonically across a step where the true marginal cost is **infinite**.

The margin is what shows it:

| step | tokens per additional answered query |
|---|---|
| 200 → 400 | 1,411 |
| 400 → 800 | 2,038 |
| **800 → 1200** | **∞** |
| 1200 → 2000 | 20,850 |
| 2000 → 4000 | 24,768 |

Seventeen-fold between the cheap end and the dear end, and one step that buys none at any
price.

An average over a budget curve mixes the answers you were always going to get with the
answers the extra spend bought. The margin separates them, which is the only question a
spending decision asks. This is the same arithmetic as week 7's `answer_density` — 0.237 at
800 words, 0.098 at 2,000 — and the same arithmetic as the reranking ceiling. Compute the
margin before you buy, not the average after.

---

## And the dearest setting is the best one

4,000 words answers **0.85**, the highest number in the table, at 5.6 times the tokens of
800.

No measurement settles that. It needs a price, a request volume, and somebody's judgment
about what an unanswered question costs — and **none of those three live in your
repository**. Liu et al. suggests a further complication: a longer context is not reliably
better for the model that has to read it, so the retrieval-side gain at 4,000 words may not
survive contact with generation at all.

What the report owes is not a decision procedure. It is the curve, the margin, `waste`
turned down, and one sentence naming which of the three missing inputs you assumed.

---

> **Known** — model performance over long contexts is not monotonic in context length, with
> material degradation for information placed mid-context (`liu-2024`) · a signal that
> triggers work is an indicator and one that explains it is a diagnostic (`sre-book`)
> **Inferred** — that over-provisioned context budgets are the normal state of production
> RAG systems, because every observable signal either stays flat or improves when the
> budget is raised. Ours
> **Derived** — raising the budget from 800 to 1,200 words raises tokens per query from 885
> to 1,403, a 58% increase, while the answered rate stays at 0.70, so the marginal cost per
> additional answered query is infinite · the average cost per answered query rises
> monotonically across that same step and therefore cannot locate it · the marginal cost
> per additional answer is 1,411 tokens at the 200→400 step and 24,768 at the 2000→4000
> step, a factor of 17.6
> **Unknown** — the right context budget for any corpus. There is no primary source, as
> there was none for chunk size in week 4, and the gap is in the same place in the stack
