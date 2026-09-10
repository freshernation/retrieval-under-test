# Week 8 — Generation and grounding

> **Destination**
> Ship a system that answers questions from your corpus, and a set of checks that tell you
> when it is lying — none of which involve reading the answers.

**Project 2.** Seven weeks of retrieval finally produce prose, and the first thing prose
does is prove week 1's claim.

---

## The week

| Day | Folder | What you'll be able to do |
|---|---|---|
| Mon | `day-1/` | Measure whether the answer was ever in the context |
| Tue | `day-2/` | Check citations, and find a bug in your own checker |
| Wed | `day-3/` | Measure faithfulness, and see why it is not correctness |
| Thu | `day-4/` | Design refusal, and price it |
| Fri | `milestone/` | **Project 2** — the pipeline and its report card |

---

## The generator is a stipulated model

There is no language model in this course: weeks 1 to 9 run offline, deterministically, with
no API key. `raglab.generator.SimulatedGenerator` is a hundred lines of rules that reproduce
the behaviours this week is about — it answers whatever it is given, grounds its wording in
the retrieved text, cites, and prefers the highest-ranked chunk.

It does not paraphrase, synthesise or reason. **Do not use it to estimate answer quality.**
Use it to test the machinery that checks answers, which is what this week builds and which
is the part that transfers. Week 7's rule applies unchanged.

---

## Four numbers, and why you need all of them

**It answers everything.** Twenty queries, twenty answers, zero refusals — including the
out-of-scope one and the two that nothing retrieves. That is the default behaviour of every
generation system before somebody designs against it.

**Thirty percent are confidently wrong.** Fourteen of twenty had the answer somewhere in the
context. All twenty got fluent, cited prose. Six are confident answers to questions the
system could not answer, and nothing in the text distinguishes them.

**Your citation checker reports fabrications that never happened.** The naive parser finds
44 citations and flags 5 as unresolvable. The generator invented none — the five are
`[RFC3629]`-style cross-references *quoted from the corpus*. An 11% false-positive
fabrication rate, sourced from the documents, and you would have blamed the model.

**Faithfulness is 1.00.** Every sentence is supported by the chunk it cites. Thirty percent
of the answers are still wrong.

---

## The keystone

`r05` — *must JSON be encoded in UTF-8*.

The answer opens *"JSON text SHALL be encoded in UTF-8, UTF-16, or UTF-32"*, cited to
`rfc-7159#10`. Faithfulness **1.0**: the chunk says exactly that.

RFC 7159 was withdrawn in December 2017.

Week 2 found the trap. Week 6 watched retrieval walk into it. This is what it produces at
the last station: a fluent, correctly cited, perfectly faithful, **false** answer — and
nothing inside the faithfulness machinery can see it, because the fact that makes it wrong
is in a different document.

> **Faithfulness is a relation between the answer and the context. Correctness is a relation
> between the answer and the world.** Measuring the first tells you nothing about the second,
> and every "we measure faithfulness, so our answers are trustworthy" claim is this
> confusion.

---

## And the one thing that helps

Refusal is not free, but the **first part of it is**. At a confidence threshold of 0.55:
fourteen correct answers kept — all of them — and two confidently-wrong answers removed, at
a cost of exactly nothing.

Past that, every further refusal is bought with a correct answer, and the exchange rate gets
worse. Where you stop is a question about what a wrong answer costs relative to an unhelpful
one, which is not a technical question and is not yours to answer alone.

---

## Milestone

**Project 2**: the pipeline, and a report card in which every number was computed by
machinery you wrote. Spec in `milestone/README.md`.
