# Whose decision is this

*Week 8 · Day 4 · about 20 minutes*

> By the end of this you can say who should choose your refusal threshold, and what they need
> from you in order to choose it.

---

## Sources

| Source | Tier | What it gives you |
|---|---|---|
| [**Rajpurkar, Jia & Liang**](https://arxiv.org/abs/1806.03822) | 1 | Abstention as an evaluated behaviour rather than a fallback |

> The argument here is ours. It is week 2's currency-policy argument, at the last station.

---

## The question the frontier does not answer

You have the trade priced:

- 0.55 — two wrong answers removed, nothing lost
- 0.60 — one more removed, two correct answers lost
- 0.80 — every wrong answer gone, six correct answers lost

Past the free region the choice is an **exchange rate**: how many correct answers is it worth
losing to prevent one wrong one?

Nothing in the data answers that. It depends entirely on what happens when the system is
wrong, and what happens when it is unhelpful — and those are facts about the world your system
sits in, not about your system.

| setting | a wrong answer costs | an unhelpful answer costs |
|---|---|---|
| internal documentation search | a few minutes | a few minutes |
| customer-facing support | a complaint, sometimes churn | a support ticket |
| clinical or dosage information | **potentially a life** | a phone call |
| legal discovery | a missed obligation | more manual review |

Same frontier. Four completely different thresholds. In the third row the correct setting is
plausibly "refuse unless nearly certain", losing most of the correct answers, and that is not
timidity — it is the right answer.

---

## Which means it is not your decision

**The person who owns the consequences owns the threshold.** Not the engineer who built the
retriever, unless they also own the consequences — which occasionally they do, and then they
should say so out loud rather than deciding by default.

Engineers make this call constantly without noticing, and the way they make it is by not
making it: the default is 0.0, refuse nothing, answer everything. That is a policy. Nobody
chose it, nobody reviewed it, and it is the most permissive one available.

Your job is different and more useful:

1. **Produce the frontier.** The four-way table at several thresholds
2. **Name the free region.** If part of the improvement costs nothing, that part is not a
   decision and should just be taken
3. **State the exchange rate** past the free region, in answers rather than in metric points:
   *"below 0.6 we lose two correct answers for each additional wrong one prevented"*
4. **Report `overlaps`**, so nobody imagines a setting exists that has neither error
5. **Say what you cannot see** — the refusal decision uses retrieval confidence, and there are
   wrong answers with high confidence that no threshold removes

Then hand it over.

---

## What to write in the report

A sentence about **consequences**, not about the metric:

> We chose 0.55 because it removes two of six confidently-wrong answers at no cost in correct
> answers. Going further to 0.6 would prevent one additional wrong answer and lose two correct
> ones; on a documentation search where a wrong answer costs a few minutes, that trade is not
> worth taking. If this system moves to a customer-facing setting, the threshold should be
> revisited by whoever owns that decision.

Every clause is checkable, the trade is explicit, and the last sentence hands it to the right
person.

Compare the version that usually appears: *"we set the confidence threshold to 0.55 based on
validation performance."* True, uninformative, and it conceals that a policy choice was made
by a default.

---

## The pattern, three times now

Week 2: should a superseded document be demoted, filtered, or annotated? Depends on what a
wrong answer costs.

Week 6: should a filter be applied? Depends on the requirement, and the recall it costs is
not a defect.

Week 8: should the system refuse? Depends on the exchange rate between two kinds of error.

Each time the engineering produces a **frontier** and the choice on it comes from outside.
Each time the failure mode is the same: the engineer picks a point, ships it, and the person
who owns the consequences never learns there was a choice.

**Producing the frontier is the job. Choosing on it usually is not.**

---

> **Known** — abstention is an evaluated behaviour with its own trade-offs rather than a
> fallback (`squad2-2018`)
> **Inferred** — that the refusal threshold should be owned by whoever owns the consequences,
> and that engineers make the choice by default when nobody does. Ours, and it is the third
> instance of the pattern in this course
> **Derived** — past the free region, each additional correct refusal costs at least one
> correct answer, so the choice is an exchange rate rather than an optimisation
> **Unknown** — how refusal thresholds are actually set in deployed systems. Every
> practitioner we have asked says "the default", which is 0
