"""
Tests for inflation term structure bindings.

Corresponds to src/termstructures/inflation/*.cpp bindings.
"""

import pytest

import pyquantlib as ql


# =============================================================================
# Fixtures
# =============================================================================


@pytest.fixture(scope="module")
def inflation_env():
    """Common data for inflation term structure tests."""
    original_date = ql.Settings.instance().evaluationDate
    today = ql.Date(15, ql.January, 2025)
    ql.Settings.instance().evaluationDate = today

    calendar = ql.TARGET()
    dc = ql.Actual365Fixed()

    # Flat nominal discount curve at 3%
    nominal_curve = ql.FlatForward(today, 0.03, dc)
    nominal_handle = ql.YieldTermStructureHandle(nominal_curve)

    # Base date for inflation (obs lag = 3 months)
    obs_lag = ql.Period(3, ql.Months)
    base_date = ql.Date(1, ql.October, 2024)

    yield {
        "today": today,
        "calendar": calendar,
        "dc": dc,
        "nominal_curve": nominal_curve,
        "nominal_handle": nominal_handle,
        "obs_lag": obs_lag,
        "base_date": base_date,
    }

    ql.Settings.instance().evaluationDate = original_date


# =============================================================================
# Seasonality ABC
# =============================================================================


def test_seasonality_abc_exists():
    """Test Seasonality ABC is in base submodule."""
    assert hasattr(ql.base, "Seasonality")


def test_seasonality_zombie():
    """Test direct instantiation creates a zombie object."""
    zombie = ql.base.Seasonality()
    assert zombie is not None


# =============================================================================
# MultiplicativePriceSeasonality
# =============================================================================


def test_multiplicativepriceseasonality_exists():
    """Test MultiplicativePriceSeasonality is in main module."""
    assert hasattr(ql, "MultiplicativePriceSeasonality")


def test_multiplicativepriceseasonality_default():
    """Test default construction."""
    s = ql.MultiplicativePriceSeasonality()
    assert s is not None


def test_multiplicativepriceseasonality_parameterized():
    """Test construction with base date, frequency, and factors."""
    base_date = ql.Date(1, ql.January, 2024)
    factors = [1.0, 1.01, 1.02, 0.99, 0.98, 1.0,
               1.01, 1.03, 0.97, 0.98, 1.0, 1.01]
    s = ql.MultiplicativePriceSeasonality(base_date, ql.Monthly, factors)

    assert s.seasonalityBaseDate() == base_date
    assert s.frequency() == ql.Monthly
    assert len(s.seasonalityFactors()) == 12


def test_multiplicativepriceseasonality_factor():
    """Test seasonalityFactor retrieval for a specific date."""
    base_date = ql.Date(1, ql.January, 2024)
    factors = [1.0, 1.01, 1.02, 0.99, 0.98, 1.0,
               1.01, 1.03, 0.97, 0.98, 1.0, 1.01]
    s = ql.MultiplicativePriceSeasonality(base_date, ql.Monthly, factors)

    # Factor for January should be factors[0] = 1.0
    jan_date = ql.Date(15, ql.January, 2025)
    factor = s.seasonalityFactor(jan_date)
    assert factor == pytest.approx(1.0)


def test_multiplicativepriceseasonality_set():
    """Test set() method to update parameters."""
    s = ql.MultiplicativePriceSeasonality()

    base_date = ql.Date(1, ql.January, 2024)
    factors = [1.0] * 12
    s.set(base_date, ql.Monthly, factors)

    assert s.seasonalityBaseDate() == base_date
    assert s.frequency() == ql.Monthly


# =============================================================================
# KerkhofSeasonality
# =============================================================================


def test_kerkhofseasonality_exists():
    """Test KerkhofSeasonality is in main module."""
    assert hasattr(ql, "KerkhofSeasonality")


def test_kerkhofseasonality_construction():
    """Test KerkhofSeasonality construction."""
    base_date = ql.Date(1, ql.January, 2024)
    factors = [1.0, 1.01, 1.02, 0.99, 0.98, 1.0,
               1.01, 1.03, 0.97, 0.98, 1.0, 1.01]
    s = ql.KerkhofSeasonality(base_date, factors)

    assert s.seasonalityBaseDate() == base_date
    assert len(s.seasonalityFactors()) == 12
    assert isinstance(s, ql.MultiplicativePriceSeasonality)


# =============================================================================
# Inflation Bootstrap Helper ABCs
# =============================================================================


def test_zeroinflationhelper_abc_exists():
    """Test ZeroInflationHelper base exists in base submodule."""
    assert hasattr(ql.base, "ZeroInflationHelper")


def test_relativedatezeroinflationhelper_abc_exists():
    """Test RelativeDateZeroInflationHelper base exists."""
    assert hasattr(ql.base, "RelativeDateZeroInflationHelper")


def test_yoyinflationhelper_abc_exists():
    """Test YoYInflationHelper base exists in base submodule."""
    assert hasattr(ql.base, "YoYInflationHelper")


def test_relativedateyoyinflationhelper_abc_exists():
    """Test RelativeDateYoYInflationHelper base exists."""
    assert hasattr(ql.base, "RelativeDateYoYInflationHelper")


# =============================================================================
# ZeroCouponInflationSwapHelper
# =============================================================================


def test_zerocouponinflationswaphelper_exists():
    """Test ZeroCouponInflationSwapHelper is in main module."""
    assert hasattr(ql, "ZeroCouponInflationSwapHelper")


def test_zerocouponinflationswaphelper_rate(inflation_env):
    """Test ZeroCouponInflationSwapHelper construction from rate."""
    idx = ql.USCPI()
    helper = ql.ZeroCouponInflationSwapHelper(
        0.025,
        inflation_env["obs_lag"],
        ql.Date(15, ql.January, 2027),
        inflation_env["calendar"],
        ql.ModifiedFollowing,
        inflation_env["dc"],
        idx,
        ql.CPI.Flat,
    )
    assert helper is not None
    assert isinstance(helper, ql.base.ZeroInflationHelper)


def test_zerocouponinflationswaphelper_quote(inflation_env):
    """Test ZeroCouponInflationSwapHelper construction from Quote."""
    idx = ql.USCPI()
    quote = ql.SimpleQuote(0.025)
    helper = ql.ZeroCouponInflationSwapHelper(
        quote,
        inflation_env["obs_lag"],
        ql.Date(15, ql.January, 2027),
        inflation_env["calendar"],
        ql.ModifiedFollowing,
        inflation_env["dc"],
        idx,
        ql.CPI.Flat,
    )
    assert helper is not None


def test_zerocouponinflationswaphelper_handle(inflation_env):
    """Test ZeroCouponInflationSwapHelper construction from Handle<Quote>."""
    idx = ql.USCPI()
    quote = ql.SimpleQuote(0.025)
    handle = ql.QuoteHandle(quote)
    helper = ql.ZeroCouponInflationSwapHelper(
        handle,
        inflation_env["obs_lag"],
        ql.Date(15, ql.January, 2027),
        inflation_env["calendar"],
        ql.ModifiedFollowing,
        inflation_env["dc"],
        idx,
        ql.CPI.Flat,
    )
    assert helper is not None


# =============================================================================
# YearOnYearInflationSwapHelper
# =============================================================================


def test_yearonyearinflationswaphelper_exists():
    """Test YearOnYearInflationSwapHelper is in main module."""
    assert hasattr(ql, "YearOnYearInflationSwapHelper")


def test_yearonyearinflationswaphelper_rate(inflation_env):
    """Test YearOnYearInflationSwapHelper construction from rate."""
    zero_idx = ql.USCPI()
    yoy_idx = ql.YoYInflationIndex(zero_idx)
    helper = ql.YearOnYearInflationSwapHelper(
        0.025,
        inflation_env["obs_lag"],
        ql.Date(15, ql.January, 2027),
        inflation_env["calendar"],
        ql.ModifiedFollowing,
        inflation_env["dc"],
        yoy_idx,
        ql.CPI.Flat,
        inflation_env["nominal_handle"],
    )
    assert helper is not None
    assert isinstance(helper, ql.base.YoYInflationHelper)


def test_yearonyearinflationswaphelper_quote(inflation_env):
    """Test YearOnYearInflationSwapHelper construction from Quote."""
    zero_idx = ql.USCPI()
    yoy_idx = ql.YoYInflationIndex(zero_idx)
    quote = ql.SimpleQuote(0.025)
    helper = ql.YearOnYearInflationSwapHelper(
        quote,
        inflation_env["obs_lag"],
        ql.Date(15, ql.January, 2027),
        inflation_env["calendar"],
        ql.ModifiedFollowing,
        inflation_env["dc"],
        yoy_idx,
        ql.CPI.Flat,
        inflation_env["nominal_handle"],
    )
    assert helper is not None


# =============================================================================
# ZeroInflationCurve (Interpolated)
# =============================================================================


def test_zeroinflationcurve_exists():
    """Test ZeroInflationCurve is in main module."""
    assert hasattr(ql, "ZeroInflationCurve")


def test_zeroinflationcurve_construction(inflation_env):
    """Test ZeroInflationCurve construction from dates and rates."""
    dates = [
        inflation_env["base_date"],
        ql.Date(1, ql.October, 2025),
        ql.Date(1, ql.October, 2026),
        ql.Date(1, ql.October, 2027),
    ]
    rates = [0.02, 0.022, 0.025, 0.027]

    curve = ql.ZeroInflationCurve(
        inflation_env["today"], dates, rates, ql.Monthly,
        inflation_env["dc"],
    )

    assert curve is not None
    assert isinstance(curve, ql.base.ZeroInflationTermStructure)
    assert curve.frequency() == ql.Monthly


def test_zeroinflationcurve_inspectors(inflation_env):
    """Test ZeroInflationCurve date/rate/node inspectors."""
    dates = [
        inflation_env["base_date"],
        ql.Date(1, ql.October, 2025),
        ql.Date(1, ql.October, 2026),
        ql.Date(1, ql.October, 2027),
    ]
    rates = [0.02, 0.022, 0.025, 0.027]

    curve = ql.ZeroInflationCurve(
        inflation_env["today"], dates, rates, ql.Monthly,
        inflation_env["dc"],
    )

    assert len(curve.dates()) == 4
    assert len(curve.rates()) == 4
    assert len(curve.times()) == 4
    assert len(curve.data()) == 4
    assert curve.rates()[0] == pytest.approx(0.02)

    nodes = curve.nodes()
    assert len(nodes) == 4
    assert nodes[0][1] == pytest.approx(0.02)


def test_zeroinflationcurve_zero_rate(inflation_env):
    """Test ZeroInflationCurve zeroRate at an interpolated point."""
    dates = [
        inflation_env["base_date"],
        ql.Date(1, ql.October, 2025),
        ql.Date(1, ql.October, 2026),
        ql.Date(1, ql.October, 2027),
    ]
    rates = [0.02, 0.022, 0.025, 0.027]

    curve = ql.ZeroInflationCurve(
        inflation_env["today"], dates, rates, ql.Monthly,
        inflation_env["dc"],
    )

    # Rate at an input date should match
    rate = curve.zeroRate(ql.Date(1, ql.October, 2025))
    assert rate == pytest.approx(0.022, abs=1e-6)


def test_zeroinflationcurve_with_seasonality(inflation_env):
    """Test ZeroInflationCurve construction with seasonality."""
    dates = [
        inflation_env["base_date"],
        ql.Date(1, ql.October, 2025),
        ql.Date(1, ql.October, 2026),
    ]
    rates = [0.02, 0.022, 0.025]

    base_date = ql.Date(1, ql.January, 2024)
    factors = [1.0] * 12
    seasonality = ql.MultiplicativePriceSeasonality(
        base_date, ql.Monthly, factors,
    )

    curve = ql.ZeroInflationCurve(
        inflation_env["today"], dates, rates, ql.Monthly,
        inflation_env["dc"], seasonality,
    )

    assert curve.hasSeasonality()


# =============================================================================
# YoYInflationCurve (Interpolated)
# =============================================================================


def test_yoyinflationcurve_exists():
    """Test YoYInflationCurve is in main module."""
    assert hasattr(ql, "YoYInflationCurve")


def test_yoyinflationcurve_construction(inflation_env):
    """Test YoYInflationCurve construction from dates and rates."""
    dates = [
        inflation_env["base_date"],
        ql.Date(1, ql.October, 2025),
        ql.Date(1, ql.October, 2026),
        ql.Date(1, ql.October, 2027),
    ]
    rates = [0.02, 0.022, 0.025, 0.027]

    curve = ql.YoYInflationCurve(
        inflation_env["today"], dates, rates, ql.Monthly,
        inflation_env["dc"],
    )

    assert curve is not None
    assert isinstance(curve, ql.base.YoYInflationTermStructure)


def test_yoyinflationcurve_inspectors(inflation_env):
    """Test YoYInflationCurve date/rate/node inspectors."""
    dates = [
        inflation_env["base_date"],
        ql.Date(1, ql.October, 2025),
        ql.Date(1, ql.October, 2026),
        ql.Date(1, ql.October, 2027),
    ]
    rates = [0.02, 0.022, 0.025, 0.027]

    curve = ql.YoYInflationCurve(
        inflation_env["today"], dates, rates, ql.Monthly,
        inflation_env["dc"],
    )

    assert len(curve.dates()) == 4
    assert len(curve.rates()) == 4
    assert len(curve.times()) == 4
    assert len(curve.data()) == 4
    assert curve.rates()[0] == pytest.approx(0.02)

    nodes = curve.nodes()
    assert len(nodes) == 4


def test_yoyinflationcurve_yoy_rate(inflation_env):
    """Test YoYInflationCurve yoyRate at an interpolated point."""
    dates = [
        inflation_env["base_date"],
        ql.Date(1, ql.October, 2025),
        ql.Date(1, ql.October, 2026),
        ql.Date(1, ql.October, 2027),
    ]
    rates = [0.02, 0.022, 0.025, 0.027]

    curve = ql.YoYInflationCurve(
        inflation_env["today"], dates, rates, ql.Monthly,
        inflation_env["dc"],
    )

    rate = curve.yoyRate(ql.Date(1, ql.October, 2025))
    assert rate == pytest.approx(0.022, abs=1e-6)


# =============================================================================
# PiecewiseZeroInflationCurve (Bootstrapped)
# =============================================================================


def test_piecewisezeroinflationcurve_exists():
    """Test PiecewiseZeroInflationCurve is in main module."""
    assert hasattr(ql, "PiecewiseZeroInflationCurve")


def _build_zero_inflation_helpers(env, rates_by_year):
    """Build zero-coupon inflation swap helpers."""
    idx = ql.USCPI()
    # Add base fixing required for bootstrapping
    idx.addFixing(ql.Date(1, ql.October, 2024), 315.0)
    helpers = []
    for years, rate in rates_by_year:
        maturity = env["today"] + ql.Period(years, ql.Years)
        helpers.append(ql.ZeroCouponInflationSwapHelper(
            rate,
            env["obs_lag"],
            maturity,
            env["calendar"],
            ql.ModifiedFollowing,
            env["dc"],
            idx,
            ql.CPI.Flat,
        ))
    return helpers


def test_piecewisezeroinflationcurve_bootstrap(inflation_env):
    """Test PiecewiseZeroInflationCurve bootstrapping from helpers."""
    helpers = _build_zero_inflation_helpers(inflation_env, [
        (1, 0.020), (2, 0.022), (3, 0.025),
        (5, 0.027), (7, 0.028), (10, 0.030),
    ])

    curve = ql.PiecewiseZeroInflationCurve(
        inflation_env["today"],
        inflation_env["base_date"],
        ql.Monthly,
        inflation_env["dc"],
        helpers,
    )

    assert curve is not None
    assert isinstance(curve, ql.base.ZeroInflationTermStructure)


def test_piecewisezeroinflationcurve_nodes(inflation_env):
    """Test PiecewiseZeroInflationCurve nodes accessor."""
    helpers = _build_zero_inflation_helpers(inflation_env, [
        (1, 0.020), (2, 0.022), (3, 0.025),
        (5, 0.027), (7, 0.028), (10, 0.030),
    ])

    curve = ql.PiecewiseZeroInflationCurve(
        inflation_env["today"],
        inflation_env["base_date"],
        ql.Monthly,
        inflation_env["dc"],
        helpers,
    )

    nodes = curve.nodes()
    assert len(nodes) > 0

    dates = curve.dates()
    times = curve.times()
    data = curve.data()
    assert len(dates) == len(nodes)
    assert len(times) == len(nodes)
    assert len(data) == len(nodes)


def test_piecewisezeroinflationcurve_zero_rate(inflation_env):
    """Test bootstrapped curve produces sensible zero rates."""
    input_rates = [
        (1, 0.020), (2, 0.022), (3, 0.025),
        (5, 0.027), (7, 0.028),
    ]
    helpers = _build_zero_inflation_helpers(inflation_env, input_rates)

    curve = ql.PiecewiseZeroInflationCurve(
        inflation_env["today"],
        inflation_env["base_date"],
        ql.Monthly,
        inflation_env["dc"],
        helpers,
    )

    # Query mid-curve point (within max date); verify rate is sensible
    mid_date = inflation_env["today"] + ql.Period(3, ql.Years)
    rate = curve.zeroRate(mid_date)
    # Should be between the 2Y (0.022) and 5Y (0.027) input rates
    assert 0.020 < rate < 0.030


# =============================================================================
# PiecewiseYoYInflationCurve (Bootstrapped)
# =============================================================================


def test_piecewiseyoyinflationcurve_exists():
    """Test PiecewiseYoYInflationCurve is in main module."""
    assert hasattr(ql, "PiecewiseYoYInflationCurve")


def test_piecewiseyoyinflationcurve_bootstrap(inflation_env):
    """Test PiecewiseYoYInflationCurve bootstrapping from helpers."""
    zero_idx = ql.USCPI()
    yoy_idx = ql.YoYInflationIndex(zero_idx)

    helpers = []
    for years, rate in [(1, 0.020), (2, 0.022), (3, 0.025), (5, 0.027)]:
        maturity = inflation_env["today"] + ql.Period(years, ql.Years)
        helpers.append(ql.YearOnYearInflationSwapHelper(
            rate,
            inflation_env["obs_lag"],
            maturity,
            inflation_env["calendar"],
            ql.ModifiedFollowing,
            inflation_env["dc"],
            yoy_idx,
            ql.CPI.Flat,
            inflation_env["nominal_handle"],
        ))

    curve = ql.PiecewiseYoYInflationCurve(
        inflation_env["today"],
        inflation_env["base_date"],
        0.02,  # base YoY rate
        ql.Monthly,
        inflation_env["dc"],
        helpers,
    )

    assert curve is not None
    assert isinstance(curve, ql.base.YoYInflationTermStructure)


def test_piecewiseyoyinflationcurve_nodes(inflation_env):
    """Test PiecewiseYoYInflationCurve nodes accessor."""
    zero_idx = ql.USCPI()
    yoy_idx = ql.YoYInflationIndex(zero_idx)

    helpers = []
    for years, rate in [(1, 0.020), (2, 0.022), (3, 0.025)]:
        maturity = inflation_env["today"] + ql.Period(years, ql.Years)
        helpers.append(ql.YearOnYearInflationSwapHelper(
            rate,
            inflation_env["obs_lag"],
            maturity,
            inflation_env["calendar"],
            ql.ModifiedFollowing,
            inflation_env["dc"],
            yoy_idx,
            ql.CPI.Flat,
            inflation_env["nominal_handle"],
        ))

    curve = ql.PiecewiseYoYInflationCurve(
        inflation_env["today"],
        inflation_env["base_date"],
        0.02,
        ql.Monthly,
        inflation_env["dc"],
        helpers,
    )

    nodes = curve.nodes()
    assert len(nodes) > 0

    dates = curve.dates()
    times = curve.times()
    data = curve.data()
    assert len(dates) == len(nodes)
    assert len(times) == len(nodes)
    assert len(data) == len(nodes)


# =============================================================================
# InflationTermStructure.setSeasonality
# =============================================================================


def test_inflationtermstructure_set_seasonality(inflation_env):
    """Test setSeasonality on an inflation curve."""
    dates = [
        inflation_env["base_date"],
        ql.Date(1, ql.October, 2025),
        ql.Date(1, ql.October, 2026),
    ]
    rates = [0.02, 0.022, 0.025]

    curve = ql.ZeroInflationCurve(
        inflation_env["today"], dates, rates, ql.Monthly,
        inflation_env["dc"],
    )

    assert not curve.hasSeasonality()

    base_date = ql.Date(1, ql.January, 2024)
    factors = [1.0] * 12
    seasonality = ql.MultiplicativePriceSeasonality(
        base_date, ql.Monthly, factors,
    )
    curve.setSeasonality(seasonality)
    assert curve.hasSeasonality()

    # Remove seasonality
    curve.setSeasonality()
    assert not curve.hasSeasonality()


def test_inflationtermstructure_seasonality_accessor(inflation_env):
    """Test seasonality() accessor returns the set seasonality."""
    dates = [
        inflation_env["base_date"],
        ql.Date(1, ql.October, 2025),
        ql.Date(1, ql.October, 2026),
    ]
    rates = [0.02, 0.022, 0.025]

    base_date = ql.Date(1, ql.January, 2024)
    factors = [1.0] * 12
    seasonality = ql.MultiplicativePriceSeasonality(
        base_date, ql.Monthly, factors,
    )

    curve = ql.ZeroInflationCurve(
        inflation_env["today"], dates, rates, ql.Monthly,
        inflation_env["dc"], seasonality,
    )

    retrieved = curve.seasonality()
    assert retrieved is not None
