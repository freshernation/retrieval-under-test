# The metrics

*Week 1 · Day 3 · about 30 minutes*

> By the end of this you can pick a metric for a situation and say what it will not tell
> you — which is the harder half.

---

## Read the primary sources first

| Source | Tier | What it gives you |
|---|---|---|
| [**Järvelin & Kekäläinen, *Cumulated gain-based evaluation***](https://dl.acm.org/doi/10.1145/582415.582418) | 1 | nDCG, from the people who defined it, including why the discount is logarithmic |
| [**TREC overview papers**](https://trec.nist.gov/pubs.html) | 1 | MAP, and the conventions the field actually reports |
| [**Robertson & Zaragoza**](https://www.staff.city.ac.uk/~sbrp622/papers/foundations_bm25_review.pdf) §2 | 1 | The evaluation framing the ranking model was built against |

---

## One idea, five compressions

Every metric here takes a ranked list plus judgments and returns one number. That number is
a *compression*, and the only interesting question about any of them is what got thrown
away.

| Metric | Keeps | Throws away |
|---|---|---|
| **recall@k** | did we find them | where they are, and what else came back |
| **precision@k** | how much of the top k is useful | where they are, and how many we missed |
| **MRR** | where the first one is | everything after the first one |
| **nDCG@k** | position and grade | anything past k |
| **MAP** | position of all of them | grades — it is binary |

Nobody's system is summarised by one of these. Report two, always, and pick them so their
blind spots do not overlap.

---

## recall@k — the station-4 metric

*Of this query's relevant documents, what fraction is in the top k?*

The first number to compute and the one that gates everything else. **If the document is
not in the candidate set, no downstream stage can put it in the answer.** Every hour spent
on ranking while recall is low is an hour spent reordering things that are all wrong.

The trap is `k`, and it is not subtle:

> Recall@10 over 30 documents is asking for a third of the corpus. Recall@10 over three
> million is asking for 0.0003%. They are written down identically.

Whenever you see a recall figure, ask for the corpus size, and put yours next to your own.
This is the single most common way a retrieval number is quoted misleadingly, and it is
usually not deliberate.

---

## precision@k — the one everyone misreads

*Of the top k, what fraction is relevant?*

The misreading: **precision@10 is capped by how many relevant documents exist.** A query
with three relevant documents cannot exceed 0.3, no matter what. Averaging precision@10
across queries with different numbers of relevant documents produces a number describing
your judgments as much as your system.

Divide by `k`, not by however many results you returned. A retriever that returns three
results and gets all three right left seven slots empty and the metric should say so.

In RAG, precision has a cost you can point at: every irrelevant chunk in the context window
is tokens you paid for, latency you spent, and — week 7 — a chance for the generator to be
distracted by the wrong passage. It is the metric that turns into money.

---

## MRR — the one that stops caring

*1 / the rank of the first relevant document.*

Right for one situation and wrong for most: a user who reads the top result and nothing
else. In every other case it is actively misleading, because two systems can have identical
MRR while one found all four relevant documents and the other found one and then four
irrelevant ones.

For RAG specifically, where you are assembling five or ten passages into a context, MRR is
close to meaningless and it is reported constantly.

---

## nDCG@k — the station-5 metric

Two ideas stacked:

**Gain.** Grade 3 is worth more than grade 2. The convention is `2^g - 1`, which makes a
grade 3 worth seven times a grade 1.

**Discount.** Position 1 is worth more than position 5. The convention is `1 / log2(i + 1)`.

Then divide by the best possible arrangement of these judgments, so the number is in [0, 1]
and can be averaged across queries with different numbers of relevant documents. That
normalisation is the whole reason nDCG exists.

**Both conventions are choices, not truths.** Neither was derived from user behaviour, and
different tools use different gains — some use linear `g` instead of exponential, which
changes rankings and is rarely stated in a results table. Know which yours uses.

### The pair that does the diagnostic work

| recall@50 | nDCG@10 | What it means |
|---|---|---|
| low | low | station 4. The documents are not being found |
| **high** | **low** | **station 5. Found, and ordered badly. Different afternoon entirely** |
| high | high | retrieval is fine. Look at stations 1, 2 and 6 |

Compute both, every time. This is the most useful thing in the day.

---

## Where these all break for RAG

Every metric above assumes you are ranking documents for a person to read. A RAG system
does something else: it takes the top k, concatenates them into a window, and generates.
Three consequences the classical metrics do not capture:

- **Redundancy is free in IR and expensive here.** Five chunks saying the same thing score
  well on precision and waste 80% of your context. Week 7 is about this
- **Position within the window matters differently.** Not a log discount — models attend
  unevenly to long contexts, and the shape is not the shape nDCG assumes
- **The unit is a chunk, not a document.** Once week 4 starts splitting documents, "the
  relevant document" needs a definition, and your judgments were written about documents

None of that makes these metrics wrong. It makes them **necessary and insufficient**, which
is the honest position: they measure retrieval, retrieval sets the ceiling, and week 8 adds
the metrics that measure what happens under the ceiling.

---

## Where this is now

The RAG literature has grown its own metric vocabulary — faithfulness, answer relevance,
context precision, context recall — mostly popularised by evaluation frameworks rather than
by papers. Several of them are the classical metrics renamed. "Context recall" is recall.
Knowing that saves you from believing you have learned something new, and week 9 goes
through the mapping.

---

> **Known** — nDCG's normalisation exists to make cross-query averaging valid
> (`jarvelin-2002`) · MAP is the TREC convention (`trec-overview`)
> **Inferred** — that recall and nDCG together localise a failure to station 4 versus
> station 5. This follows from what each metric ignores; the framing is ours
> **Derived** — precision@k is bounded above by `min(k, relevant) / k`, so it is not
> comparable across queries with different numbers of relevant documents
> **Unknown** — whether the log discount matches attention over a language model's context
> window. It was not designed to, and we have found no study aligning the two
