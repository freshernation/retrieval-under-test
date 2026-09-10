# Project 2 — [your name]

> Template. Replace everything in brackets. Every number carries
> `metric value (run:<id>)` or `tools/check_evals.py` fails.
>
> **No number in this report may come from reading an answer.**

---

## The two numbers that must appear together

**Faithfulness [N] (run:<id>). Confidently wrong: [N] of [N].**

[One paragraph on why either alone would mislead.]

---

## The report card

| | |
|---|---|
| n | |
| response_rate | |
| grounded_rate | |
| faithfulness | |
| citations parsed / resolved / unresolvable / not-in-context | |
| uncited sentences | |

**Outcomes**

| answered_right | answered_wrong | refused_right | refused_wrong |
|---|---|---|---|

---

## The answers I got wrong

[Every query in `confidently_wrong`, pasted in full, with one sentence each on what a user
would do with it. Not a summary. The text.]

**1. [query id] — "[query]"**

> [the answer, verbatim]

[What a user would do with this.]

*(repeat for each)*

**The tell:** [anything in the text distinguishing a wrong answer from a right one — or the
statement that there is none, and what that implies about reviewing answers by hand.]

---

## Station 1 — currency at the last station

**Citing a superseded document:** [query ids].

[`r05` in full: the answer, its faithfulness score, and the date the specification was
withdrawn. Then what would have to change to catch it, and why that is not a faithfulness
metric's job.]

---

## Station 6 — refusal

| threshold | answered_right | answered_wrong | refused_right | refused_wrong |
|---|---|---|---|---|

**Free region:** up to [N]. **Exchange rate turns at:** [N].

**Separation:** min confidence when the answer was present [N]; max when absent [N];
**overlaps: [true/false]**.

**Chosen: [N].** [Justification in terms of consequences, not metrics.]
**Who should actually choose this:** [role, and what they would need to know.]

---

## Three configurations

| config | grounded_rate | faithfulness | confidently_wrong | outcomes |
|---|---|---|---|---|
| mine | | | | |
| [deliberate fault] | | | | |
| refusal on | | | | |

[Which metrics moved and which did not, and the sentence about what a single-metric report
would have concluded.]

---

## Station 7 — what exists at serving time

| metric | available live? |
|---|---|
| response_rate | |
| grounded_rate | |
| faithfulness | |
| citation validity | |
| confidently_wrong | |

[One paragraph: the short list of things you cannot measure in production is the reason
week 9 exists.]

---

## Confirmed on the held-out split

**[metric] [N] (run:<id>)**, n=[N]. Read once.

---

## The failure library

Three cards this week. At least one must be about a check rather than the system.

1. **[title]** — station [N] · found by [diagnostic] · [what it cost]
2. **[title]** — station [N] · found by [diagnostic] · [what it cost]
3. **[title]** — station [N] · found by [diagnostic] · [what it cost]

## What I would not defend

[One honest paragraph.]
