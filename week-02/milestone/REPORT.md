# Week 2 report — [your name]

> Template. Replace everything in brackets. Every number carries
> `metric value (run:<id>)` or `tools/check_evals.py` fails.

---

## Station 1 — the corpus

### The manifest

[Paste the per-document table. Ten rows. Not a total.]

### Coverage gaps

[Paste `coverage_gaps()` verbatim. Do not tidy the wording — it is generated so that it
stays true, and editing it by hand is how it stops being.]

### What I did not expect

[Three things. At least one must be something you found by opening a file rather than by
running code.]

### What this corpus cannot answer

[Two classes of question, with an example of each. One should be a class you only noticed
because of the manifest.]

---

## Station 7 — the eval set

**Four new queries**, bringing the set to [N].

| Shape | Query id | What it tests |
|---|---|---|
| answer changed between documents | | |
| needs both halves of a superseded pair | | |
| answer cut by a page boundary | | |
| unanswerable | | |

**Self-agreement:** [N]% raw, kappa [N], over [N] commonly-judged documents.
Week 1's kappa was [N]. [One sentence on the difference, and whether four weeks of
practice or four easier queries explains it.]

---

## The two changes

### Change 1 — cleaning the corpus

Removed [N]% of the text, ranging from [N]% (`[doc]`) to [N]% (`[doc]`).

**recall@3 [N] (run:<id>)** → **recall@3 [N] (run:<id>)**, n=[N], delta [N]
[95% CI [N], [N]].
**recall@5 [N] (run:<id>)** → **recall@5 [N] (run:<id>)**, delta [N] [95% CI [N], [N]].

Queries that got worse: [N]. Queries that moved at all: [list them by id].

Near-duplicate pairs above 0.05: [N] before, [N] after.

**This is a [tuning change / correctness fix]** because [one sentence].
**Decision: [ship / hold].** [Two sentences. If you are shipping a change whose interval
touches zero, the justification cannot be the interval.]

### Change 2 — demoting superseded documents

**ndcg@3 [N] (run:<id>)** → **ndcg@3 [N] (run:<id>)**, n=[N], delta [N]
[95% CI [N], [N]].

Queries that got worse: [N].
Query `r05` specifically: ndcg@3 [N] → [N].

**This is a [tuning change / correctness fix]** because [one sentence].
**Decision: [ship / hold].**

### Confirmed on the held-out split

**[metric] [N] (run:<id>)**, n=[N], configuration: [which one, and why that one].

---

## Stations 2 to 6

**2 Chunk** — still whole documents. [One sentence on what a 222-word verbatim run
between two documents implies for the week you start chunking.]

**3 Index** — still a set of terms. [One sentence: where would `superseded_by` have to
live for a retriever to use it, rather than a post-processing step?]

**4 Retrieve** — unchanged, by the fence. [One sentence on what not being allowed to
touch it made you find.]

**5 Rank** — the demotion. [One sentence on the fact that your only ranking change this
week came from metadata rather than from scoring.]

**6 Generate** — not built. [One sentence: what should an answer say when its best source
is superseded, and who decides?]

---

## The failure library

Two cards, in `logs/failure-library.md`. At least one must be a station 1 card.

1. **[title]** — station [N] · found by [diagnostic] · [what it cost]
2. **[title]** — station [N] · found by [diagnostic] · [what it cost]

## What I would not defend

[One honest paragraph.]
