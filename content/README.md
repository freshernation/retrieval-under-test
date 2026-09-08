# Course content

The reading for every day. One article per `Read first` item, each opening with the
**primary sources** for its topic — and, where none exists, saying so plainly.

Every day README links here; these articles link on to each other. They are written to be
publishable as standalone pages, and every relative link resolves within this tree
(`python3 tools/check_links.py`).

| | |
|---|---|
| **Articles** | 8 |
| **Weeks covered** | 1 |
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

## Weeks 2–12

Not yet written. See `instructor/PLAN.md` for the build order.
