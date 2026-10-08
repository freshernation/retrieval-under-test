# Attribution by machine

*Week 10 · Day 3 · about 20 minutes*

> By the end of this you can read an attribution report, and you will know why the two
> empty rows are the result.

---

## Sources

| Source | Tier | What it gives you |
|---|---|---|
| [**OpenTelemetry**, trace specification](https://opentelemetry.io/docs/specs/otel/trace/api/) | 1 | The record the walk runs over |
| [**SQuAD**](https://arxiv.org/abs/1606.05250) | 1 | Answer spans as ground truth, which is what each branch tests against |

> The attribution walk itself has **no primary source**. It is this course's teaching
> device, stated as one in week 1 and implemented here. Nobody should cite it as
> literature.

---

## The walk, as code

Nine lines.

| station | the test |
|---|---|
| 1 corpus | the query has no answer spans at all |
| 2 chunk | spans exist, and no chunk contains them |
| 4 retrieve | a chunk has them, and the shortlist does not |
| 5 rank | the shortlist has them, and the packed context does not |
| 6 generate | the context has them, and the answer is unfaithful |
| 7 none | every station did its job |

There is **no station 3 branch**. An index failure — a tokenisation bug, a missing field, a
stale segment — presents as a retrieval failure, and the trace cannot distinguish them.
Saying that is better than inventing a test that pretends otherwise. Week 3 is where you
would go to tell them apart, and it needs evidence this record does not carry.

The order is the whole value. A downstream failure cannot be reported while an upstream one
exists: `r19`'s answer is unfaithful **and** its shortlist never contained the answer, and
the walk reports retrieve. Fixing the prompt for a query whose candidates are empty is the
characteristic wasted week in this field.

---

## The report

Twenty dev queries:

| station | queries |
|---|---|
| 1 corpus | 1 |
| 2 chunk | **0** |
| 4 retrieve | 2 |
| 5 rank | 3 |
| 6 generate | **0** |
| 7 none | 14 |

Six failures. Five of them are the candidate set — two queries whose shortlist never
contained the answer, three where the word budget dropped a chunk that did.

And the six are **exactly** week 8's six confidently-wrong answers, found without being
told which six they were.

---

## The two zeros

**Station 6 is empty.** Station 6 is the prompt. It is where essentially all public
effort in this field goes, it is where the tooling is, it is what the vendor conferences
are about, and on this corpus it has not failed once.

**Station 2 is empty.** Station 2 is the chunker — the other thing people rewrite, and the
decision week 4 showed has no primary literature behind it at all. Also clean.

Those two rows are the week's result, and they are worth more than the latency work that
earned the right to read them. Not because prompting and chunking never fail — week 8 built
a generator that fails on demand, and week 4 measured chunk size dominating at every k —
but because **on this system, today, they are not where the failures are**, and the report
says so in a form that is hard to argue with.

The honest reaction is some version of *"so the model was fine all along"*, delivered
flatly, as a letdown. It is the opposite of a letdown. It is five weeks of prompt
engineering that nobody is now going to do.

---

## What `7 none` does not mean

Fourteen queries attributed `7 none`. One of them is `r05`.

`r05` asks whether JSON must be UTF-8. Its answer is perfectly faithful — 1.00 — every
citation resolves, the context contains the answer spans, and it is grounded in RFC 7159,
withdrawn in December 2017 and wrong about precisely this.

Every station did its job. The answer is wrong.

The walk is blind to it for the same reason week 8's faithfulness was: the disqualifying
fact lives in a **different document**, and no stage of the pipeline is responsible for
noticing. There is no branch to add, because there is no station at fault.

Which is where station 7 comes in. `7 none` means *the pipeline is not the problem* — and
when the answer is still wrong, the problem is what you are measuring. That is a station-7
failure, it has been a station-7 failure since week 1, and the attribution report's job is
to stop you from mistaking a clean trace for a correct answer.

---

> **Known** — answer spans are the ground truth each branch of the walk tests against
> (`squad-2016`) · a span's attributes are the record the walk reads (`otel-spec`)
> **Inferred** — that attributing to exactly one station and refusing to report downstream
> of the break prevents the characteristic wasted effort of this field. Ours. It is a
> teaching device with no primary source and the course says so
> **Inferred** — that an index failure is not separable from a retrieval failure in a trace
> of this shape, so no station 3 branch should exist. Ours
> **Derived** — the walk names a station for exactly the six queries week 8 measured as
> confidently wrong, and clears the other fourteen, without being given that list · five of
> the six failures are stations 4 and 5, so the candidate set rather than the prompt
> **Unknown** — whether the empty station 6 row generalises past this corpus and this
> simulated generator. It will not, in general; what generalises is running the walk before
> choosing the work
