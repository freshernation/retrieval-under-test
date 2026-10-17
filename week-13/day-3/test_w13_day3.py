"""Day 3 — the gate runs itself.

`test_zero_tolerance_blocks_a_change_the_noise_floor_lets_through` is the day.
"""

import json
from functools import cache
from pathlib import Path

import pytest

import raglab
from bm25 import search
from cigate import RULES, decide, measure, read_baseline, run, write_baseline
from dense import DenseRetriever
from gate import HIGHER, Rule
from postings import Index
from sections import section_corpus
from windows import parent

CORPUS = raglab.corpus.load()
DOCS = {d.id: d.title + "\n" + d.text for d in CORPUS}
HERE = Path(__file__).resolve().parent


@cache
def chunks():
    return section_corpus(DOCS, 100, 300)


@cache
def dev():
    return raglab.judgments.load(file="queries-extended.yml").split("dev")


def documents(chunk_ids):
    out = []
    for chunk in chunk_ids:
        if parent(chunk) not in out:
            out.append(parent(chunk))
    return out


@cache
def bm25_index():
    return Index(chunks(), stopwords=None)


def bm25(k1=1.2):
    return lambda text: documents(search(bm25_index(), text, 60, k1=k1))


@cache
def small_dense():
    return DenseRetriever(dims=8).fit(chunks())


@cache
def baseline():
    return measure(bm25(), dev())


def test_measure():
    assert baseline() == {"mrr": 0.8202, "recall@3": 0.9123, "n": 19}


def test_a_real_regression_is_blocked():
    """An 8-dimension dense retriever loses 0.105 of recall@3 - beyond the noise."""
    candidate = measure(lambda t: documents(small_dense().search(t, 60)), dev())
    verdict = decide(baseline(), candidate)
    assert not verdict["pass"] and len(verdict["failures"]) == 1
    assert verdict["failures"][0].startswith("recall@3: 0.9123 -> 0.8070")


def test_zero_tolerance_blocks_a_change_the_noise_floor_lets_through():
    """k1 = 2.0 gains 0.075 of MRR and loses one query at recall@3. Both are inside
    the noise floor on nineteen queries: zero tolerance blocks it, the chosen
    tolerance passes it, and neither calls it an improvement."""
    candidate = measure(bm25(k1=2.0), dev())
    strict = [Rule("mrr", HIGHER, 0.0), Rule("recall@3", HIGHER, 0.0)]
    assert decide(baseline(), candidate, strict)["pass"] is False
    chosen = decide(baseline(), candidate, RULES)
    assert chosen["pass"] is True and chosen["improved"] == []


def test_an_improvement_beyond_the_tolerance_is_named():
    assert decide({"mrr": 0.5, "recall@3": 0.5}, {"mrr": 0.7, "recall@3": 0.55})["improved"] == ["mrr"]


# -- the baseline file ---------------------------------------------------------


def test_a_baseline_needs_a_reason(tmp_path):
    with pytest.raises(ValueError):
        write_baseline(tmp_path / "b.json", {"mrr": 1.0}, "  ")
    write_baseline(tmp_path / "b.json", {"mrr": 1.0}, " first run ")
    assert read_baseline(tmp_path / "b.json") == {"metrics": {"mrr": 1.0}, "reason": "first run"}
    assert read_baseline(tmp_path / "missing.json") is None


def test_no_baseline(tmp_path):
    said = []
    assert run(bm25(), dev(), tmp_path / "b.json", say=said.append) == 2
    assert run(bm25(), dev(), tmp_path / "b.json", accept="first", say=said.append) == 0
    assert read_baseline(tmp_path / "b.json")["metrics"] == baseline()


def test_a_regression_never_writes_the_baseline(tmp_path):
    path = tmp_path / "b.json"
    write_baseline(path, baseline(), "measured")
    said = []
    code = run(lambda t: documents(small_dense().search(t, 60)), dev(), path,
               accept="I like it", say=said.append)
    assert code == 1 and read_baseline(path)["metrics"] == baseline()
    assert any(line.startswith("REGRESSION") for line in said)


def test_accepting_a_pass(tmp_path):
    path = tmp_path / "b.json"
    write_baseline(path, baseline(), "measured")
    assert run(bm25(k1=2.0), dev(), path, accept="k1 2.0, inside noise, kept for recall@1",
               say=lambda line: None) == 0
    assert read_baseline(path)["reason"].startswith("k1 2.0")


# -- the workflow --------------------------------------------------------------


def workflow():
    lines = [l for l in (HERE / "retrieval-gate.yml").read_text().splitlines()
             if l.strip() and not l.strip().startswith("#")]
    assert lines, "retrieval-gate.yml contains only comments so far - write it."
    return "\n".join(lines)


def test_the_workflow_runs_the_gate_on_pull_requests():
    text = workflow()
    assert "pull_request" in text and "run_gate.py" in text and "requirements.txt" in text


def test_the_workflow_never_accepts():
    assert "--accept" not in workflow(), (
        "CI that accepts its own new numbers is a gate that can be talked into anything."
    )
