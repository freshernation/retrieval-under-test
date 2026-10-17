"""The retrieval service - given.

    uvicorn run_service:app --host 0.0.0.0 --port 8000

Reads SNAPSHOT, VERSIONS and QUEUE (paths) and KEYS_FILE (JSON: key -> {"name",
"groups", "writer"}) from the environment. Builds the index from the corpus on the
first start, and loads the snapshot on every start after that.
"""

import json
import os
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import conftest  # noqa: E402,F401

import raglab  # noqa: E402
from operations import boot, create_service  # noqa: E402
from sections import section_corpus  # noqa: E402

CORPUS = raglab.corpus.load()
DOCS = {d.id: d.title + "\n" + d.text for d in CORPUS}
RESTRICTED = {"rfc-2324", "rfc-6585", "rfc-7725"}
ACL = {d.id: ({"staff"} if d.id in RESTRICTED else set()) for d in CORPUS}


def chunker(documents):
    return section_corpus(documents, 100, 300)


def keys():
    raw = json.loads(Path(os.environ["KEYS_FILE"]).read_text())
    return {key: {**caller, "groups": set(caller.get("groups", []))} for key, caller in raw.items()}


STATE = boot(os.environ.get("SNAPSHOT", "data/index.json"), os.environ.get("VERSIONS", "data/versions.json"),
             os.environ.get("QUEUE", "data/queue.db"), DOCS, chunker, stopwords=None)
app = create_service(STATE, ACL, keys())
