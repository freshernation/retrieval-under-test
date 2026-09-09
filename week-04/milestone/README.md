# Milestone 4 — A chunker, chosen on evidence

> **Ship:** answer spans for your own queries, an audited chunking configuration selected
> from a measured frontier, and `REPORT.md` stating the two numbers the decision required.

The first milestone where the deliverable is a **decision** rather than an improvement.
Chunking will not make your retrieval better. It will make it affordable, and the report
has to say so honestly.

---

## The brief

### 1. Write answer spans for your own queries

Every answerable query in your set needs at least one. Verbatim, from the corpus,
whitespace-collapsed, short enough to check by hand.

Rules, and they are the whole exercise:

- **A quotation, not a paraphrase.** If it needed adjusting to match, it is not evidence
- **The minimal span that answers the question.** Too long makes chunking look worse than it
  is; too short makes it look better. You are calibrating your own instrument and there is
  no way to do it without judgment
- **A query needing two documents gets two spans**, and `is_answered_by` will require both
- **Unanswerable queries get none**, and are excluded from the metric rather than scored zero

Then `python3 -c "import raglab; ..."` to check every span is actually present in the
corpus. A span that is not found is a typo, and it silently makes that query unanswerable
for the rest of the course.

### 2. Audit before you measure

`audit()` on every configuration you are considering, **before** running any retrieval.
Report `broken` for each. A configuration that destroys an answer is disqualified, not
penalised — no k, no ranker and no model recovers it.

### 3. Build the frontier

At least **five** configurations — including `whole` — at `k` in 1, 3, 5, 10. Two numbers
each: answer recall, and context words.

Report the **full table and the frontier**, with dominated points still visible and marked.
A frontier with the dominated points hidden looks like a set of good options rather than a
set of options.

### 4. Choose, with a requirement

State your **target coverage** and your **context budget** before you look at which
configuration they select, and justify each in terms of consequences:

> "One query in ten where the answer is not in the context at all is acceptable **because
> [what happens then]**."

Not "0.9 seems reasonable". If you cannot finish that sentence, you do not have a
requirement, you have a preference — and a preference is what your chunk size will encode
whether you write it down or not.

### 5. Confirm once on `test`

The chosen configuration, one read, both numbers.

### 6. Write `REPORT.md`

`python3 tools/check_evals.py` must pass.

---

## The rubric

| Station | This week |
|---|---|
| 1 Corpus | Week 2's cleaning, finally: does it help *at chunk granularity*? Measure it and settle it |
| 2 Chunk | **The week.** The audit, the frontier, the choice, the requirement |
| 3 Index | One sentence on what chunking did to your index size and to document frequency |
| 4 Retrieve | Answer recall replaces recall. One sentence on why the old number is no longer the right one |
| 5 Rank | One sentence on what `k` is now doing that it was not doing over documents |
| 6 Generate | Not built. One sentence: your chosen configuration puts N words in a window. What happens when the answer is at the end of it? |
| 7 Measure | The spans, and what changing the ground truth invalidated |

---

## The bar

- `pytest week-04 -v` green
- `python3 tools/check_evals.py` green
- Answer spans for every answerable query, all verified present
- `audit` run on every candidate configuration, `broken` reported for each
- Full table **and** frontier, dominated points visible
- Target and budget stated **with consequences**, before the selection
- Exactly one `test` run this week
- You survive Friday

---

## What you will want to do and should not

**Report the winning configuration without the frontier.** The frontier *is* the result;
the winner is one row of it and is only meaningful relative to what it beat.

**Pick the target after seeing which configuration it selects.** That is choosing the answer
and calling it a requirement. Write both numbers down first, in the report, and let them
select whatever they select.

**Write long answer spans.** A span covering a whole paragraph is nearly impossible for a
chunk boundary to destroy, so your chunking looks robust and is not. Minimal spans.

**Conclude that chunking improved retrieval.** It did not. Say what it did.
