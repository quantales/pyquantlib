"""Tests for ql/pricingengines/swaption/*.hpp bindings."""

import pytest

import pyquantlib as ql


@pytest.fixture
def swaption_env():
    """Environment for swaption pricing tests."""
    today = ql.Date(15, ql.January, 2026)
    ql.Settings.instance().evaluationDate = today

    # Term structure
    dc = ql.Actual365Fixed()
    curve = ql.FlatForward(today, 0.05, dc)

    # Index
    index = ql.Euribor6M(curve)

    # Create a vanilla swap
    fixed_schedule = ql.Schedule(
        today + ql.Period(1, ql.Years),
        today + ql.Period(6, ql.Years),
        ql.Period(1, ql.Years),
        ql.TARGET(),
        ql.ModifiedFollowing,
        ql.ModifiedFollowing,
        ql.DateGeneration.Forward,
        False,
    )
    float_schedule = ql.Schedule(
        today + ql.Period(1, ql.Years),
        today + ql.Period(6, ql.Years),
        ql.Period(6, ql.Months),
        ql.TARGET(),
        ql.ModifiedFollowing,
        ql.ModifiedFollowing,
        ql.DateGeneration.Forward,
        False,
    )
    swap = ql.VanillaSwap(
        ql.SwapType.Payer,
        1000000.0,
        fixed_schedule,
        0.05,
        ql.Thirty360(ql.Thirty360.BondBasis),
        float_schedule,
        index,
        0.0,
        ql.Actual360(),
    )

    # Create a European swaption
    exercise = ql.EuropeanExercise(today + ql.Period(1, ql.Years))
    swaption = ql.Swaption(swap, exercise)

    return {
        "today": today,
        "curve": curve,
        "index": index,
        "swap": swap,
        "swaption": swaption,
    }


# --- TreeSwaptionEngine ---


def test_treeswaptionengine_construction_timesteps(swaption_env):
    """Test TreeSwaptionEngine construction with time steps."""
    env = swaption_env

    model = ql.HullWhite(env["curve"], a=0.1, sigma=0.01)
    engine = ql.TreeSwaptionEngine(model, timeSteps=50)
    assert engine is not None


def test_treeswaptionengine_construction_timegrid(swaption_env):
    """Test TreeSwaptionEngine construction with time grid."""
    env = swaption_env

    model = ql.HullWhite(env["curve"], a=0.1, sigma=0.01)
    times = [0.0, 0.5, 1.0, 2.0, 3.0, 4.0, 5.0]
    time_grid = ql.TimeGrid(times)
    engine = ql.TreeSwaptionEngine(model, timeGrid=time_grid)
    assert engine is not None


def test_treeswaptionengine_pricing(swaption_env):
    """Test TreeSwaptionEngine swaption pricing."""
    env = swaption_env

    model = ql.HullWhite(env["curve"], a=0.1, sigma=0.01)
    engine = ql.TreeSwaptionEngine(model, timeSteps=100)
    env["swaption"].setPricingEngine(engine)

    npv = env["swaption"].NPV()
    assert npv == pytest.approx(15996.569867907741, rel=1e-5)
