"""The run ledger. Every measurement you have ever taken, written down for you.

You do not maintain this by hand. `record()` writes a file every time you
evaluate, which is deliberate: a ledger you have to remember to update is a
ledger with gaps exactly where the embarrassing results were.

`tools/check_evals.py` reads this directory and holds your milestone documents to
it — a number in prose that disagrees with the run it cites fails the build.
"""

from __future__ import annotations

import datetime as _dt
import hashlib
import json
from dataclasses import dataclass
from pathlib import Path

import yaml

from raglab.metrics import Evaluation

RUNS_DIR = Path(__file__).resolve().parent.parent / "runs"
TEST_LOG = RUNS_DIR / ".test-access.log"


def config_hash(config: dict) -> str:
    """A stable 8-character fingerprint of a configuration.

    Two runs with the same hash measured the same system. If you thought you
    changed something and the hash did not move, you did not change it — which
    catches a surprising number of afternoons.
    """
    blob = json.dumps(config, sort_keys=True, default=str).encode()
    return hashlib.sha256(blob).hexdigest()[:8]


@dataclass(frozen=True)
class Run:
    id: str
    created: str
    split: str
    n: int
    config: dict
    config_hash: str
    metrics: dict[str, float]
    note: str = ""
    compared_to: str = ""
    queries_worse: int | None = None

    def metric(self, name: str) -> float:
        if name not in self.metrics:
            raise KeyError(f"run {self.id} has no metric {name!r}; has {sorted(self.metrics)}")
        return self.metrics[name]


def _new_id(config: dict, when: _dt.datetime) -> str:
    stamp = when.strftime("%Y-%m-%d")
    salt = f"{config_hash(config)}{when.isoformat()}".encode()
    return f"{stamp}-{hashlib.sha256(salt).hexdigest()[:4]}"


def record(
    evaluation: Evaluation,
    config: dict,
    note: str = "",
    compared_to: Evaluation | str | None = None,
    metric: str = "recall@10",
    runs_dir: Path | None = None,
) -> Run:
    """Write one run to the ledger and return it.

    Reading the `test` split is logged separately and permanently. That log is
    not a punishment — it is the only way anyone, including you in three weeks,
    can tell whether a `test` number was confirmed once or fished for.
    """
    directory = runs_dir or RUNS_DIR
    directory.mkdir(parents=True, exist_ok=True)
    now = _dt.datetime.now()
    run_id = _new_id(config, now)

    worse = None
    against = ""
    if isinstance(compared_to, Evaluation):
        worse = len(evaluation.worse_than(compared_to, metric))
    elif isinstance(compared_to, str):
        against = compared_to

    run = Run(
        id=run_id,
        created=now.isoformat(timespec="seconds"),
        split=evaluation.split,
        n=evaluation.n,
        config=dict(config),
        config_hash=config_hash(config),
        metrics={k: round(v, 4) for k, v in evaluation.metrics.items()},
        note=note,
        compared_to=against,
        queries_worse=worse,
    )
    payload = {
        "id": run.id,
        "created": run.created,
        "split": run.split,
        "n": run.n,
        "config_hash": run.config_hash,
        "config": run.config,
        "metrics": run.metrics,
        "note": run.note,
        "compared_to": run.compared_to,
        "queries_worse": run.queries_worse,
    }
    (directory / f"{run_id}.yml").write_text(
        yaml.safe_dump(payload, sort_keys=False), encoding="utf-8"
    )
    if evaluation.split == "test":
        log = directory / TEST_LOG.name
        with log.open("a", encoding="utf-8") as fh:
            fh.write(f"{run.created}\t{run.id}\t{run.config_hash}\t{note}\n")
    return run


def load(run_id: str, runs_dir: Path | None = None) -> Run:
    path = (runs_dir or RUNS_DIR) / f"{run_id}.yml"
    if not path.exists():
        raise FileNotFoundError(f"no run {run_id!r} at {path}")
    raw = yaml.safe_load(path.read_text(encoding="utf-8"))
    return Run(
        id=raw["id"],
        created=raw["created"],
        split=raw["split"],
        n=raw["n"],
        config=raw.get("config", {}),
        config_hash=raw.get("config_hash", ""),
        metrics=raw.get("metrics", {}),
        note=raw.get("note", ""),
        compared_to=raw.get("compared_to", ""),
        queries_worse=raw.get("queries_worse"),
    )


def all_runs(runs_dir: Path | None = None) -> list[Run]:
    directory = runs_dir or RUNS_DIR
    if not directory.exists():
        return []
    out = []
    for path in sorted(directory.glob("*.yml")):
        try:
            out.append(load(path.stem, runs_dir=directory))
        except (KeyError, TypeError):
            continue
    return out


def test_reads(runs_dir: Path | None = None) -> list[tuple[str, str, str, str]]:
    """Every recorded read of the held-out split: (when, run id, config hash, note)."""
    log = (runs_dir or RUNS_DIR) / TEST_LOG.name
    if not log.exists():
        return []
    rows = []
    for line in log.read_text(encoding="utf-8").splitlines():
        if line.strip():
            parts = line.split("\t")
            rows.append(tuple((parts + ["", "", "", ""])[:4]))
    return rows
