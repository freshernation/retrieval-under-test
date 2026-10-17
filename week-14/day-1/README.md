# Day 1 — Guardrails, measured

> **By the end of today** you can guard a query and an answer for card numbers and email
> addresses, and say how often each guard fires on something innocent.

---

## Read first

- [ ] [**Card-shaped is not a card**](../../content/week-14/day-1/card-shaped-is-not-a-card.md) — 25 min

---

## Predict first

1,000 random sixteen-digit order references. None is a card.

**How many does a card-number pattern flag? The Luhn check? Luhn and the issuer?**

---

## The lab

`guardrails.py`.

```python
digits(text)   luhn(number)   issuer(number)
pattern_cards(text)   luhn_cards(text)   cards(text)
redact(text)   guard_query(text, max_chars)   guard_answer(answer, cited, allowed)
```

```bash
pytest week-14/day-1 -v
```

---

## The written exercise

`week-14/day-1/guardrails.md`, one page.

1. Your predictions, and the answers
2. Why does Luhn let one random number in ten through? Show it
3. The 18 that pass Luhn and an issuer: what would stop them, and what would that cost?
4. Why is a card number in a question a reason to redact rather than refuse?
