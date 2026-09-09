# Milestone 6 — A hybrid retriever, and permission to refuse it

> **Ship:** a configured hybrid retriever, a tuned constant, a verdict at every k you care
> about, and `REPORT.md` — which may legitimately conclude that you are not shipping it.

---

## The brief

### 1. Move to the extended query set, and say what that invalidates

`raglab.judgments.load(file="queries-extended.yml")`. Your own queries too — bring your
set to at least the nineteen answerable dev queries the course now ships, and report your
count.

Then one paragraph: **which week-5 numbers are no longer comparable?** All of them measured
against the old set. This is not a formality; it is the reason both files exist.

### 2. Build the hybrid, and tune the constant

`HybridRetriever`, with `c`, weights, depth and filter in the config.

Sweep `c` over at least five values at every k you report. **Report the sweep**, not the
winner — the paper's 60 captures none of the headroom at k=10 on this corpus and all of it
at k=3, and a single number hides that.

### 3. Deliver a verdict at k = 1, 3, 5, 10

For each: fused, every input, oracle, `beats_all`, `dilution`, `captured`.

**`beats_all` is strictly greater than every input.** A fusion that beats the weaker of its
two inputs is a worse version of the stronger one.

### 4. Break it down by family, and name what is unreachable

`by_family` with `n` on every row, and `unreachable` at your deployment k.

The report must contain, in its own paragraph: **which failures fusion cannot touch, and
what would.**

### 5. Choose a filter and measure what it costs

At least one — currency or date. Report recall, mean and maximum `shortfall`, and
`survival` at your shortlist depth. Then state whether the recall change is a *cost* or a
*requirement*, and how you can tell.

### 6. Run `ship_check`, and obey it

Confirm once on `test`, and write `REPORT.md`.

---

## The rubric

| Station | This week |
|---|---|
| 1 Corpus | The filter. Week 2's supersession graph, four weeks later, as a predicate |
| 2 Chunk | One sentence: why can a filter only work if a chunk knows its parent? |
| 3 Index | One sentence on what a pre-filter costs you in indexes |
| 4 Retrieve | **The week.** Fusion, the constant, the verdict at every k |
| 5 Rank | One sentence: RRF ignores scores entirely. What does that discard? |
| 6 Generate | Not built. One sentence: two chunks from two retrievers say different things. Which does the answer use? |
| 7 Measure | The new instrument, what it invalidated, and the family that is failing |

---

## The bar

- `pytest week-06 -v` green, `tools/check_evals.py` green
- The extended set in use, with the invalidation paragraph
- A `c` sweep at every reported k
- A verdict at four values of k, with `dilution` and `captured`
- Family table with `n`; `unreachable` named
- One filter measured, with `shortfall`
- `ship_check` run and obeyed at your deployment k
- Exactly one `test` run this week
- You survive Friday

---

## What you will want to do and should not

**Report the k where fusion wins.** All three verdicts, or none.

**Compare the fusion against dense retrieval.** It beats it at k=5 and is worse than the
BM25 you already had.

**Use `c = 60` because it is the default.** Sweep it. It costs a minute.

**Treat the filter's recall drop as a regression.** Sometimes it is the requirement working.
Say which, and how you know.

**Ship because you built it.** *"We did not ship hybrid retrieval because BM25 alone scored
higher at k=5"* is a better report than most published ones, and it is the correct answer
here at one of the three k values.
