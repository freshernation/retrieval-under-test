# What this course does not teach

An advisor's most valuable output is the cut list. Every item below is a real thing
engineers use, and every one is out.

- **Framework tours.** No LangChain, LlamaIndex or Haystack survey. One agent framework
  appears in week 11, after you have built the pattern by hand and can say what the
  framework is doing
- **Vector database vendor comparison.** No Pinecone-versus-Weaviate-versus-Qdrant. You
  build an HNSW index in week 5; after that they are all the same idea with different
  billing
- **Model training of any kind** — no fine-tuning embeddings, no adapters, no distilling
  a reranker. It is a real technique and it is the last thing you should reach for
- **Prompt engineering as a subject.** Prompts appear in week 8 as station 6 and are
  measured like everything else. There is no week on prompt patterns
- **Leaderboard chasing.** No MTEB rankings as a shopping list. Week 5 teaches why the
  top model on MTEB is frequently worse on your corpus
- **GraphRAG, knowledge graphs, and entity extraction pipelines**
- **Multimodal retrieval** — images, audio, video. Week 2 handles figures and tables only
  as far as "what did the extractor lose"
- **Serving and infrastructure at scale** — sharding a vector index, replication, GPU
  serving. Week 10 gets it running and priced on one machine, and stops
- **Security and access control on retrieval.** Real, hard, and a different course
- **Agent frameworks as an organising idea.** Week 11 is one week, and it is partly about
  when agentic retrieval is a worse answer than a better retriever
- Everything with a vendor's name on it that will be renamed within two years

---

## Why

Every item above is learnable later in about a week, and **none of them is what fails
people building retrieval systems.**

What fails people is: shipping without an eval set, changing three things at once,
reporting a mean that hides a collapsed query class, tuning on the held-out split without
noticing, blaming the model for a parsing failure, and being unable to say which stage
went wrong. Those six things are the whole course.

Say this out loud in week 1. Students who know *why* something was cut stop worrying that
they are missing it, and that worry is a major cause of drift in month two.

---

## The two that will be argued about

**No vector search until week 5.** Every competitor starts there, and it is what students
think they are buying. A vector database in week 1 teaches you that retrieval is a
solved thing you install. It is not, and the students who believe it plateau at "mostly
fine" and cannot say why — because they never saw what dense retrieval was better
*than*, or the queries where it is worse.

The concession: you will watch a friend on another course have a working demo in week 1
while you are still labelling. That is real and it is uncomfortable. In week 6 you will
be able to say why their demo fails on acronyms and they will not.

**No framework until week 11.** The counter-argument is that nobody writes their own
retrieval loop in industry, which is true. But you will spend your career debugging one,
and a framework you cannot see inside is a stage of the pipeline you can never attribute
a failure to. Forty lines of BM25, written once, buys ten years of being able to reason
about a search engine.

---

## What to add afterwards, in order

1. **One retrieval engine, properly.** Lucene's scoring and query internals, or
   pgvector's index types. The most common real gap
2. **Run something people use.** Nothing teaches query distribution like reading a week
   of real logs and discovering what people actually type
3. **Read three papers end to end** — Robertson & Zaragoza, the RRF paper, and one from
   your own domain
4. **Fine-tune an embedding model** on your own labelled data, now that you have some
5. **The organisational half** — who decides what goes in the corpus, and who is
   accountable when the answer is wrong. It decides more real systems than any technique
   here, and this course deliberately ignores it
