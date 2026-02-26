"""
Tests for exotic option pricing engines.

Corresponds to src/pricingengines/exotic/*.cpp bindings.
"""

import pytest

import pyquantlib as ql


@pytest.fixture(scope="module")
def exotic_env():
    """Setup for exotic engine tests."""
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
    exercise = ql.EuropeanExercise(expiry)

    return {
        "today": today,
        "rate": rate,
        "div": div,
        "process": process,
        "expiry": expiry,
        "exercise": exercise,
    }


# =============================================================================
# AnalyticCompoundOptionEngine
# =============================================================================


def test_compoundoption_pricing(exotic_env):
    """Test compound option pricing."""
    env = exotic_env
    mother_payoff = ql.PlainVanillaPayoff(ql.Call, 5.0)
    mother_exercise = ql.EuropeanExercise(env["today"] + ql.Period("6M"))
    daughter_payoff = ql.PlainVanillaPayoff(ql.Call, 100.0)
    daughter_exercise = ql.EuropeanExercise(env["expiry"])

    option = ql.CompoundOption(
        mother_payoff, mother_exercise, daughter_payoff, daughter_exercise
    )

    engine = ql.AnalyticCompoundOptionEngine(env["process"])
    option.setPricingEngine(engine)

    assert option.NPV() == pytest.approx(5.9289, rel=1e-4)


# =============================================================================
# AnalyticSimpleChooserEngine
# =============================================================================


def test_simplechooser_pricing(exotic_env):
    """Test simple chooser option pricing."""
    env = exotic_env
    choosing_date = env["today"] + ql.Period("6M")
    option = ql.SimpleChooserOption(choosing_date, 100.0, env["exercise"])

    engine = ql.AnalyticSimpleChooserEngine(env["process"])
    option.setPricingEngine(engine)

    assert option.NPV() == pytest.approx(13.4175, rel=1e-4)


# =============================================================================
# AnalyticComplexChooserEngine
# =============================================================================


def test_complexchooser_pricing(exotic_env):
    """Test complex chooser option pricing."""
    env = exotic_env
    choosing_date = env["today"] + ql.Period("6M")
    call_exercise = ql.EuropeanExercise(env["expiry"])
    put_exercise = ql.EuropeanExercise(env["today"] + ql.Period("18M"))
    option = ql.ComplexChooserOption(
        choosing_date, 100.0, 105.0, call_exercise, put_exercise
    )

    engine = ql.AnalyticComplexChooserEngine(env["process"])
    option.setPricingEngine(engine)

    assert option.NPV() == pytest.approx(13.6593, rel=1e-4)
