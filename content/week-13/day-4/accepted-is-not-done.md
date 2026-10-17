# Accepted is not done

*Week 13 · Day 4 · about 20 minutes*

> By the end of this you can explain what a service promises when it answers 202, who it
> must refuse, and where the honest answer about its state lives.

---

## Sources

| Source | Tier | What it gives you |
|---|---|---|
| [**RFC 9110**, HTTP Semantics — 202 Accepted](https://www.rfc-editor.org/rfc/rfc9110.html) | 1 | Accepted for processing, which may not have been completed — or may never be |
| [**FastAPI**, Tutorial](https://fastapi.tiangolo.com/tutorial/) | 1 | Routes, request bodies as models, dependencies |

---

## A door has two sides

Everything so far was called by you, from Python, with every document visible. A service
is called by other people. Some may read everything; most may read some things; a few may
change the corpus. The door has to know which, before it does anything.

So every request but the health check carries a key, and every key belongs to somebody with
groups and, perhaps, the right to write. Keys are compared in constant time, against every
key, for the reason Agent In Production gave in its first week: a comparison that stops at
the first wrong character leaks how many were right.

---

## Filter, then take k

Searching for a reader means week 12's predicate in front of every result. The order
matters. Take the top five and then filter, and a staff-heavy query gives a public reader
two results, or none. Take a deep candidate list — sixty — filter it, then take five. The
public reader gets five results they may read, and never learns that better ones existed.

---

## 202 means queued

A writer posts a document. The service does not index it inside the request: indexing is
day 1's job, done by a worker draining the queue, so that a slow or failing document never
holds a connection open and never half-indexes because a client gave up.

So the honest answer is **202 Accepted**: the request is valid, it has been queued, and it
has not been done. HTTP's own definition says as much, including that the processing may
never happen.

Today's finding is the consequence, stated plainly. Between the 202 and the next drain, a
search for the document does not find it. Nothing is broken. The writer was told the truth
and heard something else.

---

## Where the truth lives

`/health` reports how many chunks are indexed, the debt from week 12, how many changes are
**queued**, and how many are **dead**. Those last two are the gap between what the service
was asked and what it has done. A monitoring system that reads one number from this
service should read those.

---

## What this is not

Authentication by a key in a file is enough to teach who is calling. It is not how keys
should be stored, rotated or revoked, and Agent In Production spends a week on running a
service like this for real. The point here is narrower: a retrieval service has readers
with different rights and writers whose changes are not instant, and both have to be
designed in, not found out.
