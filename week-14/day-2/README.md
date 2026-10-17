# Day 2 — A cache that answers similar questions

> **By the end of today** a cache answers paraphrases from earlier answers, and refuses to
> answer a question that differs only in a number.

---

## Read first

- [ ] [**Similar is not the same question**](../../content/week-14/day-2/similar-is-not-the-same-question.md) — 20 min

---

## Predict first

"What does section 3.2 of RFC 3986 define" and "what does section 3.4 of RFC 3986 define".

**How similar are they, by week 5's embedding — more or less than a real paraphrase?**

---

## The lab

`semcache.py`.

```python
embedder(retriever)   identifiers(text)
SemanticCache(embed, threshold, guard_identifiers=True)  .put  .get
sweep(pairs, embed, thresholds, guard_identifiers)
```

```bash
pytest week-14/day-2 -v
```

---

## The written exercise

`week-14/day-2/semcache.md`, one page.

1. Your prediction, and the answer
2. The sweep table, both ways. Which threshold would you ship, and why?
3. Write a near miss the identifier guard does not catch
4. Week 12's cache leaked across readers. Where is that leak closed here?
