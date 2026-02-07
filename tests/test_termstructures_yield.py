"""
Tests for yield term structure bindings.

Corresponds to src/termstructures/yield/*.cpp bindings:
- ratehelpers.cpp (Pillar, RateHelper, DepositRateHelper, FraRateHelper, SwapRateHelper)
- oisratehelper.cpp (OISRateHelper)
- piecewiseyieldcurve.cpp (PiecewiseYieldCurve instantiations)
"""

import pytest

import pyquantlib as ql

# =============================================================================
# Fixtures
# =============================================================================


@pytest.fixture(scope="module")
def curve_env():
    """Common data for yield curve tests."""
    original_date = ql.Settings.instance().evaluationDate
    today = ql.Date(15, ql.January, 2025)
    ql.Settings.instance().evaluationDate = today

    calendar = ql.TARGET()
    day_counter = ql.Actual365Fixed()

    # Flat forwarding curve at 3%
    flat_curve = ql.FlatForward(today, 0.03, day_counter)
    curve_handle = ql.YieldTermStructureHandle(flat_curve)

    # Euribor6M index for swap helpers
    euribor6m = ql.Euribor6M(curve_handle)

    yield {
        "today": today,
        "calendar": calendar,
        "day_counter": day_counter,
        "flat_curve": flat_curve,
        "curve_handle": curve_handle,
        "euribor6m": euribor6m,
    }

    ql.Settings.instance().evaluationDate = original_date


# =============================================================================
# Pillar
# =============================================================================


def test_pillar_enum_values():
    """Test Pillar.Choice enum values exist."""
    assert hasattr(ql, "Pillar")
    assert hasattr(ql.Pillar, "Choice")
    assert ql.Pillar.Choice.MaturityDate is not None
    assert ql.Pillar.Choice.LastRelevantDate is not None
    assert ql.Pillar.Choice.CustomDate is not None


def test_pillar_enum_distinct():
    """Test Pillar.Choice values are distinct."""
    assert ql.Pillar.Choice.MaturityDate != ql.Pillar.Choice.LastRelevantDate
    assert ql.Pillar.Choice.MaturityDate != ql.Pillar.Choice.CustomDate
    assert ql.Pillar.Choice.LastRelevantDate != ql.Pillar.Choice.CustomDate


# =============================================================================
# RateHelper (base class)
# =============================================================================


def test_ratehelper_exists():
    """Test RateHelper class exists in base submodule."""
    assert hasattr(ql.base, "RateHelper")


def test_relativedateratehelper_exists():
    """Test RelativeDateRateHelper class exists in base submodule."""
    assert hasattr(ql.base, "RelativeDateRateHelper")


# =============================================================================
# DepositRateHelper
# =============================================================================


def test_depositratehelper_rate_index(curve_env):
    """Test DepositRateHelper construction with rate and IborIndex."""
    helper = ql.DepositRateHelper(0.03, curve_env["euribor6m"])
    assert helper is not None
    assert helper.maturityDate() > curve_env["today"]


def test_depositratehelper_quote_index(curve_env):
    """Test DepositRateHelper construction with SimpleQuote (hidden handle)."""
    quote = ql.SimpleQuote(0.025)
    helper = ql.DepositRateHelper(quote, curve_env["euribor6m"])
    assert helper is not None


def test_depositratehelper_handle_index(curve_env):
    """Test DepositRateHelper construction with QuoteHandle."""
    quote = ql.SimpleQuote(0.025)
    handle = ql.QuoteHandle(quote)
    helper = ql.DepositRateHelper(handle, curve_env["euribor6m"])
    assert helper is not None


def test_depositratehelper_full_params(curve_env):
    """Test DepositRateHelper with explicit market conventions."""
    helper = ql.DepositRateHelper(
        0.03,
        ql.Period(6, ql.Months),
        2,  # fixingDays
        curve_env["calendar"],
        ql.ModifiedFollowing,
        True,  # endOfMonth
        ql.Actual360(),
    )
    assert helper is not None
    assert helper.maturityDate() > curve_env["today"]


def test_depositratehelper_pillar_date(curve_env):
    """Test DepositRateHelper pillar date."""
    helper = ql.DepositRateHelper(0.03, curve_env["euribor6m"])
    pillar = helper.pillarDate()
    assert pillar > curve_env["today"]


def test_depositratehelper_base_methods(curve_env):
    """Test RateHelper base class methods via DepositRateHelper."""
    helper = ql.DepositRateHelper(0.03, curve_env["euribor6m"])

    assert helper.earliestDate() is not None
    assert helper.latestDate() is not None
    assert helper.latestRelevantDate() is not None
    assert helper.maturityDate() is not None


# =============================================================================
# FraRateHelper
# =============================================================================


def test_fraratehelper_months(curve_env):
    """Test FraRateHelper with monthsToStart."""
    helper = ql.FraRateHelper(0.035, 3, curve_env["euribor6m"])
    assert helper is not None
    assert helper.maturityDate() > curve_env["today"]


def test_fraratehelper_period(curve_env):
    """Test FraRateHelper with period to start."""
    helper = ql.FraRateHelper(
        0.035, ql.Period(6, ql.Months), curve_env["euribor6m"]
    )
    assert helper is not None
    assert helper.maturityDate() > curve_env["today"]


def test_fraratehelper_with_pillar(curve_env):
    """Test FraRateHelper with explicit pillar choice."""
    helper = ql.FraRateHelper(
        0.035, 3, curve_env["euribor6m"],
        pillar=ql.Pillar.Choice.MaturityDate,
    )
    assert helper is not None


def test_fraratehelper_hidden_handle(curve_env):
    """Test FraRateHelper with SimpleQuote (hidden handle)."""
    quote = ql.SimpleQuote(0.035)
    helper = ql.FraRateHelper(quote, 3, curve_env["euribor6m"])
    assert helper is not None


# =============================================================================
# SwapRateHelper
# =============================================================================


def test_swapratehelper_rate(curve_env):
    """Test SwapRateHelper construction with rate."""
    helper = ql.SwapRateHelper(
        0.04,
        ql.Period(5, ql.Years),
        curve_env["calendar"],
        ql.Annual,
        ql.Unadjusted,
        ql.Thirty360(ql.Thirty360.BondBasis),
        curve_env["euribor6m"],
    )
    assert helper is not None
    assert helper.maturityDate() > curve_env["today"]


def test_swapratehelper_hidden_handle(curve_env):
    """Test SwapRateHelper with SimpleQuote (hidden handle)."""
    quote = ql.SimpleQuote(0.04)
    helper = ql.SwapRateHelper(
        quote,
        ql.Period(5, ql.Years),
        curve_env["calendar"],
        ql.Annual,
        ql.Unadjusted,
        ql.Thirty360(ql.Thirty360.BondBasis),
        curve_env["euribor6m"],
    )
    assert helper is not None


def test_swapratehelper_quote_handle(curve_env):
    """Test SwapRateHelper with QuoteHandle."""
    quote = ql.SimpleQuote(0.04)
    handle = ql.QuoteHandle(quote)
    helper = ql.SwapRateHelper(
        handle,
        ql.Period(5, ql.Years),
        curve_env["calendar"],
        ql.Annual,
        ql.Unadjusted,
        ql.Thirty360(ql.Thirty360.BondBasis),
        curve_env["euribor6m"],
    )
    assert helper is not None


def test_swapratehelper_swap(curve_env):
    """Test SwapRateHelper underlying swap access."""
    helper = ql.SwapRateHelper(
        0.04,
        ql.Period(5, ql.Years),
        curve_env["calendar"],
        ql.Annual,
        ql.Unadjusted,
        ql.Thirty360(ql.Thirty360.BondBasis),
        curve_env["euribor6m"],
    )
    swap = helper.swap()
    assert swap is not None
    assert isinstance(swap, ql.VanillaSwap)


def test_swapratehelper_spread(curve_env):
    """Test SwapRateHelper spread method."""
    helper = ql.SwapRateHelper(
        0.04,
        ql.Period(5, ql.Years),
        curve_env["calendar"],
        ql.Annual,
        ql.Unadjusted,
        ql.Thirty360(ql.Thirty360.BondBasis),
        curve_env["euribor6m"],
    )
    spread = helper.spread()
    assert spread is not None


def test_swapratehelper_forward_start(curve_env):
    """Test SwapRateHelper with forward start."""
    helper = ql.SwapRateHelper(
        0.04,
        ql.Period(5, ql.Years),
        curve_env["calendar"],
        ql.Annual,
        ql.Unadjusted,
        ql.Thirty360(ql.Thirty360.BondBasis),
        curve_env["euribor6m"],
        fwdStart=ql.Period(1, ql.Years),
    )
    fwd_start = helper.forwardStart()
    assert fwd_start == ql.Period(1, ql.Years)


# =============================================================================
# OISRateHelper
# =============================================================================


@pytest.fixture(scope="module")
def ois_env():
    """Common data for OIS tests."""
    original_date = ql.Settings.instance().evaluationDate
    today = ql.Date(15, ql.January, 2025)
    ql.Settings.instance().evaluationDate = today

    calendar = ql.TARGET()
    flat_curve = ql.FlatForward(today, 0.03, ql.Actual365Fixed())
    curve_handle = ql.YieldTermStructureHandle(flat_curve)

    overnight_index = ql.OvernightIndex(
        "TESTON", 0, ql.EURCurrency(), calendar,
        ql.Actual360(), curve_handle
    )

    yield {
        "today": today,
        "overnight_index": overnight_index,
    }

    ql.Settings.instance().evaluationDate = original_date


def test_oisratehelper_rate(ois_env):
    """Test OISRateHelper construction with rate."""
    helper = ql.OISRateHelper(
        2,  # settlementDays
        ql.Period(1, ql.Years),
        0.035,
        ois_env["overnight_index"],
    )
    assert helper is not None
    assert helper.maturityDate() > ois_env["today"]


def test_oisratehelper_hidden_handle(ois_env):
    """Test OISRateHelper with SimpleQuote (hidden handle)."""
    quote = ql.SimpleQuote(0.035)
    helper = ql.OISRateHelper(
        2,
        ql.Period(1, ql.Years),
        quote,
        ois_env["overnight_index"],
    )
    assert helper is not None


def test_oisratehelper_quote_handle(ois_env):
    """Test OISRateHelper with QuoteHandle."""
    quote = ql.SimpleQuote(0.035)
    handle = ql.QuoteHandle(quote)
    helper = ql.OISRateHelper(
        2,
        ql.Period(1, ql.Years),
        handle,
        ois_env["overnight_index"],
    )
    assert helper is not None


def test_oisratehelper_pillar_date(ois_env):
    """Test OISRateHelper has valid pillar and maturity dates."""
    helper = ql.OISRateHelper(
        2,
        ql.Period(1, ql.Years),
        0.035,
        ois_env["overnight_index"],
    )
    assert helper.pillarDate() > ois_env["today"]
    assert helper.maturityDate() > ois_env["today"]


def test_oisratehelper_optional_params(ois_env):
    """Test OISRateHelper with optional parameters."""
    helper = ql.OISRateHelper(
        2,
        ql.Period(1, ql.Years),
        0.035,
        ois_env["overnight_index"],
        telescopicValueDates=True,
        paymentLag=2,
        paymentConvention=ql.ModifiedFollowing,
        paymentFrequency=ql.Annual,
    )
    assert helper is not None


def test_oisratehelper_averaging_method(ois_env):
    """Test OISRateHelper with explicit RateAveraging parameter."""
    helper_compound = ql.OISRateHelper(
        2,
        ql.Period(1, ql.Years),
        0.035,
        ois_env["overnight_index"],
        averagingMethod=ql.RateAveraging.Type.Compound,
    )
    assert helper_compound is not None

    helper_simple = ql.OISRateHelper(
        2,
        ql.Period(1, ql.Years),
        0.035,
        ois_env["overnight_index"],
        averagingMethod=ql.RateAveraging.Type.Simple,
    )
    assert helper_simple is not None


# =============================================================================
# PiecewiseYieldCurve
# =============================================================================


def test_piecewise_classes_exist():
    """Test all PiecewiseYieldCurve instantiations exist."""
    assert hasattr(ql, "PiecewiseLogLinearDiscount")
    assert hasattr(ql, "PiecewiseLinearDiscount")
    assert hasattr(ql, "PiecewiseLinearZero")
    assert hasattr(ql, "PiecewiseCubicZero")
    assert hasattr(ql, "PiecewiseLinearForward")
    assert hasattr(ql, "PiecewiseBackwardFlatForward")
    assert hasattr(ql, "PiecewiseFlatForward")
    # PiecewiseFlatForward is an alias for PiecewiseBackwardFlatForward
    assert ql.PiecewiseFlatForward is ql.PiecewiseBackwardFlatForward


def _build_helpers(today, calendar, euribor6m):
    """Build a set of rate helpers for curve bootstrapping."""
    helpers = []

    # Deposit helpers (short end)
    deposit_rates = [
        (ql.Period(1, ql.Months), 0.0320),
        (ql.Period(3, ql.Months), 0.0330),
        (ql.Period(6, ql.Months), 0.0340),
    ]
    for tenor, rate in deposit_rates:
        helpers.append(ql.DepositRateHelper(
            rate, tenor, 2, calendar,
            ql.ModifiedFollowing, True, ql.Actual360()
        ))

    # Swap helpers (long end)
    swap_rates = [
        (ql.Period(1, ql.Years), 0.0350),
        (ql.Period(2, ql.Years), 0.0360),
        (ql.Period(3, ql.Years), 0.0370),
        (ql.Period(5, ql.Years), 0.0390),
        (ql.Period(10, ql.Years), 0.0420),
    ]
    for tenor, rate in swap_rates:
        helpers.append(ql.SwapRateHelper(
            rate, tenor, calendar,
            ql.Annual, ql.Unadjusted,
            ql.Thirty360(ql.Thirty360.BondBasis),
            euribor6m,
        ))

    return helpers


def test_piecewise_loglinear_discount(curve_env):
    """Test PiecewiseLogLinearDiscount bootstrapping."""
    helpers = _build_helpers(
        curve_env["today"], curve_env["calendar"], curve_env["euribor6m"]
    )
    curve = ql.PiecewiseLogLinearDiscount(
        curve_env["today"], helpers, curve_env["day_counter"]
    )
    assert curve is not None

    # Verify basic curve properties
    assert curve.referenceDate() == curve_env["today"]

    # Discount at reference date is 1.0
    assert curve.discount(curve_env["today"]) == pytest.approx(1.0)

    # Discount at 1 year is close to exp(-0.035)
    one_year = curve_env["today"] + ql.Period(1, ql.Years)
    df_1y = curve.discount(one_year)
    assert 0.9 < df_1y < 1.0

    # Zero rate at 5 years should be close to input
    five_years = curve_env["today"] + ql.Period(5, ql.Years)
    zero_5y = curve.zeroRate(
        five_years, curve_env["day_counter"], ql.Continuous
    )
    assert zero_5y.rate() == pytest.approx(0.039, abs=0.005)


def test_piecewise_loglinear_discount_nodes(curve_env):
    """Test PiecewiseLogLinearDiscount node inspection."""
    helpers = _build_helpers(
        curve_env["today"], curve_env["calendar"], curve_env["euribor6m"]
    )
    curve = ql.PiecewiseLogLinearDiscount(
        curve_env["today"], helpers, curve_env["day_counter"]
    )

    nodes = curve.nodes()
    assert len(nodes) > 0
    # First node should be at reference date with discount 1.0
    assert nodes[0][1] == pytest.approx(1.0)

    dates = curve.dates()
    assert len(dates) == len(nodes)

    times = curve.times()
    assert len(times) == len(nodes)
    assert times[0] == pytest.approx(0.0)

    data = curve.data()
    assert len(data) == len(nodes)
    assert data[0] == pytest.approx(1.0)


def test_piecewise_linear_zero(curve_env):
    """Test PiecewiseLinearZero bootstrapping."""
    helpers = _build_helpers(
        curve_env["today"], curve_env["calendar"], curve_env["euribor6m"]
    )
    curve = ql.PiecewiseLinearZero(
        curve_env["today"], helpers, curve_env["day_counter"]
    )
    assert curve is not None
    assert curve.discount(curve_env["today"]) == pytest.approx(1.0)

    # Check 10Y zero rate is close to input
    ten_years = curve_env["today"] + ql.Period(10, ql.Years)
    zero_10y = curve.zeroRate(
        ten_years, curve_env["day_counter"], ql.Continuous
    )
    assert zero_10y.rate() == pytest.approx(0.042, abs=0.005)


def test_piecewise_cubic_zero(curve_env):
    """Test PiecewiseCubicZero bootstrapping."""
    helpers = _build_helpers(
        curve_env["today"], curve_env["calendar"], curve_env["euribor6m"]
    )
    curve = ql.PiecewiseCubicZero(
        curve_env["today"], helpers, curve_env["day_counter"]
    )
    assert curve is not None
    assert curve.discount(curve_env["today"]) == pytest.approx(1.0)


def test_piecewise_flat_forward(curve_env):
    """Test PiecewiseFlatForward bootstrapping."""
    helpers = _build_helpers(
        curve_env["today"], curve_env["calendar"], curve_env["euribor6m"]
    )
    curve = ql.PiecewiseFlatForward(
        curve_env["today"], helpers, curve_env["day_counter"]
    )
    assert curve is not None
    assert curve.discount(curve_env["today"]) == pytest.approx(1.0)


def test_piecewise_linear_forward(curve_env):
    """Test PiecewiseLinearForward bootstrapping."""
    helpers = _build_helpers(
        curve_env["today"], curve_env["calendar"], curve_env["euribor6m"]
    )
    curve = ql.PiecewiseLinearForward(
        curve_env["today"], helpers, curve_env["day_counter"]
    )
    assert curve is not None
    assert curve.discount(curve_env["today"]) == pytest.approx(1.0)

    # Check forward rate is reasonable
    five_years = curve_env["today"] + ql.Period(5, ql.Years)
    zero_5y = curve.zeroRate(
        five_years, curve_env["day_counter"], ql.Continuous
    )
    assert zero_5y.rate() == pytest.approx(0.039, abs=0.005)


def test_piecewise_backward_flat_forward(curve_env):
    """Test PiecewiseBackwardFlatForward bootstrapping."""
    helpers = _build_helpers(
        curve_env["today"], curve_env["calendar"], curve_env["euribor6m"]
    )
    curve = ql.PiecewiseBackwardFlatForward(
        curve_env["today"], helpers, curve_env["day_counter"]
    )
    assert curve is not None
    assert curve.discount(curve_env["today"]) == pytest.approx(1.0)


def test_piecewise_linear_discount(curve_env):
    """Test PiecewiseLinearDiscount bootstrapping."""
    helpers = _build_helpers(
        curve_env["today"], curve_env["calendar"], curve_env["euribor6m"]
    )
    curve = ql.PiecewiseLinearDiscount(
        curve_env["today"], helpers, curve_env["day_counter"]
    )
    assert curve is not None
    assert curve.discount(curve_env["today"]) == pytest.approx(1.0)


def test_piecewise_settlement_days_constructor(curve_env):
    """Test PiecewiseYieldCurve with settlement days constructor."""
    helpers = _build_helpers(
        curve_env["today"], curve_env["calendar"], curve_env["euribor6m"]
    )
    curve = ql.PiecewiseLogLinearDiscount(
        2, curve_env["calendar"], helpers, curve_env["day_counter"]
    )
    assert curve is not None
    assert curve.settlementDays() == 2


def test_piecewise_discounts_monotonic(curve_env):
    """Test that bootstrapped discount factors are monotonically decreasing."""
    helpers = _build_helpers(
        curve_env["today"], curve_env["calendar"], curve_env["euribor6m"]
    )
    curve = ql.PiecewiseLogLinearDiscount(
        curve_env["today"], helpers, curve_env["day_counter"]
    )

    prev_df = 1.0
    for years in [1, 2, 3, 5, 10]:
        target = curve_env["today"] + ql.Period(years, ql.Years)
        df = curve.discount(target)
        assert df < prev_df, f"Discount not decreasing at {years}Y"
        prev_df = df


def test_piecewise_forward_rate(curve_env):
    """Test forward rate extraction from bootstrapped curve."""
    helpers = _build_helpers(
        curve_env["today"], curve_env["calendar"], curve_env["euribor6m"]
    )
    curve = ql.PiecewiseFlatForward(
        curve_env["today"], helpers, curve_env["day_counter"]
    )

    date1 = curve_env["today"] + ql.Period(1, ql.Years)
    date2 = curve_env["today"] + ql.Period(2, ql.Years)
    fwd = curve.forwardRate(
        date1, date2, curve_env["day_counter"], ql.Continuous
    )
    # Forward rate between 1Y and 2Y should be positive and reasonable
    assert 0.01 < fwd.rate() < 0.10


def test_piecewise_in_handle(curve_env):
    """Test PiecewiseYieldCurve works in a YieldTermStructureHandle."""
    helpers = _build_helpers(
        curve_env["today"], curve_env["calendar"], curve_env["euribor6m"]
    )
    curve = ql.PiecewiseLogLinearDiscount(
        curve_env["today"], helpers, curve_env["day_counter"]
    )

    handle = ql.YieldTermStructureHandle(curve)
    assert not handle.empty()
    assert handle.currentLink().discount(1.0) == pytest.approx(
        curve.discount(1.0)
    )


def test_piecewise_with_fra_helpers(curve_env):
    """Test PiecewiseYieldCurve with FRA helpers in the mix."""
    helpers = []

    # Deposits
    helpers.append(ql.DepositRateHelper(
        0.032, ql.Period(3, ql.Months), 2,
        curve_env["calendar"], ql.ModifiedFollowing,
        True, ql.Actual360()
    ))

    # FRA
    helpers.append(ql.FraRateHelper(0.034, 3, curve_env["euribor6m"]))
    helpers.append(ql.FraRateHelper(0.036, 6, curve_env["euribor6m"]))

    # Swap
    helpers.append(ql.SwapRateHelper(
        0.040, ql.Period(2, ql.Years), curve_env["calendar"],
        ql.Annual, ql.Unadjusted,
        ql.Thirty360(ql.Thirty360.BondBasis),
        curve_env["euribor6m"],
    ))

    curve = ql.PiecewiseLinearZero(
        curve_env["today"], helpers, curve_env["day_counter"]
    )
    assert curve is not None
    assert curve.discount(curve_env["today"]) == pytest.approx(1.0)
