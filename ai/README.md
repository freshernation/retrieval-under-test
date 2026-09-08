# The seven roles

One AI, seven characters. Which one you open matters more than what you type into it.

Five come from the ALTER framework (`instructor/alter-framework-prompts.md`) — Advisor,
Librarian, Tutor, Editor, Roommate — plus two this course needs: an **Annotator** and an
**Adversary**.

The **Advisor** role is missing on purpose. This repo *is* the advisor's output: the
destination, the sequence, the cut list and the milestones were decided before you
arrived. Asking an AI to redesign your curriculum in week 3 is procrastination wearing a
lab coat.

| Role | File | When |
|---|---|---|
| **Librarian** | `librarian.md` | You need to know something and do not know who to believe |
| **Annotator** | `annotator.md` | You are writing relevance judgments and want a second opinion, not a first one |
| **Tutor** | `tutor.md` | You are stuck and twenty minutes have passed |
| **Editor** | `editor.md` | Your milestone report is finished and you want it attacked |
| **Adversary** | `adversary.md` | Your retriever works. Break it |
| **Defend** | `defend.md` | Friday, on your milestone, before your instructor sees it |
| **Roommate** | `roommate.md` | Your intuition for a problem has run out |

## How to use one

Open a fresh chat. Paste the whole role file as your first message, filling in the
`[SQUARE BRACKETS]` at the top, **and paste that week's `FENCE.md`**. Then talk normally.

**Start a new chat for each session.** A chat running for three days has forgotten its
instructions and is quietly back to being a generic assistant.

## The two that ruin this course

> "Just build the RAG pipeline for me."

An AI will produce a working retrieval pipeline for any corpus in twenty seconds, with
total confidence and no evaluation. It will be *fine*. You will not be able to say why it
is fine, what it is better than, or which stage is failing when it stops being fine — and
Friday is a person asking you exactly that.

> "Here are my 40 documents and 12 queries. Write the relevance judgments."

This one is worse, and it is the reason `annotator.md` exists and is written the way it
is. An eval set written by a model is a measurement of that model's opinion. Every number
you compute against it afterwards is real-looking, reproducible, precise, and about
nothing. You would not find out. Nobody would find out.

The annotator is built to refuse this. Do not go around it by opening a plain chat — you
are only cheating the one person the course is for.

## What goes in your log

Every role ends its session by printing a `SIGNAL` block. Copy it into
`logs/signal-log.md`. Ten seconds, and it is how your instructor knows where to spend
tomorrow's hour.
