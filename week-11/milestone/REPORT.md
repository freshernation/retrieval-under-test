# Project 3 report — [your name]

> Fill this in. Every number cites a run id, and every delta names the MDE of the set it
> was measured on. `tools/check_evals.py` enforces the first.

---

## 1 · The recommendation

**One sentence, first.** Somebody should be able to act on it without reading further.

Then two sentences of why.

## 2 · The target list

Week 10's attribution report named the failures. Which did you aim at, and which technique
at which station?

| Query | Station | Technique aimed at it | Did it move |
|---|---|---|---|
| | | | |

## 3 · The ceiling

The oracle over your strategies, computed **before** the mechanism.

| | answered |
|---|---|
| baseline | |
| best single strategy | |
| oracle | |
| headroom | |

**Run:** `run:<id>`

## 4 · The comparison

| | baseline | agent |
|---|---|---|
| answered | | |
| citing superseded (ids) | | |
| retrievals | | |
| tokens/query | | |
| faithfulness | | |

`answered_delta`, and the **MDE of this set at this n**, on the same line:

Is it detectable? If no, say so here and not in a footnote.

## 5 · Cost

Retrieval multiple. Token multiple. One sentence on why they differ and which one a reader
would have watched.

## 6 · What each stage did alone

| Stage | answered | superseded fixed | superseded broken | retrievals |
|---|---|---|---|---|
| rewrite | | | | |
| route | | | | |
| hop | | | | |
| loop | | | | |

**The interaction.** Any result that only appears when two stages are on: name it, and say
how durable you think it is.

**The dial that did nothing.** There is one. Name it.

## 7 · The refusal

`ship_check` output, verbatim.

Then one paragraph agreeing with it, in your own words, with the numbers in the sentences.

## 8 · What you would do instead

Ranked. Cheapest first. If one of them is *"write more queries"*, price it — week 9 has the
arithmetic.

## 9 · The MDE audit, one row longer

Week 9 built this table. Add this week's row.

| Claim | Delta | n | MDE | Above the floor |
|---|---|---|---|---|
| | | | | |

## 10 · The failure library

Two cards minimum this week. The dial that did nothing, and the query where the fix was
wrong.

> the failure · the station · the diagnostic that finds it · the fix · the measured delta ·
> the conditions under which the fix stops working

## 11 · What I could not measure

- whether a router works, because five queries decide it and the MDE at n=5 is unusable
- whether the family router's signal is approximable from anything a request carries
- whether the loop-and-hop interaction survives a change to either stage
- what a real model would do differently at any of the four stages
