# Week 12 — A corpus that changes

> **Destination**
> The system you measured, after a document is withdrawn, a document arrives, a reader who
> may not see everything asks a question, and somebody plants a document — with a release
> check that says whether it is still the system you measured.

Every number in this course so far describes a frozen corpus, read by one person, written
by nobody but its authors. None of those three things is true of a system anybody uses.

This week changes them one at a time, and each time something that looked finished turns
out to have been resting on the assumption.

---

## The week

| Day | Folder | What you'll be able to do |
|---|---|---|
| Mon | `day-1/` | Delete from an index without rebuilding it, and measure what the cheap way costs |
| Tue | `day-2/` | Re-embed only what changed, and find that an added chunk is not a rebuilt one |
| Wed | `day-3/` | Put a permission in front of the retriever, and find the leak that is not in it |
| Thu | `day-4/` | Plant a document, take a question, and watch every answer check pass |
| Fri | `milestone/` | Ship the release check for a changing system — and have it say no |

---

## Four findings

Each is a test with the day's name on it.

| Day | The finding |
|---|---|
| Mon | Tombstone 28 chunks of 266 and no dead document is ever returned — and **8 of 20** top-tens are not the ones a rebuilt index gives. No top result changes, which is why nobody notices |
| Tue | Fold two new RFCs into the old embedding basis, or refit it: the top five agree for **5 of 20** queries. Recall cannot tell you which is better. They are simply different retrievers |
| Wed | Neither filter leaks. A cache keyed on the question, filled by staff, serves a public reader a restricted chunk **11 times in 20** |
| Thu | One planted sentence takes **20 of 20** questions, and the answer scores faithfulness **1.0** |

---

## What they have in common

In every case a number you already trusted kept saying the system was fine.

| The number | What it was measuring | What went wrong underneath |
|---|---|---|
| debt 0.105 | how many documents were dead | what the dead ones did to the scores of the living |
| recall, within noise | whether the right documents came back | that it was a different retriever from the one you evaluated |
| leaks 0 from the retriever | the path the filter is on | the cache in front of it |
| faithfulness 1.0 | whether the answer follows from the context | whether the context should be believed |

Station 1, the corpus, has been the quiet row in every rubric since week 2. This is the
week it is not quiet.

---

## `--live`

Nothing this week needs a model or a network. Thursday's deep track does: whether a real
model *obeys* an instruction in a retrieved chunk is a question the stipulated generator
cannot answer, and a live run is a different system from an offline one, as always.

---

## Milestone

`changes.py` and `REPORT.md`: the release check for a system that changes. It has five
numbers. Four have a limit you choose. One does not.
