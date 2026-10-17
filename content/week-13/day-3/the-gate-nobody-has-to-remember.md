# The gate nobody has to remember

*Week 13 · Day 3 · about 20 minutes*

> By the end of this you can explain what changes when a gate runs on every pull request,
> and why the file it compares against is the most important thing in it.

---

## Sources

| Source | Tier | What it gives you |
|---|---|---|
| [**GitHub**, Quickstart for GitHub Actions](https://docs.github.com/en/actions/get-started/quickstart) | 1 | Where a workflow lives, and how a pull request triggers it |
| [Week 9, day 4](../../week-09/day-4/) | — | The gate, its rules, its tolerance and its false-alarm rate |

---

## A gate in a library is a gate that is skipped

Week 9 built a good gate. Rules with a direction, a tolerance from the noise floor, a
verdict that says what it checked. And then it sat in a library and ran when somebody
remembered to run it.

People remember to run their checks before the changes they are proud of. The changes they
are not sure about — the late-night one, the one-line tweak to `k1` — are the ones that go
in without. A gate that has to be remembered measures the changes that needed it least.

Today it runs on every pull request, and the arithmetic is the least interesting part.

---

## The baseline is a file, and it needs a reason

The gate compares a candidate with a **baseline**: the numbers the current system gets. If
the baseline lives on somebody's laptop, or is recomputed from `main` every time, then
"good" quietly means "whatever we last shipped". Put it in the repository as a file and
changing what good means becomes a change somebody reviews.

And it carries a **reason**. Not because a sentence makes the numbers truer, but because the
alternative is a history of baselines that moved and nobody remembers why. `write_baseline`
refuses an empty one.

---

## CI checks; people accept

The rule the tests are strictest about: **the workflow never passes `--accept`.** A gate
that writes its own new baseline whenever it passes is harmless. A gate that writes it
whenever it is told to, by a line in a YAML file, will be told to the first time it is
inconvenient — and from then on every regression becomes the new normal, one pull request
at a time. Accepting new numbers is a person, on purpose, with a reason.

---

## The tolerance is decided before the result

Today's finding. `k1 = 2.0` against the baseline, on nineteen answerable queries: MRR goes
up by **0.075**, and recall@3 goes down — by one query changing its mind.

With zero tolerance the gate blocks it. With week 9's tolerance of 0.08 — about the minimum
detectable effect on nineteen queries — it passes, and it does not call the MRR gain an
improvement either, because 0.075 is inside the same noise.

Both of those are right. The tolerance was chosen before anybody saw this change, from the
size of the eval set. Choosing it afterwards, to let a change you like through or keep one
you dislike out, is the thing the gate exists to prevent.

A real regression is not subtle: an eight-dimension dense retriever loses **0.105** of
recall@3, beyond the tolerance, and the gate says so with the numbers.

---

## What a green tick means

That the candidate is no worse than the baseline, by more than the noise, on the dev split,
on the metrics in the rules. Not that it is better. Not that it is good. Not anything about
the test split, which nobody should be looking at in a pull request. Write those four
sentences in the workflow's README and you will be asked about them less.
