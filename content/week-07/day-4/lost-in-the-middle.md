# Lost in the middle

*Week 7 · Day 4 · about 25 minutes*

> By the end of this you can order a context window on the best evidence available, and say
> precisely how weak that evidence is for your case.

---

## Read the primary source first

| Source | Tier | What it gives you |
|---|---|---|
| [**Liu et al., *Lost in the Middle: How Language Models Use Long Contexts***](https://arxiv.org/abs/2307.03172) | 1 | The measurement, the models tested, and the conditions. **Read what was varied** |
| [**Liu et al.**](https://arxiv.org/abs/2307.03172) §4 | 1 | The multi-document QA setup, which is close to a RAG window and not identical |

---

## The finding

Place a document containing the answer at different positions in a long context and ask the
same question. Performance is **highest when it is at the beginning or the end**, and
lowest in the middle.

A U-shape. Reported across several models, at several context lengths, and it is one of the
most-cited practical results about long contexts.

The obvious consequence: **do not put your best result in the middle.** `ends_first` — rank
1 first, rank 2 last, rank 3 second — is the standard mitigation and it is three lines.

---

## Read what was actually varied

This is the part that gets dropped, and it is why today's lab stipulates rather than
measures.

The study places **one** answer-bearing document among distractors, at controlled positions,
in a controlled multi-document QA setup, with particular models and prompts, at particular
context lengths.

Your setting differs in at least four ways:

- **Your answer may be in several chunks**, or in none
- **Your prompt is not theirs**, and prompt structure interacts with position
- **Your window is shorter** than the long-context regime where the effect was largest
- **Your model is not one they tested**, and the effect varies by model — including by
  model *version*, which changes under you

None of that makes the finding wrong. It makes the size of the effect **in your system**
unknown, and it is the size that decides whether reordering is worth anything.

---

## What the lab does instead

Builds a **stipulated model**: a parabola, 1.0 at both ends, `dip` in the middle.

Its *shape* is from the literature. Its *numbers* are invented. Nothing in this course can
check them, because checking requires a generator and week 8 is where the generator arrives.

So the lab uses it for exactly one thing: **comparing orderings**. Under the stipulated
model, ends-first > rank order > document order — and the last test confirms that ranking
survives changing `dip` across its range, which is the property that makes the comparison
usable while the values remain meaningless.

The report may say *"ends-first ranks above rank order under a stipulated U-shaped
weighting"*. It may not say by how much.

---

## What is measured

One thing today is real: **where the answer-bearing chunk actually lands.**

On this corpus, in rank order, the first answer-bearing chunk sits about a **third** of the
way into the window — which is the region the stipulated model penalises most, and is why
the question is worth asking at all.

That number needs no model. It is a property of your retriever and your budget, you can
compute it now, and it is the input to any decision about ordering.

---

## Document order, and what it is for

The third ordering is not a positional strategy at all.

Grouping by parent document and sorting by chunk index restores **reading order**: two
consecutive sections of one RFC read as an argument, where the same two interleaved with a
third document read as three fragments.

Under the stipulated model it scores worst, because it ignores rank entirely. It may still
be right — coherence is not something the model represents, and a generator asked to
summarise a procedure may do better with the procedure in order than with its best-scoring
step first.

That is a hypothesis. It is testable in week 8. It is the kind of thing that gets decided by
taste for years because nobody sets up the comparison.

---

> **Known** — model performance on retrieving information from a long context is highest at
> the beginning and end and lowest in the middle, across several models and context lengths
> (`lost-in-the-middle`) · the effect was measured in a controlled multi-document QA setup
> with a single answer-bearing document (`lost-in-the-middle` §4)
> **Inferred** — that the effect's *size* in a given RAG system is unknown without measuring
> it there, because the setting differs in prompt, window length, model and answer
> multiplicity. Ours, and it is the reason for the stipulation
> **Derived** — an ordering comparison whose result is invariant to the stipulated
> parameter depends on the model's shape rather than its values
> **Unknown** — the position effect for the models, prompts and window sizes anyone reading
> this actually uses. It is measurable per system in an afternoon from week 8 onward
