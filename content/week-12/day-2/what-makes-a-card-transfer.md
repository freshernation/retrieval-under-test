# What makes a card transfer

*Week 12 · Day 2 · about 25 minutes*

> By the end of this you can tell a failure mode from a bug, and you will know which field
> of the card does the work.

---

## Sources

| Source | Tier | What it gives you |
|---|---|---|
| [**Google SRE Book**, ch. 15](https://sre.google/sre-book/postmortem-culture/) | 1 | Postmortems as a durable, searchable corpus rather than per-incident paperwork |
| [**Gebru et al.**, *Datasheets for Datasets*](https://arxiv.org/abs/1803.09010) | 1 | Fixed fields, including the uses a thing is *not* for |
| [**Sculley et al.**, *Hidden Technical Debt in ML Systems*](https://papers.nips.cc/paper_files/paper/2015/hash/86df7dcfd896fcaf2674f757a2463eba-Abstract.html) | 1 | Failure modes that are properties of the system's shape rather than of its code |

---

## The six fields

> the failure · the station it belongs to · the diagnostic that finds it · the fix ·
> the measured delta · **the conditions under which the fix stops working**

Five of those get filled in. The sixth is left blank, and the sixth is the one that makes
the card worth keeping.

A card with five fields says *"this worked for me"*. A card with six says *"this works when,
and here is how you check"* — and the difference is the difference between a note and a
method. It is also the only field that can be wrong in a way somebody else can detect,
which is what makes the card falsifiable.

Example, from week 3:

| field | |
|---|---|
| failure | tuned BM25 beats the default by a large margin on one query family and loses on another |
| station | 3 index |
| diagnostic | per-family breakdown of the sweep, not the aggregate |
| fix | tune `k1` and `b` on the dev split, report per family |
| delta | k1=1.2 ranked 38th of 45 settings; best setting +0.09 aggregate |
| **stops working when** | the query mix changes. The gain is a weighted average over families and the weights are your traffic's, not the corpus's |

That last line is what somebody on a different corpus needs. Everything above it is about
this one.

---

## The test

**Would this card help somebody on a corpus they have never read?**

Three outcomes.

**Yes — it is about a mechanism.** Keep it. *"An aggregate over a retrieved context cannot
tell you which member of it was load-bearing"* is true of every context, every corpus and
every metric built that way. The course found it three times in different places, which is
how it was recognised.

**No — it is about this corpus.** Keep it *only* if you can rewrite the failure as a class.

```
RFC 7159 does not know it is obsolete                            corpus-specific
The fact that disqualifies an answer can live in a document
the answer did not come from, and no metric computed over
that answer's sources can see it                                 transferable
```

The rewrite is the work of day 2 and it is harder than it looks, because the general
statement has to be *true* and not merely vaguer. A card that generalises by removing
detail until nothing is falsifiable is worse than the specific one.

**No — it is about a bug I fixed.** Delete it. A citation parser that counted the corpus's
own `[RFC3629]` reference tags was a bug; *"print what your rule matched before you believe
its count"* is a failure mode. The first is a line of code, the second is a habit, and only
one of them belongs in a library.

Expect to delete a third and rewrite a third. A thirty-card library you edited is worth
more than a sixty-card one you accumulated, and the deletions are evidence that you can
tell the difference.

---

## Why the library and not the system

The pipeline you built runs on ten documents. It is a teaching exercise and it does not
leave with you in any useful form.

The library does. It is a set of diagnostics attached to stations, each with a measured
delta and a stated boundary, and it is the thing that lets somebody debug a retrieval system
on a corpus nobody has written a blog post about. That is the only thing in this course that
generalises, and it is why the library is the portfolio artefact rather than the agent.

Sculley et al. is the argument by analogy: the expensive failures in machine-learning
systems are properties of the system's *shape* — entanglement, undeclared consumers, hidden
feedback — rather than of any line of code. Shape-level failures recur across systems. Code
bugs do not. A library of the first kind is an asset; a library of the second is a changelog.

---

## The list at the front

The library opens with the failures you **cannot** card.

Correctness is on it: twelve weeks and no diagnostic. So is the distribution-mismatch
floor — whether your eval queries resemble real ones, which is unmeasurable from inside the
eval set. So is *"a document that should have been superseded and was not"*, which has no
mechanism anywhere in the repository.

That list is the honest boundary of the library and it belongs at the **front**, not the
back, for the same reason a report's limitations come before its numbers: a reader who meets
thirty confident cards first will assume the coverage is complete.

---

> **Known** — postmortems are maintained as a durable searchable corpus rather than
> per-incident paperwork (`sre-book-postmortem`) · documentation with fixed fields records
> the uses a thing is not appropriate for, not only those it is (`gebru-2021`) · the
> expensive failure modes in ML systems are properties of system shape rather than of code
> (`sculley-2015`)
> **Inferred** — that the *conditions under which the fix stops working* field is what makes
> a card transferable and falsifiable, and is the field most often left blank. Ours
> **Inferred** — that a corpus-specific card is worth keeping only if its failure can be
> restated as a class that is still falsifiable, and that generalising by removing detail
> produces something worse than the specific version. Ours
> **Inferred** — that a bug is not a failure mode, because shape-level failures recur across
> systems and code defects do not. Ours, by analogy with `sculley-2015`
> **Derived** — a library whose uncardable failures are listed last will be read as complete,
> by the same ordering mechanism that makes a report's trailing limitations go unread
> **Unknown** — how large a useful failure library is. Thirty cards is this course's output
> and nothing establishes it as the right number
