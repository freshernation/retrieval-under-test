# Week 13 — Retrieval as a service

> **Destination**
> The system you measured, running as a service: changes arrive through a queue in any
> order and are applied correctly, the index survives a restart, the gate runs on every
> pull request without anyone deciding to run it, and other people search it through a
> door that knows who they are.

Week 10 put the pipeline behind a boundary. It was still a Python object that lived as long
as the process did, changed only when you changed it, and was evaluated when you
remembered to evaluate it. This week removes each of those three comforts.

---

## The week

| Day | Folder | What you'll be able to do |
|---|---|---|
| Mon | `day-1/` | Apply changes that arrive out of order and more than once, and get the right index |
| Tue | `day-2/` | Write the index to disk so a crash cannot half-write it, and refuse to load it wrong |
| Wed | `day-3/` | Run the gate on every pull request, with a baseline only a person can move |
| Thu | `day-4/` | Put the index behind HTTP, with keys, groups, and a queue for writers |
| Fri | `milestone/` | Ship the service: boot from the snapshot, drain the queue, say whether it is ready |

---

## Four findings

| Day | The finding |
|---|---|
| Mon | Shuffle three changes, deliver two of them twice, apply in arrival order: the index is wrong **19 times in 20**. With a version per document, **never** |
| Tue | A snapshot built without stopwords, queried with them: **19 of 26** top tens change, **6** at rank one, and nothing raises |
| Wed | `k1 = 2.0` gains 0.075 of MRR and loses one query at recall@3. **Both inside the noise.** A zero-tolerance gate blocks it; the chosen tolerance does not, and calls neither an improvement |
| Thu | A document the service answered **202 Accepted** for is not searchable until the queue drains — and `/health` is the only place that says so |

---

## What they have in common

Every one of them is the system being right about a different moment from the one you
are asking about. The change log is right in the order it was written; the snapshot was
right with the analyzer it was built with; the gate is right about nineteen queries; the
service is right about what it was asked, not about what it has done yet.

---

## `--live`

Nothing this week needs a model. The deep track is the one in `compose.yaml`: run the API
and the worker as two containers on one volume, and kill the worker in the middle of a
drain.

---

## Milestone

`operations.py` and `REPORT.md`: the service that boots, takes changes, survives a restart
and says whether it is ready to take traffic.
