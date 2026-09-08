# The baseline you must beat

*Week 1 · Day 4 · about 25 minutes*

> By the end of this you can say why a deliberately bad retriever is worth building, and
> name the four things wrong with it before you run it.

---

## Sources

| Source | Tier | What it gives you |
|---|---|---|
| [**Robertson & Zaragoza**](https://www.staff.city.ac.uk/~sbrp622/papers/foundations_bm25_review.pdf) §1–2 | 1 | Exactly which of today's defects the next fifty years of IR was spent fixing |
| [**Lin, *The neural hype and comparisons against weak baselines***](https://sigir.org/wp-content/uploads/2019/01/p040.pdf) | 1 | A field discovering that many published improvements were over baselines nobody had tuned |

---

## Why build something bad on purpose

Three reasons, and the third is the real one.

**1. A number you did not build is a number you will stop comparing to.** A baseline
imported from a library is a fact about the library. One you wrote in forty lines is
something you understand well enough to argue with.

**2. It sets the floor for "worth it".** Everything you add for the next eleven weeks costs
something — latency, money, a service to operate, a model that will be deprecated. The
question is never "does this help", it is "does this help *more than counting words*", and
you cannot ask that without the number.

**3. It is a well-tuned-baseline problem in miniature.** Lin's 2019 paper made an
uncomfortable observation about neural IR: a substantial number of published improvements
were measured against baselines the authors had not tuned, and vanished when someone tuned
them. The same thing is happening in RAG now, at greater volume and with less review. The
defence is to be the person who has the boring baseline, and it is a defence you can only
build once.

---

## The scorer, in one line

> Split on non-letters, lowercase, count how many distinct query terms the document
> contains, sort.

That is it. No weighting, no index, no notion that some words matter more.

---

## The four defects

You should be able to name these before running anything.

### 1. Every term is worth the same

`the` counts exactly as much as `4213`.

For the query **"what does ROCC stand for"**, four words carry no information and one
carries all of it. Documents containing `what`, `does` and `for` score 3. The glossary,
which answers the question completely, contains `rocc` and nothing else, and scores 1.

It ranks **last**. Position 22 of 22.

This is the defect the next fifty years of information retrieval was mostly about, and the
fix — weight a term by how rare it is — is one line of arithmetic in week 3. Knowing it is
one line, before you learn it, is worth more than learning it.

### 2. Longer documents win, if you count repeats

Counting occurrences instead of distinct terms seems obviously better and is worse: an
eleven-page governance document says `fare` more often than a five-page enforcement policy,
and takes the top slot for "what is the penalty for fare evasion" without answering it.

Two more things BM25 is for, both visible here: **length normalisation** (divide by how
long the document is) and **saturation** (the tenth occurrence of a word is not worth ten
times the first).

### 3. A word the document is about but does not contain is invisible

The corpus says `31-day pass`. The user says `monthly pass`. Overlap on the word that
matters: zero.

This one is **not fixable by arithmetic**. No amount of weighting makes `monthly` match
`31-day`, because they share no characters. Stemming does not help. This is the vocabulary
gap, it is the entire reason dense retrieval exists, and it is why week 5 arrives when it
does — after you have spent four weeks unable to fix it.

Write that down now, and check in week 5 whether embeddings actually fixed it on your
corpus. Sometimes they do not, and that is a more interesting result.

### 4. The tokeniser destroys structure

`$3.00` becomes `3` and `00`. `31-day` becomes `31` and `day`. `ROCC` and `rocc` become the
same string — which helps here, and will hurt the moment the corpus contains both an
acronym and a common word spelled the same way.

Every tokeniser makes these choices. Most people never look at what theirs does, and then
wonder why price queries do not work.

---

## The number, and why it flatters you

On the sample corpus this retriever gets recall@10 of 0.875 on `dev`, which sounds
respectable and is an artefact.

**Thirty documents.** Asking for the top ten asks for a third of the corpus. A retriever
that ranked randomly would score around 0.33 on this task. The gap between "counting words"
and "random" is real but it is much smaller than 0.875 suggests, and on a corpus of a
million the same retriever would be somewhere near useless.

Two habits from this, and they are the point of the day:

- **Always state the corpus size next to a recall figure.** Yours and everyone else's
- **Always compute what random would score.** It is one line and it is the only way to know
  whether a number is an achievement or a property of the setup

---

## What this baseline is genuinely good at

Not nothing, and it matters for week 6.

Exact identifiers. `stop 4213` returns the right document first, because `4213` appears in
two documents in the whole corpus and nothing dilutes it. `route 42 detour` is correct on
the first result.

Keep that. In week 5 you will build dense retrieval and discover it is *worse* at exactly
these queries, and the correct response is not disappointment — it is week 6, where you
stop choosing and combine them.

---

> **Known** — published neural IR improvements have repeatedly been measured against
> untuned baselines (`lin-neural-hype`) · term weighting by rarity, length normalisation and
> saturation are the components of the classical model (`bm25-foundations`)
> **Inferred** — that building your own baseline makes you more likely to keep comparing to
> it. Teaching experience, not a measured claim
> **Derived** — with 30 documents, top-10 is a third of the corpus, so a random ranker
> scores about 0.33 recall@10 and the reported 0.875 must be read against that
> **Unknown** — how much of the RAG literature would survive comparison against a tuned
> lexical baseline. Nobody has done the Lin study for RAG, and somebody should
