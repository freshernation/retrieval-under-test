# Similar is not the same question

*Week 14 · Day 2 · about 20 minutes*

> By the end of this you can explain why a cache keyed on embedding similarity will
> answer the wrong question, and what one check an embedding cannot make fixes it.

---

## Sources

| Source | Tier | What it gives you |
|---|---|---|
| [**Regmi & Pun**, GPT Semantic Cache](https://arxiv.org/abs/2411.05276) | 3 | A semantic cache for model queries, and the hit rates it reports |
| [Week 5, day 3](../../week-05/day-3/) | — | Dense retrieval loses on identifiers |
| [Week 12, day 3](../../week-12/day-3/) | — | A cache keyed on the question leaks across readers |

---

## The cache that could not be measured

Week 10's cache answered only questions it had seen word for word. The eval set, built to
have no duplicates, could not even measure it: twenty-six distinct questions, a hit rate of
zero.

A semantic cache answers questions that are **close enough**. Embed the question, compare
it with every cached question, and if the best one is above a threshold, serve its answer.
"Which status code tells a client it sent too many requests" is served the answer to "what
status code should I return when a client sends too many requests". That is the whole
appeal, and it works.

---

## The same blind spot, inherited

Week 5's finding was that dense retrieval loses to BM25 on identifiers: a smoothed
representation keeps the topic and drops the exact token. A semantic cache is a dense
retriever over its own past questions, and it inherits that finding exactly.

"What does section 3.2 of RFC 3986 define" and "what does section 3.4 of RFC 3986 define"
score **0.981**. Nine of the ten real paraphrases score lower. So does every pair of
questions about two different status codes — "418" and "451" are both, to the embedding,
"a status code".

Sweep the threshold and there is no safe setting. At 0.8 the cache answers five of ten
paraphrases and two near misses with the wrong answer. At 0.95 it answers one paraphrase
and still one near miss. At 0.98 it answers no paraphrases at all — and still answers 3.4
with 3.2.

---

## One check the embedding cannot make

The fix is not a better threshold. It is a second test the embedding is structurally unable
to make: **the identifiers in the two questions must be identical** — every token with a
digit in it, from status codes to section numbers to RFC numbers.

With that check, at 0.8: the same five paraphrases hit, and **none** of the near misses do.
Nothing about the embedding changed. The cache simply stopped asking it a question it
cannot answer.

---

## And the reader

Week 12 found its leak in front of the filter: a cache keyed on the question, filled by
staff, served to the public. The semantic cache keeps an entry per set of reader groups, so
a public reader is never compared against anything staff stored. The cost is the same as
week 12's: fewer hits. It is not optional.
