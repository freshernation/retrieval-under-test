# What you would not do

*Week 12 · Day 3 · about 20 minutes*

> By the end of this you can read three of the ten clinics properly, and you will see why
> the station is not the hard part.

---

## Sources

| Source | Tier | What it gives you |
|---|---|---|
| [**Zheng et al.**, LLM-as-a-judge](https://arxiv.org/abs/2306.05685) | 1 | Judge agreement rates, for clinic 6 |
| [**RFC 8259**](https://www.rfc-editor.org/rfc/rfc8259.html) | 1 | Obsoletes 7159 and reverses it, for clinic 2 |
| [**Google SRE Book**, ch. 6](https://sre.google/sre-book/monitoring-distributed-systems/) | 1 | Indicator against diagnostic, for clinic 10 |

---

## Three worked clinics

Not the answer key — three of the ten, worked in the form the drill asks for, so the shape
of a good answer is visible. The other seven are yours.

---

### Clinic 1 — *"Faithfulness is 1.00 and users keep telling us the answers are wrong."*

**Station 7.** Measure.

**The diagnostic.** Take the queries users complained about and ask whether the answer spans
were in the retrieved context. That is `grounded_rate`, it needs labels, and it is the
number faithfulness is being mistaken for. Week 8 measured 1.00 faithfulness against 70%
grounded.

**What you would not do.** Tune the faithfulness threshold. It is working correctly —
faithfulness relates the answer to the *context*, and every one of those answers is
supported by what it was given. The complaint is about the world, which faithfulness has
never measured and cannot.

The tell that this is station 7 rather than station 6: **the metric and the users disagree,
and the metric is internally consistent.** A broken metric is noisy; a mis-specified one is
confidently fine.

---

### Clinic 5 — *"The new reranker improved nDCG@5 by 0.04 on our 19-query set. Ship it?"*

**Station 7.** Not station 5, and that is the trap — the reranker is at station 5 and the
failure is not.

**The diagnostic.** The paired standard deviation and the minimum detectable effect.
0.04 against an MDE of 0.1003 at n=19: the result is not distinguishable from zero.

**What you would not do.** Three things. Do not ship it on that number. Do not conclude the
reranker is useless — the set cannot say either way, and *"we measured nothing"* is not
*"there is nothing"*. And do not run the comparison again hoping for a bigger number, which
is a repeated comparison and inflates whatever you eventually report.

What you would do: compute how many queries 0.04 needs — week 9's arithmetic says roughly
120 — and decide whether the reranker is worth that much labelling before doing it.

This clinic is the one students most often get wrong by being too clever: they diagnose the
reranker. The question was whether to ship, and the answer is about the instrument.

---

### Clinic 10 — *"Answers are 40% longer and carry twice as many citations. Quality is up."*

**Station 7**, again, and the third one in the set.

**The diagnostic.** The AUC of each dashboard signal against something you have labels for.
Week 9 measured answer length at 0.45 and citation count at 0.46 — both chance.

**What you would not do.** Celebrate, obviously. But more importantly: do not *remove* those
metrics. They are fine diagnostics — *"answers suddenly got 40% longer"* is a real signal
that something changed — and terrible indicators. The failure is putting them in the wrong
column, where a change in them triggers belief.

And the thing to check next, which is the part that makes this clinic worth five minutes:
week 8 measured that padding **raises** a word-overlap faithfulness score. So a verbose
system moves three dashboard metrics in the right direction while answering no more
questions, and week 10 found a budget setting that does exactly that for 58% more money.

---

## The pattern across all three

Each one is station 7, and in each one the station is obvious the moment you ask *"does the
number mean what the sentence assumes it means?"*

That question is the whole of station 7, and it is the station eleven weeks of this course
were about. The other six stations are a pipeline. Station 7 is whether you can read your
own instruments — and the reason three of ten clinics live there is that in real work, the
proportion is higher.

---

> **Known** — model judges agree with human raters at rates that must be reported against a
> baseline (`zheng-2023`) · RFC 8259 obsoletes RFC 7159 and reverses its UTF-8 guidance
> (`rfc-8259`) · an indicator triggers work while a diagnostic explains it (`sre-book`)
> **Inferred** — that a mis-specified metric presents as confidently fine while a broken one
> presents as noisy, so internal consistency alongside user disagreement is the tell for a
> station 7 failure. Ours
> **Inferred** — that *we measured nothing* and *there is nothing* are different conclusions,
> and conflating them is how a usable technique gets abandoned on an under-powered set. Ours
> **Derived** — 0.04 against a minimum detectable effect of 0.1003 at n=19 is not
> distinguishable from zero, and detecting it would require roughly 120 queries · a verbose
> system moves answer length, citation count and word-overlap faithfulness favourably while
> answering no more questions
> **Unknown** — the real proportion of production retrieval complaints that are station 7
> failures. Higher than three in ten, on everything we have seen, and that is not a sample
