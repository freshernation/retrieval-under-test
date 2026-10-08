# Week 11 — Friday clinic

Twenty minutes, three phases, then a retro. **This one is Project 3**, so it runs long and
the bar is higher.

Week 10 asked whether they can tell packaging from improvement. **This week asks whether
they can decline to ship their own best work.**

---

## Before they arrive

1. **Is there a ceiling, computed before the mechanism?** No oracle, no verdict.
2. **Was any rewrite rule derived from a failing query?** The one disqualifying answer.
3. **Is cost reported in retrievals as well as tokens?** The loop is free in tokens.
4. **Is the headline delta compared against the MDE?** +0.05 against 0.1003.
5. **Does every stage default to off?** Third week of this rule.
6. **Does `citing_superseded` appear as ids?** One stage zeroes it, another adds to it.
7. **Does `ship_check` refuse?** It should, and they should agree with it.

---

## Phase 1 — Explain (7 min)

1. *"Your agent is better. Is the improvement real?"* **The question of the week, and of
   the project.** +0.05 against an MDE of 0.1003. One query.
2. *"Your rewrite was aimed at two queries. What happened to them?"* Nothing. Both still
   fail.
3. *"The family router captures 100%. Why not ship it?"* Family is an eval-set label.
4. *"What is your second hop, really?"* A metadata join, available in week 2.
5. *"The loop made 24 extra retrievals. What did they buy?"* Nothing, and `churn` says so.

| 5 | 3 | 1 |
|---|---|---|
| Volunteers the MDE comparison before being asked; names the hop as a join | Gets there with prompting | Presents +0.05 as the result |

## Phase 2 — Change something (7 min)

### A — *"Your eval set triples to 60 queries."*

Looking for: the MDE falls to about 0.056, so +0.05 is **still** not detectable and the
answer is more queries again. A strong answer notices that the `verdict` function takes the
MDE as an argument precisely because it is a property of the set, and that nobody ever
updates it when the set changes.

### B — *"A real model does the rewriting."*

Looking for: the measurement machinery is unchanged — ceiling, capture, per-family
breakdown, cost in retrievals. And the two specific things to re-check: whether the
`paraphrase` family moves at all, and whether the rewrite still breaks `r04` and `r06`,
because *dilution of an exact identifier is not a weakness of the rewriting method, it is a
weakness of lexical matching.* A student who says "a real model would be better" without
proposing the measurement has learned nothing in two weeks.

### C — *"Legal says you must never cite a superseded document."*

Looking for: the hop or the filter does it, and `r07` breaks — the one query where
supersession was not an error. A strong answer separates *superseded* from *wrong*, proposes
annotating rather than dropping, and concedes that the distinction is semantic while the
edge is not.

| 5 | 3 | 1 |
|---|---|---|
| Separates superseded from wrong; keeps the MDE argument alive under a changed set | Gets there messily | Promises a better model |

## Phase 3 — Break it (7 min)

| Attack | What you are watching for |
|---|---|
| *"Turn off query rewriting and show me the diff."* | Byte-identical, with the loop on. A dial that did nothing and was in the config |
| *"Your best result is a two-stage interaction. What happens if either stage changes?"* | It is the least durable result they have, and they should say so |
| *"The loop produces a quality signal at strength 0.786. Ship that instead?"* | Interesting, and it costs 2.2×. Compare against week 9's free 0.83 |
| *"Which of this week's four stages would you delete?"* | Rewriting and the loop. Both, with numbers |
| *"You spent a week on agents and are recommending a week-2 one-liner. Defend the week."* | The week bought the knowledge that the one-liner is sufficient, which was not free |

| 5 | 3 | 1 |
|---|---|---|
| Recommends against their own build, with the numbers; defends the week honestly | Finds it with prompting | Ships the agent |

**Pass is 4 in Phase 1 and 3 in the others.** This is a project week.

---

## Retro (20 min)

1. *"What did you predict the rewrite would do to the paraphrase family?"*
2. *"Which stage surprised you by doing nothing?"* Usually the loop; sometimes routing.
3. *"Which station did you skip?"* This week it is often **7** — the agent is fun and the
   verdict gets written last.
4. *"What is going in the failure library?"* The dial that did nothing, at minimum.
5. *"What did I explain badly?"*

---

## Instructor: what week 12 rests on

Week 12 is the report and the clinics. No new mechanism.

- **Project 3's refusal is the model for the final report.** A document that recommends
  against the thing it describes, with numbers, is what week 12 asks them to write about
  the whole course
- **The MDE audit grows one more row.** Week 9 killed week 6's fusion headline; this week
  adds Project 3's own
- **The failure library is now about thirty cards** and it is the portfolio artefact. Week
  12 is where it gets edited rather than extended

Signal sheet: **did they volunteer the MDE comparison**, and **did they recommend against
their own agent**. The first predicts whether they will ever report a null result; the
second predicts whether anybody should trust their next recommendation.

---

## Things that went wrong the first time this week was taught

- **Somebody writes a synonym dictionary from the failing queries** and gets a wonderful
  number. Catch it Monday, and make the catch public — it is the most instructive mistake
  available in this week
- **The loop is the most fun and the least useful.** Expect it to absorb two days unless
  the histogram goes on the board on Thursday morning
- **"But everyone uses agents."** True, and the week does not argue with it. The claim is
  narrower and defensible: *on this corpus, measured, these four stages cost 2.45× and
  produce a gain inside the floor.* Hold the line at that and do not over-claim
- **The verdict gets written last.** It is Project 3's deliverable. Ask to see the
  `ship_check` output on Thursday
