# Thirty cards, and the twelve that matter

*Week 12 · Day 2 · about 20 minutes*

> By the end of this you can see which of the course's findings are mechanisms and which
> are facts about ten RFCs.

---

## Sources

| Source | Tier | What it gives you |
|---|---|---|
| [**Voorhees**, IR evaluation](https://doi.org/10.1007/3-540-45691-0_34) | 1 | What generalises from a test collection, and what does not |
| [**Lin**, *The Neural Hype*](https://doi.org/10.1145/3308774.3308781) | 1 | Findings that were about a baseline rather than a method |

---

## The twelve

This is the course's own edit, offered as a worked example rather than an answer key. Each
one is stated as a class, and each one was found by measuring something specific.

**1 · A metric without its N is not a number.** recall@10 on a ten-document corpus is ~1.0
by construction. *Found in week 1, and it is the first thing most published retrieval
numbers are missing.*

**2 · A shipped default is a hypothesis.** BM25's `k1=1.2` ranked 38th of 45. RRF's `c=60`
captured 0% of the available headroom. Chunk size 400 was dominated at every k. *Three
independent instances, which is what made it a card rather than a grievance.*

**3 · The fact that disqualifies an answer can live in a document the answer did not come
from.** No metric computed over the answer's own sources can see it. *Week 2 found it, week
6 walked into it, week 8 cited it with a perfect score, week 10's attribution said no station
failed.*

**4 · An exact token match is information that a smoothed representation drops.** *Week 5,
and week 11 met the same mechanism again when query expansion destroyed the identifier
family.*

**5 · An aggregate over a set cannot tell you which member was load-bearing.** Answer recall
over a context, faithfulness over an answer, an overlap score over two contexts. *Three
places, three weeks apart.*

**6 · Faithfulness relates the answer to the context; correctness relates it to the world.**
1.00 with 30% of answers confidently wrong. *Week 8, and it is the course's keystone.*

**7 · A judge number without its baseline is not a number.** Accuracy 0.70 is the base rate;
kappa 0.000 is a function returning `True`. *Week 9.*

**8 · Cheap metrics are properties of the artefact; informative ones are properties of the
relationship.** Answer length AUC 0.45, retrieval confidence 0.83. *Week 9, and the
exception — a relationship metric whose comparison is already inside the request — is the
useful part.*

**9 · A proxy is validated for one decision.** AUC 0.83 for *answer in context*, 0.333 for
*will a rewrite help*. Write the arrow. *Week 11.*

**10 · A tolerance below the minimum detectable effect is a coin flip, and the gate will be
muted.** 35% false alarms at 0.02 against ~5% at the MDE. *Week 9.*

**11 · Packaging is not improvement.** A service that meets every SLO over a pipeline that
cannot answer six of twenty questions. *Week 10, and the attribution report is what makes it
sayable.*

**12 · Which edge am I following, and is it already a field?** Multi-hop retrieval along a
metadata edge is a query-time join, replaceable by an ingest-time one at lower cost. *Week
11, and it cost 1.25× to find out.*

---

## What did not make it

Worth naming, because the cuts are instructive.

**"Chunk size 400 is best."** A fact about ten RFCs with a section structure. The
transferable version is card 2, plus *"the most consequential decision in a RAG system has
no primary literature behind it"* — which is a fact about the field and survives.

**"The citation parser counted `[RFC3629]` tags."** A bug. The transferable version is
*print what your rule matched before you believe its count*, which is already week 3's
lesson and does not need a second card.

**"Retrieval confidence predicts answer availability at 0.83."** A measurement on one
corpus with one retriever. Card 8 carries the mechanism; the 0.83 is an example inside it,
not a claim.

**"The loop's iteration count predicts answerability at 0.786."** Same. The transferable
version is *a mechanism's by-product can be worth more than its purpose, and is usually
obtainable more cheaply once identified* — which is a habit and not a number.

Notice the pattern in all four cuts: **the number was the specific thing and the mechanism
was the general one**, and the instinct is to keep the number because it is the part that
took the work.

---

## The honest caveat about all twelve

Every one was measured on ten documents, twenty-six queries, a latent-semantic dense
representation, a simulated generator and a simulated judge.

Voorhees's framing is the right one: a test collection supports **relative comparisons under
stated conditions**. It does not establish absolute quality, and it does not establish that
a mechanism found on one collection is the dominant mechanism on another.

So the twelve are hypotheses with a demonstrated instance each, which is a stronger position
than most of what gets written about this subject and is not the same as a result. The way
to treat them is the way the course treated every default it inherited: as something to
measure on your corpus, with the floor computed first.

---

> **Known** — a test collection supports relative comparisons under stated conditions rather
> than absolute quality claims (`voorhees-2002`) · findings can turn out to be about a
> baseline rather than a method (`lin-neural-hype`)
> **Inferred** — that the generalisable card is the mechanism and not the number, and that
> the instinct is to keep the number because it is the part the work went into. Ours, and the
> four worked cuts are the evidence
> **Inferred** — that a mechanism observed three times in different places is worth a card
> and one observed once is worth a note. Ours, and cards 2 and 5 are the instances
> **Derived** — every finding in the course rests on ten documents, twenty-six queries, a
> latent-semantic dense representation and two stipulated models, so each is a hypothesis
> with one demonstrated instance rather than a result
> **Unknown** — which of the twelve survive on a corpus of a hundred thousand documents with
> a real embedding model and a real generator. Cards 1, 3, 6, 7 and 10 are arithmetic or
> definitional and should; the rest are empirical and might not
