# Turning the loop inside out

*Week 3 · Day 2 · about 25 minutes*

> By the end of this you can say what an inverted index stores, what each part costs, and
> what it buys that scanning cannot.

---

## Read the primary sources first

| Source | Tier | What it gives you |
|---|---|---|
| [**Lucene index file formats**](https://lucene.apache.org/core/9_9_0/core/org/apache/lucene/codecs/lucene99/package-summary.html) | 1 | What a production index actually writes to disk, file by file |
| [**Manning, Raghavan & Schütze, *Introduction to Information Retrieval*, ch. 1–2**](https://nlp.stanford.edu/IR-book/) | 2 | The textbook construction, including skip pointers and postings compression |
| [**Robertson & Zaragoza**](https://www.staff.city.ac.uk/~sbrp622/papers/foundations_bm25_review.pdf) §3 | 1 | The statistics the index has to make available for scoring |

---

## The idea

Week 1's retriever holds *document → terms* and loops over documents. An inverted index
holds *term → documents* and loops over query terms.

```
forward:   rfc-7725  →  {http, status, code, 451, legal, obstacles, …}
inverted:  451       →  {rfc-7725: [12, 47, 89, …]}
```

That is the whole idea. It has been the whole idea since punch cards, and every search
engine you will ever use is a very good implementation of it.

The consequence that matters: query cost stops depending on corpus size and starts
depending on **how many documents contain your terms**. A query for `451` touches one
document whether the corpus has ten or ten million. A query for `the` touches everything,
which is why rare terms are cheap and common terms are expensive — the exact opposite of
the intuition that a rare word is hard to find.

---

## What it has to store

Not just "which documents". Wednesday's scoring needs four statistics, and the index is
the thing that makes each one a lookup:

| Statistic | Used for | Where it lives |
|---|---|---|
| **term frequency** — occurrences of t in d | saturation | the postings entry |
| **document frequency** — documents containing t | idf | the length of the postings list |
| **document length** | length normalisation | a separate per-document array |
| **average length** | length normalisation | one number |

Document frequency being *free* — it is the length of a list you already have — is the
quiet reason idf is universal. The most useful statistic in retrieval costs nothing to
maintain.

---

## Positions, and what they cost

Storing *where* each term occurs, not just how often, is the single biggest line item in a
real index. It commonly doubles or triples it.

It buys exactly one thing: **phrase and proximity search**. On this corpus that is not a
marginal feature —

| query | result |
|---|---|
| OR `too many requests` | two documents, tied at three terms each |
| AND `too many requests` | the same two |
| **phrase** `too many requests` | **one**, the document whose section heading is literally `429 Too Many Requests` |

The boolean scorers cannot separate them. The phrase does it exactly.

Whether that is worth tripling your index is a real decision with a real answer that
depends on your queries, and the point of building it by hand is that you now know what you
are being sold when a service offers it.

### The trap

Phrase matching is not "every term is present and each one is adjacent to the first". It is
"there exists **one** start position at which every term lines up".

This course's own reference solution got it wrong. Checking each term independently against
the first term's positions makes `pot of coffee` match RFC 2324 — which contains `coffee
pot` in one place and `of` in a thousand others, and does not contain the phrase. Every
term found *a* start that worked; no single start worked for all of them.

The bug produces plausible extra results and raises nothing. Carry a set of candidate
starts and intersect it term by term.

---

## The lengths, and the argument for Wednesday

Print `index.lengths` and look at the spread:

```
rfc-7725    1,247 tokens
rfc-3986   19,462 tokens
```

**Fifteen times.** Any scorer that adds up per-term contributions without dividing by
something hands every query to RFC 3986 — which is exactly what week 1's `frequency_score`
did when it put the eleven-page governance document on top of a question it did not
answer.

The average, 5,278, describes no document in the corpus. Wednesday's `b` parameter is
entirely about this number, and having seen the spread first is what makes `b` a decision
rather than a default.

---

## What a real index does that yours does not

Yours is a dict of dicts in memory. A production index adds, roughly in order of
importance:

- **Compression.** Postings are sorted document ids, so store the *gaps* and
  variable-byte or bitpack them. Often 4–8× smaller, and smaller means fewer disk reads,
  so it is also faster
- **Skip pointers**, so an intersection can jump rather than scan
- **Segments.** Immutable index pieces, merged in the background, so a write does not
  block a read. Deletion is a tombstone, not an edit
- **A term dictionary** that fits in memory while the postings do not

None of these change the semantics. All of them are why a real engine is thousands of
times faster than yours and why you should use one — after you know what it is doing.

---

> **Known** — production indexes store term frequencies, positions and per-document lengths
> in separate compressed structures (`lucene-formats`) · document frequency is the postings
> list length and costs nothing additional (`mrs-irbook`) · scoring requires tf, df,
> document length and average length (`bm25-foundations`)
> **Inferred** — that positional data typically doubles or triples index size. Consistent
> with the file formats; the multiplier depends on the corpus and we have not measured it
> here
> **Derived** — query cost scales with the number of documents containing the query's
> terms, not with corpus size, so rare terms are cheap and common terms are expensive
> **Unknown** — what fraction of deployed systems store positions they never use. Phrase
> search is off by default in several stacks and paid for anyway
