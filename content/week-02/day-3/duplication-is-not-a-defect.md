# Duplication is not a defect

*Week 2 · Day 3 · about 20 minutes*

> By the end of this you can say why the reflex to delete a near-duplicate is wrong here,
> and you will have hit the wall that tomorrow exists to get over.

---

## Sources

| Source | Tier | What it gives you |
|---|---|---|
| [**RFC 8259**](https://www.rfc-editor.org/rfc/rfc8259.txt) header | 1 | `Obsoletes: 7159`, in the document itself |
| [**RFC 2026 — The Internet Standards Process**](https://www.rfc-editor.org/rfc/rfc2026.txt) §2.1 | 1 | What "obsoletes" formally means, and why an RFC is never edited |

---

## The reflex

You find two documents 55% identical. The reflex is to delete one, and it is a good reflex
in most corpora — a mirrored page, a re-uploaded attachment, the same press release on
three subdomains. Duplication wastes index, splits evidence, and fills context windows.

Here it is wrong in both directions, and working out why is the day.

**Delete RFC 7159**, the older JSON spec, and you lose the ability to answer *"what did RFC
8259 change about JSON?"* — which is query `r14` in your own held-out split, which needs
both documents because neither contains the comparison. You would not find out for weeks.

**Delete RFC 8259**, the newer one, and your corpus now confidently returns a rule that was
withdrawn in 2017.

The two documents are not redundant. They are a **version history**, and a version history
is information.

---

## What kind of relationship is this

Say it precisely, because the precision is what makes tomorrow possible.

RFC 8259 **obsoletes** RFC 7159. That is a formal relationship in the IETF standards
process: the newer document replaces the older as the definitive specification, and the
older remains published, permanently, because the standards process does not delete things.
RFC 8615 obsoletes RFC 5785 in exactly the same way.

Two instances of one relationship. And:

| Pair | Jaccard |
|---|---|
| RFC 7159 / RFC 8259 | **0.547** |
| RFC 5785 / RFC 8615 | **0.185** |

Nearly a factor of three apart. Set your threshold at 0.5 and you catch the first and miss
the second. Set it at 0.15 and you catch both — along with, on any real corpus, an enormous
amount of noise.

**There is no threshold.** Not "the threshold is hard to tune": there is no value of a
similarity score that identifies this relationship, because the relationship is not a fact
about the text.

Two documents can be nearly identical and unrelated. Two documents can be 18% similar and
one can formally replace the other. The similarity measures how much text they share; the
relationship is about *authority*, and authority is not written in the prose.

---

## Where it is written

It is written down. It has been sitting in your corpus since Monday.

```
Internet Engineering Task Force (IETF)                      T. Bray, Ed.
Request for Comments: 8259                                    Textuality
Obsoletes: 7159                                            December 2017
```

Three lines from the top of RFC 8259. Unambiguous, machine-readable, and put there
deliberately by the publisher for exactly this purpose.

That is tomorrow. The point of today ending here, at a wall, is that **you should feel the
wall** — you have a real question, you have applied the standard technique properly, and
the technique cannot answer it. The answer is not a better similarity measure. The answer
is metadata, and metadata comes from reading the corpus rather than from processing it.

---

## The direction the fact points

One detail decides the shape of tomorrow's code, and it is worth noticing now.

**RFC 7159 contains no mention of RFC 8259.** It cannot: an RFC is never edited after
publication, which is a deliberate property of the standards process — a published document
is a fixed, citable artefact for ever. When 8259 was published in 2017, nothing went back
and annotated 7159.

So the supersession graph is built entirely from the *newer* document's header, and:

> **The fact that makes a retrieved passage wrong lives in a different document.**

Sit with that, because it generalises far past RFCs. A retracted paper does not contain its
retraction. A superseded policy does not contain the memo that superseded it. A deprecated
API's documentation page usually does say so — but only because somebody remembered to edit
it, and in most corpora nobody does.

Your retriever returns a passage. The passage is internally consistent, well written,
authoritative in tone, and wrong. **Nothing in it can warn you.** Nothing in it will ever
warn you. The warning is somewhere else, and the only way to get it is to have gone and
built the relationship at ingest time.

That is station 1's strongest argument, and it is why this course spends a week on the
corpus before it spends a day on the ranker.

---

## When deletion *is* right

To be fair to the reflex, because it is usually right:

- **Exact duplicates** — same content, different id. Delete, keep one, record the alias
- **Mirrors** — same document at three URLs. Keep the canonical, record the others
- **Format variants** — the PDF and the HTML of the same thing. Keep the better extraction
- **Chunks that overlap by construction** — week 4's problem, not this one

What these share is that **nothing is lost**. Version history is not on the list, because
something is.

The test to apply: *can I write a query, right now, that only the document I am about to
delete can answer?* For `r14`, you can. That is the end of the argument.

---

> **Known** — "obsoletes" is a formal relationship in the IETF standards process, and
> published RFCs are never edited (`rfc2026`) · RFC 8259's header declares it obsoletes
> 7159 (`rfc8259`)
> **Inferred** — that no similarity threshold can identify supersession in general. Shown
> here by two instances differing by a factor of three; the general claim is ours
> **Derived** — since an RFC is never edited, a superseded document cannot contain a
> reference to the document that superseded it, so the relationship is only recoverable
> from the newer one
> **Unknown** — how often production retrieval corpora contain superseded documents with no
> supersession metadata. Anecdotally it is the common case and we have no measurement
