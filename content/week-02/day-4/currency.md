# Currency, and what a corpus owes its reader

*Week 2 · Day 4 · about 25 minutes*

> By the end of this you can say what your system should do when its best source is out of
> date, and why that is a policy decision rather than a technical one.

---

## Sources

| Source | Tier | What it gives you |
|---|---|---|
| [**RFC 2026**](https://www.rfc-editor.org/rfc/rfc2026.txt) §2.1 | 1 | A publisher that solved this problem deliberately, and what it cost them |
| [**RFC 7322**](https://www.rfc-editor.org/rfc/rfc7322.txt) §4 | 1 | The metadata fields, and what each one is for |

> The four policies and the argument about who owns them are ours.

---

## The IETF solved this and it is worth seeing how

The RFC series faced exactly the problem your corpus has, in 1969, and made three decisions
that are worth stealing:

1. **Never delete.** A published RFC is permanent and citable. The obsolete JSON spec is
   still there, still fetchable, still correct about what the rule was in 2014
2. **Never edit.** No silent revision. What you cite is what you read
3. **Record the relationship in the successor**, in a fixed field, in the header

The cost is a corpus permanently containing documents that are wrong if you read them as
current. The benefit is that the wrongness is **always recoverable** — mechanically, from
metadata, without judgment.

Most corpora make the opposite trade without deciding to: they edit in place, delete
freely, and record nothing. That produces a corpus where every document *looks* current and
none of them can be checked, which is worse in every way except that it feels tidier.

If you have any influence over how your corpus is produced, the RFC discipline is the thing
to argue for, and this article is the argument.

---

## Currency is not one thing

Four different properties, routinely conflated, with different fixes:

| Property | Question | Recoverable from |
|---|---|---|
| **Age** | when was this written | metadata, usually |
| **Currency** | is this still the operative version | supersession metadata, rarely |
| **Validity** | was it ever right | nothing. A human decides |
| **Applicability** | is it right *for this reader* | the query, plus context you do not have |

Age is easy and almost useless on its own — RFC 3986 is from 2005 and is completely
current; RFC 7159 is from 2014 and is withdrawn. **Sorting by date is not a currency
policy**, and it is what people build when they have not made this distinction.

Currency is what you built today. It is mechanical, cheap, and available only when somebody
recorded the relationship.

Validity is the retraction case and no pipeline can infer it.

Applicability is the hardest and the most common in practice: a document about the 2019
process is current, valid, and wrong for a user asking about their own situation. Retrieval
cannot see it. Week 8 can at best make the answer say which situation it is describing.

---

## The four policies, and who owns them

| Policy | The system says | Right when |
|---|---|---|
| **Silent** | nothing | never, once you know |
| **Annotate** | "this was superseded by X" | almost always. Cheap, honest, pushes the decision to the reader |
| **Demote** | ranks current sources first | when the current version answers the same question |
| **Refuse** | "the source I have is out of date" | when being wrong is expensive and being unhelpful is not |

The row that matters is the last one, and it is where the engineering stops.

**Whether a system should refuse to answer from a stale source is not a technical
question.** It depends on what happens when the answer is wrong. A search over
specifications: annotate, and let the reader judge. A system telling a nurse a dosage: refuse
loudly. The same code, the same graph, opposite correct behaviour.

Engineers routinely make this call by default and without noticing they have made it —
usually landing on "silent", because silent is what you get when nobody chooses. **Naming
the choice, in the report, with the reason, is the deliverable.** If the person who owns the
consequences is not you, the choice is not yours either, and the useful thing you can do is
put the number in front of them: *twenty percent of this corpus is obsolete.*

---

## What the reader is owed

A working definition, which you may argue with:

> **A retrieval system owes its reader every fact it holds that would change how the
> reader reads the answer.**

Not every fact. The reader does not need the ingest date or the chunk id. But if your
system knows the passage is from a withdrawn specification and does not say so, it is
withholding something it has, and it produced a worse answer than it was capable of.

This is a low bar and almost nothing clears it, because clearing it requires having gone and
built the metadata — which is a Thursday afternoon of regex work with no metric attached to
it, and it never gets prioritised.

---

## The number to take away

**Two of your ten documents are obsolete. Twenty percent.**

That is not a property of RFCs — the IETF is unusually good at this, and you know the number
only because they wrote it down. On a corpus where nobody recorded supersession, the
fraction is whatever it is and you cannot measure it, which is not the same as it being
zero.

The question to bring to Friday, and to your job: **what is that number where you work, and
how would you find out?**

For most corpora the honest answer to the second half is "I could not, without reading
them". That is a finding about the corpus, it belongs in a report, and it is worth more than
any retrieval improvement you could make on top of it.

---

> **Known** — the IETF never deletes or revises published RFCs and records supersession in
> the successor's header (`rfc2026`, `rfc7322`)
> **Inferred** — that age, currency, validity and applicability are routinely conflated, and
> that sorting by date is what results. Ours, from practice
> **Derived** — a corpus that edits in place and records nothing cannot have its currency
> checked mechanically, because the evidence has been overwritten
> **Unknown** — what the right default refusal policy is. It depends on the cost of a wrong
> answer, which is not a property of the retrieval system, and we know of no framework that
> makes this decision well
