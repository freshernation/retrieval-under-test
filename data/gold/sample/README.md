# The sample corpus

**30 documents, 12 queries, 39 judged pairs.** A fictional transit authority — the
Metro Regional Transit Authority — and its public document register.

## This is week 1's corpus only, and it is course-authored

Say this plainly, because the whole course is about provenance and it would be absurd to
be vague here.

These documents were **written for this course**. They are not real, no transit authority
published them, and nothing in them is a fact about the world. They exist so that every
lab has an exact, offline, reproducible number from day one, and so that the harness's own
tests have something to run against.

The **gold corpus** is [`../rfc/`](../rfc/README.md) — ten real RFCs with real provenance —
and the course runs on it from week 2 onward. This set stays, for one reason: week 1's
exercise is to judge a corpus *exhaustively*, and 23 KB of invented transit policy can be
read end to end in twenty minutes where 389 KB of RFCs cannot.

That you can no longer read all of the gold corpus is the premise of week 2.

## What has been put in it on purpose

Every one of these is a real failure mode, reproduced small enough to see:

| In the corpus | The failure it produces |
|---|---|
| `mrta-001` and `mrta-002` — the 2023 and 2024 fare policies, near-identical | Retrieving the superseded version. Confidently correct, factually wrong, station 1 |
| Repeated header and footer boilerplate on every register document | Boilerplate dominating a short chunk's tokens, station 2 |
| `mrta-014` — a table flattened into a run of numbers by the extractor | The answer is in the corpus and is not readable, station 1 |
| `mrta-030` — a glossary of eleven acronyms | Where lexical retrieval beats dense retrieval outright, weeks 3 and 5 |
| "31-day pass" throughout, never "monthly" | The vocabulary gap that motivates the whole of week 5 |
| Stop numbers, route numbers, dollar amounts | Exact-match queries, and what an embedding does to them |
| `mrta-012` and `mrta-013` — FAQs restating policy in plainer words | Near-duplicate content, and what it does to precision |

## The splits

8 `dev`, 4 `test`. Tiny — deliberately. On 8 queries a single query is 12.5% of the mean,
which makes the confidence intervals embarrassingly wide, and noticing that in week 1 is
worth more than any result you could get from a set large enough to hide it.

## Licence

Course material. Same licence as the repository.
