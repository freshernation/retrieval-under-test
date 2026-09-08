# Week 3 — Friday clinic

Twenty minutes on the milestone, in three phases, then a retro.

Week 1 asked whether they wrote their judgments. Week 2 asked whether they opened the
files. **This week asks whether they can be trusted with a number that went up.**

It is the first week where the results are genuinely good, and the failure mode changes
completely: not despair, but enthusiasm.

---

## Before they arrive

Read `REPORT.md`, the run ledger, and `my-queries.yml`. Pick your target and check five
things first:

1. **How big is the eval set?** If it is still 10/6, the milestone was not done and
   everything else in the report is unreportable. Start there and be direct about it.
2. **Six runs, one change each?** Diff consecutive `config_hash` values in the ledger. Two
   knobs moving between runs is the week's cardinal sin, and it is visible in ten seconds.
3. **Does the index run reproduce the baseline exactly?** If not, they have a bug they
   have reported as a result.
4. **Are the four tuning warnings in the report, next to the number?** In a footnote does
   not count.
5. **How many `test` reads this week?** Grid search is when this number climbs.

---

## Phase 1 — Explain (6 min)

1. *"`status` scores 0.047 and `429` scores 1.992. Where do those come from, and why is
   one forty times the other?"* Make them derive the idf out loud. **The question of the
   week.** A student who cannot rebuild it copied the formula.
2. *"You removed stopwords on Monday and recall got worse. Why?"* Looking for: a stopword
   list is a guess made before any evidence; idf is the same idea computed from the corpus.
   The weak answer is "the list was wrong for this corpus", which is true and shallow.
3. *"Three queries improved on Wednesday. Name them and tell me why each one did."* Three
   different reasons. If they can only give one, they have looked at the mean.
4. *"Your interval's lower bound was exactly zero. Not nearly — exactly. Why?"* The floor
   arithmetic. If they cannot get there, walk it with them: six unchanged out of nine,
   `(6/9)⁹`, 0.0260, just over 0.025.
5. *"How many queries did you need, and how many did you write?"*

| 5 | 3 | 1 |
|---|---|---|
| Derives idf live; explains the exact-zero lower bound from the arithmetic | Gets both with prompting | Quotes the improvement and cannot rebuild any of it |

## Phase 2 — Change something (7 min)

Pick **one**. Ask what stops being true before they say what they would do.

### A — *"The corpus grows to ten thousand documents. Which of your numbers survive?"*

The best mutation this week. Looking for: idf changes for every term and their tuning is
invalidated; average length changes so `b` means something different; recall@3 stops being
degenerate and becomes informative; and their eval set, which they just tripled, is now a
vanishing sample again. A strong answer notices that **the tuned parameters are the least
portable thing they built** and the analyzer is the most.

### B — *"Half your users start pasting error messages instead of asking questions."*

Twenty-token queries full of identifiers and punctuation. Looking for: what their tokeniser
does to `HTTP/1.1 429 Too Many Requests`, whether `keep_identifiers` helps or floods, and
that BM25 sums independently so a long query dilutes nothing but adds noise.

### C — *"Show me your grid search with b fixed at 0.75 and only k1 varying. Now justify having searched both."*

Looking for: honesty about how much of the 45-point grid was information. Two parameters,
nine queries, forty-five looks. A good student concedes that a one-dimensional sweep would
have been better evidence and nearly as good a result.

| 5 | 3 | 1 |
|---|---|---|
| Names what is portable and what is not; reasons from the formula | Gets there messily | Proposes re-tuning |

## Phase 3 — Break it (7 min)

| Attack | What you are watching for |
|---|---|
| *"Your grid says k1 = ∞. That means turn off saturation. Do you believe it?"* | **The centre of the week.** Looking for: they investigated rather than shipped or dismissed. Ten documents, long, few queries. The correct answer contains "I do not know, and here is what would tell me" |
| *"The tuned config also won on `test`. Does that settle it?"* | Six queries, one read, four warnings still true. Looking for: they can say why a confirming held-out number is the most dangerous result in applied retrieval — it retires the doubt |
| *"Which of your six runs changed two things?"* | Ask it even if the answer is none. The ones who did will usually admit it here |
| *"You wrote twenty-six new queries. How many did you write against RFC 6265?"* | Whether they grew the set to cover the corpus or grew it wherever was easy |
| *"Your kappa went [up/down] since week 1. Why?"* | Honesty. Down is a fine answer — harder queries — and "I got better at it" with no supporting detail is not |

| 5 | 3 | 1 |
|---|---|---|
| Concedes cleanly where the answer is "I got away with it" | Finds it with prompting | Defends the tuned number by its size |

**Pass is 3 in every phase.**

---

## Retro (15 min)

1. *"Which station did you skip?"* This week it is usually **1** again — the corpus went
   quiet the moment the retriever became interesting.
2. *"On Monday you predicted what stopwords would do. What did you write?"* Nearly everyone
   writes +0.05 to +0.15. It was negative.
3. *"You spent a day writing queries and an hour tuning. Which produced more?"* The answer
   is the day, and the reason is the floor arithmetic. This is the sentence to send them
   home with.
4. *"What is going in the failure library?"*
5. *"What did I explain badly?"*

---

## Instructor: what next week rests on

Week 4 is chunking — the decision with **no primary source behind it**, and the first week
where the unit of retrieval stops being a document.

Three things carry forward, and the third is the one that decides how week 4 goes:

- **The eval set must have grown.** Week 4's changes are smaller than BM25's and there is
  no chance of measuring them at n=9. A student who skipped the labelling will spend week 4
  unable to detect anything and will conclude that chunking does not matter
- **The `b` conversation.** Length normalisation exists because documents vary fifteenfold.
  Chunking makes them uniform. Ask on Friday what they expect `b` to do next week; the good
  answer is "matter much less", and it is a nice hook
- **Week 2's cleaning, still unresolved.** They have now measured it twice and it has moved
  nothing twice. Week 4 is where a chunk can be *entirely* boilerplate and the question
  finally gets a real answer. Make sure they leave knowing it is still open rather than
  quietly concluding cleaning was pointless

The failure mode to watch for all of next week: **a student who now trusts numbers.** Week
3 rewards them for the first time, and week 4's deltas are small, noisy and easy to
over-read. The four warnings from day 4 are the thing to keep pointing back at.
