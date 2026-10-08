# Milestone 10 — The service, its contract, and its refusal

> **Ship:** the pipeline behind a boundary that states what it promises, what it costs,
> what it records when it fails — and a report that refuses to ship it.

---

## The brief

### 1. Build the service

`Service`: one request in, one answer and one trace out. A cache in front, optional and
**defaulting to off**. A per-stage budget. Nothing computed that the eval harness already
computes.

The cache default is not fussiness. Day 2 served `r05` from a pre-8259 cache and got an
answer grounded entirely in a withdrawn RFC. A cache changes what the system *says*, so it
goes in the config and in the run id, and a cached run may not be compared against an
uncached one.

### 2. Write the budget, in work units

Per stage, with the number's provenance. Postings touched, comparisons made, tokens
consumed — never milliseconds, because a millisecond is a property of your laptop.

A stage with no budget goes on the list too, with a reason. An unbudgeted stage is how a
200ms reranker arrives without anyone deciding.

### 3. Report the tail next to the middle

p50 and p95, and the sample count beside them. Your p95 is the nineteenth of twenty
observations and your p99 is the twentieth; say so, because week 9's arithmetic does not
stop applying to latency.

### 4. Run the attribution, and read it

Day 3's walk over the whole dev set. Then answer, in the report, the question it raises:
**station 6 is empty and station 2 is empty, so what are you not going to work on?**

### 5. Price the budget curve

The curve, the marginal cost per additional answered query, and `waste`. Turn the wasteful
setting down. If you report a monthly figure, the rate you assumed is on the same line.

### 6. Make it refuse

`ship_check`, and it should still say no. Every SLO met, no stage over budget, six failures
in the attribution — and an operational green light over a system that cannot answer six
of twenty questions is the thing this course exists to prevent.

### 7. Confirm once on `test`, and write `REPORT.md`

---

## The rubric

| Station | This week |
|---|---|
| 1 Corpus | **The week's quiet one.** What invalidates your cache when a document changes? |
| 2 Chunk | One sentence: zero failures here. What does that mean for your chunker backlog? |
| 3 Index | The work count, and what it over-estimates |
| 4 Retrieve | Two of six failures. The budget for this stage, and its provenance |
| 5 Rank | Three of six failures — the word budget dropping a chunk that had the answer |
| 6 Generate | Zero failures, and the tokens. The cost section lives here |
| 7 Measure | The trace, the attribution report, and the refusal |

---

## The bar

- `pytest week-10 -v` green, `tools/check_evals.py` green
- Every reported performance number is a work count, not a clock reading
- p50 **and** p95, with n beside them
- The cache in the config, and in the run id
- The attribution report, with the two empty stations addressed in prose
- `waste` computed, and the wasteful setting turned down
- No price quoted as a result
- `ship_check` refuses, and the report says why
- Exactly one `test` run this week
- You survive Friday

---

## What you will want to do and should not

**Report milliseconds.** They describe your laptop. Compare your figure with the person
next to you before you believe otherwise.

**Quote one percentile.** The mean hides a 269-fold spread and the p95 hides the p99,
which on twenty samples is the next observation along.

**Leave the cache on.** Then every week-8 number in your repository is quietly wrong, and
nothing will tell you.

**Claim the week improved the system.** It did not. It made the system operable and it
moved no quality number, and a report that says so is a stronger report than one that
finds something to celebrate.

**Lead with the latency win.** The attribution report is the week's result. The latency
work is how you earned the right to read it.
