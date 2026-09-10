# Week 8 — Friday clinic

**Thirty minutes**, not twenty — this is Project 2. Three phases and a retro.

Week 7 asked whether they could leave techniques switched off. **This week asks whether they
read the answers.**

---

## Before they arrive

1. **Are the six wrong answers pasted in full?** Not summarised. If they are not there, the
   milestone was not done, and everything else in the report is a number without a referent.
2. **Do faithfulness and `confidently_wrong` appear together, near the top?**
3. **Is there a quality score anywhere?** There is no way to compute one this week.
4. **Did they blame the model for the five bad citations?**
5. **Is `overlaps` reported with the refusal threshold?**

---

## Phase 1 — Explain (8 min)

1. *"Read me the answer to `r19`."* Then: *"is it wrong?"* — and it is, entirely, and it
   reads perfectly. **The question of the week.**
2. *"Your faithfulness is 1.00 and six answers are wrong. Explain."* Looking for:
   faithfulness relates the answer to the context; correctness relates it to the world. If
   they say the metric is broken, they have missed it.
3. *"Your checker reported five fabricated citations. Which five?"* `[RFC3629]` and friends,
   out of the corpus. Press until they say the bug was theirs.
4. *"What does `r05` say, and what year was it withdrawn?"* 2017. Then: *"which week found
   that?"* Week 2.
5. *"Which of your metrics could you compute in production?"*

| 5 | 3 | 1 |
|---|---|---|
| Separates faithfulness from correctness unprompted; owns the checker bug | Gets there with prompting | Reports faithfulness as evidence of quality |

## Phase 2 — Change something (8 min)

### A — *"Your corpus doubles and half of it is out of date."*

The best mutation. Looking for: `citing_superseded` is the only check that would move, it
needs week 2's graph, and nothing in the faithfulness machinery would notice. A strong answer
says the currency check must be built at ingest and cannot be retrofitted at generation.

### B — *"Legal says a wrong answer is a hundred times worse than no answer."*

Straight to the frontier. Looking for: they move the threshold to 0.8, lose six correct
answers, and **say so** rather than presenting it as free. And that the overlap means they
cannot have both.

### C — *"Your generator starts paraphrasing instead of quoting."*

Faithfulness collapses — because the support check rewards copying. Looking for: they know
the metric would report a regression that is not one, and that this is why it is a proxy.

| 5 | 3 | 1 |
|---|---|---|
| Sees that the currency check is an ingest-time obligation; prices refusal honestly | Gets there messily | Proposes prompt changes for a station-1 problem |

## Phase 3 — Break it (9 min)

| Attack | What you are watching for |
|---|---|
| *"Show me the tell that distinguishes a wrong answer from a right one."* | There is none. If they claim one, take a wrong answer and a right one and ask them to sort blind |
| *"Your system refuses nothing. Is that a bug?"* | It is a missing design decision, not a bug, and it is the default everywhere |
| *"You chose threshold 0.55. Who should have chosen it?"* | Not them. Looking for a role and what that person would need to know |
| *"`grounded_rate` is identical for your good system and your broken one. What is it measuring?"* | Retrieval. It is blind to every generation fault, which is correct and dangerous |
| *"What in this report would still be computable if I took away your answer spans?"* | Very little. This is week 9's opening |

| 5 | 3 | 1 |
|---|---|---|
| Concedes there is no tell; names who owns the refusal decision | Finds it with prompting | Defends answer quality from the faithfulness score |

**Pass is 3 in every phase.**

---

## Retro (15 min)

1. *"How long did it take to read the six wrong answers, and what did it change?"* If the
   answer is "nothing", ask which one they read most carefully.
2. *"On Monday you predicted how many the system would refuse."* Everyone says some. It is
   zero.
3. *"Which station did you skip?"* Usually **1** — and week 2's graph was the thing that
   would have caught `r05`.
4. *"Three cards for the failure library. Which is about a check rather than the system?"*
5. *"What did I explain badly?"*

---

## Instructor: what week 9 rests on

Week 9 is evaluation at depth: LLM-as-judge, sample size, and regression gates.

- **The list of metrics that need answer spans is week 9's motivation.** Nearly everything
  this week computed is unavailable in production, and a judge is the standard answer. Make
  sure that list exists in every report
- **Week 7's stipulated-model discipline is the defence.** A judge produces numbers with a
  model's authority attached, and week 7 taught exactly what to do about numbers you cannot
  check. Refer back explicitly
- **`confidently_wrong` is the ground truth week 9 measures a judge against.** They will need
  it, so it must be right

Signal sheet: **did they paste the answers**, and **did they report a quality score**. The
second predicts precisely how they will treat a judge's output next week.

---

## Things that went wrong the first time this week was taught

- **Nobody reads the answers.** The single most common failure of the milestone, and the
  most costly. Check before the clinic, not during it
- **"The generator is fake so none of this counts."** It is stipulated and the *machinery* is
  what transfers. Have the week-7 parallel ready
- **Somebody fixes `r05` with a prompt instruction.** It cannot work: the fact that makes the
  answer wrong is not in the context. Walk the stations with them
