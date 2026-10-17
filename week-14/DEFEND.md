# Week 14 — Friday clinic

Twenty minutes, three phases, then a retro.

**This week asks whether they can state the condition attached to each technique** — the
one the documentation leaves out.

---

## Before they arrive

1. **Is each guardrail reported with its false-positive rate?** A detector with only its
   catch rate is an advertisement.
2. **Is the cache keyed by the redacted text and the reader?**
3. **Does the HNSW cost count distances, not wall-clock time?**
4. **Does the sharded search use global statistics by default?**
5. **In `guarded_search`, does the guard come first?**

---

## Phase 1 — Explain (6 min)

1. *"Your guard catches every test card. Is it a good guard?"* **The question of the week.**
   Not without the 18 order numbers it also redacts — and the ones a person needed to read.
2. *"Why can no similarity threshold make the cache safe?"*
3. *"The graph index is slower than a scan here. Why build it at all?"*
4. *"Each shard's BM25 is correct. Why is the merged list wrong?"*
5. *"Why must the guard come before the cache?"*

| 5 | 3 | 1 |
|---|---|---|
| States each technique's condition with its number | Gets there with prompting | Reports catch rates, hit rates and speed as wins |

## Phase 2 — Change something (7 min)

### A — *"Support says the guard keeps eating order numbers."*

Looking for: context (the word "order" nearby), a different format for order numbers,
or accepting the cost — with the false-positive rate quoted. Not "remove the guard".

### B — *"Traffic grows a hundredfold. Which of this week's four do you turn on first?"*

Looking for: shards only when one machine cannot hold the index, the graph only past the
size where it beats a scan, the cache with identifiers and readers — and a measurement
for each before switching.

## Phase 3 — Debug (7 min)

| Seed | Break | What it does |
|---|---|---|
| Easy | `luhn` doubles the wrong digits | Most real cards slip through |
| Medium | the cache ignores identifiers | 3.4 is answered with 3.2 |
| Medium | `scatter_gather` defaults to `shared=False` | 25 of 26 top tens move, nothing errors |
| Nasty | `guarded_search` checks the cache before the guard | A card number becomes a cache key, and the next reader's lookup compares against it |

---

## Retro (5 min)

1. *"Which of the four would you have shipped on the documentation's word?"*
2. *"What did I explain badly?"*

---

## Instructor: what week 15 rests on

Week 15 is the report and the review. Fourteen weeks of findings, and the ones that
transfer are mostly the negative ones — this week adds four.
