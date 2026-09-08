# Building an eval set that can hurt you

*Week 1 · Day 2 · about 25 minutes*

> By the end of this you can build a query set that is capable of telling you your system
> is bad, which is a specific and unusual property.

---

## Sources

| Source | Tier | What it gives you |
|---|---|---|
| [**TREC overview papers**](https://trec.nist.gov/pubs.html) | 1 | How judgment sets get built when the goal is comparability across systems |
| [**BEIR**](https://arxiv.org/abs/2104.08663) | 1 | Eighteen retrieval datasets, and how differently the same models rank across them |

> The eval-set *smells* in this article are ours. They are a checklist assembled from
> teaching, not a published taxonomy, and you should add to them.

---

## The property that matters

An eval set is not a collection of questions. It is **an instrument, and the question about
an instrument is what it is capable of detecting.**

Most eval sets people build cannot detect anything. They are twelve questions the builder
knew the system answered well, judged after seeing the answers, containing nothing the
corpus cannot support. Such a set will report a good number on day one and the same good
number for ever, through six months of the system quietly getting worse.

The test to apply to your own set, and it is uncomfortable:

> **If my system were bad, would this set say so?**

---

## The seven smells

Four of these `smells()` catches. Three it cannot, and those are the dangerous ones.

**Machine-detectable:**

1. **A query with nothing relevant.** Unanswerable. Drags every mean down for reasons that
   have nothing to do with the retriever
2. **A query where everything judged is relevant.** The query cannot punish a bad result —
   any ranking of the judged documents scores the same. **The one that ruins eval sets**,
   and it is invisible in every metric
3. **A judgment for a document not in the corpus.** A typo, or a corpus that changed under
   you
4. **Fewer than three judgments on a query.** Too thin to mean anything

**Not machine-detectable, and worse:**

5. **Every query is the same shape.** Twelve factual lookups. Your set now measures one
   capability and reports it as a system score, and the failures that will actually hurt
   you — the paraphrases, the multi-document questions, the ones with no answer — are
   simply absent
6. **No out-of-scope query.** Nothing in the set can detect the system answering a question
   it should have refused. This is the most common omission in the field and it is the
   failure that reaches users
7. **The judgments were written after seeing the results.** Undetectable by anything, at
   any point, ever. The only defence is the order you work in

---

## Diversity is not a nice-to-have

An eval set's coverage of *query shapes* decides which failures it can see at all. This is
the same argument as measuring station-by-station, one level up: an aggregate over twelve
similar queries hides everything, and it hides it behind a number that looks like evidence.

The shapes worth having, and the failure each one detects:

| Shape | What only it can catch |
|---|---|
| Plain lookup | nothing special — the control |
| Vocabulary gap | that your matching is purely lexical |
| Exact identifier | that your matching has stopped being lexical enough |
| Acronym / expansion | both of the above at once, which is why it is the sharpest single query type |
| Needs two documents | that your system stops at the first plausible passage |
| Answer changed over time | that you have no notion of currency |
| **Out of scope** | that your system will answer anything |
| Negation | that retrieval cannot represent "not" |
| Ambiguous | that your system picks a reading silently |

Twelve queries covering eight shapes is a far better instrument than a hundred covering
two, and it is less work. **Diversity beats volume at small scale**, every time, and small
scale is where you will always be with hand-built judgments.

---

## Dev and test

Split them, from the first day, before you have any reason to care.

`dev` is for tuning. Look at it constantly, overfit it into the ground, that is what it is
for. `test` is for confirming — once per milestone.

The failure this prevents is not dishonesty. It is a completely honest sequence: you try
something, look at `test`, it is slightly worse, you try a variant, look again, it is
better, you ship the variant. Nothing was concealed and nothing was faked. You have also
just used `test` as a tuning set, your reported number is now optimistic by an unknown
amount, and there is no way to recover it — the only fix is judgments you have never seen,
which means more labelling.

Twelve queries makes a four-query held-out split, which is absurdly small. It is still
worth doing, because the *habit* is what transfers, and a habit built when the stakes are
low is the only kind that survives when they are not.

---

## How many queries

More than you have, fewer than you fear.

The honest answer is that it depends on the effect size you want to detect, and week 9
computes it properly. The rough shape: **50 queries is where a paired bootstrap starts
resolving differences of a few points; 12 will only resolve large ones.** Below about 30 you
are measuring your own noise.

So why twelve this week? Because the point of week 1 is that you have judged documents with
your own hands, and twelve well-judged queries teach that in a way that a hundred rushed
ones do not. Your set grows from week 2 onwards, over your own corpus, and by week 9 it is
the thing you are proudest of.

---

## The bias you cannot remove

Your eval set was built by looking at documents that some process surfaced. Documents no
process ever surfaced are graded 0 by default and will be graded 0 for ever.

The mitigation is `unjudged_in_top_k`: every time you change a retriever, look at what it
surfaced that you never judged, and judge it. This does not remove the bias — it just keeps
it from getting monotonically worse as your systems improve, and it gives you a *number*
for it: how many newly-judged documents turned out to be relevant.

State that number in your report. Almost nobody does, and it is the single most informative
thing about an eval set's quality.

---

> **Known** — pooling is standard practice and biases against unpooled documents
> (`trec-overview`) · model rankings differ substantially across retrieval datasets
> (`beir-2021`)
> **Inferred** — that query-shape diversity matters more than query count at small scale.
> Consistent with BEIR's cross-dataset variation, but we know of no direct study
> **Derived** — a query whose judged documents are all relevant produces the same score for
> every ranking of them, so it cannot discriminate between systems
> **Unknown** — the minimum viable size for a hand-built eval set. It depends on the effect
> size you need to detect, which is week 9, and nobody can give you a number without that
