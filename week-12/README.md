# Week 12 — The report and the review

> **Destination**
> Write the evaluation a stakeholder acts on, edit thirty failure cards down to the ones
> that transfer, survive ten timed clinics, and say which of your findings expire.

**There is no `pytest` in this week.** That is deliberate and it is the point: everything
here is work a machine cannot check, which is why it is last and why eleven weeks of
machine-checked work came first.

---

## The week

| Day | Folder | What you'll be able to do |
|---|---|---|
| Mon | `day-1/` | Write a report whose first line is a blocker |
| Tue | `day-2/` | Edit a failure library down to the cards that transfer |
| Wed | `day-3/` | Attribute ten failures to one station each, under time |
| Thu | `day-4/` | Say which of your findings expire, and when |
| Fri | `milestone/` | The final report, the library, and the clinic scores |

---

## What the course measured

Eleven weeks of numbers, and the ones worth carrying out are mostly the negative ones.

| Week | The finding | Why it transfers |
|---|---|---|
| 1 | recall@10 is ~1.0 on ten documents | a metric without its N is not a number |
| 2 | RFC 7159 does not know it is obsolete | the fact that makes an answer wrong lives elsewhere |
| 3 | BM25's `k1=1.2` ranked 38th of 45 | a shipped default is a hypothesis |
| 4 | chunk size 400 dominated at every k, with no literature behind it | the most consequential decision has no science |
| 5 | dense retrieval loses on identifiers | an exact token match is information a smoothed representation drops |
| 6 | RRF's `c=60` captured **0%** of the headroom | second default to fail, and the pattern is named |
| 7 | the best blend weight was the identity | three negative results and one frontier |
| 8 | faithfulness **1.00** with 30% of answers confidently wrong | faithfulness relates the answer to the context, not to the world |
| 9 | judge accuracy 0.70, kappa **0.000** | a judge number without its baseline is not a number |
| 10 | nothing failed at station 6 | the prompt is where the work goes and not where the failures are |
| 11 | the agentic win was a metadata join | which edge am I following, and is it already a field |

Three defaults failed. Three weeks ended on a refusal. One thing has been unmeasurable
since week 1 and still is: **correctness**.

---

## The three rules, eleven weeks on

**1. No change without a measured delta.** Week 9 then showed that most of the course's
deltas were inside the minimum detectable effect of the sets they were measured on. The
rule survives that — it is the reason the audit was possible at all.

**2. Retrieval before generation.** Week 10's attribution report is the vindication: zero
failures at station 6, five of six in the candidate set.

**3. A system nobody has attacked is a demo.** Eleven Friday clinics. This week is ten more
in two hours.

---

## Milestone

The final report, the edited failure library, ten scored clinics, and an expiry date on
every claim. Spec in `milestone/README.md`.
