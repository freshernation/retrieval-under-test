# Count the work, not the seconds

*Week 10 · Day 1 · about 20 minutes*

> By the end of this you can explain why a millisecond is not a property of your system,
> and what to report instead.

---

## Sources

| Source | Tier | What it gives you |
|---|---|---|
| [**Lucene**, scoring and query internals](https://lucene.apache.org/core/documentation.html) | 1 | What an inverted index does per query term, and what it skips |
| [**Robertson & Zaragoza**](https://doi.org/10.1561/1500000019) | 1 | The cost model: one postings list per term |
| [**Google SRE Book**, ch. 6](https://sre.google/sre-book/monitoring-distributed-systems/) | 1 | Signals chosen for what they indicate |

---

## The problem with the stopwatch

Time the lexical stage on this course's pipeline and it is 82% of the request. That number
is true, reproducible on this laptop, and almost entirely meaningless, because it is a
statement about a pure-Python inverted index competing against a simulated generator that
returns in under a millisecond.

Put a real model behind the generate stage and lexical becomes 2% of the request. Nothing
about the retrieval changed. Run it on a busy machine and every figure moves. Run it on
somebody else's laptop and you cannot compare notes.

A stopwatch measures **this implementation, on this machine, under this load**. That makes
it the right tool for exactly one job — finding your own slow stage — and the wrong tool
for any number that leaves the room.

---

## What to count instead

Work: the quantity of operations the algorithm requires.

| Stage | Unit | Why it is the right unit |
|---|---|---|
| lexical | postings touched | what the index reads, per distinct term |
| dense | comparisons | one per indexed vector, exhaustively |
| fuse | merges | one per candidate per input ranking |
| assemble | tokens | what the next stage is charged for |
| generate | tokens in, tokens out | the bill, and the latency driver |

These are identical on every machine. They are comparable between two designs — *"this
reranker triples the comparisons"* survives a hardware upgrade in a way that *"this
reranker adds 40ms"* does not. And they are the units a budget should be written in, because
a budget is a design constraint and a design does not have a clock speed.

Seconds go in the logs, where you need them, and nowhere else.

---

## The honest caveats

`work(index, query)` sums the document frequencies of the query's distinct terms. Three
things about that are approximations and all three are worth knowing.

**It assumes the whole postings list is read.** Real engines skip. Lucene's block-max and
WAND-style strategies can terminate early once no unseen document could enter the top k,
which means the count is an upper bound.

**It assumes one consultation per term.** Phrase and proximity queries consult positions
too, which costs more.

**The over-estimate is not uniform.** Pruning helps most when one term is rare and
discriminating — exactly the identifier queries, which are already the cheapest. So the
count probably over-estimates the cheap queries less than the dear ones, which *widens* the
true spread rather than narrowing it.

Say all three in the report. A count with its approximations stated is a measurement; a
count presented as exact is a claim you cannot defend when somebody profiles the real
engine.

---

## This is the stipulated-model discipline again

Week 7 needed a positional weighting and had no generator, so it asserted direction and
forbade quoting a value. Week 8 did it for a simulated generator, week 9 for a simulated
judge.

Week 10 does it for time. The *shape* — which stage dominates, which stage's cost varies,
how the spread behaves — transfers. The *values* in milliseconds do not, and the fence
forbids reporting them.

Four weeks, four applications, one rule: **when a value cannot be checked, assert direction
only.** It has stopped being a technique and become the course's house style, and this is
the week to say so out loud.

---

> **Known** — an inverted index consults one postings list per query term, and real engines
> skip blocks and terminate early rather than reading each list in full (`lucene-scoring`) ·
> document frequency is the length of a term's postings list (`robertson-zaragoza-2009`) ·
> monitoring signals should be chosen for what they indicate (`sre-book`)
> **Inferred** — that work counts belong in a reported budget and wall-clock readings do
> not, because a count is a property of the design and a reading is a property of the
> machine. Ours
> **Inferred** — that pruning reduces the cost of discriminating-term queries more than
> broad ones, so a postings count over-estimates dear queries more than cheap ones and the
> true spread is wider than 269-fold. Ours, and unmeasured
> **Derived** — a stage share measured against a sub-millisecond simulated generator cannot
> predict the same share against a model whose latency is three orders of magnitude larger
> **Unknown** — the real ratio between postings touched and wall-clock time in any
> production engine. It depends on cache residency, which depends on traffic
