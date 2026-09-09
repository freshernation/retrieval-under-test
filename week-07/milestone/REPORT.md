# Week 7 report — [your name]

> Template. Replace everything in brackets. Every number carries
> `metric value (run:<id>)` or `tools/check_evals.py` fails.
>
> **No score from the stipulated positional model appears anywhere in this report.**

---

## The ceiling, before anything else

**Answer recall at k=[N]: [N] (run:<id>). Over a [N]-deep shortlist: [N] (run:<id>).**

**Available to reranking: [N] points.** [One sentence on whether that justified building
one.]

---

## Station 5 — the three stages

### Reranking

| alpha | k=1 | k=3 | k=5 |
|---|---|---|---|
| 0.0 | | | |
| … | | | |
| 1.0 | | | |

**Best alpha: [N].** [If it is 1.0 — the identity — say so plainly and say what that means
about the features.]

**Enabled: [yes/no].** [Justification against not having it, or the reason not to.]

### Deduplication and diversity

| config | answered | density | words | redundancy | distinct docs |
|---|---|---|---|---|---|
| none | | | | | |
| dedupe [th] | | | | | |
| mmr [lam] | | | | | |

**Regressions:** [query ids, or none].

> [The paragraph about measurability. Answer recall is indifferent to redundancy. What
> would have to be true of your eval set for this table to decide anything?]

**Enabled: [yes/no].**

### Order

Under a stipulated U-shaped weighting, the orderings rank: **[first] > [second] > [third]**,
and that ranking [does / does not] survive varying `dip` across [range].

Measured, not stipulated: the first answer-bearing chunk sits at position [N] of [N] on
average.

**Chosen: [which], because [one sentence].**

---

## Station 3 to 4 — the budget

| budget | truncate | chunks | words | answered | density |
|---|---|---|---|---|---|

**Chosen: [N] words, truncate=[bool].**

**Requirement:** [target answered], because [consequence]. **Budget:** [N] words, because
[cost].

[One sentence on the truncation decision, including the case where it destroys a span.]

---

## Stations 1, 2, 6 and 7

**1 Corpus** — [one sentence: how much of your window is boilerplate, six weeks after
week 2?]

**2 Chunk** — [one sentence: your chunk size sets the granularity of your budget. Would you
choose it differently now?]

**6 Generate** — not built. [One sentence: your window is [N] words at density [N]. What
would you expect a generator to do with the rest?]

**7 Measure** — [which of this week's three stages your eval set can actually evaluate, and
what you would add.]

---

## Confirmed on the held-out split

**[metric] [N] (run:<id>)**, n=[N], budget=[N]. Read once.

---

## The failure library

Two cards. At least one about something this week could not measure.

1. **[title]** — station [N] · found by [diagnostic] · [what it cost]
2. **[title]** — station [N] · found by [diagnostic] · [what it cost]

## What I would not defend

[One honest paragraph.]
