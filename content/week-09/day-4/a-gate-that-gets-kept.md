# A gate that gets kept

*Week 9 · Day 4 · about 25 minutes*

> By the end of this you can build a regression gate that is still switched on in three
> months.

---

## Sources

| Source | Tier | What it gives you |
|---|---|---|
| [**Google SRE Book**, ch. 6](https://sre.google/sre-book/monitoring-distributed-systems/) | 1 | Alerting philosophy: every page should be actionable, and noisy alerts get ignored |
| [**Cohen**](https://doi.org/10.4324/9780203771587) | 2 | The sampling floor the tolerance has to clear |

---

## The point of nine weeks

A change that makes the system worse should be stopped **before** it ships, automatically, by
something that does not get tired and does not have an opinion about whose change it is.

That is a gate: run the eval suite on the candidate, compare against the baseline, block if a
guarded metric moved the wrong way by more than a tolerance.

Three lines of arithmetic and a decision. The difficulty is entirely in the tolerance.

---

## The two ways it fails

**A gate that never fires.** The tolerance is wider than any regression that actually
happens. It passes everything, costs CI time, and provides reassurance in exchange for
nothing.

**A gate that always fires.** The tolerance is inside the noise, so it blocks identical
systems. Somebody overrides it, then somebody overrides it again, then it is muted — and now
it protects nothing *while everybody believes it is there*, which is strictly worse than
never having built it.

The second is the common one, it comes from wanting to be rigorous, and it is exactly the
alerting failure the SRE literature has been describing for a decade: an alert that fires on
noise trains people to ignore alerts.

---

## The tolerance comes from the MDE

Yesterday: at n=19, sd 0.223, the minimum detectable effect is **0.100**.

So a tolerance of 0.02 is **five times smaller than the smallest difference this eval set can
distinguish from zero.** It is not strict; it is measuring sampling noise, and it will fire
about as often on an improvement as on a regression.

Measured, on forty consecutive runs of an unchanged system:

| tolerance | false-alarm rate |
|---|---|
| 0.02 | **> 35%** |
| 0.10 (the MDE) | ~5% |

More than a third of runs blocked, on a system nobody touched.

> **Set the tolerance at the MDE. If that is wider than the regression you care about, the
> answer is more queries, not a tighter gate.**

That sentence is the day. It converts an argument about strictness into a resourcing
decision, which is where it belongs.

---

## Measure the false-alarm rate before deploying

`false_alarm_rate(gate, runs)` over repeated runs of an unchanged system. Every firing is
spurious by construction — nothing changed.

Nobody does this, and it takes minutes. A gate whose false-alarm rate you have not measured
is a gate you are about to mute.

The corollary is that the tolerance is **a function of the eval set**, so it must be
revisited whenever the set changes. Triple the queries and the MDE falls to 0.056; leave the
tolerance at 0.100 and the gate is now half as sensitive as it could be. Nobody revisits
this either, so gates drift out of calibration silently in the safe direction, which is why
the first failure mode is so common in mature systems.

---

## Two details that decide whether it works

**Direction is per metric.** `confidently_wrong` and `unresolvable_citations` are numbers you
want to *fall*. A gate assuming higher-is-better everywhere waves through a system that
doubled its wrong answers, and it will look like it is working.

**Report what was checked.** A gate that silently skips a metric missing from one of the two
reports **passes**. The most common reason a gate passes is that it stopped running — a
renamed field, a changed schema — and a pass is indistinguishable from success unless the
count is in the output.

---

## Annotate failures with detectability

`regression_check` adds `detectable` to each failure: is the movement larger than the MDE?

This is what makes the gate honest in the argument that follows a red build. An engineer
says "that is noise". If the failure is below the MDE, **they are right**, and the gate is
miscalibrated. If it is above, the burden shifts to them.

Without that field the conversation is two people asserting things about randomness, and the
person who wants to ship usually wins.

---

> **Known** — alerts that fire on noise are ignored, and every alert should be actionable
> (`sre-book`) · the minimum detectable effect is set by sample size and variance
> (`cohen-1988`)
> **Inferred** — that a gate's tolerance should be derived from the MDE, and that failing to
> revisit it as the eval set grows leaves gates silently under-sensitive. Ours
> **Derived** — a tolerance below the MDE fires on sampling variation, so its false-alarm rate
> on an unchanged system is substantial regardless of the system's quality
> **Unknown** — how many production eval gates have had their false-alarm rate measured. We
> have not encountered one
