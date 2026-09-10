# Week 9 report — [your name]

> Template. Replace everything in brackets. Every number carries
> `metric value (run:<id>)` or `tools/check_evals.py` fails.

---

## The Monday summary

```
[paste summary(report) verbatim — blockers, then unmeasured, then numbers]
```

---

## Station 7 — what this eval set can detect

**Before the results.**

| | |
|---|---|
| n | |
| paired sd | |
| **minimum detectable effect** | |

| n | 2 points | 5 points | 10 points |
|---|---|---|---|
| [yours] | | | |
| 77 | | | |
| 479 | | | |

### The retrospective audit

| week | claimed delta | n | MDE at that n | above the floor? |
|---|---|---|---|---|
| 2 cleaning | | | | |
| 3 BM25 | | | | |
| 6 fusion | | | | |
| 7 reranking ceiling | | | | |

[One paragraph. This is the most valuable page in the milestone; write it as a finding rather
than an apology.]

---

## Station 6 — the judge

| | judge | constant "yes" |
|---|---|---|
| accuracy | | |
| kappa | | |

**Self-agreement:** label agreement [N] across two runs, mean score drift [N].

**Bias probes:** short [N] versus padded [N] with `length_bias` **zero**.

**Would you gate on it? [yes/no]** — [one paragraph, and if no, what would have to change.]

---

## Station 4 — serving-time proxies

| signal | AUC | strength | direction | instrument it? |
|---|---|---|---|---|
| retrieval confidence | | | | |
| distinct documents | | | | |
| answer length | | | | |
| citation count | | | | |

**Offline-only metrics:** [list]. [One sentence each on what you would do if a user reported
a bad answer and you could not compute it.]

---

## The gate

| metric | direction | tolerance | where the tolerance came from |
|---|---|---|---|

**Measured false-alarm rate:** [N] over [N] consecutive runs of an unchanged system.

**Deliberately not guarded:** [metrics], because [reason per metric].

**Blocked a deliberate regression:** [which configuration, which rules fired, and whether
each failure was `detectable`].

---

## Stations 1, 2, 3 and 5

**1 Corpus** — [which of your checks would notice a document going out of date?]

**2 Chunk** — [what your chunk size did to the paired standard deviation.]

**3 Index** — [which serving-time signal would tell you the index had degraded?]

**5 Rank** — [what you can detect at your n.]

---

## Confirmed on the held-out split

**[metric] [N] (run:<id>)**, n=[N]. Read once.

---

## The failure library

Two cards. At least one about a measurement rather than the system.

1. **[title]** — station [N] · found by [diagnostic] · [what it cost]
2. **[title]** — station [N] · found by [diagnostic] · [what it cost]

## What I would not defend

[One honest paragraph.]
