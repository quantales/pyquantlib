"""
Tests for Python extensions.

Corresponds to pyquantlib/extensions/*.py.
"""

import pytest

import pyquantlib as ql
from pyquantlib.extensions import ModifiedKirkEngine, SviSmileSection


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


# =============================================================================
# SviSmileSection (Python extension)
# =============================================================================


def test_svi_time_based_construction():
    """Time-based constructor sets exerciseTime correctly."""
    params = [0.04, 0.1, 0.3, -0.4, 0.0]
    smile = SviSmileSection(1.0, 100.0, params)

    assert smile.exerciseTime() == pytest.approx(1.0)
    assert smile.atmLevel() == pytest.approx(100.0)
    assert isinstance(smile, ql.base.SmileSection)


def test_svi_date_based_construction():
    """Date-based constructor computes exerciseTime from date and day counter."""
    today = ql.Date(15, 1, 2025)
    ql.Settings.instance().evaluationDate = today
    maturity = today + ql.Period(12, ql.Months)
    params = [0.04, 0.1, 0.3, -0.4, 0.0]

    smile = SviSmileSection(maturity, 100.0, params)

    assert smile.exerciseTime() == pytest.approx(1.0, abs=0.01)
    assert smile.exerciseDate() == maturity
    assert smile.atmLevel() == pytest.approx(100.0)


def test_svi_date_based_with_explicit_dc():
    """Date-based constructor accepts an explicit day counter."""
    today = ql.Date(15, 1, 2025)
    ql.Settings.instance().evaluationDate = today
    maturity = today + ql.Period(6, ql.Months)
    params = [0.04, 0.1, 0.3, -0.4, 0.0]

    smile = SviSmileSection(maturity, 100.0, params, dc=ql.Actual365Fixed())

    assert smile.exerciseTime() == pytest.approx(0.4958904109589041, rel=1e-10)
    assert smile.exerciseDate() == maturity


def test_svi_time_and_date_give_same_vol():
    """Time-based and date-based construction produce identical volatilities."""
    today = ql.Date(15, 1, 2025)
    ql.Settings.instance().evaluationDate = today
    maturity = today + ql.Period(12, ql.Months)
    params = [0.04, 0.1, 0.3, -0.4, 0.0]

    smile_time = SviSmileSection(1.0, 100.0, params)
    smile_date = SviSmileSection(maturity, 100.0, params)

    for K in [80.0, 90.0, 100.0, 110.0, 120.0]:
        assert smile_date.volatility(K) == pytest.approx(
            smile_time.volatility(K), rel=0.01,
        )


def test_svi_digital_option_price():
    """digitalOptionPrice matches C++ SviSmileSection."""
    params = [0.04, 0.1, 0.3, -0.4, 0.0]
    smile = SviSmileSection(1.0, 100.0, params)

    digital = smile.digitalOptionPrice(100.0, ql.OptionType.Call, 1.0)
    assert digital == pytest.approx(0.4772728978252871, rel=1e-6)

    # Cross-validate against C++ SviSmileSection
    cpp_smile = ql.SviSmileSection(1.0, 100.0, params)
    assert digital == pytest.approx(
        cpp_smile.digitalOptionPrice(100.0, ql.OptionType.Call, 1.0), rel=1e-6,
    )
