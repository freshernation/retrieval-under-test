# Milestone 5 — A dense retriever, and an honest comparison

> **Ship:** a fitted dense retriever frozen with a manifest, a side-by-side comparison at
> four values of k, and `REPORT.md` that does not claim a winner.

---

## The brief

### 1. Fit and freeze

`DenseRetriever(dims=...).fit(chunks)` over **your** week-4 chunking, then `freeze()` to a
`.npy` and a manifest that `raglab.vectors.load` accepts.

The manifest is the deliverable people skip. Embeddings are a frozen artefact of a
representation at a version; a matrix with no record of what made it is a matrix you cannot
compare with anything in six months.

### 2. Sweep the dimensions

At least four values. Report answer recall and the variance kept at each. There is no elbow
here — it rises and flattens — so present it as a frontier, exactly as you presented chunk
size, and choose with a requirement rather than by eye.

### 3. Compare, at four values of k

`side_by_side` against your week-3 BM25 over the same chunks. For each k: both recalls, the
oracle, the headroom, and the four-way tally.

**The report must state the k at which each claim holds.** If your winner flips, say so in
the first paragraph rather than picking the k where your preferred system wins.

### 4. Check comparability

`is_comparable` between every pair of configurations you report. Two indexes over different
chunkings are different corpora, and a score difference between them is not attributable to
anything you chose.

### 5. Decide whether week 6 is worth it

Headroom, at every k, on your dev split. Then one paragraph: **is fusion worth a week?**

If your headroom is zero, say so and say what you would need to establish otherwise. That
is a legitimate finding and it is a better report than one that assumes the answer.

### 6. Confirm once on `test`, and write `REPORT.md`

---

## The rubric

| Station | This week |
|---|---|
| 1 Corpus | One sentence: LSA learns its axes from your corpus. What does that mean for a query using a word your corpus never contains? |
| 2 Chunk | One sentence on why the dense index is not comparable across chunkings |
| 3 Index | **The week.** The space, the dimensions, the freeze, the manifest, the ANN structure |
| 4 Retrieve | The comparison, at four k, with the flip stated |
| 5 Rank | One sentence on what cosine is doing that BM25's `b` was doing |
| 6 Generate | Not built. One sentence: dense retrieval returns a chunk with no matching terms. How would you cite it? |
| 7 Measure | Headroom, and the decision about week 6 |

---

## The bar

- `pytest week-05 -v` green, `tools/check_evals.py` green
- A frozen `.npy` and manifest that `raglab.vectors.load` accepts
- Dimension sweep, at least four points
- Comparison at four k, with tally, oracle and headroom at each
- `is_comparable` checked between reported configurations
- Exactly one `test` run this week
- You survive Friday

---

## What you will want to do and should not

**Report the k where your preferred system wins.** The flip is the finding.

**Fuse the two.** It is next week and the fence forbids it, and the point of Wednesday is
that you now know whether it is worth doing.

**Call this an embedding model.** It is latent semantic analysis over your own corpus, it
has one limitation a trained model does not have, and the report should name it.

**Conclude that dense retrieval is better or worse.** Nine queries. One query is eleven
points.
