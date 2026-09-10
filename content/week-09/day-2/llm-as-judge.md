# LLM-as-judge

*Week 9 · Day 2 · about 25 minutes*

> By the end of this you can name the documented biases of a model judge and probe for each
> one in four lines.

---

## Read the primary sources first

| Source | Tier | What it gives you |
|---|---|---|
| [**Zheng et al., *Judging LLM-as-a-Judge***](https://arxiv.org/abs/2306.05685) | 1 | The foundational study: position bias, verbosity bias, self-enhancement, and agreement with humans |
| [**Es et al., *RAGAS***](https://arxiv.org/abs/2309.15217) | 1 | Model-judged faithfulness as shipped in a RAG evaluation framework |
| [**Wang et al., *Large Language Models are not Fair Evaluators***](https://arxiv.org/abs/2305.17926) | 1 | Position bias measured, and how large it is |

---

## Why it exists

Yesterday's audit: correctness, groundedness and answer recall all need ground truth, and a
live system has none. A model that reads the question, the context and the answer, and says
whether the answer is good, would close that gap.

It is a genuinely good idea. Model judges agree with human raters at rates comparable to the
agreement between humans, on the tasks where that has been measured, and they are orders of
magnitude cheaper than people.

They are also **a second system**, with its own accuracy, its own biases, and its own failure
modes — and unlike your retriever, nobody measures them before quoting their output.

---

## The documented biases

**Position bias.** In a pairwise comparison, the order in which candidates are presented
changes the verdict. Measured and substantial. The mitigation — run both orders, discard
disagreements — doubles the bill, which is why it is often skipped.

**Verbosity bias.** Longer answers score higher, independently of content. This one is
particularly awkward for RAG, where "add more context" and "say more" are the easiest changes
to make and both move the score.

**Self-enhancement.** A judge prefers text produced by itself or by models like it. If your
generator and your judge are the same family, your evaluation is partly a measurement of
family resemblance.

**Self-inconsistency.** The same judge, the same input, a different run, a different verdict.

`raglab.judge.SimulatedJudge` has all four, switchable, so you can isolate each — and, like
week 8's generator, it is a **stipulated model**. Its base judgment is word overlap. Its
biases are real; its numbers are not.

---

## The one nobody switches on

Here is the uncomfortable finding from today's lab.

Set every bias flag to **zero**, and the clean judge still scores a padded answer higher than
the short one — 0.86 against 0.71 on identical content.

The bias is **in the metric**, not in a flag. More words means more words overlapping the
context, so any overlap-based judgment rewards verbosity by construction. And that is the
same proxy week 8 used for faithfulness, so **week 8's faithfulness numbers have this in them
too**.

Which generalises past this simulator: a judge's bias is not only what the model does, it is
also what the *scoring rule* does, and the second is easier to overlook because it feels like
arithmetic rather than judgment.

---

## The probes

Each is four lines and each isolates one bias.

**Length probe.** The same claim, padded with repeated content. If the padded version scores
higher, verbosity is contaminating every comparison between a terse system and a wordy one.

**Position probe.** Ask the judge to compare an answer **with itself**. The correct answer is
`tie`, twice. Anything else means position decides something.

**Self-agreement.** Run the judge twice on the same inputs. Report both score drift and label
agreement — a judge can drift a lot in score without crossing the threshold, which is harmless
for a gate and fatal for a trend line.

**Constant baseline.** Tomorrow's article, and the most important of the four.

---

## What a judge is good for

Not nothing — the pessimism here is about *unvalidated* judges.

**Ranking systems** is what they are best at: comparing two configurations on the same
queries, where shared bias partly cancels. **Flagging for review** works well; a judge that
surfaces the worst 5% for a human is cheap and effective. **Absolute scores** is where they
are weakest, and it is what gets reported.

And a judge should be **validated against a labelled set you already have**. You have one —
week 8's `confidently_wrong` is ground truth for "was this answer any good", built by hand,
and it is exactly what tomorrow measures the judge against.

---

> **Known** — model judges exhibit position bias, verbosity bias and self-enhancement, and
> can agree with human raters at rates comparable to human-human agreement on some tasks
> (`zheng-2023`) · position bias is substantial and mitigated by running both orders
> (`wang-2023`) · model-judged faithfulness is shipped in RAG evaluation frameworks
> (`ragas-2023`)
> **Inferred** — that a scoring rule's own bias is easier to overlook than a model's, because
> it presents as arithmetic. Ours, and today's clean-judge length result is the instance
> **Derived** — a word-overlap judgment scores a padded answer above an identical short one,
> since padding adds overlapping words without adding claims
> **Unknown** — how much of a deployed judge's disagreement with humans is bias versus genuine
> difficulty. The published agreement rates do not decompose it
