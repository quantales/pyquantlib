"""
Tests for experimental exotic options module.

Corresponds to src/experimental/exoticoptions/*.cpp bindings.
"""

import pytest

import pyquantlib as ql


# =============================================================================
# TwoAssetCorrelationOption
# =============================================================================


def test_twoassetcorrelationoption_construction():
    """TwoAssetCorrelationOption can be constructed."""
    exercise = ql.EuropeanExercise(ql.Date(15, ql.January, 2026))
    option = ql.TwoAssetCorrelationOption(ql.Call, 100.0, 100.0, exercise)
    assert option is not None


def test_twoassetcorrelationoption_put():
    """TwoAssetCorrelationOption can be constructed with Put type."""
    exercise = ql.EuropeanExercise(ql.Date(15, ql.January, 2026))
    option = ql.TwoAssetCorrelationOption(ql.Put, 95.0, 105.0, exercise)
    assert option is not None


def test_twoassetcorrelationoption_pricing():
    """TwoAssetCorrelationOption prices correctly with analytic engine."""
    ql.Settings.evaluationDate = ql.Date(15, 5, 2025)

    spot1 = ql.SimpleQuote(100.0)
    vol1 = ql.BlackConstantVol(
        ql.Date(15, 5, 2025), ql.NullCalendar(), 0.20, ql.Actual365Fixed()
    )
    rate = ql.FlatForward(ql.Date(15, 5, 2025), 0.05, ql.Actual365Fixed())
    div1 = ql.FlatForward(ql.Date(15, 5, 2025), 0.02, ql.Actual365Fixed())
    process1 = ql.BlackScholesMertonProcess(spot1, div1, rate, vol1)

    spot2 = ql.SimpleQuote(100.0)
    vol2 = ql.BlackConstantVol(
        ql.Date(15, 5, 2025), ql.NullCalendar(), 0.25, ql.Actual365Fixed()
    )
    div2 = ql.FlatForward(ql.Date(15, 5, 2025), 0.01, ql.Actual365Fixed())
    process2 = ql.BlackScholesMertonProcess(spot2, div2, rate, vol2)

    corr = ql.SimpleQuote(0.5)
    exercise = ql.EuropeanExercise(ql.Date(15, 5, 2026))
    option = ql.TwoAssetCorrelationOption(ql.Call, 100.0, 100.0, exercise)
    engine = ql.AnalyticTwoAssetCorrelationEngine(process1, process2, corr)
    option.setPricingEngine(engine)
    assert option.NPV() == pytest.approx(9.052216, rel=1e-4)


def test_twoassetcorrelationengine_hidden_handle():
    """AnalyticTwoAssetCorrelationEngine accepts shared_ptr correlation."""
    ql.Settings.evaluationDate = ql.Date(15, 5, 2025)

    spot = ql.SimpleQuote(100.0)
    vol = ql.BlackConstantVol(
        ql.Date(15, 5, 2025), ql.NullCalendar(), 0.20, ql.Actual365Fixed()
    )
    rate = ql.FlatForward(ql.Date(15, 5, 2025), 0.05, ql.Actual365Fixed())
    div = ql.FlatForward(ql.Date(15, 5, 2025), 0.02, ql.Actual365Fixed())
    process = ql.BlackScholesMertonProcess(spot, div, rate, vol)

    corr = ql.SimpleQuote(0.5)
    engine = ql.AnalyticTwoAssetCorrelationEngine(process, process, corr)
    assert engine is not None
