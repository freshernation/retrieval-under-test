# Two ways a citation fails

*Week 8 · Day 2 · about 25 minutes*

> By the end of this you can check that a citation points at something real, and you will
> know why that check is the easy half.

---

## Sources

| Source | Tier | What it gives you |
|---|---|---|
| [**Rashkin et al., *Attributable to Identified Sources***](https://arxiv.org/abs/2112.12870) | 1 | A formal definition of attribution, and how much work it is to evaluate |
| [**Liu, Zhang & Liang, *Evaluating Verifiability in Generative Search Engines***](https://arxiv.org/abs/2304.09848) | 1 | Human evaluation of deployed systems' citations. The numbers are worse than you expect |
| [**Ji et al.**](https://arxiv.org/abs/2202.03629) | 1 | Hallucination taxonomy, including fabricated references |

---

## The two failures are independent

An answer with a citation reads as verifiable. Whether it *is* has two parts, and they fail
separately:

**The citation points at nothing.** The id is not a chunk, or is a chunk that was not in this
context. Cheap to detect: resolve the id, check membership. No model, no judgment.

**The citation points at the wrong thing.** The id resolves, the chunk was in the context, and
the text it names does not support the claim attached to it. That needs a *support* check,
which is Wednesday, and it is much harder.

Today is the first. It is worth doing first because it is free, and because a system failing
it is broken in a way no prompt work fixes.

---

## Present-in-context is the one people skip

Resolving the id is obvious. Checking it was in *this* context is not, and it is the one that
matters.

A generator that cites a real chunk it was never shown has not made a small error. It has
produced text whose provenance is fictional: a reader follows the link, sees plausible
material, and concludes the claim is sourced. It is not — the wording came from somewhere
else, or from nowhere.

`not_in_context` is three lines and it is the difference between "this system cites" and
"this system's citations mean something".

---

## The unit is the sentence

An answer-level citation list tells you the answer drew on four chunks. It does not tell you
**which chunk supports which claim**, and that is the only question worth asking.

So `cited_sentences` pairs each sentence with the citations attached to it — and there is a
trap in doing that which is worth getting right rather than around.

A citation follows the sentence it supports, so it appears **after the full stop**:

```
The 429 status code indicates rate limiting. [rfc-6585#4] Retry-After may be included. [rfc-6585#5]
```

A sentence splitter puts `[rfc-6585#4]` at the *start of the next sentence*. Split naively and
every citation is attached to the following claim — off by one for the entire answer,
producing a support check that is wrong everywhere while looking fine.

Pull leading markers back onto the sentence before them.

---

## Uncited sentences

Not automatically wrong. A summarising or transitional sentence may legitimately cite
nothing.

They are, however, exactly where an unsupported claim hides — there is no citation to check
it against, so any support check must either skip it or check it against the whole context,
which is the lenient choice. Count them and report the count.

---

## Where the real numbers are

Human evaluation of deployed generative search engines has found that a substantial fraction
of generated sentences are **not fully supported by their citations**, and that a substantial
fraction of citations do not support the sentence they are attached to. This is in shipped,
widely used systems, evaluated by people.

Two things follow. Citation checking is not a hypothetical concern. And the checks in this
lab — mechanical, cheap, no model — catch only the crudest version of it; the version those
studies measured needed humans.

---

> **Known** — attribution has a formal definition and evaluating it is substantial work
> (`rashkin-2021`) · human evaluation of deployed generative search engines finds a
> substantial fraction of sentences not fully supported by their citations
> (`liu-verifiability-2023`) · fabricated references are a documented failure mode
> (`ji-2022`)
> **Inferred** — that present-in-context is the check people skip and the one that matters.
> Ours, from the failure it permits
> **Derived** — a citation marker following a full stop is assigned to the following sentence
> by any splitter that breaks on sentence-final punctuation, so naive splitting misattributes
> every citation in an answer
> **Unknown** — the rate of not-in-context citation in production RAG systems specifically, as
> opposed to generative search. We have not found it measured
