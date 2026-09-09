# Chunking is a cost decision

*Week 4 · Day 4 · about 25 minutes*

> By the end of this you can state what chunking bought on this corpus, in a sentence a
> person who does not work on retrieval would act on.

---

## Sources

| Source | Tier | What it gives you |
|---|---|---|
| [**Liu et al., *Lost in the Middle***](https://arxiv.org/abs/2307.03172) | 1 | Long contexts are not weakly better: position within the window changes how information is used |
| [**Robertson & Zaragoza**](https://www.staff.city.ac.uk/~sbrp622/papers/foundations_bm25_review.pdf) §3.2 | 1 | The retrieval model's own handling of length, which chunking is often credited with |

---

## The table

Everything this week produced, in six rows:

| configuration | k | answers found | context words |
|---|---|---|---|
| whole documents | 3 | **100%** | 22,943 |
| whole documents | 1 | 56% | 10,264 |
| fixed 800 | 5 | **100%** | 3,648 |
| fixed 400 | 5 | 78% | 1,926 |
| fixed 200/25 | 10 | **100%** | 1,887 |
| **sections 100–300** | **5** | **100%** | **984** |

Read the first row and the last together. **Identical coverage. Twenty-three times the
cost.**

And read the whole column: no chunking configuration, at any k, found an answer that whole
documents missed. Several lost answers. None gained one.

---

## So what did chunking buy

Not accuracy. Not precision. Not relevance.

**It bought the ability to afford the system**, and that is a real and large thing rather
than a consolation prize.

Say it to somebody who does not work on retrieval:

> "We get the same answers using a twenty-third of the context. At our query volume that is
> the difference between a system we can run and one we cannot."

That sentence is actionable, defensible, and true. Compare it with what the same work is
usually written up as — *"we tuned chunk size to 512 and saw a 3% improvement in relevance"*
— which is a smaller claim, a noisier claim, and probably a false one.

---

## Three costs, one of which is not money

**Tokens.** Twenty-three times the context is twenty-three times the input cost, per query,
for ever. It is also twenty-three times the cost of every experiment you run against it,
which is why an expensive pipeline is a slow pipeline to improve.

**Latency.** Longer contexts take longer to transmit and to process, and this is the cost
users experience directly.

**Attention.** The one that inverts the naive view. A model's use of information in a long
context depends on *where* it is: material in the middle of a long window is used less
reliably than material near either end. So a 22,943-word context is not merely twenty-three
times more expensive than a good 984-word one — **it can also produce worse answers**, while
containing strictly more information.

That is week 7's material and it is the reason "just use a long context window" is not the
end of this conversation. More context is not weakly better and merely pricey. It is pricey
and can be actively harmful, and the pathology is not visible in any retrieval metric.

---

## What this reframing prevents

If chunking is a quality knob, you tune it against nDCG, watch it wobble by two points on
nine queries, pick a winner from noise, and write it up as an improvement. That is the shape
of nearly every chunk-size table published, and week 3's floor arithmetic says most of them
measured nothing.

If chunking is a cost decision, the question is **how little context can I spend and still
have the answer in it** — which has two axes, an explicit requirement, and a frontier.

It also tells you when to stop. There is no optimal chunk size, so there is no search to run
for ever. You pick a point on the frontier and go and do something else.

---

## The honest caveats

**Ten documents.** Whole-document retrieval is perfect here partly because there are ten
documents and the top 3 is a third of the corpus. At ten thousand it would not be, and the
value of chunking would then include coverage as well as cost. We cannot measure where that
turns over with ten.

**BM25's length normalisation is doing work.** Part of what chunking is credited with —
stopping long documents dominating — the scoring function already handles, and week 3's `b`
is where that lives. A retriever without length normalisation would make chunking look far
more valuable than it is.

**Nine answerable queries, binary metric.** Full coverage means "no failures observed", not
"no failures". At n=9 that is a weak statement and the report should say so.

---

> **Known** — a model's use of information in a long context varies with position within the
> window (`lost-in-the-middle`) · length normalisation in the retrieval model addresses
> documents of differing length independently of chunking (`bm25-foundations`)
> **Inferred** — that chunking's value on this corpus is entirely cost rather than coverage.
> Measured here; the generalisation beyond ten documents is ours and is not established
> **Derived** — a configuration that never retrieves an answer a coarser one missed cannot
> have improved coverage, so its value lies elsewhere
> **Unknown** — the corpus size at which whole-document retrieval stops being viable. It
> plainly exists, it is not ten, and we have no way to locate it from here
