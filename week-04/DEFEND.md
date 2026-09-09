# Week 4 — Friday clinic

Twenty minutes, three phases, then a retro.

Week 3 asked whether they could be trusted with a number that went up. **This week asks
whether they can present a decision that has two axes**, and whether they noticed that
their instrument was wrong for three weeks.

---

## Before they arrive

Read `REPORT.md`, `my-queries.yml`, and the run ledger. Check five things:

1. **Are there answer spans, and are they minimal?** A span covering a whole paragraph is
   nearly impossible for a boundary to destroy, so their chunking looks robust and is not.
   This is the most common way to get a clean-looking week-4 report that means nothing.
2. **Was the target stated before the selection?** If the target is exactly met by the
   chosen configuration and by nothing cheaper, ask when they wrote it down.
3. **Is the frontier in the report, with dominated points visible?** Winner-only is the
   failure this week is built to prevent.
4. **Does the report claim chunking improved retrieval?** It did not.
5. **Did they settle week 2's cleaning question?** They have carried it for two weeks.

---

## Phase 1 — Explain (6 min)

1. *"Whole documents get every answer into the top 3. So what is chunking for?"* **The
   question of the week.** A student who says "precision" or "relevance" has not internalised
   their own table. The answer is cost.
2. *"Read me your two smallest answer spans. Why those words and not more?"* Looking for a
   judgment they can defend, not a rule they followed.
3. *"At 200 words with no overlap, one query's answer left the corpus. Which stage could
   have recovered it?"* None. Press until they say none.
4. *"Your document-level metric said the overlap that rescued that answer was a regression.
   Why?"* Wrong granularity, and the destroyed query was in the held-out split. Both.
5. *"What is your target coverage, and what happens when it is missed?"*

| 5 | 3 | 1 |
|---|---|---|
| Says "cost" immediately and has the ratio to hand; defends a span choice | Gets there with prompting | Describes chunking as a retrieval improvement |

## Phase 2 — Change something (7 min)

### A — *"Your corpus is now support tickets. No headings, no sections, no numbering."*

The best mutation this week. Their entire day-3 result rests on a regex that works on RFCs.
Looking for: the *method* transfers and the implementation does not; what would play the
role of a heading in a ticket (a blank line, a quoted reply, a timestamp); and — the strong
answer — that they would run the span audit first and find out empirically rather than
guessing.

### B — *"Halve your context budget."*

Looking for: they go back to the frontier rather than re-tuning. The frontier already
contains the answer, which is the point of having built one. A student who starts changing
chunk sizes has not understood what they produced.

### C — *"Your queries get twice as long and much more specific."*

Longer queries match more chunks, and a small chunk containing three of eight query terms
now scores where it did not. Looking for: the frontier is a function of the query
distribution, so it is not a property of the corpus and would have to be remeasured.

| 5 | 3 | 1 |
|---|---|---|
| Separates method from implementation; returns to the frontier rather than the knobs | Gets there messily | Proposes a new chunk size |

## Phase 3 — Break it (7 min)

| Attack | What you are watching for |
|---|---|
| *"Show me a span where a slightly longer version would have changed your result."* | Whether they know their instrument is a set of judgment calls. There is always one |
| *"`fixed 400` is what the internet recommends and it is dominated at every k. Where did that number come from?"* | A default in an example notebook. Looking for: they can say there is no primary source, and they are not smug about it — their own number is corpus-specific too |
| *"You picked target 1.0. What would you have picked if your users were doctors? If it was a shopping site?"* | Whether the requirement is a real requirement or a round number |
| *"Your answer recall is 1.0 on nine queries. How confident are you?"* | Week 3's floor arithmetic. A binary metric at n=9 is coarse, and 1.0 means "no failures observed" rather than "no failures" |
| *"Chunking made retrieval worse on three configurations. Would you have found that if you had only measured nDCG?"* | The week's thesis, from the other end |

| 5 | 3 | 1 |
|---|---|---|
| Names a span whose length changes the answer; treats 1.0 as "unobserved" | Finds it with prompting | Defends the configuration as optimal |

**Pass is 3 in every phase.**

---

## Retro (15 min)

1. *"On Thursday morning you wrote one sentence on what chunking is for. What did you
   write?"* Almost everyone writes something about precision.
2. *"Which station did you skip?"* Usually **1** — a fourth consecutive week where the
   corpus went quiet once something else got interesting. Point out that it is now a
   pattern rather than an accident.
3. *"You changed the ground truth this week. What did that invalidate?"* The most important
   question in the retro and the one they will most want to answer briefly.
4. *"What is going in the failure library?"*
5. *"What did I explain badly?"*

---

## Instructor: what next week rests on

Week 5 is embeddings — the first week with a model in it, and the week students have been
waiting four weeks for.

Three things carry forward:

- **The answer-span metric.** Week 5 compares dense against BM25, and it must be compared
  on answer recall and cost, not on nDCG. If their spans are sloppy, week 5's comparison is
  sloppy and its conclusion — that dense retrieval *loses* on several queries — will look
  like a bug in their embedding code
- **The chunk configuration.** Week 5 embeds their chunks. A student still on whole
  documents will embed 19,000-word documents into a single vector and get nonsense, which is
  a real lesson but not the one week 5 is teaching. Make sure everyone leaves with a chosen
  configuration
- **`r02` and `r06`.** Still broken after four weeks, still the vocabulary gap, and week 5
  is the first plausible fix. Remind them on Friday that they identified these in week 3 and
  have been carrying them since

The thing to watch for: **the student who expects embeddings to fix everything.** Week 5 is
built so that dense retrieval loses at least one query BM25 gets right, and a student
arriving with high expectations reads that as their own failure. Set expectations on Friday:
week 5 is not an upgrade, it is a different set of strengths.
