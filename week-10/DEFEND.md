# Week 10 — Friday clinic

Twenty minutes, three phases, then a retro.

Week 9 asked whether they can say what they do not know. **This week asks whether they can
tell packaging from improvement** — and resist a week of visible, satisfying work that
moved no number that matters.

---

## Before they arrive

1. **Is the latency figure a count or a clock?** A reported millisecond is a reported
   laptop.
2. **Is the tail next to the middle?** One percentile is a lie of omission.
3. **Does the cache appear in the config?** It changes what the system says.
4. **Which traffic distribution did the hit rate assume?** If the report does not say,
   the hit rate is not a number.
5. **Does the trace record ids?** If not, the attribution section was written by hand and
   will not survive an incident.
6. **Is there a price anywhere in a result?** The fence forbids it.
7. **Does `ship_check` still refuse?** It should. If it does not, ask what changed.

---

## Phase 1 — Explain (6 min)

1. *"Your p95 work is 829. How many requests is that?"* **The question of the week.**
   One. It is the nineteenth of twenty, and p99 is the twentieth at 1,075.
2. *"Your cache hit rate is 0.30. Where did that come from?"* A skew parameter. Press
   until they name it.
3. *"Nothing failed at station 6. What were you planning to work on next?"* Watch the
   answer.
4. *"The 1,200-word budget costs 58% more. What does it buy?"* Nothing. Then: *"so why was
   it on?"*
5. *"What did this week improve?"* The honest answer is *nothing*, and saying it is a pass.

| 5 | 3 | 1 |
|---|---|---|
| Says a p95 on twenty samples is one request; names packaging as packaging | Gets there with prompting | Reports a millisecond figure as a property of the system |

## Phase 2 — Change something (7 min)

### A — *"Traffic turns out to be uniform, not concentrated."*

Looking for: the hit rate falls from 0.79 to 0.19 at capacity five, so the cache's
justification evaporates and the capacity decision has to be remade. A strong answer says
the measurement was never of the system — it was of an assumption — and proposes logging
the real distinct-query rate, which costs one counter.

### B — *"You get a real model, and it is 400ms."*

Looking for: generation becomes the critical path, every stage budget is now wrong, and the
work counts are unaffected — which is the argument for having counted work. A student who
re-times everything in milliseconds and reports the new numbers has missed the week.

### C — *"Legal asks you to drop the chunk ids from the logs."*

Looking for: attribution dies. The durations survive and they can only find slow stages,
never wrong ones. A strong answer offers hashed ids, or ids retained for a short window,
rather than conceding the field — and says plainly what is lost if it goes.

| 5 | 3 | 1 |
|---|---|---|
| Separates what the change invalidates from what it does not; defends the ids concretely | Gets there messily | Re-measures everything and reports it |

## Phase 3 — Break it (7 min)

| Attack | What you are watching for |
|---|---|
| *"Your service meets every SLO. Ship it."* | It refuses, on six failures. The whole week in one answer |
| *"Show me a cached answer and tell me how old it is."* | `r05`, grounded in a withdrawn RFC, and nothing in the system minds |
| *"Your staleness check scores 0.83. Is that good?"* | The missing 17% is the answer. An aggregate over a context cannot see which member mattered |
| *"Turn the cache on and tell me which of your week-8 numbers are still valid."* | None of them, until re-run. A cached run is a different system |
| *"You have spent a week on latency. Name the latency number a user would notice."* | None measured. Work counts are not user-visible time, and saying so is the point |

| 5 | 3 | 1 |
|---|---|---|
| Defends the refusal; concedes that work counts are not user-visible latency | Finds it with prompting | Ships, or claims the week improved the system |

**Pass is 3 in every phase.**

---

## Retro (15 min)

1. *"What did you expect the attribution report to say, and what did it say?"* Most expect
   station 6.
2. *"Which of your settings was pure waste?"* Everyone has one, and most have the 1,200.
3. *"Which station did you skip?"* This week it is often **1** — provenance feels finished
   and the cache is the thing that makes it un-finish.
4. *"What is going in the failure library?"* The cached withdrawn RFC, at minimum.
5. *"What did I explain badly?"*

---

## Instructor: what week 11 rests on

Week 11 is agentic retrieval, and it is Project 3.

- **The attribution report is the target list.** Five of six failures are the candidate set —
  two queries nothing retrieves, three the budget drops. That is exactly what rewriting,
  routing and multi-hop claim to fix, so next week has a measured goal rather than a
  fashion
- **Cost is now a measured quantity**, which is the only reason an agent can be evaluated
  honestly: a loop that runs four retrievals costs four times as much, and week 10 is where
  that stopped being free
- **Week 9's proxies are the routing signal.** Retrieval confidence at AUC 0.83 is what a
  router would branch on, and they have had it for a week

Signal sheet: **count or clock**, and **did `ship_check` still refuse**. The first predicts
whether their performance numbers will mean anything to anyone else; the second predicts
whether they can tell work from progress.

---

## Things that went wrong the first time this week was taught

- **The week feels like the best one.** Services, caches, traces, dashboards — it is
  satisfying, visible work and it improved nothing. Say so on Monday and again on Friday
- **Somebody reports milliseconds.** They always do. The fix is to ask them to compare
  against the person next to them
- **The cache gets switched on and left on**, and then week 8's numbers are quietly wrong.
  The config hash test exists because of this
- **The attribution result lands as a letdown** — *"so the model was fine all along"*. It is
  the opposite of a letdown; it is five weeks of prompt work that nobody will now do
