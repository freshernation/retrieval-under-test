# Week 9 — Friday clinic

Twenty minutes, three phases, then a retro.

Week 8 asked whether they read the answers. **This week asks whether they can say what they
do not know** — and say it first, before the numbers.

---

## Before they arrive

1. **Is the judge reported with its baseline?** All four numbers, or the report is
   uninterpretable.
2. **Does the power section come before the results?**
3. **Is the retrospective MDE audit there?** Most of the course's deltas were below the
   floor. A report that omits this is a report that has not read its own history.
4. **How many guarded metrics?** More than five and the compounding arithmetic applies.
5. **Is the false-alarm rate measured, or asserted?**
6. **Does the summary lead with a blocker?**

---

## Phase 1 — Explain (6 min)

1. *"Your judge scored 0.70. Is that good?"* **The question of the week.** It is the base
   rate. If they hesitate, ask what a judge that always says yes would score.
2. *"Its kappa is zero. What does that mean?"* It agreed with the truth exactly as often as
   chance predicts given the class balance — it has learned nothing.
3. *"Why did it call all six confidently-wrong answers good?"* It is a faithfulness judge and
   the answers are faithful. Week 8's keystone, with a model doing the checking.
4. *"How many queries to detect five points?"* 77. Then: *"and you have?"*
5. *"Which of your gate's tolerances is below your MDE?"* Ideally none.

| 5 | 3 | 1 |
|---|---|---|
| Identifies 0.70 as the base rate unprompted; connects kappa to class balance | Gets there with prompting | Reports judge accuracy as evidence of judge quality |

## Phase 2 — Change something (7 min)

### A — *"Your eval set triples to 60 queries."*

Looking for: MDE falls to about 0.056, so a 5-point regression becomes gateable and the
tolerance should tighten with it. A strong answer notices that **the gate's tolerance is a
function of the eval set** and must be revisited whenever the set changes — which nobody
does, so gates drift out of calibration silently.

### B — *"You get a real model as the judge."*

Looking for: the validation machinery runs unchanged, and the first three things to measure
are the baseline, self-agreement across runs, and the length probe. A student who says "a
real model would be better" without proposing to measure it has learned nothing this week.

### C — *"The gate fires on a release and the engineer says it is noise."*

Looking for: `detectable` — is the failure larger than the MDE? If not, they are right and
the gate is miscalibrated. If it is, the burden shifts. This is the conversation the field
is worst at.

| 5 | 3 | 1 |
|---|---|---|
| Sees the tolerance as a function of the eval set; proposes the validation before trusting a real judge | Gets there messily | Tightens the gate to catch more |

## Phase 3 — Break it (7 min)

| Attack | What you are watching for |
|---|---|
| *"Show me a metric you decided not to guard, and defend not guarding it."* | Compounding. If they guard everything, the arithmetic |
| *"Your week-6 fusion result was 0.053 on 19 queries. Was it real?"* | Below the MDE. It never was, and the course said so at the time |
| *"Your judge is length-biased with the bias flag at zero. Where did that come from?"* | The metric. Word overlap rewards more words, and week 8's faithfulness has it too |
| *"What would you instrument in production, and why not answer length?"* | AUC 0.45. It is easy, always available, and chance |
| *"Nine weeks of measurement. Name the thing you still cannot measure."* | Correctness. It has been unmeasurable since week 1 and still is |

| 5 | 3 | 1 |
|---|---|---|
| Concedes which past results were never measurable; names correctness as still out of reach | Finds it with prompting | Defends the judge, or the tight gate |

**Pass is 3 in every phase.**

---

## Retro (15 min)

1. *"On Monday you ranked four signals. What did you rank last, and what was it actually?"*
2. *"Which of your own past results did the MDE audit kill?"* Everyone has at least one.
3. *"Which station did you skip?"* This week it is often **6** — the judge section gets
   written last and thinnest, which is the opposite of the priority.
4. *"What is going in the failure library?"*
5. *"What did I explain badly?"*

---

## Instructor: what week 10 rests on

Week 10 is production: latency budgets, caching, tracing, cost, and the first real services.

- **The proxies are what you instrument.** Two signals with AUC 0.83 that need no ground
  truth — that is the observability plan, and it came out of a lab rather than a vendor
- **The gate is what runs in CI.** It needs to be fast, and week 10 is where "fast" becomes a
  number
- **`--live` mode arrives.** The first thing to do with a real model is re-run weeks 8 and 9
  and find out which comparisons survive. Set that expectation on Friday

Signal sheet: **judge reported with baseline**, and **number of guarded metrics**. The first
predicts whether they will trust a vendor's quality score; the second predicts whether their
CI gate survives its first month.

---

## Things that went wrong the first time this week was taught

- **The judge section gets written last.** It is the week's centrepiece. Check for it early
- **Somebody sets a 1-point tolerance because it looks rigorous.** Walk them through the
  false-alarm measurement; it is more persuasive than the argument
- **The retrospective audit reads as an apology.** Reframe it: the course reported every one
  of those intervals at the time, and the audit is the payoff for having done so
