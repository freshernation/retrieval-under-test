# Your checker's false positives

*Week 8 · Day 2 · about 20 minutes*

> By the end of this you will have found a bug in your own measurement before finding one in
> the system, and you will know why that order is common.

---

## Sources

| Source | Tier | What it gives you |
|---|---|---|
| [**RFC 7322**](https://www.rfc-editor.org/rfc/rfc7322.txt) §4.8 | 1 | The RFC citation convention — bracketed reference tags — which is the whole problem |
| [**Liu, Zhang & Liang**](https://arxiv.org/abs/2304.09848) | 1 | What a careful citation evaluation involves |

---

## The measurement

The generator emits **39** citations across twenty answers and invents none.

The naive parser — anything in square brackets — finds **44**, and flags **5 as
unresolvable**.

A fabrication rate of 11%, for a generator that fabricated nothing.

---

## Where they came from

```
[RFC3629]   [RFC3986]   [RFC6585]   [RFC2818]
```

RFCs cite each other with bracketed reference tags; it is in the style guide. The generator
copies sentences verbatim from chunks, and some of those sentences contain references.

So the corpus put them there, the generator faithfully carried them through, and the checker
counted them as the model's citations.

**Your metric had an 11% false-positive rate sourced from the documents, and the conclusion
it invited was "the model fabricates citations".**

---

## Why this order is common

A new measurement is applied to a system nobody has measured before, and it reports a
problem. The natural reading is that the problem is in the system: that is what you were
looking for, and finding it feels like the measurement working.

It is also the first time the measurement has ever run. Its own error rate is unknown, has
never been checked, and — crucially — **its failures look exactly like the failures it was
built to detect.**

The habit that catches it costs ten minutes:

> **Before believing a new metric's finding, look at the individual items it flagged.**

Five items. Print them. `RFC3629` is not a chunk id and does not look like one, and the whole
thing is over in a minute.

This is week 3's *print what your rule matched* rule, arriving at a different station. It
generalises: a checker is a system too, its first run is untested, and the cheapest possible
validation is to read what it flagged.

---

## Two fixes, and only one of them is real

**Resolve against the chunk ids.** `chunk_citations` keeps only parsed ids that are actually
chunks. The number becomes right — 39, all real, all present.

It is papering over the ambiguity rather than removing it. A cited id that *coincidentally*
matches a chunk id still slips through, and the checker is now silently discarding things it
does not understand, which is a different way to be wrong.

**Make the marker something the corpus cannot contain.** The real fix, upstream, at the point
where you define the contract between the prompt and the parser: a delimiter, or a required
id shape, that no document uses.

And then find a corpus where your new marker also appears — they exist — and notice that you
have made the collision rarer rather than impossible. Which is the honest state of most
delimiter choices.

---

## The general shape

Any measurement over text has this problem: the text was not written for your parser.
Bracketed references, markdown that is data rather than formatting, quoted JSON, code blocks
containing your delimiter.

Three defences, in order of how much they cost:

1. **Read what your checker flagged.** Ten minutes, catches most of it
2. **Report the checker's own error rate** alongside the system's. If you have never measured
   it, say that
3. **Design the contract so the ambiguity cannot arise**, and accept that you have reduced
   rather than eliminated it

Nobody does the second. It is the one that would have prevented the wrong conclusion here.

---

> **Known** — RFCs use bracketed reference tags by convention (`rfc7322`) · careful citation
> evaluation requires distinguishing the system's citations from artefacts of the source text
> (`liu-verifiability-2023`)
> **Inferred** — that a new checker's failures resemble the failures it was built to detect,
> so its first findings are systematically over-trusted. Ours, and this day is the instance
> **Derived** — a parser matching any bracketed token counts corpus reference tags as
> citations whenever the generator quotes text containing them
> **Unknown** — how often published RAG citation metrics are contaminated by source-text
> artefacts. Given how common bracketed references are in technical corpora, our guess is
> often
