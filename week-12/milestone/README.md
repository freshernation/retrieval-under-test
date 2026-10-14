# Milestone 12 — The release check for a system that changes

> **Ship:** one function that decides whether the system is still the one you measured,
> and a report in which it says no.

---

## The brief

### 1. Write the check

`changes.py`: `release_check(measured, limits)` and `change_report(measured, limits)`.

Five numbers, all produced this week:

| Metric | From | Rule |
|---|---|---|
| `leaks` | day 3 | **must be 0. Takes no limit** |
| `debt` | day 1 | at or below your limit |
| `drift` | day 1 | at or below your limit |
| `poison_answered` | day 4 | at or below your limit |
| `stale_entries` | day 3 | at or below your limit |

A metric that was not measured fails. A limit that was not given is an error. And a limit
*given* for `leaks` is an error too.

### 2. Measure this week's system

As the week left it: the two obsoleted RFCs tombstoned, a filter in front of every result,
and anybody able to add a document.

### 3. Read what it says

`leaks` 0. `debt` 0.105, inside any sensible limit. And it does not ship: `drift` is 0.40
and a planted sentence reaches the answer every time.

### 4. Fix what you can, and re-measure

Compact the index. Put `trusted` in front of the generator. Then measure again and say
which numbers moved, which did not, and which you could not move at all.

### 5. Write `REPORT.md`

---

## The rubric

| Station | This week |
|---|---|
| 1 Corpus | **The week's loud one.** Who can write to it, and how would you know a document was planted? |
| 2 Chunk | Two of twenty-one chunks reusable after a revision. What does that do to your update cost? |
| 3 Index | Debt, drift, and your compaction rule |
| 4 Retrieve | Fold-in against refit: which one your eval numbers describe |
| 5 Rank | The planted chunk went to the front. What would have had to be true for it not to? |
| 6 Generate | Faithfulness 1.0 on a poisoned answer, in one sentence |
| 7 Measure | The release check, and the metric with no limit |

---

## The bar

- `pytest week-12 -v` green, `tools/check_evals.py` green
- `release_check` refuses this week's system, and the report says which two metrics and why
- No limit for `leaks`, anywhere, including in prose
- Drift reported at a stated depth, next to the debt that produced it
- The poison result reported as two rates: reached the context, reached the answer
- What `trusted` fixed and what it left
- One finding you could not act on, named as such
- You survive Friday

---

## What you will want to do and should not

**Set a small leak budget "to be realistic".** There is no realistic number of people who
may read what they should not. If the measurement is noisy, fix the measurement.

**Report debt and call the index healthy.** Debt was 0.105 and forty percent of the
top-tens had moved.

**Call the poisoned answer a generation failure.** The generator quoted the best-matching
sentence in its context, which is its job. Station 1.

**Add a keyword filter for the planted text.** You wrote the planted text. The next one
will not contain your keywords.

**Report this week as an improvement.** It moved no quality number. It found four ways the
numbers you had could stop being true, and that is the result.
