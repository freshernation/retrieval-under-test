# Week 2 — The corpus is the system

> **Destination**
> Take a corpus you did not make, find out what is actually in it, and produce an ingest
> that reports what it lost.

Week 1's premise was that you cannot improve what you cannot measure. This week's is
narrower and less comfortable: **most of what is wrong with a retrieval system was
already wrong before retrieval started**, and you cannot see any of it from the metrics.

You will not touch the retriever. `FENCE.md` forbids it, and the reason is that while the
retriever is available to you as an explanation you will never look at the corpus
seriously.

---

## The week

| Day | Folder | What you'll be able to do |
|---|---|---|
| Mon | `day-1/` | Count what the format did to the text, before repairing any of it |
| Tue | `day-2/` | Repair it — and find out that the metric does not care |
| Wed | `day-3/` | Find near-duplicates, and say why deleting one would be wrong |
| Thu | `day-4/` | Read the metadata, and fix a failure retrieval could never have fixed |
| Fri | `milestone/` | Ship the ingest and its loss report, then defend both |

---

## What you are about to find

The corpus is ten RFCs. It looks like the easy case — plain text, one publisher, one
format, permanently archived. It is not, and every one of the following is in there
without anybody having arranged it:

- About **5% of every document is page furniture** — footers, running headers, form feeds
- **One document has none of that**, because it was published in 2022 under a different
  format. Your cleaner will silently do nothing to it and report success
- **Seventeen sentences in RFC 3986 are cut in half by a page boundary**, and stripping
  the furniture does not put them back together
- **Two documents are obsolete.** One of them flatly contradicts its replacement about
  whether JSON must be UTF-8
- **Neither obsolete document knows it is obsolete**, because an RFC is never edited after
  publication. The fact lives in the newer document
- The shortest document is **39% boilerplate**; the longest is 18%. A corpus average would
  have hidden that entirely

---

## The two results that make this week

You will make two changes you believe in. Neither will produce an interval that excludes
zero, and they fail to for different reasons — which is the whole point.

**Cleaning the corpus** removes up to 39% of every document, and moves recall@3 by exactly
nothing. The one metric that moves, moves because of a single query out of nine. By rule 1
you have measured nothing — and then on Wednesday you discover that the cleaning collapsed
eight spurious near-duplicate pairs and sharpened the real one. The value of a change does
not always appear in the task you had in mind when you made it.

**Demoting superseded documents** stops the withdrawn JSON specification outranking the
current one. The interval touches zero again. Ship it anyway, and be able to say why:
returning a specification withdrawn in 2017 is wrong on nine queries and on nine million,
and the measurement's job is not to justify a correctness fix but to prove it cost nothing.

A tuning change with no delta is superstition. A correctness fix with no delta is a
correctness fix on an eval set too small to see it. **Saying which, out loud, in the
report, is the difference between discipline and ritual.**

---

## Milestone

An ingest with a loss report. Spec in `milestone/README.md`.

---

## What this week is not about

Making the numbers go up. They mostly will not.

It is about being the person who knows that two documents in the index contradict each
other — which nobody finds by looking at recall, and everybody finds by opening the files.
