# Day 3 — The clinics

> **By the end of today** you can attribute a failure to one station in under a minute,
> name the diagnostic, and say what you would not do.

**No lab.** Ten scenarios, five minutes each, in pairs. Then swap and run them again.

---

## Read first

- [ ] [**Under a minute**](../../content/week-12/day-3/under-a-minute.md) — 25 min
- [ ] [**What you would not do**](../../content/week-12/day-3/what-you-would-not-do.md) — 20 min

---

## How to run it

In pairs. One reads the scenario aloud, the other answers three things and is timed:

> **which station · what diagnostic finds it · what you would not do**

Then swap. Then do it again with the pairs rotated, because the second pass is where the
reasoning gets fast enough to be useful.

**Score the third answer hardest.** Naming the station is the mechanical part. Declining to
reach for the prompt, the chunker or a better model is where eleven weeks either took or did
not.

---

## The ten

They are not in order of difficulty and the station is not always the obvious one. Three of
them are station 7, which is the point.

**1.** *"Faithfulness is 1.00 across the board and users keep telling us the answers are
wrong."*

**2.** *"The system answered a policy question by citing a document that says the opposite
of our current policy. The citation is correct — the document really does say that."*

**3.** *"Recall@10 is 0.98. The answers are bad."*

**4.** *"We raised the retrieved-context budget last quarter. The bill went up 58% and
nothing on the dashboard moved."*

**5.** *"The new reranker improved nDCG@5 by 0.04 on our 19-query evaluation set. Ship
it?"*

**6.** *"Our LLM judge agrees with human raters 70% of the time. That seems good enough to
gate releases on."*

**7.** *"A query that worked last Tuesday now returns nothing relevant. Nobody deployed
anything."*

**8.** *"A user reported a bad answer four hours ago. We cannot reproduce it — the same query
gives a good answer now. Cache hit rate is 30%."*

**9.** *"Our agent scores higher than the single-shot pipeline on our benchmark and users say
it is worse."*

**10.** *"Dashboard says answers are 40% longer and carry twice as many citations as last
quarter. Quality is clearly up."*

---

## The written exercise

`week-12/day-3/clinics.md`.

1. Your ten answers, three lines each, written **before** you discuss them
2. The ones you got wrong, and what you reached for instead
3. **Which station did you over-use?** Everybody has one. Most people over-use 4
4. The scenario you would add as an eleventh, drawn from your own corpus, with its answer

---

## Deep track

> Write five more scenarios from your own system, exchange them with somebody else's five,
> and score each other blind. A scenario whose station the author and the reader disagree
> about is either badly written or a genuinely ambiguous failure — and telling those two
> apart is the most advanced thing in this course.

---

## Log

`logs/stuck-log.md` and `logs/signal-log.md`.
