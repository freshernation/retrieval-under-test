# Day 4 — The step that buys nothing

> **By the end of today** you can find the spend in your pipeline that purchases no
> answers, and you can price a decision without quoting a price as a result.

---

## Read first

- [ ] [**The step that buys nothing**](../../content/week-10/day-4/the-step-that-buys-nothing.md) — 25 min
- [ ] [**The fastest-ageing number**](../../content/week-10/day-4/the-fastest-ageing-number.md) — 20 min

---

## Predict first

Week 7 measured answer density collapsing from 0.237 at an 800-word budget to 0.098 at
2,000.

**Predict the answered rate at 800 and at 1,200 words.** Two numbers.

---

## The lab

`cost.py`.

```python
TOKENS_PER_WORD      tokens(text)      context_tokens(context)
cost_curve(budgets, build_context, queries)
marginal(curve)      waste(curve)      price(token_count, per_1k)
```

`marginal` is the function that matters. An average cost per answer rises smoothly across
the whole curve and shows no cliff; the margin shows a step that costs 518 tokens per query
and buys nothing at all.

```bash
pytest week-10/day-4 -v
```

---

## The written exercise

`week-10/day-4/cost.md`, one page.

1. Your two predicted answered rates and the measured ones
2. The budget curve, as a table, with `waste` marked
3. **One step costs 58% more per request, forever, and answers nothing new.** Write the
   change you are making, and what on your dashboard would have told you — the honest
   answer is nothing
4. The 4,000-word budget is the best quality setting in the table at 5.6× the tokens.
   Name the three things you would need to decide it, and which of them exist in your
   repository. Then make the decision anyway and say what you assumed

---

## Deep track

> `TOKENS_PER_WORD = 1.3` is stipulated, and this corpus is full of `rfc-7231` and `428`,
> which tokenise badly. Measure the real ratio with a real tokeniser on your own corpus,
> per query family. If identifier queries tokenise 40% worse than plain ones, every
> per-query cost figure in your report is wrong by a query-dependent amount — and the
> families you are worst at are not the families you are dearest on, which is its own
> finding.

---

## Log

`logs/stuck-log.md` and `logs/signal-log.md`.
