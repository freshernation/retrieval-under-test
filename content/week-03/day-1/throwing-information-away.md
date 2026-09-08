# Throwing information away in advance

*Week 3 · Day 1 · about 25 minutes*

> By the end of this you can say why stopword lists and stemmers are guesses, and what the
> alternative is.

---

## Sources

| Source | Tier | What it gives you |
|---|---|---|
| [**Robertson & Zaragoza**](https://www.staff.city.ac.uk/~sbrp622/papers/foundations_bm25_review.pdf) §3.1 | 1 | idf as the principled version of what a stopword list approximates |
| [**Porter, *An algorithm for suffix stripping***](https://tartarus.org/martin/PorterStemmer/def.txt) | 1 | The stemmer everyone uses, from its author, including his own warnings |
| [**Lucene analysis documentation**](https://lucene.apache.org/core/9_9_0/core/org/apache/lucene/analysis/package-summary.html) | 1 | What production engines actually enable by default |

---

## Two guesses

**A stopword list guesses that a term carries no information.**
**A stemmer guesses that two strings mean the same thing.**

Both guesses are made **before any evidence is available** — before you have seen the
corpus, before you know the query distribution, in a fixed list or a fixed set of rules
written by someone who had never seen your data. And both are *destructive*: once the term
is gone or merged, no later stage can recover it.

That combination — a guess, made early, that cannot be undone — is why they behave badly,
and it is a shape worth recognising because you will meet it again in week 4 with chunk
boundaries.

---

## What the stopword list is approximating

`the` appears 2,913 times in this corpus and in all ten documents. It is genuinely almost
useless for discriminating between documents. The list is not stupid.

But look at the actual numbers from today's lab:

| | tokens | vocabulary |
|---|---|---|
| all terms | 52,779 | 4,273 |
| stopwords removed | 38,027 | 4,229 |

**28% of the text, and 1% of the vocabulary.** Forty-four types carry a quarter of the
corpus.

That asymmetry is precisely what a *frequency-based weighting* handles, and it handles it
without a list, without a language assumption, and without deleting anything. Wednesday's
one logarithm gives `the` a weight of 0.047 and `429` a weight of 1.992 — and if `the`
turns out to matter for some query, it is still there, weighted low, rather than absent.

**The list is a binary approximation of a continuous quantity, decided in advance.** Put
that way it is obvious which one you want.

### And why removing them made things *worse*

recall@3 fell from 0.759 to 0.685.

The scorer counts distinct matching terms. Removing stopwords removes terms from *both*
sides, so queries and documents both get shorter, and the ranking is decided by fewer,
noisier signals. Nothing about the scoring function got better — it just got less to work
with.

The lesson is not "stopwords are bad". It is that **you cannot fix a scoring problem in the
tokeniser**, and the reason people try is that the tokeniser is where you can see the
problem.

---

## What the stemmer breaks

Run your stemmer over the corpus vocabulary and read the output. In this corpus:

- `status` → `statu` — not a plural, and now a term that appears nowhere in English
- `cookies` → `cooky`
- `caching` → `cach`, but `cache` → `cache`. **The two still do not match**, which is the
  case the stemmer existed for

The third is the important one. A suffix stripper conflates `caching` and `cached` while
leaving `cache` alone, so it half-solves the problem it was introduced for. A real stemmer
— Porter's, or a lemmatiser — handles this case better and makes the *same kind* of
mistake elsewhere: Porter famously conflates `universal`, `university` and `universe`.

Porter's own paper is careful about this in a way that its users generally are not. The
algorithm is a heuristic with known failure classes, presented as such.

On this corpus, stemming cost 0.037 ndcg@3 and broke two queries outright — `r08`, which
turns on the exact phrasing of a status-code rule, and `r10`, the unanswerable one, where
merging terms made a spurious match *look* better.

---

## When they are right

To be fair to both, because both are standard and both are sometimes correct:

- **Stopword removal helps when the index is the constraint.** Dropping 28% of postings was
  a serious saving in 1998. It is rarely the binding cost now
- **Stopword removal helps phrase-heavy systems** by shrinking positional data enormously
- **Stemming helps in morphologically rich languages**, where the ratio of surface forms to
  lemmas is far higher than in English. The English intuition that it is marginal does not
  transfer to Finnish or Turkish
- **Stemming helps short documents**, where a single missed match is the difference between
  a hit and nothing

What they share is that the benefit is about *cost or coverage*, not about relevance. Where
relevance is the goal and you can afford the index, weighting beats deleting.

---

## The general principle

> **Prefer changes that add information to changes that discard it, and prefer decisions
> made from the corpus to decisions made in advance.**

Today's three changes, scored against that principle:

| Change | Adds or discards | Decided | Helped |
|---|---|---|---|
| stopword removal | discards | in advance | no |
| stemming | discards | in advance | no, and broke two queries |
| keep identifiers | adds | in advance | **yes** |
| idf (Wednesday) | neither — weights | **from the corpus** | yes, a lot |

The principle predicts all four rows, and it will predict most of week 4 as well. Write it
down now, before Wednesday makes it look obvious in hindsight.

---

## Where this is now

Default analyzer configurations in modern engines are less aggressive than they were:
stopword removal is off by default in several, on the grounds that scoring handles it and
disk is cheap. Stemming is usually still available and usually still enabled, mostly by
inertia.

The larger change is that the whole question is now often bypassed rather than answered —
embeddings do not tokenise this way at all, which is week 5. It is worth noticing that
"bypassed" is not "solved": an embedding model has its own tokeniser, with its own
destructive choices, and you did not choose them and generally cannot see them.

---

> **Known** — idf weights terms by corpus frequency rather than by a fixed list
> (`bm25-foundations`) · Porter's stemmer is a heuristic with documented failure classes,
> stated by its author (`porter-stemmer`) · production analyzers vary in which filters they
> enable by default (`lucene-analysis`)
> **Inferred** — that "add rather than discard, and decide from the corpus rather than in
> advance" predicts which analyzer changes help. Ours, and this day is the evidence for it
> **Derived** — removing terms from both the query and the documents leaves the same
> scoring function with strictly less evidence, so it cannot improve discrimination except
> by removing noise
> **Unknown** — how much of the standard stemming-and-stopwords configuration in deployed
> systems has ever been measured on the corpus it runs against. Our guess is very little
