# Week 14 — Guarded, cached, scaled

> **Destination**
> The service with a guard on the way in and the way out, a cache that answers similar
> questions without answering the wrong one, and two ways to make search bigger — each
> measured against the size at which it stops costing more than it saves.

Week 13 made the system a service. This week adds the four things every production
retrieval system is told it needs. Each is real. Each, measured, turns out to have a
condition attached that nobody mentions.

---

## The week

| Day | Folder | What you'll be able to do |
|---|---|---|
| Mon | `day-1/` | Guard queries and answers, and measure how often a guardrail fires on the innocent |
| Tue | `day-2/` | Answer similar questions from a cache, and stop it answering different ones |
| Wed | `day-3/` | Build an HNSW graph index by hand, and find the size at which it is worth it |
| Thu | `day-4/` | Split the index into shards, and keep BM25's statistics whole |
| Fri | `milestone/` | One guarded, cached, sharded search path, in the only safe order |

---

## Four findings

| Day | The finding |
|---|---|
| Mon | On 1,000 random order references, a card-number pattern flags **1,000**. Add the Luhn check: **80**. Add the issuer: **18**. Every real test card is caught all three ways |
| Tue | "section 3.2" and "section 3.4" score **0.981** — higher than nine of ten real paraphrases. No threshold answers a paraphrase without also answering a near miss. Checking identifiers removes every near miss and keeps every hit |
| Wed | On 266 chunks the graph reads **241** of them to reach 0.99 recall — **91%** of a scan. Asked for perfect recall, it reads more than the scan. At 2,000 vectors it reaches 0.978 reading a third |
| Thu | Four shards, each scoring with its own statistics: **25 of 26** top tens change. Share the statistics — one more round trip — and **none** do |

---

## What they have in common

Each technique answers the question it was designed for, and is quiet about the
neighbouring one. A guardrail detects card-shaped numbers, not cards. A semantic cache
finds similar text, not the same question. A graph index is fast when the corpus is
large, and this one is not. Shards search in parallel and each believes it is the corpus.

---

## `--live`

Nothing this week needs a model. The deep track is day 3 at a size where the graph wins
by a long way: build it over 50,000 vectors and plot recall against distances per query.

---

## Milestone

`guarded.py` and `REPORT.md`.
