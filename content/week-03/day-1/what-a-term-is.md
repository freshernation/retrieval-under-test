# What a term is

*Week 3 · Day 1 · about 25 minutes*

> By the end of this you can say what an analyzer decides, and why the same decision has
> to be made identically on both sides of a search.

---

## Read the primary sources first

| Source | Tier | What it gives you |
|---|---|---|
| [**Lucene analysis documentation**](https://lucene.apache.org/core/9_9_0/core/org/apache/lucene/analysis/package-summary.html) | 1 | The tokenise-then-filter model that every production engine uses, from the engine most of them are |
| [**Robertson & Zaragoza**](https://www.staff.city.ac.uk/~sbrp622/papers/foundations_bm25_review.pdf) §2 | 1 | What the retrieval model assumes a "term" is, which is less than you would think |
| [**Unicode UAX #29**](https://unicode.org/reports/tr29/) | 1 | What a word boundary actually is, once you leave English |

---

## The decision

A retriever does not match text. It matches **terms**, and a term is whatever your
analyzer says it is. Everything else this week — the index, the scoring, the tuning —
operates downstream of that decision and cannot repair it.

The standard shape, unchanged since the 1990s and used by every engine you will meet:

```
text  →  tokenise  →  filter  →  filter  →  …  →  terms
```

Tokenise splits. Filters transform, drop, or add. That is the whole architecture, and its
simplicity is why the decisions inside it get so little attention.

---

## What your week-1 tokeniser did

`[^a-z0-9]+` on a lowercased string. Four consequences you already met:

| Input | Terms | Cost |
|---|---|---|
| `UTF-8` | `utf`, `8` | `8` is in nine of ten documents; `utf-8` is what people search for |
| `$3.00` | `3`, `00` | the price is gone |
| `RFC 8259` | `rfc`, `8259` | fine, and `8259` is now beautifully rare |
| `ROCC` / `rocc` | same term | helps here; will hurt when an acronym collides with a word |

The third row is worth dwelling on. **Splitting is not always destruction.** Breaking
`RFC 8259` apart produced `8259`, a term appearing in one document, and rare terms are
where all the retrieval signal lives. The same operation that ruined `$3.00` created the
best term in the corpus.

An analyzer is a series of these trades, and almost nobody looks at what theirs is
trading.

---

## Adding rather than discarding

`keep_identifiers` emits the pieces **and** the compound: `utf`, `8`, and `utf-8`.

It is slightly wasteful — the index grows, and one input produces three postings where the
information is arguably one thing. It is also the only change on this day that improves
retrieval.

That is not a coincidence, and it generalises into today's thesis:

> **A filter that adds a term risks noise. A filter that removes one risks the answer.**

The costs are not symmetric. An extra term that nobody searches for sits in the index doing
nothing measurable. A missing term makes a query unanswerable, silently, with no error and
no way for the user to tell that the document they wanted exists.

Stopword lists and stemmers are both in the second category. That is Monday's whole result.

---

## The same analyzer on both sides

The most common bug in hand-built search, and it survives code review because the two call
sites are usually in different files:

> The index was built with one analyzer and the query is analysed with another.

Symptoms: everything works, most queries are fine, and one class of query returns nothing
at all. It looks exactly like a ranking problem, so people tune the ranker.

It happens because the two operations feel different. Building an index is a batch job in
an ingest script; analysing a query is one line in a request handler. Nobody writes them at
the same time, and the query side gets `text.lower().split()` because that is obviously
what tokenising means.

The defence is structural rather than disciplinary: **the index owns the analyzer**, and
the query goes through `index.analyze_query`. Then they cannot diverge, because there is
only one of them. Day 2's `Index` does exactly this, and it is the only reason it stores
its options.

---

## Where English stops being the case

Everything above assumes whitespace and punctuation separate words. Three places that
fails, worth knowing exist even though this corpus does not test them:

- **No spaces.** Chinese, Japanese and Thai do not delimit words, so tokenisation becomes
  segmentation, which is a model rather than a regex
- **Rich morphology.** Finnish and Turkish inflect so heavily that a stemmer is closer to
  essential than optional, and the English intuition that stemming is a marginal
  optimisation does not transfer
- **Normalisation.** `café` can be one code point or two, and the two forms are different
  strings that render identically. A user typing one and a document containing the other do
  not match, and nothing in the interface reveals it

Unicode's UAX #29 defines word boundaries properly and any real engine implements it. The
reason to know is not to implement it — it is to recognise that a system working well in
English tells you almost nothing about its behaviour elsewhere, and this is routinely
discovered after launch.

---

> **Known** — the tokenise-then-filter architecture is the standard analysis model
> (`lucene-analysis`) · word boundaries are defined by Unicode and are not whitespace
> (`uax29`) · the retrieval model treats terms as opaque symbols (`bm25-foundations`)
> **Inferred** — that additive filters are safer than subtractive ones. Ours, argued from
> the asymmetry of the failure modes and measured on this corpus in today's lab
> **Derived** — if the index and query analyzers differ, terms that should match cannot,
> so the failure presents as ranking rather than as an error
> **Unknown** — how often production systems have divergent index-time and query-time
> analysis. Everyone who has looked has found some; nobody has counted
