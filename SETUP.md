# Day zero

Twenty minutes. Do it before week 1, not during it.

---

## 1. Python

You need 3.10 or newer — the labs use `X | None` type syntax.

```bash
python3 --version
```

## 2. The repository

```bash
git clone <your fork of this repo>
cd RAG
python3 -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

The dependency list is deliberately short: `numpy`, `pyyaml`, `pytest`. There is no
retrieval library in it, because you are writing the retrieval.

## 3. Check it works

```bash
pytest tests/ -q
```

All green. Those are the tests for `raglab/`, the harness the labs run on — it ships
finished because you are not building it, you are using it.

```bash
python3 -c "import raglab; print(raglab.corpus.summary())"
python3 tools/build_corpus.py --check
```

The first prints the gold corpus — ten RFCs, sixteen queries, and which split each is in.
The second re-fetches them and confirms your checked-in copy is byte-for-byte what the
judgments were written against. An RFC is never edited after publication, so if that check
ever fails, find out why before you rebuild.

```bash
pytest week-01 -q
```

**Almost everything red.** That is correct and it stays correct until you write the code.
Every lab in this repo ships as a stub that raises `NotImplementedError`.

```bash
python3 tools/check_sources.py
python3 tools/check_evals.py
python3 tools/check_links.py
```

All three green.

## 4. No network, no API keys, no Docker — until week 10

This surprises people, so it is worth stating plainly. Weeks 1 to 9 run entirely offline
on your laptop:

- the corpus is in the repo, and `tools/build_corpus.py --check` proves it has not moved
- the embeddings for week 5 onwards are **precomputed and frozen** into `.npy` files, so
  you build the index and the search without ever calling a model
- the language-model responses for weeks 8 and 9 are **recorded cassettes**, so
  generation tests are deterministic and free

You may run against live models at any point — `raglab.cassette` has a `--live` mode —
and by week 8 you should. But nothing is *graded* on a live call, because a test whose
result depends on a model's sampling is not a test.

Docker, real services and real API keys arrive in **week 10**, and `SETUP-week-10.md`
covers them then.

## 5. A writing tool you will actually open

You will write a milestone document every week, in Markdown, in this repo. What matters
is that it lives in the same place as the runs, because a document that lives in a
different tool from the numbers stops agreeing with them by about week three.

## 6. Your AI, set up properly

Read [`ai/README.md`](ai/README.md). Seven roles, seven files, and the rule is one fresh
chat per session with the whole role file pasted in first.

The two that matter most here are the **annotator** (`ai/annotator.md`) and the
**adversary** (`ai/adversary.md`), and they are the two people skip. Any model will build
you a RAG pipeline. Very few will help you write relevance judgments without quietly
writing them *for* you — which would destroy the eval set and you would never find out.

---

## What you need to know already

- Enough Python to write a function and run `pytest`
- What a dictionary and a list comprehension are
- What an HTTP API is

That is the whole list. **No machine learning background is assumed.** No linear algebra
beyond "a dot product is a sum of products", which is re-taught in week 5. No information
retrieval background at all — that is what weeks 1 to 4 are.

**What you do not need:** a job in the field, a GPU, a cloud account, or any experience
with vector databases. Weeks are marked with a **deep track** for people who have that
background; the core is written for people who do not.

---

## The one habit to start now

When you read a claim about retrieval — a chunk size, a model, a technique that helps —
write down **who measured it, on what corpus, and when** before you write down what they
said.

It takes ten seconds. It is the entire difference between knowing something and having
read something, and by week 4 you will not be able to read a RAG blog post any other way.
