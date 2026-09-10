# Day 3 — Faithfulness, and the thing it is not

> **By the end of today** you can measure whether each claim is supported by its source,
> and you can explain why a perfect score does not mean the answers are right.

---

## Read first

- [ ] [**Supported by what**](../../content/week-08/day-3/supported-by-what.md) — 25 min
- [ ] [**Faithful and wrong**](../../content/week-08/day-3/faithful-and-wrong.md) — 25 min

---

## Predict first

The default generator copies sentences from the chunks it cites.

1. **What will its faithfulness score be?**
2. **How many of its answers are correct?**

Write both, and notice if you expected them to be related.

---

## The lab

`faithful.py`.

```python
content_words(text)      support(claim, source)       best_support(claim, sources)
sentence_verdicts(answer, context, chunks, threshold)
faithfulness(answer, context, chunks)                 faithfulness_rate(answers, ...)
cites_superseded(answer, chunks, graph)
```

`support` is **word overlap**, and it is a proxy. It rewards copying and punishes correct
paraphrase, and it cannot see a negation — `MUST` and `MUST NOT` score the same. Write the
test for that yourself before you trust any number it gives you.

`faithfulness` needs an explicit refusal check. "I could not find an answer" shares no words
with the context, so a naive implementation scores it 0.0 — punishing the system for the one
behaviour week 8 is trying to encourage.

```bash
pytest week-08/day-3 -v
```

---

## The written exercise

`week-08/day-3/faithful.md`, one page.

1. Your two predictions and the results
2. **`r05`, in full.** Paste the answer, its faithfulness score, and the date RFC 7159 was
   withdrawn. Then one paragraph on what would have to change for a faithfulness metric to
   catch this — and why it is not a faithfulness metric's job
3. Three answers cite a superseded document. Why does `cites_superseded` live outside the
   faithfulness machinery rather than inside it?
4. The support check cannot see a negation. Construct a query against your corpus where that
   would produce a confidently wrong, perfectly faithful answer

---

## Deep track

> Replace word overlap with something better that still needs no model — a sentence-level
> alignment, or overlap weighted by idf so that matching `429` counts for more than matching
> `the`. Measure both on all four generator configurations. Report whether the ordering of
> configurations changes, which is the only claim you are entitled to make.

---

## Log

`logs/stuck-log.md` and `logs/signal-log.md`.
