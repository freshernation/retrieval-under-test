# Day 2 — Relevance is a judgment

> **By the end of today** you can write a relevance judgment, defend the line between a 1
> and a 2, and put a number on how much you disagree with yourself.

---

## Read first

- [ ] [**Relevance is a judgment, not a property**](../../content/week-01/day-2/relevance-is-a-judgment.md) — 25 min · sources: [TREC](https://trec.nist.gov/pubs.html), [Voorhees on judgment variation](https://trec.nist.gov/pubs/trec8/papers/overview_8.pdf)
- [ ] [**Building an eval set that can hurt you**](../../content/week-01/day-2/building-an-eval-set.md) — 25 min

---

## Predict first

You are about to judge 12 query-document pairs, and then judge the same 12 again in three
days without looking at your first answers.

**What fraction do you think you will agree with yourself on?** Write the number down now,
sealed. Most people write 95. Come back on Friday.

---

## The lab

`judging.py`.

```python
parse_grade(value)                    relevant_set(judgments, threshold=2)
agreement(a, b)                       overlap_size(a, b)
binary_disagreements(a, b)            cohens_kappa(a, b)
pool(rankings, depth=10)              smells(judgments_by_query, corpus_ids)
```

Write `cohens_kappa` after `agreement` and run
`test_kappa_is_zero_when_both_judges_just_say_no`. Two judges agreeing 90% of the time and
having told you nothing at all is more persuasive in one assertion than any amount of
prose about chance-corrected agreement.

Then `smells`, and read `test_the_one_that_ruins_eval_sets` carefully. That failure is
undetectable in every metric you will compute for the rest of the course.

```bash
pytest week-01/day-2 -v
```

---

## The written exercise

Judge twelve pairs by hand, in `week-01/day-2/judgments.md`.

Take the queries `q01`, `q02`, `q05` and `q07` from `data/gold/sample/queries.yml`. For
each, **ignore the shipped grades** and judge three documents of your own choosing from
the corpus. Write the grade, and one sentence of why.

Then compare with the shipped grades and answer, in a paragraph:

> Where do you disagree with the person who wrote the shipped set, and is either of you
> wrong?

Do not skip that question. The answer is usually "neither", and the consequences of it
being usually "neither" are what tomorrow's metrics are built on top of.

**You may not use a language model for any part of this**, including checking your work.
`FENCE.md` explains why at length and it is the most important rule in the week.

---

## Deep track

> If you have run an annotation project before: implement Krippendorff's alpha alongside
> kappa and say, in three sentences, when the difference between them would change a
> decision you made. Most people who quote kappa cannot.

---

## Log

`logs/stuck-log.md` and `logs/signal-log.md`.
