# Week 12 — Concept fence

## Allowed

- Everything from weeks 1 to 10
- **Index maintenance**: adding, removing and tombstoning documents; statistics that count
  the dead; debt; compaction; drift against a rebuilt index
- **Change detection**: content fingerprints, diffing two chunk sets by id and by content
- **Folding in**: projecting new chunks into a fitted basis; unseen vocabulary; agreement
  between two retrievers
- **Permissions**: groups, an access control list, a reader as a predicate, failing closed,
  a cache key that includes the reader, revocation
- **Poisoning**: a planted chunk, retrieval rate, answer rate, displacement, provenance
- **A release check** with limits, and one metric that takes none

## Not yet

Agentic retrieval, query rewriting, routing and loops — week 11's mechanisms are not used
this week, so that a change in a result has one cause · distributed indexes: shards,
replicas, consistency between them · a real permissions service · encryption, tenancy
and network isolation · detecting poisoned text by reading it · anything that requires a
model to *obey* a retrieved instruction — that is behind `--live`, in Thursday's deep track

---

## The permissions are stipulated

Three RFCs are declared staff-only. There is nothing confidential about them. This is the
same move as week 7's positional model and week 8's generator: the *mechanism* is real and
the *values* are ours, so no number this week is a claim about anybody's access-control
deployment.

## Why week 11 is fenced out

An agent that rewrites its query and retrieves three times would make every finding this
week harder to attribute: did the planted chunk get in on the first retrieval or the
third? The four findings are about the corpus, the index, the reader and the cache. Hold
the retriever still and they have one cause each.

When you are done, run Thursday's attack against week 11's loop. That is the deep track,
and the loop makes it worse.
