"""
Tests for cliquet option pricing engines.

Corresponds to src/pricingengines/cliquet/*.cpp bindings.
"""

import pytest

import pyquantlib as ql


@pytest.fixture(scope="module")
def cliquet_env():
    """Setup for cliquet engine tests."""
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
# AnalyticCliquetEngine
# =============================================================================


def test_cliquet_pricing(cliquet_env):
    """Test cliquet option pricing with quarterly resets."""
    env = cliquet_env
    payoff = ql.PercentageStrikePayoff(ql.Call, 1.0)
    exercise = ql.EuropeanExercise(env["expiry"])
    reset_dates = [
        env["today"] + ql.Period("3M"),
        env["today"] + ql.Period("6M"),
        env["today"] + ql.Period("9M"),
    ]

    option = ql.CliquetOption(payoff, exercise, reset_dates)
    engine = ql.AnalyticCliquetEngine(env["process"])
    option.setPricingEngine(engine)

    assert option.NPV() == pytest.approx(13.2894, rel=1e-4)
