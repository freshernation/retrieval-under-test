#!/usr/bin/env python3
"""Enforce rule 1 — no change without a measured delta. See EVALS.md.

Reads every milestone document and holds its numbers to the run ledger.

The citation form is fixed, because a checker that guesses at prose is a checker
students learn to write around:

    recall@10 0.68 (run:2026-09-08-a41c)

Fails when:
  - a milestone document cites no run at all
  - a cited run id has no file in `runs/`
  - a number in prose disagrees with the run it cites
  - a milestone cites more than one run against the `test` split
  - a milestone reports a `test` number without also citing a `dev` run
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from raglab import runs as _runs  # noqa: E402

CITATION = re.compile(r"([a-zA-Z_]+(?:@\d+)?)\s+([0-9]*\.?[0-9]+)\s*\(run:([\w.-]+)\)")
BARE_RUN = re.compile(r"\(run:([\w.-]+)\)")
TOLERANCE = 0.0051  # runs are stored to 4dp; prose is usually quoted to 2 or 3


def milestone_docs() -> list[Path]:
    return sorted(ROOT.glob("week-*/milestone/REPORT.md"))


def check_doc(path: Path, runs_dir: Path) -> list[str]:
    problems: list[str] = []
    rel = path.relative_to(ROOT)
    text = path.read_text(encoding="utf-8")

    if "[your name]" in text:
        print(f"  - {rel}: still the unedited template, skipping")
        return []

    cited_ids = set(BARE_RUN.findall(text))
    if not cited_ids:
        return [
            f"{rel}: cites no run. Every claim of improvement names a run — see EVALS.md"
        ]

    loaded = {}
    for run_id in sorted(cited_ids):
        try:
            loaded[run_id] = _runs.load(run_id, runs_dir=runs_dir)
        except FileNotFoundError:
            problems.append(f"{rel}: cites run {run_id!r}, which is not in the ledger")

    for line_no, line in enumerate(text.splitlines(), 1):
        for metric, value, run_id in CITATION.findall(line):
            run = loaded.get(run_id)
            if run is None:
                continue
            if metric not in run.metrics:
                problems.append(
                    f"{rel}:{line_no}: run {run_id} has no metric {metric!r} "
                    f"(it has {', '.join(sorted(run.metrics))})"
                )
                continue
            claimed, actual = float(value), run.metrics[metric]
            if abs(claimed - actual) > TOLERANCE:
                problems.append(
                    f"{rel}:{line_no}: claims {metric} {claimed} but run {run_id} "
                    f"recorded {actual}"
                )

    test_runs = sorted(r.id for r in loaded.values() if r.split == "test")
    dev_runs = [r for r in loaded.values() if r.split == "dev"]
    if len(test_runs) > 1:
        problems.append(
            f"{rel}: cites {len(test_runs)} runs against the held-out split "
            f"({', '.join(test_runs)}). One per milestone. Tuning against `test` is "
            f"the failure this rule exists to make impossible to do quietly"
        )
    if test_runs and not dev_runs:
        problems.append(
            f"{rel}: reports a `test` number with no `dev` run cited. The held-out "
            f"split confirms a result; it does not produce one"
        )
    return problems


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--runs", type=Path, default=ROOT / "runs")
    args = parser.parse_args()

    docs = milestone_docs()
    if not docs:
        print("no milestone reports written yet")
        return 0

    problems = [p for d in docs for p in check_doc(d, args.runs)]
    if problems:
        print(f"{len(problems)} problems across {len(docs)} milestone reports:\n")
        for p in problems:
            print("  " + p)
        return 1

    total_reads = len(_runs.test_reads(runs_dir=args.runs))
    print(f"evals ok — {len(docs)} reports, {len(_runs.all_runs(args.runs))} runs in the ledger")
    print(f"held-out split read {total_reads} time(s), all recorded")
    return 0


if __name__ == "__main__":
    sys.exit(main())
