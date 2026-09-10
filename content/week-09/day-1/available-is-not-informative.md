# Available is not informative

*Week 9 · Day 1 · about 20 minutes*

> By the end of this you can explain why the easiest metrics to collect are the ones most
> likely to be worthless.

---

## Sources

| Source | Tier | What it gives you |
|---|---|---|
| [**Google SRE Book**, ch. 6](https://sre.google/sre-book/monitoring-distributed-systems/) | 1 | The four golden signals, chosen for what they indicate rather than for availability |
| [**Fawcett**](https://doi.org/10.1016/j.patrec.2005.10.010) | 1 | Discrimination, measured |

---

## The two that fail

**Answer length: AUC 0.45. Citation count: 0.46.** Both indistinguishable from chance.

Both are trivially available on every request. Both *feel* like quality — a longer, more
heavily cited answer looks more thorough. Both are exactly what ends up on a dashboard,
because building a dashboard starts with "what do we already have".

And a system whose answers got longer and more heavily cited would look better on that
dashboard while being no better at all. Worse: week 8 found that padding raises a
word-overlap faithfulness score, so a verbose system moves *three* dashboard metrics in the
right direction while getting no more answers right.

---

## Why easy metrics are usually bad ones

Not a coincidence, and the mechanism is worth naming.

A metric is easy to collect when it is a property of the **artefact** — how long the answer
is, how many citations it has, how fast it was, how many chunks were retrieved. Artefact
properties are right there, structured, free.

A metric is informative when it is a property of the **relationship** between the artefact
and the question — did it answer, was it right, was the answer available. Relationships need
something to compare against, and that something is the expensive part.

So the ranking by collection cost is almost the reverse of the ranking by information, and a
process that starts from what is cheap ends up instrumenting the least informative things
available. That is not a failure of diligence; it is what optimising for cost does.

---

## The exception, and why it is instructive

**Retrieval confidence** is cheap *and* informative — AUC 0.83, one line, no ground truth.

It is a relationship metric that happens to be free: the comparison it needs, query against
context, is already inside the request. Nothing had to be labelled.

So the rule is not "cheap metrics are bad". It is that **a metric's value comes from what it
is compared against**, and the cheap-and-good ones are those where the comparison is already
happening. That is a useful thing to go looking for: *what comparisons does my system already
make, and could any of them be reported?*

Distinct-documents-in-context is another. So is the score margin between the first and second
result. None of them require anything new.

---

## What to do with the useless ones

Not delete them. Length and citation count are worth collecting — for **debugging**, where
"answers suddenly got 40% longer" is a real and useful signal that something changed.

The distinction is between a **diagnostic** and an **indicator**:

- an **indicator** says whether the system is doing its job. It goes on the dashboard, it has
  a threshold, somebody is woken up
- a **diagnostic** helps you find out what happened once an indicator fired. It goes in the
  logs and nobody watches it

Answer length is a fine diagnostic and a terrible indicator, and the failure is putting it in
the wrong column — where a change in it triggers work, and a lack of change is taken as
reassurance.

Measure the AUC. It takes one line, it needs a labelled set you already have, and it tells
you which column a signal belongs in.

---

> **Known** — production monitoring guidance recommends choosing signals by what they
> indicate rather than by availability (`sre-book`) · AUC quantifies discrimination
> independently of any threshold (`fawcett-2006`)
> **Inferred** — that collection cost is inversely related to informativeness, because cheap
> metrics are artefact properties and informative ones are relationship properties. Ours, and
> retrieval confidence is the instructive exception
> **Derived** — a signal with AUC near 0.5 cannot separate the two populations at any
> threshold, so no cutoff makes it a useful indicator
> **Unknown** — how many production RAG dashboards consist mainly of artefact metrics. Every
> one we have been shown, but that is not a sample
