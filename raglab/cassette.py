"""Recorded model responses, so weeks 8 and 9 are deterministic and free.

A cassette maps a *prompt fingerprint* to a recorded completion. Ask for a prompt
that was recorded and you get exactly what the model said that day, every time,
on every machine, offline.

Why this exists in a course rather than only in a test suite: a generation result
that changes when you rerun it cannot be graded, and — much more importantly — it
cannot be *attributed*. Week 8 asks which station failed, and you cannot answer
that while the last station is rolling dice.

    tape = cassette.load("week-08")
    answer = tape.complete(prompt)          # recorded; KeyError if unseen
    answer = tape.complete(prompt, live=True)   # calls a real model, if configured

Live mode exists and by week 8 you should use it while developing. Nothing is
*graded* on a live call.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field
from pathlib import Path

CASSETTE_DIR = Path(__file__).resolve().parent.parent / "data" / "cassettes"


def fingerprint(prompt: str, **params) -> str:
    """A stable id for a prompt and its parameters.

    Whitespace is normalised, because a prompt that differs only in indentation is
    the same prompt and should not miss the tape. Nothing else is normalised —
    change a word and it is a different request, which is the point.
    """
    normalised = " ".join(prompt.split())
    blob = json.dumps({"p": normalised, **params}, sort_keys=True).encode()
    return hashlib.sha256(blob).hexdigest()[:16]


@dataclass
class Cassette:
    """One tape. Recorded responses, and the manifest of what recorded them."""

    name: str
    model: str
    recorded: str
    entries: dict[str, dict] = field(default_factory=dict)
    path: Path | None = None

    def complete(self, prompt: str, live: bool = False, **params) -> str:
        """The recorded completion for this prompt.

        Raises `KeyError` when the prompt is not on the tape, with the fingerprint
        in the message — that is the normal way you discover you changed a prompt,
        and it is a better error than a silently different answer.
        """
        key = fingerprint(prompt, **params)
        if key in self.entries:
            return self.entries[key]["completion"]
        if live:
            return self._live(prompt, **params)
        raise KeyError(
            f"cassette '{self.name}' has no recording for fingerprint {key}. "
            f"Either the prompt changed, or this is a new prompt — re-record with "
            f"`python3 tools/record_cassette.py --name {self.name}`, or pass live=True."
        )

    def _live(self, prompt: str, **params) -> str:
        raise NotImplementedError(
            "Live model calls are configured in week 10, in `SETUP-week-10.md`. "
            "Until then every graded path runs off the tape."
        )

    def __contains__(self, prompt: object) -> bool:
        return isinstance(prompt, str) and fingerprint(prompt) in self.entries

    def __len__(self) -> int:
        return len(self.entries)


def load(name: str, root: Path | None = None) -> Cassette:
    path = (root or CASSETTE_DIR) / f"{name}.json"
    if not path.exists():
        raise FileNotFoundError(f"no cassette {name!r} at {path}")
    raw = json.loads(path.read_text(encoding="utf-8"))
    return Cassette(
        name=name,
        model=raw.get("model", "unknown"),
        recorded=raw.get("recorded", "unknown"),
        entries=raw.get("entries", {}),
        path=path,
    )
