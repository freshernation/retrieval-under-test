# k was never a budget

*Week 7 · Day 3 · about 25 minutes*

> By the end of this you can size a context window in the unit the generator charges for.

---

## Sources

| Source | Tier | What it gives you |
|---|---|---|
| [**Liu et al., *Lost in the Middle***](https://arxiv.org/abs/2307.03172) | 1 | Long contexts are not weakly better, so budget is not only money |
| [**Robertson & Zaragoza**](https://www.staff.city.ac.uk/~sbrp622/papers/foundations_bm25_review.pdf) | 1 | Length normalisation — the retriever's own handling of a related problem |

---

## The unit is wrong

Every week so far has retrieved "the top k". A generator does not consume k chunks. It
consumes **words**, and your chunks are not the same size — sections here run from 100 to
300.

So `k = 5` on this corpus is somewhere between 500 and 1,500 words depending on which query
you asked. A range of three, in the quantity you are billed for, and nobody chose it.

Replace `k` with a budget and two things become possible: the cost is a number you set
rather than one that happens, and `answer_density` becomes computable.

---

## Packing

Fill the budget from the ranking, best first, and **stop at the first chunk that does not
fit.**

The tempting alternative — skip it, take a smaller one from further down — is wrong for a
reason worth stating: it silently reorders the window by *size*, so the context no longer
reflects the ranking you spent six weeks building. A 120-word chunk at rank 9 displaces a
280-word chunk at rank 3 because it fits, and now your careful hybrid fusion is a
size-sorted list.

If you want a size-aware selection, that is a knapsack problem and a deliberate choice. It
is not something to arrive at by accident in a packing loop.

---

## Truncation, which is a real trade

Cut the first non-fitting chunk to the remaining space instead of stopping.

**It helps at tight budgets, substantially.** At 200 words, packing whole chunks answers
0.263 of queries — most chunks are bigger than the entire budget, so almost nothing fits and
you send 75 words. Truncating answers **0.474**.

Half a chunk beats no chunk, and that is not obvious in either direction.

**And it can destroy an answer.** A span at the end of a chunk does not survive being cut.
This is week 4's boundary problem, arriving at assembly time — and it is worse here, because
it happens *after* retrieval succeeded. Every retrieval metric you have says the system
worked.

The rule that follows: truncate when the budget is tight relative to your chunk size, and
know that you have introduced a failure mode invisible to everything upstream. Measuring it
requires checking the span against the *packed* text rather than the retrieved chunk, which
is one line and is the kind of line that does not get written.

---

## The frontier, again

| budget | answered | density |
|---|---|---|
| 200 | 0.263 | 0.263 |
| 400 | 0.474 | 0.309 |
| 800 | 0.737 | 0.237 |
| 1200 | 0.737 | 0.146 |
| 2000 | 0.789 | **0.098** |

Same shape as week 4's chunking frontier, same shape as week 5's dimension sweep, same shape
as week 3's `k1` plateau: rises, flattens, no elbow.

And the same procedure: state a requirement — *how often is it acceptable for the answer not
to reach the window, and what will you pay* — and let the frontier select. Going from 800 to
2,000 words buys **five points** for 2.5× the context.

---

## Words are not tokens

One caveat, because it will bite in production.

`word_count` counts whitespace-separated words. A model bills tokens, and for English prose
the ratio is roughly 0.75 words per token — but for the identifier-heavy text in this corpus
it is much worse, because `application/coffee-pot-command` is one word and several tokens.

So a budget in words underestimates your bill, and underestimates it *most* for exactly the
technical corpora where retrieval is most useful. When you have a tokeniser, use it. The
frontier's shape does not change; the numbers on the axis do.

---

> **Known** — a model's use of long context varies with position, so window size has costs
> beyond price (`lost-in-the-middle`) · retrieval models handle length explicitly through
> normalisation (`bm25-foundations`)
> **Inferred** — that skipping a non-fitting chunk silently reorders the window by size.
> Ours, and it follows from what a greedy skip does
> **Derived** — with chunks of 100–300 words, a fixed k corresponds to a word budget varying
> by a factor of three across queries
> **Unknown** — the word-to-token ratio for a given corpus and tokeniser. It is measurable in
> one line once you have a tokeniser and it is routinely assumed instead
