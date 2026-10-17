# The snapshot and its analyzer

*Week 13 · Day 2 · about 25 minutes*

> By the end of this you can explain why an index written to disk must carry the settings
> that built it, and why a crash in the middle of a save must not be able to cost you the
> last good one.

---

## Sources

| Source | Tier | What it gives you |
|---|---|---|
| [**Python**, `os.replace`](https://docs.python.org/3/library/os.html#os.replace) | 1 | The rename is atomic when both paths are on the same file system |
| [**SQLite**, Atomic commit](https://www.sqlite.org/atomiccommit.html) | 1 | How a database makes a write all-or-nothing, and what that costs |
| [**Elasticsearch reference**, Search analyzer](https://www.elastic.co/guide/en/elasticsearch/reference/current/search-analyzer.html) | 1 | Query text and indexed text must be analysed compatibly, or matches silently fail |

---

## Every index so far died with its process

Twelve weeks of indexes, every one of them built by the Python process that used it and
gone when that process ended. That is fine in a notebook. In a service it means two
things: the service is down for as long as indexing takes, every time it starts, and it
indexes whatever corpus it can see at that moment — which may not be the one you measured.

So the index is written to disk once, and read back on every start. Two things make that
harder than calling `json.dump`.

---

## A half-written file is worse than no file

Write the snapshot straight to its path and the process dies halfway through: the file
now holds half an index. The next start either refuses to read it — and the service will
not come up — or, worse, reads the half that is there.

The answer is to never write to the real path. Write the whole snapshot to a temporary file
beside it, then **replace** the old file with the new one in a single step. On the same
file system that step is atomic: anyone reading the path sees the old snapshot or the new
one, never a mixture. The test makes the writer die partway through and checks the old
snapshot is untouched.

---

## An index means nothing without its analyzer

This is the part nobody writes down until it bites. Week 3 built the index with
`stopwords=None`: every word kept. Suppose the service that loads the snapshot analyses
queries with the default stoplist. Every query loses its common words before it is scored
— against an index that still contains them, with document frequencies and lengths that
count them.

Nothing errors. Every query returns ten results. And **nineteen of twenty-six** top tens
are not the ones you measured; for **six** queries the first result changes.

The snapshot therefore carries a **manifest**: the format version, the analyzer options,
the number of documents, and a fingerprint of what is stored. Loading compares the options
it is asked to use with the ones in the manifest and refuses a mismatch, loudly, at start-up
— the one moment when refusing is cheap.

---

## The fingerprint

The fingerprint is a hash of every stored chunk's id and length, and the tombstones. After
loading, the index computes its own fingerprint and compares. A snapshot edited by hand, or
truncated by a copy that ran out of disk, or written by a different version of the code,
does not match. It is not a security measure — anyone who can edit the file can edit the
manifest — it is a correctness one.

---

## What the snapshot does not include

The **versions** from day 1. The index on disk says what is indexed; it does not say which
version of each document that was. Restart with the snapshot and without the versions, and
every change the queue redelivers looks new. The milestone saves both, and the test that
proves it is the one named after it.
