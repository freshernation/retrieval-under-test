# Day 2 — Citations

> **By the end of today** you can check that a citation points at something real, and you
> will have found a bug in your own checker before you found one in the generator.

---

## Read first

- [ ] [**Two ways a citation fails**](../../content/week-08/day-2/two-ways-a-citation-fails.md) — 25 min
- [ ] [**Your checker's false positives**](../../content/week-08/day-2/checker-false-positives.md) — 20 min

---

## Predict first

The generator emits 39 citations across 20 answers and invents none.

**How many will a naive `[...]` parser report as unresolvable?**

---

## The lab

`cite.py`.

```python
parse_citations(text)      strip_citations(text)     cited_sentences(text)
uncited_sentences(text)    chunk_citations(text, chunks)
unresolvable(citations, chunks)                      not_in_context(citations, context)
citation_report(answers, contexts, chunks)
```

`cited_sentences` has a trap in it. A citation follows the sentence it supports, so it comes
**after** the full stop — and a sentence splitter therefore puts it at the start of the
*next* sentence. Split naively and every citation is attached to the following claim: off by
one for the whole answer, and it produces a support check that is wrong everywhere while
looking fine.

```bash
pytest week-08/day-2 -v
```

---

## The written exercise

`week-08/day-2/citations.md`, one page.

1. Your prediction and the result
2. **The five false positives.** Name them, find one in the corpus, and explain in two
   sentences how a corpus artefact became a model failure in your metrics
3. `chunk_citations` resolves against real ids and makes the number right. Say why that is
   papering over the problem, and what the real fix is
4. The generator's citations are 100% valid and six of its answers are wrong. Write the
   sentence you would use to explain to a stakeholder why "all our answers are cited" is not
   the reassurance it sounds like

---

## Deep track

> Design a citation marker the corpus cannot contain, and change the generator's prompt
> contract to use it. Then measure the false-positive rate again. Then find a corpus where
> your new marker also appears — they exist — and say what that implies about ever solving
> this by choosing a delimiter.

---

## Log

`logs/stuck-log.md` and `logs/signal-log.md`.
