"""
Tests for swaption pricing engines.

Corresponds to src/pricingengines/swaption/*.cpp bindings.
"""

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


# --- JamshidianSwaptionEngine ---


def test_jamshidianswaptionengine_construction(swaption_env):
    """Test JamshidianSwaptionEngine construction."""
    env = swaption_env

    model = ql.HullWhite(env["curve"], a=0.1, sigma=0.01)
    engine = ql.JamshidianSwaptionEngine(model)
    assert engine is not None


def test_jamshidianswaptionengine_pricing(swaption_env):
    """Test JamshidianSwaptionEngine swaption pricing."""
    env = swaption_env

    model = ql.HullWhite(env["curve"], a=0.1, sigma=0.01)
    engine = ql.JamshidianSwaptionEngine(model)
    env["swaption"].setPricingEngine(engine)

    npv = env["swaption"].NPV()
    assert npv == pytest.approx(15860.419233975226, rel=1e-5)


# --- G2SwaptionEngine ---


def test_g2swaptionengine_construction(swaption_env):
    """Test G2SwaptionEngine construction."""
    env = swaption_env

    model = ql.G2(env["curve"], a=0.1, sigma=0.01, b=0.1, eta=0.01, rho=-0.75)
    engine = ql.G2SwaptionEngine(model, range=6.0, intervals=200)
    assert engine is not None


def test_g2swaptionengine_pricing(swaption_env):
    """Test G2SwaptionEngine swaption pricing."""
    env = swaption_env

    model = ql.G2(env["curve"], a=0.1, sigma=0.01, b=0.1, eta=0.01, rho=-0.75)
    engine = ql.G2SwaptionEngine(model, range=6.0, intervals=200)
    env["swaption"].setPricingEngine(engine)

    npv = env["swaption"].NPV()
    assert npv == pytest.approx(12050.213410784432, rel=1e-5)


# --- FdHullWhiteSwaptionEngine ---


def test_fdhullwhiteswaptionengine_construction(swaption_env):
    """Test FdHullWhiteSwaptionEngine construction."""
    env = swaption_env

    model = ql.HullWhite(env["curve"], a=0.1, sigma=0.01)
    engine = ql.FdHullWhiteSwaptionEngine(model)
    assert engine is not None


def test_fdhullwhiteswaptionengine_with_params(swaption_env):
    """Test FdHullWhiteSwaptionEngine construction with parameters."""
    env = swaption_env

    model = ql.HullWhite(env["curve"], a=0.1, sigma=0.01)
    # NOTE: xGrid must be a multiple of 40 due to suspected QuantLib bug
    # (non-deterministic results with other grid sizes on MSVC Release builds)
    engine = ql.FdHullWhiteSwaptionEngine(
        model, tGrid=50, xGrid=80, dampingSteps=0
    )
    assert engine is not None


def test_fdhullwhiteswaptionengine_pricing(swaption_env):
    """Test FdHullWhiteSwaptionEngine swaption pricing."""
    env = swaption_env

    model = ql.HullWhite(env["curve"], a=0.1, sigma=0.01)
    # NOTE: xGrid must be a multiple of 40 due to suspected QuantLib bug
    # (non-deterministic results with other grid sizes on MSVC Release builds)
    engine = ql.FdHullWhiteSwaptionEngine(model, tGrid=100, xGrid=200)
    env["swaption"].setPricingEngine(engine)

    npv = env["swaption"].NPV()
    assert npv == pytest.approx(15860.169093245760, rel=1e-5)


# --- FdG2SwaptionEngine ---


def test_fdg2swaptionengine_construction(swaption_env):
    """Test FdG2SwaptionEngine construction."""
    env = swaption_env

    model = ql.G2(env["curve"], a=0.1, sigma=0.01, b=0.1, eta=0.01, rho=-0.75)
    engine = ql.FdG2SwaptionEngine(model)
    assert engine is not None


def test_fdg2swaptionengine_with_params(swaption_env):
    """Test FdG2SwaptionEngine construction with parameters."""
    env = swaption_env

    model = ql.G2(env["curve"], a=0.1, sigma=0.01, b=0.1, eta=0.01, rho=-0.75)
    engine = ql.FdG2SwaptionEngine(
        model, tGrid=50, xGrid=25, yGrid=25, dampingSteps=0
    )
    assert engine is not None


def test_fdg2swaptionengine_pricing(swaption_env):
    """Test FdG2SwaptionEngine swaption pricing."""
    env = swaption_env

    model = ql.G2(env["curve"], a=0.1, sigma=0.01, b=0.1, eta=0.01, rho=-0.75)
    engine = ql.FdG2SwaptionEngine(model)
    env["swaption"].setPricingEngine(engine)

    npv = env["swaption"].NPV()
    assert npv == pytest.approx(11913.177527894266, rel=1e-5)
