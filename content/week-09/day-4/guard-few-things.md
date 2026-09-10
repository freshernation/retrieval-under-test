# Guard few things

*Week 9 · Day 4 · about 20 minutes*

> By the end of this you can say which metrics belong in a gate and which belong in a report,
> and defend the difference with arithmetic.

---

## Sources

| Source | Tier | What it gives you |
|---|---|---|
| [**Google SRE Book**, ch. 6](https://sre.google/sre-book/monitoring-distributed-systems/) | 1 | Few signals, chosen for actionability |
| [**Lin, *The neural hype***](https://sigir.org/wp-content/uploads/2019/01/p040.pdf) | 1 | What repeated comparisons do to a field's conclusions |

---

## The arithmetic

If each guarded metric fires spuriously with probability *p*, and they are roughly
independent, the gate fires on an unchanged system with probability

$$1 - (1 - p)^m$$

| metrics | 5% each |
|---|---|
| 1 | 5% |
| 5 | 23% |
| **10** | **40%** |
| 20 | 64% |

Ten metrics at a 5% individual false-alarm rate blocks **two builds in five** on a system
nobody touched.

This is week 3's multiple-comparisons problem — forty-five grid configurations, two
spuriously good results for free — arriving in CI, where the consequence is not a wrong
conclusion but a muted gate.

---

## Guard versus report

The test is one question: **would you roll back for this?**

| metric | guard | why |
|---|---|---|
| `grounded_rate` | **yes** | retrieval got worse; users get fewer answers |
| `faithfulness` | **yes** | the system started making things up |
| `confidently_wrong` | **yes** | more wrong answers reaching users |
| `unresolvable_citations` | **yes** | citations stopped pointing at anything |
| answer length | no | diagnostic. Interesting when something else fires |
| citation count | no | diagnostic, and AUC 0.46 |
| `distinct_documents` | no | a proxy. Alert on it; do not block a release on it |
| latency | *elsewhere* | real, and it belongs in a different gate with a different owner |

Four guarded. At 5% each that is a 19% compound rate, which is still high — and is why the
tolerances come from the MDE rather than from taste.

**Everything else is reported.** Reporting is not a lesser status: a metric in the report is
read by a person who can weigh it, and a metric in the gate is enforced by a machine that
cannot.

---

## Why faithfulness and grounded_rate must both be guarded

Week 8's pairing, enforced by a machine.

A misattributing generator — every citation attached to a claim it does not support —
produces:

| | plain | misattributing |
|---|---|---|
| grounded_rate | 0.70 | **0.70** |
| faithfulness | 1.00 | **0.09** |

Retrieval is unchanged, so the retrieval metric is unchanged. A gate guarding only
`grounded_rate` passes a system whose citations have become meaningless.

And the mirror: a gate guarding only `faithfulness` passes a system whose retrieval collapsed,
because a generator with nothing useful in its context can still be perfectly faithful to it.

**Neither alone is sufficient, and this is not a hypothetical** — it is the configuration
comparison from week 8's milestone, run through a gate.

---

## What to do about the compound rate

**Fewer metrics.** The main lever. Four rather than ten halves it.

**Tolerances from the MDE**, which lowers *p* itself rather than the count.

**Require two consecutive failures** for anything below a hard blocker. Halves the false-alarm
rate at the cost of one build's delay, and is the standard alerting trick.

**Do not correct the threshold statistically.** A Bonferroni-style correction on four metrics
makes each one so insensitive that real regressions pass, which converts a noisy gate into a
useless one. In a gate, unlike in a paper, the asymmetry favours a few sensitive checks on
things you would genuinely roll back for.

---

## The last word on nine weeks

The gate is where every earlier week arrives. It guards `grounded_rate` because of weeks 1
to 6, `faithfulness` and `confidently_wrong` because of week 8, and its tolerance comes from
week 9. It is fifty lines.

And it cannot check the thing that matters most — whether the answers are **correct** —
because nothing in this course can. Nine weeks of measurement, and correctness is still out
of reach; what you have instead is a system whose *failures you can name*, and a machine that
stops the named ones from shipping.

That is a lot, and it is worth being clear that it is not the same as knowing the system is
good.

---

> **Known** — monitoring guidance recommends few, actionable signals (`sre-book`) · repeated
> comparisons inflate apparent findings (`lin-neural-hype`)
> **Inferred** — that statistical correction is the wrong response to compounding in a gate,
> because insensitivity to real regressions is the worse error there. Ours
> **Derived** — with m independent guarded metrics each firing spuriously with probability p,
> the gate fires on an unchanged system with probability 1 − (1 − p)^m
> **Unknown** — the false-alarm rate of any deployed RAG eval gate. It is measurable in
> minutes and we have never seen it reported
