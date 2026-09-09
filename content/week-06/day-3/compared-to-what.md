# Compared to what

*Week 6 · Day 3 · about 25 minutes*

> By the end of this you can state a fusion result in a form that survives the only
> question that matters.

---

## Sources

| Source | Tier | What it gives you |
|---|---|---|
| [**Lin, *The neural hype***](https://sigir.org/wp-content/uploads/2019/01/p040.pdf) | 1 | A field's published improvements measured against the wrong baseline |
| [**Cormack, Clarke & Buettcher**](https://plg.uwaterloo.ca/~gvcormac/cormacksigir09-rrf.pdf) | 1 | A fusion paper that does compare against its inputs |
| [**Smucker, Allan & Carterette**](https://dl.acm.org/doi/10.1145/1321440.1321528) | 1 | What establishing a difference requires |

---

## The claim that is true and wrong

> "We added hybrid retrieval and recall improved by five points."

At k=5 on this corpus: fusion 0.737, dense retrieval 0.737, **lexical 0.789**.

Compare the fusion against dense and you have a tie. Compare it against dense at a
different k and you have an improvement. Compare it against the BM25 you already had and
you have a **regression of five points**.

All three comparisons use the same numbers. Nobody lied. And the team has just deployed a
system worse than the one they replaced, with a report saying it is better.

This is not a rare pathology. It is the default outcome of comparing a new system against
*a* baseline rather than against **every input it is built from**, and it is the single
most common failure in applied retrieval work.

---

## The gate

```
beats_all = fused > every input, strictly, at the k you will deploy at
```

Strictly, because a tie is not a reason to add a component: you have doubled the
infrastructure, doubled the latency and doubled the failure modes for nothing.

At the k you will deploy at, because the verdict changes with k and a result at k=3 is not a
claim about k=5.

Against **every** input, because a hybrid has two and it is the weaker one you will
accidentally compare against.

That is three lines of code and it is `ship_check`. At k=5 it refuses, and the sentence it
produces —

> *"We did not ship hybrid retrieval because BM25 alone scored higher at k=5"*

— is a better report than most published ones.

---

## Dilution, and why fusion can lose

`dilution = best_input − fused`, floored at zero. At k=5 here it is 0.053.

The mechanism is worth understanding rather than treating as noise. RRF promotes documents
that **both** retrievers ranked highly. That is exactly what you want when they disagree
usefully. It also means a document that *one* retriever was confidently right about, and
the other simply had no opinion on, gets less support than a document both were lukewarm
about.

At k=3 there is room for disagreement to matter. At k=10 there is room for everything. At
k=5, on this data, the dilution costs more than the complementarity pays.

**Combining two signals can make things worse.** It is not obvious, it is measurable, and
`dilution` is where you look.

---

## Captured, and why it is sometimes None

`captured = (fused − best) / (oracle − best)` — the fraction of available headroom the
fusion took.

It is the right summary because it separates two questions that get conflated: *was there
anything to win* (headroom) and *did the technique win it* (captured). A fusion capturing
100% of a tiny headroom is a good technique on a corpus where fusion does not matter, and
that is a different report from a fusion capturing 30% of a large one.

When there is no headroom, `captured` is **None**, not 0.0 or 1.0. A percentage of nothing
is not a number, and returning one invites a reader to compare it with a percentage of
something.

---

## What to write

Three sentences, at every k you report:

> At k=[N], fusion scored [N] against lexical [N] and dense [N]. The oracle was [N], so the
> available headroom was [N] and the fusion captured [percentage].
> [Shipped / not shipped], because [beats_all / the input that beat it].

Nobody can misread that, and it takes as long to write as the misleading version.

---

> **Known** — comparing against a weak or single baseline inflated a substantial share of
> published IR improvements (`lin-neural-hype`) · the RRF paper compares against its
> individual inputs (`rrf-2009`) · establishing a difference requires paired testing at
> adequate sample size (`smucker-2007`)
> **Inferred** — that `beats_all` should be strict rather than allowing ties, because a tie
> buys infrastructure and latency for nothing. Ours
> **Derived** — a fused ranking scoring below one of its inputs is, for that k, strictly
> worse than not fusing
> **Unknown** — how often published hybrid-retrieval results compare against every input. We
> have not surveyed it and would be surprised if it were most
