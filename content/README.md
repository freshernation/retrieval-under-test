# Course content

The reading for every day. One article per `Read first` item, each opening with the
**primary sources** for its topic — and, where none exists, saying so plainly.

Every day README links here; these articles link on to each other. They are written to be
publishable as standalone pages, and every relative link resolves within this tree
(`python3 tools/check_links.py`).

| | |
|---|---|
| **Articles** | 48 |
| **Weeks covered** | 1–6 |
| **Weeks planned** | 12 |

---

## What "sources first" means here

The Python course anchors on docs.python.org, and that is easy: there is one authority and
it is obviously correct.

**Retrieval has an authority for half of itself and none for the other half.** The
information-retrieval half — BM25, nDCG, pooling, significance testing — has fifty years of
peer-reviewed work behind it, and weeks 1 to 7 lean on it heavily. The RAG half is four
years old, is written mostly by vendors, and has no shared benchmark. Pretending those two
halves have the same evidential status would be the easiest way to teach this badly.

So each article opens with a tiered, dated source table, and ends by saying which of its own
claims are Tier 1 and which are this course's opinion. See [`../SOURCES.md`](../SOURCES.md)
for the doctrine and [`sources/`](sources/) for the claims ledgers.

Where an article is our own framing — the seven stations, the eval-set smells, the nine
questions — it says so. A course that will not apply its own rule to itself is not worth
much.

---

## Week 1 — Measure before you build

**Day 1** · [What a RAG answer actually is](week-01/day-1/what-a-rag-answer-is.md) · [The seven stations](week-01/day-1/the-seven-stations.md)

**Day 2** · [Relevance is a judgment, not a property](week-01/day-2/relevance-is-a-judgment.md) · [Building an eval set that can hurt you](week-01/day-2/building-an-eval-set.md)

**Day 3** · [The metrics](week-01/day-3/the-metrics.md) · [Is that a real difference?](week-01/day-3/is-that-a-real-difference.md)

**Day 4** · [The baseline you must beat](week-01/day-4/the-baseline-you-must-beat.md) · [Reading a claim about retrieval](week-01/day-4/reading-a-rag-claim.md)

---

## Week 2 — The corpus is the system

**Day 1** · [Open the file](week-02/day-1/open-the-file.md) · [What extraction destroys](week-02/day-1/what-extraction-destroys.md)

**Day 2** · [Cleaning a corpus](week-02/day-2/cleaning-a-corpus.md) · [The change you cannot prove](week-02/day-2/the-change-you-cannot-prove.md)

**Day 3** · [Finding what is repeated](week-02/day-3/finding-what-is-repeated.md) · [Duplication is not a defect](week-02/day-3/duplication-is-not-a-defect.md)

**Day 4** · [The fact is in a different document](week-02/day-4/the-fact-is-in-a-different-document.md) · [Currency, and what a corpus owes its reader](week-02/day-4/currency.md)

---

## Week 3 — Lexical retrieval, properly

**Day 1** · [What a term is](week-03/day-1/what-a-term-is.md) · [Throwing information away in advance](week-03/day-1/throwing-information-away.md)

**Day 2** · [Turning the loop inside out](week-03/day-2/turning-the-loop-inside-out.md) · [Boolean search, and why it lost](week-03/day-2/boolean-search.md)

**Day 3** · [Three ideas and one formula](week-03/day-3/three-ideas-and-one-formula.md) · [What BM25 still cannot do](week-03/day-3/what-bm25-cannot-do.md)

**Day 4** · [Two numbers, eighteen points](week-03/day-4/two-numbers-eighteen-points.md) · [How big does an eval set have to be?](week-03/day-4/how-big-does-an-eval-set-have-to-be.md)

---

## Week 4 — Chunking, and what it is actually for

**Day 1** · [Why chunk at all](week-04/day-1/why-chunk-at-all.md) · [The number with no source](week-04/day-1/the-number-with-no-source.md)

**Day 2** · [An eval set is a model of the thing you measure](week-04/day-2/an-eval-set-is-a-model.md) · [Overlap, and how much is enough](week-04/day-2/overlap.md)

**Day 3** · [The document already told you](week-04/day-3/the-document-already-told-you.md) · [Semantically right, dimensionally useless](week-04/day-3/dimensionally-useless.md)

**Day 4** · [Chunking is a cost decision](week-04/day-4/chunking-is-a-cost-decision.md) · [Choosing on a frontier](week-04/day-4/choosing-on-a-frontier.md)

---

## Week 5 — Embeddings, and what they are actually better at

**Day 1** · [One axis per word](week-05/day-1/one-axis-per-word.md) · [Cosine, and why not the dot product](week-05/day-1/cosine.md)

**Day 2** · [Factorising a corpus](week-05/day-2/factorising-a-corpus.md) · [How many dimensions](week-05/day-2/how-many-dimensions.md)

**Day 3** · ["Which is better" is the wrong question](week-05/day-3/the-wrong-question.md) · [What transfers from LSA to a real model](week-05/day-3/what-transfers.md)

**Day 4** · [Avoiding the scan](week-05/day-4/avoiding-the-scan.md) · [Two recalls, multiplied](week-05/day-4/two-recalls.md)

---

## Week 6 — Hybrid, and what fusion can and cannot do

**Day 1** · [Growing an eval set is a new instrument](week-06/day-1/a-new-instrument.md) · [Two kinds of number](week-06/day-1/two-kinds-of-number.md)

**Day 2** · [Reciprocal rank fusion](week-06/day-2/reciprocal-rank-fusion.md) · [Another default from somebody else's corpus](week-06/day-2/another-default.md)

**Day 3** · [Compared to what](week-06/day-3/compared-to-what.md) · [What fusion cannot conjure](week-06/day-3/what-fusion-cannot-conjure.md)

**Day 4** · [Before or after](week-06/day-4/before-or-after.md) · [A filter is a requirement, not a defect](week-06/day-4/a-filter-is-a-requirement.md)

---

## Weeks 7–12

Not yet written. See `instructor/PLAN.md` for the build order.
