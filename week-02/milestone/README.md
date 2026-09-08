# Milestone 2 — An ingest, and what it lost

> **Ship:** a pipeline that turns the raw corpus into a searchable index, a per-document
> manifest, a generated list of coverage gaps, and `REPORT.md` with both of this week's
> unproven changes argued properly.

Week 1's milestone was an instrument. This one is the thing the instrument gets pointed at.

---

## The brief

### 1. The ingest — `ingest.py`

Compose four days into one pass. `ingest`, `manifest`, `search`, `coverage_gaps`.

The manifest is **per document, never a corpus total**. A total would say "27% removed"
and hide that the shortest document lost 39% and the longest 18%, which is the finding.

### 2. Extend your eval set

Add **four queries** to `my-queries.yml`, over the RFC corpus, chosen to exercise what you
found this week. At least:

- one whose answer changed between two documents in the corpus
- one that needs **both** halves of a superseded pair
- one whose answer sits in text that a page boundary cut in half
- one more `unanswerable: true`, different in shape from your week-1 one

Judge them by hand. No language model, still. Report your kappa against week 1's.

### 3. Measure both changes, properly

Four runs, all on `dev`:

| Run | Config |
|---|---|
| baseline | week 1's retriever, raw corpus |
| cleaned | week 1's retriever, cleaned corpus |
| demoted | week 1's retriever, raw corpus, superseded demoted |
| both | cleaned and demoted |

For each, against baseline: the delta, the interval, and **the list of queries that got
worse**. Then read `test_the_real_pair_gets_sharper_and_the_spurious_ones_collapse` again
and measure the near-duplicate pair counts before and after cleaning, because that is a
delta too and it is the one that moved.

Then **once** on `test`, for whichever configuration you are shipping.

### 4. Decide, and defend the decision

Both changes have intervals that touch zero. You must ship or hold each one, and the
report must say which and why, in these terms:

> A **tuning change** with no delta is superstition — hold it.
> A **correctness fix** with no delta is a correctness fix on an eval set too small to see
> it — ship it, and prove it cost nothing.

Say which each of your two changes is. The wrong answer here is not "hold both" or "ship
both"; it is failing to say which kind of change you were making.

### 5. Write `REPORT.md`

Template in this folder. `python3 tools/check_evals.py` must pass.

---

## The rubric

| Station | This week |
|---|---|
| 1 Corpus | **The week.** The manifest, the gaps, the two obsolete documents, the format outlier |
| 2 Chunk | Still whole documents. One sentence on what the 222-word shared run implies for when you do chunk |
| 3 Index | Still a set of terms. One sentence on what supersession metadata would need in order to live in an index |
| 4 Retrieve | Unchanged, deliberately. Say so, and say what that fence bought you |
| 5 Rank | The demotion. Your one ranking change, and it came from metadata rather than from scoring |
| 6 Generate | Not built. One sentence: what should an answer say when its best source is superseded? |
| 7 Measure | Two changes, four runs, two intervals, and the argument |

---

## The bar

- `pytest week-02 -v` green
- `python3 tools/check_evals.py` green
- `coverage_gaps()` output pasted into the report verbatim
- Exactly **one** `test` run in the ledger for this week
- Every number carries `metric value (run:<id>)`
- Your four new queries judged, with `smells()` returning nothing
- You survive Friday

---

## What you will want to do and should not

**Delete RFC 7159.** It is 55% identical to a newer document that supersedes it and
removing it makes two problems go away at once. It also makes query `r14` unanswerable,
and `r14` is in the held-out split, so you would find out in three weeks.

**Report the corpus total.** It is one number instead of ten and it is the number that
hides the finding.

**Describe the cleaning as an improvement.** It is a change. You have the interval.

**Quietly re-run `test` after the first result disappoints.** The log records it and
Friday asks.
