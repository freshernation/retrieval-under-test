# An eval set is a model of the thing you measure

*Week 4 · Day 2 · about 25 minutes*

> By the end of this you can say why yesterday's failure was not a metric problem, and what
> it costs to fix.

---

## Sources

| Source | Tier | What it gives you |
|---|---|---|
| [**TREC overview papers**](https://trec.nist.gov/pubs.html) | 1 | Passage-level judgments as a distinct track from document-level, and why they were needed |
| [**Voorhees, TREC-8**](https://trec.nist.gov/pubs/trec8/papers/overview_8.pdf) | 1 | Judgment variation, and the stability of system rankings under it |
| [**Rajpurkar et al., *SQuAD***](https://arxiv.org/abs/1606.05250) | 1 | Answer spans as ground truth: verbatim substrings of a passage, judged by people |

---

## What went wrong yesterday

Not the metric. The metric worked exactly as defined.

You changed the unit of retrieval from a document to a chunk, and kept judging documents.
So the question your eval set answers — *was the right document retrieved* — stopped being
the question your system answers, which is *did the right text reach the context window*.

The consequences were not subtle:

- A chunk boundary destroyed an answer, and the answer became **unreachable at any k**.
  Document recall did not move, because the document was still retrieved
- Adding overlap — which repaired it — was scored as a **regression**, 0.834 to 0.779
- And the destroyed query was in the held-out split, so the number you were tuning on could
  not have contained the failure even in principle

> **An eval set is a model of the thing you are measuring.** When the thing changes, the
> model is wrong, and it does not announce it — it keeps returning numbers.

---

## The fix, and what it costs

Ground truth at chunk granularity. Three ways to get it, in increasing order of cost:

**Judge chunks directly.** Every query against every chunk. Correct, and hopeless: your
266-chunk corpus times sixteen queries is 4,256 judgments, and **it has to be redone every
time you change the chunking**, which is the thing you are trying to compare.

**Project document judgments down.** A chunk inherits its document's grade. Cheap, and it
answers the wrong question — every chunk of RFC 6585 inherits grade 3 for `r01`, including
the pages about 428 and 511 that answer nothing.

**Record the answer.** For each query, the verbatim span that constitutes the answer. A
chunk is answer-bearing if it contains a span.

The third is what this course does, and its decisive property is that it is **invariant to
chunking**. The span is a fact about the corpus, not about your configuration, so it is
written once and every chunking configuration for the rest of the course is measured against
it. Fifteen spans, an afternoon, and it does not have to be redone.

This is the SQuAD construction, borrowed: an answer as a verbatim substring rather than a
label, so that correctness is checkable by string containment rather than by judgment at
scoring time.

---

## What a span is, and what it is not

**A quotation.** If it needed adjusting to match, it is not evidence. Whitespace is
collapsed on both sides — because chunking splits on whitespace — and nothing else is
normalised.

**Minimal.** The shortest text that answers the question. This matters more than it looks:

- A span covering a whole paragraph is nearly impossible for a boundary to destroy, so your
  chunking looks robust and is not
- A span of three words is present all over the corpus, so your chunking looks better than
  it is

Both errors are invisible in the result. **You are calibrating your own instrument, and
there is no way to do it without judgment** — which is why the milestone asks you to name
the two spans you found hardest and say what you decided.

**Not the whole answer, necessarily.** `r14` needs two spans, in two documents, because
neither contains the comparison. `is_answered_by` requires all of them, and a system
returning one and stopping produces a confident half-answer.

---

## What the metric becomes

**Answer recall at k:** do the top `k` chunks, **together**, contain every span?

Together, because that is what a context window does — it concatenates. And binary per
query, because a context window either contains the answer or it does not. There is no
partial credit for nearly, and a graded version would be inventing a distinction the
downstream stage cannot act on.

It is a coarse metric. On nine answerable queries it takes ten values. That coarseness is
honest — it reflects that the underlying event is binary — and it is why week 3's floor
arithmetic matters even more here.

---

## The limitation you should hold onto

A span checks that the answer's *text* reached the context. It does not check that the
chunk is **usable**.

A chunk can contain `MUST be encoded using UTF-8` and be useless: no indication of which
specification, no subject for the sentence, cut off before the exception that follows. The
string is there and a reader could not act on it.

So answer-span recall is a **necessary condition, not a sufficient one**. It cleanly detects
the failure that nothing downstream can repair — the answer not being present at all — and
it is silent about whether the present answer is any good. That second question needs a
generator and a judge, and it is week 8.

Knowing which question your metric answers is most of what separates measuring from
appearing to measure.

---

## The uncomfortable part

You now have three weeks of decisions made against an instrument that could not see this.

Most of them are fine — weeks 1 to 3 retrieved whole documents, so document judgments were
the right model. But the habit is what to take away: **when you change what the system does,
ask what your eval set now assumes**, before you ask what the numbers say.

Week 8 changes it again, when the output stops being a ranking and becomes prose.

---

> **Known** — passage-level judgments exist as a distinct evaluation activity from
> document-level (`trec-overview`) · answer spans as verbatim substrings are a standard
> ground-truth construction (`squad-2016`) · system rankings are relatively stable under
> judgment variation (`voorhees-trec8`)
> **Inferred** — that span-based ground truth is the right trade here because it is
> invariant to chunking. Ours; the alternatives are enumerated above and this is an
> engineering judgment, not a result
> **Derived** — chunk-level judgments must be redone whenever the chunking changes, so they
> cannot be used to compare chunking configurations without recreating the ground truth per
> configuration
> **Unknown** — how sensitive a chunking comparison is to the exact spans chosen. We expect
> substantially, and we have not measured it. If you do, tell your instructor
