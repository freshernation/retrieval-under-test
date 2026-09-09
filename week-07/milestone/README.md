# Milestone 7 — A context assembler, with everything off

> **Ship:** the component that turns a ranking into the string a generator receives, with
> every optional stage **off by default** and a measurement for each one you turned on.

---

## The brief

### 1. Build the assembler

`ContextAssembler`: shortlist → rerank → dedupe → MMR → pack → order → assemble.

**Every optional stage defaults to `None`.** A pipeline whose stages default to on is a
pipeline nobody measured, and this week found that two of the three cost more than they buy
here.

### 2. Compute the ceiling before you build anything

`ceiling()` over your shortlist at the depth you will use. If it equals your answer recall
at your budget, **reranking cannot help you** and the report should say so in its first
paragraph.

### 3. The budget frontier

At least five budgets, with and without truncation. Three numbers each: `answered`,
`density`, `words`.

Then choose, with a requirement — the same discipline as week 4, and this time the cost axis
is the one you will be invoiced for.

### 4. Justify every stage you enable, against not having it

For each of reranking, deduplication and MMR: the configuration with it, the configuration
without it, and `regressions` naming any query it broke.

**A stage that does not improve `answered` at equal or lower `words` does not go in.**
"It is standard practice" is not a measurement.

### 5. Order the window, and be honest about it

Report the three orderings' ranking under the stipulated model, and the sensitivity of that
ranking to `dip`.

**Do not quote a score from the stipulated model.** The report may say that ends-first ranks
above rank order under a stipulated U-shaped weighting, and may not say by how much.

### 6. Confirm once on `test`, and write `REPORT.md`

---

## The rubric

| Station | This week |
|---|---|
| 1 Corpus | One sentence: what fraction of the window is boilerplate, six weeks after week 2? |
| 2 Chunk | One sentence: your chunk size decides the granularity of your budget. Would you choose it differently now? |
| 3 Index | One sentence on what the shortlist depth costs |
| 4 Retrieve | The ceiling, and what it says about whether reranking was worth building |
| 5 Rank | **The week.** Reranking, diversity, order — and which of the three you can measure |
| 6 Generate | Not built. One sentence: your window is [N] words with density [N]. What would you expect a generator to do with the other 80%? |
| 7 Measure | Which of this week's three stages your eval set is capable of evaluating |

---

## The bar

- `pytest week-07 -v` green, `tools/check_evals.py` green
- Ceiling computed and reported **before** the reranking section
- Budget frontier, at least five points, both truncation settings
- Every enabled stage justified against not having it, with `regressions`
- Ordering reported as a **ranking**, with no stipulated score quoted
- Exactly one `test` run this week
- You survive Friday

---

## What you will want to do and should not

**Enable reranking because reranking is standard.** It loses here. Measure yours.

**Report a number from `expected_use`.** It is a parabola somebody invented. Report the
ordering and the sensitivity.

**Treat MMR's flat recall as proof it does nothing.** Your metric cannot see diversity. Say
that, and write the queries that would.

**Pick the largest budget you can afford.** Density at 2,000 words is 0.098, and week 8 will
give you a second reason that matters.
