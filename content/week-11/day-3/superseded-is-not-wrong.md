# Superseded is not wrong

*Week 11 · Day 3 · about 20 minutes*

> By the end of this you can explain why the fix for `r05` breaks `r07`, and why no version
> of the fix avoids it.

---

## Sources

| Source | Tier | What it gives you |
|---|---|---|
| [**RFC 8259**](https://www.rfc-editor.org/rfc/rfc8259.html) | 1 | Obsoletes 7159, and changes the answer |
| [**RFC 8615**](https://www.rfc-editor.org/rfc/rfc8615.html) | 1 | Obsoletes 5785, and does **not** change the answer |

---

## Two supersessions, graded differently

The corpus has exactly two supersession edges and they were chosen to be different.

| edge | did the answer change | query | grade |
|---|---|---|---|
| 7159 → 8259 | **yes**, UTF-8 guidance reversed | `r05` | 7159 is not relevant |
| 5785 → 8615 | **no**, `/.well-known/` unchanged | `r07` | **both** are relevant |

Week 2 wrote the judgments that way on purpose, and this is the week it pays.

`r07` asks where well-known URIs live. RFC 8615 obsoletes RFC 5785 and the answer is the
same in both. So RFC 5785 is superseded, still correct, still relevant, and **still carries
an answer span**.

---

## What the fix does

Both strategies — the second hop and week 2's filter — take `answered` from 0.700 to 0.650,
and the lost query is `r07`.

A blanket *drop the superseded document* rule is right about `r05` and wrong about `r07`. It
has no way to be otherwise, because:

**the edge is syntactic and the distinction is semantic.**

`Obsoletes: 7159` and `Obsoletes: 5785` are the same kind of fact, parsed by the same
regular expression, stored in the same dictionary. Nothing in the header says whether the
obsoleting document changed any particular answer. That information exists only by reading
both documents and comparing them on the specific question being asked — which is a
question-dependent judgment, not a property of the pair.

Which means there is no rule over the metadata that gets both queries right. Not a better
hop, not a better filter, not a better graph. The field does not contain the distinction.

---

## So what do you ship

Three options, and the third is the honest one.

**Drop the superseded.** Right about `r05`, wrong about `r07`. Correct on the dangerous
case and lossy on the harmless one. Defensible if a wrong answer is much worse than a
missing one, which for a specification corpus it probably is.

**Demote rather than drop** — week 2's `demote_superseded`, which keeps the chunk and ranks
it below current ones. Keeps `r07`, and `r05` comes back the moment the budget is large
enough to reach the demoted chunk. It converts a correctness property into a budget
coincidence, which is the worst of the three.

**Annotate.** Keep the chunk, mark it, and make the mark visible to whatever consumes the
context — in the chunk text itself, not in a field the generator never sees. *"[Obsoleted by
RFC 8259]"*. This is the only option that preserves the information needed to get both
queries right, and it moves the decision to the generator, which is where the semantic
judgment has to happen.

And then measure it, because this course's position on moving a decision to a model is that
it is a hypothesis.

---

## The general shape

This is the third time the course has met this and it is worth naming.

- week 6 — a filter's recall cost is not a defect. `published_since(2015)` took recall from
  0.789 to 0.316 and was doing exactly what it was told
- week 10 — a cache's staleness check scored 0.833 and missed the only chunk that mattered
- week 11 — a supersession filter is correct for one edge and lossy for the other

Each time: **a rule over metadata enforces a syntactic property, and the thing you wanted
was semantic.** The rule is not broken. It is answering the question it was given, and the
question was a proxy for the one you had.

The response is never a cleverer rule. It is to decide which error you prefer, write the
decision down with the number attached, and make the loss visible rather than quiet. A
filtered system is measured against what the filter permits — week 6's sentence, and it is
still the right one.

---

> **Known** — RFC 8259 obsoletes RFC 7159 and changes its UTF-8 guidance (`rfc-8259`) · RFC
> 8615 obsoletes RFC 5785 while the `/.well-known/` mechanism itself is unchanged
> (`rfc-8615`)
> **Inferred** — that no rule over supersession metadata can distinguish an edge that
> changed an answer from one that did not, because the header records the relationship and
> not its consequences. Ours
> **Inferred** — that demotion converts a correctness property into a function of the
> context budget, making it the least defensible of the three options. Ours
> **Inferred** — that annotating the chunk text is the only option preserving the
> information needed for both queries, and that moving the judgment to a generator is a
> hypothesis requiring measurement rather than a solution. Ours
> **Derived** — both the hop and the filter take the answered rate from 0.700 to 0.650, and
> the single lost query is the one whose superseded document is still graded relevant
> **Unknown** — whether an annotation in the chunk text changes what a real generator cites.
> Measurable in an afternoon with an API key, and not measurable here
