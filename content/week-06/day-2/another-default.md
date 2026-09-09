# Another default from somebody else's corpus

*Week 6 · Day 2 · about 20 minutes*

> By the end of this you can recognise the pattern, because it is the third time.

---

## Sources

| Source | Tier | What it gives you |
|---|---|---|
| [**Cormack, Clarke & Buettcher**](https://plg.uwaterloo.ca/~gvcormac/cormacksigir09-rrf.pdf) | 1 | Where 60 came from |
| [**Lin, *The neural hype***](https://sigir.org/wp-content/uploads/2019/01/p040.pdf) | 1 | What untuned components do to a field's published results |
| [**BEIR**](https://arxiv.org/abs/2104.08663) | 1 | Why a value chosen on one collection does not transfer |

---

## The third time

| week | the default | where it came from | its rank here |
|---|---|---|---|
| 3 | BM25 `k1 = 1.2, b = 0.75` | TREC news collections | **38th of 45** |
| 4 | chunk size 512, overlap 10% | a default in an example notebook | dominated at every k |
| 6 | RRF `c = 60` | 2009 TREC runs | captures **0%** of the headroom at k=10 |

Three parameters, three fields, three defaults, and none of them good on this corpus.

The pattern is not that the defaults are bad. `k1 = 1.2` is a perfectly sensible value for
news articles; `c = 60` is a sensible value when the retrievers being fused have noisy
orderings. **The pattern is that a default encodes somebody else's data**, it ships with
the implementation, it is never surfaced as a decision, and so it never gets checked.

---

## What c=60 costs here

At k=10 the oracle is 0.895 and lexical alone is 0.842.

| c | recall@10 | headroom captured |
|---|---|---|
| 1 | 0.895 | **100%** |
| 10 | 0.895 | **100%** |
| 20 | 0.895 | **100%** |
| 60 | 0.842 | **0%** |
| 200 | 0.842 | 0% |

The default produces a fused system that exactly ties the better of its inputs. Every point
of complementarity you spent the week finding is thrown away by a constant nobody chose.

And the failure is silent in the worst possible way: the fusion *works*. It runs, it
returns sensible results, it is better than dense retrieval, and it is not better than the
BM25 you had before. Without the input-by-input comparison from Wednesday, this looks like
a successful week.

---

## Why 60, specifically

The paper is four pages and worth reading for this alone. The authors chose 60 to reduce
the influence of high rankings from individual systems that were, in their setting,
frequently wrong — the fusion was over many TREC submissions of varying quality, and a
large `c` says "I do not trust any one system's top result very much".

Your setting is two carefully built retrievers over your own corpus, one of which you spent
three weeks tuning. Their orderings are not noisy in the way 2009 TREC submissions were.

So the default is not wrong; **it is an answer to a different question**, and the sweep
takes a minute.

---

## The rule, stated once for the rest of the course

> Any constant you did not choose is a hypothesis somebody else tested on data you have
> never seen. Sweep it, report the sweep, and if the default wins, say that — it is a
> result and it is cheap.

The corollary is about reading rather than building. When a write-up reports that hybrid
retrieval improved recall by five points, the questions are: which constant, swept or
default, and compared against **both** inputs. Almost none of them answer any of the three.

---

## What to do when the sweep is flat

Sometimes it will be, and then the right choice is the least surprising one.

`tune_c` breaks ties towards the value nearest 60 for exactly this reason: on a plateau,
picking the conventional value means you will not have to defend it twice, and there is no
evidence to defend a different one with. That is not timidity — it is declining to spend
credibility on a coin flip.

Say in the report that the sweep was flat. That is more informative than the value you
picked.

---

> **Known** — RRF's c=60 was chosen for fusing many TREC submissions of varying quality
> (`rrf-2009`) · untuned components inflated a substantial share of published IR results
> (`lin-neural-hype`) · retrieval results do not transfer between collections
> (`beir-2021`)
> **Inferred** — that a shipped default is systematically under-checked because it is never
> surfaced as a decision. Ours, and this course now has three instances
> **Derived** — a fusion capturing 0% of the available headroom is, by definition, no better
> than its best input, so its value is entirely in the constant
> **Unknown** — what a good default `c` would be for a modern lexical-plus-dense pair.
> Somebody should re-derive it; as far as we can find, nobody has
