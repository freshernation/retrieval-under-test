# Churn is not progress

*Week 11 · Day 4 · about 20 minutes*

> By the end of this you can tell a loop that is working from a loop that is moving, and
> you will know what the loop produced instead.

---

## Sources

| Source | Tier | What it gives you |
|---|---|---|
| [**Fawcett**, ROC analysis](https://doi.org/10.1016/j.patrec.2005.10.010) | 1 | AUC, for the one thing the loop did produce |
| [**Google SRE Book**, ch. 6](https://sre.google/sre-book/monitoring-distributed-systems/) | 1 | Indicator and diagnostic |
| [**Lin**, *The Neural Hype*](https://doi.org/10.1145/3308774.3308781) | 1 | Why a plausible mechanism plus a moving number is not evidence |

---

## The number

At a 0.8 bar, over twenty queries, the loop makes **44 retrievals**. Twenty-four of them are
iterations after the first.

`churn` — the shortlist changed and the confidence did not improve — counts **24**.

All of them. Every single iteration the loop ever takes produces a different candidate set
and gets no closer.

---

## Why that is the convincing failure mode

Because it looks exactly like work.

New documents arrive in the candidate set. The query grows. The trace fills with spans.
Each iteration is doing something visible, and in an agent trace viewer it reads as
deliberation — the system considering, refining, trying again.

Now consider the no-progress detector a sensible engineer would write: *stop if the
candidate set stops changing.* It is the obvious guard, it is cheap, and on this pipeline it
fires **never**. The candidate set always changes, because the query always changes, because
the feedback terms are always different. Zero iterations saved.

**Churn and progress are indistinguishable to every signal the loop can see** except the one
that is not improving. Which means the only usable guard is a condition on the thing you
actually care about — is the confidence rising — and that is the condition people leave out,
because *"did something change"* is easier to write and feels equivalent.

This is the local version of a general error, and Lin's argument about neural retrieval is
the same error at field scale: a plausible mechanism and a number that moves are not
evidence that the mechanism produced the movement. Here the mechanism is plausible, the
candidate set moves, and the outcome does not.

---

## What the loop did produce

One thing, and it is real.

The **iteration count** predicts whether the query was answered: AUC 0.214 — strength
**0.786** — clear of this course's 0.7 floor.

Compare it with week 10, which measured query *cost* as a quality signal and got 0.417:
chance. The loop manufactures the correlation that cost did not have, and the reason is
structural: it spends the most on the queries it cannot answer. Every capped query is a
query the retriever could not satisfy.

So an iterative agent on this corpus answers nothing new, costs 2.2 times as much, and
emits a usable serving-time quality signal as a by-product.

Is that worth 2.2×? Probably not, and the comparison that settles it is week 9's: two free
signals at AUC 0.83, available on the first retrieval, needing no loop at all. The loop's
diagnostic is weaker and costs more than doubling your retrieval bill.

But notice the shape of the finding, because it recurs. **The by-product of a mechanism can
outlive the mechanism's purpose.** The loop failed at what it was for and produced something
usable on the way. That is worth looking for whenever a stage disappoints — not as
consolation, but because the by-product is often available far more cheaply once you know
you want it. An iteration count that predicts failure suggests a single-shot predictor of
the same thing, and week 9 already had two.

---

## What to write down

Three sentences, and they are the day's deliverable:

1. The loop made 44 retrievals for 20 queries and 24 of 24 post-first iterations were churn.
2. The answered rate was 0.700 at every stopping threshold and every cost multiple.
3. The iteration count predicts answerability at strength 0.786, which is the only output
   worth keeping, and week 9 has a better one for free.

A loop is a very easy thing to build and a very hard thing to decline to ship. The numbers
above are what declining looks like.

---

> **Known** — AUC measures discrimination of a specified outcome without a threshold
> (`fawcett-2006`) · an indicator triggers work and a diagnostic explains it (`sre-book`) ·
> a plausible mechanism accompanied by a moving number is not evidence that the mechanism
> caused the movement (`lin-neural-hype`)
> **Inferred** — that a no-progress guard based on candidate-set change cannot work when the
> operator changes the query every iteration, so the guard must be on the outcome signal.
> Ours, and measured here as zero iterations saved
> **Inferred** — that a mechanism's by-product can be worth more than its purpose, and is
> often obtainable more cheaply once identified. Ours, and the iteration-count signal is the
> instance
> **Derived** — 44 retrievals for 20 queries, of which 24 are post-first iterations, and
> `churn` counts 24 · the iteration count predicts answerability at AUC 0.214, strength
> 0.786, against query cost's 0.417 measured in week 10 · week 9's free signals reach 0.83
> on the first retrieval
> **Unknown** — whether the iteration count adds anything to retrieval confidence once
> combined. The deep track asks for it, and at n=20 the combination's gain is unlikely to be
> resolvable
