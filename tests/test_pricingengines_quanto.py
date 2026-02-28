"""
Tests for quanto option pricing engines.

Corresponds to src/pricingengines/quanto/*.cpp bindings.
"""

import pytest

import pyquantlib as ql


@pytest.fixture(scope="module")
def quanto_env():
    """Setup for quanto engine tests."""
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

    foreign_rate = ql.FlatForward(today, 0.04, ql.Actual365Fixed())
    fx_vol = ql.BlackConstantVol(today, ql.TARGET(), 0.15, ql.Actual365Fixed())
    correlation = ql.SimpleQuote(0.3)

    expiry = today + ql.Period("1Y")

    return {
        "today": today,
        "process": process,
        "foreign_rate": foreign_rate,
        "fx_vol": fx_vol,
        "correlation": correlation,
        "expiry": expiry,
    }


# =============================================================================
# QuantoVanillaEngine
# =============================================================================


def test_quanto_pricing(quanto_env):
    """Test quanto vanilla option pricing."""
    env = quanto_env
    payoff = ql.PlainVanillaPayoff(ql.Call, 100.0)
    exercise = ql.EuropeanExercise(env["expiry"])

    option = ql.QuantoVanillaOption(payoff, exercise)
    engine = ql.QuantoVanillaEngine(
        env["process"],
        ql.YieldTermStructureHandle(env["foreign_rate"]),
        ql.BlackVolTermStructureHandle(env["fx_vol"]),
        ql.QuoteHandle(env["correlation"]),
    )
    option.setPricingEngine(engine)

    assert option.NPV() == pytest.approx(8.0754, rel=1e-4)


def test_quanto_greeks(quanto_env):
    """Test quanto-specific greeks (qvega, qrho, qlambda)."""
    env = quanto_env
    payoff = ql.PlainVanillaPayoff(ql.Call, 100.0)
    exercise = ql.EuropeanExercise(env["expiry"])

    option = ql.QuantoVanillaOption(payoff, exercise)
    engine = ql.QuantoVanillaEngine(
        env["process"],
        ql.YieldTermStructureHandle(env["foreign_rate"]),
        ql.BlackVolTermStructureHandle(env["fx_vol"]),
        ql.QuoteHandle(env["correlation"]),
    )
    option.setPricingEngine(engine)

    assert option.qvega() == pytest.approx(-3.2084, rel=1e-4)
    assert option.qrho() == pytest.approx(53.4735, rel=1e-4)
    assert option.qlambda() == pytest.approx(-1.6042, rel=1e-4)


def test_quanto_hidden_handle(quanto_env):
    """Test quanto engine construction with hidden handles."""
    env = quanto_env
    payoff = ql.PlainVanillaPayoff(ql.Call, 100.0)
    exercise = ql.EuropeanExercise(env["expiry"])

    option = ql.QuantoVanillaOption(payoff, exercise)
    engine = ql.QuantoVanillaEngine(
        env["process"],
        env["foreign_rate"],
        env["fx_vol"],
        env["correlation"],
    )
    option.setPricingEngine(engine)

    assert option.NPV() == pytest.approx(8.0754, rel=1e-4)


# =============================================================================
# QuantoForwardVanillaEngine
# =============================================================================


def test_quanto_forward_pricing(quanto_env):
    """Test quanto forward vanilla option pricing."""
    env = quanto_env
    payoff = ql.PlainVanillaPayoff(ql.Call, 100.0)
    exercise = ql.EuropeanExercise(env["expiry"])
    reset_date = env["today"] + ql.Period("3M")

    option = ql.QuantoForwardVanillaOption(1.0, reset_date, payoff, exercise)
    engine = ql.QuantoForwardVanillaEngine(
        env["process"],
        ql.YieldTermStructureHandle(env["foreign_rate"]),
        ql.BlackVolTermStructureHandle(env["fx_vol"]),
        ql.QuoteHandle(env["correlation"]),
    )
    option.setPricingEngine(engine)

    assert option.NPV() == pytest.approx(6.9594, rel=1e-4)


def test_quanto_forward_greeks(quanto_env):
    """Test quanto forward option greeks (qvega, qrho, qlambda)."""
    env = quanto_env
    payoff = ql.PlainVanillaPayoff(ql.Call, 100.0)
    exercise = ql.EuropeanExercise(env["expiry"])
    reset_date = env["today"] + ql.Period("3M")

    option = ql.QuantoForwardVanillaOption(1.0, reset_date, payoff, exercise)
    engine = ql.QuantoForwardVanillaEngine(
        env["process"],
        ql.YieldTermStructureHandle(env["foreign_rate"]),
        ql.BlackVolTermStructureHandle(env["fx_vol"]),
        ql.QuoteHandle(env["correlation"]),
    )
    option.setPricingEngine(engine)

    assert option.qvega() == pytest.approx(-2.4855, rel=1e-3)
    assert option.qrho() == pytest.approx(41.4248, rel=1e-3)
    assert option.qlambda() == pytest.approx(-1.2427, rel=1e-3)


def test_quanto_forward_hidden_handle(quanto_env):
    """Test quanto forward engine with hidden handles."""
    env = quanto_env
    payoff = ql.PlainVanillaPayoff(ql.Call, 100.0)
    exercise = ql.EuropeanExercise(env["expiry"])
    reset_date = env["today"] + ql.Period("3M")

    option = ql.QuantoForwardVanillaOption(1.0, reset_date, payoff, exercise)
    engine = ql.QuantoForwardVanillaEngine(
        env["process"],
        env["foreign_rate"],
        env["fx_vol"],
        env["correlation"],
    )
    option.setPricingEngine(engine)

    assert option.NPV() == pytest.approx(6.9594, rel=1e-4)
