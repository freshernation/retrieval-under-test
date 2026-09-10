# Project 2 — The pipeline, and its report card

> **Ship:** a system that answers questions from your corpus, and a report card in which
> **every number was computed by machinery you wrote** — no number produced by reading.

This is the keystone. Seven weeks of retrieval, one week of generation, and the deliverable
is not the system: it is the evidence about the system.

---

## The brief

### 1. Build the `Answerer`

Assembler + generator + refusal policy, with a config that names all three. A report that
does not say which generator produced its numbers is not reproducible, and the generator's
flags are the difference between faithfulness 1.00 and 0.09.

### 2. Produce the report card

`report_card` over your dev set: `n`, `response_rate`, `grounded_rate`, the four-way
`outcomes` table, `faithfulness`, the citation counts, and the three lists —
`confidently_wrong`, `citing_superseded`, `uncited_sentences`.

**Both `faithfulness` and `confidently_wrong` must appear.** Either alone is misleading, and
the pairing is the week's whole finding.

### 3. Read the answers you got wrong

Every query in `confidently_wrong`, in full, pasted into the report with one sentence each on
what a user would do with it.

This is not decoration. The numbers are the excuse for the reading, and a student who
reports six and reads none has not done the milestone.

### 4. Price refusal

The full frontier, at least six thresholds. Name the free region, name the point where the
exchange rate turns, and report `separation` — including `overlaps`.

Then choose a threshold and justify it with a sentence about **consequences**, not about the
metric.

### 5. Compare at least three configurations

Yours, plus one with a deliberate fault (`misattribute` or `fabricate`), plus one with
refusal on. Show which metrics move and which do not — `grounded_rate` is identical across
all three, and demonstrating that is the point.

### 6. Confirm once on `test`, and write `REPORT.md`

---

## The rubric

| Station | This week |
|---|---|
| 1 Corpus | `citing_superseded`. Week 2's graph, at the last station, catching what faithfulness cannot |
| 2 Chunk | One sentence: your chunk size decides what a citation points at. Is it a useful unit for a reader? |
| 3 Index | One sentence on what the answer would look like if retrieval returned nothing |
| 4 Retrieve | `grounded_rate` — and the fact that it is unchanged by every generation fault |
| 5 Rank | One sentence on what the top-ranked chunk did to `r05` |
| 6 Generate | **The week.** Citations, faithfulness, refusal, and what none of them measure |
| 7 Measure | Which of your numbers exist at serving time, and which need answer spans |

---

## The bar

- `pytest week-08 -v` green, `tools/check_evals.py` green
- Report card complete, with **both** faithfulness and `confidently_wrong`
- Every `confidently_wrong` answer pasted and read
- Refusal frontier with the free region and `overlaps` named
- Three configurations compared
- Exactly one `test` run this week
- No number in the report produced by reading an answer
- You survive Friday

---

## What you will want to do and should not

**Lead with faithfulness.** It is 1.00 and thirty percent of the answers are wrong.

**Report a quality score.** There is no field for it because nothing here can compute one.
Week 9 is about what happens when you ask a model to.

**Skip the reading.** Six answers. Fifteen minutes. It is the only part of this milestone
that changes how you think.

**Blame the model for the five bad citations.** They came out of the corpus, and your
checker put them there.

**Fix `r05` by prompting.** The fact that makes it wrong is in a different document. Week 2
told you which one, and week 2's demotion is the fix.
