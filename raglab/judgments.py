"""Queries, graded relevance judgments, and the split that decides your honesty.

A judgment is a person saying *this document answers this query*. Grades:

    0  irrelevant
    1  related, but does not answer it
    2  answers it
    3  answers it completely, on its own

`recall` and the rest collapse this to relevant = grade >= 2. nDCG uses the
grades, which is the only reason to record them — and the reason week 1 makes you
record them anyway is that the 1s are where you discover you disagree with
yourself.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

import yaml

from raglab.corpus import DATA_ROOT, DEFAULT_SET

RELEVANT_AT = 2
VALID_GRADES = {0, 1, 2, 3}
VALID_SPLITS = {"dev", "test"}


@dataclass(frozen=True)
class Query:
    """One query, its split, and every judgment written for it."""

    id: str
    text: str
    split: str
    judgments: dict[str, int] = field(default_factory=dict)
    note: str = ""
    family: str = ""
    """The query shape this belongs to — `identifier`, `vocabulary-gap`,
    `paraphrase`, `superseded`, `acronym`, `multi-document`, `negation`,
    `out-of-scope`, `plain`.

    Added in week 5. A mean over a mixed query set hides that two retrievers can
    score identically and be good at completely different things, and on a small
    eval set the family table is more stable than the mean — it aggregates over
    the thing that actually varies.
    """

    answer_spans: tuple[str, ...] = ()
    """Verbatim strings from the corpus that constitute the answer.

    Document-level judgments cannot see chunking. Once the unit of retrieval is
    a chunk, "did we retrieve the right document" stops being the question — a
    chunk can come from exactly the right document and contain none of the
    answer, and a chunk boundary can cut the answer in half so that **no chunk
    contains it at any k**. Nothing at document granularity notices either.

    A span is checked after collapsing whitespace, because chunking splits on
    whitespace and rejoins with single spaces. It is deliberately verbatim and
    deliberately short: you can find it by hand, and you can disagree with it.

    Written in week 4, when the unit of retrieval changed. An eval set has to be
    at the granularity of the thing you are measuring, and yours was not.
    """

    unanswerable: bool = False
    """The corpus cannot answer this query, and the correct behaviour is a refusal.

    Such a query has no relevant document *on purpose*, and every metric in this
    course scores it zero — correctly, because there was nothing to retrieve. It
    is not scored on retrieval at all; it is scored on what station 6 does with
    an empty or irrelevant candidate set, which is week 8.

    An eval set with no unanswerable queries cannot detect the single failure
    mode that reaches users most often: a fluent answer to a question the corpus
    never contained. Almost nobody includes one.
    """

    @property
    def relevant(self) -> set[str]:
        """Document ids at grade >= 2."""
        return {d for d, g in self.judgments.items() if g >= RELEVANT_AT}

    def spans_in(self, text: str) -> set[str]:
        """Which of this query's answer spans appear in `text`.

        Whitespace is collapsed on both sides first. Nothing else is normalised:
        a span is a quotation, and a quotation that needed adjusting to match is
        not evidence.
        """
        haystack = " ".join(text.split())
        return {s for s in self.answer_spans if " ".join(s.split()) in haystack}

    def is_answered_by(self, texts) -> bool:
        """Whether these texts together contain **every** answer span.

        Every, not any: r14 needs both halves of a superseded pair and neither
        document contains the comparison. A system that returns one and stops
        has produced a confident half-answer.
        """
        if not self.answer_spans:
            return False
        found: set[str] = set()
        for text in texts:
            found |= self.spans_in(text)
        return found == set(self.answer_spans)

    def grade(self, doc_id: str) -> int:
        """The grade for a document, 0 for anything unjudged.

        Treating unjudged as irrelevant is the standard assumption and it is
        wrong in a specific way worth knowing: a retriever that finds a genuinely
        good document nobody labelled is punished for it. On a small hand-built
        set this happens constantly, which is why week 1 makes you look at the
        top results your baseline returns that you never judged.
        """
        return self.judgments.get(doc_id, 0)


class QuerySet(list):
    """The queries, with the split filters you will use constantly."""

    def split(self, which: str) -> "QuerySet":
        if which not in VALID_SPLITS:
            raise ValueError(f"split must be one of {sorted(VALID_SPLITS)}, got {which!r}")
        return QuerySet(q for q in self if q.split == which)

    def by_id(self, query_id: str) -> Query:
        for q in self:
            if q.id == query_id:
                return q
        raise KeyError(query_id)


def load(
    name: str = DEFAULT_SET, root: Path | None = None, file: str = "queries.yml"
) -> QuerySet:
    """Load `data/gold/<name>/<file>`, validating grades and splits.

    `file` exists because an eval set that grows is a **new instrument**, not a
    corrected one, and results taken with the two are not comparable. Week 6
    adds ten dev queries and loads `queries-extended.yml`; weeks 1 to 5 keep the
    sixteen-query set they measured against. Editing one file in place would
    have silently invalidated five weeks of numbers, which is the mistake this
    parameter exists to make visible.
    """
    path = (root or DATA_ROOT) / name / file
    if not path.exists():
        raise FileNotFoundError(f"no queries at {path}")
    raw = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    out = QuerySet()
    seen: set[str] = set()
    for entry in raw.get("queries", []):
        qid = entry["id"]
        if qid in seen:
            raise ValueError(f"duplicate query id {qid!r} in {path}")
        seen.add(qid)
        split = entry.get("split", "dev")
        if split not in VALID_SPLITS:
            raise ValueError(f"{qid}: split {split!r} not in {sorted(VALID_SPLITS)}")
        judgments = dict(entry.get("judgments", {}) or {})
        for doc_id, grade in judgments.items():
            if grade not in VALID_GRADES:
                raise ValueError(f"{qid}/{doc_id}: grade {grade!r} not in {sorted(VALID_GRADES)}")
        out.append(
            Query(
                id=qid,
                text=entry["text"],
                split=split,
                judgments=judgments,
                note=entry.get("note", ""),
                unanswerable=bool(entry.get("unanswerable", False)),
                answer_spans=tuple(entry.get("answer_spans", []) or []),
                family=entry.get("family", ""),
            )
        )
    return out


def check_against(queries: QuerySet, corpus) -> list[str]:
    """Every problem an eval set can have that a machine can see.

    Returns a list of complaints, empty when the set is sound. Run it on your own
    judgments in week 2 — the third one catches the mistake that ruins eval sets.
    """
    problems = []
    for q in queries:
        for doc_id in q.judgments:
            if doc_id not in corpus:
                problems.append(f"{q.id}: judges {doc_id!r}, which is not in the corpus")
        if q.unanswerable and q.answer_spans:
            problems.append(f"{q.id}: marked unanswerable but carries answer spans")
        if q.answer_spans and not q.relevant:
            problems.append(
                f"{q.id}: has answer spans but no document graded >= {RELEVANT_AT}"
            )
        if q.unanswerable and q.relevant:
            problems.append(
                f"{q.id}: marked unanswerable but grades {sorted(q.relevant)} at "
                f">= {RELEVANT_AT}. It is one or the other"
            )
        elif not q.relevant and not q.unanswerable:
            problems.append(
                f"{q.id}: no document is graded >= {RELEVANT_AT}. Either judge one, or "
                f"mark it `unanswerable: true` if the corpus genuinely cannot answer it"
            )
        if q.judgments and len(q.judgments) == len(q.relevant):
            problems.append(
                f"{q.id}: every judged document is relevant — you labelled only "
                f"what you already believed was relevant, so this query cannot "
                f"punish a retriever for a bad result"
            )
    return problems
