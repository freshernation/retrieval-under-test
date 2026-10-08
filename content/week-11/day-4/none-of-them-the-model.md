# Three things, none of them the model

*Week 11 · Day 4 · about 25 minutes*

> By the end of this you can say what decides whether a control loop works, and none of the
> three answers is the model inside it.

---

## Sources

| Source | Tier | What it gives you |
|---|---|---|
| [**Yao et al.**, *ReAct*](https://arxiv.org/abs/2210.03629) | 1 | The loop: reason, act, observe, repeat |
| [**Asai et al.**, *Self-RAG*](https://arxiv.org/abs/2310.11511) | 1 | A critic deciding whether to retrieve again |
| [**LangGraph** documentation](https://langchain-ai.github.io/langgraph/) | 3 | The loop as a framework primitive, with the cap as a parameter |

---

## The shape, and what actually decides it

Every agent diagram is the same loop. Retrieve, inspect, decide it is not good enough,
rewrite, go again. Stop when satisfied or when somebody capped it.

Three things make or break it and none of them is the model:

**The stopping condition.** What counts as satisfied. It has to be computable at serving
time — a stopping condition that needs ground truth is not a stopping condition, it is a
measurement you can only make afterwards. Week 9's retrieval confidence is the only
candidate this course has.

**The cap.** What happens when it is never satisfied. Not a safety net: on a query the
corpus cannot answer, the cap is the **only** thing that terminates the loop.

**The cost.** Which multiplies by the iteration count. Week 10 made that sentence have a
number in it; before week 10, *"the agent costs more"* was a shrug.

---

## Two details that decide whether the loop is honest

**Score the original query, not the rewritten one.**

The tempting implementation scores the current query against the context retrieved for the
current query. That loop grades its own homework: each rewrite is chosen to match the
documents it then gets credit for matching, and confidence rises while nothing improves. It
terminates early and it terminates confidently.

Score the **user's** question against every context. The bar does not move when the query
does.

**Keep the best context, not the last.**

The last iteration is, by construction, the one that failed to clear the bar. A loop that
returns its final state returns its worst attempt whenever it was capped — and capped is the
common case.

Both of these are two lines, both are the difference between a measurement and a
demonstration, and both are easy to get wrong in a way that makes the loop look better.

---

## What it cost, and what it bought

| stop_at | answered | retrievals | cost |
|---|---|---|---|
| 0.6 | **0.700** | 30 | 1.50× |
| 0.8 | **0.700** | 44 | 2.20× |
| 1.0 | **0.700** | 48 | 2.40× |

The answered rate is unchanged at every price. Not within noise of unchanged — identical.

---

## The histogram, which is the thing to read first

| stop_at | iterations |
|---|---|
| 0.6 | `{1: 15, 3: 5}` |
| 0.8 | `{1: 8, 3: 12}` |
| 1.0 | `{1: 6, 3: 14}` |

**No query, at any threshold, ever stops on iteration two.**

Either the first retrieval was good enough or the loop ran to the cap. One rewrite never
once turned a failing query into a passing one. A three-state machine with two reachable
states, and the iterations in between are the bill.

That is a strong statement and it has a mechanism behind it, from day 1: pseudo-relevance
feedback is a refinement operator. It sharpens a query that was nearly working. The queries
below the bar are the ones whose first retrieval contained nothing relevant, so the feedback
has nothing to harvest, so the second attempt is no better than the first. **The loop
inherits the limitation of its rewrite**, and no number of iterations repairs it.

Which is worth generalising, because it is the structural fact about loops: a loop whose
operator cannot redirect the query is a loop whose iteration count cannot help. Measure the
operator once before putting it in a loop, and the loop's ceiling is already known.

---

## The cap is the only termination

`r10` asks how to configure OAuth scopes. The corpus contains the word once, in a
bibliography.

Set the bar out of reach and the loop runs to whatever cap you gave it — twelve retrievals
for twelve — and its confidence **falls monotonically** from 0.44 to 0.11 as feedback terms
drag it further from the question.

The loop does not notice. Nothing in it could: every signal it has says *try again*, and
trying again is what makes it worse. There is no internal condition that distinguishes
*"not satisfied yet"* from *"not satisfiable"*, and if you want one you have to add it from
outside — a floor on confidence, a check that it is still rising, a refusal. Week 8 built a
refusal and this is where it would go.

So the cap is not a parameter you tune. It is the component that makes the loop
terminate, and on this corpus a quarter of the queries depend on it.

---

> **Known** — the standard agentic formulation interleaves reasoning, action and observation
> in a loop with an iteration limit (`yao-2023`, `langgraph-docs`) · a critic model can
> decide whether to retrieve again (`asai-2023`)
> **Inferred** — that scoring the rewritten query against its own retrieval makes a loop
> self-confirming, so the original question must be the bar. Ours
> **Inferred** — that a loop inherits the limitation of its rewrite operator, so measuring
> the operator once establishes the loop's ceiling without running the loop. Ours, and the
> histogram is the evidence
> **Inferred** — that no internal signal distinguishes *not satisfied yet* from *not
> satisfiable*, so termination on an unanswerable query is a property of the cap alone. Ours
> **Derived** — the answered rate is 0.700 at cost multiples of 1.50, 2.20 and 2.40 · no
> query stops on iteration two at any of three thresholds · with the bar out of reach the
> out-of-scope query runs the full cap of twelve while its confidence falls from 0.44 to
> 0.11
> **Unknown** — whether a model-driven rewrite produces a reachable middle state in the
> histogram. That single number would settle more about agentic retrieval than any benchmark
> we have read
