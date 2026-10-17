# Week 12 — Friday clinic

Twenty minutes, three phases, then a retro.

Week 10 asked whether they can tell packaging from improvement. **This week asks whether
they can tell a number that is true from a number that is still true** — after the corpus
moved, the reader changed, and somebody else wrote a document.

---

## Before they arrive

1. **Is drift reported next to debt, with a depth?** Debt alone is the reassuring number.
2. **Does the report say which retriever its recall describes?** Fold-in or refit.
3. **Is there a limit for `leaks` anywhere?** In code or in prose. There must not be.
4. **Is the cache key scoped?** And is the cost to the hit rate stated?
5. **Are the poison results two rates?** Reached the context, reached the answer.
6. **Does the poisoned answer's faithfulness appear, as 1.0?** If it is missing, they
   did not run the check.
7. **Does `release_check` still refuse?** After their fixes it may not — ask what moved.

---

## Phase 1 — Explain (6 min)

1. *"No dead document was ever returned. So what changed?"* **The question of the week.**
   The scores of the live ones, because idf and average length still count the dead.
2. *"No top result changed. Why does that make it worse?"* Because every spot check passes.
3. *"Your recall is the same after folding in. Is it the same retriever?"* No: five of
   twenty lists agree. And twenty queries cannot rank the two.
4. *"Neither filter leaked. Where was the leak?"* In front of the filter. Press until they
   list a second place besides the cache.
5. *"Faithfulness 1.0 on a planted answer. Is the check broken?"* No. Make them say what
   it measures and what it does not.

| 5 | 3 | 1 |
|---|---|---|
| Says what each trusted number was measuring, and what moved underneath it | Gets there with prompting | Reports debt, recall and faithfulness as evidence the system is fine |

## Phase 2 — Change something (7 min)

### A — *"Compaction takes an hour and blocks writes. How often do you run it?"*

Looking for: a trigger on debt, an admission that debt does not predict drift, and a
proposal to measure drift on a sample of real queries before deciding. A weak answer picks
a percentage.

### B — *"The planted document comes from a source you trust."*

`trusted` passes it. Looking for: provenance narrows who can attack, it does not remove
the attack; the remaining controls are review at ingest and limiting what an answer can
do. A student who reaches for a content filter has not absorbed Thursday.

## Phase 3 — Break it (7 min)

Seed one before they arrive.

| Seed | Break | Probes |
|---|---|---|
| Easy | `doc_ids` returns tombstoned ids too | Dead documents in results. Do they go to the filter or the index? |
| Medium | `remove` leaves empty posting lists behind | Vocabulary size is wrong; results are not. What would notice? |
| Medium | `can_read` treats `None` as public | Every test with a full ACL passes |
| Hard | `scoped_key` joins groups unsorted | Two readers with the same groups get different keys. Nothing leaks; the cache quietly stops working |
| Nasty | `release_check` accepts `limits["leaks"] = 0` | Behaves identically today. The door is open for the day someone sets it to 1 |

The **Nasty** one is the week: a change with no effect on any current result, whose whole
cost is in what it permits later.

---

## Retro (5 min)

1. *"Which number did you trust on Monday that you trust less now?"*
2. *"What sits in front of the filter in a system you have worked on?"*
3. *"What did I explain badly?"*

---

## Instructor: what week 13 rests on

Week 13 runs the system as a service and week 14 guards, caches and scales it. Week 15
is the report and the clinics.

- **The failure library gains its four most transferable cards this week.** None of them
  depends on this corpus: statistics that count the dead, an eval that describes a
  retriever you no longer run, a check that protects only its own path, and grounding
  that is not trust.
- **Station 1 finally has entries.** Every earlier rubric had it nearly empty. The report
  should say so, and say why it took twelve weeks.
