# Week 3 report — [your name]

> Template. Replace everything in brackets. Every number carries
> `metric value (run:<id>)` or `tools/check_evals.py` fails.

---

## Station 7 — the instrument

**Eval set:** [N] dev, [N] test, up from 10 and 6.

| Shape | Count | Notes |
|---|---|---|
| plain lookup | | |
| vocabulary gap | | |
| exact identifier | | |
| acronym | | |
| needs two documents | | |
| answer changed | | |
| **unanswerable** | | at least 3 |
| negation | | |
| [your own] | | |

**Documents now covered by at least one query:** [N] of 10. Previously [N].
[Which documents were uncovered, and what class of failure that hid.]

**Self-agreement:** week 1 kappa [N], week 2 [N], week 3 [N], over [N] re-judged.
[One sentence on the trend. If it is not improving, say so — it is a more interesting
result than if it is.]

### The floor arithmetic

Before growing the set: n=[N], unchanged=[N], floor=[N], **pinned=[true/false]**,
`queries_needed` = [N].

After: n=[N], unchanged=[N], floor=[N], **pinned=[true/false]**.

> [One sentence. Can you now report the week's headline result, and what changed to make
> that true?]

---

## Station 3 — the index

**Vocabulary** [N] terms · **postings** [N] · **average length** [N] tokens ·
**shortest** [N] · **longest** [N].

[What you store, what it costs, and what positions bought you.]

**The reproduction check:** the index run and the baseline run returned identical rankings
for [N] of [N] queries. [If not all: which, and why. A difference here is a bug, not a
result.]

---

## Station 4 — retrieval

| Run | Change | recall@3 | ndcg@3 | delta | 95% CI | worse | pinned |
|---|---|---|---|---|---|---|---|
| baseline (run:<id>) | week 1 | | | — | — | — | — |
| index (run:<id>) | lookup not scan | | | | | | |
| bm25 (run:<id>) | BM25 defaults | | | | | | |
| identifiers (run:<id>) | +identifiers | | | | | | |
| tuned (run:<id>) | k1=[N] b=[N] | | | | | | |
| cleaned (run:<id>) | week 2 corpus | | | | | | |

**One change per run.** [Confirm it, and name anything you nearly changed twice.]

**Which week-1 defect survives:** [name it, and the queries that still fail because of it.]

**Week 2's cleaning, at document granularity:** [the delta, the interval, and the sentence
that says whether this settles it or defers it to week 4.]

---

## Station 5 — tuning

**Chosen: k1 = [N], b = [N].**

| Warning | Value | What it means here |
|---|---|---|
| default's rank in the grid | [N] of 45 | |
| optimum at the grid edge | [yes/no] | |
| configurations evaluated | [N] | |
| queries the gain rides on | [N] of [N] | |

**The plateau.** [Your paragraph on k1 → ∞ and whether you believe it.]

**Spread across the grid:** [low] to [high].

---

## Confirmed on the held-out split

**[metric] [N] (run:<id>)**, n=[N], configuration [which].
Read once. [Say what you would have done if it had come back worse — before you saw it.]

---

## Stations 1, 2 and 6

**1 Corpus** — [one sentence on the cleaned-corpus run.]

**2 Chunk** — still whole documents. [One sentence on what a 15× length spread is doing to
`b`, and what changes when the unit gets smaller.]

**6 Generate** — not built. [One sentence: name a query where retrieval is now perfect and
the answer would still be wrong.]

---

## The failure library

Two cards. At least one must be about the eval set rather than the retriever.

1. **[title]** — station [N] · found by [diagnostic] · [what it cost]
2. **[title]** — station [N] · found by [diagnostic] · [what it cost]

## What I would not defend

[One honest paragraph.]
