# Three ideas and one formula

*Week 3 · Day 3 · about 30 minutes*

> By the end of this you can derive BM25's three components from the defects they fix, and
> say what each parameter does.

---

## Read the primary sources first

| Source | Tier | What it gives you |
|---|---|---|
| [**Robertson & Zaragoza, *The Probabilistic Relevance Framework: BM25 and Beyond***](https://www.staff.city.ac.uk/~sbrp622/papers/foundations_bm25_review.pdf) §3 | 1 | The derivation, from the people who did it. §3.2 for k1 and b specifically |
| [**Robertson, *Understanding inverse document frequency***](https://www.staff.city.ac.uk/~sbrp622/papers/foundations_bm25_review.pdf) | 1 | Why idf has the form it does, rather than any other decreasing function |
| [**Lucene's BM25Similarity**](https://lucene.apache.org/core/9_9_0/core/org/apache/lucene/search/similarities/BM25Similarity.html) | 1 | The formula as actually implemented, including where it differs from the paper |

---

## The formula

$$\text{score}(q, d) = \sum_{t \in q} \text{idf}(t) \cdot \frac{tf_{t,d} \cdot (k_1 + 1)}{tf_{t,d} + k_1 \cdot \left(1 - b + b \cdot \frac{|d|}{\text{avgdl}}\right)}$$

It looks worse than it is. Three ideas, each fixing one defect you named in week 1 and
could not repair.

---

## Idea 1 — a rare term tells you more

$$\text{idf}(t) = \ln\left(1 + \frac{N - df_t + 0.5}{df_t + 0.5}\right)$$

On this corpus:

| term | documents | idf |
|---|---|---|
| `status` | 10 of 10 | **0.047** |
| `code` | 10 of 10 | 0.047 |
| `429` | 1 of 10 | **1.992** |

Forty times the weight. That is week 1's first defect — *every term is worth the same* —
repaired by one logarithm, and repaired **from the corpus** rather than from a list
somebody wrote in advance.

Two details worth having:

**Why a logarithm.** Not because logarithms are pleasant. It falls out of a probabilistic
argument: idf approximates the log-odds that a document containing the term is relevant,
under the assumption that terms are independent. The assumption is false and the estimator
is robust anyway, which is the honest summary of a lot of information retrieval.

**Why the halves.** Without them, a term in all N documents gives `ln(1 + 0/N) = 0` exactly
— it contributes nothing, so a query made only of common words returns nothing at all
rather than something weak. The smoothing keeps it barely alive, which is almost always
what you want. Some formulations produce *negative* idf for very common terms and then have
to clamp it, which is worth knowing when a library's numbers surprise you.

---

## Idea 2 — the tenth occurrence is not worth ten times the first

$$\frac{tf \cdot (k_1 + 1)}{tf + k_1}$$

At `k1 = 1.2`:

| tf | 1 | 2 | 10 | 100 |
|---|---|---|---|---|
| contribution | 1.00 | 1.38 | 1.96 | 2.17 |

A hundred occurrences are worth barely twice one. That is week 1's second defect — the
eleven-page document winning by repetition — repaired.

The shape is right for a reason you can state: the difference between a document
mentioning a term **once** and **not at all** is enormous, and the difference between
twenty and twenty-one times is nothing. A linear count gets both of those wrong.

`k1` controls how fast it flattens. At `k1 = 0` every term is binary — present or absent,
repetition worth nothing at all. As `k1 → ∞` it approaches raw counting. The conventional
1.2 to 2.0 is a *convention*, and tomorrow you find out what this corpus thinks.

---

## Idea 3 — a long document has more chances to match

$$1 - b + b \cdot \frac{|d|}{\text{avgdl}}$$

This corpus: shortest 1,247 tokens, longest 19,462. **Fifteen times.** Without
normalisation every query lands on RFC 3986, which is exactly what week 1's
`frequency_score` did.

`b = 0` disables it. `b = 1` divides fully by relative length. The default 0.75 is three
quarters of the way, and the reason it is not 1 is a real tension: **a long document
genuinely is more likely to be relevant** — it covers more ground — so full normalisation
punishes it for a property that is partly a virtue. `b` is where you express your opinion
about that trade, per corpus.

### Where the normalisation goes

In the denominator, **multiplied by k1** — not applied to the whole term:

$$\frac{tf \cdot (k_1 + 1)}{tf + k_1 \cdot B}$$

This matters and is easy to get wrong. Because `B` scales `k1`, a long document needs
*more* occurrences to reach the same saturation, so length interacts with the saturation
curve rather than scaling the final score. Divide at the end instead and you get a working
retriever with subtly wrong behaviour — the worst kind of bug, because everything passes
and the numbers are merely slightly off.

---

## Why it is a sum

BM25 scores each query term independently and adds. That is a bag-of-words assumption and
it is **wrong**: `not` before a term, word order, and multi-word concepts all carry meaning
that summation discards.

It is also extraordinarily hard to beat. Every attempt to model term dependence adds
parameters, adds fragility, and buys a few points on some collections and loses them on
others. Thirty years on, BM25 remains the baseline that new methods are measured against,
and a startling number of them lose to it once it is tuned — which was Lin's finding in
week 1's reading.

**Know that the assumption is false.** It is the reason `r02` — "how do I tell a client to
slow down" — is still broken after today, and it is week 5's opening.

---

## What today buys

On the dev split: ndcg@3 from **0.651 to 0.805**, recall@3 from **0.759 to 0.963**, and
nothing gets worse. It is the largest clean improvement in the course, from about forty
lines that were fully understood by 1994.

Three of the nine answerable queries improve. Six do not — four were already perfect, and
two are still broken and will stay broken until week 5.

---

## Where this is now

BM25 is the default scoring function in Lucene, Elasticsearch and OpenSearch, and has been
since roughly 2015 in the first two — before that it was a tf-idf variant, and switching
was an improvement they published.

Modern practice pairs it with a dense retriever rather than replacing it (week 6). The
reason is precisely today's material: an exact-identifier query like `451` is a problem
BM25 solves *correctly*, not merely adequately, and no amount of semantic similarity
improves on being right.

---

> **Known** — idf derives from a probabilistic argument under a term-independence
> assumption, and the smoothing constants prevent a zero or negative weight for universal
> terms (`bm25-foundations`) · k1 controls saturation and b controls length normalisation,
> with the normalisation multiplying k1 in the denominator (`bm25-foundations`,
> `lucene-bm25`) · BM25 is the default similarity in Lucene-based engines (`lucene-bm25`)
> **Inferred** — that the sum-over-terms independence assumption is why the vocabulary-gap
> query survives this week. Follows from the model; the attribution to this specific query
> is ours
> **Derived** — with the halves, a term present in all N documents has idf `ln(1 + 0.5/(N +
> 0.5)) > 0`, so it contributes weakly rather than not at all
> **Unknown** — how much of BM25's durability is the model and how much is that it is the
> tuned baseline everyone else is measured against. Lin's argument suggests the second is
> larger than assumed
