# Day 3 — Cut where the document says to

> **By the end of today** you can chunk on structure, pack the result into usable sizes,
> and show that it gets the same answers for a quarter of the cost.

---

## Read first

- [ ] [**The document already told you**](../../content/week-04/day-3/the-document-already-told-you.md) — 25 min
- [ ] [**Semantically right, dimensionally useless**](../../content/week-04/day-3/dimensionally-useless.md) — 20 min

---

## Predict first

This corpus has 286 sections. Write down:

1. The **median** section length in words
2. The **shortest** section
3. The **longest**

Then look. The spread is the reason `pack` exists.

---

## The lab

`sections.py`.

```python
heading(line)                       split_sections(text)
section_lengths(documents)          pack(sections, min_words, max_words)
section_corpus(documents, min_words, max_words)
```

Write `heading` and then run it over the corpus and **read what it matched**. The rule that
makes it work here is that RFC body text is indented three spaces and headings are not —
which is a fact about this format, written down nowhere, that you found by reading a
document in week 2.

`split_sections` keeps each heading inside its section body. That is the cheapest useful
thing in the file: a chunk beginning `2.4. Caching` carries its own topic, and a chunk cut
at word 400 does not know what it is about.

Then `pack`, and get the flush order right — both flushes, and the docstring says why.

```bash
pytest week-04/day-3 -v
```

---

## The written exercise

`week-04/day-3/structure.md`, one page.

1. Your three predicted section lengths and the real ones
2. `pack` merges **adjacent** sections. Section 4 and section 5 are different topics, and a
   chunk containing both is less focused than either. Argue for the merge anyway
3. The result: same coverage as 800-word windows, a quarter of the tokens. Which of those
   two numbers would you put in a summary for someone who does not work on retrieval, and
   why
4. **The portability question.** Your `heading` regex works on RFCs. Name three corpora it
   would fail on, and for each say what you would use instead — and whether you could find
   out without reading a document

---

## Deep track

> Sections nest: `2.3.1` lives inside `2.3` lives inside `2`. `split_sections` flattens
> that completely. Build the tree instead, then chunk at whichever depth gives sections
> closest to your target size, per document rather than globally. Measure it against the
> flat version and report whether the extra machinery paid.

---

## Log

`logs/stuck-log.md` and `logs/signal-log.md`.
