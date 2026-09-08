# Day 1 worksheet — attribute the failure

Eight answers from a retrieval system over the MRTA sample corpus. For each, fill the
three columns. **One station only**, and it is the *first* one in order 1 → 7 that failed.

The stations: **1** corpus · **2** chunk · **3** index · **4** retrieve · **5** rank ·
**6** generate · **7** measure

---

### A

**Query:** how much is a single adult fare
**Answer:** "A single adult fare is $2.75, valid for 90 minutes including transfers."
**Note:** The fare rose to $3.00 in March 2024. Both policy documents are in the corpus.

| Station | How I would confirm it | What someone would wrongly change |
|---|---|---|
| | | |

### B

**Query:** light rail ridership growth in 2025
**Answer:** "I could not find information about ridership figures."
**Note:** The 2025 ridership report is in the corpus. Its table came out of the PDF as
`Bus 41,200,000 43,900,000 45,100,000`.

| Station | How I would confirm it | What someone would wrongly change |
|---|---|---|
| | | |

### C

**Query:** can I get a refund on my monthly pass
**Answer:** "MRTA does not appear to offer refunds on passes."
**Note:** The refunds procedure is in the corpus and says a 31-day pass is refundable pro
rata in its first seven days. It never uses the word "monthly".

| Station | How I would confirm it | What someone would wrongly change |
|---|---|---|
| | | |

### D

**Query:** what does ROCC stand for
**Answer:** "ROCC appears to be an operational body within MRTA that issues track access
permits."
**Note:** The glossary is in the corpus and says Rail Operations Control Centre. It was
ranked ninth; the contractor safety document was ranked first.

| Station | How I would confirm it | What someone would wrongly change |
|---|---|---|
| | | |

### E

**Query:** who approves spending over $250,000
**Answer:** "The Board approves expenditure above $250,000."
**Note:** True but incomplete. The procurement document adds that it is on the
recommendation of the Audit and Risk Committee, and a formal tender is required. Only the
governance document was retrieved.

| Station | How I would confirm it | What someone would wrongly change |
|---|---|---|
| | | |

### F

**Query:** what is the parking charge at Eastfield station
**Answer:** "Parking at Eastfield station costs $4.00 per day."
**Note:** There is nothing about parking anywhere in the corpus.

| Station | How I would confirm it | What someone would wrongly change |
|---|---|---|
| | | |

### G

**Query:** are electric scooters allowed
**Answer:** "Uncontrolled when printed. Verify against the register before relying on this
copy. MRTA · 400 Halloran Street."
**Note:** The retrieved passage was 180 characters long.

| Station | How I would confirm it | What someone would wrongly change |
|---|---|---|
| | | |

### H

**Query:** service animal policy
**Answer:** Correct and well cited.
**Note:** The team changed the retriever this week and reported a 4-point improvement.
This query was one of six they tried by hand. Nobody knows what happened to the other
several hundred kinds of question, and there is no eval set.

| Station | How I would confirm it | What someone would wrongly change |
|---|---|---|
| | | |

---

## After you read the corpus

Which of your eight answers changed, and why?

## Your prediction

Which station produces the most failures in production RAG systems, and why?
