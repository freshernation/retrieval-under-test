# The fact is in a different document

*Week 2 · Day 4 · about 25 minutes*

> By the end of this you can build a supersession graph from metadata, and say why this
> particular failure is unreachable from every station downstream of the corpus.

---

## Read the primary sources first

| Source | Tier | What it gives you |
|---|---|---|
| [**RFC 2026 — The Internet Standards Process**](https://www.rfc-editor.org/rfc/rfc2026.txt) §2.1 | 1 | What "obsoletes" means formally, and the rule that RFCs are never revised |
| [**RFC 7322 — RFC Style Guide**](https://www.rfc-editor.org/rfc/rfc7322.txt) §4 | 1 | The header block, field by field, from the publisher |
| [**RFC 8259**](https://www.rfc-editor.org/rfc/rfc8259.txt) §8.1 | 1 | `MUST be encoded using UTF-8`, and the paragraph saying previous specifications did not require it |

---

## The failure, stated precisely

A user asks whether JSON must be UTF-8. The retriever returns RFC 7159, section 8.1:

> JSON text SHALL be encoded in UTF-8, UTF-16, or UTF-32.

Every stage did its job. The corpus contains the document. The chunk contains the whole
rule. The index found it. The ranker put it first — reasonably, since it is a document
about JSON encoding and the query was about JSON encoding. The generator grounded its
answer faithfully in the retrieved text and cited it correctly.

**The answer is wrong.** The rule was withdrawn in December 2017.

Now walk the stations and ask where the fix goes. Not station 4 — the document is genuinely
about the query. Not station 5 — reordering requires knowing 7159 is worse, and by every
signal available at station 5 it is not. Not station 6 — the generator was faithful, and
"be more careful" is not an instruction anything can follow.

The fix is at station 1, and it is not a retrieval technique at all. It is going and
reading the header.

---

## Why it is unreachable downstream

Because of one property of the standards process:

> **An RFC is never revised after publication.**

RFC 7159 was published in March 2014 and is byte-for-byte what it was then. When RFC 8259
superseded it in 2017, nothing went back and annotated 7159 — that would break the
permanence that makes an RFC citable.

So `Obsoletes: 7159` appears in RFC 8259, and RFC 7159 contains no trace of its own
supersession. Search it for "8259" and you get nothing.

**The information that makes a retrieved passage wrong is not in the passage.** It is not
in the document. It is in a *different document*, one your retriever may not have returned
and may not even contain.

No amount of reading the retrieved text more carefully recovers it. This is the sharpest
example in the course of a failure that is invisible from inside the pipeline, and it
generalises much further than RFCs:

- a retracted paper does not contain its retraction
- a superseded policy does not contain the memo that superseded it
- a resolved ticket's original description still describes the bug as open
- last quarter's pricing page is still a coherent, confident, well-written pricing page

In every case the document is internally consistent and externally false, and the only
defence was built at ingest.

---

## Parsing the header

Three lines from RFC 8259:

```
Internet Engineering Task Force (IETF)                      T. Bray, Ed.
Request for Comments: 8259                                    Textuality
Obsoletes: 7159                                            December 2017
```

Machine-readable, and the lab makes you find out what "machine-readable" means in practice.
Four traps, all in this corpus, all real:

**The layout is not fixed.** The date is right-aligned on the `Request for Comments:` line
in one document, on the `Obsoletes:` line in another, and alone on line 12 in a third.

**Author names share the line.** `Category: Standards Track       G. Illyes` is a category
of "Standards Track". Two-or-more spaces is the column separator, and a `.+$` capture puts
an author's name inside your category field for one document in ten.

**The window is a guess.** RFC 3986 carries `STD`, `Updates` *and* `Obsoletes`, which pushes
its date to line 12. A twelve-line window works on nine documents and loses the date on the
one with the most metadata — the wrong one to lose it on.

**Encoding and format vary.** RFC 9309 begins with a byte-order mark. RFC 2324 dates itself
`1 April 1998`, day first, alone in the corpus.

This is what "just parse the metadata" means. It is an afternoon, it is fiddly, none of it
is intellectually interesting, and it produces the only thing this week that fixes a real
failure. That ratio is characteristic of station 1 work and it is why the work does not get
done.

---

## What to do with the graph

Four options, increasing in strength. The lab builds two.

| Option | What it does | Cost |
|---|---|---|
| **Annotate** | attach `superseded_by` to each result | none. Pushes the decision to station 6 |
| **Demote** | superseded results below current ones | tiny. Can hide a document a query needed |
| **Filter** | drop superseded results | breaks "what changed" queries outright |
| **Rewrite** | prepend a warning to the superseded chunk's text | changes the index; affects matching |

**Demote, do not filter.** The obsolete document is the only answer to *"what did 8259
change"*, and query `r14` in the held-out split needs both halves of the pair. Filtering
trades one failure for another, and the mean might not even notice which is why it is such
an attractive mistake.

And annotate regardless of what else you do. Annotation is nearly free and it is the only
option that lets station 6 say the true thing — *"the current specification says X; an
earlier version said Y"* — which is a better answer than either document alone.

---

## What the numbers will say

Demotion moves ndcg@3 from 0.651 to 0.720, with a 95% interval of [+0.000, +0.125]. The
interval touches zero. **Nothing got worse on any query.**

By the letter of rule 1 you have not measured an improvement. Ship it anyway, and say why:
this is a correctness fix, the defect is nameable without reference to any metric, and the
measurement's job here is to show it cost nothing rather than to justify it. That is
[yesterday's article](../day-2/the-change-you-cannot-prove.md), and this is the clean case
of it.

Twenty percent of this corpus is obsolete. The real question the day leaves you with is
what that number is where you work, and how you would find out.

---

> **Known** — RFCs are never revised after publication, and supersession is declared by the
> newer document (`rfc2026`, `rfc7322`) · RFC 8259 requires UTF-8 and notes that previous
> specifications did not (`rfc8259`)
> **Inferred** — that this class of failure is unreachable from stations 2 to 6. Follows
> from the information not being present in the retrieved text; the framing is ours
> **Derived** — a document that is never edited cannot reference a document published after
> it, so supersession is recoverable only from the newer document
> **Unknown** — what fraction of production corpora carry recoverable currency metadata at
> all. Where the corpus is a shared drive, the answer is often none
