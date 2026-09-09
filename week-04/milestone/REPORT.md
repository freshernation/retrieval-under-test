# Week 4 report — [your name]

> Template. Replace everything in brackets. Every number carries
> `metric value (run:<id>)` or `tools/check_evals.py` fails.

---

## Station 7 — the ground truth changed

**Answer spans written:** [N], covering [N] of [N] answerable queries.

[Two spans you found hard to write, and why. The judgment you made in each case.]

**Verification:** all [N] spans found in the corpus. [If any were not, say what the typo was
and how long it would have gone unnoticed.]

### What changing the ground truth invalidated

[The uncomfortable paragraph. You have three weeks of decisions made against document-level
judgments, and this week showed that instrument cannot see chunking. Which earlier
conclusions are still supported, which are unsupported, and which are now known to be
wrong?]

---

## Station 2 — the chunking

### The audit, before any retrieval

| Configuration | chunks | min | median | max | **broken** |
|---|---|---|---|---|---|
| whole | | | | | |
| [config] | | | | | |

[Any configuration with a non-empty `broken` is disqualified. Name them and say which query
each one destroyed.]

### The frontier

| Configuration | k | answer recall | context words | on frontier |
|---|---|---|---|---|
| whole documents | 3 | | | |
| … | | | | |

[Full table. Dominated points visible and marked, not deleted.]

### The requirement, stated before the selection

**Target coverage: [N].** Acceptable because [what happens when the answer is not in the
context at all — a consequence, not a preference].

**Context budget: [N] words.** Because [what that costs, in what].

**Selected: [configuration] at k=[N]** — answer recall [N] (run:<id>), [N] words.

**Against no chunking:** [N] words → [N] words, **[N]× less context for [the same /
[N] less] coverage.**

---

## Station 1 — week 2's cleaning, settled

[Measured at chunk granularity, with the two numbers. Weeks 2 and 3 both failed to detect
an effect. Does this? Whatever the answer, this closes the question — say which way and
stop carrying it.]

---

## Stations 3 to 6

**3 Index** — [what chunking did to index size, and to document frequency. `429` was in 1
document of 10; how many chunks of how many is it in now, and what does that do to its idf?]

**4 Retrieve** — [one sentence on why document recall is no longer the right number.]

**5 Rank** — [one sentence: `k` used to mean "how many documents"; what does it trade
against now?]

**6 Generate** — not built. [One sentence: your configuration puts N words in a window. What
happens when the answer is at the end of it?]

---

## Confirmed on the held-out split

**answer recall [N] (run:<id>)**, [N] words, n=[N]. Read once.

---

## The failure library

Two cards. At least one about the ground truth rather than the chunker.

1. **[title]** — station [N] · found by [diagnostic] · [what it cost]
2. **[title]** — station [N] · found by [diagnostic] · [what it cost]

## What I would not defend

[One honest paragraph.]
