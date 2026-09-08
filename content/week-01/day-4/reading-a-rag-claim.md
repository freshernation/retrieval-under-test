# Reading a claim about retrieval

*Week 1 · Day 4 · about 25 minutes*

> By the end of this you can read a RAG blog post and say, in under a minute, whether it
> contains a result.

---

## Sources

| Source | Tier | What it gives you |
|---|---|---|
| [**Lin, *The neural hype***](https://sigir.org/wp-content/uploads/2019/01/p040.pdf) | 1 | What happens to a field's published improvements when someone tunes the baselines |
| [**BEIR**](https://arxiv.org/abs/2104.08663) | 1 | The same models ranked across eighteen datasets, disagreeing |
| [**TREC overview papers**](https://trec.nist.gov/pubs.html) | 1 | What a field looks like when it is being careful about comparability |

---

## The nine questions

You will read a great deal about retrieval this year, most of it written by people selling
a component of it. Nine questions, in order of how often the answer is missing:

**1. What was the baseline, and was it tuned?**
"Improved by 40%" over an untuned default is not a result. This is Lin's finding and it is
the single most productive question you can ask.

**2. What corpus, and how big?**
Recall@10 over 30 documents and over three million are written identically. Without corpus
size, a recall figure carries almost no information.

**3. What eval set, and who wrote the judgments?**
If the judgments were written by the people who built the system, or by a model from the
same family as the system, say so. Both are common and neither is usually disclosed.

**4. How many queries?**
Under about 30, most differences are noise. The number is often absent, which is itself
informative.

**5. Was there a confidence interval?**
Almost never. Its absence does not make a result wrong; it makes it unverifiable.

**6. How many things changed at once?**
"We switched embedding model, chunk size and top-k, and recall improved 8 points" tells you
nothing about which of the three did it — including the possibility that two helped and one
hurt.

**7. What got worse?**
Every retrieval change moves some queries down. A write-up that reports only the mean has
either not looked or has looked and not said.

**8. Who is the publisher and what do they sell?**
Not disqualifying. Often they are the only people who have run the experiment at all. But a
reranking benchmark published by a reranking vendor is Tier 1 *and* conflicted, and both
halves belong in your notes.

**9. What date?**
A 2023 embedding comparison is archaeology. Models turn over in months.

---

## Applying it to this course

The rule from `SOURCES.md` is that a course which will not apply its own standard to itself
is not worth much, so:

- **The baseline here is deliberately weak.** Every number you produce this week is against
  a retriever that ignores term rarity. That is stated everywhere it is used, and week 3
  replaces it with a properly tuned lexical baseline for exactly this reason
- **The sample corpus is 30 documents.** Every number from it is a demonstration, not a
  result. When your instructor says "recall went up", ask which corpus
- **The seven stations are ours**, they are Tier 3, and no study supports them
- **The eval sets are written by one person** — the course author for the shipped set, you
  for yours. Single-annotator judgments, which is the weakest kind, and the reason day 2
  makes you measure your own kappa rather than assuming it

---

## The claim you will meet most often

> "We added [technique] and answer quality improved."

Take it apart with the stations. **Answer quality** is station 6, measured how? By reading
some answers — which day 1 established you cannot do, because wrong answers read exactly
like right ones. If there is no eval set, there is no claim, however careful the writing is.

And notice what technique is usually being added: a reranker, a different chunk size, a
better prompt. Stations 5, 2 and 6. Almost never station 1, and almost never station 7 —
which is where the problem usually was.

---

## Where this is now

RAG evaluation is being standardised, mostly by evaluation frameworks rather than by an
academic community, and largely around LLM-as-judge metrics. That work is real and week 9
covers it seriously, including the evidence that model judges have systematic biases —
towards longer answers, towards their own family's outputs, towards fluency.

The state of the field, honestly: **most published RAG improvements are not verifiable from
what is published.** That is not an accusation of bad faith. It is what a young field with
commercial pressure and no shared benchmark looks like, and it will improve. In the
meantime, the person with a hand-built eval set and a tuned baseline is in a very small
minority, and that is worth knowing about your own position.

---

> **Known** — untuned baselines inflated a substantial fraction of published neural IR
> improvements (`lin-neural-hype`) · model rankings vary considerably across retrieval
> datasets, so a single-dataset result generalises poorly (`beir-2021`)
> **Inferred** — that the nine questions are the right nine. It is a checklist assembled
> from the failure modes above, not a validated instrument
> **Derived** — a comparison in which several components changed simultaneously cannot
> attribute the difference to any one of them
> **Unknown** — what fraction of current RAG claims would survive this checklist. We would
> like the number and have not found anyone who has computed it
