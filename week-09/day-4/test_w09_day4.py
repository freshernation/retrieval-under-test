"""Day 4 — the gate.

`test_a_tolerance_below_the_mde_is_a_coin_flip` is the day.
"""

import pytest

from gate import (
    HIGHER,
    LOWER,
    Gate,
    Rule,
    compound_alarm_rate,
    false_alarm_rate,
    tolerance_from_mde,
)
from power import mde

SD = 0.2229


def noisy_runs(n: int, spread: float, seed: int = 0) -> list[dict[str, float]]:
    """Repeated measurements of an unchanged system."""
    import random

    rng = random.Random(seed)
    return [{"recall": 0.75 + spread * (rng.random() - 0.5)} for _ in range(n)]


# -- rules --------------------------------------------------------------------


def test_direction_is_per_metric():
    """`confidently_wrong` is a metric you want to fall. A gate assuming
    higher-is-better everywhere waves through a system that doubled its wrong
    answers."""
    up = Rule("recall", HIGHER)
    down = Rule("confidently_wrong", LOWER)
    assert up.violated(0.80, 0.70) is True
    assert up.violated(0.70, 0.80) is False
    assert down.violated(3, 6) is True
    assert down.violated(6, 3) is False


def test_tolerance_allows_drift():
    rule = Rule("recall", HIGHER, tolerance=0.05)
    assert rule.violated(0.80, 0.77) is False
    assert rule.violated(0.80, 0.70) is True


# -- the gate -----------------------------------------------------------------


def test_it_reports_what_it_checked():
    """A gate that silently skips a missing metric **passes**, and the most
    common cause of a gate passing is that it stopped running."""
    gate = Gate([Rule("recall"), Rule("missing_metric")])
    result = gate.check({"recall": 0.8}, {"recall": 0.8})
    assert result["pass"] is True
    assert result["checked"] == 1


def test_a_failure_is_readable_at_seven_in_the_morning():
    gate = Gate([Rule("recall", HIGHER, tolerance=0.01)])
    result = gate.check({"recall": 0.80}, {"recall": 0.60})
    assert result["pass"] is False
    assert len(result["failures"]) == 1
    message = result["failures"][0]
    assert "recall" in message and "0.8" in message and "0.6" in message


def test_it_blocks_a_real_regression():
    gate = Gate([Rule("recall", HIGHER, tolerance=0.02), Rule("confidently_wrong", LOWER)])
    good = {"recall": 0.80, "confidently_wrong": 3}
    bad = {"recall": 0.60, "confidently_wrong": 9}
    assert gate.check(good, good)["pass"] is True
    assert gate.check(good, bad)["pass"] is False
    assert len(gate.check(good, bad)["failures"]) == 2


# -- the two failure modes ----------------------------------------------------


def test_a_gate_that_never_fires_protects_nothing():
    gate = Gate([Rule("recall", HIGHER, tolerance=1.0)])
    assert gate.check({"recall": 0.9}, {"recall": 0.1})["pass"] is True


def test_a_tolerance_below_the_mde_is_a_coin_flip():
    """**The day.**

    An unchanged system, remeasured, wanders by roughly the sampling noise. Set
    the tolerance at 0.02 when the minimum detectable effect is 0.10 and the gate
    fires on **more than a third** of consecutive runs of a system nobody
    touched. Set it at the MDE and it fires on one run in twenty.

    A gate with a high false-alarm rate is muted within a fortnight — and then it
    protects nothing while everybody believes it is there, which is worse than
    not having one."""
    runs = noisy_runs(40, spread=0.14, seed=1)
    tight = Gate([Rule("recall", HIGHER, tolerance=0.02)])
    honest = Gate([Rule("recall", HIGHER, tolerance=tolerance_from_mde(mde(19, SD)))])

    tight_rate = false_alarm_rate(tight, runs)
    honest_rate = false_alarm_rate(honest, runs)
    assert tight_rate > 0.3
    assert honest_rate < 0.1
    assert honest_rate < tight_rate / 5


def test_the_tolerance_comes_from_the_mde():
    """If your eval set cannot distinguish a 10-point change from zero, a gate at
    2 points is measuring sampling noise. The answer is more queries, not a
    tighter gate."""
    assert tolerance_from_mde(mde(19, SD)) == pytest.approx(0.100, abs=0.005)
    assert tolerance_from_mde(mde(500, SD)) == pytest.approx(0.020, abs=0.003)
    assert tolerance_from_mde(mde(19, SD)) > tolerance_from_mde(mde(100, SD))


def test_an_unchanged_system_passes_an_honest_gate():
    runs = noisy_runs(40, spread=0.10, seed=7)
    honest = Gate([Rule("recall", HIGHER, tolerance=tolerance_from_mde(mde(19, SD)))])
    assert false_alarm_rate(honest, runs) == 0.0


# -- and why not to gate on everything ----------------------------------------


def test_gating_on_ten_metrics_fires_on_nothing_two_times_in_five():
    """Ten metrics each firing spuriously 5% of the time gives a **40%** chance
    that at least one fires on an unchanged system.

    Guard the few metrics whose regression you would actually roll back for.
    Report the rest."""
    assert compound_alarm_rate(0.05, 1) == pytest.approx(0.05)
    assert compound_alarm_rate(0.05, 10) == pytest.approx(0.4013, abs=0.001)
    assert compound_alarm_rate(0.05, 20) > 0.6


def test_a_perfect_metric_never_compounds():
    assert compound_alarm_rate(0.0, 100) == 0.0
    with pytest.raises(ValueError):
        compound_alarm_rate(1.5, 3)
