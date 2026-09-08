# The gold corpus — ten RFCs

**10 documents, 389,335 characters, 16 queries, 57 judged pairs.** Fetched from
`rfc-editor.org`, checked in, and used by weeks 2 to 12.

```bash
python3 tools/build_corpus.py --check     # confirm your copy still matches
```

## Why RFCs

Three reasons, and the third is the one that decided it.

**They are real, free, and stable.** Every document has a URL, a publication date and a
named author. An RFC is never edited after publication, so a corpus of them cannot drift
underneath your judgments — and `--check` proves it has not.

**They are small enough to check by hand.** Ten documents. The shortest is four pages. You
can open RFC 7725, search for "451", and disagree with our grade in about fifteen seconds.
Every judgment in `queries.yml` was written by reading the document, and every one of them
is falsifiable by you. That property is worth more than corpus size, and it disappears the
moment a corpus grows past what one person can hold.

**They contain the failures, unforced.** We did not have to construct any of the following.
They are simply what this corpus is.

## What is in it, and what each document is for

| Document | Published | Why it is here |
|---|---|---|
| **RFC 3986** — URI Generic Syntax | 2005 | The long one, 141 KB, with an ASCII syntax diagram no extractor keeps |
| **RFC 6265** — HTTP State Management | 2011 | Cookies. Users say "expire"; the document says `Expires` and `Max-Age` |
| **RFC 6585** — Additional HTTP Status Codes | 2012 | 428, 429, 431, 511. And a bibliography that mentions OAuth |
| **RFC 7725** — HTTP 451 | 2016 | Four pages. The easiest document in the corpus to verify by hand |
| **RFC 7159** — JSON | 2014 | **Obsoleted by 8259.** Does not know it |
| **RFC 8259** — JSON | 2017 | The current spec. Same title, same author, contradicts 7159 |
| **RFC 5785** — Well-Known URIs | 2010 | **Obsoleted by 8615.** Outdated without being wrong |
| **RFC 8615** — Well-Known URIs | 2019 | The current spec |
| **RFC 9309** — Robots Exclusion Protocol | 2022 | robots.txt, standardised 28 years after it was invented |
| **RFC 2324** — HTCPCP | 1998 | 418. Published on 1 April and it is a joke |

## The failure modes, free

| In the corpus | The failure it produces |
|---|---|
| **7159 and 8259 disagree about UTF-8** — `SHALL be UTF-8, UTF-16, or UTF-32` versus `MUST be encoded using UTF-8` | Returning the superseded answer. Station 1, and query `r05` |
| **7159 does not say it is obsolete.** The `Obsoletes: 7159` line is in 8259 only | The fact that makes an answer wrong lives in a *different document*. Nothing in the retrieved passage will ever warn you |
| **5785 and 8615 also supersede**, but the answer did not change | So supersession is not automatically an error. Graded 2 where `r05` grades 1. Be able to say why |
| **Page footers, form feeds, `Status of This Memo`, `Copyright Notice`, tables of contents** in every document | Boilerplate that outweighs a short chunk. Station 2, week 4 |
| **RFC 3986's ASCII syntax diagram** | Structure the extractor cannot represent. Station 1, week 2 |
| **"OAuth" appears only in a bibliography** | A confident top result for a question the corpus cannot answer. Query `r10` |
| **RFC 2324 is a joke** | Correct retrieval, dubious authority. Whether it belongs in the corpus is a station 1 argument, and it is the best one this corpus starts |
| **Acronyms everywhere; expansions almost nowhere** | ABNF, IANA, BCP, URI, IRI. Query `r06` |
| **Bare identifiers — 451, 429, 418, section numbers** | Where lexical retrieval is not merely competitive but correct, and dense retrieval will lose in week 5 |

## The splits

10 `dev`, 6 `test`. `dev` is yours. `test` is read **once per milestone**, and every read is
logged to `runs/.test-access.log`. See [`../../../EVALS.md`](../../../EVALS.md).

## Report at k=3, not k=10

**The corpus has ten documents, so recall@10 is very nearly 1.0 by construction** and says
nothing at all. The week-1 baseline scores recall@10 of 1.00 on `dev` and recall@3 of 0.76,
and only the second number is a measurement.

Headline metrics for this corpus are **recall@3** and **ndcg@3**. Report @5 alongside if
you like. Quoting @10 on a ten-document corpus is the same error as quoting @10 on three
million and not saying so — it is simply more obvious here, which is why the corpus is this
size.

## The week-1 baseline, for reference

Day 4's forty-line retriever, over whole documents:

| | dev | test |
|---|---|---|
| recall@3 | 0.76 | 0.92 |
| ndcg@3 | 0.65 | 0.84 |
| recall@10 | 1.00 | 1.00 |

Per-query on `dev`, it gets `r03` ("451") and `r09` (cookie expiry) perfectly, and scores
**zero** on `r01` — "what status code should I return when a client sends too many
requests" — because `status`, `code`, `client`, `sends` and `requests` are everywhere and
`429` is nowhere in the query. That single query is week 3's entire argument.

And on `r05` it returns **RFC 7159, the obsolete one, above RFC 8259**. Nobody arranged
that.

## Licence and provenance

RFCs are published by the IETF and are freely redistributable; each carries its own
copyright notice, which `build_corpus.py` deliberately does not strip. Every document
records the URL it came from and the date it was retrieved, and a truncated SHA-256 so you
can prove your copy is the one the judgments were written against.

## The other corpus

`data/gold/sample/` is a 30-document synthetic set used only in week 1. It exists because
week 1's exercise is to judge a corpus *exhaustively*, and 23 KB of invented transit policy
can be read end to end in twenty minutes where 389 KB of RFCs cannot.

From week 2 onward the course runs on this one, and the fact that you can no longer read
all of it is the premise of week 2.
