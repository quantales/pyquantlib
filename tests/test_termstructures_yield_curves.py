"""
Tests for interpolated yield curve bindings.

Corresponds to src/termstructures/yield/*.cpp bindings:
- zerocurve.cpp (ZeroCurve)
- discountcurve.cpp (DiscountCurve)
- forwardcurve.cpp (ForwardCurve)
- zerospreadedtermstructure.cpp (ZeroSpreadedTermStructure)
"""

import pytest

import pyquantlib as ql


# =============================================================================
# Fixtures
# =============================================================================


@pytest.fixture(scope="module")
def curve_data():
    """Common data for yield curve tests."""
    today = ql.Date(15, ql.January, 2025)
    ql.Settings.evaluationDate = today
    dates = [
        ql.Date(15, ql.January, 2025),
        ql.Date(15, ql.April, 2025),
        ql.Date(15, ql.July, 2025),
        ql.Date(15, ql.January, 2026),
        ql.Date(15, ql.January, 2027),
        ql.Date(15, ql.January, 2030),
    ]
    zero_rates = [0.03, 0.032, 0.034, 0.036, 0.038, 0.04]
    day_counter = ql.Actual365Fixed()
    return {
        "today": today,
        "dates": dates,
        "zero_rates": zero_rates,
        "day_counter": day_counter,
    }


# =============================================================================
# ZeroCurve
# =============================================================================


def test_zerocurve_construction(curve_data):
    """Test ZeroCurve construction from dates and zero rates."""
    curve = ql.ZeroCurve(
        curve_data["dates"], curve_data["zero_rates"], curve_data["day_counter"]
    )
    assert curve is not None
    assert curve.discount(curve_data["today"]) == pytest.approx(1.0)


def test_zerocurve_with_calendar(curve_data):
    """Test ZeroCurve construction with calendar."""
    curve = ql.ZeroCurve(
        curve_data["dates"],
        curve_data["zero_rates"],
        curve_data["day_counter"],
        ql.TARGET(),
    )
    assert curve is not None


def test_zerocurve_with_compounding(curve_data):
    """Test ZeroCurve with explicit compounding."""
    curve = ql.ZeroCurve(
        curve_data["dates"],
        curve_data["zero_rates"],
        curve_data["day_counter"],
        compounding=ql.Compounded,
        frequency=ql.Semiannual,
    )
    assert curve is not None


def test_zerocurve_data_access(curve_data):
    """Test ZeroCurve data accessor methods."""
    curve = ql.ZeroCurve(
        curve_data["dates"], curve_data["zero_rates"], curve_data["day_counter"]
    )
    assert len(curve.dates()) == 6
    assert len(curve.data()) == 6
    assert len(curve.zeroRates()) == 6
    assert len(curve.times()) == 6
    nodes = curve.nodes()
    assert len(nodes) == 6


def test_zerocurve_zero_rate(curve_data):
    """Test ZeroCurve zero rate interpolation."""
    curve = ql.ZeroCurve(
        curve_data["dates"], curve_data["zero_rates"], curve_data["day_counter"]
    )
    # 5-year point should be 4%
    five_years = curve_data["dates"][-1]
    zero_5y = curve.zeroRate(five_years, curve_data["day_counter"], ql.Continuous)
    assert zero_5y.rate() == pytest.approx(0.04, abs=1e-6)


def test_zerocurve_discount_factor(curve_data):
    """Test ZeroCurve discount factor computation."""
    curve = ql.ZeroCurve(
        curve_data["dates"], curve_data["zero_rates"], curve_data["day_counter"]
    )
    one_year = curve_data["dates"][3]  # Jan 2026
    df = curve.discount(one_year)
    # df = exp(-r*t) where r=0.036, t~1.0
    assert df == pytest.approx(0.96464, rel=1e-3)


# =============================================================================
# DiscountCurve
# =============================================================================


def test_discountcurve_construction(curve_data):
    """Test DiscountCurve construction from dates and discount factors."""
    dfs = [1.0, 0.992, 0.983, 0.965, 0.927, 0.835]
    curve = ql.DiscountCurve(
        curve_data["dates"], dfs, curve_data["day_counter"]
    )
    assert curve is not None
    assert curve.discount(curve_data["today"]) == pytest.approx(1.0)


def test_discountcurve_with_calendar(curve_data):
    """Test DiscountCurve construction with calendar."""
    dfs = [1.0, 0.992, 0.983, 0.965, 0.927, 0.835]
    curve = ql.DiscountCurve(
        curve_data["dates"], dfs, curve_data["day_counter"], ql.TARGET()
    )
    assert curve is not None


def test_discountcurve_data_access(curve_data):
    """Test DiscountCurve data accessor methods."""
    dfs = [1.0, 0.992, 0.983, 0.965, 0.927, 0.835]
    curve = ql.DiscountCurve(
        curve_data["dates"], dfs, curve_data["day_counter"]
    )
    assert len(curve.dates()) == 6
    assert len(curve.discounts()) == 6
    assert curve.discounts()[0] == pytest.approx(1.0)
    nodes = curve.nodes()
    assert len(nodes) == 6


def test_discountcurve_interpolation(curve_data):
    """Test DiscountCurve discount factor interpolation."""
    dfs = [1.0, 0.992, 0.983, 0.965, 0.927, 0.835]
    curve = ql.DiscountCurve(
        curve_data["dates"], dfs, curve_data["day_counter"]
    )
    # 5-year discount factor should match input
    df_5y = curve.discount(curve_data["dates"][-1])
    assert df_5y == pytest.approx(0.835, abs=1e-6)


# =============================================================================
# ForwardCurve
# =============================================================================


def test_forwardcurve_construction(curve_data):
    """Test ForwardCurve construction from dates and forward rates."""
    forwards = [0.03, 0.034, 0.036, 0.038, 0.04, 0.042]
    curve = ql.ForwardCurve(
        curve_data["dates"], forwards, curve_data["day_counter"]
    )
    assert curve is not None
    assert curve.discount(curve_data["today"]) == pytest.approx(1.0)


def test_forwardcurve_with_calendar(curve_data):
    """Test ForwardCurve construction with calendar."""
    forwards = [0.03, 0.034, 0.036, 0.038, 0.04, 0.042]
    curve = ql.ForwardCurve(
        curve_data["dates"], forwards, curve_data["day_counter"], ql.TARGET()
    )
    assert curve is not None


def test_forwardcurve_data_access(curve_data):
    """Test ForwardCurve data accessor methods."""
    forwards = [0.03, 0.034, 0.036, 0.038, 0.04, 0.042]
    curve = ql.ForwardCurve(
        curve_data["dates"], forwards, curve_data["day_counter"]
    )
    assert len(curve.dates()) == 6
    assert len(curve.forwards()) == 6
    nodes = curve.nodes()
    assert len(nodes) == 6


# =============================================================================
# ZeroSpreadedTermStructure
# =============================================================================


def test_zerospreadedtermstructure_construction(curve_data):
    """Test ZeroSpreadedTermStructure construction."""
    base_curve = ql.FlatForward(curve_data["today"], 0.03, curve_data["day_counter"])
    spread = ql.SimpleQuote(0.005)
    spreaded = ql.ZeroSpreadedTermStructure(base_curve, spread)
    assert spreaded is not None


def test_zerospreadedtermstructure_spread_applied(curve_data):
    """Test that spread is correctly applied to zero rates."""
    base_curve = ql.FlatForward(curve_data["today"], 0.03, curve_data["day_counter"])
    spread = ql.SimpleQuote(0.005)
    spreaded = ql.ZeroSpreadedTermStructure(base_curve, spread)

    one_year = curve_data["today"] + ql.Period(1, ql.Years)
    base_rate = base_curve.zeroRate(
        one_year, curve_data["day_counter"], ql.Continuous
    ).rate()
    spreaded_rate = spreaded.zeroRate(
        one_year, curve_data["day_counter"], ql.Continuous
    ).rate()

    assert spreaded_rate == pytest.approx(base_rate + 0.005, abs=1e-6)


def test_zerospreadedtermstructure_dynamic_spread(curve_data):
    """Test that ZeroSpreadedTermStructure responds to spread changes."""
    base_curve = ql.FlatForward(curve_data["today"], 0.03, curve_data["day_counter"])
    spread_quote = ql.SimpleQuote(0.005)
    spreaded = ql.ZeroSpreadedTermStructure(base_curve, spread_quote)

    one_year = curve_data["today"] + ql.Period(1, ql.Years)

    rate_before = spreaded.zeroRate(
        one_year, curve_data["day_counter"], ql.Continuous
    ).rate()
    assert rate_before == pytest.approx(0.035, abs=1e-6)

    # Change spread
    spread_quote.setValue(0.01)
    rate_after = spreaded.zeroRate(
        one_year, curve_data["day_counter"], ql.Continuous
    ).rate()
    assert rate_after == pytest.approx(0.04, abs=1e-6)
