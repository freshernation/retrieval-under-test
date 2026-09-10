# Refusal has to be designed

*Week 8 · Day 4 · about 25 minutes*

> By the end of this you can make a system decline to answer, price the decision, and state
> the limit of any threshold you choose.

---

## Sources

| Source | Tier | What it gives you |
|---|---|---|
| [**Rajpurkar, Jia & Liang, *Know What You Don't Know* (SQuAD 2.0)**](https://arxiv.org/abs/1806.03822) | 1 | Unanswerable questions as a first-class evaluation target, and how much harder they made the task |
| [**Ji et al.**](https://arxiv.org/abs/2202.03629) | 1 | Why answering without support is the default behaviour |
| [**Kadavath et al., *Language Models (Mostly) Know What They Know***](https://arxiv.org/abs/2207.05221) | 1 | Model self-assessment of correctness — the signal a real system has and this one does not |

---

## It does not happen on its own

Twenty queries. Twenty answers. Zero refusals — including the out-of-scope one and the two
that nothing retrieves.

That is not a defect in the simulator. It is what the last stage *is*: a component that takes
text and produces fluent prose about it. Given weakly related text it produces fluent prose
weakly related to the question, confidently, because confidence is a property of the register
rather than of the evidence.

**Refusal is a feature you add.** Nothing produces it by default, and a system that has never
been given a refusal policy has one anyway: answer everything.

---

## Counting refusals tells you nothing

A refusal is right or wrong depending on whether the answer was available, so the unit is a
four-way table:

| | answer was in context | was not |
|---|---|---|
| **answered** | `answered_right` | `answered_wrong` |
| **refused** | `refused_wrong` | `refused_right` |

Refusing everything and refusing nothing both produce a single "refusal rate", and they are
opposite systems. Only the split makes a refusal scorable — and the split needs **answer
spans**, which is week 4 paying for itself again.

---

## The frontier, and the free part

Sweep a confidence threshold and the trade is not what you expect:

| threshold | answered_right | answered_wrong | refused_right | refused_wrong |
|---|---|---|---|---|
| 0.00 | 14 | 6 | 0 | 0 |
| 0.50 | **14** | 4 | **2** | **0** |
| 0.55 | **14** | 4 | 2 | **0** |
| 0.60 | 12 | 3 | 3 | 2 |
| 0.70 | 8 | 2 | 4 | 6 |
| 0.80 | 8 | 0 | 6 | 6 |

**Up to 0.55, refusal is free.** Two confidently-wrong answers removed, every correct answer
kept.

Past it, every further refusal is bought with a correct answer and the rate worsens: 0.6 buys
one refusal for two answers; 0.8 removes the last four wrong answers for six right ones.

Two habits follow. **Find the free region** — it exists more often than people expect, and
nobody looks because refusal is assumed to be a trade. And **take the highest threshold that
costs nothing**: among free settings, the one refusing most, because below it you are
declining to use information you have.

---

## And the limit

| | confidence |
|---|---|
| answer **was** in context | mean 0.81, **minimum 0.56** |
| answer was **not** | mean 0.59, **maximum 0.78** |

The distributions **overlap**. A query whose answer is present can score lower than one whose
answer is absent, so **no threshold keeps every correct answer and refuses every wrong one.**

That is not a fact about refusal. It is a fact about *this signal* — query-term overlap with
the best chunk, the crudest thing available. A better signal would move the two populations
apart, and a perfect one would give a threshold with no trade at all.

So the frontier is the floor, not the ceiling, and `overlaps` belongs in the report. A refusal
policy presented without it implies a separation that does not exist — which is what "our
system knows when it doesn't know" almost always means.

---

## What a real system has that this one does not

A model can be asked. Self-assessed confidence — *"is your answer correct?"* — is a real
signal and better calibrated than people expect, and it is a **different** signal from
retrieval confidence: it can notice that the context does not address the question, which
term overlap cannot.

It also introduces the week-9 problem: you are asking the system that produced the answer
whether the answer is good, and its errors correlate with its own.

Both signals, combined, and measured against ground truth. Which requires the four-way table
you built today, and answer spans, and a held-out split — none of which the confidence
question replaces.

---

> **Known** — unanswerable questions require explicit handling and are substantially harder
> than answerable ones (`squad2-2018`) · answering without support is a documented default
> behaviour (`ji-2022`) · models can self-assess correctness with better-than-chance
> calibration (`kadavath-2022`)
> **Inferred** — that a free refusal region exists more often than practitioners expect and
> goes unlooked-for. Ours, from this corpus and from refusal being assumed to be a trade
> **Derived** — when the confidence distributions of answer-present and answer-absent queries
> overlap, no threshold achieves both perfect recall of correct answers and perfect refusal of
> wrong ones
> **Unknown** — how much better a model's self-assessed confidence is than retrieval
> confidence for this decision, on a real corpus. Measurable from week 10
