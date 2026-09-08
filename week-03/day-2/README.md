# Day 2 — The inverted index

> **By the end of today** you can build the data structure every search engine is, and
> you can do one thing with it that week 1's retriever could not do at all.

---

## Read first

- [ ] [**Turning the loop inside out**](../../content/week-03/day-2/turning-the-loop-inside-out.md) — 25 min
- [ ] [**Boolean search, and why it lost**](../../content/week-03/day-2/boolean-search.md) — 20 min

---

## Predict first

`too many requests` against this corpus.

- How many documents does an **OR** return, and can it separate the best from the second?
- How many does **AND** return?
- How many does the **phrase** return?

Three numbers, before you run anything.

---

## The lab

`postings.py`. Day 1's `analyze` is importable.

```python
Index(documents, **options)
  .n_documents  .vocabulary_size  .average_length  .lengths  .total_postings()
  .postings(term)  .term_frequency(term, doc)  .document_frequency(term)
  .analyze_query(query)

search_or(index, query)     search_and(index, query)     phrase(index, query)
```

**Store positions**, not just counts. They are the biggest line item in a real index and
they buy exactly one thing, which is phrase search. Knowing what you are paying for is the
reason to build this rather than import it.

`test_or_reproduces_week_one_exactly` is the one to write toward. You have made week 1's
retriever a lookup instead of a scan; you must not have made it a *different* retriever,
and "faster" and "different" are things you have to be able to tell apart.

Then `phrase`, and read `test_every_term_must_share_one_start_position` before you write
it. That trap caught this course's own reference solution: checking each term against the
first term's positions independently makes `pot of coffee` match a document that does not
contain it, with no error and a plausible-looking result.

```bash
pytest week-03/day-2 -v
```

---

## The written exercise

`week-03/day-2/the-index.md`, one page.

1. Your three predictions and the results
2. Your index holds 9,969 postings for a 390 KB corpus. What would it hold with positions
   removed, and what would you lose? Give both numbers
3. **The length table.** Your shortest document is 1,247 tokens and your longest is 19,462
   — a factor of fifteen. Write one paragraph predicting what a scorer that simply adds up
   per-term contributions will do, and name the week-1 function that already did it
4. Phrase search is the sharpest tool here and it found the right document where OR tied
   two. Say why you would not build a search engine out of it

---

## Deep track

> Implement `search_and` two ways: intersecting Python sets, and merging sorted posting
> lists with a skip on the shortest list first. Time both on the corpus. Then work out at
> what corpus size the difference would start to matter, and check whether your answer is
> within an order of magnitude of the size at which anybody would notice.

---

## Log

`logs/stuck-log.md` and `logs/signal-log.md`.
