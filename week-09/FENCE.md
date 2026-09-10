# Week 9 — Concept fence

## Allowed

- Everything from weeks 1 to 8
- **LLM-as-judge**, via `raglab.judge.SimulatedJudge` — a stipulated model with switchable
  biases
- **Judge validation**: accuracy against a constant baseline, Cohen's kappa, self-agreement
  across runs, controlled bias probes
- **Serving-time proxies**: AUC, separation strength, direction
- **Power**: paired standard deviation, minimum detectable effect, required sample size,
  the judge noise floor
- **Gates**: rules with direction and tolerance, false-alarm rate, compounding

## Not yet

Production services, real models, caching, tracing · agentic retrieval, query rewriting,
routing · anything that changes the *system* rather than what you know about it

---

## The rule that matters most this week

**Every judge number is reported next to its baseline.**

A judge's accuracy alone cannot be interpreted. This week's judge scores **0.70** — which is
exactly what a judge that returns "yes" without reading anything scores, because 70% of the
answers happen to be good.

So: accuracy **and** constant-baseline accuracy. Kappa **and** baseline kappa. A judge is
not permitted into a report without the two-line calculation that says whether it has
learned anything.

## The other rule

**No tolerance below the minimum detectable effect.**

If your eval set cannot distinguish a 10-point change from zero, a gate set at 2 points is
firing on sampling noise — about as often on an improvement as on a regression. It will be
muted within a fortnight, and then it protects nothing while everybody believes it is there.

When the MDE is wider than the regression you care about, the answer is **more queries**,
not a tighter gate.
