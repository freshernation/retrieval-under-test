# Stipulated models

*Week 7 · Day 4 · about 20 minutes*

> By the end of this you can use a model you cannot verify without being misled by it, and
> you will recognise the pattern when somebody else does not.

---

## Sources

| Source | Tier | What it gives you |
|---|---|---|
| [**Liu et al.**](https://arxiv.org/abs/2307.03172) | 1 | The shape being borrowed |

> The discipline in this article is ours. It is the same rule week 4 applied to chunk sizes
> and week 3 applied to a plateau, stated generally.

---

## What a stipulated model is

A model you adopt because you need *some* model, whose form is defensible and whose
parameters are invented.

`attention_weight` is one: a parabola, 1.0 at the ends, `dip` in the middle. The U-shape
comes from a Tier 1 source. The parabola, and `dip = 0.5`, come from nowhere — a real curve
depends on the model, the prompt, the window length and the task, and this course has none
of those.

There is nothing wrong with this. Every simulation, every cost model, every capacity plan is
built on stipulated numbers. What matters is what you are then allowed to say.

---

## The rule

> **Assert the direction, never the value.**

Concretely, for a stipulated model:

**You may say** that A ranks above B under it. That is a comparison, and if it survives
varying the parameter it depends on the model's *shape* rather than its numbers.

**You may not say** that A scores 0.687 and B scores 0.670. Those are outputs of a parabola
somebody invented, and the moment they appear in a report somebody will quote them back as
evidence — usually within a month, usually to justify a decision, usually without the word
"stipulated" attached.

**You must report the sensitivity.** Vary the parameter across its plausible range and check
the ordering holds. If it flips, you have learned that the comparison is a claim about the
parameter and not about the orderings, which is a genuine and useful finding.

This is exactly the discipline that let week 4 report a chunking frontier without asserting
a chunk size, and let week 3 refuse to ship a k1 plateau it did not understand. The failure
it prevents is a number acquiring authority it never had.

---

## How stipulated numbers escape

The mechanism is always the same and it is worth recognising:

1. Somebody builds a model to compare two options
2. The comparison is reported with its scores, because scores look rigorous
3. A reader quotes a score without the model
4. The score is now a fact about the world

Step 3 does not require carelessness. A number in a table is a number in a table, and the
caveat lives in a paragraph the reader did not copy.

The defence is to make the number **unquotable**: report the ordering, report the
sensitivity, and do not put the score in the table at all. That is why the week-7 report
template forbids it explicitly rather than merely warning about it.

---

## When to stop stipulating

As soon as you can measure.

Week 8 has a generator. The very first thing to do with it is to check today's ordering
against a real one — and it may not survive, in which case a week of your reasoning was
wrong in a way that cost nothing, because you never asserted the values.

That is the whole point of the discipline. A stipulated model held loosely is a way to make
a decision under uncertainty and change it cheaply. A stipulated model whose numbers you
have quoted is a commitment you will defend.

---

## The pattern in other people's work

Once you have done this deliberately you will notice how often it is not.

- A cost model with an assumed cache hit rate, quoted as a saving
- A latency budget with an assumed p99, quoted as a guarantee
- A retrieval benchmark with an assumed query distribution, quoted as accuracy
- **An LLM-as-judge score with an assumed rubric**, quoted as quality

The last one is week 9, it has more authority attached than any of the others because it
comes out of a model, and it is the same problem exactly.

The question to ask, of your own work and everyone else's: **which of these numbers could I
check, and which did somebody choose?**

---

> **Known** — the positional shape is reported in the literature for particular models and
> settings (`lost-in-the-middle`)
> **Inferred** — that stipulated models should be reported as orderings with sensitivity
> rather than as scores. Ours; it is a discipline rather than a result, and this course
> applies it in weeks 3, 4 and 7
> **Derived** — a comparison invariant to a model's free parameter depends on the model's
> shape rather than its parameterisation
> **Unknown** — how much of the practical guidance circulating about RAG rests on stipulated
> numbers reported as measurements. Our impression is: a great deal
