#!/usr/bin/env python3
"""Enforce the evidence doctrine on `content/sources/*.yml`. See SOURCES.md.

Fails when:
  - a source has no tier, or no published/retrieved date (undated: true is legal)
  - a claim has no `sources` (only `derived` and `unknown` claims may cite nothing)
  - a `known` claim is supported only by Tier 3 or Tier 4
  - a `known` claim rests on a single source marked `conflict: true`
  - a claim references a source id that does not exist
  - a file has an empty `sources:` list without a `no_sources_reason`
  - --check-urls is passed and a URL does not resolve
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
SOURCES_DIR = ROOT / "content" / "sources"
VALID_KINDS = {"known", "inferred", "derived", "unknown"}
LOAD_BEARING_TIERS = {1, 2}


def check_file(path: Path, check_urls: bool = False) -> list[str]:
    problems: list[str] = []
    raw = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    name = path.name

    sources = raw.get("sources") or []
    if not sources and not raw.get("no_sources_reason"):
        problems.append(
            f"{name}: no sources and no `no_sources_reason`. An empty list with no "
            f"reason is indistinguishable from an unfinished file"
        )

    by_id = {}
    for src in sources:
        sid = src.get("id", "<no id>")
        by_id[sid] = src
        if "tier" not in src:
            problems.append(f"{name}/{sid}: no tier")
        elif src["tier"] not in {1, 2, 3, 4}:
            problems.append(f"{name}/{sid}: tier {src['tier']!r} is not 1-4")
        if not src.get("undated") and not src.get("published"):
            problems.append(f"{name}/{sid}: no `published` date and not marked `undated: true`")
        if not src.get("retrieved"):
            problems.append(f"{name}/{sid}: no `retrieved` date")
        if src.get("conflict") and not src.get("conflict_note"):
            problems.append(
                f"{name}/{sid}: marked conflict: true without a conflict_note saying "
                f"what the publisher sells"
            )
        if check_urls and src.get("url") and not src.get("manual"):
            problems.extend(_check_url(name, sid, src["url"]))

    for claim in raw.get("claims") or []:
        cid = claim.get("id", "<no id>")
        kind = claim.get("kind")
        cited = claim.get("sources") or []
        if kind not in VALID_KINDS:
            problems.append(f"{name}/{cid}: kind {kind!r} not in {sorted(VALID_KINDS)}")
            continue
        unknown_ids = [s for s in cited if s not in by_id]
        if unknown_ids:
            problems.append(f"{name}/{cid}: cites unknown source ids {unknown_ids}")
        if kind in {"known", "inferred"} and not cited:
            problems.append(
                f"{name}/{cid}: a {kind} claim must cite something. Only `derived` and "
                f"`unknown` may cite nothing"
            )
        if kind == "known":
            # Judged only among sources that actually resolve: a claim citing a bad
            # id has one problem, not two.
            resolvable = [by_id[s] for s in cited if s in by_id]
            if resolvable and not any(s.get("tier") in LOAD_BEARING_TIERS for s in resolvable):
                problems.append(
                    f"{name}/{cid}: a known claim rests only on Tier 3/4. Downgrade it "
                    f"to `inferred` or find a primary source"
                )
            conflicted = [s for s in resolvable if s.get("conflict")]
            if resolvable and len(resolvable) == len(conflicted) == 1:
                problems.append(
                    f"{name}/{cid}: a known claim rests on a single source with a "
                    f"declared conflict of interest. Pair it with an independent "
                    f"replication, or mark the claim `inferred`"
                )
    return problems


def _check_url(name: str, sid: str, url: str) -> list[str]:
    import urllib.error
    import urllib.request

    req = urllib.request.Request(url, method="HEAD", headers={"User-Agent": "retrieval-under-test"})
    try:
        urllib.request.urlopen(req, timeout=15)
    except urllib.error.HTTPError as exc:
        if exc.code in (403, 405):
            return [f"{name}/{sid}: {exc.code} on {url} — mark `manual: true` if you read it by hand"]
        return [f"{name}/{sid}: HTTP {exc.code} on {url}"]
    except Exception as exc:  # noqa: BLE001 — a network error is a finding, not a crash
        return [f"{name}/{sid}: could not retrieve {url} ({exc.__class__.__name__})"]
    return []


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check-urls", action="store_true", help="also resolve every URL")
    args = parser.parse_args()

    files = sorted(SOURCES_DIR.glob("*.yml")) if SOURCES_DIR.exists() else []
    if not files:
        print(f"no source files in {SOURCES_DIR.relative_to(ROOT)} yet")
        return 0

    problems = [p for f in files for p in check_file(f, args.check_urls)]
    if problems:
        print(f"{len(problems)} problems across {len(files)} source files:\n")
        for p in problems:
            print("  " + p)
        return 1
    n_claims = sum(len(yaml.safe_load(f.read_text()).get("claims") or []) for f in files)
    print(f"sources ok — {len(files)} files, {n_claims} recorded claims")
    return 0


if __name__ == "__main__":
    sys.exit(main())
