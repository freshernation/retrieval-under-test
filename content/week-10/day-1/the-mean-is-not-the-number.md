# The mean is not the number

*Week 10 · Day 1 · about 25 minutes*

> By the end of this you can explain why the average request is the least interesting
> request in the system, and why capacity sized on it is wrong by a measurable amount.

---

## Sources

| Source | Tier | What it gives you |
|---|---|---|
| [**Dean & Barroso**, *The Tail at Scale*](https://doi.org/10.1145/2408776.2408794) | 1 | Why tail latency dominates, and why it gets worse as a system is fanned out |
| [**Google SRE Book**, ch. 6](https://sre.google/sre-book/monitoring-distributed-systems/) | 1 | Distributions over averages, and choosing signals for actionability |
| [**Robertson & Zaragoza**](https://doi.org/10.1561/1500000019) | 1 | What a term's document frequency is, which is also what it costs |

---

## The measurement

Twenty dev queries. The lexical stage's work, counted as postings touched:

| | postings |
|---|---|
| min (`428`) | **4** |
| p50 | 379 |
| mean | 423 |
| p95 | 829 |
| p99 / max | **1,075** |

The dearest query costs **269 times** the cheapest. Both are one HTTP request against one
endpoint with one timeout, and the mean — 423 — describes neither of them.

Dense search, over the same queries: 266 comparisons. Every query. Always. Its cost does
not depend on what you asked, which is either its best property or its worst depending on
whether you asked something cheap.

---

## Why the mean is the wrong summary, precisely

Not a matter of taste. Three concrete consequences.

**Capacity.** Provision for 423 and the 95th percentile request needs 829 — you are
**96% short** for one request in twenty. That request does not fail gracefully; it queues,
and the queue is what the next request waits behind.

**Comparison.** The mean moves when the *mix* of queries changes, with nothing about the
system having changed. Add four identifier queries to an eval set and your mean latency
improves. Nothing improved.

**Attribution.** A mean cannot tell you whether you have one slow stage or a few slow
requests, and those have opposite fixes: optimise the stage, or cap the input.

Dean & Barroso make the structural argument, and it is the one worth carrying: in a system
that fans out, the *slowest* component response determines the request, so tail latency
becomes the system's latency. A pipeline is a fan-out in series. Five stages each with a
rare slow case gives a request with a less rare slow case.

---

## The percentile that is one request

Here is where this course's own discipline bites.

p95 of twenty observations is the nineteenth value. p99 is the twentieth. They are
**adjacent in the sorted data and 30% apart** — 829 and 1,075. There is nothing between
them because there is nothing between them: no observation exists there.

So a p95 on twenty queries is one query. Change which query, and the figure moves by a
third. Week 9 computed a minimum detectable effect of 0.1003 at n=19 for a mean; for a
tail percentile the situation is strictly worse, because the estimate rests on the
observations you have fewest of.

This does not make the p95 useless. It makes it a number that must be quoted **with its
n**, like every other number in this course. `p95 = 829 (n=20)` is honest. `p95 = 829` is
an invitation.

---

## What a budget looks like

Per stage, not per request.

```
lexical    ≤ 900 postings
dense      ≤ 300 comparisons
fuse       ≤ 20 merges
assemble   ≤ 1,200 tokens
generate   ≤ (nothing, and that is the problem)
```

A total that passes tells you nothing about which stage is about to stop passing. Per-stage
numbers tell you where you have headroom and where you have none, which is the only
question a budget exists to answer.

And an **unbudgeted stage is not a free stage**. It is a stage nobody has thought about,
which is how a 200ms reranker arrives in a pipeline without a decision having been made.
`exceeds` reports an unbudgeted stage as over budget on purpose.

---

## The thing cost does not tell you

The obvious hope, once you can see a 269-fold spread: route the expensive queries
somewhere cheaper, since they were probably hopeless anyway.

Run week 9's AUC over it. Does query cost predict whether the answer ended up in the
context? **0.417 — strength 0.583.** Under the 0.7 floor. Chance.

Split the twenty queries at the median cost and the cheap half answers 0.67 against the
dear half's 0.73, six hundredths apart on nine and eleven queries with an MDE of 0.10.
Zero.

The by-family table is more tempting and no better: identifier queries cost 67 and answer
1.00, paraphrases cost 163 and answer 0.33, plain questions cost 617 and answer 0.80. That
reads like a trend. The families have one to five queries each. It is a story told by n=1,
and the split refutes it.

So cost and quality are two independent budgets. You cannot triage by cost, you cannot
spend your way to an answer, and any system that trades one for the other should be made
to show its exchange rate.

---

> **Known** — tail latency dominates in fanned-out systems and worsens with fan-out
> (`dean-barroso-2013`) · distributions rather than averages are the appropriate summary
> for latency, and signals should be chosen for actionability (`sre-book`) · a term's
> document frequency is the length of its postings list (`robertson-zaragoza-2009`)
> **Inferred** — that a per-stage budget is more useful than a request budget, because a
> passing total cannot say which stage is nearly failing. Ours
> **Derived** — p95 of twenty observations is the nineteenth value and p99 the twentieth, so
> the two are adjacent and a 30% gap between them rests on no observation at all · mean 423
> against p95 829 is a 96% shortfall for capacity sized on the mean · cost AUC 0.417 has
> strength 0.583, under this course's 0.7 floor
> **Unknown** — how much `work` over-estimates a real engine's cost, since block skipping
> and early termination both reduce it by amounts we have not measured on this corpus
