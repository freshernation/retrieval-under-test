# Day 1 — The first answers

> **By the end of today** you can measure the one thing about a generated answer that needs
> no judgment: whether the answer was in the context at all.

---

## Read first

- [ ] [**A search result rewritten into prose**](../../content/week-08/day-1/rewritten-into-prose.md) — 25 min
- [ ] [**The generator is a stipulated model**](../../content/week-08/day-1/a-stipulated-generator.md) — 20 min

---

## Predict first

Twenty dev queries. Two of them nothing retrieves; one the corpus cannot answer.

1. **How many will the system refuse?**
2. **How many answers will be confidently wrong?**

---

## The lab

`ground.py`.

```python
answer_all(generator, queries, build_context)     answer_in_context(query, context)
response_rate(answers)                            grounded_rate(answers, queries, contexts)
confidently_wrong(answers, queries, contexts)     report(answers, queries, contexts)
```

`grounded_rate` divides by **every** query, not by the answered ones. Dividing by the
answered ones is how a system that refuses hard queries reports a higher score for answering
fewer of them.

Then **read the six answers in `confidently_wrong`.** All of them. That is the exercise, and
the numbers are the excuse for it.

```bash
pytest week-08/day-1 -v
```

---

## The written exercise

`week-08/day-1/first-answers.md`, one page.

1. Your two predictions and the results
2. **Paste the answer to `r19`** — *how do I stop search engines indexing my site* — in
   full. Then write two sentences on what a user would do with it
3. Six answers are confidently wrong. Two have been unreachable since week 6. What are the
   other four, and why did nobody notice them before this week?
4. Write down the tell — anything in the text that distinguishes a wrong answer from a right
   one. If you cannot find one, say so, and say what that implies about reviewing answers by
   hand

---

## Deep track

> `grounded_rate` uses answer spans, which exist only offline. Write down every metric this
> week will produce and mark each one **available at serving time** or **not**. The list of
> things you cannot measure in production is short, and it is the reason week 9 exists.

---

## Log

`logs/stuck-log.md` and `logs/signal-log.md`.
