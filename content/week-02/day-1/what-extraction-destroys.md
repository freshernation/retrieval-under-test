# What extraction destroys

*Week 2 · Day 1 · about 25 minutes*

> By the end of this you can name four things a format does to text, and say which of them
> a downstream stage can repair and which are gone for good.

---

## Sources

| Source | Tier | What it gives you |
|---|---|---|
| [**RFC 7994**](https://www.rfc-editor.org/rfc/rfc7994.txt) | 1 | The plain-text format's own requirements, including pagination |
| [**RFC 3986**](https://www.rfc-editor.org/rfc/rfc3986.txt) §3 | 1 | The ASCII syntax diagram, as an example of structure that survives as characters and not as meaning |
| [**Docling technical report**](https://arxiv.org/abs/2408.09869) | 1 | A modern layout-aware extractor, and what its authors say it does and does not preserve |

---

## Four kinds of damage

They are worth separating because they have different fixes, and two of them have no fix.

### 1. Insertion — text that nobody wrote

Page footers, running headers, form feeds, `Status of This Memo`, copyright notices,
watermarks, "Confidential — do not distribute" on every page, the navigation menu scraped
along with the article.

**Repairable, and it is the easy one.** Detect it, delete it. About 5% of a paginated RFC
by line count.

The reason it matters is not the 5%. It is that inserted text is *retrievable*: a query
containing "standards" matches a page footer in every document at once, and short documents
are mostly furniture, so the shorter the document the more it is misrepresented by its own
index entry.

### 2. Fragmentation — one thing became two

A sentence cut by a page boundary. A table row split across a column break. A section whose
heading is on one page and whose body is on the next.

**Repairable, but only if you notice**, and the noticing is the hard part. Seventeen
sentences in RFC 3986 are cut in half. Neither half contains the whole rule, both halves
are grammatical-looking, and the metric that would show you this — a retrieval failure on a
query about that rule — will point you at station 4.

The critical subtlety, and it is today's lab: **removing the furniture does not repair the
fragmentation.** Delete the footer and the running header and you are left with the blank
lines that padded the bottom of the page, so the sentence is still two paragraphs. The
damage outlives its cause, and a cleaner that only deletes is a cleaner that leaves every
break exactly where it was.

### 3. Flattening — structure became characters

RFC 3986's syntax diagram:

```
     foo://example.com:8042/over/there?name=ferret#nose
     \_/   \______________/\_________/ \_________/ \__/
      |           |            |            |        |
   scheme     authority       path        query   fragment
```

As a picture, that is a labelled decomposition of a URI. As a string it is a run of
backslashes and underscores followed by five words with no visible relationship to
anything. A table of status codes becomes a run of numbers. A nested list becomes
indentation, which becomes whitespace, which the next stage normalises away.

**Not repairable downstream, and this is the important category.** The relationship was
carried by two-dimensional layout, the layout is gone, and no amount of cleaning
reconstructs it. What you can do is *notice* — mark the document as containing structure
you did not preserve, and put the number in the loss report — so that when a query about
URI components fails, you have somewhere to look other than the ranker.

### 4. Substitution — characters became different characters

A byte-order mark at the start of RFC 9309. Smart quotes becoming `â€œ`. Ligatures. A
non-breaking space that is not the space your tokeniser splits on. Hyphenation inserted at
a line break, so `interoper-` and `ability` are two tokens and `interoperability` is
absent.

**Sometimes repairable, always specific**, and each one is invisible until a particular
query fails. The hyphenation case is the cruellest, because the word the user searched for
does not exist anywhere in your index and no amount of ranking will conjure it.

---

## Which stage each one breaks

This is why the damage types are worth separating.

| Damage | Breaks | Shows up as |
|---|---|---|
| Insertion | station 2, then 4 | short documents matching everything; boilerplate retrieved as an answer |
| Fragmentation | station 2 | a rule that is in the corpus and cannot be retrieved whole |
| Flattening | station 1 | an answer that is *not in the corpus* even though the document is |
| Substitution | station 3 | one query class failing completely, everything else fine |

Flattening is the one to sit with. When a table is destroyed, the information has left the
corpus. The document is present, indexed, and retrievable, and the answer is not in it. No
station downstream can help and the honest thing your system can say is that it does not
know — which requires station 6 to be capable of saying so, which is week 8.

---

## The rule this produces

> **An ingest reports what it lost.**

Not "an ingest logs errors" — an ingest that hits no errors has still lost things. A
manifest, per document, saying how much was removed, how many fragments were healed, how
many structures were flattened and left flat.

Almost no pipeline produces one. The consequence is a specific and very common conversation
six months later, where a user says the system does not know something, and nobody can tell
whether the document is missing, was dropped by the extractor, was extracted into
nonsense, or is present and simply out-ranked. Four completely different problems, and
without a manifest they are indistinguishable from the outside.

---

## Where this is now

Layout-aware extraction has improved substantially — modern tools recover table structure,
reading order and hierarchy from PDFs at a level that was research-grade a few years ago.

Two things have not changed. Their output is still unexamined by the pipelines that consume
it, so a confidently wrong extraction propagates silently. And the flattening category
still exists at the edges: a chart, a diagram, a scanned form, a two-column layout with a
sidebar. What has changed is the *rate*, which means the failures are rarer and therefore
harder to find, which is not obviously an improvement in the ability to trust the corpus.

---

> **Known** — the plain-text RFC format specifies pagination, so page furniture is a
> publishing artefact rather than content (`rfc7994`) · modern layout-aware extractors
> reconstruct table and reading-order structure that earlier tools discarded
> (`docling-2024`)
> **Inferred** — that flattening is the category most often mistaken for a ranking failure.
> Ours, from the shape of the pipeline rather than from a study
> **Derived** — stripping page furniture cannot rejoin a fragmented sentence, because the
> blank lines that separated it are not furniture and remain
> **Unknown** — the relative frequency of these four damage types in real corpora. Every
> number we have seen is from a vendor benchmarking its own extractor
