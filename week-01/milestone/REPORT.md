# Week 1 report — [your name]

> Template. Replace everything in brackets. Every number carries
> `metric value (run:<id>)` or `tools/check_evals.py` fails.

---

## Station 7 — the eval set

**Twelve queries, [N] judgments, [N] documents touched.**

| Shape | Query id | Why it is in the set |
|---|---|---|
| plain lookup | | |
| vocabulary gap | | |
| exact identifier | | |
| acronym | | |
| needs two documents | | |
| answer changed | | |
| **out of scope** | | |
| negation | | |

**Self-agreement:** [N]% raw over [N] commonly-judged documents, kappa [N].
Judged [date] and re-judged [date].

> The floor this sets: [one sentence. Below what difference does a result stop meaning
> anything for me?]

**Where I disagreed with myself:** [name two, and say what the distinction was. The 1/2
line, in your own words.]

**Coverage:** [N]% of the corpus carries at least one judgment.
**Bias audit:** `unjudged_in_top_k` surfaced [N] documents I had not judged. On judging
them, [N] were relevant — so my original numbers understated the baseline by [N].

---

## Station 1 — the corpus

[What is in it. What kind of question it cannot answer, with an example. Anything you
noticed about the documents themselves — versions, duplication, extraction damage.]

## Station 2 — chunking

Whole documents. [One sentence on what that costs, with a document id as evidence.]

## Station 3 — indexing

A set of normalised terms per document. [One sentence on what that cannot represent.]

## Station 4 — retrieval

**recall@10 [N] (run:[id])** on `dev`, n=[N].
**recall@5 [N] (run:[id])**.

Confirmed once on the held-out split: **recall@10 [N] (run:[id])**, n=[N].

The queries it missed entirely: [list, with one sentence each on why. Use `explain()`.]

## Station 5 — ranking

**ndcg@10 [N] (run:[id])** against **recall@10 [N] (run:[id])**.

[Which of your failures are ordering rather than retrieval? Name the queries where the
right document came back and came back low.]

## Station 6 — generation

Not built this week. [One sentence: given your single worst retrieval result, what would a
generator do with it, and would a reader be able to tell?]

---

## What got worse

[Not applicable in week 1 — there is nothing to compare to. Say so, and say what you will
compare to in week 3.]

## The failure library

Two cards, in `logs/failure-library.md`:

1. **[title]** — station [N] · found by [diagnostic] · [what it cost]
2. **[title]** — station [N] · found by [diagnostic] · [what it cost]

## What I would not defend

[One honest paragraph. The claim in this document most likely to be wrong, and how you
would find out.]
