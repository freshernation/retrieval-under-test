#!/usr/bin/env python3
"""Fetch the gold corpus from the RFC Editor and write it to data/gold/rfc/.

    python3 tools/build_corpus.py            # fetch and write
    python3 tools/build_corpus.py --check    # verify the checked-in copy still matches

The corpus is **checked in**, so nothing in the course needs the network. This
script exists so that the provenance of every document is a URL and a date rather
than an assertion, and so you can see exactly what was and was not done to the
text on the way in.

What this script does to the text: **nothing.** It strips no boilerplate, joins no
lines, removes no page footers, and repairs no tables. Week 2 is about the gap
between the text you think you have and the text you have, and a build script that
quietly cleaned the corpus would be teaching the opposite lesson while claiming
the credit for it.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
import time
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "data" / "gold" / "rfc"
BASE = "https://www.rfc-editor.org/rfc/rfc{n}.txt"

# Ten documents, chosen so that every failure this course teaches is present in a
# corpus a student can read in an afternoon and search by hand.
#
#   why: what this document is here to make possible
DOCUMENTS = [
    dict(n=3986, title="Uniform Resource Identifier (URI): Generic Syntax", year=2005,
         why="the long one, and the ASCII syntax diagram the extractor cannot keep"),
    dict(n=6265, title="HTTP State Management Mechanism", year=2011,
         why="cookies. Users say 'cookie expiry'; the document says 'Max-Age' and 'Expires'"),
    dict(n=6585, title="Additional HTTP Status Codes", year=2012,
         why="429, 428, 431, 511. Exact identifiers, and 'rate limit' appears nowhere"),
    dict(n=7725, title="An HTTP Status Code to Report Legal Obstacles", year=2016,
         why="451, in four pages. The shortest document, and the easiest to verify by hand"),
    dict(n=7159, title="The JavaScript Object Notation (JSON) Data Interchange Format", year=2014,
         why="**obsoleted by 8259.** Half of the first real supersession pair"),
    dict(n=8259, title="The JavaScript Object Notation (JSON) Data Interchange Format", year=2017,
         why="the current JSON spec. The other half. Same title, same subject, one is wrong"),
    dict(n=5785, title="Defining Well-Known Uniform Resource Identifiers (URIs)", year=2010,
         why="**obsoleted by 8615.** The second supersession pair, so it is not a fluke"),
    dict(n=8615, title="Well-Known Uniform Resource Identifiers (URIs)", year=2019,
         why="the current well-known URIs spec"),
    dict(n=9309, title="Robots Exclusion Protocol", year=2022,
         why="robots.txt, standardised 28 years after it was invented. The most recent document"),
    dict(n=2324, title="Hyper Text Coffee Pot Control Protocol (HTCPCP/1.0)", year=1998,
         why="418. Published on 1 April 1998 and it is a joke. Station 1 asks whether it belongs"),
]


def fetch(number: int) -> str:
    url = BASE.format(n=number)
    req = urllib.request.Request(url, headers={"User-Agent": "retrieval-under-test (course corpus)"})
    with urllib.request.urlopen(req, timeout=30) as response:
        return response.read().decode("utf-8", errors="replace")


def build(check_only: bool = False) -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    path = OUT / "documents.jsonl"
    retrieved = time.strftime("%Y-%m-%d")

    existing = {}
    if path.exists():
        for line in path.read_text(encoding="utf-8").splitlines():
            if line.strip():
                doc = json.loads(line)
                existing[doc["id"]] = doc

    rows, drifted = [], []
    for spec in DOCUMENTS:
        doc_id = f"rfc-{spec['n']}"
        if check_only and doc_id not in existing:
            print(f"  ! {doc_id} is not checked in")
            drifted.append(doc_id)
            continue
        print(f"  {doc_id} …", end="", flush=True)
        try:
            text = fetch(spec["n"])
        except Exception as exc:  # noqa: BLE001
            print(f" FAILED ({exc.__class__.__name__})")
            if check_only:
                continue
            return 1
        digest = hashlib.sha256(text.encode()).hexdigest()[:16]
        print(f" {len(text):>7,} chars  sha {digest}")

        if check_only:
            if existing[doc_id]["meta"].get("sha256_16") != digest:
                drifted.append(doc_id)
            continue

        rows.append(
            {
                "id": doc_id,
                "title": spec["title"],
                "text": text,
                "source": BASE.format(n=spec["n"]),
                "retrieved": retrieved,
                "meta": {
                    "rfc": spec["n"],
                    "published": spec["year"],
                    "format": "text/plain",
                    "sha256_16": digest,
                    "why_it_is_here": spec["why"],
                },
            }
        )
        time.sleep(0.5)

    if check_only:
        if drifted:
            print(f"\n{len(drifted)} documents no longer match the checked-in copy: {drifted}")
            print("An RFC's text is meant to be immutable. If this fires, find out why before")
            print("you rebuild — a corpus that changed under you invalidates every judgment.")
            return 1
        print(f"\ncorpus ok — {len(DOCUMENTS)} documents match the checked-in copy")
        return 0

    with path.open("w", encoding="utf-8") as fh:
        for row in rows:
            fh.write(json.dumps(row, ensure_ascii=False) + "\n")
    total = sum(len(r["text"]) for r in rows)
    print(f"\nwrote {len(rows)} documents, {total:,} characters to {path.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="verify the checked-in copy")
    sys.exit(build(parser.parse_args().check))
