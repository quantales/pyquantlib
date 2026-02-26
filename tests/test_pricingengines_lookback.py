"""
Tests for lookback option pricing engines.

Corresponds to src/pricingengines/lookback/*.cpp bindings.
"""

import pytest

import pyquantlib as ql


@pytest.fixture(scope="module")
def lookback_env():
    """Setup for lookback engine tests."""
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
# AnalyticContinuousFloatingLookbackEngine
# =============================================================================


def test_floating_lookback_call_pricing(lookback_env):
    """Test floating lookback call pricing."""
    env = lookback_env
    payoff = ql.FloatingTypePayoff(ql.Call)
    exercise = ql.EuropeanExercise(env["expiry"])
    option = ql.ContinuousFloatingLookbackOption(100.0, payoff, exercise)

    engine = ql.AnalyticContinuousFloatingLookbackEngine(env["process"])
    option.setPricingEngine(engine)

    assert option.NPV() == pytest.approx(16.4219, rel=1e-4)


def test_floating_lookback_put_pricing(lookback_env):
    """Test floating lookback put pricing."""
    env = lookback_env
    payoff = ql.FloatingTypePayoff(ql.Put)
    exercise = ql.EuropeanExercise(env["expiry"])
    option = ql.ContinuousFloatingLookbackOption(100.0, payoff, exercise)

    engine = ql.AnalyticContinuousFloatingLookbackEngine(env["process"])
    option.setPricingEngine(engine)

    assert option.NPV() == pytest.approx(14.5002, rel=1e-4)


# =============================================================================
# AnalyticContinuousFixedLookbackEngine
# =============================================================================


def test_fixed_lookback_call_pricing(lookback_env):
    """Test fixed lookback call pricing."""
    env = lookback_env
    payoff = ql.PlainVanillaPayoff(ql.Call, 100.0)
    exercise = ql.EuropeanExercise(env["expiry"])
    option = ql.ContinuousFixedLookbackOption(100.0, payoff, exercise)

    engine = ql.AnalyticContinuousFixedLookbackEngine(env["process"])
    option.setPricingEngine(engine)

    assert option.NPV() == pytest.approx(18.3436, rel=1e-4)


def test_fixed_lookback_put_pricing(lookback_env):
    """Test fixed lookback put pricing."""
    env = lookback_env
    payoff = ql.PlainVanillaPayoff(ql.Put, 100.0)
    exercise = ql.EuropeanExercise(env["expiry"])
    option = ql.ContinuousFixedLookbackOption(100.0, payoff, exercise)

    engine = ql.AnalyticContinuousFixedLookbackEngine(env["process"])
    option.setPricingEngine(engine)

    assert option.NPV() == pytest.approx(12.5785, rel=1e-4)


# =============================================================================
# AnalyticContinuousPartialFloatingLookbackEngine
# =============================================================================


def test_partial_floating_lookback_pricing(lookback_env):
    """Test partial floating lookback pricing."""
    env = lookback_env
    payoff = ql.FloatingTypePayoff(ql.Call)
    exercise = ql.EuropeanExercise(env["expiry"])
    lookback_end = env["today"] + ql.Period("6M")
    option = ql.ContinuousPartialFloatingLookbackOption(
        100.0, 1.0, lookback_end, payoff, exercise
    )

    engine = ql.AnalyticContinuousPartialFloatingLookbackEngine(env["process"])
    option.setPricingEngine(engine)

    assert option.NPV() == pytest.approx(14.7273, rel=1e-4)


# =============================================================================
# AnalyticContinuousPartialFixedLookbackEngine
# =============================================================================


def test_partial_fixed_lookback_pricing(lookback_env):
    """Test partial fixed lookback pricing."""
    env = lookback_env
    payoff = ql.PlainVanillaPayoff(ql.Call, 100.0)
    exercise = ql.EuropeanExercise(env["expiry"])
    lookback_start = env["today"] + ql.Period("6M")
    option = ql.ContinuousPartialFixedLookbackOption(
        lookback_start, payoff, exercise
    )

    engine = ql.AnalyticContinuousPartialFixedLookbackEngine(env["process"])
    option.setPricingEngine(engine)

    assert option.NPV() == pytest.approx(16.1399, rel=1e-4)
