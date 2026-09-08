"""The documents. Loading them, and being honest about where they came from.

Every document carries its provenance — where it came from and when it was
retrieved — because station 1 of the seven is *corpus*, and a corpus whose
provenance you cannot state is one you cannot defend when an answer is wrong.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path

DATA_ROOT = Path(__file__).resolve().parent.parent / "data" / "gold"
DEFAULT_SET = "rfc"


@dataclass(frozen=True)
class Document:
    """One document, as it was ingested.

    `text` is what the extractor produced, not what a human would have typed —
    including its boilerplate, its broken tables and its duplicated headers. Week
    2 is about the gap between those two things, so the harness does not clean
    anything for you.
    """

    id: str
    title: str
    text: str
    source: str
    retrieved: str
    meta: dict = field(default_factory=dict)

    @property
    def n_chars(self) -> int:
        return len(self.text)


class Corpus:
    """A document collection, addressable by id and iterable in a fixed order."""

    def __init__(self, documents: list[Document], name: str = "unnamed") -> None:
        self.name = name
        self._docs = {d.id: d for d in documents}
        if len(self._docs) != len(documents):
            seen: set[str] = set()
            dupes = {d.id for d in documents if d.id in seen or seen.add(d.id)}
            raise ValueError(f"duplicate document ids: {sorted(dupes)}")
        self._order = [d.id for d in documents]

    def __len__(self) -> int:
        return len(self._order)

    def __iter__(self):
        return (self._docs[i] for i in self._order)

    def __contains__(self, doc_id: object) -> bool:
        return doc_id in self._docs

    def __getitem__(self, doc_id: str) -> Document:
        return self._docs[doc_id]

    @property
    def ids(self) -> list[str]:
        return list(self._order)

    def get(self, doc_id: str, default: Document | None = None) -> Document | None:
        return self._docs.get(doc_id, default)


def load(name: str = DEFAULT_SET, root: Path | None = None) -> Corpus:
    """Load a shipped document set from `data/gold/<name>/documents.jsonl`."""
    base = (root or DATA_ROOT) / name
    path = base / "documents.jsonl"
    if not path.exists():
        raise FileNotFoundError(
            f"no corpus at {path}. Shipped sets: {sorted(p.name for p in (root or DATA_ROOT).iterdir() if p.is_dir())}"
        )
    docs = []
    with path.open(encoding="utf-8") as fh:
        for line_no, line in enumerate(fh, 1):
            line = line.strip()
            if not line:
                continue
            try:
                raw = json.loads(line)
            except json.JSONDecodeError as exc:
                raise ValueError(f"{path}:{line_no} is not valid JSON") from exc
            docs.append(
                Document(
                    id=raw["id"],
                    title=raw.get("title", ""),
                    text=raw["text"],
                    source=raw.get("source", "unknown"),
                    retrieved=raw.get("retrieved", "unknown"),
                    meta=raw.get("meta", {}),
                )
            )
    return Corpus(docs, name=name)


def summary(name: str = DEFAULT_SET) -> str:
    """A one-paragraph description, for `SETUP.md`'s check and for sanity."""
    from raglab import judgments as _j

    c = load(name)
    qs = _j.load(name)
    dev = [q for q in qs if q.split == "dev"]
    test = [q for q in qs if q.split == "test"]
    n_judged = sum(len(q.judgments) for q in qs)
    n_relevant = sum(len(q.relevant) for q in qs)
    chars = sum(d.n_chars for d in c)
    return (
        f"corpus '{name}': {len(c)} documents, {chars:,} characters\n"
        f"queries: {len(qs)} ({len(dev)} dev, {len(test)} test)\n"
        f"judgments: {n_judged} labelled pairs, {n_relevant} relevant (grade >= 2)\n"
        f"mean relevant per query: {n_relevant / max(1, len(qs)):.2f}"
    )
