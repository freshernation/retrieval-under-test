# The generator is a stipulated model

*Week 8 · Day 1 · about 20 minutes*

> By the end of this you can say what this week's results are evidence for, and what they
> are not.

---

## Sources

| Source | Tier | What it gives you |
|---|---|---|
| [**Liu et al., *Lost in the Middle***](https://arxiv.org/abs/2307.03172) | 1 | Week 7's stipulated model, and the discipline this article reuses |
| [**Ji et al., *Survey of Hallucination in NLG***](https://arxiv.org/abs/2202.03629) | 1 | The behaviours the simulator is built to reproduce |

> The simulator itself is ours, and this article is the disclosure.

---

## What it is

`raglab.generator.SimulatedGenerator` is about a hundred lines of rules. Given a query and a
context it scores each chunk by query-term overlap, picks the best, copies the sentences with
the most query terms, and appends a citation.

It has three switchable faults, deliberately orthogonal because they are caught by different
machinery:

| flag | behaviour | caught by |
|---|---|---|
| `fabricate` | cites an id that was not in the context | resolving ids (Tuesday) |
| `misattribute` | cites a real, present chunk that does not support the claim | support check (Wednesday) |
| `overreach` | adds a confident sentence supported by nothing | support check (Wednesday) |

And one that is off by default and is the point of Thursday: `refuse_below`.

---

## What it reproduces faithfully

These are the behaviours week 8 is about, and the simulator has them because they are what a
real system does:

- **It answers whatever it is given**, including when the context contains no answer. This is
  the default behaviour of every generation system before somebody designs against it
- **It grounds its wording in the retrieved text**, so its answers read as well-supported
  whether or not they are
- **It cites**, and its citations fail in the two distinct ways real citations fail
- **It prefers the highest-ranked chunk**, so a superseded document that outranks its
  replacement produces a confident, fluent, wrong answer

---

## What it does not

Paraphrase. Synthesis across chunks. Reasoning. Fluency failures. Refusal in phrasings other
than one fixed sentence. Every emergent behaviour that makes a real model interesting or
dangerous.

So: **do not use this week's numbers to estimate how good your answers will be.**

Its faithfulness of 1.00 is a property of a rule-based copier — it quotes verbatim, and the
support check rewards copying. A real model paraphrases, and would score *lower* on the same
metric while being no less faithful. The number is an artefact of the pair.

---

## The rule, unchanged from week 7

> **Assert the direction, never the value.**

What transfers from this week:

- the **machinery** — the citation checker, the support check, the four-way refusal table,
  the report card. All of it runs unchanged against a real model
- the **comparisons** — a misattributing generator scores far below a faithful one; refusal
  removes wrong answers before it removes right ones; `grounded_rate` is blind to every
  generation fault
- the **structural findings** — faithfulness is not correctness; a citation proves provenance
  and not truth; refusal does not happen on its own

What does not transfer: every absolute number on the report card.

---

## Why not just use a model

Three reasons, and the third is the one that decided it.

**Determinism.** A test whose result depends on sampling is not a test, and a result you
cannot reproduce cannot be attributed to a station.

**Access.** A course whose labs need a paid account is a course some students cannot take.

**Isolation.** With a real model, every finding this week would be confounded by the model's
own behaviour, and a student could not tell a bug in their citation checker from a quirk of
the model. The simulator holds station 6 still so that stations 1 to 5 and the *checking
machinery* are what vary.

By week 10 there is a real model and `--live` mode, and the first thing to do with it is
re-run this week's checks and see which of the comparisons survive. Some will not, and
finding out which is a better exercise than never having had the baseline.

---

> **Known** — the failure behaviours simulated here — answering without support, citation
> errors, confident fabrication — are documented in the hallucination literature (`ji-2022`)
> **Inferred** — that holding the generator fixed isolates the checking machinery, which is
> the part that transfers. Ours, and it is the design argument for the simulator
> **Derived** — a support metric based on word overlap scores verbatim copying at 1.0, so a
> copying generator's faithfulness is an artefact of the metric-generator pair
> **Unknown** — which of this week's comparisons survive contact with a real model. Testable
> from week 10 and worth doing deliberately
