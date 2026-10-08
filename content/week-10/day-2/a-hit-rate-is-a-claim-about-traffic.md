# A hit rate is a claim about traffic

*Week 10 · Day 2 · about 25 minutes*

> By the end of this you can explain why your eval set cannot measure a cache, and why
> every hit rate you have ever read was a statement about an assumption.

---

## Sources

| Source | Tier | What it gives you |
|---|---|---|
| [**Breslau et al.**, *Web Caching and Zipf-like Distributions*](https://doi.org/10.1109/INFCOM.1999.749260) | 1 | Request popularity is Zipf-like, and what that implies for hit rate against cache size |
| [**RFC 9111**, HTTP Caching](https://www.rfc-editor.org/rfc/rfc9111.html) | 1 | Freshness, staleness and revalidation, specified rather than folklore |
| [**Google SRE Book**, ch. 6](https://sre.google/sre-book/monitoring-distributed-systems/) | 1 | Choosing what to measure |

---

## Start with the thing that should stop you

Run a cache over the eval set. Twenty-six queries, **twenty-six distinct keys**, hit rate
**zero**. Normalise the keys — lowercase, strip punctuation, collapse whitespace — and
nothing collides. Still zero.

This is not a flaw in the eval set. It is the eval set working correctly: duplicates would
*weight* it, so a well-built judgment set has none by construction. Which means the
instrument nine weeks of this course went into building is **structurally unable** to
produce the number this day is about.

That is worth sitting with, because it is the general case. An eval set measures quality
per query. A cache's value is a property of the *distribution of queries over time*, and
nothing about the eval set encodes time or repetition. Two different objects, and the
nine-week habit of reaching for the eval set gives the wrong answer rather than no answer.

---

## So where does a hit rate come from

Simulation, and the simulation is the result.

One LRU, capacity five, three assumptions about traffic over the same twenty queries:

| assumed skew | hit rate |
|---|---|
| 0 — uniform | 0.19 |
| 1 — Zipf | 0.30 |
| 2 — concentrated | **0.79** |

**Four-fold**, from one parameter typed into a generator. The code is identical. The cache
is identical. The only thing that changed is a belief about what people ask.

And the hit rate is, nearly always, the figure that justifies the cache.

Breslau et al. is the reason skew 1 is the respectable default: web request popularity is
Zipf-like, which is a real and well-replicated finding. But *your* traffic's exponent is an
empirical question about your product, and the paper does not answer it for you. Borrowing
the shape and inventing the parameter produces a number with a citation attached and no
evidence underneath.

---

## The unbounded case, and why it is not reassuring

With no capacity limit, the uniform stream and the Zipf stream give the **same** hit rate:
0.800 and 0.800.

Of course they do. An unbounded cache keeps everything it has ever seen, so its hit rate is
`1 - distinct / requests`, and both streams eventually touch all twenty queries. The shape
of the distribution is irrelevant.

Which means a hit rate measured against an unbounded cache is not evidence about traffic at
all — it is a restatement of how many distinct queries appeared in the window. Report it and
somebody will reasonably believe you measured something.

---

## The metric that is not the hit rate

Day 1 measured a 269-fold spread in query cost. So:

Cache the ten cheapest queries and **18%** of the work goes away. Cache the ten dearest and
**82%** does. Same ten entries. Same 0.50 hit rate. **Four and a half times** the saving.

Hit rate counts requests. You were not trying to avoid requests; you were trying to avoid
work. These are the same number only when popularity and cost are uncorrelated — and in a
real system they are correlated in the unhelpful direction, because the popular queries are
the short ones and the short ones are cheap.

So the pair to report is **hit rate and work saved**, and the second one is the one the
capacity decision should be made on.

---

## One counter settles it

The honest fix is not a better simulation. It is a counter.

Log a hash of the normalised query key and count distinct keys per hour. That single number
gives you `1 - distinct / requests` for the real traffic, which is the unbounded ceiling,
and it costs one hash and one set per window. Nothing about it is sensitive and nothing
about it is expensive.

Almost nobody has it, and almost everybody has a hit-rate target.

---

> **Known** — request popularity in web traffic is Zipf-like, and hit rate grows roughly
> logarithmically with cache size under that assumption (`breslau-1999`) · HTTP specifies
> freshness and revalidation rather than leaving staleness to convention (`rfc-9111`)
> **Inferred** — that an eval set cannot measure a cache, because a judgment set is built
> without duplicates and a cache's value is a property of repetition over time. Ours, and
> demonstrated here at 26 distinct keys from 26 queries
> **Inferred** — that popular queries are systematically cheaper than rare ones, so hit
> rate over-states work saved in real traffic. Ours, and the direction follows from day 1's
> cost spread rather than from any measurement of real traffic
> **Derived** — an unbounded cache's hit rate equals `1 - distinct / requests` and is
> therefore independent of the popularity distribution, which is why uniform and Zipf
> streams both give 0.800 here · caching the dearest half of this query set saves 82% of the
> work against 18% for the cheapest half, at an identical hit rate
> **Unknown** — the skew of any real RAG product's query distribution. Measurable with one
> counter and, as far as we can find, not reported anywhere
