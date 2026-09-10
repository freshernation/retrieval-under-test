# Two lines before you trust it

*Week 9 · Day 2 · about 25 minutes*

> By the end of this you can tell a judge that has learned something from one that has
> learned nothing, in two lines of arithmetic.

---

## Sources

| Source | Tier | What it gives you |
|---|---|---|
| [**Cohen, *A coefficient of agreement for nominal scales***](https://doi.org/10.1177/001316446002000104) | 1 | Chance-corrected agreement, 1960 |
| [**Zheng et al.**](https://arxiv.org/abs/2306.05685) | 1 | Judge-human agreement rates, and how they are reported |
| [**Voorhees, TREC-8**](https://trec.nist.gov/pubs/trec8/papers/overview_8.pdf) | 1 | Why raw agreement is the wrong statistic when one class dominates |

---

## The measurement

The judge scores twenty answers. **It labels all twenty "good".**

| | judge | a judge that always says yes |
|---|---|---|
| accuracy | **0.70** | **0.70** |
| Cohen's kappa | **0.000** | **0.000** |

They are indistinguishable. The judge read the answers and arrived at exactly the
performance of a function that returns `True`.

And 0.70 would have looked respectable on a slide.

---

## Why accuracy alone cannot be interpreted

Fourteen of twenty answers are good. So a constant "yes" is right 70% of the time **for free**,
purely from the class balance, before any judgment is involved.

Any accuracy figure is therefore uninterpretable without the base rate beside it. On a set
that is 95% good, a judge scoring 0.94 is *worse than useless* and the number looks excellent.

**Cohen's kappa** fixes exactly this:

$$\kappa = \frac{p_{\text{observed}} - p_{\text{chance}}}{1 - p_{\text{chance}}}$$

Agreement beyond what the class balance gives you for free. A constant judge scores 0. A
perfect one scores 1.

You wrote this function in **week 1, day 2**, to measure whether you agreed with yourself
about relevance. It is the right tool here for the same reason: when one class dominates, raw
agreement is high by construction.

---

## Why this judge fails

It is a **faithfulness** judge, and week 8 established that all twenty answers are faithful —
the generator copies from its context, so every claim is supported.

Six of the twenty are confident prose about questions the system could not answer. They are
faithful *and* wrong, and a judge measuring the answer-to-context relation cannot see it.
Putting a model in the loop did not change that; it changed who is confidently telling you
the answers are fine.

> **A model judge inherits the blindness of whatever it was asked to judge.** Ask about
> faithfulness and you get faithfulness, with a model's authority attached and no more
> information than the word-overlap proxy had.

---

## The bar, and it is low

`validated()` checks three cheap conditions:

1. **Kappa beats the constant baseline.** Two lines
2. **Self-agreement at least 0.95** on labels across runs
3. **Not length-sensitive**, by the padded-pair probe

A judge passing all three is **not known to be good**. It is *not known to be useless*, which
is a much lower bar than the one people assume when they start quoting its scores.

This judge fails the first, so nothing else about it matters.

---

## What to do with a judge that fails

**Ask it a different question.** A faithfulness judge cannot detect wrongness. A judge asked
*"does this answer the question that was asked?"* is a different measurement, and the right
one for the failure that dominates here. Change the question before changing the model.

**Use it where the bias cancels.** Comparing two systems on the same queries is much safer
than scoring one absolutely.

**Use it to triage.** Surfacing the worst 5% for a human is valuable even from a judge whose
absolute scores are worthless.

**Do not gate on it.** Not until kappa clears the baseline by a margin larger than its own
self-disagreement — which is tomorrow's arithmetic and is a genuinely demanding condition.

---

## The number to carry

> **Accuracy without a baseline is not a number.**

It applies to every classifier anybody shows you, and it is two lines. This week found one
whose accuracy exactly equalled the baseline — and the only reason anyone noticed is that the
baseline was computed first.

---

> **Known** — Cohen's kappa corrects agreement for chance given the observed class
> distribution (`cohen-1960`) · raw agreement is misleading when one class dominates
> (`voorhees-trec8`) · judge-human agreement is the standard way judge quality is reported
> (`zheng-2023`)
> **Inferred** — that a model judge inherits the blindness of the question it is asked, so a
> faithfulness judge cannot detect a faithful wrong answer. Ours, following from week 8's
> keystone
> **Derived** — with 70% of cases positive, a constant-positive classifier achieves 0.70
> accuracy and kappa 0, so any judge matching those numbers has added nothing
> **Unknown** — how often deployed LLM-judge metrics are reported with a baseline. We have not
> seen one that was
