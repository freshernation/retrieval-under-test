# How many dimensions

*Week 5 · Day 2 · about 20 minutes*

> By the end of this you can choose a dimension count the way you chose a chunk size, and
> say why "90% of the variance" is the wrong justification.

---

## Sources

| Source | Tier | What it gives you |
|---|---|---|
| [**Deerwester et al.**](https://asistdl.onlinelibrary.wiley.com/doi/10.1002/(SICI)1097-4571(199009)41:6%3C391::AID-ASI1%3E3.0.CO;2-9) | 1 | The original, which reports dimension counts chosen empirically |
| [**MTEB**](https://arxiv.org/abs/2210.07316) | 1 | Modern embedding models compared, at the dimensions their authors shipped |

---

## It is the same shape as chunk size

| dims | variance kept | answer recall@5 |
|---|---|---|
| 16 | 24% | 0.40 |
| 32 | 34% | 0.67 |
| 64 | 51% | 0.73 |
| 128 | 74% | 0.80 |
| 192 | 90% | **0.87** |
| 256 | 100% | 0.87 |

It rises and flattens. **There is no elbow**, no optimum, and no principled place to stop —
exactly like week 4, and exactly like week 3's k1 plateau.

So treat it exactly as you treated chunk size: a **frontier** with cost on the other axis
(memory, and the comparisons in Thursday's index), and a requirement that selects a point.

---

## Why variance is the wrong criterion

"Keep 90% of the variance" is the standard rule of thumb and it is answering the wrong
question.

**Variance is not relevance.** The directions explaining the most variance describe what
your corpus is *mostly about*; the directions that distinguish one chunk from another may be
much weaker. On this corpus the strongest direction is essentially "is this the cookies
RFC", which is a large share of the variance and no help to any query.

The test is empirical and you have it: **answer recall against dimensions**. That measures
the thing you care about, and it disagrees with the variance curve — 128 dimensions keeps
74% of variance and gets 92% of the achievable recall.

Report both. Quote only the second.

---

## What the numbers mean and do not

Two cautions before anyone takes a number from that table anywhere.

**191 of 266.** Ninety percent of the variance needs seventy percent of the directions,
which is barely a compression. Ten technical standards on adjacent subjects do not repeat
themselves much. On a corpus of a million chunks the ratio would be wildly different, and
nothing here predicts it.

**Nine queries, binary metric.** Every value in that column is a multiple of 1/9. The
difference between 0.80 and 0.87 is *one query*, and week 3's floor arithmetic says a
difference of one query is not a result.

So the table is a shape, not a set of measurements. The shape — rises, flattens, no elbow —
is the transferable part.

---

## What real models do

You do not choose dimensions for a trained embedding model. It ships at 384, 768, 1024 or
1536 and that is a property of the model.

Two things follow, and the second is where the money is.

**Dimensionality is now a model-selection decision**, bundled with everything else about the
model, so you cannot trade it independently.

**Storage and search cost scale with it, linearly.** A million chunks at 1536 float32
dimensions is about 6 GB, at 384 it is 1.5 GB, and every query's comparisons scale the same
way. Which is why quantisation — storing 8-bit or 1-bit approximations — is standard
practice: it is the same trade you are making today, moved from "how many dimensions" to
"how precise is each one".

Some recent models are trained so that a *prefix* of their dimensions is usable on its own,
which puts today's knob back in your hands. If you use one, the sweep above is the procedure
for setting it, and the criterion is still answer recall rather than variance.

---

> **Known** — LSA dimension counts are chosen empirically rather than derived
> (`deerwester-1990`) · deployed embedding models ship at fixed dimensionalities
> (`mteb-2022`)
> **Inferred** — that variance kept is the wrong selection criterion because variance is not
> relevance. Ours, and the disagreement between the two curves here is the evidence
> **Derived** — with nine binary-scored queries every recall value is a multiple of 1/9, so
> adjacent rows of the sweep differ by one query
> **Unknown** — how the variance-versus-recall gap behaves on a large corpus. We would expect
> it to widen and have no way to check from here
