# Relevance is a judgment, not a property

*Week 1 · Day 2 · about 25 minutes*

> By the end of this you can defend the line between a 1 and a 2, and you will have stopped
> expecting relevance to be a fact about a document.

---

## Read the primary sources first

| Source | Tier | What it gives you |
|---|---|---|
| [**TREC overview papers**](https://trec.nist.gov/pubs.html) | 1 | Thirty years of a field building judgment sets on purpose, and documenting what went wrong |
| [**Voorhees, *Variations in relevance judgments***](https://trec.nist.gov/pubs/trec8/papers/overview_8.pdf) | 1 | The result that assessors disagree substantially, and that system *rankings* survive it anyway |
| [**Robertson & Zaragoza**](https://www.staff.city.ac.uk/~sbrp622/papers/foundations_bm25_review.pdf) §1 | 1 | What "relevance" is being modelled as, formally, and by whom |

---

## The thing that takes a day to accept

**A document is not relevant. A document is relevant *to a person asking a question for a
reason*.**

This sounds like philosophy and it is arithmetic. Take "how much is a single adult fare"
against the MRTA corpus. The 2023 fare policy states an adult single fare, clearly, in
section 2. Is it relevant?

- To a person planning a journey tomorrow: **no**. It is wrong, and it is wrong in the
  worst way, which is confidently and in the right format
- To an auditor reconstructing a 2023 refund: **completely**. It is the only document that
  answers them
- To someone asking what fares used to be: **completely**
- To a retrieval system that does not know which of these people is asking: **unanswerable
  as posed**

Every one of those is a defensible grade for the same document and the same query string.
Which means the grade is not in the document. It is in your model of the user, and you are
writing that model down when you judge.

This is why the report template asks what a complete answer would contain *before* you look
at documents. Write the model down, then apply it, or you will construct the model from
whatever you happen to find and it will be a model of your corpus rather than of a person.

---

## The four grades, and where the argument is

```
0  irrelevant
1  related, but does not answer it
2  answers it
3  answers it completely, on its own
```

Nobody argues about 0 and 3. The entire annotation literature, and every hour you will
spend on this, lives on **the line between 1 and 2**, because that line is where a
document stops being background and becomes an answer.

Useful tests, in rough order of how often they settle it:

- **Could a person act on this document alone?** If they would still have to find something
  else, it is a 1
- **Is it about the question, or does it contain the answer?** A document about MRTA
  refunds that never states the refund window is a 1
- **Would you be annoyed to be shown this as the top result?** Annoyed is 1. Satisfied but
  wanting more is 2

Then write your own test down in one sentence and use the same one for all twelve queries.
The consistency matters more than which test you chose. A set graded by three different
rules is a set with three different meanings of recall in it, and no metric will tell you.

---

## You will disagree with yourself

The number to have in your head: assessors disagree with each other substantially, and
with themselves across time, and this has been true in every study since the 1960s. Raw
agreement in the 70-80% range is normal for careful people. Yours will not be 95%, however
much you would like it to be, and Tuesday's sealed prediction exists so you cannot rewrite
that memory on Friday.

Then the part that saves the field, from Voorhees: **system rankings are largely stable
under judgment variation.** Swap the assessor and the absolute numbers move; which system
is better usually does not. That is the empirical result that makes evaluation possible at
all, and it is why we measure differences between systems rather than quoting absolute
scores as facts.

The practical consequence, and it is the whole reason today exists:

> **Your self-agreement is the floor on every improvement you can claim.** If you disagree
> with yourself 22% of the time, a 3-point gain in week 6 is inside your own noise, and a
> confidence interval computed against those judgments is measuring something narrower than
> you think.

---

## Why kappa and not agreement

If 90% of everything you judge is a 0 — which it will be, because most documents are
irrelevant to most queries — then two judges who label nearly everything 0 agree nearly
always, by construction.

Cohen's kappa asks how much you agree *beyond* what that arithmetic gives you for free:

    kappa = (observed - chance) / (1 - chance)

with `chance` computed from each judge's own grade distribution. Two lazy judges score near
0. Two judges who agree on the hard cases score high. Report kappa alongside raw agreement,
always, and report the overlap size next to both — perfect agreement on three documents is
not a finding.

Kappa has its own well-known pathologies with skewed distributions, and there is a whole
literature of people arguing about it. Use it anyway, as a floor rather than a
certification, and be suspicious of your own number when it is high.

---

## Judge the document, not the system

The single most expensive mistake available to you this week:

> Running the retriever, looking at what came back, and judging that.

It produces an eval set that is a *description of your retriever*. Every subsequent
measurement is then partly a measurement of the thing being measured, the correlation is
invisible, the numbers look completely normal, and there is no later point at which anyone
finds out.

The defence is order. Judgments Tuesday, retriever Thursday. That is the only reason this
week runs in the sequence it does.

Pooling — judging the union of several systems' top results — is the standard compromise
when a corpus is too large to judge, and it is what TREC has done since 1992. It is also
biased in a specific, permanent way: **a document no system in the pool ever ranked highly
is graded 0 for ever**, including for a better future system that finds it. Every retrieval
benchmark you will ever read carries this bias. Most do not mention it.

---

## Where this is now

Judging with a language model is now common, and the debate about it is live rather than
settled. The case for is cost; the case against is that model judgments correlate with
model *preferences*, which makes a model-judged eval set systematically friendly to
systems built from the same models.

Week 9 covers it properly, with the evidence pointing both ways. In week 1 it is banned
outright, for a reason that is not really about accuracy: **you cannot calibrate a judge
you have never been.** Judge four hundred documents by hand once in your life and you will
have opinions about automated judging worth listening to.

---

> **Known** — assessors disagree substantially, and system rankings are largely stable
> under that variation (`voorhees-trec8`) · pooling has been TREC's method since 1992
> (`trec-overview`)
> **Inferred** — that your own self-agreement bounds the smallest improvement you can
> honestly claim. This follows from the noise argument and we know of no study measuring it
> directly for single-annotator eval sets
> **Derived** — with a heavily skewed grade distribution, raw agreement is high by
> construction and kappa corrects for exactly that
> **Unknown** — how much annotation training changes single-annotator self-agreement. The
> TREC literature studies inter-assessor agreement far more than intra-assessor
