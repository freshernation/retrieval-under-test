# The document already told you

*Week 4 · Day 3 · about 25 minutes*

> By the end of this you can chunk on a document's own boundaries, and say what that buys
> and what it assumes.

---

## Sources

| Source | Tier | What it gives you |
|---|---|---|
| [**RFC 7322 — RFC Style Guide**](https://www.rfc-editor.org/rfc/rfc7322.txt) §4 | 1 | The section numbering and heading conventions this week's regex depends on |
| [**Docling technical report**](https://arxiv.org/abs/2408.09869) | 1 | A modern extractor whose output *is* a structure tree, and what it recovers |
| [**RFC 7994**](https://www.rfc-editor.org/rfc/rfc7994.txt) | 1 | What survives into the plain-text rendering, and what does not |

---

## A fixed window is a decision made with no information

Cut every 400 words. Why 400? No reason. Why *there*? No reason — that is just where 400
words happened to end.

Meanwhile the document contains an explicit, authored, machine-readable statement of where
its ideas begin and end. It is called a heading, the author put it there deliberately, and
extracting it costs one regex.

```python
HEADING = re.compile(r"^(\d+(?:\.\d+)*)\.?\s+(\S.*)$")
```

That is the whole technique. Everything else today is dealing with the consequences.

---

## Keep the heading in the chunk

The cheapest useful thing in the file, and it is one line.

A chunk beginning `2.4. Caching` carries its own topic. A query about caching matches it on
the heading alone, before any of the body has been considered. A chunk cut at word 400 does
not know what it is about, and neither does the retriever.

This also matters at station 6. A chunk that says `2.4. Caching` can be cited as *section
2.4* rather than as *part of a document*, and week 8's citations get sharper for free
because of a decision made in week 4.

---

## What it assumes, and how you found out

The regex works because **RFC body text is indented three spaces and headings are not**.
Without the `^` anchor it would match `2.3.1 is where this is defined` in the middle of a
paragraph and shatter the document.

That fact is written down nowhere. It is not in RFC 7322, which specifies the numbering but
not the indentation of body text. You know it because you read a document in week 2.

**Every corpus has an equivalent fact and none of them are documented.** Markdown uses `#`.
HTML uses `<h2>`, unless the author styled a `<p>` to look like a heading, which they did.
A Word export uses a style name that survived conversion, or did not. A scanned PDF has
headings that are only bold and larger, which is a visual property and gone after
extraction.

So structure-aware chunking is **not a technique you can apply without reading the corpus**,
and that is its real cost. It is also why it is not the default in tools: a tool cannot know
your corpus's undocumented fact, so it ships a fixed window, which works badly everywhere
rather than well somewhere.

---

## Structure that did not survive

Week 2's flattening category returns.

RFC 3986's ASCII syntax diagram is structure carried by two-dimensional layout, and after
extraction it is a run of backslashes. No heading regex recovers it, and neither does
anything else.

Modern layout-aware extractors are much better at this — they emit a structure tree rather
than a string, which makes chunking a tree traversal rather than a regex — and it is worth
knowing that the whole of today's work is *reconstructing* something a better extractor
would have handed you.

If you control ingestion, that is the leverage: **structure preserved at extraction is worth
more than structure recovered later**, because recovery only works where the format left
enough evidence.

---

## Where this stops working

Be clear about the boundary, because it is closer than it looks.

**Documents with no structure.** Support tickets, chat logs, transcripts, emails. There is
nothing to cut on and the fallback is a fixed window.

**Documents whose structure is wrong for retrieval.** A legal contract's sections are
numbered and meaningful and can be forty pages, or one sentence. Structure tells you where
the boundaries are and nothing about whether they are the right *size*, which is the next
article.

**Documents where structure is decorative.** A marketing page's headings are chosen for
rhythm, not for topic decomposition.

The honest summary: structure-aware chunking is the best available option **when the
structure means what you hope it means**, and checking that is a corpus-reading job rather
than a code job.

---

> **Known** — RFC section numbering and heading conventions are specified by the publisher
> (`rfc7322`) · the plain-text rendering preserves some structure and discards other
> structure (`rfc7994`) · modern layout-aware extractors emit structure trees rather than
> flat text (`docling-2024`)
> **Inferred** — that structure-aware chunking cannot be applied without reading the corpus,
> because the rule distinguishing a heading from prose is format-specific and undocumented.
> Ours, from this corpus and from experience
> **Derived** — an unanchored heading pattern matches numbered references inside body text,
> so anchoring is required wherever body text can begin with a number
> **Unknown** — how much better tree-based chunking from a layout-aware extractor is than
> regex recovery from flat text. We would expect a lot and have not measured it
