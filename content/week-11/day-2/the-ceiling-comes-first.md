# The ceiling comes first

*Week 11 · Day 2 · about 25 minutes*

> By the end of this you can compute what routing could buy before you build a router, and
> you will know what happened when this course tried.

---

## Sources

| Source | Tier | What it gives you |
|---|---|---|
| [**Cormack, Clarke & Buettcher**, RRF](https://doi.org/10.1145/1571941.1572114) | 1 | Combining rankings, and the oracle framing week 6 used |
| [**Cohen**, *Statistical Power Analysis*](https://doi.org/10.4324/9780203771587) | 2 | Why the n on which a decision rests is the n that matters |
| [**LangGraph** documentation](https://langchain-ai.github.io/langgraph/) | 3 | Routing as a framework primitive, which is where most people meet it |

---

## Why the ceiling, and why first

Day 1 produced a rewrite that gains two queries and loses three. The right response is not
to abandon it — it is to apply it only where it helps. That is routing, and it is the most
defensible idea in this week.

So compute the ceiling before building the router. Week 7 computed the reranking ceiling
before the reranker; the reason is the same and it is worth stating as a rule.

**A mechanism whose maximum possible gain you have not calculated is a mechanism you cannot
evaluate.** Build a router, measure +0.00, and you cannot tell *"the router does not work"*
from *"there was nothing here to get"*. Those have opposite responses — fix the signal
versus stop working on this — and nothing in the measurement distinguishes them.

The oracle is four lines: per query, did **any** strategy answer it.

| | answered |
|---|---|
| baseline | 0.700 |
| rewrite | 0.650 |
| **oracle** | **0.800** |
| headroom | **0.100** |

Ten points, from two strategies neither of which gets there. The opportunity is real and it
is the largest unexploited gap the course has found since week 7's reranking ceiling.

The oracle is not achievable, by construction: it requires knowing whether a strategy
answered the query before choosing the strategy. That is what makes it a ceiling rather
than a design.

---

## The router, and what it captured

The signal is week 9's best discovery: retrieval confidence. AUC 0.83 for predicting
whether the answer reached the context, no ground truth needed, available on every request.
A router is exactly what a signal like that is for, and the direction is the intuitive
one — rewrite the queries the retriever seems unsure about.

Swept across ten thresholds:

| threshold | routed | answered | capture |
|---|---|---|---|
| 0.50 | 2 | 0.700 | 0% |
| 0.60 | 5 | 0.700 | 0% |
| 0.65 | 8 | 0.700 | 0% |
| **0.70** | 10 | 0.650 | **-50%** |
| 0.75 | 11 | 0.650 | -50% |
| 0.80 | 12 | 0.700 | 0% |
| 1.01 | 20 | 0.650 | -50% |

**Zero per cent at best.** Negative at four of the ten. No threshold beats not routing at
all.

---

## Why, exactly

Look at where the decisive queries sit on the signal.

| query | confidence | rewrite |
|---|---|---|
| `r21` | 0.556 | **helps** |
| `r04` | 0.571 | hurts |
| `r07` | 0.667 | hurts |
| `r23` | 0.778 | **helps** |
| `r06` | 0.800 | hurts |

Interleaved. The two queries the rewrite gains sit at 0.556 and 0.778, with two it loses
between them and one above. No threshold separates those sets, because they are not
separated.

This is the second time a reasonable default has captured none of a real gap. Week 6 found
RRF's `c=60` capturing **0%** of the available fusion headroom while `c=10` captured 100%.
The mechanism is the same both times: **the quantity being thresholded is not the quantity
that decides the outcome**, and nothing about a threshold sweep can create a separation that
the signal does not contain.

---

## Five queries decide it

Here is the part that should stop the work.

Of twenty queries, **five** have a different outcome under the two strategies. The other
fifteen are invariant — route them however you like and nothing happens. So those five are
the entire evidence base for any router you build.

Week 9 measured a minimum detectable effect of 0.1003 at n=19. At n=5 nothing is
detectable. Which means **a router cannot be validated on this eval set** — not that it does
not work, but that the set cannot say, and any router that appears to work has been fitted
to five observations.

That is the cheapest argument against shipping a router that anybody will ever hand you,
and it takes one line of counting to produce. Run it before the sweep, not after.

---

> **Known** — combining rankings is evaluated against the best achievable combination, and a
> constant chosen without that comparison cannot be assessed (`cormack-2009`) · a claim's
> reliability depends on the n of the comparison that produced it (`cohen-1988`) · routing
> is offered as a first-class primitive by agent frameworks (`langgraph-docs`)
> **Inferred** — that an oracle ceiling must be computed before the mechanism, because
> without it a null result is indistinguishable from an absent opportunity. Ours, stated in
> week 7 and generalised here
> **Inferred** — that counting the decisive queries is the cheapest pre-check available
> before building a router, since those queries are its entire evidence base. Ours
> **Derived** — baseline 0.700, rewrite 0.650 and oracle 0.800 give ten points of routing
> headroom · a confidence-threshold router captures at most 0% of it across ten thresholds
> and -50% at four of them · the two queries the rewrite gains sit at confidence 0.556 and
> 0.778 with two it loses between them, so no threshold separates the sets · five of twenty
> queries are decisive, and the MDE at that n exceeds any effect available
> **Unknown** — whether any serving-time signal separates *this rewrite helps* from *this
> rewrite hurts*. We have not found one, and the search space is not large
