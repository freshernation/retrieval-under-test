# Day 1 — The analyzer, and its limits

> **By the end of today** you can build a configurable analyzer, and you can say why the
> two classic improvements it offers do not work.

---

## Read first

- [ ] [**What a term is**](../../content/week-03/day-1/what-a-term-is.md) — 25 min
- [ ] [**Throwing information away in advance**](../../content/week-03/day-1/throwing-information-away.md) — 25 min

---

## Predict first

You are about to remove stopwords and then apply a stemmer. Write down, for each:

1. What will recall@3 do? A number, with a sign.
2. How confident are you, 1 to 5?

Most people write +0.05 to +0.15 for stopwords. Keep the paper until Wednesday.

---

## The lab

`analyzer.py`.

```python
split_terms(text)          keep_identifiers(text)      remove_stopwords(tokens)
stem(token)                stem_all(tokens)            analyze(text, **options)
vocabulary(documents)      document_frequency(documents)
```

Write `document_frequency` before you write anything clever, and print it for the terms in
query `r01` — *what status code should I return when a client sends too many requests*.
`status` is in 10 documents out of 10. `code` is in 10. `429`, which is the answer, is in
1, and the user did not type it.

Then run `test_removing_stopwords_does_not_help` and
`test_stemming_actively_breaks_two_queries`.

```bash
pytest week-03/day-1 -v
```

---

## The written exercise

`week-03/day-1/analysis.md`, one page.

1. Your predictions and the actual numbers
2. `stem` over the corpus vocabulary. Find **five** terms it damages. `status` → `statu`
   and `cookies` → `cooky` are two; find three more, and say what each would cost
3. A stemmer exists to make `cache` match `caching`. On this corpus it does not — one
   strips to `cach` and the other keeps its `e`. Would a real stemmer fix that, and what
   would you have to check to find out?
4. **The paragraph that matters.** Keeping identifiers helps; stopwords and stemming do
   not. State the general principle in one sentence, and then say what it predicts about a
   technique you have not met yet

Question 4's answer is roughly *changes that add information are safer than changes that
discard it*, and you should arrive at it yourself before Wednesday makes it obvious.

---

## Deep track

> Build a stopword list *from the corpus* — the top N terms by document frequency, rather
> than the fixed English list — and sweep N from 0 to 200 against recall@3. You are
> hand-rolling a crude version of what Wednesday does properly. Find the N that helps
> most, then compare it against Wednesday's BM25 result and say what the gap is made of.

---

## Log

`logs/stuck-log.md` and `logs/signal-log.md`.
