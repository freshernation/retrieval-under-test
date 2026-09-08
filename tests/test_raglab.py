"""The harness's own tests. These ship green — you use raglab, you do not build it."""

from pathlib import Path

import numpy as np
import pytest

import raglab
from raglab.judgments import Query, QuerySet
from raglab.metrics import bootstrap, evaluate, mrr, ndcg_at_k, precision_at_k, recall_at_k


def q(relevant=("a", "b"), grades=None, split="dev"):
    judgments = grades if grades is not None else {d: 2 for d in relevant}
    return Query(id="q", text="t", split=split, judgments=judgments)


# -- corpus -------------------------------------------------------------------


def test_the_sample_corpus_loads():
    c = raglab.corpus.load()
    assert len(c) == 30
    assert "mrta-001" in c
    assert c["mrta-030"].title.startswith("Glossary")


def test_documents_keep_their_provenance():
    for doc in raglab.corpus.load():
        assert doc.source and doc.source != "unknown"
        assert doc.retrieved


def test_duplicate_ids_are_rejected():
    from raglab.corpus import Corpus, Document

    d = Document(id="x", title="", text="", source="s", retrieved="r")
    with pytest.raises(ValueError, match="duplicate"):
        Corpus([d, d])


# -- judgments ----------------------------------------------------------------


def test_the_sample_judgments_are_sound():
    c, qs = raglab.corpus.load(), raglab.judgments.load()
    assert raglab.judgments.check_against(qs, c) == []


def test_splits_are_eight_and_four():
    qs = raglab.judgments.load()
    assert len(qs.split("dev")) == 8
    assert len(qs.split("test")) == 4


def test_an_all_relevant_query_is_flagged():
    """The mistake that ruins eval sets: labelling only what you already believed
    was relevant, so the query cannot punish a bad result."""
    c = raglab.corpus.load()
    qs = QuerySet([Query(id="bad", text="t", split="dev", judgments={"mrta-001": 3})])
    problems = raglab.judgments.check_against(qs, c)
    assert any("every judged document is relevant" in p for p in problems)


def test_unjudged_documents_score_zero():
    assert q().grade("never-labelled") == 0


# -- metrics ------------------------------------------------------------------


def test_recall_counts_relevant_found():
    assert recall_at_k(["a", "z", "b"], q(), k=10) == 1.0
    assert recall_at_k(["a", "z", "y"], q(), k=10) == 0.5
    assert recall_at_k(["z", "y", "a"], q(), k=2) == 0.0


def test_precision_is_capped_by_the_judgments():
    """Two relevant documents and k=10 means precision cannot exceed 0.2. This is
    not a bug in the retriever and week 1 makes you notice it."""
    assert precision_at_k(["a", "b"] + list("cdefghij"), q(), k=10) == pytest.approx(0.2)


def test_mrr_is_the_first_hit_only():
    assert mrr(["z", "a", "b"], q()) == pytest.approx(0.5)
    assert mrr(["z", "y"], q()) == 0.0


def test_ndcg_is_one_for_the_ideal_order():
    graded = q(grades={"a": 3, "b": 2, "c": 1})
    assert ndcg_at_k(["a", "b", "c"], graded, k=10) == pytest.approx(1.0)


def test_ndcg_punishes_the_wrong_order():
    graded = q(grades={"a": 3, "b": 2, "c": 1})
    good = ndcg_at_k(["a", "b", "c"], graded, k=10)
    bad = ndcg_at_k(["c", "b", "a"], graded, k=10)
    assert bad < good


def test_recall_high_and_ndcg_low_is_a_ranking_failure():
    """The pair that does most of the diagnostic work: everything was found, and
    it was found in the wrong order. Station 5, not station 4."""
    graded = q(grades={"a": 3, "b": 3, "z": 0, "y": 0, "x": 0})
    ranked = ["z", "y", "x", "a", "b"]
    assert recall_at_k(ranked, graded, k=10) == 1.0
    assert ndcg_at_k(ranked, graded, k=10) < 0.6


# -- evaluate and bootstrap ---------------------------------------------------


def full_eval(offset=0):
    qs = raglab.judgments.load().split("dev")
    rankings = {}
    for i, query in enumerate(qs):
        rel = sorted(query.relevant)
        pad = [d for d in raglab.corpus.load().ids if d not in rel][: 10 - len(rel)]
        rankings[query.id] = (pad[:offset] + rel + pad[offset:])[:10]
    return evaluate(rankings, qs)


def test_evaluate_returns_a_mean_and_every_query():
    ev = full_eval()
    assert ev.n == 8
    assert set(ev.per_query) == {f"q0{i}" for i in range(1, 9)}
    assert ev.metrics["recall@10"] == pytest.approx(1.0)


def test_evaluate_refuses_a_mixed_split():
    with pytest.raises(ValueError, match="one split at a time"):
        evaluate({}, raglab.judgments.load())


def test_a_missing_ranking_scores_zero_rather_than_being_skipped():
    qs = raglab.judgments.load().split("dev")
    ev = evaluate({}, qs)
    assert ev.n == 8
    assert ev.metrics["recall@10"] == 0.0


def test_bootstrap_is_seeded_and_reproducible():
    a, b = full_eval(offset=0), full_eval(offset=3)
    assert bootstrap(a, b) == bootstrap(a, b)


def test_bootstrap_of_a_system_against_itself_straddles_zero():
    a = full_eval()
    delta, low, high = bootstrap(a, a)
    assert delta == 0.0 and low <= 0 <= high


def test_worse_than_names_the_queries():
    a, b = full_eval(offset=0), full_eval(offset=3)
    assert a.worse_than(b, "ndcg@10") == []
    assert b.worse_than(a, "ndcg@10")


# -- runs ---------------------------------------------------------------------


def test_a_run_is_written_and_reloads(tmp_path: Path):
    ev = full_eval()
    run = raglab.runs.record(ev, {"retriever": "stub"}, note="hello", runs_dir=tmp_path)
    again = raglab.runs.load(run.id, runs_dir=tmp_path)
    assert again.metrics["recall@10"] == run.metrics["recall@10"]
    assert again.note == "hello"


def test_the_config_hash_moves_only_when_the_config_does():
    h = raglab.runs.config_hash
    assert h({"a": 1, "b": 2}) == h({"b": 2, "a": 1})
    assert h({"a": 1}) != h({"a": 2})


def test_reading_the_test_split_is_logged(tmp_path: Path):
    qs = raglab.judgments.load().split("test")
    ev = evaluate({q.id: sorted(q.relevant) for q in qs}, qs)
    assert not raglab.runs.test_reads(runs_dir=tmp_path)
    raglab.runs.record(ev, {"retriever": "stub"}, note="confirm", runs_dir=tmp_path)
    reads = raglab.runs.test_reads(runs_dir=tmp_path)
    assert len(reads) == 1 and reads[0][3] == "confirm"


def test_reading_dev_is_not_logged(tmp_path: Path):
    raglab.runs.record(full_eval(), {"r": "stub"}, runs_dir=tmp_path)
    assert raglab.runs.test_reads(runs_dir=tmp_path) == []


# -- text ---------------------------------------------------------------------


def test_token_count_is_deterministic_and_rough():
    assert raglab.text.approx_tokens("") == 0
    assert raglab.text.approx_tokens("a" * 400) == 100
    assert raglab.text.truncate_to_tokens("one two three four five", 2).split() == ["one", "two"]


# -- vectors and cassettes ----------------------------------------------------


def test_missing_vectors_say_what_to_do():
    with pytest.raises(FileNotFoundError, match="tools/build_vectors.py"):
        raglab.vectors.load("sample")


def test_a_vector_manifest_out_of_step_is_refused(tmp_path: Path):
    base = tmp_path / "s" / "vectors"
    base.mkdir(parents=True)
    np.save(base / "documents.npy", np.zeros((3, 4)))
    (base / "documents.json").write_text('{"ids": ["a", "b"], "model": "m"}')
    with pytest.raises(ValueError, match="out of step"):
        raglab.vectors.load("s", root=tmp_path)


def test_a_cassette_replays_and_refuses_an_unseen_prompt(tmp_path: Path):
    import json

    from raglab.cassette import fingerprint, load

    prompt = "Answer only from the context."
    (tmp_path / "t.json").write_text(
        json.dumps({"model": "m", "entries": {fingerprint(prompt): {"completion": "ok"}}})
    )
    tape = load("t", root=tmp_path)
    assert tape.complete(prompt) == "ok"
    assert tape.complete("  Answer only    from the context. ") == "ok"
    with pytest.raises(KeyError, match="no recording"):
        tape.complete("something else")
