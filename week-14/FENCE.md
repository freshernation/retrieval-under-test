# Week 14 — Concept fence

## Allowed

- Everything from weeks 1 to 13
- **Guardrails**: patterns, the Luhn checksum, issuer prefixes, redaction, a guard on the
  query and on the answer, false-positive rates
- **Semantic caching**: embedding similarity, a threshold, identifiers, a cache scoped by
  reader
- **Graph indexes**: HNSW layers, greedy best-first search, `M`, `ef`, distances per query
  as the cost
- **Sharding**: hashing chunks to shards, scatter-gather, local and global statistics

## Not yet

A real embedding model in the graded path · a vector database · a guardrail model ·
replication and consistency between shards · detecting personal data other than card
numbers and email addresses · week 11's agentic retrieval

---

## The test cards are public

Every card number in day 1 is a published test number from the card networks' developer
documentation. None can be charged. Do not put a real one anywhere in this repository,
including a test.

## Why a scan is the baseline

Every approximate index is measured against reading everything. On 266 chunks reading
everything is cheap, which is exactly why the comparison is honest: it shows the overhead
the approximation brings before it starts to pay.
