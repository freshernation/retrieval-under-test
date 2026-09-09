# The number with no source

*Week 4 · Day 1 · about 25 minutes*

> By the end of this you can say why there is no right chunk size, and why the ones you
> have read exist anyway.

---

## Sources

| Source | Tier | What it gives you |
|---|---|---|
| — | — | **There is no Tier 1 or Tier 2 source for chunk size.** That is this article |
| [**Anthropic, *Contextual Retrieval***](https://www.anthropic.com/news/contextual-retrieval) | 1 | A first-party experiment on chunk handling, by a party to the question. Read the caveat below |
| [**BEIR**](https://arxiv.org/abs/2104.08663) | 1 | Evidence for the general principle: retrieval results do not transfer between corpora |

---

## Go and look

Search for chunk size advice and count what you find: 512 tokens. 1000 characters. 10%
overlap. 20% overlap. Sentence windows. Paragraphs.

Now follow any one of them to its source.

You will find a tutorial citing a tutorial, a framework's default value, a blog post whose
methodology is "we tried a few and this felt best", and — if you are persistent — an
example notebook from 2023 where somebody wrote `chunk_size=512` because it was a round
number that fitted a model's context window.

**That is the entire evidential basis for the most consequential parameter in a RAG
system.** Not a bad study; no study. This course's `SOURCES.md` calls that Tier 4 —
widely repeated, no traceable origin — and week 4's source file records the topic as having
none, which is a thing the checker explicitly supports because it comes up.

---

## Why there is no answer

Not because nobody has tried. Because the question is malformed.

The best chunk size depends on:

- **How the answers are distributed in your documents.** A corpus of one-paragraph FAQ
  entries and a corpus of sixty-page standards want different things
- **How long your answers are.** The span that answers a question is 6 words in one of
  this corpus's queries and 19 in another. A chunk must contain the longest one
- **How your documents are structured**, and whether that structure survived extraction
- **What your queries look like.** Long specific queries match small chunks; short vague
  ones need more surrounding context
- **What you can afford**, which is not a property of the corpus at all
- **What your retriever is.** BM25's length normalisation means chunk size interacts with
  `b`; a dense retriever has a completely different relationship to length

Six inputs, four of which are properties of *your* corpus and users. A number derived from
somebody else's six is not evidence about yours. It is not even weak evidence — it is a
number from a different question.

This is BEIR's finding one level down: if retrieval *models* do not transfer between
datasets, retrieval *parameters* certainly do not.

---

## A worked example of the emptiness

`fixed 400` — near the middle of every recommendation you will read — is **dominated at
every k** on this corpus. Not narrowly beaten: dominated, meaning there exists a
configuration that is at least as accurate and strictly cheaper, so no requirement whatever
would select it.

It loses 22% of the answers while costing twice as much as the configuration that loses
none.

That is not because 400 is a bad number. It is because 400 is a number about a different
corpus, and this one has long documents with clean section structure and short answer spans.
On a corpus of chat transcripts it might be excellent, and you would still have no way to
know without measuring.

---

## The vendor-benchmarked exception

Anthropic's contextual retrieval post is a genuine experiment with numbers, published by
people who ran it. It is Tier 1.

It is also written by a company selling the model that performs the contextualisation step
it recommends. Both are true, and this course's doctrine has a flag for exactly this case:
record it as Tier 1 with `conflict: true`, name what the publisher sells, and do not let a
`known` claim rest on it alone.

That is not an accusation. It is frequently the only measurement anybody has run, which is
itself the point — **the best available evidence on chunking is a vendor's blog post**, and a
field where that is true is a field where you should be measuring things yourself.

---

## What to do instead

The rest of this week, and it is a procedure rather than a number:

1. **Write down what an answer looks like** in your corpus — a span, verbatim. Tuesday
2. **Check that your chunking does not destroy any of them.** One pass, no retrieval,
   before anything else. Tuesday
3. **Measure coverage against cost**, on your corpus, with your queries. Thursday
4. **State a requirement** — how often it is acceptable to miss, and what you will pay —
   and let the frontier select. Thursday
5. **Report the frontier**, not the winner

Five steps, none of which is a number, all of which transfer to a corpus nobody has written
about. That is what this week has instead of an answer.

---

## And be honest about your own number afterwards

When you finish this week you will have a configuration that works on ten RFCs with sixteen
queries. It is not the right chunk size. It is the right chunk size **for this corpus, this
query set, this retriever, and this budget**, measured on nine answerable dev queries, which
is a small number.

If you write it up, say all of that. The alternative is to add one more entry to the pile of
sourceless numbers that made this article necessary.

---

> **Known** — retrieval model rankings do not transfer between datasets (`beir-2021`) ·
> a first-party experiment on chunk handling exists and is published by a party to the
> question (`anthropic-contextual`)
> **Inferred** — that no general chunk-size recommendation can be valid, because the answer
> depends on corpus, query distribution, answer length, retriever and budget. Ours, argued
> rather than measured
> **Derived** — a configuration dominated at every k cannot be selected by any requirement,
> since something is at least as accurate and strictly cheaper
> **Unknown** — essentially everything. There is no controlled study of chunking strategy
> across corpora that we can find, and this is the most consequential gap in the field's
> literature
