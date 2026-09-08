# Day 4 — Provenance, and a fix retrieval could not have made

> **By the end of today** you can stop a withdrawn specification from outranking its
> replacement, and you can say exactly why no amount of retrieval work would have done it.

---

## Read first

- [ ] [**The fact is in a different document**](../../content/week-02/day-4/the-fact-is-in-a-different-document.md) — 25 min
- [ ] [**Currency, and what a corpus owes its reader**](../../content/week-02/day-4/currency.md) — 25 min

---

## Predict first

Yesterday ended at a wall: two pairs, same relationship, similarities of 0.547 and 0.185,
and no threshold separating that relationship from coincidence.

**Where is the relationship written down?** Answer before you read on. It is written down,
and you have had it since Monday.

---

## The lab

`lineage.py`.

```python
parse_header(text)                       supersession(documents)
is_current(doc_id, graph)                current_version(doc_id, graph)
annotate(ranked, graph)                  demote_superseded(ranked, graph)
```

`parse_header` is the whole morning and it is deliberately fiddly, because "just parse the
header" is a sentence people say about real corpora and this is what it means. Four traps,
all real, all in the docstring. The one that will get you is the header window: RFC 3986
carries `STD`, `Updates` *and* `Obsoletes`, which pushes its date to line 12.

Then `supersession`, and notice where the fact comes from — the **newer** document. RFC
7159 will never mention RFC 8259, because an RFC is never edited after publication.

Then `test_the_obsolete_json_spec_stops_outranking_the_current_one`, which is the week's
headline, and the last two tests, which are the week's actual lesson.

```bash
pytest week-02/day-4 -v
```

---

## The written exercise

`week-02/day-4/currency.md`, one page.

1. The supersession graph, and the two-sentence argument for why similarity could not have
   produced it
2. **The demotion changes ndcg@3 from 0.651 to 0.720, with an interval of
   [+0.000, +0.125].** Would you ship it? Answer in a paragraph, and the paragraph must
   contain the phrase "correctness" or explain why it does not
3. `demote_superseded` moves stale results down. Name two other things you could do
   instead — one weaker, one stronger — and say what each would cost
4. Your corpus has ten documents and two are obsolete. **Twenty percent.** What is that
   number on a corpus you have worked with, and how would you find out?

Question 4 is the one to bring to Friday.

---

## Deep track

> Supersession is a graph and this corpus gives you two edges of length one. Real chains
> are longer: 4627 → 7158 → 7159 → 8259. Extend `lineage` to load the full RFC index,
> build the whole graph, and answer — for the ten documents you have, how many are
> obsolete *transitively* by documents you do not have? Then say what that implies about a
> corpus assembled by downloading what somebody linked to.

---

## Log

`logs/stuck-log.md` and `logs/signal-log.md`.
