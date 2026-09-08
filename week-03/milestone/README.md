# Milestone 3 — A retriever, and an instrument big enough to measure it

> **Ship:** a configured BM25 retriever that beats week 1 on the held-out split, an eval
> set grown to the size your own arithmetic says it needs, and `REPORT.md` with the four
> tuning warnings stated plainly.

This is the first milestone where the numbers move properly. It is also the first where
the honest report is longer than the result.

---

## The brief

### 1. Grow the eval set — **do this first**

Your nine answerable dev queries cannot confirm a 15-point improvement. `queries_needed`
says you need **10** at the current unchanged rate, and that is the bare minimum for one
result. Aim for **30 dev and 15 test**, which is where a 5-point difference starts being
detectable.

That is roughly 26 new queries, judged by hand, over ten documents you have now read
twice. Budget a full day. It is the least glamorous work in the course and the highest
leverage, which is why it is scheduled rather than suggested.

Requirements:

- At least **six shapes** from the week-1 list, and at least **three** more `unanswerable`
- At least four written **against a document you have not queried yet** — check which
  those are; a set that never mentions RFC 6265 cannot detect a failure on cookies
- Re-judge **ten** of your existing queries blind, and report kappa against your week-1 and
  week-2 numbers. Three data points is a trend

Then run `smells()`, and `judgments.check_against`. Both must be clean.

### 2. Ship a configured retriever

`Retriever(documents, **config)`, with the whole configuration in one dict so that
`raglab.runs.record` hashes it.

**One change per run.** Analyzer options, k1, b, k — each its own run id and its own
delta. `FENCE.md` explains why at length and it is the rule that matters this week.

Minimum runs, all on `dev`:

| Run | What changed |
|---|---|
| baseline | week 1's retriever, unchanged |
| index | same scoring, via the inverted index — **must reproduce baseline exactly** |
| bm25 | BM25 at the defaults |
| identifiers | BM25 with `identifiers=True` |
| tuned | BM25 at your chosen k1, b |
| cleaned | your chosen configuration over week 2's cleaned corpus |

The last one settles week 2's open question at whole-document granularity. It probably
still will not move. Say so, and say that week 4 is where you will ask again.

### 3. Tune, and distrust it

Grid search on `dev`. Report `best`, `spread`, `rank_of` the defaults, `at_edge`, `looks`,
and `moved_queries` against the defaults. All six. The report must contain the four
warnings from day 4 next to the tuned number, not in a footnote.

### 4. Confirm once on `test`

One configuration. One read. The log records it.

### 5. Write `REPORT.md`

Template in this folder. `python3 tools/check_evals.py` must pass.

---

## The rubric

| Station | This week |
|---|---|
| 1 Corpus | One sentence: did the cleaned corpus help at document granularity? |
| 2 Chunk | Still whole documents. One sentence on what document length is doing to `b` |
| 3 Index | **The week.** The analyzer, the postings, what you store and what it costs |
| 4 Retrieve | BM25, its three ideas, and which week-1 defect survives |
| 5 Rank | k1 and b, the grid, and the four warnings |
| 6 Generate | Not built. One sentence: which of your queries would still produce a wrong answer with perfect retrieval? |
| 7 Measure | **The other week.** The eval set, the floor arithmetic, and the new kappa |

---

## The bar

- `pytest week-03 -v` green
- `python3 tools/check_evals.py` green
- Eval set at **30 dev / 15 test** or the report says why not
- `smells()` and `check_against` clean
- Six runs, one change each
- Exactly one `test` run in the ledger this week
- You survive Friday

---

## What you will want to do and should not

**Tune before you grow the eval set.** Tuning is fun and labelling is not. Do it in the
order written: a grid search against nine queries is forty-five looks at an instrument
that cannot resolve them, and you will have to redo it.

**Turn two knobs in one run.** Stopword removal makes things worse and BM25 makes them
much better. Turn both at once, see a net win, and you will believe stopword removal helped
for the rest of your career.

**Ship k1 = ∞ because the grid said so.** Investigate it. Then decide, in the report, with
a reason that is not "the number was highest".

**Report the tuned number without the four warnings.** That is the whole of the difference
between this course and a blog post.
