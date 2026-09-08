#!/usr/bin/env python3
"""Fail when a relative link inside the repo's Markdown does not resolve.

Rot in a course's own cross-links is invisible until a student clicks one on a
Tuesday evening and quietly gives up on the reading.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LINK = re.compile(r"\[[^\]]*\]\(([^)]+)\)")
SKIP_DIRS = {".git", ".venv", "__pycache__", ".pytest_cache", "instructor", "node_modules"}


def markdown_files() -> list[Path]:
    out = []
    for path in ROOT.rglob("*.md"):
        if not SKIP_DIRS & set(path.relative_to(ROOT).parts):
            out.append(path)
    return sorted(out)


def main() -> int:
    problems = []
    for path in markdown_files():
        for line_no, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            for target in LINK.findall(line):
                target = target.split(" ")[0].strip()
                if target.startswith(("http://", "https://", "mailto:", "#")) or not target:
                    continue
                resolved = (path.parent / target.split("#")[0]).resolve()
                if not resolved.exists():
                    rel = path.relative_to(ROOT)
                    problems.append(f"{rel}:{line_no}  ->  {target}")

    if problems:
        print(f"{len(problems)} broken relative links:\n")
        for p in problems:
            print("  " + p)
        return 1
    print(f"links ok — {len(markdown_files())} markdown files")
    return 0


if __name__ == "__main__":
    sys.exit(main())
