# The leak is in front of the filter

*Week 12 · Day 3 · about 25 minutes*

> By the end of this you can put a permission in front of a retriever, say which of two
> correct filters to use, and find the place a correct filter does not protect.

---

## Sources

| Source | Tier | What it gives you |
|---|---|---|
| [**OWASP LLM08:2025**, Vector and Embedding Weaknesses](https://genai.owasp.org/llmrisk/llm082025-vector-and-embedding-weaknesses/) | 2 | Misaligned access control named as a retrieval-specific risk |
| [**RFC 9111**, HTTP Caching](https://www.rfc-editor.org/rfc/rfc9111.html) | 1 | What a cache key is, as a specified thing |
| [**Zanzibar**](https://research.google/pubs/zanzibar-googles-consistent-global-authorization-system/) | 1 | Permissions as a system of their own, with their own consistency problem |

---

## One reader, until today

Every query in this course was asked by you, and you can read everything.

Put the system in front of an organisation and that stops being true. Two people ask the
same question. One of them may not read some of the documents. They must get different
results, and the one with fewer permissions must not be able to tell what they are
missing.

For this week three RFCs are declared staff-only. That is stipulated — there is nothing
confidential about HTTP 418 — and it is all the lab needs: a predicate that is true for
some chunks and some readers.

---

## The rule, and its one hard case

A document lists the groups that may read it. A reader has groups. They may read it if the
two overlap, or if the document lists none.

The hard case is the document with **no recorded rule at all**. It reached the index
before its permissions did — a sync job lagged, a field was null, a new source was
connected without a mapping.

There are two things to do with it and only one is defensible. **Treat it as unreadable.**
A document nobody can see is a bug somebody reports by lunchtime. A document everybody can
see is a bug somebody reports to a regulator.

---

## Two filters, both correct

Week 6 day 4 built both and found they agreed on recall.

- **Post-filter**: retrieve, then drop what the reader may not see.
- **Pre-filter**: restrict the candidates to what the reader may see, then retrieve.

Neither leaks. Check it: across twenty queries, no restricted chunk reaches the public
reader from either. As security controls they are the same.

As retrieval they are not.

| Public reader, k = 5 | Short of five | Empty |
|---|---|---|
| Post-filter the top 5 | 11 of 20 | 5 of 20 |
| Fetch 20, filter, keep 5 | 0 | 0 |
| Pre-filter | 2 | 0 |

Post-filtering the top five returns **nothing at all** for five questions. Each of them
has public documents that answer it. They were ranked sixth or lower, behind five chunks
this reader is not allowed to see, and the filter threw away the five and stopped.

Over-fetching fixes it here. How far to over-fetch depends on how much of the corpus this
reader cannot see, which is different for every reader and is not something a retriever
knows. Pre-filtering does not have the problem. Its two short results are true: there are
not five visible chunks that match.

---

## And then the cache

Every retrieval above was filtered correctly. Now put week 10's cache back.

Its key is the normalised question. A member of staff asks twenty questions; the cache
stores twenty results. A public reader asks the same twenty questions. Same keys. Twenty
hits.

**Eleven of them contain a chunk that reader may not see.**

Nothing in the retriever is wrong. The filter was applied to the query that filled the
cache, for the reader who asked it. The cache sits in front of the filter and has no idea
readers exist.

This is the general shape, and it is worth more than the specific fix: **a permission
check protects the path it is on.** Every shortcut around that path — a cache, a
precomputed summary, a suggested-question list, a log — needs the reader in it, or it
needs to be downstream of the check.

The fix for the cache is to put the reader's groups in the key. It costs what you would
expect: the cache now holds one entry per question per kind of reader, and the hit rate
week 10 measured is divided accordingly.

---

## Taking a permission away

A grant can lag without harm. A revocation cannot.

When a reader loses access to a document, every cache entry built on that document is
still there and still correct for the reader it was computed for. So the entry has to
record which chunks it is serving — week 10 day 3 insisted on that for a different reason
— and a revocation has to walk the entries and drop those that touch the document.

---

> **Known** — a cache may reuse a stored response only for a request matching its key, and
> what the key contains is specified (`rfc-9111`) · access control lists at scale are held
> by a dedicated system in which consistency between a change and its enforcement is a
> design problem (`zanzibar-2019`)
> **Inferred** — that misaligned access control is a recognised retrieval-specific risk
> (`owasp-llm08`) · that an unrecorded permission must mean unreadable. Ours, as a rule for
> this pipeline (`owasp-llm08`)
> **Derived** — post-filtering the top 5 leaves 11 of 20 dev queries short and 5 empty;
> over-fetching 20 leaves none short; pre-filtering leaves 2 · a cache keyed on query text,
> filled by staff, serves a public reader a restricted chunk for 11 of 20 queries
> **Unknown** — how long a revoked permission survives in the caches of a typical deployed
> system. We have no measurement
