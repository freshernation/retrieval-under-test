# What a RAG answer actually is

*Week 1 · Day 1 · about 20 minutes*

> By the end of this you can say what part of a RAG answer is retrieval and what part is
> generation, and why almost every published "improvement" fails to distinguish them.

---

## Read the primary sources first

| Source | Tier | What it gives you |
|---|---|---|
| [**Lewis et al., *Retrieval-Augmented Generation***](https://arxiv.org/abs/2005.11401) | 1 | The paper the acronym comes from, 2020. Worth reading for how narrow the original claim was |
| [**Robertson & Zaragoza, *The Probabilistic Relevance Framework***](https://www.staff.city.ac.uk/~sbrp622/papers/foundations_bm25_review.pdf) §1 | 1 | What "relevance" meant for thirty years before anyone bolted a language model to it |
| [**TREC overview papers**](https://trec.nist.gov/pubs.html) | 2 | How a field measures retrieval when it is being serious about it |

> **This article's own framing is ours**, and is marked as such at the bottom. The stations
> are a teaching device, not a citation.

---

## The two-sentence version

A RAG answer is **a search result that has been rewritten into prose**.

That is the whole thing. Everything else is detail. And the sentence is worth reading
twice, because it contains the field's central and most expensive misunderstanding: people
believe they are building an answering system with a search component, when they are
building a search system with an answering component.

The difference decides where you spend your time. If the answer is a rewritten search
result, then the ceiling on answer quality is set by the search, and no amount of work on
the rewriting moves the ceiling. You can spend a month on the prompt. The document either
came back or it did not.

---

## What the model can and cannot repair

Given retrieved text, a competent model can:

- summarise it
- select the relevant part of it
- refuse when the text does not support an answer, *if asked to and sometimes even then*
- express uncertainty about it

It cannot:

- retrieve a document that was not retrieved
- recover information the extractor destroyed
- know that the passage it was given is the superseded 2023 version
- know what the corpus does not contain

Every item in the second list is a failure that will present itself to you as a
*generation* problem, because generation is the part you can see. This is the single most
reliable way to waste a quarter.

---

## The confident wrong answer

Ask a RAG system a question its corpus cannot answer, and the default behaviour of every
such system ever built is to answer anyway. This is not a defect in a particular model. It
is what the last stage is for: the last stage takes text and produces fluent prose about
it, and if the text is only vaguely related then the prose is fluent and vaguely wrong.

Worse, the answer looks *exactly* like a right one. There is no tell. There is no
hesitation in the prose, no hedge, no degradation in the writing quality — a wrong RAG
answer and a right one are the same object with different contents.

Two consequences the whole course rests on:

1. **You cannot evaluate a RAG system by reading its answers.** They all read well. You
   will conclude the system is good. Everyone does, including the people who built the
   systems in the write-ups you have read.
2. **Refusal must be designed, measured, and defended**, because it will not happen on its
   own. Week 8's hardest section is about this, and it is why half of `ai/adversary.md`'s
   query families are questions the corpus cannot answer.

---

## Where the answer actually comes from

Consider a question with a true answer of "$3.00", and follow it backwards.

The model said $3.00 because the passage said $3.00. The passage said $3.00 because it was
the 2024 policy rather than the 2023 one. It was the 2024 policy because it ranked above
the 2023 one, which happened for reasons nobody chose — the two documents differ in about
nine characters, and whichever scoring function you are using broke the tie somehow.

**A coin flip decided your answer.** It came up right this time. Nothing in the system
knows there was a coin.

This is the shape of most RAG behaviour: outcomes that look designed and were not. The
work of this course is turning that coin into a decision — and the only way to find the
coins is to measure enough queries that the flips average out and show you a rate rather
than an anecdote.

---

## What "grounded" means, and what it does not

A grounded answer is one supported by the retrieved text. Three things that sounds like
and is not:

- **Not "true".** An answer perfectly grounded in the 2023 fare policy is wrong. Grounding
  is a relation between the answer and the passage, and it says nothing about the world
- **Not "cited".** A citation is a claim about grounding. Systems produce citations that
  do not support the sentence they are attached to, routinely, and nobody checks
- **Not "the model did not make anything up".** The model can be perfectly faithful to a
  passage that was retrieved for the wrong query

Faithfulness is measurable (week 8). Correctness usually is not, without people. Say which
one you mean, every time, and notice how often published work does not.

---

## Where this is now

RAG as a term has drifted since 2020 to mean roughly "any system that puts retrieved text
in a prompt", which is much broader than the paper. The 2020 architecture — retrieval
trained jointly with generation — is not what almost anyone means by RAG in 2026, and
citing Lewis et al. as the source of what you built is usually wrong. Cite it for the idea;
do not claim it as the design.

---

> **Known** — the 2020 paper describes joint training of retriever and generator
> (`rag-2020`) · relevance judgment and pooled evaluation predate RAG by decades
> (`trec-overview`)
> **Inferred** — that the ceiling on answer quality is set by retrieval follows from the
> model's inability to retrieve, but we know of no controlled study isolating it
> **Derived** — a wrong answer and a right one are indistinguishable by fluency, because
> fluency is a property of the generator and not of the passage
> **Unknown** — what fraction of production RAG failures originate before generation. We
> have not found a published measurement. If you find one, tell your instructor
