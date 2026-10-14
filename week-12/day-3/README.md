# Day 3 — The leak is in front of the filter

> **By the end of today** two readers asking the same question get different results, the
> one with fewer permissions gets a full page, and you have found the place a correct
> filter does not protect.

---

## Read first

- [ ] [**The leak is in front of the filter**](../../content/week-12/day-3/the-leak-is-in-front-of-the-filter.md) — 25 min

---

## Predict first

Three of the ten RFCs are staff-only. A public reader asks the twenty dev questions, and
you filter each top five down to what they may see.

**How many of the twenty come back with nothing at all?**

---

## The lab

`access.py`. Week 6's `filters.py` and week 10's `caching.py` are importable, and today is
mostly those two meeting.

```python
can_read(user_groups, doc_groups)        reader(acl, groups)
leaks(results, predicate)                scoped_key(query_text, groups)
revoke(entries, doc_id)
```

`reader` returns a predicate, which is exactly what `pre_filter` and `post_filter` take.
You wrote the filters in week 6. Today you find out which one to use.

```bash
pytest week-12/day-3 -v
```

---

## The written exercise

`week-12/day-3/access.md`, one page.

1. Your prediction and the three rows: post-filter, over-fetch, pre-filter
2. Over-fetching twenty was enough here. Say what it depends on, and why the retriever
   cannot know it
3. **A document with no recorded rule.** The lab makes it unreadable. Write the argument
   for the other choice as strongly as you can, and then say why you still would not ship
   it
4. The cache leaked eleven times and no test on the retriever would have caught it. List
   every other place in this pipeline that sits in front of the filter
5. Scoped keys made the leak go away. State what they did to week 10's hit rate, and the
   traffic assumption your answer depends on

---

## Deep track

> A reader can learn that a hidden document exists without ever seeing it. Find a way, on
> this pipeline: compare what a public reader gets back from a post-filter with what they
> get from a pre-filter, and look at counts and at scores. Write down what leaks, and which
> of the two filters you would now call correct.

---

## Log

`logs/stuck-log.md` and `logs/signal-log.md`.
