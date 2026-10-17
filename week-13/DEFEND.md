# Week 13 — Friday clinic

Twenty minutes, three phases, then a retro.

Week 12 asked whether they can tell a number that is true from one that is still true.
**This week asks whether they can say which moment a number is true about.**

---

## Before they arrive

1. **Does the queue remember a withdrawal's version?** Read `apply`. Without it, a late
   copy brings the document back.
2. **Is the snapshot written to a temporary file first?**
3. **Does `load` refuse other analyzer options?** Try it.
4. **Does the workflow ever pass `--accept`?** It must not.
5. **Is the tolerance written down with where it came from?**
6. **Does `/search` filter before taking k?** Filtering after can return fewer than k, or
   worse, the wrong k.

---

## Phase 1 — Explain (6 min)

1. *"Every change was applied. Why was the index wrong?"* **The question of the week.**
   Order: a newer change was overwritten by an older one delivered later.
2. *"Why does a withdrawal need a version at all?"*
3. *"The snapshot loaded without error. Why is that not enough?"*
4. *"Your gate passed a change that lost a query. Defend that."* The noise floor.
5. *"The service said 202. Is the document searchable?"*

| 5 | 3 | 1 |
|---|---|---|
| Names the moment each number is true about | Gets there with prompting | Treats "applied", "loaded", "passed" and "accepted" as "done" |

## Phase 2 — Change something (7 min)

### A — *"Two workers drain the same queue."*

Looking for: claiming must be atomic (week 3 of Agent In Production, `BEGIN IMMEDIATE`),
versions still decide, and the snapshot now has two writers. A weak answer says "add a lock".

### B — *"A reviewer wants the gate to fail on any drop at all."*

Looking for: the false-alarm rate from week 9, on nineteen queries, and what the team will
do the third time it fires on noise.

## Phase 3 — Debug (7 min)

| Seed | Break | What it does |
|---|---|---|
| Easy | `apply` records versions for upserts only | A withdrawn RFC comes back after a redelivery |
| Medium | `save` writes straight to the path | A crash leaves a snapshot that will not load — or worse, one that does |
| Medium | the workflow runs `run_gate.py --accept "ci"` | Every regression becomes the new baseline |
| Nasty | `boot` loads the snapshot but rebuilds versions as all 1 | Every redelivered change after a restart looks new |

---

## Retro (5 min)

1. *"Which of the four would you have shipped without noticing?"*
2. *"What did I explain badly?"*

---

## Instructor: what week 14 rests on

Week 14 guards, caches and scales the service. It needs the service to be exactly what it
says it is — so if a student's queue or snapshot is wrong, fix that first.
