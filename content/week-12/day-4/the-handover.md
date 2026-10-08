# The handover

*Week 12 · Day 4 · about 20 minutes*

> By the end of this you can write the one page that saves the next person a month, and you
> will know which month.

---

## Sources

| Source | Tier | What it gives you |
|---|---|---|
| [**Gebru et al.**, *Datasheets for Datasets*](https://arxiv.org/abs/1803.09010) | 1 | Provenance, intended use, and what a dataset is not for |
| [**Google SRE Book**, ch. 15](https://sre.google/sre-book/postmortem-culture/) | 1 | The record that outlives the person who wrote it |
| [**Sculley et al.**](https://papers.nips.cc/paper_files/paper/2015/hash/86df7dcfd896fcaf2674f757a2463eba-Abstract.html) | 1 | Undeclared consumers and the cost of undocumented coupling |

---

## One page, five things

Written for somebody who inherits this system when you no longer work here. Not a design
doc — a design doc describes what exists, and this describes what they will get wrong.

**1 · What the eval set is, how it was built, and what it cannot see.**

Where the queries came from, who wrote the judgments, what the splits are, and the list of
things it is blind to. Correctness is on that list. So is whether the queries resemble real
traffic, which is unmeasurable from inside the set and is plausibly the largest of the three
floors.

Without this they will treat the set as ground truth, because that is what a judgment file
looks like.

**2 · The three numbers to watch, and the gate.**

Three, not ten — week 9's compounding arithmetic, and ten metrics at 5% each fire on two
builds in five. The tolerance for each, and the sentence that the tolerance came from the
MDE and must be revisited when the set changes.

**3 · The two empty stations.**

This is the entry that saves the month.

Week 10's attribution found **zero failures at station 6 and zero at station 2** — the prompt
and the chunker. Those are exactly the two things a new person will start on, because they
are the two things the field talks about and they are both pleasant work.

Write it down with the numbers: *the attribution report says the failures are in the
candidate set; before you touch the prompt, re-run it and check that is still true.*

**4 · The failures with no card.**

So they are not surprised by them, and so they do not spend a week discovering that
correctness is hard. The list is short and it is honest and it belongs here.

**5 · What you would do with one more week.**

Ranked, cheapest first. For this course the answer is *write more queries*, priced at 77 for
five points — which is a real plan with a number, and it is more useful than any opinion
about the architecture.

---

## What not to put in it

**A tour of the code.** They can read the code. What they cannot read is which parts of it
you no longer believe in.

**Your best numbers.** Those are in the report.

**Advice.** *"Be careful with chunking"* is not actionable. *"Chunk size 400 dominated at
every k on this corpus, the sweep is in week 4's milestone, and nothing in the literature
derives any particular size"* is.

The difference is that the second one tells them what to re-run.

---

## And the undeclared consumer

Sculley's term, and it is the thing most likely to break after you leave.

Somewhere there is a thing depending on your system that you do not know about: a dashboard
reading a metric, a script parsing your output format, somebody's weekly report quoting your
faithfulness number. None of them are in your tests and all of them break when you change
something reasonable.

For a retrieval system there is a specific one worth naming: **somebody is quoting a number
whose meaning you have narrowed.** If faithfulness went into a slide in month two and you
discovered in month four that it is 1.00 while 30% of answers are wrong, the slide is still
circulating and the number is still 1.00.

Say so, in the handover, by name. *"Faithfulness appears in the Q3 review deck. It does not
mean what that deck implies. Here is the one-sentence correction."*

That is the least glamorous paragraph you will write in twelve weeks and it is the one most
likely to prevent a specific wrong decision.

---

## The last thing

The handover is written for a person who does not exist yet and may never read it, which
makes it the easiest thing in the milestone to skip and the only artefact whose value
depends entirely on having been written in advance.

It is also the best test of whether you understood your own system. One page, five
headings, no code. If you cannot write it, the thing you cannot write is the thing you do
not know.

---

> **Known** — dataset documentation records provenance, intended use and inappropriate uses
> (`gebru-2021`) · an incident record is written to outlive its author
> (`sre-book-postmortem`) · undeclared consumers couple systems invisibly and break on
> reasonable changes (`sculley-2015`)
> **Inferred** — that a handover describes what the next person will get wrong rather than
> what exists, since the code already describes the latter. Ours
> **Inferred** — that naming the two empty stations is the highest-value entry in a retrieval
> handover, because they are simultaneously where the failures are not and where a new person
> will start. Ours
> **Inferred** — that a narrowed metric circulating in an old document is the most likely
> undeclared consumer of a retrieval system, and naming it specifically is more effective
> than a general caution. Ours
> **Derived** — guarding three metrics rather than ten reduces the spurious-alarm probability
> from about 40 percent to about 14 percent at 5 percent each, which is why the handover names
> three
> **Unknown** — whether handover notes are read. We have no evidence either way and the
> argument for writing one does not depend on it
