# The change you cannot prove

*Week 2 · Day 2 · about 25 minutes*

> By the end of this you can tell a tuning change from a correctness fix, and you will know
> which of them may be shipped without a measured delta.

---

## Sources

| Source | Tier | What it gives you |
|---|---|---|
| [**Smucker, Allan & Carterette**](https://dl.acm.org/doi/10.1145/1321440.1321528) | 1 | Which significance tests hold up on retrieval results |
| [**Lin, *The neural hype***](https://sigir.org/wp-content/uploads/2019/01/p040.pdf) | 1 | What a field looks like when improvements are reported without this discipline |

> The tuning-versus-correctness distinction in this article is ours. It is a refinement of
> rule 1 in `EVALS.md`, added while building week 2, because the rule as originally stated
> would have forced the wrong answer twice in five days.

---

## The situation

You have just removed a third of your corpus. recall@3 is unchanged to four decimal places.
recall@5 improved by 0.100 — and the improvement is one query out of nine, with an interval
of [+0.000, +0.300] that touches zero.

Rule 1 says: no change without a measured delta. You have no measured delta.

So do you ship it?

The honest first answer is **no, not on this evidence**, and it is worth sitting with how
uncomfortable that is. You know cleaning is right. Everyone knows cleaning is right. The
whole industry cleans. And you have a measurement, taken carefully, on judgments you wrote
yourself, that declines to support it.

---

## Three wrong ways out

**"The eval set is too small."** True, and it is a reason to grow the eval set, not a reason
to ignore this one. "My instrument disagrees with me so I will disregard the instrument" is
the position rule 1 exists to make impossible to hold quietly. If you would accept a
+0.100 with this interval as evidence *for* a change, you must accept it as evidence for
nothing.

**"It is obviously better."** This is the one that feels like engineering judgment and is
not. Every change anyone has ever made was obviously better to the person making it. The
industry's chunk-size folklore is entirely made of things that were obviously better.

**"I will keep tuning until it shows."** This is how a held-out split dies. Not through
dishonesty — through a sequence of individually reasonable retries.

---

## The distinction that resolves it

Not every change is the same kind of thing.

**A tuning change** adjusts a parameter or a heuristic to make the system score better.
Chunk size, `k`, a fusion weight, a similarity threshold. It has no independent
justification: the only argument for chunk size 400 over 512 *is* the number. **A tuning
change with no delta is superstition** — there is nothing else holding it up. Hold it.

**A correctness fix** repairs something that is wrong independent of any measurement.
Returning a specification withdrawn in 2017 is wrong. Indexing the copyright notice as
though it were content is wrong. These would still be wrong if your eval set contained no
query that noticed, if your eval set were empty, if you had no eval set at all.

For a correctness fix, the measurement's job changes completely. It is not there to justify
the change — the defect justifies the change. **It is there to prove the change cost
nothing**, which is a question an interval on nine queries can actually answer, via
`worse_than` rather than via the mean.

---

## Applying it, honestly

So which is cleaning?

It is genuinely arguable, and the argument is the exercise. The case for correctness: page
footers are not content, they were inserted by a publishing process, and indexing them as
text misrepresents the document. The case for tuning: nothing is *wrong* — the text is a
faithful rendering of what was published, you are removing it because you believe it will
retrieve better, and that belief is exactly the kind of claim rule 1 governs.

Our reading is that cleaning is mostly a **tuning change** dressed as a correctness fix,
which is why it is worth the discomfort of holding it — and then tomorrow you discover it
collapsed eight spurious near-duplicate pairs, which *is* a measured delta, on a different
task, and it ships on that evidence instead.

Thursday's demotion is the clean case in the other direction: unambiguously a correctness
fix, unambiguously unprovable on nine queries, and it ships.

**The wrong answer this week is not "ship" or "hold". It is failing to say which kind of
change you were making.** A report that ships both without the distinction and a report
that holds both without it are the same report, and neither is engineering.

---

## The amendment

`EVALS.md` rule 1 now reads, in full:

> No change without a measured delta — **or, for a correctness fix, a measurement showing
> it cost nothing.** Say which kind of change you are making, in the report, every time.

This course amends its own doctrine when the doctrine turns out to be incomplete, and says
so, with the date and the reason. A rule that cannot be amended is not being applied
seriously — it is being recited, and the difference shows up exactly here, on the day the
rule as written would force you into an answer you know is wrong.

---

## What this is not a licence for

It would be very easy to read this article as "call it a correctness fix and ship
anything". Three guards:

- **A correctness fix names the defect first**, in terms that do not mention your metric.
  If you cannot state what is wrong without saying "recall", it is a tuning change
- **It still requires `worse_than` to be empty.** A correctness fix that breaks queries is
  a trade, and a trade needs the full argument
- **The defect must be one a user would recognise.** "The obsolete spec outranks the
  current one" passes. "Chunks are not aligned to section boundaries" does not — that is a
  hypothesis about retrieval quality, which is a tuning change

---

> **Known** — paired significance testing is the appropriate discipline for IR comparisons
> (`smucker-2007`) · a field that reports improvements without it accumulates results that
> do not survive scrutiny (`lin-neural-hype`)
> **Inferred** — that separating correctness fixes from tuning changes prevents both the
> superstition failure and the paralysis failure. Ours, and week 2 is the argument for it
> **Derived** — a confidence interval containing zero is consistent with no change, so it
> cannot on its own support a claim of improvement
> **Unknown** — whether practitioners who adopt this distinction classify changes
> consistently. We would expect substantial disagreement at the boundary, and the boundary
> is where it matters
