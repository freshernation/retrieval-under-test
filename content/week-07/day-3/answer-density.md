# Answer density

*Week 7 · Day 3 · about 20 minutes*

> By the end of this you can say what fraction of your context window is doing any work,
> and why the number gets worse as you spend more.

---

## Sources

| Source | Tier | What it gives you |
|---|---|---|
| [**Liu et al., *Lost in the Middle***](https://arxiv.org/abs/2307.03172) | 1 | Why a mostly-irrelevant window is worse than a small relevant one, not merely dearer |
| [**Rajpurkar et al., *SQuAD***](https://arxiv.org/abs/1606.05250) | 1 | Answer spans, the ground truth this metric is built on |

---

## The number

**Of the words you send, what fraction sits in a chunk carrying an answer span?**

| budget | answered | **density** |
|---|---|---|
| 200 | 0.263 | 0.263 |
| 400 | 0.474 | 0.309 |
| 800 | 0.737 | **0.237** |
| 2000 | 0.789 | **0.098** |

At 800 words — a reasonable choice — three quarters of the context is not carrying the
answer. At 2,000, nine tenths.

This is the first metric in the course that describes **what you are paying for** rather
than whether you succeeded. Every earlier one stopped at "the answer is present".

---

## Why it falls

Mechanically: `answered` saturates and `words` does not. Past the point where the answer is
usually in the window, every extra word is a word that is not carrying the answer, so
density falls monotonically for ever.

Which means **density and coverage are in direct tension**, and there is no budget that
maximises both. Another frontier, and by now the shape should be familiar.

---

## It is a loose upper bound

Be careful with this number, because it flatters you.

A chunk containing the span is counted **whole** — all 250 words of it, including the 240
that are context around a ten-word answer. So the "useful" fraction the metric reports is
much larger than the useful fraction that exists.

The tighter version — words within some distance of the span — is the deep track, and it
gives a smaller and more honest number. Neither is what you actually want, which is *how
much of this did the generator use*, and that needs a generator.

So: **density is an upper bound on usefulness, computed without a model.** Report it as
that. It is genuinely informative — an order-of-magnitude answer to "how much of this is
waste" — and it is not a measurement of value.

---

## Where the waste comes from

Two sources, both decisions you already made:

**Surrounding text in answer-bearing chunks.** Your chunk size. Sections of 100–300 words
around a ten-word span. Smaller chunks raise density and, from week 4, lose answers.

**Chunks carrying nothing.** Your `k`, or now your budget. Four of five chunks typically
carry no span at all.

Neither is fixable at this stage. Density is a **diagnostic that points upstream** — at
station 2 and station 4 — which is the seven stations doing exactly what they are for.

---

## Why it matters beyond money

If context were merely expensive, the answer would be to buy more of it and stop worrying.

It is not merely expensive. A model's use of information in a long context varies with
position, so a 2,000-word window at density 0.098 is not just 2.5× the price of an 800-word
window at 0.237 — it may also produce **worse answers**, because the answer is now buried
among nine times as much unrelated material.

That is week 8's measurement and this is where you should start expecting it. The intuition
"more context is weakly better and just costs more" is the thing to give up, and density is
the number that makes giving it up concrete.

---

> **Known** — a model's use of information in a long context depends on its position
> (`lost-in-the-middle`) · answer spans as verbatim substrings are a standard ground truth
> (`squad-2016`)
> **Inferred** — that density is an upper bound on usefulness rather than a measure of it,
> because an answer-bearing chunk is counted whole. Ours, and the deep track tightens it
> **Derived** — once `answered` saturates, every additional word is non-answer-bearing, so
> density falls monotonically with budget
> **Unknown** — the relationship between density and generated-answer quality. It is exactly
> what week 8 can measure and we would expect it to be strong and non-linear
