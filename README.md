# Retrieval Under Test

Twelve weeks building retrieval over a corpus nobody has written about, proving with
numbers that it works, and finding out where it fails before someone else does.

This is not a tour of the stack. A student who has wired a vector database to a language
model has built one system; when the answers come back wrong on a corpus with no blog
post about it, they have no procedure. What transfers is the diagnostic — and the
production tools, when they arrive in week 10, are packaging for a pipeline that already
works and whose numbers you already have.

---

## The three rules

**1. No change without a measured delta.**
Every decision in every milestone document cites a run id, a metric, a split, and the
delta. `python3 tools/check_evals.py` enforces it. A retrieval system you cannot measure
is not a system you are improving, it is one you are stirring. See [`EVALS.md`](EVALS.md).

**2. Retrieval before generation.**
You may not touch a prompt until recall is on the board. Weeks 1 to 4 forbid embeddings
*and* language models outright. The whole first month is information retrieval, which is
the month everyone skips and the reason their systems plateau at "mostly fine".

**3. A system nobody has attacked is a demo.**
Every week ends with twenty minutes of somebody trying to make your system answer wrongly
and confidently. That is the grade. The tests are not.

---

## The seven stations

The spine. Every milestone runs all seven; every week deepens one or two.

| Station | Produces | The failure it prevents |
|---|---|---|
| **1 Corpus** | what is in scope, what was dropped, and where each document came from | answering from a corpus that never contained the answer |
| **2 Chunk** | the retrieval unit, and the reason it is that size | a chunk that can be found but cannot be answered from |
| **3 Index** | the representations — lexical, dense, structured | one representation asked to do every job |
| **4 Retrieve** | the candidate set, the filters, the fusion | tuning the ranker when the answer was never in the candidates |
| **5 Rank** | the final order, deduplicated, inside a context budget | right documents, wrong order, truncated away |
| **6 Generate** | a grounded answer, its citations, and its refusals | a fluent answer the sources do not support |
| **7 Measure** | the eval set, the metric, the run record, the gate | "it feels better" |

**The rule that makes this a method rather than a diagram:**

> Attribute the failure to exactly one station before you change anything. Walk 1 → 7,
> stop at the first station that failed, and never fix downstream of the break.

Most RAG work in the world is people rewriting the prompt — station 6 — for a failure
that happened at station 1. The reason it sometimes appears to work is that nobody is
measuring.

---

## The twelve weeks

| Week | | Milestone |
|---|---|---|
| 1 | Measure before you build | A labelled eval set, and a lexical baseline |
| 2 | The corpus is the system | An ingest of a real corpus, with a loss report |
| 3 | Lexical retrieval, properly | A tuned BM25 retriever that beats week 1 |
| 4 | Chunking, the decision with no science behind it | A chunker that beats fixed-window, measured |
| 5 | Embeddings and vector search | A dense index — and where it loses to BM25 |
| 6 | Hybrid, and what fusion actually does | A hybrid retriever, fusion chosen on evidence |
| 7 | Ranking and the context budget | A reranker that pays for its latency |
| 8 | **Generation and grounding** | **Project 2** — the full pipeline, cited answers |
| 9 | Evaluation at depth | An eval harness, and a gate that blocks a regression |
| 10 | Production: latency, cache, tracing, cost | The pipeline on real services, traced and priced |
| 11 | **Agentic retrieval** | **Project 3** — an agent that beats week 8, measured |
| 12 | The report and the review | Ten scored failure clinics |

Week 1 is where most people's assumptions break — they arrive wanting to build and spend
five days labelling. Week 8 is the keystone. Week 5 is the one you will want to argue
with.

---

## How to work

```bash
source .venv/bin/activate          # every session

pytest week-01/day-2 -v            # one day
pytest week-01 -v                  # one week
python3 tools/check_evals.py       # your claimed deltas
python3 tools/check_sources.py     # your claims
python3 tools/check_links.py       # your links
```

Tests are the *smallest* part of the grade here, and it is worth being clear about that
on day one. `pytest` can check that your nDCG implementation matches the definition. It
cannot check whether the thing you measured was worth measuring.

| | Checks | Can it be faked |
|---|---|---|
| `pytest` | the mechanisms | no |
| The milestone rubric | that all seven stations were run, and the deltas are real | partly |
| **The Friday clinic** | whether you can find the failure under attack | no |

Every lab ships as a stub that raises `NotImplementedError`, and is red before you write
anything. The tests in `tests/` are the harness's own and ship green — you use `raglab`,
you do not build it.

---

## dev and test

The shipped corpus has two splits, and the difference between them is most of what
professional retrieval work is.

**`dev`** is yours. Tune on it, look at it, overfit it into the ground.

**`test`** you may read **once per milestone**. Every read is recorded to `runs/`, and
`tools/check_evals.py` fails a milestone that reports a `test` number from more than one
run that week. This is not bureaucracy. Quietly tuning against the held-out set until the
number looks good is *the* characteristic failure of applied retrieval, it is invisible
in every write-up it has ever ruined, and the only defence is a rule you cannot bend
without noticing.

---

## Map

| Path | What it is |
|---|---|
| [`SETUP.md`](SETUP.md) | Day zero. Do this before week 1, not during it |
| [`EVALS.md`](EVALS.md) | The measurement doctrine. Rule 1, in detail |
| [`SOURCES.md`](SOURCES.md) | The evidence doctrine — what counts as knowing something |
| `week-01/` … `week-12/` | Four days, a milestone, a fence, a clinic |
| [`content/`](content/README.md) | The reading for every day, each opening with its primary sources |
| `content/sources/` | The claims ledgers — known, inferred, derived, unknown |
| [`ai/`](ai/README.md) | Your seven AI roles |
| `raglab/` | The deterministic harness the labs run on |
| `data/gold/` | The shipped corpus, its judgments, and its splits |
| `runs/` | Your run ledger. Every measurement you have ever taken |
| `tools/` | The three checkers |
| `logs/` | Your stuck log and your daily five numbers |
| [`CUT_LIST.md`](CUT_LIST.md) | What this course deliberately does not teach, and why |

Each week has a `FENCE.md` listing what you have met and what you have not. Paste both
lists into any AI role before you use it — it is what stops the model handing you a
week-9 technique in week 2 and making your toolkit feel inadequate.

Both logs are **read by your instructor before every live hour.** They are not marked. An
honest amber gets you help; a blank log gets you asked why it is blank.

---

## The failure library

The thing you actually carry out of this course. Roughly thirty one-page cards —
the failure, the station it belongs to, the diagnostic that finds it, the fix, the
measured delta, and the conditions under which the fix stops working — accumulated one
milestone at a time.

It is what lets you debug a retrieval system on a corpus nobody has blogged about, which
is the only thing that generalises.

---

## What this is not about

Frameworks. Vector database vendors. Being able to say what the current best embedding
model is.

There is a well-known course that gets you a running RAG app in week 1, and if that is
what you want, take it — it is good, and it is honest about being a build. Here you will
not have a running app until week 8, and in week 1 you will spend five days writing
relevance judgments by hand and hating it.

What you get for that is the ability to tell whether a retrieval system is any good.
Nobody can buy that back later, and almost nobody in this field has it.
