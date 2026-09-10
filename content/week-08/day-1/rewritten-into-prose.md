# A search result rewritten into prose

*Week 8 · Day 1 · about 25 minutes*

> By the end of this you can measure the only property of a generated answer that needs no
> judgment, and you will have seen why every other property needs one.

---

## Read the primary sources first

| Source | Tier | What it gives you |
|---|---|---|
| [**Lewis et al., *Retrieval-Augmented Generation***](https://arxiv.org/abs/2005.11401) | 1 | The architecture, and how narrow the original claim was |
| [**Rajpurkar et al., *SQuAD***](https://arxiv.org/abs/1606.05250) | 1 | Answer spans — the ground truth that makes today measurable |
| [**Ji et al., *Survey of Hallucination in NLG***](https://arxiv.org/abs/2202.03629) | 1 | The taxonomy: intrinsic versus extrinsic, and why the distinction matters here |

---

## Week 1's claim, now demonstrable

> A RAG answer is a search result that has been rewritten into prose.

Seven weeks ago that was an assertion. Today it is a measurement.

The system answers twenty queries. Fourteen of them had the answer somewhere in the context.
All twenty received fluent, cited prose.

So **six answers — thirty percent — are confident text about questions the system could not
answer.** And the reason this matters more than the number: *nothing in the answers
distinguishes them.* Same length, same register, same citation density, same authoritative
tone. Put a right one and a wrong one side by side and sort them blind — you cannot.

That is the whole argument for machinery, and it is why the fence forbids grading an answer
by reading it.

---

## Groundedness is measurable and correctness is not

Three different questions, routinely conflated:

| question | relates | measurable here |
|---|---|---|
| **grounded** — was the answer in the context | context ↔ world | **yes**, with answer spans |
| **faithful** — does the answer follow from the context | answer ↔ context | Wednesday, by proxy |
| **correct** — is the answer true | answer ↔ world | **no** |

Today is the first. It is the only one available without either a human or a model, and it
is available because of a decision made in week 4: **answer spans**, verbatim and minimal,
written once and reused ever since.

Note what it does *not* tell you. Groundedness says the generator **had** what it needed. A
system can be grounded and still produce a wrong answer — by picking the wrong sentence, by
misreading, or, as Wednesday shows, by picking a sentence from a document withdrawn in 2017.

---

## Divide by every query

`grounded_rate` divides by the whole query set, not by the answered ones.

That sounds pedantic and it is the difference between a metric and a lever. Divide by the
answered ones, and a system that declines every hard question reports a *higher* score for
answering fewer of them. It will happen by accident the first time somebody tunes a refusal
threshold, and the dashboard will go up.

The general rule, and it applies to every rate in this course: **the denominator is the
population you care about, not the population your system chose to act on.**

---

## The two kinds of made-up answer

The hallucination literature distinguishes them, and the distinction decides where you look:

**Intrinsic** — the answer contradicts the context it was given. Detectable by comparing the
answer to the context, which is Wednesday.

**Extrinsic** — the answer adds something the context does not contain. Detectable only
against the world, which you do not have.

Today's six are neither, exactly, and that is what makes them interesting. The answers are
*faithful to a context that does not contain the answer*. The generator did nothing wrong at
station 6; retrieval failed at station 4, and the generator's job description does not
include noticing.

Which is why the six are a **retrieval** finding surfaced by generation. Four of them were
retrieval failures nobody had looked at, because no metric had ever put prose in front of
you.

---

## Read the six

The exercise today is not the numbers. It is reading all six answers in `confidently_wrong`,
in full.

Fifteen minutes, and it changes what the rest of the week feels like. A 30% confidently-wrong
rate is a statistic; *"how do I stop search engines indexing my site"* answered with a
paragraph about URI normalisation, cited, confident, and completely useless, is a thing you
remember when somebody proposes shipping.

---

> **Known** — the RAG architecture retrieves passages and conditions generation on them
> (`rag-2020`) · answer spans as verbatim substrings are a standard ground truth
> (`squad-2016`) · hallucination is standardly split into intrinsic and extrinsic
> (`ji-2022`)
> **Inferred** — that a wrong RAG answer is not distinguishable from a right one by reading.
> Demonstrated on this corpus and this generator; the generalisation is ours and is week 1's
> original claim
> **Derived** — a rate whose denominator is the answered queries rises when a system refuses
> more, independently of any change in answer quality
> **Unknown** — what fraction of production RAG answers are confident responses to
> unretrieved questions. It is measurable with answer spans and we have not seen it published
