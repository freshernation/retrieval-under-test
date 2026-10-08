# Week 11 — Agentic retrieval

> **Destination**
> Build the four things an agent is made of, aim each at a failure identified
> *before* you chose the technique, and find out what they cost.

> **Deep track** — the whole week. It is the course's third project and its hardest
> measurement problem, because every technique here is defensible, fashionable, and
> plausible-sounding when it does not work.

Week 10's attribution report named six failures. Five are the candidate set. Rewriting,
routing and multi-hop each claim to fix one of those, so this week has a target list
rather than a reading list.

---

## The week

| Day | Folder | What you'll be able to do |
|---|---|---|
| Mon | `day-1/` | Rewrite a query without letting the eval set into the rule |
| Tue | `day-2/` | Compute a routing ceiling, and find out what captures it |
| Wed | `day-3/` | Hop to a superseding document, and name what the hop really is |
| Thu | `day-4/` | Run a loop, and tell its progress from its motion |
| Fri | `milestone/` | **Project 3** — an agent, measured, and the recommendation |

---

## Five findings

**The rewrite helps what it was not aimed at.** Pseudo-relevance feedback gains `r21` and
`r23`, loses `r04`, `r06` and `r07`, and leaves the `paraphrase` family at **1/3** — the two
queries the week was aimed at are untouched. By family: plain and vocabulary-gap up,
identifier and acronym and superseded down. Week 5's finding in a new hat — adding terms
helps loose prose and destroys an exact match.

**Routing has ten points of headroom and the router captures none.** Baseline 0.70, a
perfect router 0.80. Week 9's best signal — retrieval confidence, AUC 0.83 — swept across
ten thresholds: **0% at best, -50% at four of them.** Asked the new question *"will a
rewrite help"* the same signal scores strength 0.667, under the floor. A proxy is validated
for one decision at a time.

**And the router that works needs a field production does not have.** Route by query
*family* and it captures **100%** — exactly the oracle. Family is a label in the eval set.
Week 9's serving-time gap in its strongest form: not a metric you cannot compute, but a
decision you cannot make.

**The agentic win is a metadata join.**

| | citing superseded | answered | retrievals |
|---|---|---|---|
| baseline | 3 | 0.700 | 20 |
| second hop | **0** | 0.650 | **25** |
| week 2's `is_current` filter | **0** | 0.650 | 20 |

Identical, at 1.25× the cost, and the filter was available before embeddings existed. And
the fix breaks `r07`, the query where supersession was *not* an error — which week 2 put in
the corpus on purpose.

**Every iteration after the first is churn.** At a 0.8 bar the loop makes 44 retrievals for
20 queries, the answered rate is 0.700 at every price, and no query ever stops on iteration
two: either the first retrieval was enough or the loop ran to the cap. All 24 extra
iterations changed the candidate set and improved nothing. A no-progress detector built on
*did the candidate set change* fires never.

---

## Project 3

The best configuration — loop **and** hop, which neither achieves alone — gets the best
numbers in the course: answered **0.75**, citing superseded **0**, at **2.45×** the
retrievals.

`ship_check` refuses. +0.05 is inside week 9's MDE of 0.1003: the gain is one query and it
is not distinguishable from zero, and four days of work does not change that.

The recommendation Project 3 asks for is **ship the hop, do not ship the loop, and go and
write more queries.**

---

## Milestone

Project 3, and the refusal. Spec in `milestone/README.md`.
