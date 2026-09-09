# A filter is a requirement, not a defect

*Week 6 · Day 4 · about 20 minutes*

> By the end of this you can tell a filter that broke your system from a filter that is
> doing its job.

---

## Sources

| Source | Tier | What it gives you |
|---|---|---|
| [**RFC 2026**](https://www.rfc-editor.org/rfc/rfc2026.txt) §2.1 | 1 | What "obsoletes" means, and why currency is a property you can filter on |
| [**RFC 7322**](https://www.rfc-editor.org/rfc/rfc7322.txt) §4 | 1 | The metadata that makes the filter possible |

---

## The number that looks like a disaster

`published_since(2015)` takes answer recall from **0.789 to 0.316**.

Sixty percent of your retrieval quality, gone, from one predicate.

If that number reaches a dashboard without context, somebody will spend a quarter trying to
fix it. And there is nothing to fix: most of the answers are in RFC 3986 (2005), RFC 6265
(2011) and RFC 6585 (2012), and the user asked not to see documents published before 2015.

**The filter did exactly what it was told.** The recall loss is the requirement, expressed
as a number.

---

## The rule

> **A filtered system must be measured against what the filter allows**, not against the
> unfiltered corpus.

Two different questions, and only one of them is about your retriever:

- *Of the answers the filter permits, how many did we find?* — retrieval quality
- *Of all the answers, how many does the filter permit?* — a property of the requirement

Report both, separately, and label them. Collapsing them into one number produces either a
system that looks broken or a requirement that looks free, and both cost somebody a
quarter.

---

## How to tell which you are looking at

Ask one question: **is the answer inside the filter's scope?**

- Answer is in a permitted document and you did not retrieve it → **your problem**
- Answer is only in an excluded document → **the requirement's consequence**

`unreachable`, restricted to the filtered corpus, separates them mechanically. It is worth
running before you conclude anything about a filtered system's quality.

---

## The other direction: filters that hide a defect

The converse is worth naming because it is sneakier.

Week 2's currency filter removes superseded documents. Apply it and the query *"what did
RFC 8259 change about JSON?"* becomes unanswerable — the obsolete half of the pair is gone,
and the comparison exists in neither remaining document.

Week 2 chose **demotion** for exactly this reason: the obsolete document is the only answer
to "what changed". Today you implemented the same relation as a **hard filter**, and it is a
different product.

Neither is right. They are answers to different questions:

| | keeps "what changed" | risks returning withdrawn text |
|---|---|---|
| demote | **yes** | yes, lower down |
| filter | no | **no** |

Which you want depends on who is asking and what happens when they are wrong — the same
shape as week 2's refusal policy, and the same conclusion: **it is not a technical decision
and it should not be made by default.**

---

## What belongs in the report

- The predicate, in words a non-engineer can check
- What fraction of the corpus it keeps
- Recall **within** the filter's scope
- What the filter makes unanswerable, with an example
- Whether it is a hard filter or a demotion, and who chose

The fourth is the one nobody writes and the one that gets discovered by a user.

---

> **Known** — supersession is a formal relation declared in document metadata (`rfc2026`,
> `rfc7322`)
> **Inferred** — that filtered systems should be measured within the filter's scope. Ours,
> and it follows from the two questions being distinct
> **Derived** — if the answers to a query exist only in documents a filter excludes, no
> retriever operating under that filter can retrieve them
> **Unknown** — how often production systems report retrieval quality without saying which
> filters were active. Anecdotally, usually
