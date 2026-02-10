"""
Tests for yield term structure bindings.

Corresponds to src/termstructures/yield/*.cpp bindings.
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


# =============================================================================
# ZeroCurve
# =============================================================================


@pytest.fixture(scope="module")
def curve_data():
    """Common data for interpolated yield curve tests."""
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


# =============================================================================
# BondHelper
# =============================================================================


def test_bondhelper_construction(curve_env):
    """Test BondHelper construction with a pre-built bond."""
    today = curve_env["today"]
    calendar = curve_env["calendar"]

    schedule = ql.Schedule(
        today, today + ql.Period("5Y"),
        ql.Period(ql.Annual), calendar,
        ql.Unadjusted, ql.Unadjusted,
        ql.DateGeneration.Backward, False,
    )
    bond = ql.FixedRateBond(3, 100.0, schedule, [0.04],
                            ql.Thirty360(ql.Thirty360.BondBasis))

    price = ql.SimpleQuote(101.0)
    helper = ql.BondHelper(price, bond)

    assert helper.bond() is not None
    assert helper.priceType() == ql.BondPriceType.Clean


def test_bondhelper_dirty_price(curve_env):
    """Test BondHelper with Dirty price type."""
    today = curve_env["today"]
    calendar = curve_env["calendar"]

    schedule = ql.Schedule(
        today, today + ql.Period("3Y"),
        ql.Period(ql.Annual), calendar,
        ql.Unadjusted, ql.Unadjusted,
        ql.DateGeneration.Backward, False,
    )
    bond = ql.FixedRateBond(3, 100.0, schedule, [0.03],
                            ql.Thirty360(ql.Thirty360.BondBasis))

    price = ql.SimpleQuote(100.5)
    helper = ql.BondHelper(price, bond, ql.BondPriceType.Dirty)

    assert helper.priceType() == ql.BondPriceType.Dirty


# =============================================================================
# FixedRateBondHelper
# =============================================================================


def test_fixedratebondhelper_construction(curve_env):
    """Test FixedRateBondHelper construction with scalar price."""
    today = curve_env["today"]
    calendar = curve_env["calendar"]

    schedule = ql.Schedule(
        today, today + ql.Period("5Y"),
        ql.Period(ql.Annual), calendar,
        ql.Unadjusted, ql.Unadjusted,
        ql.DateGeneration.Backward, False,
    )
    helper = ql.FixedRateBondHelper(
        101.0, 3, 100.0, schedule, [0.04],
        ql.Thirty360(ql.Thirty360.BondBasis),
    )

    assert helper.bond() is not None
    assert helper.priceType() == ql.BondPriceType.Clean
    assert helper.pillarDate() > today


def test_fixedratebondhelper_with_quote(curve_env):
    """Test FixedRateBondHelper construction with SimpleQuote."""
    today = curve_env["today"]
    calendar = curve_env["calendar"]

    schedule = ql.Schedule(
        today, today + ql.Period("5Y"),
        ql.Period(ql.Annual), calendar,
        ql.Unadjusted, ql.Unadjusted,
        ql.DateGeneration.Backward, False,
    )
    price = ql.SimpleQuote(101.0)
    helper = ql.FixedRateBondHelper(
        price, 3, 100.0, schedule, [0.04],
        ql.Thirty360(ql.Thirty360.BondBasis),
    )

    assert helper.bond() is not None


def test_fixedratebondhelper_bootstrap(curve_env):
    """Test FixedRateBondHelper in yield curve bootstrap."""
    from datetime import date

    today = curve_env["today"]
    calendar = curve_env["calendar"]
    dc = curve_env["day_counter"]

    def make_bond_helper(price, maturity, coupon):
        sched = ql.Schedule(
            today, maturity,
            ql.Period(ql.Annual), calendar,
            ql.Unadjusted, ql.Unadjusted,
            ql.DateGeneration.Backward, False,
        )
        return ql.FixedRateBondHelper(
            price, 3, 100.0, sched, [coupon],
            ql.Thirty360(ql.Thirty360.BondBasis),
        )

    deposit = ql.DepositRateHelper(
        0.03, ql.Period("6M"), 2, calendar,
        ql.ModifiedFollowing, True, ql.Actual360(),
    )

    bond2y = make_bond_helper(100.5, today + ql.Period("2Y"), 0.035)
    bond5y = make_bond_helper(101.0, today + ql.Period("5Y"), 0.04)
    bond10y = make_bond_helper(99.5, today + ql.Period("10Y"), 0.045)

    helpers = [deposit, bond2y, bond5y, bond10y]
    curve = ql.PiecewiseLogLinearDiscount(today, helpers, dc)

    # Discount factors should be monotonically decreasing
    d2 = curve.discount(today + ql.Period("2Y"))
    d5 = curve.discount(today + ql.Period("5Y"))
    d10 = curve.discount(today + ql.Period("10Y"))

    assert 0 < d10 < d5 < d2 < 1.0

    # 5Y zero rate should be roughly in the 3-5% range
    zero5 = curve.zeroRate(5.0, ql.Continuous).rate()
    assert 0.03 < zero5 < 0.05


# =============================================================================
# FittingMethod (base class)
# =============================================================================


def test_fittingmethod_exists():
    """Test FittingMethod base class exists."""
    assert hasattr(ql.base, "FittingMethod")


# =============================================================================
# Nonlinear Fitting Methods
# =============================================================================


def test_nelsonsiegelfitting_construction():
    """Test NelsonSiegelFitting default construction."""
    method = ql.NelsonSiegelFitting()
    assert method is not None
    assert isinstance(method, ql.base.FittingMethod)


def test_svensonfitting_construction():
    """Test SvenssonFitting default construction."""
    method = ql.SvenssonFitting()
    assert method is not None
    assert isinstance(method, ql.base.FittingMethod)


def test_exponentialsplinesfitting_construction():
    """Test ExponentialSplinesFitting default construction."""
    method = ql.ExponentialSplinesFitting()
    assert method is not None
    assert isinstance(method, ql.base.FittingMethod)


def test_exponentialsplinesfitting_with_kappa():
    """Test ExponentialSplinesFitting with fixed kappa."""
    method = ql.ExponentialSplinesFitting(fixedKappa=0.5)
    assert method is not None


def test_cubicbsplinesfitting_construction():
    """Test CubicBSplinesFitting construction with knot vector."""
    knots = [-30.0, -20.0, 0.0, 5.0, 10.0, 15.0, 20.0, 25.0, 30.0, 40.0, 50.0]
    method = ql.CubicBSplinesFitting(knots)
    assert method is not None
    assert isinstance(method, ql.base.FittingMethod)


def test_simplepolynomialfitting_construction():
    """Test SimplePolynomialFitting construction."""
    method = ql.SimplePolynomialFitting(3)
    assert method is not None
    assert isinstance(method, ql.base.FittingMethod)


def test_spreadfittingmethod_construction(curve_env):
    """Test SpreadFittingMethod construction with explicit handle."""
    inner = ql.NelsonSiegelFitting()
    method = ql.SpreadFittingMethod(inner, curve_env["curve_handle"])
    assert method is not None
    assert isinstance(method, ql.base.FittingMethod)


# =============================================================================
# FittedBondDiscountCurve
# =============================================================================


def _build_bond_helpers(today, calendar):
    """Build bond helpers for FittedBondDiscountCurve tests."""
    helpers = []
    coupons_and_prices = [
        (ql.Period("2Y"), 0.035, 100.5),
        (ql.Period("3Y"), 0.037, 100.8),
        (ql.Period("5Y"), 0.040, 101.2),
        (ql.Period("7Y"), 0.042, 101.0),
        (ql.Period("10Y"), 0.045, 99.5),
    ]
    dc = ql.Thirty360(ql.Thirty360.BondBasis)
    for tenor, coupon, price in coupons_and_prices:
        schedule = ql.Schedule(
            today, today + tenor,
            ql.Period(ql.Annual), calendar,
            ql.Unadjusted, ql.Unadjusted,
            ql.DateGeneration.Backward, False,
        )
        helper = ql.FixedRateBondHelper(price, 3, 100.0, schedule, [coupon], dc)
        helpers.append(helper)
    return helpers


def test_fittedbonddiscountcurve_nelssiegel(curve_env):
    """Test FittedBondDiscountCurve with NelsonSiegel fitting."""
    today = curve_env["today"]
    calendar = curve_env["calendar"]
    dc = curve_env["day_counter"]
    helpers = _build_bond_helpers(today, calendar)

    method = ql.NelsonSiegelFitting()
    curve = ql.FittedBondDiscountCurve(
        today, helpers, dc, method,
    )
    assert curve is not None
    assert curve.referenceDate() == today

    # Discount at reference date is 1.0
    assert curve.discount(today) == pytest.approx(1.0)

    # Discount factors should be positive and less than 1
    df_5y = curve.discount(today + ql.Period("5Y"))
    assert 0.0 < df_5y < 1.0

    assert curve.numberOfBonds() == 5


def test_fittedbonddiscountcurve_svensson(curve_env):
    """Test FittedBondDiscountCurve with Svensson fitting."""
    today = curve_env["today"]
    calendar = curve_env["calendar"]
    dc = curve_env["day_counter"]
    helpers = _build_bond_helpers(today, calendar)

    method = ql.SvenssonFitting()
    curve = ql.FittedBondDiscountCurve(
        today, helpers, dc, method,
    )
    assert curve.discount(today) == pytest.approx(1.0)
    assert curve.numberOfBonds() == 5


def test_fittedbonddiscountcurve_settlement_days(curve_env):
    """Test FittedBondDiscountCurve with settlement days constructor."""
    today = curve_env["today"]
    calendar = curve_env["calendar"]
    dc = curve_env["day_counter"]
    helpers = _build_bond_helpers(today, calendar)

    method = ql.NelsonSiegelFitting()
    curve = ql.FittedBondDiscountCurve(
        0, calendar, helpers, dc, method,
    )
    assert curve is not None
    assert curve.numberOfBonds() == 5


def test_fittedbonddiscountcurve_fitresults(curve_env):
    """Test FittedBondDiscountCurve fitResults access."""
    today = curve_env["today"]
    calendar = curve_env["calendar"]
    dc = curve_env["day_counter"]
    helpers = _build_bond_helpers(today, calendar)

    method = ql.NelsonSiegelFitting()
    curve = ql.FittedBondDiscountCurve(
        today, helpers, dc, method,
    )

    # Force curve evaluation
    curve.discount(1.0)

    results = curve.fitResults()
    assert results is not None
    assert isinstance(results, ql.base.FittingMethod)

    # NelsonSiegel has 4 parameters
    solution = results.solution()
    assert len(solution) == 4

    assert results.numberOfIterations() > 0
    assert results.minimumCostValue() >= 0.0


def test_fittedbonddiscountcurve_discounts_monotonic(curve_env):
    """Test that fitted discount factors are monotonically decreasing."""
    today = curve_env["today"]
    calendar = curve_env["calendar"]
    dc = curve_env["day_counter"]
    helpers = _build_bond_helpers(today, calendar)

    method = ql.NelsonSiegelFitting()
    curve = ql.FittedBondDiscountCurve(
        today, helpers, dc, method,
    )

    prev_df = 1.0
    for years in [1, 2, 3, 5, 7, 10]:
        target = today + ql.Period(years, ql.Years)
        df = curve.discount(target)
        assert df < prev_df, f"Discount not decreasing at {years}Y"
        prev_df = df


def test_fittedbonddiscountcurve_zero_rate(curve_env):
    """Test FittedBondDiscountCurve zero rate extraction."""
    today = curve_env["today"]
    calendar = curve_env["calendar"]
    dc = curve_env["day_counter"]
    helpers = _build_bond_helpers(today, calendar)

    method = ql.NelsonSiegelFitting()
    curve = ql.FittedBondDiscountCurve(
        today, helpers, dc, method,
    )

    # Zero rate at 5 years should be in a reasonable range
    five_years = today + ql.Period(5, ql.Years)
    zero_5y = curve.zeroRate(five_years, dc, ql.Continuous)
    assert 0.02 < zero_5y.rate() < 0.06

