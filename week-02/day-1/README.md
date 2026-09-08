# Day 1 — Count the damage before you repair it

> **By the end of today** you can quantify what a document's *format* did to its text,
> and you will have a number for it before you have an opinion about it.

---

## Read first

- [ ] [**Open the file**](../../content/week-02/day-1/open-the-file.md) — 20 min
- [ ] [**What extraction destroys**](../../content/week-02/day-1/what-extraction-destroys.md) — 25 min

---

## Do this before anything else

```bash
less data/gold/rfc/documents.jsonl     # no
python3 -c "import raglab; print(raglab.corpus.load()['rfc-7725'].text)"
```

**Read RFC 7725 end to end.** It is four pages. It will take you six minutes and it is the
single highest-value six minutes in the course.

You are looking for everything in the string that nobody wrote: the form feed, the page
footer with an author's surname on it, the running header carrying the document's title
onto every page, the blank lines padding to the bottom of a page, the copyright notice
that appears in all ten documents.

Then open RFC 9309 and notice that it has none of them.

---

## Predict first

Before the lab, write down:

1. What percentage of a paginated RFC do you think is page furniture?
2. How many of RFC 3986's sentences do you think are cut in half by a page boundary?
3. How many lines does the four-page RFC 7725 share verbatim with other documents?

Three numbers. Sealed. The lab gives you all three.

---

## The lab

`damage.py`.

```python
page_break_lines(text)        is_page_footer(line)      is_running_header(line)
furniture_lines(text)         blank_run_lengths(text)   split_paragraphs(text)
repeated_lines(documents, min_documents=3)
loss_report(documents)
```

Write `is_running_header` carefully and run
`test_a_citation_is_not_a_header`. `RFC 2119` appears constantly in ordinary prose, and a
cleaner that deletes every line beginning with `RFC` eats real content — silently, and in
a way no test of your retriever would ever surface.

Then `test_one_document_in_this_corpus_has_no_pages_at_all`, which is the day.

```bash
pytest week-02/day-1 -v
```

---

## The written exercise

`week-02/day-1/damage-report.md`, one page.

Paste your `loss_report` table. Then answer:

1. **Which document is worst affected, and by which measure?** The answer differs
   depending on whether you count lines, percentages, or shared boilerplate, and saying
   which measure you chose is most of the work
2. **RFC 2324 shares two lines with the rest of the corpus; RFC 8259 shares 55.** Both are
   RFCs from the same publisher. Explain the difference, then say what it implies about a
   boilerplate detector tuned on the documents you happened to open first
3. **You have not repaired anything yet.** For each of the four damage types, write one
   sentence predicting whether repairing it will improve retrieval, and by how much

Keep that third answer. Tomorrow checks it.

---

## Deep track

> `blank_run_lengths` over the whole corpus, as a histogram. There are two populations in
> there — paragraph breaks and page padding — and they overlap. Find the threshold that
> separates them best, then say what fraction you would misclassify at that threshold, and
> what that fraction means for a cleaner that uses it.

---

## Log

`logs/stuck-log.md` and `logs/signal-log.md`.
