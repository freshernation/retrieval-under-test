# The number and its floor

*Week 12 · Day 1 · about 20 minutes*

> By the end of this you can write a number the way this course has been writing them for
> eleven weeks, and you will know what the audit costs.

---

## Sources

| Source | Tier | What it gives you |
|---|---|---|
| [**Cohen**, *Statistical Power Analysis*](https://doi.org/10.4324/9780203771587) | 2 | Power before the experiment, not after |
| [**Lin**, *The Neural Hype*](https://doi.org/10.1145/3308774.3308781) | 1 | Published improvements that do not survive their own baselines |
| [**Voorhees**, IR evaluation](https://doi.org/10.1007/3-540-45691-0_34) | 1 | What a test collection can and cannot establish |

---

## The form

```
0.750                                 a decoration
0.750 (n=20, MDE 0.1003)              a number
```

That is the entire rule and it takes four characters more than the bad version.

The first form invites a comparison it cannot support. Somebody reads 0.750 next to last
quarter's 0.710 and concludes something improved. The second form says, in the same breath,
that a difference of 0.04 on this set is inside the noise — so the comparison is not
available, and the reader finds that out at the same moment they find out the number.

Timing is the point. A caveat in a later paragraph arrives after the belief has formed.

---

## The audit, and what it costs

Week 9 built the retrospective MDE audit and it is uncomfortable. Here is the course's own,
which is the honest way to ask students to do theirs.

| Week | Claim | Delta | n | MDE | Above the floor |
|---|---|---|---|---|---|
| 2 | cleaning improved recall | 0.111 | 19 | 0.1003 | **yes**, barely |
| 6 | hybrid fusion | 0.053 | 19 | 0.1003 | **no** |
| 7 | reranking ceiling | 0.158 | 19 | 0.1003 | yes |
| 11 | the agent | 0.050 | 20 | 0.1003 | **no** |

Two of the course's own headline results were never distinguishable from zero. One of them
is the final project.

**And the course reported the interval alongside each of them at the time.** That is the
only reason this is a table rather than a retraction, and it is the entire argument for the
discipline: a number reported with its floor can be audited later. A number reported alone
can only be withdrawn.

---

## How to frame it without it reading as an apology

Students find this demoralising if it is not framed, and the framing is not a trick — it is
accurate.

The audit is **the payoff for eleven weeks of reporting intervals**, not the bill for
eleven weeks of mistakes. A course that had quoted bare numbers would have no audit
available. It would have a set of claims of unknown status, which is the normal state of
this literature.

Lin's argument about neural retrieval is the field-scale version: a large fraction of
published improvements do not survive comparison against a properly tuned baseline. The
response is not despair about the field; it is that the comparison has to be in the paper.

So the sentence to write is:

> Two of our four headline deltas are inside the minimum detectable effect of the sets they
> were measured on. We know which two because we reported the interval each time, and the
> remedy is a larger eval set rather than a different pipeline.

---

## What the audit tells you to do

Not *measure less confidently*. Three concrete things.

**Price the eval set.** Week 9 did: five points costs 77 queries, two points 479, and the
square is why *"we will add a few more queries"* is not a plan. Any argument about which
pipeline to build should be preceded by the question of whether the set can tell.

**Choose graded metrics where you can.** A binary per-query metric produces differences of
−1, 0 or +1 and therefore a near-maximal standard deviation. The same effect is detectable
at fewer queries with a graded one.

**Stop chasing effects below your floor.** Week 11 spent four days on techniques whose best
result was half the smallest resolvable effect. The MDE, computed on Monday, would have
said so — and the right response would have been to spend the week writing queries.

That last one is the practical payoff and it is worth a lot. **The floor is a planning tool,
not a scoring rule.** Computed before the work, it tells you whether the work can produce a
readable answer.

---

> **Known** — power analysis belongs before an experiment rather than after it
> (`cohen-1988`) · a substantial fraction of published retrieval improvements do not survive
> comparison against properly tuned baselines (`lin-neural-hype`) · a test collection
> establishes relative comparisons under stated conditions rather than absolute quality
> (`voorhees-2002`)
> **Inferred** — that a number reported with its floor can be audited later while one
> reported alone can only be withdrawn, which is the whole case for the discipline. Ours
> **Inferred** — that the minimum detectable effect is a planning tool rather than a scoring
> rule, and computed before the work it says whether the work can produce a readable answer.
> Ours
> **Derived** — of four headline deltas across the course, two sit inside the minimum
> detectable effect of their sets: week 6's fusion at 0.053 and week 11's agent at 0.050,
> against a floor of 0.1003 · a binary per-query metric has a near-maximal standard
> deviation and therefore requires more queries than a graded one at equal detectable effect
> **Unknown** — what fraction of published RAG improvements fall below the floor of their own
> sets. Sample sizes are usually reported; standard deviations almost never are, so it cannot
> be computed from the literature as published
