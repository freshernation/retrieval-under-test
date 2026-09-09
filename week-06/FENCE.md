# Week 6 — Concept fence

## Allowed

- Everything from weeks 1 to 5
- **The extended query set.** From today the labs load
  `raglab.judgments.load(file="queries-extended.yml")` — 20 dev, 6 test
- **Score normalisation**: min-max, z-score, weighted sums, and their failure modes
- **Rank fusion**: reciprocal rank fusion, the constant `c`, per-retriever weights,
  shortlist depth
- **Verdicts**: beating every input, dilution, headroom captured, per-family breakdowns
- **Filters**: pre- versus post-filtering, predicates over document metadata, shortfall,
  survival rate

## Not yet

Reranking and cross-encoders — that is next week, and a reranker applied today would hide
which of the two retrievers actually contributed · query expansion, rewriting, or
generating alternative queries · language models, for anything · context assembly and
deduplication · prompts · agents · caching

---

## The rule that matters most this week

**A fusion result must beat every input, not one of them.**

The failure this prevents is not dishonesty. You fuse, you compare against dense retrieval,
you report five points. The fused system is also worse than the BM25 you already had, and
nobody checked, and the report is true.

`ship_check` makes the comparison mechanical. At k=5 on this corpus it refuses, and *"we
did not ship hybrid retrieval because BM25 alone scored higher"* is a better report than
most published ones.

## The other rule

**Sweep the constant before quoting a fusion result.**

RRF's `c = 60` comes from a 2009 paper about TREC runs and is the default in every
implementation. On this corpus at k=10 it captures **none** of the available headroom while
`c = 10` captures all of it. It is week 3's `k1 = 1.2` placing 38th of 45, wearing a
different hat.
