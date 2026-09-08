# Cleaning a corpus

*Week 2 · Day 2 · about 25 minutes*

> By the end of this you can write a cleaner whose false positives you have looked at, and
> you will know why the order of its stages is not arbitrary.

---

## Sources

| Source | Tier | What it gives you |
|---|---|---|
| [**RFC 7994**](https://www.rfc-editor.org/rfc/rfc7994.txt) | 1 | What in the plain-text format is publishing furniture and what is content |
| [**Common Crawl / CCNet cleaning pipelines**](https://arxiv.org/abs/1911.00359) | 1 | Corpus cleaning at web scale, with the heuristics written down and their effects measured |
| [**Docling technical report**](https://arxiv.org/abs/2408.09869) | 1 | What a modern extractor considers structure worth preserving |

---

## Every rule has an invisible false-positive class

This is the whole article and the rest is detail.

`^RFC \d+` matches every running header in the corpus. It also matches every line of prose
that begins with a citation, and this corpus is full of sentences that open `RFC 2119
defines…`. Delete on that rule and you remove real content, silently, with no error and no
log line, leaving a document that is very slightly wrong in a way nothing will surface
until a query fails months later.

The fix is not a cleverer regex. It is a habit:

> **Print what your rule matched before you let it delete anything.**

Ten minutes. Look at the matches, find the class you did not intend, tighten the rule,
look again. On this corpus the tightening is requiring a month name at the end of the line
— headers have one, citations do not.

Nobody does this, and the reason is that a cleaning rule *feels* verifiable in a way it is
not: you can see that it removed the footers. You cannot see what else it removed, because
what else it removed is no longer there.

---

## Order of operations

Four stages, and three of the orderings are wrong.

1. **Strip furniture** — footers, headers, form feeds
2. **Strip front matter** — the metadata block, abstract, status, copyright, contents
3. **Heal page splits** — rejoin sentences the pagination cut in half
4. **Reflow** — collapse blank runs, join paragraph lines

Why this order:

- **Reflow cannot come first.** Joining lines before stripping welds a page footer onto
  the end of a sentence. Once `…persists in identifying the same resource over time
  Berners-Lee, et al. Standards Track [Page 5]` is one line, the footer is inside a
  sentence, and every rule that would have recognised it as a footer no longer applies. The
  damage becomes unrecoverable *because of your own cleaner*
- **Healing must come after stripping** — the split is only visible once the furniture
  between the two halves is gone
- **Healing must come before reflow** — reflow treats a blank line as a paragraph boundary,
  so a split that has not been healed is permanently two paragraphs

The general principle, and it transfers: **destructive stages go last, and detection stages
go before the thing they detect is destroyed.** Almost every cleaning bug is a violation of
that sentence.

---

## Healing is not stripping

The trap in today's lab, and it is worth stating plainly because it is not obvious.

Removing the page furniture does not repair the sentence it interrupted. What is left is:

```
   …though that is a common goal of all URI schemes.  Nevertheless, nothing in this

specification prevents an application from limiting itself to particular…
```

The footer is gone. The header is gone. The blank lines that padded the bottom of that page
are still there, and a blank line means paragraph break. So the sentence is still two
paragraphs, will still chunk into two pieces in week 4, and will still retrieve as two
fragments neither of which contains the rule.

**The damage outlives the thing that caused it.** A cleaner that only deletes is a cleaner
that leaves every fragmentation exactly where it was, while reporting that it removed 5% of
the lines and succeeded.

Healing needs a *heuristic*, not a pattern: a blank run whose preceding line does not end a
sentence and whose following line begins in lower case is pagination rather than a
paragraph break. That is a guess. It has false positives — a bulleted list of lower-case
fragments will be welded together — and the honest thing is to write down which way you
erred and why, because there is no rule here that is simply correct.

---

## What you throw away on purpose

`strip_front_matter` deletes the abstract.

An abstract is frequently the best one-paragraph summary of a document in existence,
written by the author, specifically to be read on its own. You are deleting it in order to
delete the copyright notice next to it.

That is a **trade**, and the point is not that it is the wrong trade — it is probably the
right one — but that it should appear in the loss report as a trade rather than as a
cleanup. A pipeline in which valuable content is discarded as a side effect of removing
boilerplate, with no record, is a pipeline where nobody can later ask whether it was worth
it.

Write it down. That is what a manifest is for.

---

## What cleaning is worth

Here is where the article stops being about technique.

You are about to remove between 18% and 39% of every document in the corpus, and **recall@3
will not move at all.** Not approximately: the numbers are identical.

The reason is mechanical and worth understanding rather than being surprised by. At
whole-document granularity, a query matches a document if the document contains the query's
terms *anywhere*. Boilerplate adds terms; it rarely removes the ones that mattered; and
with ten documents there is enough signal that the furniture was never what decided the
ranking. Cleaning removed noise from a channel that had plenty of margin.

This changes completely in week 4, when the unit of retrieval stops being a document. A
400-token chunk of a four-page RFC can be *entirely* copyright notice, and then boilerplate
is not noise on the channel — it is a whole result.

**So cleaning is right, and this week cannot prove it.** Holding that thought for two weeks
without either abandoning the change or pretending you proved it is the discipline the
course is for, and tomorrow gives you a second, different reason to believe it.

---

> **Known** — corpus cleaning heuristics at web scale are published with their effects
> measured, and are heuristics rather than rules (`ccnet-2019`) · the plain-text format's
> pagination is a publishing artefact (`rfc7994`)
> **Inferred** — that "destructive stages last" prevents most cleaning bugs. Ours, from the
> failure modes rather than from a study
> **Derived** — joining lines before stripping furniture makes the furniture part of a
> sentence, after which no line-oriented rule can recognise it
> **Unknown** — how often production ingest pipelines inspect what their cleaning rules
> matched. We have never seen it measured, or, anecdotally, done
