# Open the file

*Week 2 · Day 1 · about 20 minutes*

> By the end of this you will have read a document in your own corpus end to end, which
> puts you ahead of most people who have shipped a retrieval system.

---

## Sources

| Source | Tier | What it gives you |
|---|---|---|
| [**RFC 7725**](https://www.rfc-editor.org/rfc/rfc7725.txt) | 1 | Four pages. Read it |
| [**RFC 7994 — Requirements for Plain-Text RFCs**](https://www.rfc-editor.org/rfc/rfc7994.txt) | 1 | The publisher, on the record, about what the plain-text format is and is not for |
| [**RFC 8650 / the RFC format series**](https://www.rfc-editor.org/rfc/rfc7990.txt) | 1 | Why documents after 2019 look different from documents before it |

> The argument of this article — that reading the corpus is a distinct and skippable
> activity that almost everyone skips — is ours.

---

## The instruction

Stop. Open `rfc-7725` and read it, all of it, in the terminal.

```bash
python3 -c "import raglab; print(raglab.corpus.load()['rfc-7725'].text)"
```

Six minutes. Nothing in this course pays back faster, and there is a specific reason it
has to be an instruction rather than a suggestion: **reading the corpus is not a step in
any workflow.** Ingest has a step. Chunking has a step. Evaluation has a step. Looking at
what you are actually indexing appears in no diagram, has no library, produces no artefact
and cannot be scheduled, so it does not happen — and then a system is built on top of text
nobody has ever seen.

---

## What you are looking for

Everything in the string that **nobody wrote**.

A document is authored content plus the residue of the machinery that published it, and a
retriever cannot tell the two apart. Every character in the file is a character it will
match a query against.

In this file:

- a **form feed** (`\f`), five of them, one per page boundary
- a **page footer** on every page: `Nottingham                Standards Track           [Page 1]`
- a **running header** on every page: `RFC 7725     HTTP-status-451     February 2016`
- **blank lines padding** the bottom of each page to reach the footer
- a **`Status of This Memo`** section that appears in nine of your ten documents
- a **copyright notice** that appears in all ten
- a **table of contents** listing section names that then appear again as real headings

Now count: this is a four-page document, and about one line in seven of it is text it
shares verbatim with other documents in the corpus. On the 141 KB document that ratio is
one line in five hundred.

**Boilerplate is a fixed cost per document.** It is a rounding error on long documents and
a catastrophe on short ones, and the corpus average — the number you would naturally
report — is somewhere in between and describes neither.

---

## Then open the other one

```bash
python3 -c "import raglab; print(raglab.corpus.load()['rfc-9309'].text[:2000])"
```

No form feeds. No page footers. No running headers.

RFC 9309 was published in 2022, after the RFC series moved to a format where the plain-text
rendering is generated rather than authored, and the pagination went away. Same publisher,
same series, same file extension, same `.txt` URL. One in ten of your documents, in a
different format, announced by nothing.

**This is what "our corpus is homogeneous" always means in practice.** Not that the corpus
is homogeneous, but that nobody has checked which parts of it are not. Every cleaner you
write today will silently do nothing to this document, complete successfully, and report a
count of zero problems fixed — which is indistinguishable, in a log, from a document that
had no problems.

---

## The habit

Before you index anything, ever:

1. **Read one document end to end.** The shortest one
2. **Read the one that looks weird.** File size histogram, pick both tails
3. **Diff two documents that should be similar.** The shared parts are the boilerplate and
   you did not have to define what boilerplate means
4. **Count what you found**, per document, before you fix any of it

Step four is today's lab and it is the one people skip even when they do the first three,
because once you have seen the problem the urge to fix it is enormous. A repair whose size
you did not measure first is a change you cannot defend, and by Friday you will have made
two of them and been unable to prove either.

---

## Why not just clean everything aggressively

Because you do not know what is furniture until you have looked, and the cost of being
wrong is asymmetric and invisible.

A cleaner that deletes every line beginning with `RFC` removes the running headers. It also
removes every line of prose that happens to begin with a citation — and `RFC 2119` opens
sentences constantly in this corpus. You will not notice. There is no error, no log line,
no failing test; there is just a slightly smaller document with a hole in it, and a query
six months from now that returns nothing.

**Every aggressive cleaning rule has a false-positive class, and it is always invisible.**
The only defence is to look at what your rule matched before you let it delete anything,
which takes ten minutes and which almost nobody does.

---

## Where this is now

Document extraction is a mature field with excellent tools, and the tools are not the
problem. The problem is that the tools' output is the input to everything downstream and
is inspected by nobody — a PDF parser will happily return a page of extracted text with the
table silently transposed, and the pipeline around it has no notion that the output could
be wrong, only that it could be missing.

The current generation of layout-aware extractors is genuinely much better than what came
before. It has not changed the shape of this problem at all, because the failure was never
that extraction was bad; it was that its output was unexamined.

---

> **Known** — the RFC series moved to a new format process, which is why documents after
> roughly 2019 render without pagination (`rfc-format-series`) · the plain-text rendering
> is a *rendering*, with the pagination as a publishing artefact (`rfc7994`)
> **Inferred** — that reading the corpus is skipped because it is not a step in any
> pipeline. Teaching experience, not a measured claim
> **Derived** — boilerplate is a fixed number of lines per document, so its share of a
> document falls as the document lengthens, and a corpus average describes no document
> **Unknown** — what fraction of production retrieval systems have had any document read
> end to end by anyone. We would very much like this number
