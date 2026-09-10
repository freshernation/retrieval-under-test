# The serving-time gap

*Week 9 · Day 1 · about 25 minutes*

> By the end of this you can list what your system cannot know about itself once it is
> running, and you will have found two signals that partly close the gap.

---

## Sources

| Source | Tier | What it gives you |
|---|---|---|
| [**Rajpurkar et al., *SQuAD***](https://arxiv.org/abs/1606.05250) | 1 | Answer spans — the ground truth that stops existing at serving time |
| [**Google SRE Book**, ch. 6](https://sre.google/sre-book/monitoring-distributed-systems/) | 1 | Monitoring as choosing signals you can compute continuously |
| [**Fawcett, *An introduction to ROC analysis***](https://doi.org/10.1016/j.patrec.2005.10.010) | 1 | AUC as threshold-free discrimination, and what it does and does not say |

---

## The audit

Week 8's report card, classified by one question: *could I compute this for a query I have
never seen, right now, with no human involved?*

| metric | serving time? |
|---|---|
| response rate | yes |
| citation validity | yes |
| uncited sentences | yes |
| answer length | yes |
| retrieval confidence | yes |
| **faithfulness** | **yes** |
| grounded rate | **no** |
| confidently wrong | **no** |
| answer recall | **no** |
| correctness | **no** |

Five minutes with a pen, and the list is shorter and more alarming than people expect.

**Faithfulness survives**, because it compares the answer to the context and you have both.
That is the good news and it is why the metric is popular.

**The four that do not survive are the four you most want**: whether the answer was
available, whether the system was confidently wrong, retrieval recall, correctness. All four
need to know what the right answer was, and a live system does not.

---

## Two possible answers

**Find a proxy.** A signal you can compute live that correlates with the thing you cannot
see. Cheap, no new failure modes, and almost nobody looks.

**Ask a model.** Tomorrow, and it brings a whole new system with its own accuracy.

Today first, because it is the one that gets skipped.

---

## AUC, and why not a threshold

The question is *"does this signal predict that outcome"*, and the wrong way to answer it is
to pick a cutoff and measure accuracy — a useful signal can score badly at a cutoff nobody
chose, and then it gets discarded.

AUC asks instead: **what is the probability that a randomly chosen good case scores above a
randomly chosen bad one?** Ties count half. 0.5 is chance, 1.0 is perfect.

And **0.0 is also perfect, inverted** — which is why `separation_strength` exists, and why
reporting the raw number alone throws away every inverse predictor. Inverse predictors are
where the surprises live, because they are the ones nobody thought to try.

---

## What predicts

| signal | AUC | strength | direction |
|---|---|---|---|
| retrieval confidence | 0.83 | **0.83** | higher |
| **distinct documents in context** | **0.17** | **0.83** | **lower** |
| answer length | 0.45 | 0.55 | — |
| citation count | 0.46 | 0.54 | — |

Retrieval confidence works, which is unsurprising: it is week 8's refusal signal doing a
second job.

**Distinct documents is the interesting one.** As strong as confidence, pointing the other
way: when the context is drawn from one document the answer is usually there; when it has
been scraped from three, the retriever was floundering and taking whatever it could find.

It costs one line, needs no ground truth, is available on every request, and nobody
instruments it — because it is not a quality metric, it is a *shape* metric, and dashboards
are built out of quality metrics.

---

## Where a proxy is allowed to be used

Two jobs, and only one of them is safe:

**Alerting and routing** — yes. A drop in mean retrieval confidence is a real signal that
something changed, and it is available in real time. Week 11 routes on signals like these.

**Reporting quality** — no. A proxy correlates with the thing; it is not the thing. An AUC
of 0.83 is a good signal and it is wrong about roughly one pair in six, and a number
reported as quality will be treated as quality.

The honest formulation: **proxies tell you when to look. Ground truth tells you what you
found.** Keep the offline set, run it on a schedule, and use the proxies for the hours in
between.

---

> **Known** — answer-span ground truth requires annotation and is unavailable for unseen
> queries (`squad-2016`) · AUC measures threshold-free discrimination and equals the
> probability that a positive outranks a negative (`fawcett-2006`) · production monitoring
> selects signals computable continuously (`sre-book`)
> **Inferred** — that proxies are safe for alerting and unsafe for reporting quality. Ours,
> following from correlation not being identity
> **Derived** — a signal with AUC below 0.5 is predictive when inverted, so max(auc, 1−auc)
> is the informative quantity
> **Unknown** — whether distinct-documents-in-context predicts as well on a large corpus. It
> is one line to check and we have never seen it reported
