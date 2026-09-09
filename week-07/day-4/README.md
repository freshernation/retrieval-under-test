# Day 4 — Where in the window

> **By the end of today** you can order a context window deliberately, and you can say
> exactly how much confidence that decision deserves.

---

## Read first

- [ ] [**Lost in the middle**](../../content/week-07/day-4/lost-in-the-middle.md) — 25 min
- [ ] [**Stipulated models**](../../content/week-07/day-4/stipulated-models.md) — 20 min

---

## Predict first

Your answer-bearing chunk lands, on average, about a third of the way into the window.

**Is that a good place for it?** You cannot know today. Write down what evidence would tell
you.

---

## The lab

`order.py`.

```python
order_by_rank(selected)     order_by_document(selected)     ends_first(selected)
attention_weight(position, n, dip)                          answer_positions(order, chunks, query)
expected_use(order, chunks, query, dip)                     assemble(order, texts)
```

`attention_weight` is a **stipulated model**. Its shape is from the literature; its numbers
are ours and are not measured. Every test about it asserts a **direction**, never a value,
and the last test checks that the direction survives changing the parameter.

`assemble` labels every chunk. Week 8 asks the generator to cite, and it can only cite what
it can name.

```bash
pytest week-07/day-4 -v
```

---

## The written exercise

`week-07/day-4/order.md`, one page.

1. Your answer to "what evidence would tell you"
2. Where your answer-bearing chunks actually land, as a distribution. This part is
   **measured** and it is the only part that is
3. The three orderings ranked under the stipulated model, at three values of `dip`. Then the
   sentence you may honestly write about that ranking, and the sentence you may not
4. **The discipline.** Week 4 refused to assert a chunk size. Week 3 refused to ship a
   plateau it did not understand. Write two sentences on what this week is refusing, and why
   that is not the same as knowing nothing

---

## Deep track

> The U-shape is reported for particular models, prompts and window lengths. Find the
> primary source, read what was actually varied, and write down three ways your setting
> differs from theirs. Then say whether `ends_first` is still a reasonable default for you —
> and note that "reasonable default" is a much weaker claim than the one usually made.

---

## Log

`logs/stuck-log.md` and `logs/signal-log.md`.
