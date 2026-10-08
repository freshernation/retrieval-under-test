# The technique aimed at the failure

*Week 11 · Day 1 · about 25 minutes*

> By the end of this you can explain why a rewrite's net delta is the least useful number
> it produces, and why the rule about where rewrite rules come from is not pedantry.

---

## Sources

| Source | Tier | What it gives you |
|---|---|---|
| [**Rocchio**, relevance feedback](https://sigir.org/files/museum/pub-08/XXIII-1.pdf) | 1 | The original: move the query towards what was relevant |
| [**Lavrenko & Croft**, relevance-based language models](https://doi.org/10.1145/383952.383972) | 1 | The modern form of pseudo-relevance feedback, and its assumption |
| [**Robertson & Zaragoza**](https://doi.org/10.1561/1500000019) | 1 | idf, which decides which words a rewrite may discard |

---

## Why this technique, aimed here

Week 10's attribution report named six failures and put two of them at station 4: the
shortlist never contained the answer. Both are `paraphrase` queries. One asks how to stop
search engines indexing a site, against a corpus that says `crawler`, `disallow` and
`access`. Week 6 had independently flagged the same pair as retrieved by nothing.

Query rewriting is the technique pointed exactly at that gap. So this is an honest test:
**the failure was identified before the technique was chosen**, which is the opposite of the
usual order and is why the result means something.

---

## The rule about where rules come from

Before any of it: **no rewrite rule derived from a failing query.**

The tempting move takes four minutes. Look at `r19`, notice it needs `crawler` where it
says `search engines`, add `{"search engine": "crawler"}` to a dictionary, and watch the
number move.

That number is worthless, and worse than worthless because it is large. The rule was fitted
to the test, the only instrument available is the test, and nothing in the measurement can
tell you what happened. It is the eval set leaking into the system, and it is the
characteristic way applied retrieval work fools itself.

So every rewrite here is derived from the index or from the query:

- **`drop_low_idf`** — keep the highest-idf half of the terms. idf comes from the corpus
- **`prf_terms`** — the top terms of the retrieved chunks, by `count × idf`. The documents
  come from the retrieval
- **`variants` + fusion** — the original and the two rewrites, fused with week 6's RRF

If you want a hand-built mapping, build it from documents you have never measured against,
and say in the report that you did.

---

## The three results

| rewrite | before | after | delta | gained | lost |
|---|---|---|---|---|---|
| drop low idf | 0.70 | 0.60 | -0.10 | — | `r07`, `r22` |
| expand (PRF) | 0.70 | 0.65 | -0.05 | `r21`, `r23` | `r04`, `r06`, `r07` |
| fan-out + RRF | 0.70 | 0.65 | -0.05 | — | `r07` |

All three lose. And **`paraphrase` stays at 1/3** under every one of them: the two queries
the day was aimed at do not move.

---

## The net delta is the least useful number

-0.05 is one number describing five events, and the five events are the finding.

By family, for the expansion:

| family | before | after |
|---|---|---|
| plain | 4/5 | **5/5** |
| vocabulary-gap | 2/4 | **3/4** |
| identifier | 4/4 | 3/4 |
| acronym | 1/1 | **0/1** |
| superseded | 2/2 | 1/2 |
| paraphrase | 1/3 | 1/3 |

Two families up, three down, one unchanged. That is not a rewrite that fails; it is a
rewrite that is **right for one half of the query mix and wrong for the other**, which is a
different problem with a different response — and the response is tomorrow.

A report quoting -0.05 has discarded the only actionable thing it measured.

---

## And the mechanism is week 5's

Why does expansion help loose prose and destroy a precise identifier?

Because adding terms **dilutes**. BM25 scores a document against a query; lengthening the
query adds terms a relevant document may not contain and spreads the score across more
dimensions. For *"how does a server remember a visitor between page loads"* that is
helpful — the query was vague and the feedback terms sharpen it towards `cookie` and
`Set-Cookie`.

For `428` it is fatal. The query was already perfect. Four postings, one unambiguous match,
idf 4.08. Every term added is a term that pulls other documents up and this one down.

Week 5 measured dense retrieval losing to BM25 on identifier queries and gave the reason:
an exact token match is information that a smoothed representation cannot keep. Expansion
is smoothing by another route, and it loses the same thing in the same place.

Which is a useful general shape. **A technique that adds information helps where
information was missing and hurts where it was already sufficient** — and no aggregate over
a mixed query set can tell you which of those you are doing.

---

> **Known** — relevance feedback moves a query towards the terms of documents judged
> relevant (`rocchio-1971`) · pseudo-relevance feedback substitutes the top retrieved
> documents for judged ones, assuming they are relevant (`lavrenko-croft-2001`) · idf
> weights a term by its rarity in the collection (`robertson-zaragoza-2009`)
> **Inferred** — that a rewrite rule derived from a failing query cannot be evaluated on the
> set it was derived from, making the practice self-confirming. Ours
> **Inferred** — that expansion helps queries whose information was insufficient and hurts
> queries whose match was already exact, which is the same mechanism week 5 measured for
> dense retrieval on identifiers. Ours
> **Derived** — expansion by pseudo-relevance feedback gains two queries and loses three for
> a net -0.05, moving plain 4/5→5/5 and vocabulary-gap 2/4→3/4 against identifier 4/4→3/4,
> acronym 1/1→0/1 and superseded 2/2→1/2 · the `paraphrase` family stays at 1/3 under all
> three rewrites, so the two station-4 failures the day targeted are untouched
> **Unknown** — whether a model-written rewrite moves the paraphrase family. It is the one
> thing worth testing first with an API key, and the course cannot
