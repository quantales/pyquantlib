"""
Tests for Python extensions.

Corresponds to pyquantlib/extensions/*.py.
"""

import pytest

import pyquantlib as ql
from pyquantlib.extensions import ModifiedKirkEngine


@pytest.fixture
def market_setup():
    """Common market setup."""
    today = ql.Date(15, 1, 2025)
    ql.Settings.instance().evaluationDate = today
    dc = ql.Actual365Fixed()
    cal = ql.NullCalendar()

    rate_ts = ql.FlatForward(today, 0.05, dc)
    rate_handle = ql.YieldTermStructureHandle(rate_ts)

    div_ts = ql.FlatForward(today, 0.02, dc)
    div_handle = ql.YieldTermStructureHandle(div_ts)

    # Store created objects to keep them alive
    _refs = []

    def make_process(spot, vol):
        # Keep underlying objects alive to prevent garbage collection
        quote = ql.SimpleQuote(spot)
        spot_handle = ql.QuoteHandle(quote)
        vol_ts = ql.BlackConstantVol(today, cal, vol, dc)
        vol_handle = ql.BlackVolTermStructureHandle(vol_ts)

        process = ql.GeneralizedBlackScholesProcess(
            spot_handle,
            div_handle,
            rate_handle,
            vol_handle,
        )
        # Store references to keep ALL objects alive
        _refs.append((quote, spot_handle, vol_ts, vol_handle))
        return process

    return today, make_process


def test_invalid_correlation(market_setup):
    """Rejects correlation outside [-1, 1]."""
    _, make_process = market_setup
    p1 = make_process(100, 0.3)
    p2 = make_process(100, 0.2)

    with pytest.raises(ValueError):
        ModifiedKirkEngine(p1, p2, 1.5)


def test_pricing_integration(market_setup):
    """Engine integrates with QuantLib pricing framework."""
    today, make_process = market_setup
    p1 = make_process(100, 0.3)
    p2 = make_process(100, 0.2)

    maturity = today + ql.Period(6, ql.Months)
    payoff = ql.PlainVanillaPayoff(ql.OptionType.Call, 5.0)
    spread_payoff = ql.SpreadBasketPayoff(payoff)
    exercise = ql.EuropeanExercise(maturity)
    option = ql.BasketOption(spread_payoff, exercise)

    engine = ModifiedKirkEngine(p1, p2, 0.9)
    option.setPricingEngine(engine)

    npv = option.NPV()
    expected_npv = 2.3438472642728536
    assert npv == pytest.approx(expected_npv, rel=1e-6)


def test_static_methods():
    """Static helper methods work."""
    vol = ModifiedKirkEngine.kirk_volatility(100, 100, 5, 0.3, 0.2, 0.9)
    expected_vol = 0.1530491302856018
    assert vol == pytest.approx(expected_vol, rel=1e-6)

    skew = ModifiedKirkEngine.skew_slope(100, 100, 5, 0.3, 0.2, 0.9)
    expected_skew = 0.0016000116933208614
    assert skew == pytest.approx(expected_skew, rel=1e-6)
