# Week 5 — Friday clinic

Twenty minutes, three phases, then a retro.

Week 4 asked whether they could present a two-axis decision. **This week asks whether they
can decline to declare a winner** — which is harder, because they have wanted embeddings
for a month and now have a number.

---

## Before they arrive

1. **Does the report claim dense beats lexical, or the reverse?** Either is the failure.
   Check whether the flip is in the first paragraph.
2. **Is every claim's `k` stated?** A comparison at one k reported as a claim about the
   systems is the week's cardinal sin.
3. **Is there a manifest, and does `raglab.vectors.load` accept it?** Load it yourself.
4. **Did they check `is_comparable`?** Somebody will have compared a 192-dimension index
   over one chunking against a 64-dimension index over another.
5. **Did they conclude fusion is worth it without measuring headroom?**

---

## Phase 1 — Explain (6 min)

1. *"`too many requests` and `rate limiting` are exactly orthogonal in a word space and
   0.73 apart in yours. Nobody told the system they were synonyms. What happened?"* **The
   question of the week.** Looking for: the terms co-occur, so the factorisation put them on
   a shared direction. A student who says "it learned the meaning" has not read the axes.
2. *"Read me the top terms on your first direction. Is that a concept?"* It is not — it is
   "which document is this". Press if they dress it up.
3. *"`censorship` scores 0.00 against `legal reasons`. Why, and what would a trained model
   do?"*
4. *"Which retriever is better?"* — and wait. The correct answer is a question back: at what
   k.
5. *"What is your headroom, and what does it mean for next week?"*

| 5 | 3 | 1 |
|---|---|---|
| Explains co-occurrence, not "meaning"; refuses the winner question and says why | Gets there with prompting | Declares a winner from a mean |

## Phase 2 — Change something (7 min)

### A — *"Ten thousand new documents arrive, on a different subject."*

The best mutation. Looking for: the vocabulary changes, so the axes change, so **every
stored vector is invalid** — not stale, invalid, because they index into a vocabulary that
no longer exists. This is the manifest's whole purpose. A strong answer also notices that a
trained embedding model would *not* have this problem, and that the difference is exactly
what the week has been about.

### B — *"Your users start pasting error codes."*

Exact identifiers. Looking for: dense blurs them — a rare token contributes little variance
so the factorisation discards it — and this is the family lexical retrieval is not merely
competitive on but correct. And that they can name the query in their own set.

### C — *"Halve the dimensions."*

Looking for: back to the frontier, not to re-tuning. And that variance kept is not
relevance, so a dimension count justified by "90% of variance" is justified by the wrong
quantity.

| 5 | 3 | 1 |
|---|---|---|
| Sees that the vectors become invalid, not stale | Gets there messily | Proposes re-embedding without noticing the vocabulary |

## Phase 3 — Break it (7 min)

| Attack | What you are watching for |
|---|---|
| *"Your headroom is zero. Justify spending next week on fusion."* | They cannot, on this evidence, and the right answer says so and names what would change it. A student who reaches for fusion anyway has learned nothing from week 2 |
| *"Your ANN index has recall 0.53 at nprobe 1. Is that fine?"* | Two recalls, multiplied. 0.89 becomes 0.78. One in nine queries lost to a config setting |
| *"You built an approximate index over 266 vectors. Was that worth it?"* | No — it does more comparisons than brute force. Looking for: they know, and they know why they built it anyway |
| *"Show me a query where dense wins, and tell me it is not luck."* | One query out of nine. They should reach for week 3's floor arithmetic unprompted |
| *"Is this an embedding model?"* | It is LSA over their own corpus. Looking for the out-of-vocabulary limitation, named without prompting |

| 5 | 3 | 1 |
|---|---|---|
| Declines to justify fusion; distinguishes the two recalls cleanly | Finds it with prompting | Defends dense retrieval as the modern approach |

**Pass is 3 in every phase.**

---

## Retro (15 min)

1. *"On Monday you predicted a cosine. What did you write?"* Most write something small and
   positive. It is exactly zero, and the exactness is the lesson.
2. *"You waited four weeks for this. Was it worth waiting for?"* Genuinely ask. The honest
   answer is "not as an upgrade", and a student who can say that has had the week land.
3. *"Which station did you skip?"* This week it is usually **7** — the comparison machinery
   is interesting and the eval set stopped growing.
4. *"What is going in the failure library?"*
5. *"What did I explain badly?"*

---

## Instructor: what week 6 rests on

Week 6 is hybrid retrieval and fusion, and this week has just told them the case for it is
**not established on nine queries**.

That is deliberate and it needs handling on Friday, because a week that opens with "we
cannot show this is worth doing" is demoralising if it is not framed:

- Week 6's first job is **not** to fuse. It is to build the eval set that can detect
  fusion, which week 3's milestone already asked for and which most of them have not done
- The headroom on the full sixteen-query set is not zero. They must not look — but you know,
  and you can tell them the number exists and that finding it is week 6's opening
- If anybody's dev set is already at 30, their headroom may well be non-zero. Ask on Friday;
  it is the best possible advertisement for the labelling work

Carry forward on the signal sheet: **eval set size**, and **whether they declared a
winner**. The second predicts week 6 exactly — a student who declared a winner this week
will report a fusion improvement next week without checking whether it beat either input.
