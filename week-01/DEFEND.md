# Week 1 — Friday clinic

Twenty minutes on the milestone, in three phases, then a retro. The student has their
`REPORT.md` and `my-queries.yml` open; you have this page.

The bar this week is deliberately low on retrieval sophistication and high on honesty. You
are finding out whether they wrote their judgments or borrowed them, and whether they know
what their own numbers do not cover.

---

## Before they arrive

Read `my-queries.yml`, `REPORT.md`, and `runs/`. Pick, in advance:

- **one query to make them re-judge live** — choose one where the shipped set and their
  set disagree, or where their grades look mechanical
- **the mutation** for phase 2
- **the two weakest claims** for phase 3

Also check three things that are faster to check than to ask about:

1. **Is there an out-of-scope query?** The brief requires one. If it is missing, that is
   the first question, and the answer is usually "it made my numbers worse".
2. **How many `test` runs are in `runs/` for this week?** `tools/check_evals.py` catches
   more than one cited. It does not catch one cited and four taken. The log does.
3. **Do the judgment grades have a suspicious shape?** All 3s and 0s with no 1s or 2s
   means they judged binary and filled in grades afterwards, which is worth knowing on day
   five rather than in week 7 when nDCG starts mattering.

---

## Phase 1 — Explain (6 min)

1. *"Read me query 4. What would a complete answer to it contain?"* — then: *"now show me
   what you graded 2 and what you graded 1, and tell me the difference."* **This is the
   question of the week.** A student who cannot state the 1/2 line in their own words did
   not write these judgments in the sense that matters.
2. *"Where did recall@10 of [their number] come from? Which split, how many queries?"* —
   make them rebuild it out loud.
3. *"Your kappa is [N]. What does that mean for a 3-point improvement in week 6?"* —
   looking for: *it would be inside my own noise*. Most will not have connected these.
4. *"Which of your twelve queries could your baseline never answer, no matter how good the
   scoring got?"* — the vocabulary-gap one and the out-of-scope one. If they say "none",
   they have not read their own `explain()` output.
5. *"What is in the corpus that no query of yours touches?"*

| 5 | 3 | 1 |
|---|---|---|
| States the 1/2 line unprompted; connects kappa to what a result must exceed | Describes the set accurately; needs a nudge on the noise floor | Cannot say why any particular grade is what it is |

## Phase 2 — Change something (7 min)

Pick **one**. Ask what parts of the report stop being true *before* they say what they
would do.

### A — *"Your eval set was written by the same person who will build the retriever. Convince me the week 6 result will mean anything."*

The best mutation this week, and there is no clean answer — which is the lesson. Looking
for: they name the bias, they point at their own `unjudged_in_top_k` audit as the partial
defence, and they do not pretend it is solved. A student who says "I was careful" has not
understood the problem. A student who says "it is not solved, here is what I can measure
about it" has.

### B — *"The corpus grows to 30,000 documents. What happens to every number in this report?"*

Looking for: recall@10 collapses, because top-10 stops being a third of the corpus.
Coverage becomes a rounding error. Their judgments become a vanishingly thin sample. The
strong answer notices that **their metrics do not get worse — their metrics stop being
measurements**, which is different and worse.

### C — *"Half your users start asking three-word queries."*

Looking for: they check what their scorer does when the query has three terms, two of
which are stopwords. Coverage-based scoring becomes almost binary. They should be able to
predict this from `overlap.py` without running it.

| 5 | 3 | 1 |
|---|---|---|
| Names the affected sections before designing; reasons from their own numbers | Gets there messily | Starts proposing retrieval improvements immediately |

## Phase 3 — Break it (7 min)

Two attacks, pressed until they defend or concede. Do not accept *"I would look at more
data"* as an answer to anything.

| Attack | What you are watching for |
|---|---|
| *"Ask your baseline your out-of-scope query. What comes back?"* | Something comes back, scoring above zero, looking like an answer. Do they know that this is the shape of every hallucination they will see in week 8? |
| *"Your recall@10 is [N]. Show me a query in the missing part and tell me why."* | Whether they have looked at their own failures individually or only in aggregate |
| *"How many times did you actually look at `test`?"* | Honesty. Ask it plainly and without menace. The answer is often "twice" and the correct response is to thank them |
| *"Take your best query and make it worse by one word. What happens to the ranking?"* | Whether they understand their scorer mechanically or only statistically |
| *"You judged four documents for this query. Which of the other twenty-six would you have graded 2 if you had looked?"* | The pooling bias, live. A good student will find one in thirty seconds |

| 5 | 3 | 1 |
|---|---|---|
| Reasons from their own numbers; concedes cleanly where the answer is "I cannot tell" | Finds it with prompting | Answers every attack by proposing a better retriever |

**Pass is 3 in every phase.**

---

## Retro (15 min)

1. *"Which station did you skip?"* — this week it is almost always **1**. Everybody
   measures and nobody looks at the corpus. Naming it now is what stops it happening in
   week 2, where it is the whole week.
2. *"What did you write down that you could not defend just now?"*
3. *"You predicted a self-agreement number on Tuesday. What was it, and what did you get?"*
   — the sealed prediction. Most write 95 and get high 70s. Ask what it felt like.
4. *"What did I explain badly?"*

---

## Instructor: what next week rests on

Week 2 is the corpus — extraction, boilerplate, near-duplicates, provenance — and its
milestone is an ingest with a **loss report**. It only works if the student genuinely
believes that a retrieval failure can originate before retrieval.

The specific thing to check: **did they ever open a document?** A student who built an
eval set entirely from query text and document titles, without reading the corpus, will
sail through week 1 and be lost in week 2, because week 2's entire premise is that the
text you think you have is not the text you have. Phase 1 question 5 catches this. If it
went badly, spend Monday's live hour reading `mrta-014`'s flattened table together and
nothing else.

The other signal: **a student whose kappa is suspiciously high.** 0.95 self-agreement over
40 judgments usually means they re-judged with the first set open, or they only re-judged
the easy ones. Ask how they did it. It is nearly always innocent and it always matters.
