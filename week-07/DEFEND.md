# Week 7 — Friday clinic

Twenty minutes, three phases, then a retro.

Week 6 asked whether they could decline to ship something they built. **This week asks
whether they can leave three techniques switched off** — and whether they can tell "did not
help" from "could not be measured", which is the harder distinction.

---

## Before they arrive

1. **Is the ceiling in the report, before the reranking section?** If reranking is discussed
   before the ceiling is computed, the week was done backwards.
2. **Is any stage enabled without a comparison against not having it?**
3. **Does a stipulated score appear anywhere?** Grep the report for a number from
   `expected_use`. It is forbidden and it is tempting.
4. **Did they distinguish "MMR did not help" from "we cannot measure diversity"?**
5. **Is the budget chosen with a requirement, or by eye?**

---

## Phase 1 — Explain (6 min)

1. *"What is the most a reranker could have bought you, and how do you know before building
   one?"* The ceiling, three lines, computed first. **The question of the week.**
2. *"Your best alpha was 1.0. What is alpha 1.0?"* The identity. Press until they say the
   reranker's best setting was not to rerank.
3. *"Why did it lose?"* Looking for: three hand-picked features are a worse model of
   relevance than BM25 plus RRF. Not "my code was wrong".
4. *"Answer recall is identical for every MMR setting. Does MMR do nothing?"* No — the metric
   cannot see it. This distinction is the phase's real content.
5. *"What is your density at your chosen budget?"*

| 5 | 3 | 1 |
|---|---|---|
| Computes the ceiling first; separates "did not help" from "unmeasurable" | Gets there with prompting | Reports a reranking improvement, or calls MMR useless |

## Phase 2 — Change something (7 min)

### A — *"Your budget halves."*

Back to the frontier, not to the knobs. Looking for: truncation becomes much more attractive
at a tight budget (0.263 → 0.474 at 200 words), and they know that because they measured it
rather than because it sounds right.

### B — *"Your chunks are now 800 words each."*

Everything shifts. A 800-word budget is one chunk, so ordering is meaningless, MMR has
nothing to diversify, and density is entirely determined by whether that one chunk carries
the span. Looking for: **the assembly stage's options are a function of the chunk size**, a
decision made three weeks ago.

### C — *"You get a cross-encoder."*

Looking for: the ceiling does not move — reordering still cannot introduce a chunk retrieval
missed — so the sixteen points is still the maximum, and the question is whether a trained
model captures what three features did not. A strong answer says they would measure it
exactly the way they measured this one.

| 5 | 3 | 1 |
|---|---|---|
| Returns to the frontier; sees that chunk size determines this week's options | Gets there messily | Proposes tuning MMR |

## Phase 3 — Break it (7 min)

| Attack | What you are watching for |
|---|---|
| *"Read me a number from your positional model."* | They should refuse. If they read one out, that is the finding |
| *"Truncation nearly doubled `answered` at 200 words. Always truncate?"* | No — it can cut a span in half, after retrieval succeeded, invisibly to every retrieval metric |
| *"You have 2.4 documents in five results. Is that bad?"* | Unknown, and honestly unknown. It depends on whether answers need several documents, and their eval set contains one such query, in the held-out split |
| *"Your density is 0.24. Where did the other 76% go?"* | Surrounding text in answer-bearing chunks, plus four chunks that carry nothing. Both are chunk-size consequences |
| *"Which of this week's three techniques would you put in production?"* | Ideally none of them yet, with the measurement that would change each answer |

| 5 | 3 | 1 |
|---|---|---|
| Refuses to quote the stipulated model; can say what would change each decision | Finds it with prompting | Defends a stage because it is standard practice |

**Pass is 3 in every phase.**

---

## Retro (15 min)

1. *"Three negative results in one week. Was it a wasted week?"* No — they now know the
   ceiling, the budget frontier, and which questions their eval set cannot answer. Push
   until somebody says the third one.
2. *"Which station did you skip?"* Usually **7**, and this week that is nearly the point:
   the eval set could not evaluate two of three stages.
3. *"On Monday you predicted what your reranker would gain."*
4. *"What is going in the failure library?"*
5. *"What did I explain badly?"*

---

## Instructor: what week 8 rests on

Week 8 is generation and grounding — **Project 2**, the first week with a model in it, and
the keystone of the course.

- **The assembler is the input.** A student without a working `ContextAssembler` cannot
  start week 8. Check on Friday
- **Density is the hook.** 0.24 at 800 words means three quarters of the context is not
  carrying the answer, and week 8 measures what a generator does with that
- **Position becomes measurable.** Day 4's stipulated model gets checked against a real
  generator in week 8's deep track, and a student who quoted its numbers this week will
  have to retract them, which is a good thing to have arranged
- **`unreachable` still has two queries in it.** Three weeks now. Week 8 will show what a
  generator does when the answer is not in the context, which is the single most important
  behaviour in the course

Signal sheet: **stages enabled without justification**, and **whether they quoted a
stipulated score**. The second predicts how they will treat week 9's LLM-as-judge numbers,
which is exactly the same problem with more authority attached.
