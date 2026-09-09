# Week 6 — Friday clinic

Twenty minutes, three phases, then a retro.

Week 5 asked whether they could decline to declare a winner. **This week asks whether they
can decline to ship something they built.**

---

## Before they arrive

1. **Did they run `ship_check` at every k, and obey it?** A report that ships at k=5 has
   failed the week.
2. **Is the c sweep in the report?** Or just the chosen value.
3. **Is `unreachable` named?** The paraphrase queries are the week's real finding and they
   are easy to skip past.
4. **Did they compare fusion against both inputs, or against dense?**
5. **Is there an invalidation paragraph** about the query set changing?

---

## Phase 1 — Explain (6 min)

1. *"Adding the two scores gave a ranking identical to BM25 alone. Why identical rather
   than merely similar?"* **The question of the week.** Scale: 3–33 against 0.2–0.8. A
   student who says "the scales differ" without the ranges has not looked.
2. *"What does `c` control? Give me a ratio."* First place versus tenth: 5.5× at c=1, 1.15×
   at c=60.
3. *"At k=5 your fusion scores 0.737 and lexical scores 0.789. What do you do?"* Do not
   ship. Press if they hedge.
4. *"Which family is failing, and what would fix it?"* Paraphrase; query rewriting, not a
   better retriever.
5. *"Your query set changed. What did that invalidate?"*

| 5 | 3 | 1 |
|---|---|---|
| Names the scale ranges; refuses to ship at k=5 without prompting | Gets there with prompting | Reports a fusion improvement measured against dense alone |

## Phase 2 — Change something (7 min)

### A — *"Add a third retriever."*

Looking for: RRF takes any number of inputs and the arithmetic does not care, but the
oracle rises and `beats_all` gets harder, and a third weak retriever dilutes further. A
strong answer asks what the *new* headroom is before adding it.

### B — *"Your users now filter by date on every query."*

Looking for: survival rate, shortlist depth, and the ANN interaction. If the filter keeps
24% of chunks, a top-5 post-filter needs roughly 20 candidates — and from an approximate
index those are not the true top 20.

### C — *"Deploy at k=5."*

The uncomfortable one, because their own gate says do not fuse there. Looking for: they
either ship lexical alone at k=5, or they change k and say why, and either is right. What
is wrong is shipping the fusion because it exists.

| 5 | 3 | 1 |
|---|---|---|
| Asks for the new headroom before adding a retriever; handles k=5 by dropping the fusion | Gets there messily | Proposes tuning weights until fusion wins |

## Phase 3 — Break it (7 min)

| Attack | What you are watching for |
|---|---|
| *"You used c=60. Justify it."* | It is a 2009 default from TREC runs. At k=10 here it captures none of the headroom |
| *"Two of your queries are retrieved by nothing at k=10. You spent this week on fusion. Was that the right week?"* | Honest answer: partly no. Fusion won one family and cannot touch the failing one |
| *"Your filter dropped recall from 0.79 to 0.32. Is that a bug?"* | No — the answers are in pre-2015 documents and the user excluded them. Looking for: measure against what the filter allows |
| *"Show me a query where fusion put a worse result above a better one."* | Dilution, per query. They should be able to find one at k=5 |
| *"Your week-5 report said dense retrieval was competitive. Does it still?"* | Different instrument. Not comparable. This is the week's quietest trap |

| 5 | 3 | 1 |
|---|---|---|
| Concedes the week partly went to the wrong problem | Finds it with prompting | Defends the hybrid because it is the modern architecture |

**Pass is 3 in every phase.**

---

## Retro (15 min)

1. *"Which station did you skip?"* Usually **1** — again. Five weeks running.
2. *"On Monday you predicted what adding the scores would do. What did you write?"*
3. *"What is the single most useful sentence in your report?"* If it is not about the
   paraphrase family, ask why not.
4. *"What is going in the failure library?"*
5. *"What did I explain badly?"*

---

## Instructor: what week 7 rests on

Week 7 is ranking and the context budget — reranking, diversity, deduplication, and
assembling a window that a generator can actually use.

Three things carry forward:

- **`unreachable`.** Week 7 cannot fix it either — reranking reorders what retrieval found —
  and saying so on Monday prevents a week of misplaced hope
- **The k conversation.** Week 7 makes k a *budget* rather than a number, and the fusion
  verdict that flipped with k is the best possible motivation for it
- **Dilution.** The idea that adding a weaker signal can make things worse is exactly what
  reranking a shortlist has to manage, and week 6 has already taught it

The thing to watch for: **a student who now believes fusion is bad.** It won a family
outright at k=10. The lesson is that it is a technique with a measurable verdict, not a
default and not a mistake.
