# Day 4 — A retriever in forty lines

> **By the end of today** you have a baseline number, and you can name the four reasons
> it is bad without being told them.

---

## Read first

- [ ] [**The baseline you must beat**](../../content/week-01/day-4/the-baseline-you-must-beat.md) — 25 min
- [ ] [**Reading a claim about retrieval**](../../content/week-01/day-4/reading-a-rag-claim.md) — 25 min · sources: [Robertson & Zaragoza §1–2](https://www.staff.city.ac.uk/~sbrp622/papers/foundations_bm25_review.pdf)

---

## Predict first

The retriever you are about to write splits text on non-letters, counts how many query
words a document contains, and sorts. No weighting of any kind.

The query is **"what does ROCC stand for"**. The corpus contains a glossary whose second
line is `ROCC — Rail Operations Control Centre`.

**What position does the glossary come back in?** Write your number down. There are 30
documents.

---

## The lab

`overlap.py`.

```python
normalise(text)                       term_set(text)
overlap_score(query_terms, doc_terms) coverage_score(query_terms, doc_terms)
frequency_score(query_terms, doc_tokens)
rank(query, documents, k=10, score=overlap_score)
explain(query, document)
```

Write `rank` carefully. Two rules in it are not optional and both are in the docstring:
drop zero scores, and break ties by document id. The second one is why your numbers will
still be the same next week.

Then run `test_the_glossary_ranks_last_for_the_query_it_answers_perfectly` and compare it
with what you predicted.

Then `frequency_score`, which is the obvious improvement, and
`test_frequency_scoring_hands_the_top_slot_to_the_longest_document`, which is what it does.

```bash
pytest week-01/day-4 -v
```

---

## The written exercise

`week-01/day-4/four-defects.md`, one page.

The tests demonstrate four separate defects in this retriever. Name each one, and for each
say **which station it belongs to** and **what class of query it destroys**:

1. Every term is worth the same
2. Longer documents win under frequency scoring
3. A word the document is *about* but does not contain is invisible
4. `$3.00` becomes `3` and `00`

Then, the important part: **rank them by how much you expect each one to cost on a real
corpus of a million documents, and say what changes about the ranking as the corpus grows.**

Three of the four are fixed in week 3 by arithmetic. One of them is not fixable by
arithmetic at all, and finding out which is the point of the exercise.

---

## Deep track

> `explain()` on every query in `dev` where the baseline scores below 0.5. Group the
> `missed` sets. You are looking for whether the failures share a shape — if they do, you
> have just done, by hand, what week 9 automates.

---

## Log

`logs/stuck-log.md` and `logs/signal-log.md`.
