# Ranked, not sorted

*Week 12 · Day 1 · about 25 minutes*

> By the end of this you can order a report by what the reader must do, and you will know
> why the limitations go before the numbers.

---

## Sources

| Source | Tier | What it gives you |
|---|---|---|
| [**Google SRE Book**, ch. 15](https://sre.google/sre-book/postmortem-culture/) | 1 | Postmortems written to be acted on, blameless and specific |
| [**Mitchell et al.**, *Model Cards*](https://doi.org/10.1145/3287560.3287596) | 1 | Intended use and limitations as required sections, not appendices |
| [**Gebru et al.**, *Datasheets for Datasets*](https://arxiv.org/abs/1803.09010) | 1 | Documenting what a dataset was built for and what it is not for |

---

## The default order, and why it is wrong

Left alone, a report comes out in the order the work happened. Week 1 first, week 11 last,
conclusions at the end. Or it comes out in order of effort — the hardest thing most
prominent — which is the same mistake with a motive.

Both are **sorted**. What a report needs is to be **ranked**: ordered by what the reader has
to do something about.

The test is mechanical. Read your first line and ask *what would somebody do about this?*
If the answer is "nothing, it is context", it is not a first line.

```
"We evaluated four chunking strategies across 20 queries."           sorted
"Six of twenty answers are confident and wrong, and nothing in the
 pipeline distinguishes them from the fourteen that are right."      ranked
```

Both are true about the same work. Only one gets read past the first paragraph, and only
one causes anything to happen.

---

## Why section 2 comes before section 3

The order this course asks for:

```
1  what you must act on
2  what this evaluation cannot see
3  the numbers
4  what expires
```

Section 2 before section 3 is the part people argue with, so here is the argument.

A reader who meets your numbers first has already formed a view by the time they reach your
caveats, and the caveats then read as hedging — as throat-clearing a confident person would
have left out. Put them first and they are **scope**: this is what the instrument measures,
here is what it is blind to, now here is what it said.

The same information, in two orders, produces two different beliefs in the reader. That is
not a presentational preference; it is what ordering does.

Model cards made this a convention and the convention is the useful part: intended use and
limitations are **sections**, in a fixed place, at the front. Not an appendix, not a
footnote, not a sentence in the discussion. A limitation that is structurally required
cannot be quietly dropped under deadline, and that is the whole mechanism.

---

## What a blocker looks like

Four fields, and all four:

> **what is wrong** · **the station** · **the evidence, with a run id** · **the cost of doing
> nothing**

The fourth is the one that gets left out, and without it a blocker is an observation. *"Six
answers are confidently wrong"* is an observation. *"Six of twenty answers are confidently
wrong; at our volume that is roughly four hundred wrong answers a week, each of which looks
exactly like a right one"* is a blocker.

You do not need to be right about the volume. You need to have put a magnitude on it, so
somebody can argue with the magnitude instead of ignoring the finding.

---

## The paragraph you have to delete

There is one in every report, and it is usually the best-written paragraph in the document.

It describes work that was hard, interesting, and well executed, and that nobody needs to
act on. A sweep that found nothing. An implementation detail you are proud of. A negative
result you already reported in section 1 and want to explain again.

Delete it. If it is genuinely a finding, it is a row in section 3 with its n attached. If it
is a story about the work, it goes in the handover note or nowhere.

The instinct to keep it is the instinct that produces reports nobody reads, and this course
has eleven weeks of evidence that the valuable things are short.

---

## And the course's own first line

If this course wrote a report about itself, section 1 would open with:

> **Correctness is unmeasurable with the instruments built here, and it has been since week
> 1.** Faithfulness is 1.00 while 30% of answers are confidently wrong, and no metric in the
> repository distinguishes them.

Not *"we built an eval harness, a lexical retriever, a chunker, a dense index, a hybrid
fusion, a reranker, a generator and an agent."* All of that is true, took eleven weeks, and
is section 3.

---

> **Known** — postmortems are written to be acted on, with specific remediation rather than
> narrative (`sre-book-postmortem`) · model cards place intended use and limitations as
> required front-matter sections (`mitchell-2019`) · dataset documentation records what a
> dataset was built for and what it should not be used for (`gebru-2021`)
> **Inferred** — that a report must be ranked by required action rather than sorted by
> chronology or effort, and that the test is *what would somebody do about this*. Ours
> **Inferred** — that limitations placed before results read as scope and placed after read
> as hedging, so the same information in two orders produces two different beliefs. Ours
> **Inferred** — that a structurally required limitations section survives deadline pressure
> in a way an appendix does not, which is the mechanism behind the model-card convention.
> Ours
> **Derived** — a blocker lacking a magnitude for the cost of inaction cannot be argued with
> and is therefore ignorable, so the magnitude is load-bearing even when it is approximate
> **Unknown** — whether reports written in this order are acted on more often. We believe it
> and have measured nothing, which is exactly the kind of claim this course asks you to mark
