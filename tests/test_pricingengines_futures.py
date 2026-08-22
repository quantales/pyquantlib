"""
Tests for futures pricing engines.

Corresponds to src/pricingengines/futures/*.cpp bindings.
"""

import pytest

import pyquantlib as ql


def _perpetual_futures_engine(payoff_type=None):
    """Build a perpetual futures engine and instrument on a flat market.

    maxT is set to 5 rather than the 60-year default: the price has already
    converged to full double precision by then, and the default takes about a
    minute per valuation.
    """
    today = ql.Date(24, 6, 2025)
    ql.Settings.evaluationDate = today
    dc = ql.Actual365Fixed()
    domestic = ql.FlatForward(today, 0.05, dc)
    foreign = ql.FlatForward(today, 0.03, dc)
    spot = ql.SimpleQuote(100.0)
    engine = ql.DiscountingPerpetualFuturesEngine(
        ql.YieldTermStructureHandle(domestic),
        ql.YieldTermStructureHandle(foreign),
        ql.QuoteHandle(spot),
        [0.25, 0.5, 1.0],
        [0.01, 0.012, 0.015],
        [0.02, 0.02, 0.02],
        ql.DiscountingPerpetualFuturesEngine.PiecewiseConstant,
        5.0,
    )
    if payoff_type is None:
        payoff_type = ql.PerpetualFutures.Linear
    perp = ql.PerpetualFutures(payoff_type)
    perp.setPricingEngine(engine)
    return engine, perp


def test_discountingperpetualfuturesengine_linear_npv():
    """Test perpetual futures NPV under a linear payoff."""
    _, perp = _perpetual_futures_engine(ql.PerpetualFutures.Linear)
    assert perp.NPV() == pytest.approx(-97.9009202664, rel=1e-8)


def test_discountingperpetualfuturesengine_inverse_npv():
    """Test perpetual futures NPV under an inverse payoff."""
    _, perp = _perpetual_futures_engine(ql.PerpetualFutures.Inverse)
    assert perp.NPV() == pytest.approx(-102.4907091456, rel=1e-8)


def test_discountingperpetualfuturesengine_accessors():
    """Test the engine exposes its funding schedule."""
    engine, _ = _perpetual_futures_engine()
    assert list(engine.fundingTimes()) == [0.25, 0.5, 1.0]
    assert list(engine.fundingRates()) == pytest.approx([0.01, 0.012, 0.015])
    assert list(engine.interestRateDiffs()) == pytest.approx([0.02, 0.02, 0.02])
    assert engine.assetSpot().currentLink().value() == pytest.approx(
        100.0, rel=1e-12)


def test_discountingperpetualfuturesengine_interpolation_enum():
    """Test the funding-rate interpolation enum."""
    assert int(ql.DiscountingPerpetualFuturesEngine.PiecewiseConstant) == 0
    assert int(ql.DiscountingPerpetualFuturesEngine.Linear) == 1
    assert int(ql.DiscountingPerpetualFuturesEngine.CubicSpline) == 2
