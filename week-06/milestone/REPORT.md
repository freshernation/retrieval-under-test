# Week 6 report — [your name]

> Template. Replace everything in brackets. Every number carries
> `metric value (run:<id>)` or `tools/check_evals.py` fails.

---

## The verdict, first

**[Shipping / not shipping] hybrid retrieval at k=[N], because [one sentence].**

---

## Station 7 — the instrument changed

**Query set:** [N] dev ([N] answerable), [N] test. Previously [N].

**What this invalidates:** [One paragraph. Every week-5 number was measured against the
sixteen-query set. Which of your earlier conclusions still stand, which are unsupported,
and which you cannot tell.]

---

## Station 4 — fusion

### The constant

| c | k=3 | k=5 | k=10 |
|---|---|---|---|
| 1 | | | |
| 10 | | | |
| 20 | | | |
| 60 | | | |
| 200 | | | |

**Chosen: c = [N]** because [one sentence]. [If it is not 60, say what would have happened
had you used the default.]

### The verdict

| k | lexical | dense | fused | oracle | beats_all | dilution | captured |
|---|---|---|---|---|---|---|---|
| 1 | | | | | | | |
| 3 | | | | | | | |
| 5 | | | | | | | |
| 10 | | | | | | | |

[The k where fusion loses, named explicitly, with its dilution.]

### By family

| family | n | lexical | dense | fused |
|---|---|---|---|---|

**Unreachable at k=[N]:** [query ids, with their families].

> **What fusion cannot touch, and what would.** [Your own paragraph. This is the most
> valuable thing in the report.]

---

## Station 1 — the filter

**Predicate:** [which]. Keeps [N] of [N] chunks.

| | recall | mean shortfall | max shortfall | survival@[depth] |
|---|---|---|---|---|
| unfiltered | | — | — | — |
| post-filter | | | | |
| pre-filter | | | | |

**Is the recall change a cost or a requirement?** [One paragraph, and how you can tell.]

---

## Stations 2, 3, 5 and 6

**2 Chunk** — [one sentence: why can a filter only work if a chunk knows its parent?]

**3 Index** — [one sentence on what pre-filtering costs in indexes.]

**5 Rank** — [one sentence: RRF ignores scores entirely. What is discarded, and when would
you miss it?]

**6 Generate** — not built. [One sentence: two chunks from two retrievers disagree. Which
does the answer use, and who decides?]

---

## `ship_check`

```
[paste the dict, verbatim]
```

**Obeyed: [yes/no].** [If no, the justification must not be "we built it".]

---

## Confirmed on the held-out split

**[metric] [N] (run:<id>)**, n=[N], k=[N], c=[N]. Read once.

---

## The failure library

Two cards. At least one about a failure fusion cannot reach.

1. **[title]** — station [N] · found by [diagnostic] · [what it cost]
2. **[title]** — station [N] · found by [diagnostic] · [what it cost]

## What I would not defend

[One honest paragraph.]
