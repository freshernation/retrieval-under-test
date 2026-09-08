# The evidence doctrine

Every claim in this course carries a source, a date, and a tier. This page says how, and
why the rule is stricter here than in most technical writing.

It is the sibling of [`EVALS.md`](EVALS.md). That one governs claims about *your* system,
which you settle by measuring. This one governs claims about the *world* — how BM25
scores, what chunk size works, whether reranking is worth it — which you settle by
finding out who actually knows.

---

## Why this exists

Ask ten sources what chunk size to use and you will get "512 tokens with 50 overlap" from
nine of them, none of which cite anything, all of which trace back to a default value in
somebody's example notebook. The number may even be fine for your corpus. But a student
who repeats it has learned a fact, not a skill — and when they are handed a corpus of
two-page regulatory notices, they have nothing.

Retrieval has a worse version of this problem than most fields, for a specific reason:
**most of the writing is by people selling a component of the system.** A benchmark
showing that reranking helps, published by a company that sells reranking, is not
worthless — it is often the only measurement anyone has run — but it is not the same kind
of thing as an independent evaluation, and a student who cannot tell them apart will buy
whatever is loudest.

So evidence triage is graded from week 1, it has its own AI role (`ai/librarian.md`), and
it is machine-checked.

---

## The four tiers

| Tier | Meaning | Examples |
|---|---|---|
| **1 — Primary** | The people who built the thing, or ran the experiment, on the record | [Robertson & Zaragoza on BM25](https://www.staff.city.ac.uk/~sbrp622/papers/foundations_bm25_review.pdf), the [HNSW paper](https://arxiv.org/abs/1603.09320), [Lucene's own docs](https://lucene.apache.org/core/), a named engineer's post about a system they operate |
| **2 — Foundational** | The paper or official documentation a technique rests on | [RRF (Cormack et al.)](https://plg.uwaterloo.ca/~gvcormac/cormacksigir09-rrf.pdf), TREC methodology, [OpenSearch docs](https://opensearch.org/docs/latest/), model cards |
| **3 — Secondary** | Interpretation by people who did not build it | newsletters, tutorials, conference talks summarising others' work, this course |
| **4 — Folklore** | Widely repeated, no traceable origin | most numbers in most RAG tutorials, including "512 with 50 overlap" |

Tier 3 is not forbidden — a good tutorial is often clearer than the paper, and clarity
matters. It is simply never **load-bearing**.

### The fifth category this field needs: vendor-benchmarked

A Tier 1 source can still be a party to the question. Anthropic's contextual retrieval
post is written by the people who ran the experiment — genuinely Tier 1 — and it is also
a company demonstrating that its own models are useful. Both are true.

Record it as Tier 1 with `conflict: true` and a note saying what the publisher sells. The
checker requires that any `known` claim resting on a single conflicted source is either
downgraded to `inferred` or paired with an independent replication. Most of the time
there is no replication, and saying so is the honest result.

---

## The four rules

**1. No claim rests on Tier 3 alone.** If the only support for a number is a tutorial,
the number does not go in as fact. It goes in the "what we are inferring" box, or it
goes out.

**2. Everything carries a date.** A 2023 benchmark of embedding models describes 2023 and
is now archaeology. Every source records `published` and `retrieved`, and every technique
article ends with **Where this is now**.

**3. Separate what is published from what is inferred.** Every article carries this box:

> **Known** — stated in the source, with the source id
> **Inferred** — our reasoning from what is stated, marked as ours
> **Derived** — follows from arithmetic or from a definition, and cites nothing because
> there is nothing to cite
> **Unknown** — the questions the sources do not answer

The last row is usually the most interesting one, and it is always the one that gets cut
elsewhere.

**4. When there is no primary source, say so in the article.**

And when a whole topic has none, the source file says so in a `no_sources_reason` field
and carries only `unknown` and `derived` claims.

**Chunking is that topic**, and it is the most consequential decision in a RAG system.
There is no peer-reviewed result telling you what chunk size to use, because the answer
depends on a corpus and a query distribution that nobody else has. Week 4 opens by saying
this plainly and then measures it on your corpus, which is the only available answer and
is a much better one than a number from a notebook.

---

## The machinery

Each week has a source file:

```yaml
# content/sources/week-03-reading.yml
system: Week 3 reading — lexical retrieval and BM25

sources:
  - id: bm25-foundations
    title: "The Probabilistic Relevance Framework: BM25 and Beyond"
    url: https://www.staff.city.ac.uk/~sbrp622/papers/foundations_bm25_review.pdf
    publisher: Foundations and Trends in Information Retrieval
    author: Stephen Robertson and Hugo Zaragoza
    kind: paper
    tier: 1
    published: 2009
    retrieved: 2026-09-08
    note: §3 the saturation function, §3.2 length normalisation and b

claims:
  - id: bm25-saturation
    text: >-
      Term frequency saturates — the tenth occurrence of a term contributes far
      less than the second — and k1 controls how fast
    kind: known
    sources: [bm25-foundations]
```

`tools/check_sources.py` fails the build when:

- a source has no `tier`, `published` or `retrieved` date
- a claim has no `sources`
- a `known` claim is supported only by Tier 3 or 4
- a `known` claim rests on a single source marked `conflict: true`
- an `inferred` claim cites nothing (only `derived` and `unknown` may)
- a claim references a source id that does not exist
- `--check-urls` is passed and a URL does not resolve

Run all three checkers:

```bash
python3 tools/check_sources.py
python3 tools/check_evals.py
python3 tools/check_links.py
```

---

## A note on benchmarks

Published retrieval numbers are almost never comparable to yours. A recall@10 of 0.94 on
a benchmark says the benchmark's queries were answerable from the benchmark's corpus by
the benchmark's judgments. It predicts nothing about your corpus, and the honest use of a
public benchmark is as a *sanity check that your implementation is not broken*, never as
a target.

Record benchmark numbers with the dataset name attached, always. `recall@10 = 0.94` is
not a fact about a retriever.
