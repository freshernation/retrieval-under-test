# The dead still vote

*Week 12 · Day 1 · about 25 minutes*

> By the end of this you can explain why deleting a document from an index and hiding it
> are different operations, and name the number that tells them apart.

---

## Sources

| Source | Tier | What it gives you |
|---|---|---|
| [**Lucene API**, `IndexReader.docFreq`](https://lucene.apache.org/core/9_0_0/core/org/apache/lucene/index/IndexReader.html) | 1 | The sentence: document frequency does not account for deleted documents not yet merged away |
| [**Elasticsearch reference**, Merge](https://www.elastic.co/guide/en/elasticsearch/reference/current/index-modules-merge.html) | 1 | Segments are immutable, and merging is what expunges deletes |

---

## Every index so far was built once

Eleven weeks, one corpus, and it never moved. You built the index on Monday of week 3 and
have been querying the same 266 chunks ever since.

No real corpus is like that. A document arrives. One is withdrawn. One is revised, which
is both. The question this week starts with is what happens to the index.

Rebuilding is always correct. It is also the entire cost of indexing, paid again, for one
document.

---

## Two ways out

**Remove.** Find every term the document contains, delete its entry from each posting
list, subtract its length, drop any term that now belongs to nobody. Afterwards the index
is exactly the one you would have built without the document.

It needs something week 3's index never kept: for each document, the list of its terms.
Without that, removing one document means scanning the whole vocabulary. Being able to
delete has a storage price, and you pay it for every document, including the ones you
never delete.

**Tombstone.** Add the id to a set of dead documents. At query time, skip them. One line,
no scan, instant.

This is what production search engines do, and for a good reason: their index files are
written once and never modified. A delete is a mark. The space, and the postings, come
back later, when segments are merged.

---

## What a tombstone leaves behind

Everything except the result.

Recall what BM25 is made of. The idf of a term comes from how many documents contain it
and how many documents there are. Length normalisation comes from the average document
length. All three are properties of the **whole index**.

A tombstoned document is skipped at query time. It is still counted in all three.

On the gold corpus, withdraw the two obsoleted RFCs — 28 chunks of 266. The term `json`
appears in 32 chunks according to the tombstoned index. Build an index from the 238 live
chunks and it appears in 16. Half its document frequency belongs to a document that no
longer exists, so `json` looks twice as common as it is and every live chunk containing it
scores lower than it should.

---

## The demonstration

Run the twenty dev queries against both indexes and compare the ranked lists.

| Depth | Queries whose list differs |
|---|---|
| top 1 | 0 of 20 |
| top 5 | 4 of 20 |
| top 10 | 8 of 20 |

No dead document appears in any list. The filter works. The **live** documents are in a
different order, because their scores were computed from statistics that include the dead.

Read the first row again, because it is why this survives in production. Every first
result is the same. Somebody checks three queries by eye after the delete, sees the right
answers on top, and signs it off. The drift is further down — where your fusion step reads
sixty deep and your context window takes whatever fits.

---

## Debt

The fraction of stored documents that are dead. Here, 28 of 266: 0.105.

It is the number to put on a dashboard, with one caution. **Debt says how much could have
drifted, not how much did.** Ten percent debt moved forty percent of the top-tens. The
relationship depends on *which* documents died — withdraw one that shares its vocabulary
with half the corpus and a little debt goes a long way.

So debt is the trigger and drift is the measurement. When debt crosses your line, compact:
really remove the dead, and the index is once again the one you would have built.

---

> **Known** — in Lucene-based engines a delete is a mark, segments are immutable, and
> deletes are expunged at merge (`es-merge`, `lucene-indexreader`) · Lucene's document
> frequency does not take into account deleted documents not yet merged away
> (`lucene-indexreader`)
> **Inferred** — that debt measures exposure rather than damage. Ours, from one corpus,
> resting on the documented behaviour of the statistics (`lucene-indexreader`)
> **Derived** — tombstoning 28 of 266 chunks changes 8 of 20 top-tens and 4 of 20
> top-fives against a rebuilt index, and no top-one · `json` has document frequency 32
> tombstoned and 16 rebuilt
> **Unknown** — what debt should trigger compaction at realistic scale, and whether drift
> grows in proportion to debt. One corpus and one deletion pattern do not say
