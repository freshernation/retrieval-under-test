# Week 12 — The final review

Two hours. Ten clinics at five minutes each, then the report defence, then the retro.

This is the exam, and it is the same exam as every other Friday: **can you find the failure
under attack.** The difference is that nobody tells you which week it came from.

---

## Before they arrive

1. **Does the report open with a blocker?** Not a metric, not a summary of the work.
2. **Does every number carry its n?** Spot-check three.
3. **Is the MDE audit present**, and does it include their own work from week 11?
4. **How many cards in the library?** Thirty-ish, edited down from more.
5. **Does every card have a *conditions under which the fix stops working* line?** The
   field most often left blank, and the one that makes a card transferable.
6. **Is every claim marked durable / re-measure / expired?**
7. **Is there anything in the report that was built this week?** There should not be.

---

## The ten clinics

Five minutes each. Read the scenario, and the student has to answer three things:

> **which station · what diagnostic finds it · what you would not do**

The third is scored hardest, because it is where eleven weeks either took or did not.

The scenarios are in `week-12/day-3/README.md`. They are drawn from the course's own
measurements, they are not in order, and the station is not always the obvious one.

| 5 | 3 | 1 |
|---|---|---|
| Names the station, the diagnostic and the thing not to do, in under a minute | Gets the station with prompting | Reaches for the prompt, the chunker, or a better model |

**Pass is an average of 3 across ten, with no score of 1 on clinics 1, 5 or 9** — those three
are the ones where a wrong answer costs somebody else money.

---

## The report defence (20 min)

1. *"Give me your first line."* It should be a blocker.
2. *"Which of your own results did not survive the MDE audit?"* Everybody has at least
   two. Week 6's fusion headline and Project 3's +0.05 are the course's.
3. *"What can your evaluation not see?"* Correctness. Still. Since week 1.
4. *"Which of your findings expires first?"* And: *"what would you re-measure to find out?"*
5. *"Show me the card you are least sure transfers."* The honest answer is one of the
   corpus-specific ones.
6. *"If I gave you one more week, what would you do?"* Write more queries. Week 9 priced
   it: 77 for five points.

| 5 | 3 | 1 |
|---|---|---|
| Leads with a blocker; names correctness unprompted; concedes two of their own results | Gets there with prompting | Presents the system's best numbers |

---

## The attack (15 min)

Not scenarios this time. Their own report.

| Attack | What you are watching for |
|---|---|
| *"Quote me your best number without its n."* They should refuse |
| *"This card has no stop-working condition. Defend it."* It is not a card, it is an anecdote |
| *"You recommended against your own agent. Were you just hedging?"* The numbers, in sentences |
| *"Which rule did you break at least once?"* Rule 1, usually, and in week 1 |
| *"What is in this report that you would be embarrassed by in two years?"* The expired claims, and they should already be marked |

---

## Retro (20 min) — and this one is the course's

1. *"Which week changed how you work?"* Week 1 and week 9 split it, roughly.
2. *"Which week did you disagree with, and do you still?"* Week 5 is the designed answer —
   dense retrieval arriving late and arriving losing.
3. *"What did you stop doing?"* The target answer is *rewriting the prompt first*.
4. *"What will you do on Monday at your job?"* Ask for the eval set. Every time.
5. *"What did I explain badly, across twelve weeks?"* Write the answers down. This is the
   course's own eval set and it is the only one it has.

---

## Instructor: what comes after

Nothing. This is the last week, so the honest close is about what the course did not do.

- **It never gave them a running production system.** The reference course does that in
  week 1. Say so again on Friday, as you said it in week 1 — what they have instead is the
  ability to tell whether one is any good
- **It never measured a real model.** Everything from week 5 on stood in for one, declared
  openly, with the stipulated-model rule. `--live` is their first week-13
- **It never solved correctness.** Twelve weeks and it is still out of reach. That is not a
  gap in the course; it is the state of the field, and the course's contribution is that
  they will not mistake faithfulness for it

Signal sheet: **clinic average**, and **did they lead with a blocker**. The first is the
only grade in the course that cannot be faked. The second predicts whether anybody will
read their next report.
