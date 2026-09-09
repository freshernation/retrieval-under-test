# Choosing on a frontier

*Week 4 · Day 4 · about 25 minutes*

> By the end of this you can present a two-axis decision the way it should be presented,
> and you will know which of its inputs cannot come from your data.

---

## Sources

| Source | Tier | What it gives you |
|---|---|---|
| [**BEIR**](https://arxiv.org/abs/2104.08663) | 1 | Why a configuration chosen on one corpus does not transfer |

> **Pareto domination is standard vocabulary from economics and multi-objective
> optimisation**, and we cite nothing for it because it is a definition rather than a
> finding. The presentation rules below are ours.

---

## Why one number cannot express this

A chunk size has two consequences — how often the answer reaches the context, and how much
context that costs — and they move in opposite directions. Any single number combining them
has silently chosen an exchange rate between coverage and tokens, and that exchange rate is
the actual decision.

So do not combine them. Plot both, find the points that are not beaten on both axes at once,
and present those.

**Point A dominates point B** when A is at least as good on both axes and strictly better on
one. A dominated point can be discarded without argument: there is something at least as
accurate and no more expensive.

The survivors are the **frontier**. On this corpus, 24 measured points reduce to 4.

---

## Read the frontier, not just the winner

| configuration | k | coverage | words |
|---|---|---|---|
| sections 60–150 | 1 | 44% | 95 |
| sections 60–150 | 3 | 78% | 359 |
| sections 60–150 | 5 | 89% | 567 |
| **sections 100–300** | **5** | **100%** | **984** |

Four points, and the shape of them is the finding: **the last 11% of coverage costs more
than the first 89%.** Going from 89% to 100% nearly doubles the context.

That is exactly the conversation you want to be having, and it is invisible in a winner-only
report. Whether that doubling is worth it is not a retrieval question — it depends on what
happens when the answer is missing — and now it can be asked of the person who knows.

**A frontier with the dominated points hidden looks like a set of good options rather than a
set of options.** Report the full table and mark the frontier within it.

---

## Two numbers your data cannot give you

**Target coverage.** How often is it acceptable for the answer not to be in the context at
all?

**Context budget.** How much context are you willing to pay for?

Neither is a property of the corpus, the retriever, or the queries. Both come from outside,
and if you do not state them, **your chunk size chooses them for you** and nobody ever finds
out which values it picked.

The discipline is a sentence you must be able to finish:

> "One query in ten where the answer is not in the context at all is acceptable **because
> [what happens then]**."

If you can finish it, you have a requirement. If you can only say "0.9 seems reasonable",
you have a preference — and a preference is not something a reader can disagree with, which
means it is not something you can be held to.

A support search box, where a miss means the user rephrases: 0.9 is generous. A system
quoting drug interactions, where a miss means an answer assembled from nothing: nothing
short of 1.0 is defensible, and even 1.0 measured on nine queries is not much comfort.

**Same code. Same frontier. Opposite correct answers.**

---

## Write the requirement down first

The failure mode here is subtle and extremely common: run the frontier, see which
configuration you like, and set the target to whatever that configuration achieves.

Nothing was faked. The requirement is real, the measurement is real, and you have chosen the
answer and called it a requirement. It is week 3's held-out-split problem in a new costume,
and the defence is the same: **decide before you look**, and put both numbers in the report
above the table rather than below it.

---

## And refuse when nothing qualifies

If no configuration meets the target within the budget, return nothing.

Not the nearest thing. A refusal is a conversation with whoever set the requirement — *you
asked for full coverage under 500 words and the cheapest full-coverage option is 984; which
gives?* — and that is a conversation worth having.

A silent near-miss is the same conversation, not had, with the requirement quietly relaxed
by whoever wrote the code. That is how a system ends up with properties nobody chose.

---

## What transfers

Not the configuration. `sections 100–300 at k=5` is the answer for ten RFCs, sixteen
queries, BM25, and this budget. Change the retriever — week 5 does — and it moves.

What transfers is the procedure:

1. **Audit** for destroyed answers. No retrieval required, and it disqualifies rather than
   penalises
2. **Measure both axes** on your corpus with your queries
3. **Compute the frontier** and report the whole table
4. **State a requirement** with a consequence attached, before selecting
5. **Refuse** when nothing meets it

Five steps, no numbers, and they work on a corpus nobody has written a blog post about.

---

> **Known** — retrieval results do not transfer between corpora, so a configuration chosen on
> one is not evidence about another (`beir-2021`)
> **Inferred** — that presenting the full table with the frontier marked prevents the
> winner-only failure. Ours, a presentation rule rather than a result
> **Derived** — a dominated point cannot be selected by any requirement over these two axes,
> since something exists that is at least as accurate and no more expensive
> **Unknown** — how stable a frontier computed on nine queries is. The deep-track exercise
> bootstraps it, and the honest expectation is: not very
