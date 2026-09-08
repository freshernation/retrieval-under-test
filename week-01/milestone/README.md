# Milestone 1 — An eval set, and a baseline

> **Ship:** twelve queries you wrote and judged yourself, a self-agreement number, the
> day-4 baseline scored against them, and `REPORT.md`.

This is the only milestone in the course where you build no retrieval. It is also the one
every later milestone is measured against, so a rushed eval set here is a wrong number in
week 11.

---

## The brief

The MRTA corpus in `data/gold/sample/` has 30 documents. Twelve queries ship with it. You
are going to write **twelve more**, judge them, and find out what your baseline does.

### 1. Write twelve queries — `my-queries.yml`

Same schema as the shipped file. **Eight `dev`, four `test`.**

They must not be twelve versions of the same shape. Cover at least six of these, and say
in the report which query is which:

| Shape | Example against this corpus |
|---|---|
| A plain factual lookup | "how long is a transfer valid" |
| A vocabulary gap — the user's word is not the corpus's word | "monthly pass" for "31-day pass" |
| An exact identifier | "stop 4213" |
| An acronym, or its expansion | "what is the AAP" |
| A question needing two documents | "who signs off a $400,000 purchase, and what process" |
| A question whose answer changed | anything about fares |
| A question the corpus **cannot** answer | "how much is station parking" |
| A negation | "which services do not carry bicycles" |

The out-of-scope query is not optional. A query set with no unanswerable queries in it
cannot detect the failure mode that will cost you most in week 8, and almost nobody
includes one.

Mark it `unanswerable: true` in your YAML. That flag does three things: `smells()` stops
demanding a relevant document for it, `raglab.metrics.evaluate` keeps it **out of every
mean** — an unanswerable query still earns a non-zero nDCG for confidently returning
something, which is the exact behaviour it exists to catch — and it is counted separately
as `n_unanswerable` in the run ledger. See `r10` in `data/gold/rfc/queries.yml` for one
with a trap in it.

### 2. Judge them by hand

At least **four documents per query**, and **not all of them relevant** — if every
document you judged is a 2 or a 3, the query cannot punish a bad retriever, and
`smells()` will tell you so.

Write your judgments before you run anything. If you find yourself opening the retriever
to decide what to judge, stop: that is how an eval set becomes a description of the system
it was supposed to test, and it is unrecoverable.

**No language model, at any point in this step.** See `FENCE.md`.

### 3. Measure your own disagreement

Judge four of your twelve queries **a second time**, at least a day later, without looking
at your first answers. Report `agreement`, `cohens_kappa`, and `overlap_size` from day 2.

That kappa is the floor on every result you report for the rest of the course. If you and
your past self agree 78% of the time, a 3-point improvement in week 6 means nothing, and
knowing that in week 1 is worth more than any of the numbers below it.

### 4. Run the baseline and record it

Day 4's `rank` over your `dev` split, through `search_all`, scored with
`raglab.metrics.evaluate`, recorded with `raglab.runs.record`. Then **once** on `test`.

### 5. Audit the eval set

- `unjudged_in_top_k` on your dev rankings. Judge what turns up, honestly, and report how
  many of the newly-judged documents were relevant — that number is your eval set's bias,
  measured
- `judged_coverage` over the corpus
- `smells()` over your judgments. It must return nothing before you ship

### 6. Write `REPORT.md`

The template is in this folder. `python3 tools/check_evals.py` must pass.

---

## The rubric

All seven stations, though most of them are one line this week. That is the point of
running all seven every time: the empty ones are visible.

| Station | This week |
|---|---|
| 1 Corpus | What is in it, what it cannot answer, and how you know |
| 2 Chunk | "Whole documents." One sentence on what that costs |
| 3 Index | "None." One sentence on what a set of terms per document cannot represent |
| 4 Retrieve | The baseline, its recall, and the queries it misses |
| 5 Rank | nDCG against recall. Which of your failures are ordering rather than retrieval |
| 6 Generate | Not built. One sentence on what a generator would do with your worst result |
| 7 Measure | The eval set, the kappa, the coverage, the bias audit |

---

## The bar

- `pytest week-01 -v` green
- `python3 tools/check_evals.py` green
- `smells()` returns nothing
- Every number in `REPORT.md` carries `metric value (run:<id>)`
- Exactly **one** `test` run in the ledger for this week
- You survive Friday

---

## What you will want to do and should not

**Judge more documents for the queries your baseline did well on.** Everyone does this
without noticing, because those are the queries that are pleasant to look at.

**Quietly drop the out-of-scope query** when it turns out to make your numbers look worse.
It does make them look worse. That is the query telling you something true.

**Round 0.8748 up to 0.9 in the prose.** The checker will catch it. That is not the reason
not to do it.
