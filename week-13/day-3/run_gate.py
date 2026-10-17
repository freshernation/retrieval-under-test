"""The retrieval gate, as CI runs it - given.

    python3 week-13/day-3/run_gate.py                       # the check
    python3 week-13/day-3/run_gate.py --accept "why"        # a person accepting new numbers

Exits 0 when the retriever is no worse than the baseline in `baseline.json` beside
this file, 1 when it is, 2 when there is no baseline yet.
"""

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import conftest  # noqa: E402,F401  - puts the earlier labs on the path

import raglab  # noqa: E402
from bm25 import search  # noqa: E402
from cigate import run  # noqa: E402
from postings import Index  # noqa: E402
from sections import section_corpus  # noqa: E402
from windows import parent  # noqa: E402


def main() -> int:
    docs = {d.id: d.title + "\n" + d.text for d in raglab.corpus.load()}
    index = Index(section_corpus(docs, 100, 300), stopwords=None)

    def rank(text):
        ranked = []
        for chunk in search(index, text, 60):
            if parent(chunk) not in ranked:
                ranked.append(parent(chunk))
        return ranked

    accept = sys.argv[sys.argv.index("--accept") + 1] if "--accept" in sys.argv else None
    dev = raglab.judgments.load(file="queries-extended.yml").split("dev")
    return run(rank, dev, HERE / "baseline.json", accept=accept)


if __name__ == "__main__":
    sys.exit(main())
