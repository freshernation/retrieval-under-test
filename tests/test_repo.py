"""Repo guards. Four rules that were each learned by being broken.

These ship green. If one goes red, the repo is misarranged rather than the
student being wrong.
"""

import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
WEEKS = sorted(ROOT.glob("week-*"))


def lab_modules():
    for week in WEEKS:
        for path in week.rglob("*.py"):
            if path.name != "conftest.py" and not path.name.startswith("test_"):
                yield path


def test_test_files_are_uniquely_named():
    """pytest imports test modules by basename, so two `test_day2.py` files in
    different weeks are a collection error rather than two sets of tests."""
    names: dict[str, Path] = {}
    for week in WEEKS:
        for path in week.rglob("test_*.py"):
            if path.name in names:
                pytest.fail(f"{path} collides with {names[path.name]}")
            names[path.name] = path


def test_lab_modules_are_uniquely_named():
    """Same reason, one layer down: which `bm25.py` wins would depend on
    collection order."""
    names: dict[str, Path] = {}
    for path in lab_modules():
        if path.name in names:
            pytest.fail(f"{path} collides with {names[path.name]}")
        names[path.name] = path


def test_no_lab_module_shadows_the_standard_library():
    """Each day's conftest puts its folder at the front of sys.path, so a
    `queue.py` or `tokenize.py` shadows stdlib for the whole session. This is a
    live risk in this course specifically: week 3 wants to call a file
    `tokenize.py` and must not."""
    stdlib = set(sys.stdlib_module_names)
    for path in lab_modules():
        assert path.stem not in stdlib, f"{path} shadows the standard library module {path.stem}"


def test_every_lab_has_a_reference_solution():
    """Checked against the instructor's private repo, which students do not have —
    so this skips for them, by design."""
    solutions = ROOT / "instructor" / "solutions"
    if not solutions.exists():
        pytest.skip("instructor/ is a separate private repository")
    missing = [
        p for p in lab_modules() if not (solutions / p.relative_to(ROOT)).exists()
    ]
    assert not missing, f"no reference solution for: {[str(p) for p in missing]}"


def test_every_week_collects_against_the_stubs():
    """A student must be able to run `pytest week-NN` on day one and see red
    tests — not a collection error.

    Module-level setup that calls a lab function turns every test in the file
    into an ERROR during collection, which aborts the whole week's run and reads
    as "the course is broken" rather than "you have not written this yet".
    Compute that setup lazily instead.
    """
    import subprocess
    import sys

    weeks = [w.name for w in WEEKS if any(w.rglob("test_*.py"))]
    result = subprocess.run(
        [sys.executable, "-m", "pytest", *weeks, "--collect-only", "-q"],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    assert "errors during collection" not in result.stdout, result.stdout[-2000:]
