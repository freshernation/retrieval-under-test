# Before or after

*Week 6 · Day 4 · about 25 minutes*

> By the end of this you can place a filter deliberately, and say what each placement costs.

---

## Sources

| Source | Tier | What it gives you |
|---|---|---|
| [**Lucene query syntax**](https://lucene.apache.org/core/9_9_0/queryparser/org/apache/lucene/queryparser/classic/package-summary.html) | 1 | Boolean filters alongside a ranking model, as shipped |
| [**Malkov & Yashunin, *HNSW***](https://arxiv.org/abs/1603.09320) | 1 | Why a graph index cannot easily restrict its search to a subset |
| [**RFC 2026**](https://www.rfc-editor.org/rfc/rfc2026.txt) | 1 | The supersession relation the currency filter uses |

---

## Two placements

**Pre-filter** — restrict the corpus, then retrieve.
Always returns `k` results if `k` survive the predicate. Costs an index per filter, or an
index rebuild per query.

**Post-filter** — retrieve, then drop what fails.
One index, arbitrary predicates, and **you can end up with fewer than `k` results, or
none.**

Most systems post-filter, because most filters are arbitrary and nobody wants an index per
predicate. Almost nobody measures what that costs.

---

## When they agree

On this corpus, with a filter keeping 89% of chunks and a shortlist of 50, pre- and
post-filtering give **identical** answer recall: 0.789 both ways.

That is the reassuring result and it is entirely conditional. Post-filtering is safe when

$$\text{depth} \times \text{survival rate} \gg k$$

With 50 candidates, 89% survival and k=5, you have about 44 survivors for 5 slots. Fine.

Now shrink the shortlist. At depth 5, the mean shortfall is **0.47** — asking for five
results and getting four and a half on average. At depth 50 it is 0.05.

`survival()` is the one line that tells you how deep to go, and it is the calculation nobody
does.

---

## When they come apart badly

Make the filter selective. `published_since(2015)` keeps **63 of 266** chunks — 24%.

| | |
|---|---|
| mean shortfall | **0.63** |
| **maximum shortfall** | **5** |

A maximum of 5 means at least one query, given fifty candidates, has **no result at all**
that satisfies the filter. The system returns an empty list, and unless you are reporting
shortfall it looks exactly like a query with no good matches.

> A retrieval system that silently returns three results when asked for five is
> indistinguishable, from outside, from one that found three good ones.

---

## And the ANN interaction

This is the part that promised to come back from week 5, and it is why post-filtering is
worse than it looks in production.

An approximate index does not return the true top 50. It returns *about* the top 50, with
some ANN recall below 1.0 — at nprobe 1 on your own index, about half of them.

So a post-filter over approximate candidates loses recall **twice**:

1. The index missed some true neighbours
2. The filter removed some of what it did return

And you cannot fix the first by deepening the shortlist, because deeper approximate results
are still approximate. Neither loss is reported by anything: the index reports ANN recall,
the filter reports nothing at all, and the user gets four results.

Graph-based indexes make pre-filtering genuinely hard — the graph's edges were built over
the whole corpus, and restricting to a subset can disconnect it, so the search walks into a
region with no surviving neighbours. That is why filtered vector search is a named problem
with vendor-specific solutions rather than a checkbox, and why the honest question to a
vendor is *"what happens to recall when I filter?"*

---

## Filter after fusing, not before

One ordering rule for a hybrid system, and it is easy to get wrong.

Filter each retriever's output **before** fusing and each contributes a ranking over a
*different* population — lexical's tenth-place survivor and dense's tenth-place survivor are
tenth among different sets. RRF's whole premise is that a rank means the same thing on both
sides.

Fuse first, filter the fused list. One population, one meaning of rank.

---

## What to report

- **recall**, against what the filter allows
- **mean and maximum shortfall** — the maximum is where the empty results hide
- **survival rate** at your shortlist depth
- **placement**, and why

Four numbers. Most systems report none of them.

---

> **Known** — production engines expose boolean filters alongside ranking
> (`lucene-query-syntax`) · graph-based ANN indexes cannot straightforwardly restrict search
> to a metadata subset (`hnsw-2016`) · supersession is a formal relation recoverable from
> metadata (`rfc2026`)
> **Inferred** — that post-filtering over approximate candidates compounds two unreported
> recall losses. Ours, following from ANN recall bounding system recall
> **Derived** — post-filtering is safe when depth times survival rate greatly exceeds k, and
> returns fewer than k results otherwise
> **Unknown** — how much recall filtered vector search costs in practice across vendors. It
> is measurable and, as far as we can find, not published
