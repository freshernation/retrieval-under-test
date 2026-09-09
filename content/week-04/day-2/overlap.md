# Overlap, and how much is enough

*Week 4 · Day 2 · about 20 minutes*

> By the end of this you can compute the overlap your corpus needs instead of copying a
> percentage.

---

## Sources

| Source | Tier | What it gives you |
|---|---|---|
| — | — | **No primary source.** Overlap percentages are Tier 4, like chunk size |
| [**Robertson & Zaragoza**](https://www.staff.city.ac.uk/~sbrp622/papers/foundations_bm25_review.pdf) §3.2 | 1 | Why duplicated text is not free: it changes document frequency and length statistics |

---

## The problem it solves

A fixed window cuts every N words, wherever that lands. Sometimes it lands inside the
sentence that answers a question, and then **neither half contains the answer** — it is
absent from the index at any k, and no ranker, reranker, prompt or model recovers it.

On this corpus, at 200 words with no overlap, that happens to exactly one query. At 60
words it happens to a different one.

Overlap makes consecutive windows share their edges, so a span near a boundary appears whole
in at least one of them.

---

## How much

The usual answer is a percentage — 10%, 20% — and it is folklore of the same kind as chunk
size.

The actual condition is simple enough to state exactly:

> A span of length **L** words survives a chunking of size **S** with overlap **V** if
> every position it could start at leaves room for it: which holds whenever **V ≥ L − 1**.

With `S = 200` and a longest span of 19 words, an overlap of 19 guarantees survival. Your
lab computes the smallest value that actually works on this corpus, which is smaller because
the guarantee is worst-case and the spans do not sit at worst-case positions.

Two things follow, and both are better than a percentage:

**Overlap is a function of your longest answer, not of your chunk size.** Doubling the
chunk size does not double the overlap you need. A 10%-of-chunk-size rule gives you 20 words
at S=200 and 80 at S=800, and the second is seventy words of waste.

**You can compute it.** You have the spans. `smallest_overlap_that_saves` is a loop.

---

## What it costs

Overlap is not free and the costs are worth naming, because "just use overlap" is the
reflex answer and it is not free.

**Index size.** 25 words of overlap at chunk size 200 is roughly 13% more chunks and 13%
more postings. `coverage()` from yesterday reports exactly this, per document.

**Duplicated results.** The same span now appears in several chunks, so a top-5 can contain
the same text twice, spending context on a repeat. Week 7 deduplicates; this week you should
at least look at `carrying_chunks` and see it happen.

**Distorted statistics.** The subtle one. Duplicating text changes document frequency —
a term appearing once in the corpus now appears in two chunks — so **idf shifts**. Not by
much at 13%, and it is a real effect that nobody mentions, and it means an overlapped index
is not scoring quite the same function as a non-overlapped one.

---

## The better answer

Overlap is a patch for cutting in an arbitrary place. Do not cut in an arbitrary place.

Tomorrow's structure-aware chunking cuts on section boundaries, which are places the author
chose as ends of ideas — and an answer span very rarely straddles one. Sections at 100–300
words destroy **no** answers in this corpus with **no overlap at all**.

So the ordering to remember:

1. **Cut where the document says to.** Costs nothing, removes most of the problem
2. **Audit for destroyed spans.** One pass, no retrieval
3. **Add the minimum overlap that fixes what remains** — computed, not a percentage
4. Do not add overlap you have not shown you need

Most systems do step 4 first and skip steps 1 to 3, which is how a 20% overlap ends up in
production protecting against a failure nobody has ever checked for.

---

> **Known** — duplicated text alters document frequency and length statistics, which are
> inputs to the scoring function (`bm25-foundations`)
> **Inferred** — that structure-aware boundaries reduce the need for overlap. Demonstrated
> on this corpus tomorrow; the generalisation is ours
> **Derived** — a span of L words survives a fixed chunking of size S whenever the overlap
> is at least L − 1, since every possible starting position then falls within some window
> that contains the whole span
> **Unknown** — what overlap production systems actually need. The percentages in wide use
> appear to be untested, and testing one costs an afternoon
