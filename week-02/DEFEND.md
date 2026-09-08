# Week 2 — Friday clinic

Twenty minutes on the milestone, in three phases, then a retro. The student has
`REPORT.md`, their manifest and `runs/` open; you have this page.

Week 1 asked whether they wrote their judgments. This week asks whether they **opened the
files** — and the whole clinic is built to make that undeniable one way or the other.

---

## Before they arrive

Read `REPORT.md`, the manifest, and `runs/`. Pick, in advance:

- **one row of their manifest** to make them explain from memory
- **the mutation** for phase 2
- **which of their two decisions** to attack

Then check four things faster than you can ask about them:

1. **Did they ship or hold each change, and did they say which kind it was?** A report that
   ships both or holds both without using the words is the failure this week is designed
   to produce, and it is worth catching plainly.
2. **Is the corpus total in there anywhere?** If they reported "27% removed" rather than
   ten rows, they have hidden their own finding from themselves.
3. **Is RFC 7159 still in the index?** If they deleted it, ask about `r14` and watch.
4. **How many `test` runs are in `runs/` this week?** Same as last week. The number tends
   to rise in week 2 because the results are disappointing.

---

## Phase 1 — Explain (6 min)

1. *"Without looking — which document in this corpus is the odd one out, and why?"* RFC
   9309, unpaginated, 2022. **This is the question of the week.** A student who opened the
   files answers in three seconds. A student who only ran the lab says "the coffee one",
   which is a different and much easier observation.
2. *"Your cleaner removed [N]% of RFC 7725 and [N]% of RFC 3986. Why are those different?"*
   Looking for: boilerplate is a fixed cost per document. If they say "3986 is messier",
   they have the sign backwards and have not read their own table.
3. *"Where does the fact that RFC 7159 is obsolete live?"* In RFC 8259. Press until they
   say that the superseded document contains no trace of its own supersession.
4. *"Read me your coverage gaps."* Then: *"which of those would a user ever see?"*
5. *"You were not allowed to touch the retriever. What did that make you find?"*

| 5 | 3 | 1 |
|---|---|---|
| Names the format outlier instantly; explains the boilerplate asymmetry correctly | Gets both with prompting | Has not read their own manifest |

## Phase 2 — Change something (7 min)

Pick **one**. Ask what stops being true *before* they say what they would do.

### A — *"Ten more RFCs arrive. Three are from 2023 and unpaginated. One is a duplicate of one you already have, under a different number."*

The best mutation this week. Looking for: their cleaner silently no-ops on three
documents and reports success; their duplicate detection finds the pair but cannot tell
them whether it is supersession or a mirror; and the manifest is the only artefact that
would surface any of it. A strong answer says **the manifest is the thing that scales, not
the cleaner.**

### B — *"Your corpus is now PDFs, not text."*

Looking for: everything they wrote this week is about *one* extraction's failure modes, and
a different extractor fails differently — but `loss_report` and `manifest` are about the
*output*, so they transfer and the regexes do not. A student who says "I would use a better
PDF library" has missed that the question is how they would know it was better.

### C — *"A document is retracted. It must not be answerable from, but it must stay searchable for auditors."*

Looking for: this is not deletion and it is not demotion. It is a third thing, it needs a
field in the manifest, and it is a station 6 policy driven by station 1 metadata. Very few
will have the vocabulary for this and it is fine if they build it live.

| 5 | 3 | 1 |
|---|---|---|
| Names what silently no-ops before designing; reaches for the manifest | Gets there messily | Proposes a better cleaner immediately |

## Phase 3 — Break it (7 min)

Two attacks, pressed until they defend or concede.

| Attack | What you are watching for |
|---|---|
| *"Your cleaning interval touches zero. Justify shipping it — or justify holding it. Either is fine, and 'it's obviously better' is not."* | **The centre of the week.** Looking for: they distinguish a tuning change from a correctness fix, and they know which one cleaning is. It is a tuning change, and the honest answer is that its justification came from the near-duplicate result rather than from recall |
| *"Delete RFC 7159. Why not?"* | `r14` in the held-out split needs both halves. If they cannot name a query, they are arguing from principle rather than from their own eval set |
| *"Show me a query where demotion made things worse."* | There is none, and they should know that as a fact they checked, not a fact they assume. `worse_than` is the answer |
| *"Twenty percent of your corpus is obsolete. What is that number where you work, and how would you find out?"* | Whether any of this has transferred out of the exercise |
| *"Your ingest drops every abstract. Read me RFC 7725's abstract and tell me it was worthless."* | It is not worthless. Looking for: they made a trade and know it was a trade |

| 5 | 3 | 1 |
|---|---|---|
| Distinguishes the two kinds of change unprompted; cites their own queries | Finds it with prompting | Defends every change by asserting it is obviously right |

**Pass is 3 in every phase.**

---

## Retro (15 min)

1. *"Which station did you skip?"* This week it is usually **7** — they got absorbed in the
   corpus and stopped measuring carefully. Last week it was 1. Point out the symmetry.
2. *"On Tuesday you predicted what cleaning would do to recall@3. What did you write?"*
   Nearly everybody writes between +0.05 and +0.15. The answer is 0.000. Sit with it.
3. *"What did you find by opening a file that you would never have found by running code?"*
   If the answer is nothing, that is the most important thing you learn today.
4. *"What is going in the failure library?"*
5. *"What did I explain badly?"*

---

## Instructor: what next week rests on

Week 3 is lexical retrieval properly — tokenisation, the inverted index, BM25, and tuning
`k1` and `b`. The fence lifts on the retriever and it will feel like a release.

The prerequisite is that they believe two things, and the second is the fragile one:

1. **A retrieval failure can originate before retrieval.** Week 1 planted it, this week
   should have made it undeniable.
2. **A change without a delta is not an improvement, even when it is obviously correct.**
   Week 3 is the first week where changes *do* produce large, clean, interval-excluding
   improvements, and a student who has not internalised the discipline this week will
   spend week 3 changing four things at once and reporting the total.

Watch for that specifically. The signal is a week-3 student who is delighted and cannot
say which of their changes did it.

The other signal to carry forward: **a student who never opened a document.** Phase 1
question 1 finds them. There is no recovering week 2 for them retrospectively, so the fix
is to make week 3's Monday hour start with fifteen minutes reading RFC 6585 aloud, looking
for the word "rate limit", and finding it once, in parentheses.
