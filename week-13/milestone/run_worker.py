"""The ingestion worker - given. Drains the queue every five seconds.

    python3 run_worker.py
"""

import os
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import conftest  # noqa: E402,F401

import raglab  # noqa: E402
from operations import boot, work_once  # noqa: E402
from sections import section_corpus  # noqa: E402


def chunker(documents):
    return section_corpus(documents, 100, 300)


def main():
    docs = {d.id: d.title + "\n" + d.text for d in raglab.corpus.load()}
    state = boot(os.environ.get("SNAPSHOT", "data/index.json"), os.environ.get("VERSIONS", "data/versions.json"),
                 os.environ.get("QUEUE", "data/queue.db"), docs, chunker, stopwords=None)
    while True:
        tally = work_once(state, chunker)
        if any(tally.values()):
            print(tally, flush=True)
        time.sleep(5)


if __name__ == "__main__":
    main()
