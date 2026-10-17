# Card-shaped is not a card

*Week 14 · Day 1 · about 25 minutes*

> By the end of this you can explain why a guardrail must be reported with the rate at
> which it fires on the innocent, and why a checksum is a filter, not a proof.

---

## Sources

| Source | Tier | What it gives you |
|---|---|---|
| [**Wikipedia**, Luhn algorithm](https://en.wikipedia.org/wiki/Luhn_algorithm) | 3 | The checksum, worked through |
| [**Stripe**, Testing](https://docs.stripe.com/testing) | 1 | Published test card numbers that cannot be charged |
| [**OWASP**, LLM02: Sensitive information disclosure](https://genai.owasp.org/llmrisk/llm022025-sensitive-information-disclosure/) | 2 | Why personal data in prompts, logs and caches is a disclosure risk |

---

## A guardrail is a classifier

Week 9 made you measure a judge: how often it agrees, how often by chance, how often it
says yes to the wrong thing. A guardrail is a classifier too. It says "this is a card
number" or "it is not", and it is wrong in both directions.

A missed card number ends up in a log, a cache key, a trace. A false alarm redacts an order
reference a person needed, refuses an honest question, and teaches everybody who meets it
to rephrase until it stops firing. Neither error is free. Most guardrails are published
with their catch rate and nothing else.

---

## Three detectors

**A pattern.** Thirteen to nineteen digits, with spaces or dashes allowed between them.
It catches every card number, however it is written. It also catches every long number:
order references, tracking numbers, timestamps, phone numbers run together.

**The Luhn check.** Every card number ends in a check digit. Double every second digit from
the right, subtract nine from anything over nine, add them up: a real card number's total
is divisible by ten. A random number passes about one time in ten — which is the point,
and the problem.

**The issuer.** Real card numbers start with known prefixes for their network and have that
network's length: a 4 and sixteen digits, 51 to 55 and sixteen, 34 or 37 and fifteen.

---

## Measured

Today's stream is the twelve published test cards, and a thousand random sixteen-digit
order references, none of which is a card.

All three detectors catch all twelve cards. On the thousand references, the pattern flags
**all 1,000**. Luhn flags **80**. Luhn and the issuer together flag **18**.

Read that as a support team would: eighteen customers a thousand will have their order
number replaced by `[CARD]` in every reply, every log line and every ticket. That may be
the right trade. It is a trade, and now it has a number.

---

## Redact, do not refuse

A customer who pastes their card number into a question has made a mistake; they have not
asked a bad question. Refusing punishes them for it. The guard **redacts** the number and
answers the rest — and, crucially, does it before anything else touches the text, so the
number never becomes a log line, a cache key or a trace attribute. The milestone's test is
built on exactly that order.

---

## Behind the answer, too

The answer gets a guard as well: it must cite something, it must not cite a chunk the
reader may not see — week 12's filter, applied once more at the last moment — and any card
number in it is redacted. An answer that cited something hidden is not redacted and
returned; it is withheld, because the citation itself tells the reader that the hidden
document exists.
