"""
Tests for forward-start option pricing engines.

Corresponds to src/pricingengines/forward/*.cpp bindings.
"""

import pytest

import pyquantlib as ql


@pytest.fixture(scope="module")
def forward_env():
    """Setup for forward engine tests."""
    today = ql.Date(15, ql.January, 2025)
    ql.Settings.evaluationDate = today

    spot = ql.SimpleQuote(100.0)
    rate = ql.FlatForward(today, 0.06, ql.Actual365Fixed())
    div = ql.FlatForward(today, 0.02, ql.Actual365Fixed())
    vol = ql.BlackConstantVol(today, ql.TARGET(), 0.20, ql.Actual365Fixed())

    process = ql.BlackScholesMertonProcess(
        ql.QuoteHandle(spot),
        ql.YieldTermStructureHandle(div),
        ql.YieldTermStructureHandle(rate),
        ql.BlackVolTermStructureHandle(vol),
    )

    expiry = today + ql.Period("1Y")

    return {
        "today": today,
        "process": process,
        "expiry": expiry,
    }


# =============================================================================
# ForwardEuropeanEngine
# =============================================================================


def test_forward_vanilla_pricing(forward_env):
    """Test forward-start vanilla option pricing."""
    env = forward_env
    payoff = ql.PlainVanillaPayoff(ql.Call, 100.0)
    exercise = ql.EuropeanExercise(env["expiry"])
    reset_date = env["today"] + ql.Period("3M")

    option = ql.ForwardVanillaOption(1.0, reset_date, payoff, exercise)
    engine = ql.ForwardEuropeanEngine(env["process"])
    option.setPricingEngine(engine)

    assert option.NPV() == pytest.approx(8.2345, rel=1e-4)


# =============================================================================
# ForwardPerformanceEuropeanEngine
# =============================================================================


def test_forward_performance_pricing(forward_env):
    """Test forward-start performance option pricing."""
    env = forward_env
    payoff = ql.PlainVanillaPayoff(ql.Call, 100.0)
    exercise = ql.EuropeanExercise(env["expiry"])
    reset_date = env["today"] + ql.Period("3M")

    option = ql.ForwardVanillaOption(1.0, reset_date, payoff, exercise)
    engine = ql.ForwardPerformanceEuropeanEngine(env["process"])
    option.setPricingEngine(engine)

    assert option.NPV() == pytest.approx(0.0815364, rel=1e-4)


# =============================================================================
# MCForwardEuropeanBSEngine
# =============================================================================


def test_mc_forward_bs_construction(forward_env):
    """Test MCForwardEuropeanBSEngine construction."""
    engine = ql.MCForwardEuropeanBSEngine(
        forward_env["process"], rngType="pseudorandom",
        timeSteps=10, requiredSamples=100, seed=42,
    )
    assert engine is not None


def test_mc_forward_bs_pricing(forward_env):
    """Test MC forward-start BS engine pricing."""
    env = forward_env
    payoff = ql.PlainVanillaPayoff(ql.Call, 100.0)
    exercise = ql.EuropeanExercise(env["expiry"])
    reset_date = env["today"] + ql.Period("3M")

    option = ql.ForwardVanillaOption(1.0, reset_date, payoff, exercise)
    engine = ql.MCForwardEuropeanBSEngine(
        env["process"], rngType="pseudorandom",
        timeSteps=10, requiredSamples=50000, seed=42,
    )
    option.setPricingEngine(engine)

    assert option.NPV() == pytest.approx(8.2646, rel=1e-2)


def test_mc_forward_bs_lowdiscrepancy(forward_env):
    """Test MC forward BS engine with low-discrepancy RNG."""
    env = forward_env
    payoff = ql.PlainVanillaPayoff(ql.Call, 100.0)
    exercise = ql.EuropeanExercise(env["expiry"])
    reset_date = env["today"] + ql.Period("3M")

    option = ql.ForwardVanillaOption(1.0, reset_date, payoff, exercise)
    engine = ql.MCForwardEuropeanBSEngine(
        env["process"], rngType="lowdiscrepancy",
        timeSteps=10, requiredSamples=50000,
    )
    option.setPricingEngine(engine)

    # Low-discrepancy should converge close to analytic value (~8.2345)
    assert option.NPV() == pytest.approx(8.2345, rel=5e-2)


# =============================================================================
# MCForwardEuropeanHestonEngine
# =============================================================================


def test_mc_forward_heston_construction(forward_env):
    """Test MCForwardEuropeanHestonEngine construction."""
    env = forward_env
    spot = ql.SimpleQuote(100.0)
    rts = ql.FlatForward(env["today"], 0.06, ql.Actual365Fixed())
    dts = ql.FlatForward(env["today"], 0.02, ql.Actual365Fixed())

    process = ql.HestonProcess(rts, dts, spot, 0.04, 1.5, 0.04, 0.3, -0.7)

    engine = ql.MCForwardEuropeanHestonEngine(
        process, rngType="pseudorandom",
        timeSteps=10, requiredSamples=100, seed=42,
    )
    assert engine is not None


def test_mc_forward_heston_pricing(forward_env):
    """Test MC forward-start Heston engine pricing."""
    env = forward_env
    spot = ql.SimpleQuote(100.0)
    rts = ql.FlatForward(env["today"], 0.06, ql.Actual365Fixed())
    dts = ql.FlatForward(env["today"], 0.02, ql.Actual365Fixed())

    process = ql.HestonProcess(rts, dts, spot, 0.04, 1.5, 0.04, 0.3, -0.7)

    payoff = ql.PlainVanillaPayoff(ql.Call, 100.0)
    exercise = ql.EuropeanExercise(env["expiry"])
    reset_date = env["today"] + ql.Period("3M")

    option = ql.ForwardVanillaOption(1.0, reset_date, payoff, exercise)
    engine = ql.MCForwardEuropeanHestonEngine(
        process, rngType="pseudorandom",
        timeSteps=10, requiredSamples=50000, seed=42,
    )
    option.setPricingEngine(engine)

    assert option.NPV() == pytest.approx(7.9116, rel=1e-2)
