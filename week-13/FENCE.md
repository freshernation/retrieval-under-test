# Week 13 — Concept fence

## Allowed

- Everything from weeks 1 to 12
- **Queues**: at-least-once delivery, out-of-order delivery, per-document versions,
  idempotent apply, attempts and a dead-letter status, a queue in a SQLite file
- **Snapshots**: an atomic write with `os.replace`, a manifest, a fingerprint, refusing a
  mismatch
- **CI**: a baseline file in the repository, a reason for every change to it, a tolerance
  chosen in advance, a workflow that runs on pull requests and never accepts
- **A service**: FastAPI, Pydantic bodies, keys compared in constant time, groups,
  `202 Accepted`, a health route
- **Containers**: a Dockerfile and a compose file, read rather than run

## Not yet

Guardrails, semantic caching, approximate graph indexes and sharding — week 14 · a
message broker · more than one machine · a real secrets manager · authentication beyond
a key per caller · week 11's agentic retrieval

---

## Why a SQLite queue

A broker is the right answer for many systems and the wrong first answer for this one:
another service, another failure mode, and it hides the two facts this week is about —
that delivery is at least once, and not in order. A table makes both visible.

## The keys and groups are stipulated

Three RFCs are staff-only, as in week 12. Nothing about real access control is claimed.
