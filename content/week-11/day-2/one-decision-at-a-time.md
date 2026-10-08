# A proxy is validated for one decision

*Week 11 · Day 2 · about 20 minutes*

> By the end of this you can explain why week 9's best signal is worthless here without
> anything being wrong with week 9's measurement.

---

## Sources

| Source | Tier | What it gives you |
|---|---|---|
| [**Fawcett**, ROC analysis](https://doi.org/10.1016/j.patrec.2005.10.010) | 1 | AUC as discrimination *of a specified outcome* |
| [**Google SRE Book**, ch. 6](https://sre.google/sre-book/monitoring-distributed-systems/) | 1 | Signals chosen for the decision they inform |

---

## The same number, two questions

Week 9 asked: **does retrieval confidence predict whether the answer reached the context?**

> AUC 0.83. Strength 0.83. Clear of the 0.7 floor. One of the two best serving-time signals
> the course found, free on every request, and nobody instruments it.

Week 11 asks: **does retrieval confidence predict whether a rewrite will help?**

> AUC 0.333. Strength 0.667. Under the floor.

Nothing has changed about the signal, the pipeline, or week 9's arithmetic. The second
result is not a correction of the first. They are answers to different questions and the
signal carries one fact and not the other.

---

## Why this is easy to get wrong

Because of how a validated proxy gets talked about afterwards.

Week 9's result, stated carefully: *retrieval confidence discriminates contexts containing
the answer from contexts not containing it, at 0.83.* Stated the way it will be repeated
three meetings later: **"retrieval confidence is a good quality signal."**

The second sentence has no outcome in it. Once the outcome is dropped, the signal becomes
a general-purpose virtue and gets attached to any decision that needs one — route on it,
gate on it, alert on it, show it to the user. Each of those is a different outcome and each
needs its own validation.

Fawcett is explicit about this and it is in the definition: AUC is the probability that a
randomly chosen **positive** outranks a randomly chosen **negative**. Change what counts as
positive and you have changed the measurement. The number is about a pair of populations,
not about the signal.

So the discipline is a naming one. Not *"confidence: AUC 0.83"* but **"confidence → answer
in context: 0.83"**, with the arrow, every time. The arrow is what stops the number
travelling.

---

## And it is not a surprise if you look at the mechanism

Retrieval confidence is the query's term overlap with its best-matching context chunk. It
measures **how well the retrieval matched the words of the question**.

*Did the answer end up in the context* is close to that. A high-overlap chunk is likely to
be the right chunk, and the 0.83 is unsurprising in hindsight.

*Will adding feedback terms to this query help* is a question about something else
entirely: whether the query was under-specified, whether the top documents are relevant
enough to harvest from, and whether the query's existing match is exact enough to be worth
protecting. Day 1 showed that last one dominates — the queries expansion destroys are the
precise identifiers, and a precise identifier has **high** confidence, which is the wrong
side of every threshold.

In fact the sign is arguably reversed from the intuitive design. The router rewrites
low-confidence queries; the queries most *damaged* by rewriting are high-confidence ones,
which the router leaves alone — and yet it still captures nothing, because the queries
rewriting *helps* are also spread across the range.

---

## The field it would need

One router does capture the headroom. Route by query **family** — rewrite the `plain` and
`vocabulary-gap` queries, leave `identifier`, `acronym` and `superseded` alone — and it
reaches **0.800**, exactly the oracle. **100% capture.**

Family is a label in the eval set. It was written by the person who wrote the judgments. It
does not arrive with a request, and no serving-time signal in this course predicts it.

So the routing opportunity is real, fully realisable, and realisable only with information
the running system does not possess.

That is week 9's serving-time gap in its strongest form. Week 9 found metrics you cannot
compute live. This is **a decision you cannot make live** — and the difference matters,
because a metric you cannot compute can be approximated by a proxy, whereas a decision
whose input does not exist has to be given one.

Which is, finally, a constructive finding. It names a concrete thing worth building: a
query classifier over families, trained on labels you are already writing. Not an agent. A
classifier, with a confusion matrix, that you could validate — if you had more than five
decisive queries, which you do not.

---

> **Known** — AUC is the probability that a randomly chosen positive outranks a randomly
> chosen negative, and is therefore defined relative to a specified outcome
> (`fawcett-2006`) · monitoring signals should be chosen for the decision they inform
> (`sre-book`)
> **Inferred** — that a validated proxy's outcome is routinely dropped when the result is
> repeated, turning a measurement about two populations into a general-purpose virtue, and
> that writing the arrow prevents it. Ours
> **Inferred** — that a decision whose input does not exist at serving time is a harder
> problem than a metric that cannot be computed there, because the second admits a proxy and
> the first requires a new field. Ours
> **Derived** — the same signal scores 0.83 against *answer in context* and 0.333 (strength
> 0.667) against *rewrite helps*, on the same queries and the same pipeline · a family-based
> router reaches 0.800, capturing 100% of the headroom, using a label the eval set carries
> and a request does not
> **Unknown** — whether query family is predictable from a request. It is the obvious thing
> to build next, and five decisive queries cannot validate it
