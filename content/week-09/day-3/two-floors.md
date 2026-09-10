# Two floors

*Week 9 · Day 3 · about 20 minutes*

> By the end of this you can say which of your limits more queries would fix, and which they
> would not.

---

## Sources

| Source | Tier | What it gives you |
|---|---|---|
| [**Zheng et al.**](https://arxiv.org/abs/2306.05685) | 1 | Judge self-consistency as a measured property |
| [**Cohen**](https://doi.org/10.4324/9780203771587) | 2 | The sampling floor |

---

## They come from different places

**The sampling floor** — `mde = z · sd / √n`. It comes from having a finite number of
queries, and it falls as `√n`. More queries lower it, and there is no other way to lower it.

**The judge floor** — `1 − label_agreement`. It comes from the instrument disagreeing with
itself. If a judge changes its verdict on 10% of cases between runs, a 5-point difference is
inside its own noise **at any sample size at all**.

A million queries does not fix the second. It is not sampling error; it is the ruler moving.

---

## They compose, and the larger wins

```
detectable(effect, n, sd, label_agreement)
    = effect > max(mde(n, sd), judge_noise_floor(label_agreement))
```

Which produces a decision procedure worth having:

| | |
|---|---|
| sampling floor is larger | **write more queries** |
| judge floor is larger | **fix or replace the judge** — more queries are wasted |
| both above your effect | do neither; the effect is too small to chase |

The third row is the one people never reach, and it is often the right answer. An effect
below both floors is not going to be proven by anything you can afford, and the honest move
is to decide on other grounds — cost, simplicity, correctness — and say so.

---

## Which floor binds here

This course's clean judge has label agreement 1.0, so its floor is 0. The sampling floor is
0.100 at n=19.

**Sampling binds.** More queries would help, and week 3's milestone already said thirty.

Now switch the judge's noise on: label agreement drops, the judge floor rises, and past
about 10% disagreement it overtakes sampling entirely. At that point the eval set is no
longer the constraint and adding queries is pure waste — which is a mistake with a very
recognisable shape, because "we need more eval data" is always an available answer and
sounds diligent.

---

## The third floor, unmeasured

There is one more and this course cannot quantify it.

**Your queries might not be the queries users ask.** Every number in nine weeks is
conditional on the eval set being a reasonable model of the query distribution, and nothing
inside the eval set can check that.

It is not a sampling error and it does not shrink with `n` — a thousand queries drawn from the
wrong distribution is a thousand queries drawn from the wrong distribution. The only fixes are
outside: read production logs, sample real queries, ask users.

`EVALS.md` said this in week 1, and it is worth restating on the week that quantifies
everything else: **an eval set is a model of your users. Say what it is a model of, and where
you know it is wrong.**

---

## What to report

Three lines, every time you claim a difference:

> Effect [N], n [N], sd [N], MDE [N]. Judge label agreement [N], judge floor [N].
> **Detectable: [yes/no].**

If "no", the finding is that you cannot tell — which is a real finding, and it is the one this
course has reported more often than any other.

---

> **Known** — judge self-consistency is a measured property that varies by judge and prompt
> (`zheng-2023`) · the sampling floor falls as the square root of the sample size
> (`cohen-1988`)
> **Inferred** — that the two floors compose with the larger binding, and that recognising
> which binds prevents wasted labelling. Ours
> **Derived** — a judge that changes its verdict on a fraction f of cases cannot support a
> claim about a difference smaller than f, at any sample size, since the disagreement is not
> sampling error
> **Unknown** — the size of the distribution-mismatch floor for any real system. It is
> unmeasurable from inside the eval set and it is plausibly the largest of the three
