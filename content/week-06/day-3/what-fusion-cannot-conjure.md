# What fusion cannot conjure

*Week 6 · Day 3 · about 25 minutes*

> By the end of this you can name the failure your week did not touch, and say what would.

---

## Sources

| Source | Tier | What it gives you |
|---|---|---|
| [**Furnas et al., *The vocabulary problem***](https://dl.acm.org/doi/10.1145/32206.32212) | 1 | Two people agree on a word 10–20% of the time |
| [**BEIR**](https://arxiv.org/abs/2104.08663) | 1 | Where dense retrieval does and does not close that gap |
| [**Cormack, Clarke & Buettcher**](https://plg.uwaterloo.ca/~gvcormac/cormacksigir09-rrf.pdf) | 1 | Fusion's ceiling, implicit in the method |

---

## The row that does not move

| family | n | lexical | dense | fused |
|---|---|---|---|---|
| identifier | 4 | 1.00 | 1.00 | 1.00 |
| superseded | 2 | 0.50 | 1.00 | 1.00 |
| vocabulary-gap | 4 | 0.75 | 0.75 | **1.00** |
| **paraphrase** | 3 | **0.33** | **0.33** | **0.33** |

At k=3, k=5 and k=10. At every constant. Under every weighting.

Two of three paraphrase queries are retrieved by **nothing**:

- *"how do I stop search engines indexing my site"* — the corpus says **crawlers** and
  **access**, not search engines and indexing
- *"what part of a web address comes after the hash"* — the corpus says **fragment
  identifier** and **URI**

The answers are in the corpus. Both are one section away from a retriever that found them.

---

## Why fusion cannot help, by construction

Fusion's ceiling is the **oracle**: every query that at least one input retrieves. A query
neither input retrieves is not in the oracle, so no combination of them — no constant, no
weighting, no third retriever built from the same two signals — can reach it.

> **Fusion combines what your retrievers found. It cannot conjure what neither of them
> did.**

Which means every point of headroom you chased this week was a point that is *not* in this
family, and a week spent sweeping `c` is a week not spent on the failure that is actually
costing you.

That is not an argument against the week. Fusion won the vocabulary-gap family outright —
0.75 and 0.75 becoming 1.00, two retrievers each missing a different query and the fusion
getting both. It is an argument for **reading the family table before deciding what to work
on**, which takes ten minutes and almost nobody does.

---

## Why dense retrieval did not close it

Week 5 promised that changing the axes would bridge the vocabulary gap, and on
`too many requests` / `rate limiting` it did — 0.00 to 0.73.

It fails here for the reason week 5's day-3 article named: **LSA learns its axes from your
corpus and only from your corpus.** "Search engine" and "indexing" barely appear in ten
RFCs about protocols, so there is no co-occurrence structure connecting them to "crawler"
and "access". The technique has nothing to work with.

A trained embedding model plausibly does better here, because it has seen a great deal of
text in which search engines index things. **Plausibly.** We cannot test it, this course
cannot run one, and the honest report says so rather than assuming either way.

That is a real and testable prediction, and it is the best argument this course can make
for using a trained model in production.

---

## What would actually fix it

Four interventions, in rough order of cost:

**Change the query.** Expand `search engines` to include `crawler`, `robot`, `spider`;
`indexing` to include `access`, `crawl`. This is query expansion, it is the direct answer,
and it is week 11.

**Change the chunk.** A chunk beginning `2.2.2. The "Allow" and "Disallow" Lines` carries
its heading, and headings use the corpus's vocabulary rather than the user's. This helps
less than you would hope, for the same reason.

**Change the corpus.** Add a glossary mapping user vocabulary to document vocabulary. Cheap,
unglamorous, effective, and nobody does it because it is not a technique.

**Change the retriever.** A trained embedding model. Most likely to work, least likely to be
measured before adoption.

Note that three of the four are **not retrieval improvements**. This is station 1 and
station 6 work, arriving from a retrieval failure, which is the seven stations doing their
job.

---

## The habit

> Before optimising, look at what is failing. Before chasing headroom, look at what is
> outside the oracle.

`unreachable` is six lines. It runs on any two rankings you have. It tells you the set of
queries no amount of ranking work can help with, and it is the only list that says where
the remaining failure actually lives.

---

> **Known** — spontaneous vocabulary agreement is 10–20% (`furnas-1987`) · dense retrieval
> closes the vocabulary gap on some datasets and not others (`beir-2021`) · fusion's
> ceiling is the union of its inputs' results (`rrf-2009`)
> **Inferred** — that LSA fails this family because the connecting vocabulary is absent from
> a ten-RFC corpus, and that a trained model would plausibly succeed. The first follows from
> the method; the second is a prediction we cannot test here
> **Derived** — a query no input retrieves is outside the oracle, so no fusion of those
> inputs can retrieve it
> **Unknown** — whether a trained embedding model retrieves r19 and r20 on this corpus. It
> is a one-afternoon experiment for anyone with an API key, and it would settle a claim this
> course can only make conditionally
