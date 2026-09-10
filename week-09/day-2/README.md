# Day 2 — Validating a judge

> **By the end of today** you can decide whether a model-scored metric has told you anything,
> using two lines of arithmetic that nobody runs.

---

## Read first

- [ ] [**LLM-as-judge**](../../content/week-09/day-2/llm-as-judge.md) — 25 min
- [ ] [**Two lines before you trust it**](../../content/week-09/day-2/two-lines-before-you-trust-it.md) — 25 min

---

## Predict first

A judge scores your twenty answers. Its accuracy against your labels is **0.70**.

**Is that good?** Answer before the lab, and commit.

---

## The lab

`judgecheck.py`. Week 1's `cohens_kappa` is importable, doing a job it was not built for and
is exactly right for.

```python
labels(judge, cases)          accuracy(predicted, truth)      kappa(predicted, truth)
constant_baseline(truth)      self_agreement(judge, cases)
length_probe(...)             position_probe(...)             validated(report)
```

Write `constant_baseline` **before** you look at the judge's numbers. Two lines, and it is
the only thing that makes an accuracy figure interpretable.

Then the probes. `length_probe` is a **controlled pair** — identical content, different
length — and it is the cheapest bias test there is.

```bash
pytest week-09/day-2 -v
```

---

## The written exercise

`week-09/day-2/judge.md`, one page.

1. Your prediction, and the baseline
2. Judge accuracy, judge kappa, baseline accuracy, baseline kappa. Four numbers, and the
   sentence that interprets them
3. **The clean judge scores the padded answer higher than the short one with `length_bias`
   set to zero.** Explain where the bias came from, and what that implies about week 8's
   faithfulness numbers
4. The `validated()` bar is three cheap conditions and this judge fails it. Write down what
   you would need in order to trust a judge's score enough to gate a release on it

---

## Deep track

> Build a second judge with a different base — query-relevance overlap rather than
> context-support overlap — and measure agreement between the two judges as well as with the
> truth. Two judges agreeing with each other and not with you is a specific and common
> situation; work out what it means and which of the three you would trust.

---

## Log

`logs/stuck-log.md` and `logs/signal-log.md`.
