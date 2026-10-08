# Query drift

*Week 11 · Day 1 · about 20 minutes*

> By the end of this you can explain why pseudo-relevance feedback cannot fix a query it
> did not already half-answer.

---

## Sources

| Source | Tier | What it gives you |
|---|---|---|
| [**Xu & Croft**, local and global document analysis](https://doi.org/10.1145/243199.243202) | 1 | Expansion from local feedback, and where it goes wrong |
| [**Lavrenko & Croft**](https://doi.org/10.1145/383952.383972) | 1 | The assumption stated plainly: the top documents are relevant |

---

## The assumption, and what happens when it fails

Pseudo-relevance feedback is sound and it is old. The premise: the documents you retrieved
are probably about the right thing, so their vocabulary is probably useful. Harvest their
distinctive terms, add them to the query, retrieve again.

The premise is doing all the work. If the first retrieval was about the right thing, the
feedback sharpens it. If the first retrieval was wrong, the feedback comes from the wrong
documents — and the second retrieval is wrong **with more conviction**, because it is now
anchored by terms drawn from those documents.

That is called query drift, and it has been documented since the nineties. It is not a
subtle effect and it is visible here in one table.

---

## What the feedback actually contains

| query | feedback terms |
|---|---|
| `r19` *how do I stop search engines indexing my site* | `web accessed their sites rec` |
| `r20` *what part of a web address comes after the hash* | `literal brackets does found report` |
| `r06` *what does ABNF stand for* | `generic et al berners lee` |
| `r04` *what does the 418 status code mean* | `codes head 6585 2012 body` |
| `r21` *how does a server remember a visitor between page loads* | `requests response cookies cookie even` |
| `r23` *what is a name value pair in JSON called* | `string objects array pairs object` |

Read the last two first. `r21` gets `cookies` and `cookie`; `r23` gets `object`, `objects`,
`pairs`, `string`, `array`. Those are the two queries the expansion **gains**, and the
feedback is exactly what a person would have added.

Now read the first four.

`r19` gets `their` — a stopword — and `rec`, a word fragment, and `sites`, which is the
query's own word with an s. Nothing that bridges to `crawler` or `disallow`. The first
retrieval did not contain the answer, so the feedback cannot contain the vocabulary of the
answer. **There is no mechanism by which it could.**

`r06` gets `generic et al berners lee`: the bibliography. `r04` gets `6585` and `2012`,
which drag in the *other* status-code RFC — an expansion that actively moves the query away
from RFC 2324.

---

## The shape of the limitation

Pseudo-relevance feedback is a **refinement** operator. It can sharpen a query that is
pointing in roughly the right direction. It cannot rotate one that is pointing the wrong
way, because everything it knows comes from where the query was already pointing.

So the queries it helps are the ones that were nearly working, and the queries you wanted
it for are the ones it cannot reach. That is not bad luck; it is the operator's definition.
Any technique whose input is the previous output has this property, and you will meet it
again on Thursday, with a loop.

Which gives you a cheap test before building any feedback mechanism: **did the first
retrieval contain anything relevant at all?** If the answer for your worst queries is no,
feedback is the wrong tool and the headroom you are chasing is at a different station.

---

## What would work, and why the course cannot show you

The gap at `r19` is lexical: `search engines` against `crawler`. Three things could bridge
it.

- **A synonym resource built from outside the eval set** — a thesaurus, a query log, a
  taxonomy. Legitimate, and this course has none that is not the corpus
- **A better representation** — week 5's LSA has a shot at it in principle and does not
  manage it here; a real embedding model might. Untested, and the honest statement is that
  it is untested
- **A model-written rewrite** — a generator asked to produce alternative phrasings. This is
  what everybody does and it is the one thing in this week the course cannot run

So the honest finding is narrow and it is worth stating narrowly: **on this corpus,
corpus-derived feedback does not move the paraphrase family, and the mechanism explains
why.** Whether a model does is the first experiment to run with an API key, and the
machinery to measure it is already written.

---

> **Known** — expansion from local feedback improves retrieval when the feedback documents
> are relevant, and degrades it when they are not (`xu-croft-1996`) ·
> pseudo-relevance feedback assumes the top-ranked documents are relevant
> (`lavrenko-croft-2001`)
> **Inferred** — that feedback is a refinement operator and cannot redirect a query that was
> pointing the wrong way, because its entire input is the previous retrieval. Ours, and the
> same shape as week 11 day 4's loop
> **Inferred** — that *did the first retrieval contain anything relevant* is the cheap test
> to run before building any feedback mechanism. Ours
> **Derived** — the feedback terms for the two targeted queries contain a stopword and a
> word fragment and no term from the answering vocabulary, while the two queries the method
> gains receive exactly the terms a person would have added
> **Unknown** — whether a model-written rewrite moves the paraphrase family on this corpus.
> Untested here, and the measurement machinery is written and waiting
