# Day 2 — The failure library

> **By the end of today** your library is smaller than it was this morning, and every card
> left in it would help somebody on a corpus you have never seen.

**No lab.**

---

## Read first

- [ ] [**What makes a card transfer**](../../content/week-12/day-2/what-makes-a-card-transfer.md) — 25 min
- [ ] [**Thirty cards, and the twelve that matter**](../../content/week-12/day-2/the-twelve-that-matter.md) — 20 min

---

## Predict first

**How many of your cards would help on a corpus you have never seen?** A number, out of
however many you have.

Most people guess two thirds. It is usually under half.

---

## The work

### 1 · The card, and its six fields

> the failure · the station it belongs to · the diagnostic that finds it · the fix ·
> the measured delta · **the conditions under which the fix stops working**

The sixth field is the one left blank, and it is the one that makes a card transferable. A
card without it says *"this worked for me"*. A card with it says *"this works when, and here
is how you check"*, which is the difference between a note and a method.

### 2 · The edit

For each card, apply the test:

**Would this help somebody on a corpus they have never read?**

- **Yes** → keep it. It is about a mechanism
- **No, it is about this corpus** → keep it *only* if you can rewrite the failure as a class.
  *"RFC 7159 does not know it is obsolete"* is about this corpus. *"The fact that disqualifies
  an answer can live in a document the answer did not come from"* is about every corpus
- **No, it is about a bug I fixed** → delete it. A bug is not a failure mode

Expect to delete a third and to rewrite a third.

### 3 · The ones you cannot write

Make a short list of failures you **know** exist and have no card for, because you could not
diagnose them. Correctness is on it. That list is the honest boundary of the library and it
belongs in the front of it, not the back.

---

## The written exercise

`week-12/day-2/library.md`.

1. Your predicted transferable count and the actual one
2. The cards you deleted, with one line each on why
3. **Two cards rewritten from corpus-specific to general**, before and after
4. The list of failures you cannot card, and for each one the evidence you would need

---

## Deep track

> Take the three cards you are most confident in and write the **falsifying condition** for
> each: the measurement that would show the card wrong. If you cannot write one, the card is
> an opinion with a number attached. This is the hardest hour in week 12 and it is the one
> that determines whether the library is a portfolio or a method.

---

## Log

`logs/stuck-log.md` and `logs/signal-log.md`.
