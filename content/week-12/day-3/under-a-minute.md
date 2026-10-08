# Under a minute

*Week 12 · Day 3 · about 25 minutes*

> By the end of this you can attribute a failure to one station fast enough to be useful in
> a conversation, which is the only speed that matters.

---

## Sources

| Source | Tier | What it gives you |
|---|---|---|
| [**Google SRE Book**, ch. 15](https://sre.google/sre-book/postmortem-culture/) | 1 | Incident response as a practised skill rather than an improvised one |
| [**Voorhees**, IR evaluation](https://doi.org/10.1007/3-540-45691-0_34) | 1 | What evidence a judgment set can supply, which bounds every diagnostic |

> The seven-station walk has **no primary source**. It is this course's teaching device,
> declared as one in week 1, and nobody should cite it as literature.

---

## Why speed

Not because fast is better than careful. Because the conversation in which a retrieval
failure gets diagnosed is usually two minutes long, happening in a channel, with somebody
waiting — and the person who can name the station and the diagnostic in that window is the
one whose answer gets acted on.

The careful version happens afterwards, with the eval set, and it confirms or corrects the
fast one. But the fast one decides what gets worked on this week, and that is the decision
with the money in it.

So today is a drill. Ten scenarios, five minutes each, twice.

---

## The three answers

Every clinic asks for the same three things:

**Which station.** Walk 1 → 7 and stop at the first that could have failed. Not the first
that *did* — you do not have the evidence yet — the first that **could**. The order is doing
the work: a downstream explanation is unavailable while an upstream one is live.

**What diagnostic finds it.** One check, nameable, that distinguishes your hypothesis from
the next one. *"Look at the logs"* is not a diagnostic. *"Is `is_current` true for every
document the answer cited"* is.

**What you would not do.** The scored one.

---

## Why the third answer is scored hardest

Because naming the station is mechanical and declining to act is not.

The characteristic failure of this field is not misdiagnosis. It is *correct diagnosis
followed by the wrong work*, and the wrong work is almost always one of three things:

- **rewrite the prompt** — week 10 measured zero failures at station 6
- **change the chunker** — week 10 measured zero failures at station 2
- **get a better model** — which is station 6 with a budget attached

All three are available, all three feel like progress, and all three are downstream of where
the failures are. The rule exists because the pull towards them is strong enough that
knowing better is not sufficient; you have to have practised saying no.

And there is a fourth, subtler one worth naming: **collect more metrics**. A dashboard is
not a diagnostic. Week 9 measured the two signals a dashboard would carry at AUC 0.45 and
0.46 — chance — while the two informative ones were on nobody's.

---

## The station people over-use

**Station 4.** Nearly everybody.

It is the most satisfying station: retrieval is tunable, the knobs are visible, there is
always a sweep available, and a retrieval failure is nobody's fault in particular. So an
ambiguous failure gets attributed to the candidate set by default.

The two it steals from:

**Station 1.** The corpus does not contain the answer, or contains a superseded one, or
contains the answer in a form the extractor destroyed. Station 1 failures feel *finished* —
ingest was built in week 2 and nobody has looked since — and week 10's cache finding is a
station-1 failure that arrives a month after ingest stopped changing.

**Station 7.** The measurement is wrong. Three of the ten clinics are station 7, and that
proportion is not an accident: *"the number says we are fine and the users say we are
not"* is the most common real-world retrieval complaint there is, and it is a statement
about the instrument.

So the drill has a specific bias to correct. When you land on 4, check 1 and 7 once before
committing. It costs five seconds.

---

## What to do when you are wrong

In the drill, say so and name what you reached for. That is the written exercise's second
question and it is the point of doing this in pairs.

In real life, the same: the fast answer is a hypothesis, the diagnostic is what tests it,
and an attribution that survives its diagnostic is worth saying out loud again. One that
does not gets replaced without ceremony.

The thing not to do is defend the first attribution because you said it in a channel. The
seven-station walk is cheap enough to redo, and the cost of being wrong for a week about
which station failed is a week.

---

> **Known** — incident diagnosis is a practised skill supported by a written record rather
> than an improvised one (`sre-book-postmortem`) · a judgment set bounds what any diagnostic
> can establish (`voorhees-2002`)
> **Inferred** — that the two-minute diagnosis decides what gets worked on and is therefore
> the decision with the cost attached, while the careful version confirms it afterwards.
> Ours
> **Inferred** — that the characteristic failure of applied retrieval work is correct
> diagnosis followed by downstream work — the prompt, the chunker, a better model, more
> dashboards — and that declining it has to be practised rather than merely understood. Ours
> **Inferred** — that station 4 is systematically over-used because it is tunable and
> blameless, and that it steals from stations 1 and 7. Ours, from running these clinics
> **Derived** — week 10's attribution over twenty queries put zero failures at stations 2 and
> 6, so the prompt and the chunker were not where this system's failures were
> **Unknown** — whether the over-use of station 4 is general or an artefact of how this course
> teaches. It is consistent across the clinics we have run, which is not a sample
