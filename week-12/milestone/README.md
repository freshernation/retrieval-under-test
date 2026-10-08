# Milestone 12 — The report, the library, and ten clinics

> **Ship:** one report a stakeholder can act on, a failure library edited down to what
> transfers, ten scored clinics, and an expiry date on every claim.

This is the last thing you make in this course and it is the only one of the three
portfolio artefacts that leaves with you intact. The pipeline is a teaching exercise on a
ten-document corpus. The library and the method are not.

---

## The brief

### 1. The report

Four sections, in this order:

```
1  what you must act on
2  what this evaluation cannot see
3  the numbers
4  what expires
```

First line is a blocker. Section 2 before section 3. Every number carries its n and the MDE
of the set it was measured on.

### 2. The MDE audit, complete

Every claimed delta from weeks 2 to 11, marked above or below the floor of its set.
Including week 11's, which is your own work rather than the course's.

It will be uncomfortable. Week 6's fusion headline (0.053 at n=19, MDE 0.1003) and Project
3's agent (+0.05, same floor) are the course's two, and you will have more.

### 3. The failure library, edited

Roughly thirty cards, down from more. Every card has all six fields, **including the
conditions under which the fix stops working**.

And, at the front, the list of failures you could not card. Correctness is on it.

### 4. Ten clinics, scored

`week-12/day-3/README.md`, run in pairs and scored by your partner. Report the average and
your lowest three, and for each of the lowest three what you reached for instead.

### 5. Every claim marked

Durable, re-measure annually, or expired. With a count of each — if nothing is expired you
have not looked, because week 5 onwards stood in for a model and `--live` is already a
different system.

### 6. The handover note

One page, for whoever inherits this when you do not work here. The two empty stations are
on it, so they do not spend a month on the prompt.

### 7. No new mechanism

If you find a defect this week it goes in the report as a defect. The report is the
deliverable; the system was due last week.

---

## The rubric

| Station | This week |
|---|---|
| 1 Corpus | What the corpus cannot answer, and how you would know it had drifted |
| 2 Chunk | The decision, and that it has no literature behind it |
| 3 Index | What you would re-measure annually, and what you never would |
| 4 Retrieve | The station you over-use in clinics. Most people over-use this one |
| 5 Rank | The budget, and what it costs per answer |
| 6 Generate | Zero failures in week 10's attribution, and what that means for the backlog |
| 7 Measure | **The week.** The report, the audit, the library, and the expiry list |

---

## The bar

- `tools/check_evals.py` green, `tools/check_sources.py` green, `tools/check_links.py` green
- First line of the report is a blocker
- Section 2 before section 3
- No bare numbers anywhere
- The MDE audit, complete, including your own week-11 result
- Every library card has all six fields
- The list of failures you cannot card, at the front
- Clinic average of 3 or better, with no 1 on clinics 1, 5 or 9
- Every claim marked, with counts, and at least one marked expired
- A handover note
- Nothing in the report was built this week
- You survive Friday

---

## What you will want to do and should not

**Lead with what you built.** Twelve weeks of work and the reader needs one blocker. The
work is section 3.

**Keep every card.** A thirty-card library you edited is worth more than a sixty-card one
you accumulated, and the deleted cards are evidence that you can tell a bug from a failure
mode.

**Leave the stop-working line blank.** It is the field that makes a card a method. Without
it the card says *"this worked for me"*.

**Mark everything durable.** Prices, model behaviour, library APIs, the simulated
generator's numbers, every value from week 5 onward. If your expired count is zero, read
your own fences again.

**Fix the thing you found on Monday.** This is the week's main failure mode and it produces
a better system and no report. The report is what somebody acts on.

**Claim the course solved correctness.** It did not. Twelve weeks and it is still out of
reach, and the single most valuable sentence you can write is the one that says so and then
says what you measured instead.
