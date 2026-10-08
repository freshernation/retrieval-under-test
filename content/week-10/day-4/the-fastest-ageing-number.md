# The fastest-ageing number

*Week 10 · Day 4 · about 20 minutes*

> By the end of this you can price a decision without putting a price in a result, and you
> can say why that distinction is not pedantry.

---

## Sources

| Source | Tier | What it gives you |
|---|---|---|
| [**Anthropic**, model pricing](https://www.anthropic.com/pricing) | 1 | A published rate, dated, from the vendor |
| [**OpenAI**, API pricing](https://openai.com/api/pricing/) | 1 | The same, from another vendor, for comparison |
| [**Google SRE Book**, ch. 6](https://sre.google/sre-book/monitoring-distributed-systems/) | 1 | Choosing durable signals |

> Both pricing sources are Tier 1 and both carry an obvious conflict: a vendor publishing
> its own rates. That is fine for *what the rate is* and worthless for anything else.

---

## The claim this day makes

A price per thousand tokens has fallen by more than an order of magnitude over the life of
this technology, and it will have moved again between this sentence being written and being
read.

Which makes it the fastest-ageing number in this repository — faster than a model name,
faster than a framework's API, faster than the vendor list in week 10's `--live` section.

So: **`price()` takes the rate as an argument and has no default.**

```python
def price(token_count: int, per_1k: float) -> float:
    return token_count / 1000 * per_1k
```

That is the whole mechanism. A default would be a result quoted by accident — a number
somebody reads off a function signature in eighteen months and believes.

---

## What is durable and what is not

| quantity | ages | why |
|---|---|---|
| tokens per query | **no** | a property of your pipeline and corpus |
| marginal tokens per answer | **no** | a property of your retrieval |
| the budget step that wastes | **no** | a property of your curve |
| price per 1k tokens | fast | a market |
| monthly bill | fast | the product of the two |
| "it costs $X to serve" | fastest | a market and a volume forecast |

Measure the left column. Take the right column as an argument. Report a monthly figure only
with the rate on the same line as the figure, so the number can be re-derived rather than
re-believed.

This is not a style preference. A report that says *"serving costs $4,200/month"* becomes
wrong silently. A report that says *"4.9M tokens/month; at $3.00/1M input that is
$14.70/month"* becomes **correctable**, by anybody, in ten seconds. The second form survives
the thing that kills the first.

---

## Tokens are stipulated too

`TOKENS_PER_WORD = 1.3` is a stand-in and the lab says so.

Real tokenisers vary by model, by language, and by how much of your text is identifiers —
and this corpus is unusually bad for it. `rfc-7231`, `428`, `HTTP/1.1`, ABNF fragments and
section numbers all fragment into more tokens per word than prose does. The true ratio on
this corpus is worse than the figure usually quoted, and it is worse **unevenly**: the
identifier query family fragments differently from the plain one.

Which means every per-query cost figure in this week's report is wrong by a
query-dependent amount. The direction holds — the dear budgets are dearer, the wasteful
step is still wasteful, the margin still has a cliff — and the values do not.

That is the fourth application of the stipulated-model discipline in four weeks: week 7's
positional weighting, week 8's generator, week 9's judge, week 10's clock and tokeniser.
**When a value cannot be checked, assert direction only.** It is the course's house style
now.

---

## The one thing worth doing with a real price

Not forecasting. Ranking.

A price lets you compare two designs you have already measured in tokens — *is the reranker
worth its context, is the 4,000-word budget worth 5.6×* — and that comparison is **robust to
the price being wrong**, because both sides move together. A price doubling does not change
which design is cheaper.

Forecasts are not robust to it, which is why they are the thing that embarrasses people.

So the use of a price is: order the options, make the decision, record the rate you used,
and leave the forecasting to somebody whose job it is.

---

> **Known** — published per-token rates exist and are dated by their vendors
> (`anthropic-pricing`, `openai-pricing`)
> **Inferred** — that per-token prices are the fastest-ageing figures in a technical report
> about this technology and should therefore be arguments rather than constants. Ours
> **Inferred** — that a cost figure reported alongside its rate is correctable while one
> reported alone becomes silently wrong, so the first form is the only acceptable one. Ours
> **Inferred** — that identifier-heavy text tokenises worse than prose and does so unevenly
> across query families, making per-query cost figures wrong by a query-dependent amount.
> Ours, and unmeasured here because the lab has no real tokeniser
> **Derived** — a design comparison expressed in tokens is invariant to the price level,
> since both alternatives scale by the same rate, whereas an absolute forecast is not
> **Unknown** — what a token will cost when you read this, and therefore every absolute
> figure anybody has published about the cost of serving retrieval-augmented generation
