# What expires and what does not

*Week 12 · Day 4 · about 25 minutes*

> By the end of this you can mark every claim you have made durable, re-measure or expired,
> and defend each mark.

---

## Sources

| Source | Tier | What it gives you |
|---|---|---|
| [**Sculley et al.**, *Hidden Technical Debt in ML Systems*](https://papers.nips.cc/paper_files/paper/2015/hash/86df7dcfd896fcaf2674f757a2463eba-Abstract.html) | 1 | Dependencies that decay, and configuration debt |
| [**Mitchell et al.**, *Model Cards*](https://doi.org/10.1145/3287560.3287596) | 1 | Claims scoped to a model version |
| [**Voorhees**, IR evaluation](https://doi.org/10.1007/3-540-45691-0_34) | 1 | Which comparisons a collection supports, and for how long |

---

## Three marks, no fourth

| mark | means | example |
|---|---|---|
| **durable** | about information retrieval. True in ten years | a metric without its N is not a number |
| **re-measure annually** | about your corpus, traffic or costs. Will drift | the best chunk size on this corpus |
| **expired** | about a model version, a price or a library API | any per-token cost figure |

A claim you cannot mark is a claim you do not understand well enough to have written, which
is a useful side effect of the exercise.

If your **expired** count is zero, you have not looked. Everything from week 5 onwards in
this course stood in for a model, declared openly, and `--live` is a different system.

---

## The course's own list

Offered as a worked example, and the proportions are the instructive part.

### Durable

Arithmetic, definitions, and properties of representations.

- a metric without its N is not a number — recall@10 is ~1.0 on ten documents
- faithfulness relates the answer to the context; correctness relates it to the world
- a judge's accuracy is uninterpretable without its constant baseline, and kappa 0 means it
  learned nothing
- an aggregate over a set cannot identify which member was load-bearing
- a tolerance below the minimum detectable effect produces false alarms at a measurable rate
- halving a detectable effect quadruples the queries required
- an exact token match is information a smoothed representation drops
- the fact that disqualifies an answer can live in a document the answer did not come from

None of those depend on a model, a vendor or a price. They are arithmetic or they are
definitional, and the arithmetic ones can be re-derived from scratch.

### Re-measure annually

Facts about a corpus, a traffic pattern or a cost structure.

- the best chunk size and the best `k1`/`b` for this corpus
- which query families each retriever wins on
- the context budget at which spend stops buying answers
- the cache hit rate, and therefore the cache's entire justification
- the minimum detectable effect, **which changes whenever the eval set does and which
  nobody ever updates**

That last one is the most dangerous entry on the list, because it is embedded in gate
tolerances and in `verdict`'s default argument. A gate calibrated to an MDE of 0.1003 and
pointed at a sixty-query set is a gate that is now wrong in the insensitive direction, and
nothing will tell you.

### Expired

- every value produced by the simulated generator and the simulated judge, which the fences
  have said since weeks 8 and 9
- every per-token price, which day 4 of week 10 would not even let you default
- the stage shares in week 10's wall-clock timings, which describe a laptop
- the framework API in week 11's reading, which is Tier 3 and moves quarterly

---

## The asymmetry worth noticing

The durable list is **mechanisms and arithmetic**. The expired list is **values**.

That is not a coincidence and it is the strongest argument for the stipulated-model
discipline this course has been running since week 7: a report that asserts directions and
refuses to quote unverifiable values is a report whose expired section is short.

Four weeks applied it — week 7's positional weighting, week 8's generator, week 9's judge,
week 10's clock and tokeniser — and the payoff arrives today, as a list that does not need
withdrawing.

Which generalises into a thing to do on Monday: when you cannot check a value, **write the
direction and the comparison and leave the value out**. You will be quoted either way. Only
one of the two will still be true.

---

## What the mark is for

Not tidiness. One specific thing: **you will be quoted in eighteen months by somebody who
has not checked.**

It happens to every technical document that is any good. The question is only whether the
sentence they quote carries its own expiry, and that is decided now, by you, in a column.

---

> **Known** — ML systems accumulate configuration debt and decaying dependencies that are
> invisible in the code (`sculley-2015`) · model documentation scopes claims to a model
> version (`mitchell-2019`) · a collection supports specific comparisons under stated
> conditions (`voorhees-2002`)
> **Inferred** — that a claim which cannot be marked durable, re-measure or expired is a
> claim not understood well enough to have been written. Ours
> **Inferred** — that the durable claims are mechanisms and arithmetic while the expired ones
> are values, which is the strongest argument for the stipulated-model discipline: assert
> direction, leave the value out, and the expired section stays short. Ours
> **Inferred** — that the minimum detectable effect is the most dangerous re-measure entry,
> because it is embedded in gate tolerances and default arguments and is never updated when
> the eval set changes. Ours
> **Derived** — every value produced by the two stipulated models is expired by construction,
> since the fences forbade reporting them in the first place
> **Unknown** — how long a *re-measure annually* claim actually survives. Annual is a guess
> and nothing in this course derives it
