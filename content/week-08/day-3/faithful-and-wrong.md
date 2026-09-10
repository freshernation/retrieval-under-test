# Faithful and wrong

*Week 8 · Day 3 · about 25 minutes*

> By the end of this you can explain why a perfect faithfulness score is compatible with a
> false answer, using a case from your own corpus.

---

## Read the primary sources first

| Source | Tier | What it gives you |
|---|---|---|
| [**RFC 8259**](https://www.rfc-editor.org/rfc/rfc8259.txt) §8.1 | 1 | `MUST be encoded using UTF-8`, December 2017 |
| [**RFC 7159**](https://www.rfc-editor.org/rfc/rfc7159.txt) §8.1 | 1 | `SHALL be encoded in UTF-8, UTF-16, or UTF-32`, March 2014, withdrawn |
| [**RFC 2026**](https://www.rfc-editor.org/rfc/rfc2026.txt) §2.1 | 1 | Why 7159 does not know it was withdrawn |
| [**Rashkin et al.**](https://arxiv.org/abs/2112.12870) | 1 | Attribution defined as a relation to a source, not to truth |

---

## The case

**Query:** *must JSON be encoded in UTF-8*

**Answer:**

> Character Encoding JSON text SHALL be encoded in UTF-8, UTF-16, or UTF-32. `[rfc-7159#10]`
> The default encoding is UTF-8, and JSON texts that are encoded in UTF-8 are interoperable…
> `[rfc-7159#10]`

**Faithfulness: 1.00.** Every sentence is verbatim from the chunk it cites. The citation
resolves. The chunk was in the context. The support check is not being fooled — the chunk
really does say that.

**RFC 7159 was withdrawn in December 2017.** The current rule is `MUST be encoded using
UTF-8`, and it is in RFC 8259, which was also in the context, ranked second.

---

## Why no faithfulness metric can catch it

Faithfulness is a relation between the **answer** and the **context**. Both are present, both
are checkable, and the relation holds perfectly.

The fact that makes the answer wrong is not in the answer and not in the cited chunk. It is
in `rfc-8259`'s header — `Obsoletes: 7159` — a **different document**, which week 2 spent a
day establishing:

> An RFC is never revised after publication, so a superseded document contains no trace of
> its own supersession.

Improving the support check does not help. A model judge does not help — ask it *"is this
claim supported by this passage?"* and the correct answer is yes. Prompting does not help;
the instruction *"only use the provided context"* was followed exactly.

**The failure is at station 1, surfaced at station 6.** Week 2 found the trap, week 6 watched
retrieval walk into it, and this is what it produces.

---

## The three relations

| | relates | measurable here |
|---|---|---|
| **grounded** | context ↔ world | yes, via answer spans |
| **faithful** | answer ↔ context | yes, by proxy |
| **correct** | answer ↔ world | **no** |

Faithfulness is a property of the *pipeline's internal consistency*. It is genuinely
valuable — it catches invention, misattribution and overreach, and those are real failures —
and it is silent about the world by construction.

> Every *"we measure faithfulness, so our answers are trustworthy"* claim is this confusion.

Two numbers in the default report card make it unmissable: **faithfulness 1.00**, and **six
of twenty answers confidently wrong**. Neither is an error. They are answers to different
questions, and reporting either alone is misleading.

---

## What does catch it

`cites_superseded` — week 2's supersession graph, applied to the answer's citations. Three
answers flagged: `r05`, `r07`, `r23`.

Notice where it lives: **outside** the faithfulness machinery, in its own function, needing a
different kind of evidence — metadata rather than text.

That separation is the design lesson. A check requiring different evidence is a different
check, and folding a currency test into a faithfulness score produces a number that quietly
means something else and cannot be compared with anybody's.

Report them side by side. Do not average them.

---

## What the fix actually is

Not a prompt. Not a better judge. Not a stricter threshold.

**Week 2's demotion**, at station 5: rank the superseded chunk below its replacement, so the
generator's preference for the top-ranked chunk lands on `rfc-8259`. The answer changes
because the *context* changes, which is the only lever that works when the defect is
provenance.

Week 2 shipped that fix as a correctness fix with an interval that touched zero, and argued
it should ship anyway. Six weeks later, this is the argument's payoff.

---

> **Known** — RFC 8259 requires UTF-8 and obsoletes RFC 7159 (`rfc8259`) · RFC 7159 permits
> UTF-16 and UTF-32 (`rfc7159`) · a published RFC is never revised, so it carries no record of
> its own supersession (`rfc2026`) · attribution is defined as a relation between a claim and a
> source (`rashkin-2021`)
> **Inferred** — that no faithfulness metric, however implemented, can detect this class of
> error. Follows from the disqualifying fact being absent from both the answer and the cited
> source
> **Derived** — a claim copied verbatim from its cited chunk scores maximally on any
> support-based faithfulness measure, whatever the chunk's currency
> **Unknown** — what fraction of production RAG answers are faithful to superseded sources.
> Unmeasurable without supersession metadata, which most corpora do not carry
