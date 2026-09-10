"""Week 9 milestone — the eval harness and its gate."""

from functools import cache

import pytest

import raglab
from answerer import Answerer
from context import ContextAssembler
from dense import DenseRetriever
from fuse import rrf
from gate import HIGHER, LOWER, Gate, Rule, tolerance_from_mde
from harness import EvalSuite, guarded_metrics, regression_check, summary
from lineage import supersession
from raglab.generator import SimulatedGenerator
from sections import section_corpus

CORPUS = raglab.corpus.load()
DOCS = {d.id: d.title + "\n" + d.text for d in CORPUS}


@cache
def dev():
    return list(raglab.judgments.load(file="queries-extended.yml").split("dev"))


@cache
def parts():
    import sys
    from pathlib import Path

    root = Path(__file__).resolve().parents[2]
    for day in ("day-3", "day-2", "day-1"):
        sys.path.insert(0, str(root / "week-03" / day))
    from bm25 import search

    from postings import Index

    chunks = section_corpus(DOCS, 100, 300)
    index = Index(chunks, stopwords=None)
    retriever = DenseRetriever(dims=192).fit(chunks)

    def retrieve(text, depth):
        return rrf([search(index, text, 60), retriever.search(text, 60)], depth, 10)

    assembler = ContextAssembler(retrieve, chunks, budget=800, depth=20)
    return chunks, assembler, supersession({d.id: d.text for d in CORPUS})


@cache
def report(**options):
    chunks, assembler, graph = parts()
    answerer = Answerer(assembler, SimulatedGenerator(**options))
    return EvalSuite(answerer, dev(), chunks, graph).run()


@cache
def honest_gate():
    return Gate(
        [
            Rule("grounded_rate", HIGHER, tolerance_from_mde(report()["power"]["mde"])),
            Rule("faithfulness", HIGHER, 0.05),
            Rule("confidently_wrong", LOWER, 0),
            Rule("unresolvable_citations", LOWER, 0),
        ]
    )


# -- the suite ----------------------------------------------------------------


def test_it_reports_all_four_sections():
    r = report()
    assert set(r) == {"card", "proxies", "power", "judge"}


def test_the_suite_builds_the_contexts_once():
    """A harness that rebuilds retrieval per metric can report a faithfulness
    computed against a context the generator never saw, and the numbers look
    completely normal."""
    chunks, assembler, graph = parts()
    suite = EvalSuite(Answerer(assembler, SimulatedGenerator()), dev(), chunks, graph)
    first = suite.run()
    second = suite.run()
    assert first["card"]["confidently_wrong"] == second["card"]["confidently_wrong"]


def test_the_judge_is_reported_with_its_baseline():
    """A judge's accuracy without the constant-baseline accuracy next to it is a
    number that cannot be interpreted — and this week found one that matched it
    exactly."""
    j = report()["judge"]
    assert set(j) >= {"accuracy", "kappa", "baseline_accuracy", "baseline_kappa"}
    assert j["accuracy"] == pytest.approx(j["baseline_accuracy"])
    assert j["kappa"] == pytest.approx(j["baseline_kappa"], abs=0.001)


def test_the_power_section_says_what_cannot_be_seen():
    p = report()["power"]
    assert p["n"] == 20
    assert p["mde"] > 0.15


def test_the_proxy_section_names_what_is_offline_only():
    assert report()["proxies"]["offline_only"] == [
        "answer_recall",
        "confidently_wrong",
        "correctness",
        "grounded_rate",
    ]
    assert report()["proxies"]["useful"] == ["distinct_documents", "retrieval_confidence"]


# -- the gate -----------------------------------------------------------------


def test_guarded_metrics_are_few():
    """Ten guarded metrics fire spuriously two times in five. Guard only what you
    would roll back for."""
    metrics = guarded_metrics(report())
    assert len(metrics) <= 5
    assert set(metrics) == {
        "grounded_rate",
        "faithfulness",
        "confidently_wrong",
        "unresolvable_citations",
    }


def test_a_system_passes_against_itself():
    assert regression_check(report(), report(), honest_gate())["pass"] is True


def test_it_blocks_a_misattributing_system():
    result = regression_check(report(), report(misattribute=True), honest_gate())
    assert result["pass"] is False
    assert any("faithfulness" in f["failure"] for f in result["failures"])


def test_every_failure_says_whether_it_is_detectable():
    """**The field that makes a gate honest.** A failure smaller than the minimum
    detectable effect is a coin flip reported as a regression, and a gate that
    cannot say which of its failures are real will be muted."""
    result = regression_check(report(), report(misattribute=True), honest_gate())
    for failure in result["failures"]:
        assert set(failure) == {"failure", "moved", "detectable"}
    assert all(f["detectable"] for f in result["failures"])


def test_grounded_rate_does_not_move_and_the_gate_still_fires():
    """Retrieval is unchanged, so the retrieval metric is unchanged. The gate
    catches it because it guards faithfulness too — which is week 8's pairing,
    enforced by a machine."""
    base = guarded_metrics(report())
    broken = guarded_metrics(report(misattribute=True))
    assert base["grounded_rate"] == broken["grounded_rate"]
    assert base["faithfulness"] > broken["faithfulness"] + 0.5


# -- the summary --------------------------------------------------------------


def test_the_summary_leads_with_blockers():
    """A summary that opens with a metric is a summary nobody finishes."""
    lines = summary(report())
    assert lines[0].startswith("BLOCKER")
    assert "confident answers with no answer in context" in lines[0]


def test_then_what_cannot_be_measured():
    lines = summary(report())
    unmeasured = [i for i, line in enumerate(lines) if line.startswith("UNMEASURED")]
    blockers = [i for i, line in enumerate(lines) if line.startswith("BLOCKER")]
    numbers = [i for i, line in enumerate(lines) if line.startswith("faithfulness")]
    assert max(blockers) < min(unmeasured) < max(unmeasured) < min(numbers)


def test_it_says_the_judge_learned_nothing():
    assert any("does no better than always answering yes" in line for line in summary(report()))


def test_and_the_last_line_is_the_numbers():
    """Nine weeks of measurement, and the metrics come last — because by now you
    know what each of them is blind to."""
    lines = summary(report())
    assert lines[-1].startswith("faithfulness")
    assert "grounded" in lines[-1]
