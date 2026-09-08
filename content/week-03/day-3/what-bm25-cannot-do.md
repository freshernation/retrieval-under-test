# What BM25 still cannot do

*Week 3 · Day 3 · about 20 minutes*

> By the end of this you can name the week-1 defect that survives, and predict which of
> your queries will still be broken in week 4.

---

## Sources

| Source | Tier | What it gives you |
|---|---|---|
| [**Robertson & Zaragoza**](https://www.staff.city.ac.uk/~sbrp622/papers/foundations_bm25_review.pdf) §1 | 1 | What the model assumes, stated by its authors |
| [**Furnas et al., *The vocabulary problem in human-system communication***](https://dl.acm.org/doi/10.1145/32206.32212) | 1 | The measurement: two people choose the same word for the same thing about 10–20% of the time |
| [**BEIR**](https://arxiv.org/abs/2104.08663) | 1 | Where lexical retrieval wins and loses against dense methods, across eighteen datasets |

---

## Four defects, three fixed

In week 1 you named four things wrong with the baseline and ranked them by expected cost.
Score the ranking now:

| Defect | Fixed by | This week? |
|---|---|---|
| Every term is worth the same | idf | **yes** |
| Longer documents win | length normalisation | **yes** |
| The tokeniser destroys structure | keeping identifiers | **partly** |
| A word the document is *about* but does not contain is invisible | nothing | **no** |

The fourth is untouched, and nothing in the lexical toolbox touches it. Not a better
tokeniser, not a stemmer, not a bigger k1. **`monthly` and `31-day` share no characters**,
so no function of character sequences can relate them.

---

## The number behind it

Furnas and colleagues measured this in 1987 and the result is worth carrying around:

> Two people spontaneously choosing a word for the same thing agree roughly **10–20%** of
> the time.

Not for obscure concepts. For ordinary objects and everyday commands. The single most
common word for a thing is typically chosen by fewer than a third of people.

Which reframes the whole of lexical retrieval. It is not that vocabulary mismatch is an
edge case handled by a synonym list; it is that **agreement on wording is the exception**,
and a retriever matching character sequences is relying on a coincidence that happens
sometimes.

That the coincidence happens often enough for BM25 to work as well as it does is the
genuinely surprising fact — and the explanation is that a query has several words, and a
document has thousands, so *some* of them collide even when the important one does not.

---

## Where you can see it

`r02` — *how do I tell a client to slow down*.

The answer is RFC 6585 §4: status 429, plus `Retry-After`. The document contains the phrase
`rate limiting`, once, in parentheses. It contains neither `slow` nor `down`.

BM25 ranks RFC 3986 and RFC 6265 above it. Every term in the query is common, none is
discriminating, and the term that would have decided it — `429` — is one the user could not
have typed, because knowing it is the answer to their question.

**No parameter value fixes this.** Sweep k1 and b across the whole grid tomorrow and watch
`r02` not move.

`r06` — *what does ABNF stand for* — is a milder version. The expansion exists in three
documents, once each, in a reference line. BM25 gets one of them into the top three, which
is better than week 1's dead last, and it is luck rather than understanding.

---

## The three ways out, and when each arrives

**Expand the query.** Add `429`, `rate limit`, `throttle` to `slow down`. Needs a source of
related terms: a thesaurus, co-occurrence statistics, or a model. Week 6.

**Represent meaning instead of characters.** Map text to vectors where `slow down` and
`rate limiting` land near each other. This is what embeddings are for and it is week 5.

**Change the unit.** A whole document dilutes a rule stated in one paragraph. Retrieve
paragraphs and the rule's own terms stop competing with 19,000 others. Week 4, and it is
next.

The order is deliberate: the cheapest and least fashionable first.

---

## And what BM25 does that the alternatives do not

Before week 5 makes embeddings sound like the answer, note what you would be giving up.

`r03` is the query `451`. BM25 returns exactly one document, correctly, instantly, and
would still do so if the corpus had ten million documents.

That is not "good enough". It is **right**, and it is right for a reason you can state:
`451` occurs in one document, its idf is high, and the score reflects a fact about the
corpus rather than a similarity judgment. An embedding of the string `451` is a point in
space near other numbers, and week 5 shows what that does.

Exact identifiers — part numbers, error codes, section references, names, dates — are a
large share of real queries and the case where lexical retrieval is not merely competitive
but correct.

**Week 6 exists because you want both**, and you will only believe that after week 5 loses
a query you know BM25 got right.

---

> **Known** — spontaneous vocabulary agreement between two people is roughly 10–20%
> (`furnas-1987`) · lexical and dense retrieval have complementary strengths across
> datasets, with lexical stronger on exact-match and entity-heavy queries (`beir-2021`) ·
> BM25 scores terms independently (`bm25-foundations`)
> **Inferred** — that no lexical technique can bridge a vocabulary gap between strings
> sharing no characters. Follows from the model operating on character sequences
> **Derived** — a query term the user does not know cannot appear in their query, so a
> retriever matching only query terms cannot use it
> **Unknown** — what fraction of real queries in a given system are exact-identifier
> queries. It varies enormously by domain and almost nobody measures it, which is why the
> lexical-versus-dense argument is usually conducted without evidence
