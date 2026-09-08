"""Frozen embeddings, so weeks 5 onwards need no model and no network.

The vectors shipped in `data/gold/<set>/vectors/` were computed once, with the
model and the date recorded next to them, and they never change. That is what
makes a dense-retrieval lab gradable: your HNSW index and mine, built from the
same vectors, must return the same neighbours.

It is also a teaching point rather than only a convenience. Embeddings are a
*frozen artefact of a model at a version* — re-embed a corpus with a new model
release and every stored vector is silently incomparable with every new one.
Systems have been broken this way, quietly, for months. The manifest here is what
that discipline looks like.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

import numpy as np

from raglab.corpus import DATA_ROOT, DEFAULT_SET


@dataclass(frozen=True)
class VectorSet:
    """Vectors, their row order, and the manifest that says what made them."""

    ids: list[str]
    matrix: np.ndarray
    model: str
    dim: int
    normalised: bool
    created: str

    def __len__(self) -> int:
        return len(self.ids)

    def index_of(self, doc_id: str) -> int:
        try:
            return self.ids.index(doc_id)
        except ValueError as exc:
            raise KeyError(f"no vector for {doc_id!r}") from exc

    def get(self, doc_id: str) -> np.ndarray:
        return self.matrix[self.index_of(doc_id)]


def load(name: str = DEFAULT_SET, kind: str = "documents", root: Path | None = None) -> VectorSet:
    """Load `data/gold/<name>/vectors/<kind>.npy` and its manifest."""
    base = (root or DATA_ROOT) / name / "vectors"
    npy, manifest_path = base / f"{kind}.npy", base / f"{kind}.json"
    if not npy.exists():
        raise FileNotFoundError(
            f"no frozen vectors at {npy}. Week 5 onwards needs them; "
            f"run `python3 tools/build_vectors.py --set {name}` or pull them from the release."
        )
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    matrix = np.load(npy)
    if matrix.shape[0] != len(manifest["ids"]):
        raise ValueError(
            f"{npy} has {matrix.shape[0]} rows but the manifest lists "
            f"{len(manifest['ids'])} ids — the two are out of step, which means "
            f"every neighbour you compute is for the wrong document"
        )
    return VectorSet(
        ids=list(manifest["ids"]),
        matrix=matrix,
        model=manifest.get("model", "unknown"),
        dim=int(matrix.shape[1]),
        normalised=bool(manifest.get("normalised", False)),
        created=manifest.get("created", "unknown"),
    )
