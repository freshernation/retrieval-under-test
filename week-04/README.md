# Week 4 — Chunking, and what it is actually for

> **Destination**
> Choose a chunking strategy from a measured frontier of answer coverage against context
> cost, and be able to say why the number everyone recommends is on nobody's frontier.

This is the week with **no primary source**. There is no peer-reviewed result telling you
what chunk size to use, because the answer depends on a corpus and a query distribution
nobody else has. Every number you have read — 512 tokens, 10% overlap, 1000 characters —
traces back to a default in an example notebook.

So the course does the only honest thing available: measures it on your corpus, and shows
you the method rather than the number.

---

## The week

| Day | Folder | What you'll be able to do |
|---|---|---|
| Mon | `day-1/` | Cut documents into windows — and find your evaluation cannot see it |
| Tue | `day-2/` | Build ground truth at the right granularity, and catch a destroyed answer |
| Wed | `day-3/` | Chunk on the document's own boundaries, and pack the result |
| Thu | `day-4/` | Draw the coverage/cost frontier and pick a point on it |
| Fri | `milestone/` | Ship the chunker and the frontier, then defend the decision |

---

## Monday goes wrong on purpose

You will cut the corpus into 200-word windows. A boundary will land inside the sentence
that answers a query, and after chunking **no chunk in the corpus contains that answer** —
it is present in the corpus and unretrievable at any k.

Adding overlap rescues it. Your document-level metric scores the rescue as a **regression**,
0.834 down to 0.779, with four queries moving down to say so.

And the destroyed answer never appears in the number at all, because that query is in the
held-out split.

Two independent failures at once: the metric is at the wrong granularity to see span
destruction, and the split you tune on does not contain the case. Neither is fixed by more
queries or better statistics — which is why Tuesday changes the ground truth instead.

---

## The week's result

| | answers in the top k | words of context |
|---|---|---|
| whole documents, k=3 | **100%** | 22,943 |
| fixed 800-word windows, k=5 | **100%** | 3,648 |
| fixed 400-word windows, k=5 | 78% | 1,926 |
| **sections packed to 100–300, k=5** | **100%** | **984** |

Twenty-three times less context, for identical coverage.

And note what is *not* in that table: chunking never once retrieved an answer that whole
documents missed. Three days of measurement and the unchunked baseline is perfect.

> **You do not chunk because it retrieves better. You chunk because 22,943 words is a bill
> you cannot pay** — in money, in latency, and in week 7 in a generator's attention.

Anyone who tells you their chunk size improved answer quality is describing a different
measurement from this one, and it is worth asking which.

---

## Milestone

A chunker chosen from a frontier, with the two numbers that decision needs stated
explicitly. Spec in `milestone/README.md`.

---

## What this week is not about

Finding the optimal chunk size. There is not one, and the search for it is the wrong
shape: the decision has two axes and an optimum needs one.

The transferable thing is the procedure — audit for destroyed answers, measure coverage
against cost, plot the frontier, choose a point with a requirement rather than a
preference. It works on a corpus nobody has blogged about, which no chunk size does.
