# Growing an eval set is a new instrument

*Week 6 · Day 1 · about 20 minutes*

> By the end of this you can say why the old query file was kept, and what would have gone
> wrong if it had been edited.

---

## Sources

| Source | Tier | What it gives you |
|---|---|---|
| [**TREC overview papers**](https://trec.nist.gov/pubs.html) | 1 | Topic sets versioned per year, and results reported per collection, never pooled across |
| [**Voorhees, TREC-8**](https://trec.nist.gov/pubs/trec8/papers/overview_8.pdf) | 1 | System rankings under judgment variation — stable within a collection, not across |

---

## The situation

Week 5 measured the headroom between lexical and dense retrieval as **zero at every k**. On
that evidence, this week has no subject.

The cause was not the retrievers. Nine answerable queries cannot show a complementarity
that involves one or two queries in each direction — week 3's floor arithmetic, arriving
for the third time. Week 3's milestone asked for thirty dev queries precisely so this would
not happen.

So the course takes its own advice: ten more dev queries, chosen to stress the two
retrievers in opposite directions, and the headroom is no longer zero.

---

## Why the old file was not edited

The obvious move is to add the queries to `queries.yml`. It would have been wrong, and the
reason is the point of the article.

> **An eval set that grows is a new instrument, not a corrected one.**

Weeks 1 to 5 measured a great deal against sixteen queries: a baseline, a BM25 improvement,
a chunking frontier, a dimension sweep, a head-to-head. Edit the file and every one of
those numbers now refers to something that no longer exists — and, worse, *still runs*. The
tests would fail, which is the lucky case; the articles and reports would simply be wrong
while continuing to look fine.

Keeping both files makes the discontinuity visible:

```python
raglab.judgments.load()                              # weeks 1-5: sixteen queries
raglab.judgments.load(file="queries-extended.yml")   # weeks 6+: twenty-six
```

And it makes the honest statement available: **numbers from the two are not comparable.**
Not "roughly comparable" — a system scoring 0.79 on nineteen queries and 0.89 on nine has
not improved, and nothing in either number says so.

---

## The rule

> When the eval set changes, every earlier result becomes a claim about a different
> question. Version it, keep the old one, and say in the report what stopped being
> comparable.

This is what TREC does and has always done: topic sets are per year, results are reported
per collection, and nobody averages across them. It is unglamorous and it is why
twenty-year-old TREC results are still interpretable.

The same rule applies to the changes you make to a set, not only to its size. Re-judging a
query, changing a grade, adding an answer span — each produces a different instrument, and
"we improved the eval set" is a sentence that should always be followed by "so the previous
numbers are not comparable".

---

## What to put in the report

Three sentences, and the milestone requires them:

1. **What changed** — size, and which queries were added or re-judged
2. **Why** — the measurement that could not be made with the old one
3. **What became incomparable** — which earlier conclusions are now unsupported rather than
   refuted

The third is the one people skip, and it is the only one a reader needs.

---

## The uncomfortable question

The ten new queries were chosen deliberately to stress the two retrievers in opposite
directions — identifiers, where lexical is strong, and paraphrases, where dense should be.

That is a defensible design and it is also **a thumb on the scale.** A query set built to
reveal complementarity will reveal complementarity, and the headroom it measures is partly
a property of the set's design.

The honest position: say so. The set is a model of a query distribution and this one models
a distribution containing a lot of both shapes. Whether your users' distribution looks like
that is a separate question, unanswerable from inside, and it belongs in the report as a
limitation rather than being quietly omitted.

---

> **Known** — evaluation collections are versioned and results are reported per collection
> rather than pooled (`trec-overview`) · system rankings are stable within a collection
> under judgment variation (`voorhees-trec8`)
> **Inferred** — that a grown eval set should be a new file rather than an edit. Ours, and
> it follows from results not being comparable across instruments
> **Derived** — a mean over nineteen queries and a mean over nine are not comparable, since
> they are computed over different populations
> **Unknown** — how much of this corpus's measured headroom is a property of the retrievers
> and how much of the query set's deliberate design. We cannot separate them
