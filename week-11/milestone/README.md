# Project 3 — An agent, measured, and the recommendation

> **Ship:** an agent whose every stage defaults to off, a comparison against week 8's
> single-shot pipeline with cost on both sides, and a recommendation you are prepared to
> defend when it is a recommendation against your own work.

This is the third and last project. Project 1 was an eval set and a baseline; Project 2 was
the full pipeline with cited answers. Project 3 is the one where the deliverable might be
*"do not build this"*, and that is the point of it.

---

## The brief

### 1. Build the agent

`Agent`, composing the week's four stages. **Every one defaults to off.** `max_iters=1`
means no loop, and that configuration must be week 8's pipeline exactly — the baseline has
to come out of the same object or the comparison acquires a second variable nobody is
tracking.

### 2. Compute the ceiling before you build anything

The oracle over your strategies. If the headroom is small, say so on Monday and spend the
week measuring rather than building.

### 3. Report cost in retrievals **and** tokens

The loop triples the retrievals and leaves the token count exactly where it was. A cost
report in tokens calls it free, and tokens are the number everybody watches.

### 4. Compare every delta against the MDE

Week 9 measured 0.1003 for this eval set at this n. Pass it to `verdict` as an argument,
because it is a property of the set and not of your code — and nobody ever updates it when
the set changes.

### 5. Report `citing_superseded` as ids

One stage takes it to zero. A different stage **adds** to it, in a metric that day's report
did not carry. A count cannot show you that both happened.

### 6. Make it refuse, and agree with it

`ship_check` on your best configuration. It will refuse. The paragraph where you agree with
it is the most valuable page in Project 3.

### 7. Confirm once on `test`, and write `REPORT.md`

---

## The rubric

| Station | This week |
|---|---|
| 1 Corpus | The edge you hopped along, and whether it was already a field |
| 2 Chunk | One sentence: dropping a chunk is not dropping a document, and what that cost you |
| 3 Index | One sentence on what rewriting does to an exact-identifier match |
| 4 Retrieve | **The week.** The rewrite, the router, the ceiling, the capture |
| 5 Rank | What the loop's extra iterations did to the candidate set |
| 6 Generate | Faithfulness, which did not move, and why that was predictable |
| 7 Measure | The verdict, the MDE comparison, and the refusal |

---

## The bar

- `pytest week-11 -v` green, `tools/check_evals.py` green
- No rewrite rule derived from a failing query — **this one is disqualifying**
- An oracle ceiling, computed before the mechanism
- Cost in retrievals as well as tokens
- Every delta next to the MDE of the set it was measured on
- `citing_superseded` as ids, before and after
- `ship_check` refuses, and the report agrees with it in prose
- A recommendation, in one sentence, that somebody could act on
- Exactly one `test` run this week
- You survive Friday

---

## What you will want to do and should not

**Report +0.05 as the result.** The MDE is 0.1003. It is one query.

**Leave the dial on that does nothing.** Query rewriting with the loop already running
changes nothing at all, and the config will claim it was on. That is worse than a dial that
hurts: it survives review, it gets copied, and somebody eventually credits it.

**Report cost in tokens.** The expensive stage is free in tokens.

**Call the two-stage interaction a feature.** Loop-and-hop beats either alone. It is the
best number in the course and the least durable thing in your repository.

**Skip the recommendation because the numbers are negative.** A null result with a cost
attached is a finding. *"We built it, it costs 2.45×, the gain is inside our measurement
floor, and here is what to do instead"* is a stronger deliverable than any agent.
