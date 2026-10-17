# At least once, in any order

*Week 13 · Day 1 · about 25 minutes*

> By the end of this you can explain why applying every change is not enough to get the
> right index, and name the one number each document needs so that it is.

---

## Sources

| Source | Tier | What it gives you |
|---|---|---|
| [**AWS**, Amazon SQS standard queues: at-least-once delivery](https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/standard-queues-at-least-once-delivery.html) | 1 | A message may be delivered more than once, and the consumer must be idempotent |
| [**Apache Kafka**, Message delivery semantics](https://kafka.apache.org/documentation/#semantics) | 1 | At most once, at least once, exactly once — and what each costs |
| [**AWS**, Dead-letter queues](https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/sqs-dead-letter-queues.html) | 1 | Setting aside a message that keeps failing, so it does not block the rest |

---

## Last week you held the pen

Every change in week 12 was a call you made: remove this chunk, add that one, in the order
you chose. Nothing arrived while you were in the middle of something else, and nothing
arrived twice.

A running system is not written by one hand. Documents are published by one process,
revised by another, withdrawn by a person in a hurry, and all of it travels to the indexer
through a queue. Queues make promises, and the promise almost every one of them makes is
modest: **every message will be delivered at least once.** Not exactly once. Not in the
order it was sent.

---

## Two things are always possible

So for every change your indexer receives, two things may be true:

1. **You have seen it before.** The queue redelivered it because an acknowledgement was
   lost, or a worker died after applying it and before saying so.
2. **Something newer has already been applied.** The revision of a document arrived before
   the original, because two messages travelled by different paths.

Applying every change, in the order it arrives, handles neither. Today's finding is how
badly: with three changes after the initial publication, shuffled, and two of them
delivered twice, the index you end with is wrong in **nineteen of twenty** deliveries.

The failures are not exotic. A withdrawal arrives before the document's first publication,
so it removes nothing — and then the publication arrives and the withdrawn document is back.
A revision arrives, and then the original, which overwrites it.

---

## One number per document

The fix is old, boring and correct. Every change carries a **version** for its document,
assigned where the change was made. The indexer remembers the last version it applied for
each document and applies a change only if it is newer.

Duplicates become harmless: the second copy is not newer than itself. Reordering becomes
harmless: the original arrives after its revision and is not newer. Nineteen wrong becomes
**zero**.

There is one way to get this wrong that the tests are written to catch. A **withdrawal is a
version too.** If you remember versions only for documents you have indexed, then after a
withdrawal there is nothing to compare a late copy of the original against — and it is
applied. Remember the version of the change, not the presence of the document.

---

## A queue on disk, and a place for the hopeless

The queue itself is a table in a SQLite file, for the same reason Agent In Production
built its job queue on a table: a crash must lose nothing, and a table shows you exactly
what is waiting.

A change that cannot be applied — an upsert with no text, an action nobody recognises — is
tried again, because some failures are temporary. After three tries it is **dead**: set
aside with its error, so that one bad document does not stop every change behind it. A
dead change is not a solved problem. It is a problem moved to somewhere a person will look,
which is only true if a person looks. Day 4's `/health` reports the count, and the
milestone refuses to call the service ready while it is not zero.

---

## What this does not solve

Versions decide between two changes to **one** document. They say nothing about two
documents that must change together — RFC 8259 arriving and RFC 7159 being withdrawn are
two changes, and for a while the index holds both or neither. Whether that matters depends
on the questions people ask in the gap. Day 4 makes the gap visible; it does not close it.
