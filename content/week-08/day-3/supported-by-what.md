# Supported by what

*Week 8 · Day 3 · about 25 minutes*

> By the end of this you can measure whether each claim is supported by its cited source, and
> state precisely what your measurement cannot see.

---

## Read the primary sources first

| Source | Tier | What it gives you |
|---|---|---|
| [**Rashkin et al., *Attributable to Identified Sources***](https://arxiv.org/abs/2112.12870) | 1 | What "supported by" means formally, and what evaluating it costs |
| [**Es et al., *RAGAS***](https://arxiv.org/abs/2309.15217) | 1 | The faithfulness metric most RAG work uses, and how it is computed |
| [**Ji et al.**](https://arxiv.org/abs/2202.03629) | 1 | Intrinsic hallucination — the class this check is aimed at |

---

## The definition

**Faithfulness**: every claim in the answer follows from the retrieved context.

Not "is true". Not "is useful". Follows from — a relation between two texts, both of which
you have, which is exactly why it is measurable at all when correctness is not.

The standard decomposition, and it is the one to copy:

1. Split the answer into **claims** — sentences, for a first approximation
2. For each, find the **source** it cites
3. Ask whether the source **supports** it
4. Faithfulness is the fraction supported

Steps 1, 2 and 4 are mechanical. Step 3 is the whole problem.

---

## Today's proxy, and its four failures

`support(claim, source)` = fraction of the claim's words present in the source.

It catches copied text and blatant invention, and it is a **proxy**. Four things it cannot
do, and you should be able to state all four:

**It cannot see a negation.** `A crawler MUST assume complete disallow` and
`A crawler MUST NOT assume complete disallow` differ by one word and score above 0.8 against
the same source. This is the failure that matters most and word overlap is structurally blind
to it.

**It cannot see a swapped number.** `429` for `431`, `24 hours` for `48 hours`. One token out
of twenty.

**It punishes correct paraphrase.** *"Return 429 when a client is being throttled"* is a
faithful summary of the source and scores under 0.6, while a verbatim copy scores 1.0.
**Backwards as a measure of quality** — it rewards the behaviour you least want, which is a
generator that copies rather than answers.

**It has an arbitrary threshold.** 0.8 is a number this course chose. Nothing derives it.

So the metric is useful for **comparing configurations** — a misattributing generator scores
0.09 against a faithful one's 1.00, and that ordering is real — and useless as an absolute
statement about answer quality. Week 7's discipline again.

---

## What a real faithfulness check does

It asks a model. That is what RAGAS-style faithfulness is: decompose the answer into claims,
then have a language model judge whether each is entailed by the context.

Which is genuinely better at negation and paraphrase, and introduces a different problem
entirely: **you are now measuring your system with a system of unknown accuracy**, whose
errors correlate with your generator's, and which produces numbers with a model's authority
attached.

That is next week, and week 7 already taught the defence.

---

## Three design decisions worth making deliberately

**Refusals are vacuously faithful.** "I could not find an answer" shares no words with the
context. A naive implementation scores it 0.0 and punishes the system for the one behaviour
you are trying to encourage. Check for it explicitly.

**Refusals are excluded from the aggregate.** Include them at 1.0 and a system that declines
everything scores perfectly. This is the easiest way to game any faithfulness metric and it
is not hypothetical.

**Uncited claims are checked against the whole context.** That is the lenient choice. A
stricter system scores them zero, on the grounds that an unattributed claim is unverifiable
by a reader. Pick one deliberately, record which in the `basis` field, and say so in the
report — otherwise two teams' faithfulness numbers are not comparable and neither knows.

---

## The number

The default generator scores **1.00**. It copies sentences from the chunks it cites, and the
support check rewards copying.

That number is an artefact of a rule-based generator meeting a word-overlap metric. Do not
carry it anywhere. What to carry is the *comparison*: misattribution collapses it to 0.09,
overreach drops it to 0.74, and both are detected by machinery that never reads for meaning.

---

> **Known** — attribution has a formal definition requiring a claim to be supported by an
> identified source (`rashkin-2021`) · the standard RAG faithfulness metric decomposes an
> answer into claims and judges each against the context, using a model (`ragas-2023`) ·
> intrinsic hallucination is contradiction of the provided context (`ji-2022`)
> **Inferred** — that a word-overlap support check is usable for comparing configurations and
> not for absolute claims. Ours, from the four failures enumerated
> **Derived** — a metric scoring verbatim copying at 1.0 rewards a copying generator over a
> paraphrasing one of equal fidelity
> **Unknown** — how much a word-overlap proxy disagrees with a model judge on real answers. It
> is measurable in week 9 and it is the right first experiment there
