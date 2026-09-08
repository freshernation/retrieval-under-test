# Two numbers, eighteen points

*Week 3 · Day 4 · about 25 minutes*

> By the end of this you can tune k1 and b, and list four reasons the result might be
> worthless.

---

## Read the primary sources first

| Source | Tier | What it gives you |
|---|---|---|
| [**Robertson & Zaragoza**](https://www.staff.city.ac.uk/~sbrp622/papers/foundations_bm25_review.pdf) §3.2 | 1 | What k1 and b mean, and the ranges their authors suggest |
| [**Lin, *The neural hype***](https://sigir.org/wp-content/uploads/2019/01/p040.pdf) | 1 | What happens to a field when baselines are compared untuned |
| [**Lucene's BM25Similarity**](https://lucene.apache.org/core/9_9_0/core/org/apache/lucene/search/similarities/BM25Similarity.html) | 1 | The defaults nearly every deployed system is running |

---

## The size of the effect

Forty-five configurations on this corpus, ndcg@3 from **0.710 to 0.886**.

Eighteen points, from two numbers, with no change to the corpus, the index, the analyzer
or the eval set. Tuning is the highest-leverage hour of the week — which is exactly why it
is the easiest place in the course to fool yourself.

Everything today is a **tuning change** in the sense of `EVALS.md`. There is no argument
for `k1 = 2.4` except the number. So the number has to be good, and the rest of this
article is the four ways it is not.

---

## Warning 1 — the defaults are not good here

`k1 = 1.2, b = 0.75` places **38th out of 45**.

That is not a scandal and the defaults are not wrong. They were chosen on TREC collections
of news articles — thousands of documents, a few hundred words each, written in a
consistent register. This corpus is ten technical standards ranging from four to sixty
pages.

The lesson is not "the convention is bad". It is that **a convention is a convention**, it
encodes somebody else's corpus, and you cannot know whether it suits yours without doing
this. Most deployed systems are running 1.2 and 0.75 and have never checked.

---

## Warning 2 — the optimum is at the edge of the grid

The winner is `k1 = 2.4`, the largest value searched.

> **A grid search that returns a boundary value has not found an optimum. It has found the
> edge of your grid.**

This is the most reliable warning sign in parameter tuning and it is trivially checkable.
Widen it:

| k1 | 1.2 | 2.4 | 4 | 8 | 64 |
|---|---|---|---|---|---|
| ndcg@3 | 0.822 | 0.886 | 0.889 | 0.889 | 0.889 |

It rises, then flattens, and never falls. **A plateau extending to infinity.**

`k1 → ∞` means no saturation at all — score by raw term frequency, where the hundredth
occurrence is worth a hundred times the first. That is a substantive claim about this
corpus, it contradicts thirty years of practice, and it is precisely what week 1's
`frequency_score` did when it handed the top slot to the longest document.

So what is going on? Probably: ten documents, all long, few queries, and `b = 0.5` already
handling the length problem — so the saturation curve has little left to do and its exact
shape stops mattering. That is a hypothesis. The point is that **you now have to have
one**, rather than shipping a number because it won.

---

## Warning 3 — you took forty-five looks

Nine queries. Forty-five configurations.

At 95% confidence you expect roughly one in twenty comparisons to look significant by
noise alone, so forty-five looks should produce about two spuriously good results for free.
The winner of a forty-five-way contest is selected partly for being lucky, and there is no
way to tell how much.

This is the multiple-comparisons problem, it applies to every hyperparameter sweep anyone
has ever run, and the standard responses are all unsatisfying at this scale: correct the
threshold and detect nothing; use a separate validation split and have four queries in it;
or **report the number of looks** and let the reader discount it.

The third is what this course does, because it is honest and free. `looks(results)` goes in
the report.

---

## Warning 4 — the gain rides on three queries

`moved_queries` between the tuned configuration and the defaults returns `r01`, `r06`,
`r07`.

The same three that BM25 itself fixed on Wednesday. Six of the nine are untouched by
anything you did all week.

So what has actually been tuned is those three queries. Whether `k1 = 2.4` generalises is
the question of whether those three are representative — and with nine queries you cannot
answer it, which is the whole of tomorrow's milestone.

---

## And then it generalises anyway

On the held-out split the tuned configuration scores **0.962** against the defaults'
**0.917**.

It worked. You were right.

Now notice what that is worth: six test queries, one read. All four warnings above are
still true. The optimum is still on a boundary, you still took forty-five looks, the gain
still rides on three dev queries, and the tuner is still asking you to disable saturation.

> **You got away with it, and nothing available from the inside distinguishes getting away
> with it from being right.**

A held-out number that confirms a badly-founded choice is the most dangerous result in
applied retrieval, because it retires the doubt. Had it come back worse, you would have
gone looking for the reason and found the four warnings. It came back better, so you will
not — unless you decide, in advance, that the warnings are reportable regardless of which
way the confirmation goes.

That is the actual discipline. Not "check the held-out split", which everyone agrees with,
but **write down the warnings before you look**, and report them whichever way it lands.

---

## What to do

1. Tune on `dev`, always
2. Report `spread`. A grid spanning 0.71–0.89 says the parameters matter; one spanning
   0.882–0.886 says stop tuning and go and do something else
3. Report `rank_of` the defaults. If they are near the top, ship them — you have saved
   yourself a portability problem for nothing
4. Check `at_edge`. Widen until you find an interior optimum or understand the plateau
5. Report `looks`
6. Report `moved_queries`
7. Prefer the *least extreme* configuration on a plateau. On a flat region the smallest
   values are the most likely to survive contact with other data, which is why
   `grid_search` breaks ties towards smaller parameters

---

> **Known** — k1 and b have conventional ranges chosen on news collections
> (`bm25-foundations`) · Lucene's defaults are 1.2 and 0.75 and are what most deployed
> systems run (`lucene-bm25`) · comparing against untuned baselines inflated a substantial
> share of published IR improvements (`lin-neural-hype`)
> **Inferred** — that preferring the least extreme configuration on a plateau generalises
> better. Standard practice, and we know of no direct study
> **Derived** — at a 95% threshold, forty-five independent comparisons should produce about
> two apparently significant results from noise alone
> **Unknown** — what fraction of deployed BM25 systems have ever tuned k1 and b on their own
> corpus. Every practitioner we have asked says "none of mine"
