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
