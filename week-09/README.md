# Week 9 — Evaluation at depth

> **Destination**
> Know which of your numbers survive contact with production, how many queries each claim
> needs, and how to stop a regression automatically without crying wolf.

Week 8 produced a report card of ten numbers. Four of them cannot be computed once the
system is running.

---

## The week

| Day | Folder | What you'll be able to do |
|---|---|---|
| Mon | `day-1/` | Audit what survives at serving time, and find the signals that predict |
| Tue | `day-2/` | Validate a judge, and find it has learned nothing |
| Wed | `day-3/` | Say how many queries a claim needs, with a number |
| Thu | `day-4/` | Build a gate that fires on regressions and not on noise |
| Fri | `milestone/` | Ship the harness, the gate, and a Monday summary |

---

## Four findings

**Two useful signals, and neither is on anybody's dashboard.** Retrieval confidence predicts
whether the answer was in the context at **AUC 0.83**. So does the number of distinct
documents in the context — at 0.17, which is *the same strength inverted*: when the context
comes from one document the answer is usually there, and when it is scraped from three the
retriever was floundering.

Meanwhile answer length scores 0.45 and citation count 0.46 — indistinguishable from chance.
Those are exactly what gets instrumented, because they are easy and they *feel* like quality.

**The judge has learned nothing.** It labels 20 of 20 answers good. Accuracy **0.70**, Cohen's
kappa **0.000** — identical to a judge that returns "yes" without reading. Six of those
twenty are confident prose about questions the system could not answer, and it called every
one good, because it is a faithfulness judge and week 8's keystone does not stop being true
when a model does the checking.

**Five points costs seventy-seven queries.**

| detect | queries |
|---|---|
| 10 points | 20 |
| 5 points | **77** |
| 2 points | **479** |

Note the square: halving the effect quadruples the queries. At n=19 the minimum detectable
effect is **0.1003**, so most of this course's measured deltas were never distinguishable
from zero — which the course said at the time, each time.

**A gate below the MDE is a coin flip.** Set a tolerance of 0.02 when the MDE is 0.10 and the
gate fires on more than a third of consecutive runs of a system nobody touched. It gets
muted within a fortnight, and then it protects nothing while everybody believes it is there.

---

## The two floors

Week 3 found a floor from the **eval set**: with most queries unchanged, a bootstrap cannot
exclude zero however large the improvement.

This week adds one from the **judge**: if it disagrees with itself on 10% of cases, a 5-point
difference is inside its own noise at any sample size.

They compose, they bind for different reasons, and the larger one wins. Adding queries fixes
one and does nothing at all to the other.

---

## Milestone

An eval harness, a gate, and a summary whose first line is a blocker rather than a metric.
Spec in `milestone/README.md`.
