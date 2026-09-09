# Week 5 report — [your name]

> Template. Replace everything in brackets. Every number carries
> `metric value (run:<id>)` or `tools/check_evals.py` fails.

---

## The headline, and it is not a winner

[One paragraph. At k=[N] dense scores [N] and lexical [N]; at k=[N] it is the other way
round. State the flip before anything else, because a reader who takes one number away
should take that one.]

---

## Station 3 — the space

**Chunks** [N] · **vocabulary** [N] · **sparsity of the term matrix** [N]% ·
**dimensions** [N] · **variance kept** [N]%.

### The dimension sweep

| dims | variance kept | answer recall@5 (run:<id>) |
|---|---|---|
| | | |

[No elbow. Present it as a frontier and say which requirement selected your point.]

### The frozen artefact

`[path]`, [N] × [N], manifest records [what]. `raglab.vectors.load` accepts it.

[One sentence on what the manifest is for, in terms of a mistake it prevents.]

### The approximate index

| nprobe | ANN recall | comparisons | answer recall |
|---|---|---|---|
| | | | |

[The compounding, in two sentences. And whether an approximate index is worth having at
this corpus size — the answer is no, and the report should say so.]

---

## Station 4 — the comparison

| k | lexical | dense | oracle | headroom | both / lex-only / dense-only / neither |
|---|---|---|---|---|---|
| 1 | | | | | |
| 3 | | | | | |
| 5 | | | | | |
| 10 | | | | | |

**Comparability:** `is_comparable` holds between [which configurations]. [Anything that
failed, and why it was not comparable.]

### By query family

| family | n | lexical | dense |
|---|---|---|---|

[Report `n`. Most families have one or two queries and the table is suggestive rather than
evidence — say so here rather than letting a reader assume otherwise.]

---

## Station 7 — is week 6 worth it?

**Headroom at k = 1, 3, 5, 10:** [N], [N], [N], [N].

[One paragraph. If it is zero: say so, say that fusion cannot help on this evidence, and
say what you would need. If it is not zero: name the queries that produce it and say
whether one query is enough to justify a week.]

---

## Stations 1, 2, 5 and 6

**1 Corpus** — [one sentence: what does it mean that the representation learned its axes
from your corpus, for a query using a word your corpus never contains?]

**2 Chunk** — [one sentence on why the dense index is not comparable across chunkings.]

**5 Rank** — [one sentence: cosine and BM25's `b` are both length normalisation. What is
the difference?]

**6 Generate** — not built. [One sentence: dense retrieval returns a chunk sharing no term
with the query. How would you cite it, and would a reader believe the citation?]

---

## Confirmed on the held-out split

**[metric] [N] (run:<id>)**, n=[N], configuration [which], k=[N]. Read once.

---

## The failure library

Two cards. At least one about the comparison rather than either retriever.

1. **[title]** — station [N] · found by [diagnostic] · [what it cost]
2. **[title]** — station [N] · found by [diagnostic] · [what it cost]

## What I would not defend

[One honest paragraph.]
