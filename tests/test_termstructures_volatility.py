"""
Tests for termstructures/volatility module.

Corresponds to src/termstructures/volatility/*.cpp bindings.
"""

import datetime

import pytest

import pyquantlib as ql
from pyquantlib.base import SmileSection, LazyObject


# =============================================================================
# VolatilityTermStructure (ABC)
# =============================================================================


def test_volatilitytermstructure_abc_exists():
    """Verify VolatilityTermStructure is in base submodule."""
    assert hasattr(ql.base, 'VolatilityTermStructure')


def test_volatilitytermstructure_zombie():
    """Direct instantiation creates a zombie that fails on pure virtual calls."""
    ref_date = ql.Date(15, 6, 2024)
    calendar = ql.TARGET()
    bdc = ql.Following
    dc = ql.Actual365Fixed()

    zombie = ql.base.VolatilityTermStructure(ref_date, calendar, bdc, dc)
    assert zombie is not None

    # businessDayConvention is not pure virtual - should work
    assert zombie.businessDayConvention() == bdc

    # maxDate is pure virtual - should fail
    with pytest.raises(RuntimeError, match="Tried to call pure virtual function"):
        zombie.maxDate()


def test_volatilitytermstructure_python_custom():
    """Test Python subclass implementing pure virtual methods."""

    class FlatVolSurface(ql.base.VolatilityTermStructure):
        def __init__(self, reference_date, calendar, bdc, day_counter, flat_vol):
            super().__init__(reference_date, calendar, bdc, day_counter)
            self._flat_vol = flat_vol

        def maxDate(self):
            return ql.Date(31, 12, 2199)

        def minStrike(self):
            return 0.0

        def maxStrike(self):
            return float('inf')

        def update(self):
            pass

    ref_date = ql.Date(15, 6, 2024)
    calendar = ql.TARGET()
    bdc = ql.Following
    dc = ql.Actual365Fixed()

    vol_surface = FlatVolSurface(ref_date, calendar, bdc, dc, 0.20)

    assert vol_surface.referenceDate() == ref_date
    assert vol_surface.calendar().name() == calendar.name()
    assert vol_surface.businessDayConvention() == bdc
    assert vol_surface.dayCounter().name() == dc.name()
    assert vol_surface.maxDate() == ql.Date(31, 12, 2199)
    assert vol_surface.minStrike() == 0.0


def test_volatilitytermstructure_option_date_from_tenor():
    """Test optionDateFromTenor method."""

    class SimpleVolSurface(ql.base.VolatilityTermStructure):
        def __init__(self, reference_date, calendar, bdc, day_counter):
            super().__init__(reference_date, calendar, bdc, day_counter)

        def maxDate(self):
            return ql.Date(31, 12, 2199)

        def minStrike(self):
            return 0.0

        def maxStrike(self):
            return 1000.0

        def update(self):
            pass

    ref_date = ql.Date(15, 6, 2024)
    calendar = ql.TARGET()
    bdc = ql.Following
    dc = ql.Actual365Fixed()

    vol_surface = SimpleVolSurface(ref_date, calendar, bdc, dc)

    # Get option date for 3 month tenor
    tenor = ql.Period(3, ql.Months)
    option_date = vol_surface.optionDateFromTenor(tenor)

    # Should be adjusted according to business day convention
    expected = calendar.advance(ref_date, tenor, bdc)
    assert option_date == expected


def test_volatilitytermstructure_settlement_days_constructor():
    """Test construction with settlement days."""

    class SimpleVolSurface(ql.base.VolatilityTermStructure):
        def __init__(self, settlement_days, calendar, bdc, day_counter):
            super().__init__(settlement_days, calendar, bdc, day_counter)

        def maxDate(self):
            return ql.Date(31, 12, 2199)

        def minStrike(self):
            return 0.0

        def maxStrike(self):
            return 1000.0

        def update(self):
            pass

    calendar = ql.TARGET()
    bdc = ql.Following
    dc = ql.Actual365Fixed()

    vol_surface = SimpleVolSurface(2, calendar, bdc, dc)

    assert vol_surface.settlementDays() == 2
    assert vol_surface.calendar().name() == calendar.name()


# =============================================================================
# BlackVolTermStructure (ABC)
# =============================================================================


def test_blackvoltermstructure_abc_exists():
    """Verify BlackVolTermStructure is in base submodule."""
    assert hasattr(ql.base, 'BlackVolTermStructure')
    assert hasattr(ql.base, 'BlackVolatilityTermStructure')
    assert hasattr(ql.base, 'BlackVarianceTermStructure')


def test_blackvoltermstructure_handles_exist():
    """Verify handle types exist."""
    assert hasattr(ql, 'BlackVolTermStructureHandle')
    assert hasattr(ql, 'RelinkableBlackVolTermStructureHandle')


def test_blackvoltermstructure_handle_empty():
    """Test empty handle behavior."""
    handle = ql.BlackVolTermStructureHandle()
    assert handle.empty()
    assert not handle  # __bool__

    with pytest.raises(ql.Error):
        handle.get()


def test_blackvoltermstructure_python_custom():
    """Test Python subclass implementing pure virtual methods."""

    class FlatBlackVol(ql.base.BlackVolatilityTermStructure):
        def __init__(self, reference_date, calendar, bdc, day_counter, flat_vol):
            super().__init__(reference_date, calendar, bdc, day_counter)
            self._flat_vol = flat_vol

        def maxDate(self):
            return ql.Date(31, 12, 2199)

        def minStrike(self):
            return 0.0

        def maxStrike(self):
            return float('inf')

        def blackVolImpl(self, t, strike):
            return self._flat_vol

        def update(self):
            pass

    ref_date = ql.Date(15, 6, 2024)
    calendar = ql.TARGET()
    bdc = ql.Following
    dc = ql.Actual365Fixed()
    flat_vol = 0.20

    vol_surface = FlatBlackVol(ref_date, calendar, bdc, dc, flat_vol)

    assert vol_surface.referenceDate() == ref_date
    assert vol_surface.maxDate() == ql.Date(31, 12, 2199)
    assert vol_surface.minStrike() == 0.0


def test_blackvoltermstructure_python_blackvol():
    """Test blackVol method dispatches to Python blackVolImpl."""

    class FlatBlackVol(ql.base.BlackVolatilityTermStructure):
        def __init__(self, reference_date, calendar, bdc, day_counter, flat_vol):
            super().__init__(reference_date, calendar, bdc, day_counter)
            self._flat_vol = flat_vol

        def maxDate(self):
            return ql.Date(31, 12, 2199)

        def minStrike(self):
            return 0.0

        def maxStrike(self):
            return 10000.0

        def blackVolImpl(self, t, strike):
            return self._flat_vol

        def update(self):
            pass

    ref_date = ql.Date(15, 6, 2024)
    flat_vol = 0.25

    vol_surface = FlatBlackVol(ref_date, ql.TARGET(), ql.Following,
                                ql.Actual365Fixed(), flat_vol)

    # Test blackVol by date
    future_date = ref_date + ql.Period(1, ql.Years)
    assert vol_surface.blackVol(future_date, 100.0) == pytest.approx(flat_vol)

    # Test blackVol by time
    assert vol_surface.blackVol(1.0, 100.0) == pytest.approx(flat_vol)


def test_blackvoltermstructure_python_variance():
    """Test blackVariance calculation."""

    class FlatBlackVol(ql.base.BlackVolatilityTermStructure):
        def __init__(self, reference_date, calendar, bdc, day_counter, flat_vol):
            super().__init__(reference_date, calendar, bdc, day_counter)
            self._flat_vol = flat_vol

        def maxDate(self):
            return ql.Date(31, 12, 2199)

        def minStrike(self):
            return 0.0

        def maxStrike(self):
            return 10000.0

        def blackVolImpl(self, t, strike):
            return self._flat_vol

        def update(self):
            pass

    ref_date = ql.Date(15, 6, 2024)
    flat_vol = 0.20

    vol_surface = FlatBlackVol(ref_date, ql.TARGET(), ql.Following,
                                ql.Actual365Fixed(), flat_vol)

    # variance = vol^2 * t
    t = 2.0
    expected_variance = flat_vol * flat_vol * t
    assert vol_surface.blackVariance(t, 100.0) == pytest.approx(expected_variance)


def test_blackvoltermstructure_python_forward_vol():
    """Test blackForwardVol calculation."""

    class FlatBlackVol(ql.base.BlackVolatilityTermStructure):
        def __init__(self, reference_date, calendar, bdc, day_counter, flat_vol):
            super().__init__(reference_date, calendar, bdc, day_counter)
            self._flat_vol = flat_vol

        def maxDate(self):
            return ql.Date(31, 12, 2199)

        def minStrike(self):
            return 0.0

        def maxStrike(self):
            return 10000.0

        def blackVolImpl(self, t, strike):
            return self._flat_vol

        def update(self):
            pass

    ref_date = ql.Date(15, 6, 2024)
    flat_vol = 0.20

    vol_surface = FlatBlackVol(ref_date, ql.TARGET(), ql.Following,
                                ql.Actual365Fixed(), flat_vol)

    # For flat vol, forward vol = spot vol
    t1 = 1.0
    t2 = 2.0
    fwd_vol = vol_surface.blackForwardVol(t1, t2, 100.0)
    assert fwd_vol == pytest.approx(flat_vol)


def test_blackvoltermstructure_relinkable_handle():
    """Test relinkable handle functionality."""

    class FlatBlackVol(ql.base.BlackVolatilityTermStructure):
        def __init__(self, reference_date, calendar, bdc, day_counter, flat_vol):
            super().__init__(reference_date, calendar, bdc, day_counter)
            self._flat_vol = flat_vol

        def maxDate(self):
            return ql.Date(31, 12, 2199)

        def minStrike(self):
            return 0.0

        def maxStrike(self):
            return 10000.0

        def blackVolImpl(self, t, strike):
            return self._flat_vol

        def update(self):
            pass

    ref_date = ql.Date(15, 6, 2024)

    vol1 = FlatBlackVol(ref_date, ql.TARGET(), ql.Following, ql.Actual365Fixed(), 0.20)
    vol2 = FlatBlackVol(ref_date, ql.TARGET(), ql.Following, ql.Actual365Fixed(), 0.30)

    handle = ql.RelinkableBlackVolTermStructureHandle(vol1)
    assert handle.currentLink().blackVol(1.0, 100.0) == pytest.approx(0.20)

    handle.linkTo(vol2)
    assert handle.currentLink().blackVol(1.0, 100.0) == pytest.approx(0.30)


# =============================================================================
# BlackConstantVol
# =============================================================================


def test_blackconstantvol_exists():
    """Verify BlackConstantVol is in main module."""
    assert hasattr(ql, 'BlackConstantVol')


def test_blackconstantvol_construction():
    """Test BlackConstantVol construction with reference date."""
    ref_date = ql.Date(15, 6, 2024)
    calendar = ql.TARGET()
    volatility = 0.25
    dc = ql.Actual365Fixed()

    bcv = ql.BlackConstantVol(ref_date, calendar, volatility, dc)

    assert bcv.referenceDate() == ref_date
    assert bcv.dayCounter().name() == dc.name()


def test_blackconstantvol_inheritance():
    """Test BlackConstantVol inheritance hierarchy."""
    ref_date = ql.Date(15, 6, 2024)
    bcv = ql.BlackConstantVol(ref_date, ql.TARGET(), 0.20, ql.Actual365Fixed())

    assert isinstance(bcv, ql.BlackConstantVol)
    assert isinstance(bcv, ql.base.BlackVolTermStructure)
    assert isinstance(bcv, ql.base.VolatilityTermStructure)
    assert isinstance(bcv, ql.base.TermStructure)


def test_blackconstantvol_blackvol():
    """Test blackVol returns constant volatility."""
    ref_date = ql.Date(15, 6, 2024)
    volatility = 0.25
    bcv = ql.BlackConstantVol(ref_date, ql.TARGET(), volatility, ql.Actual365Fixed())

    future_date = ref_date + ql.Period(1, ql.Years)
    strike = 100.0

    assert bcv.blackVol(future_date, strike) == pytest.approx(volatility)
    assert bcv.blackVol(2.0, strike) == pytest.approx(volatility)


def test_blackconstantvol_blackvariance():
    """Test blackVariance calculation."""
    ref_date = ql.Date(15, 6, 2024)
    volatility = 0.20
    dc = ql.Actual365Fixed()
    bcv = ql.BlackConstantVol(ref_date, ql.TARGET(), volatility, dc)

    future_date = ref_date + ql.Period(2, ql.Years)
    time = dc.yearFraction(ref_date, future_date)
    strike = 100.0

    expected_variance = volatility * volatility * time
    assert bcv.blackVariance(future_date, strike) == pytest.approx(expected_variance)


def test_blackconstantvol_with_quote_handle():
    """Test BlackConstantVol with quote handle updates automatically."""
    ref_date = ql.Date(15, 6, 2024)
    dc = ql.Actual365Fixed()

    initial_vol = 0.20
    vol_quote = ql.SimpleQuote(initial_vol)
    vol_handle = ql.QuoteHandle(vol_quote)

    bcv = ql.BlackConstantVol(ref_date, ql.TARGET(), vol_handle, dc)

    strike = 100.0
    assert bcv.blackVol(1.0, strike) == pytest.approx(initial_vol)

    # Change quote value
    new_vol = 0.30
    vol_quote.setValue(new_vol)

    assert bcv.blackVol(1.0, strike) == pytest.approx(new_vol)


def test_blackconstantvol_settlement_days():
    """Test BlackConstantVol construction with settlement days."""
    today = ql.Date(15, 6, 2024)
    ql.Settings.instance().evaluationDate = today

    calendar = ql.TARGET()
    volatility = 0.25
    dc = ql.Actual365Fixed()

    bcv = ql.BlackConstantVol(2, calendar, volatility, dc)

    # Reference date should be 2 business days from evaluation date
    expected_ref = calendar.advance(today, 2, ql.Days)
    assert bcv.referenceDate() == expected_ref


def test_blackconstantvol_in_handle():
    """Test BlackConstantVol works with BlackVolTermStructureHandle."""
    ref_date = ql.Date(15, 6, 2024)
    volatility = 0.25
    bcv = ql.BlackConstantVol(ref_date, ql.TARGET(), volatility, ql.Actual365Fixed())

    handle = ql.BlackVolTermStructureHandle(bcv)
    assert not handle.empty()

    retrieved = handle.currentLink()
    assert retrieved.blackVol(1.0, 100.0) == pytest.approx(volatility)


def test_blackconstantvol_hidden_handle_reference_date():
    """Test BlackConstantVol with Quote (hidden handle) using reference date."""
    ref_date = ql.Date(15, 6, 2024)
    dc = ql.Actual365Fixed()

    vol_quote = ql.SimpleQuote(0.25)
    bcv = ql.BlackConstantVol(ref_date, ql.TARGET(), vol_quote, dc)

    assert bcv.blackVol(1.0, 100.0) == pytest.approx(0.25)

    # Quote changes propagate
    vol_quote.setValue(0.30)
    assert bcv.blackVol(1.0, 100.0) == pytest.approx(0.30)


def test_blackconstantvol_hidden_handle_settlement_days():
    """Test BlackConstantVol with Quote (hidden handle) using settlement days."""
    today = ql.Date(15, 6, 2024)
    ql.Settings.instance().evaluationDate = today

    vol_quote = ql.SimpleQuote(0.20)
    bcv = ql.BlackConstantVol(2, ql.TARGET(), vol_quote, ql.Actual365Fixed())

    expected_ref = ql.TARGET().advance(today, 2, ql.Days)
    assert bcv.referenceDate() == expected_ref
    assert bcv.blackVol(1.0, 100.0) == pytest.approx(0.20)


# =============================================================================
# BlackVarianceSurface
# =============================================================================


@pytest.fixture
def vol_surface_data():
    """Setup common test data for BlackVarianceSurface."""
    ref_date = ql.Date(15, 6, 2024)
    calendar = ql.TARGET()
    dc = ql.Actual365Fixed()

    # Dates (maturities)
    dates = [
        ql.Date(15, 9, 2024),   # 3 months
        ql.Date(15, 12, 2024),  # 6 months
        ql.Date(15, 6, 2025),   # 1 year
        ql.Date(15, 6, 2026),   # 2 years
    ]

    # Strikes
    strikes = [80.0, 90.0, 100.0, 110.0, 120.0]

    # Black volatility matrix: rows = strikes, columns = dates
    vol_matrix = ql.Matrix(5, 4)
    vols = [
        [0.25, 0.24, 0.23, 0.22],  # Strike 80.0
        [0.23, 0.22, 0.21, 0.20],  # Strike 90.0
        [0.21, 0.20, 0.19, 0.18],  # Strike 100.0
        [0.23, 0.22, 0.21, 0.20],  # Strike 110.0
        [0.25, 0.24, 0.23, 0.22],  # Strike 120.0
    ]

    for i in range(5):
        for j in range(4):
            vol_matrix[i][j] = vols[i][j]

    return {
        'ref_date': ref_date,
        'calendar': calendar,
        'dc': dc,
        'dates': dates,
        'strikes': strikes,
        'vol_matrix': vol_matrix,
    }


def test_blackvariancesurface_exists():
    """Verify BlackVarianceSurface is in main module."""
    assert hasattr(ql, 'BlackVarianceSurface')


def test_blackvariancesurface_extrapolation_enum():
    """Test extrapolation enum values are accessible."""
    assert hasattr(ql, 'BlackVarianceSurfaceExtrapolation')

    const_extrap = ql.BlackVarianceSurfaceExtrapolation.ConstantExtrapolation
    interp_extrap = ql.BlackVarianceSurfaceExtrapolation.InterpolatorDefaultExtrapolation

    assert const_extrap is not None
    assert interp_extrap is not None
    assert const_extrap != interp_extrap


def test_blackvariancesurface_construction(vol_surface_data):
    """Test basic construction of BlackVarianceSurface."""
    data = vol_surface_data

    surface = ql.BlackVarianceSurface(
        data['ref_date'],
        data['calendar'],
        data['dates'],
        data['strikes'],
        data['vol_matrix'],
        data['dc']
    )

    assert surface is not None
    assert surface.referenceDate() == data['ref_date']


def test_blackvariancesurface_construction_with_extrapolation(vol_surface_data):
    """Test construction with explicit extrapolation parameters."""
    data = vol_surface_data

    surface = ql.BlackVarianceSurface(
        data['ref_date'],
        data['calendar'],
        data['dates'],
        data['strikes'],
        data['vol_matrix'],
        data['dc'],
        ql.BlackVarianceSurfaceExtrapolation.ConstantExtrapolation,
        ql.BlackVarianceSurfaceExtrapolation.InterpolatorDefaultExtrapolation
    )

    assert surface is not None


def test_blackvariancesurface_inheritance(vol_surface_data):
    """Test BlackVarianceSurface inheritance hierarchy."""
    data = vol_surface_data

    surface = ql.BlackVarianceSurface(
        data['ref_date'],
        data['calendar'],
        data['dates'],
        data['strikes'],
        data['vol_matrix'],
        data['dc']
    )

    assert isinstance(surface, ql.BlackVarianceSurface)
    assert isinstance(surface, ql.base.BlackVolTermStructure)
    assert isinstance(surface, ql.base.VolatilityTermStructure)


def test_blackvariancesurface_strike_range(vol_surface_data):
    """Test minStrike() and maxStrike() methods."""
    data = vol_surface_data

    surface = ql.BlackVarianceSurface(
        data['ref_date'],
        data['calendar'],
        data['dates'],
        data['strikes'],
        data['vol_matrix'],
        data['dc']
    )

    assert surface.minStrike() == data['strikes'][0]   # 80.0
    assert surface.maxStrike() == data['strikes'][-1]  # 120.0


def test_blackvariancesurface_blackvol_at_grid(vol_surface_data):
    """Test blackVol at grid points."""
    data = vol_surface_data
    ql.Settings.instance().evaluationDate = data['ref_date']

    surface = ql.BlackVarianceSurface(
        data['ref_date'],
        data['calendar'],
        data['dates'],
        data['strikes'],
        data['vol_matrix'],
        data['dc']
    )

    # strikes[2] = 100.0, dates[1] = 6M date
    # vol_matrix[2][1] = 0.20
    vol = surface.blackVol(data['dates'][1], data['strikes'][2])
    assert vol == pytest.approx(0.20)


def test_blackvariancesurface_blackvariance(vol_surface_data):
    """Test blackVariance calculation."""
    data = vol_surface_data
    ql.Settings.instance().evaluationDate = data['ref_date']

    surface = ql.BlackVarianceSurface(
        data['ref_date'],
        data['calendar'],
        data['dates'],
        data['strikes'],
        data['vol_matrix'],
        data['dc']
    )

    time_to_maturity = data['dc'].yearFraction(data['ref_date'], data['dates'][1])
    variance = surface.blackVariance(time_to_maturity, data['strikes'][2])

    # Variance = vol^2 * time
    expected_variance = 0.20 ** 2 * time_to_maturity
    assert variance == pytest.approx(expected_variance)


def test_blackvariancesurface_set_interpolation(vol_surface_data):
    """Test setInterpolation method."""
    data = vol_surface_data
    ql.Settings.instance().evaluationDate = data['ref_date']

    surface = ql.BlackVarianceSurface(
        data['ref_date'],
        data['calendar'],
        data['dates'],
        data['strikes'],
        data['vol_matrix'],
        data['dc']
    )

    off_grid_strike = 95.0

    # Set bicubic interpolation
    surface.setInterpolation("bicubic")
    vol_bicubic = surface.blackVol(data['dates'][1], off_grid_strike)

    # Set bilinear interpolation
    surface.setInterpolation("bilinear")
    vol_bilinear = surface.blackVol(data['dates'][1], off_grid_strike)

    # Both should work, values may differ
    assert vol_bicubic > 0
    assert vol_bilinear > 0

    # At grid point, both should give same result
    vol_at_grid = surface.blackVol(data['dates'][1], data['strikes'][2])
    assert vol_at_grid == pytest.approx(0.20)


def test_blackvariancesurface_in_handle(vol_surface_data):
    """Test BlackVarianceSurface works with BlackVolTermStructureHandle."""
    data = vol_surface_data
    ql.Settings.instance().evaluationDate = data['ref_date']

    surface = ql.BlackVarianceSurface(
        data['ref_date'],
        data['calendar'],
        data['dates'],
        data['strikes'],
        data['vol_matrix'],
        data['dc']
    )

    handle = ql.BlackVolTermStructureHandle(surface)
    assert not handle.empty()

    retrieved = handle.currentLink()
    vol = retrieved.blackVol(data['dates'][1], 100.0)
    assert vol == pytest.approx(0.20)


# =============================================================================
# LocalVolTermStructure (ABC)
# =============================================================================


def test_localvoltermstructure_abc_exists():
    """Verify LocalVolTermStructure is in base submodule."""
    assert hasattr(ql.base, 'LocalVolTermStructure')


def test_localvoltermstructure_handles_exist():
    """Verify handle types exist."""
    assert hasattr(ql, 'LocalVolTermStructureHandle')
    assert hasattr(ql, 'RelinkableLocalVolTermStructureHandle')


def test_localvoltermstructure_handle_empty():
    """Test empty handle behavior."""
    handle = ql.LocalVolTermStructureHandle()
    assert handle.empty()
    assert not handle  # __bool__

    with pytest.raises(ql.Error):
        handle.get()


def test_localvoltermstructure_python_custom():
    """Test Python subclass implementing pure virtual methods."""

    class FlatLocalVol(ql.base.LocalVolTermStructure):
        def __init__(self, reference_date, calendar, bdc, day_counter, flat_vol):
            super().__init__(reference_date, calendar, bdc, day_counter)
            self._flat_vol = flat_vol

        def maxDate(self):
            return ql.Date(31, 12, 2199)

        def minStrike(self):
            return 0.0

        def maxStrike(self):
            return float('inf')

        def localVolImpl(self, t, strike):
            return self._flat_vol

        def update(self):
            pass

    ref_date = ql.Date(15, 6, 2024)
    calendar = ql.TARGET()
    bdc = ql.Following
    dc = ql.Actual365Fixed()
    flat_vol = 0.20

    vol_surface = FlatLocalVol(ref_date, calendar, bdc, dc, flat_vol)

    assert vol_surface.referenceDate() == ref_date
    assert vol_surface.maxDate() == ql.Date(31, 12, 2199)
    assert vol_surface.minStrike() == 0.0


def test_localvoltermstructure_python_localvol():
    """Test localVol method dispatches to Python localVolImpl."""

    class FlatLocalVol(ql.base.LocalVolTermStructure):
        def __init__(self, reference_date, calendar, bdc, day_counter, flat_vol):
            super().__init__(reference_date, calendar, bdc, day_counter)
            self._flat_vol = flat_vol

        def maxDate(self):
            return ql.Date(31, 12, 2199)

        def minStrike(self):
            return 0.0

        def maxStrike(self):
            return 10000.0

        def localVolImpl(self, t, strike):
            return self._flat_vol

        def update(self):
            pass

    ref_date = ql.Date(15, 6, 2024)
    flat_vol = 0.25

    vol_surface = FlatLocalVol(ref_date, ql.TARGET(), ql.Following,
                               ql.Actual365Fixed(), flat_vol)

    # Test localVol by date
    future_date = ref_date + ql.Period(1, ql.Years)
    assert vol_surface.localVol(future_date, 100.0) == pytest.approx(flat_vol)

    # Test localVol by time
    assert vol_surface.localVol(1.0, 100.0) == pytest.approx(flat_vol)


def test_localvoltermstructure_python_strike_dependent():
    """Test localVol with strike-dependent volatility."""

    class SkewedLocalVol(ql.base.LocalVolTermStructure):
        def __init__(self, reference_date, calendar, bdc, day_counter, atm_vol, skew):
            super().__init__(reference_date, calendar, bdc, day_counter)
            self._atm_vol = atm_vol
            self._skew = skew
            self._atm_strike = 100.0

        def maxDate(self):
            return ql.Date(31, 12, 2199)

        def minStrike(self):
            return 0.0

        def maxStrike(self):
            return 10000.0

        def localVolImpl(self, t, strike):
            # Simple linear skew
            return self._atm_vol + self._skew * (strike - self._atm_strike) / 100.0

        def update(self):
            pass

    ref_date = ql.Date(15, 6, 2024)
    atm_vol = 0.20
    skew = -0.02  # Negative skew

    vol_surface = SkewedLocalVol(ref_date, ql.TARGET(), ql.Following,
                                  ql.Actual365Fixed(), atm_vol, skew)

    # At-the-money
    assert vol_surface.localVol(1.0, 100.0) == pytest.approx(atm_vol)

    # Out-of-the-money put (higher vol)
    assert vol_surface.localVol(1.0, 80.0) == pytest.approx(atm_vol + skew * (-20.0) / 100.0)

    # Out-of-the-money call (lower vol)
    assert vol_surface.localVol(1.0, 120.0) == pytest.approx(atm_vol + skew * 20.0 / 100.0)


def test_localvoltermstructure_relinkable_handle():
    """Test relinkable handle functionality."""

    class FlatLocalVol(ql.base.LocalVolTermStructure):
        def __init__(self, reference_date, calendar, bdc, day_counter, flat_vol):
            super().__init__(reference_date, calendar, bdc, day_counter)
            self._flat_vol = flat_vol

        def maxDate(self):
            return ql.Date(31, 12, 2199)

        def minStrike(self):
            return 0.0

        def maxStrike(self):
            return 10000.0

        def localVolImpl(self, t, strike):
            return self._flat_vol

        def update(self):
            pass

    ref_date = ql.Date(15, 6, 2024)

    vol1 = FlatLocalVol(ref_date, ql.TARGET(), ql.Following, ql.Actual365Fixed(), 0.20)
    vol2 = FlatLocalVol(ref_date, ql.TARGET(), ql.Following, ql.Actual365Fixed(), 0.30)

    handle = ql.RelinkableLocalVolTermStructureHandle(vol1)
    assert handle.currentLink().localVol(1.0, 100.0) == pytest.approx(0.20)

    handle.linkTo(vol2)
    assert handle.currentLink().localVol(1.0, 100.0) == pytest.approx(0.30)


# =============================================================================
# LocalConstantVol
# =============================================================================


def test_localconstantvol_exists():
    """Verify LocalConstantVol is in main module."""
    assert hasattr(ql, 'LocalConstantVol')


def test_localconstantvol_construction():
    """Test LocalConstantVol construction with reference date."""
    ref_date = ql.Date(15, 6, 2024)
    volatility = 0.25
    dc = ql.Actual365Fixed()

    lcv = ql.LocalConstantVol(ref_date, volatility, dc)

    assert lcv.referenceDate() == ref_date
    assert lcv.dayCounter().name() == dc.name()


def test_localconstantvol_inheritance():
    """Test LocalConstantVol inheritance hierarchy."""
    ref_date = ql.Date(15, 6, 2024)
    lcv = ql.LocalConstantVol(ref_date, 0.20, ql.Actual365Fixed())

    assert isinstance(lcv, ql.LocalConstantVol)
    assert isinstance(lcv, ql.base.LocalVolTermStructure)
    assert isinstance(lcv, ql.base.VolatilityTermStructure)
    assert isinstance(lcv, ql.base.TermStructure)


def test_localconstantvol_localvol():
    """Test localVol returns constant volatility."""
    ref_date = ql.Date(15, 6, 2024)
    volatility = 0.25
    lcv = ql.LocalConstantVol(ref_date, volatility, ql.Actual365Fixed())

    future_date = ref_date + ql.Period(1, ql.Years)
    underlying = 100.0

    assert lcv.localVol(future_date, underlying) == pytest.approx(volatility)
    assert lcv.localVol(2.0, underlying) == pytest.approx(volatility)


def test_localconstantvol_strike_independent():
    """Test localVol is independent of underlying level."""
    ref_date = ql.Date(15, 6, 2024)
    volatility = 0.20
    lcv = ql.LocalConstantVol(ref_date, volatility, ql.Actual365Fixed())

    # Same vol for different underlying levels
    assert lcv.localVol(1.0, 50.0) == pytest.approx(volatility)
    assert lcv.localVol(1.0, 100.0) == pytest.approx(volatility)
    assert lcv.localVol(1.0, 200.0) == pytest.approx(volatility)


def test_localconstantvol_with_quote_handle():
    """Test LocalConstantVol with quote handle updates automatically."""
    ref_date = ql.Date(15, 6, 2024)
    dc = ql.Actual365Fixed()

    initial_vol = 0.20
    vol_quote = ql.SimpleQuote(initial_vol)
    vol_handle = ql.QuoteHandle(vol_quote)

    lcv = ql.LocalConstantVol(ref_date, vol_handle, dc)

    underlying = 100.0
    assert lcv.localVol(1.0, underlying) == pytest.approx(initial_vol)

    # Change quote value
    new_vol = 0.30
    vol_quote.setValue(new_vol)

    assert lcv.localVol(1.0, underlying) == pytest.approx(new_vol)


def test_localconstantvol_settlement_days():
    """Test LocalConstantVol construction with settlement days."""
    today = ql.Date(15, 6, 2024)
    ql.Settings.instance().evaluationDate = today

    calendar = ql.TARGET()
    volatility = 0.25
    dc = ql.Actual365Fixed()

    lcv = ql.LocalConstantVol(2, calendar, volatility, dc)

    # Reference date should be 2 business days from evaluation date
    expected_ref = calendar.advance(today, 2, ql.Days)
    assert lcv.referenceDate() == expected_ref


def test_localconstantvol_in_handle():
    """Test LocalConstantVol works with LocalVolTermStructureHandle."""
    ref_date = ql.Date(15, 6, 2024)
    volatility = 0.25
    lcv = ql.LocalConstantVol(ref_date, volatility, ql.Actual365Fixed())

    handle = ql.LocalVolTermStructureHandle(lcv)
    assert not handle.empty()

    retrieved = handle.currentLink()
    assert retrieved.localVol(1.0, 100.0) == pytest.approx(volatility)


def test_localconstantvol_hidden_handle_reference_date():
    """Test LocalConstantVol with Quote (hidden handle) using reference date."""
    ref_date = ql.Date(15, 6, 2024)
    dc = ql.Actual365Fixed()

    vol_quote = ql.SimpleQuote(0.25)
    lcv = ql.LocalConstantVol(ref_date, vol_quote, dc)

    assert lcv.localVol(1.0, 100.0) == pytest.approx(0.25)

    # Quote changes propagate
    vol_quote.setValue(0.30)
    assert lcv.localVol(1.0, 100.0) == pytest.approx(0.30)


def test_localconstantvol_hidden_handle_settlement_days():
    """Test LocalConstantVol with Quote (hidden handle) using settlement days."""
    today = ql.Date(15, 6, 2024)
    ql.Settings.instance().evaluationDate = today

    vol_quote = ql.SimpleQuote(0.20)
    lcv = ql.LocalConstantVol(2, ql.TARGET(), vol_quote, ql.Actual365Fixed())

    expected_ref = ql.TARGET().advance(today, 2, ql.Days)
    assert lcv.referenceDate() == expected_ref
    assert lcv.localVol(1.0, 100.0) == pytest.approx(0.20)


# =============================================================================
# LocalVolSurface
# =============================================================================


def test_localvolsurface_exists():
    """Verify LocalVolSurface is in main module."""
    assert hasattr(ql, 'LocalVolSurface')


def test_localvolsurface_construction():
    """Test LocalVolSurface construction from Black vol surface."""
    ref_date = ql.Date(15, 6, 2024)
    ql.Settings.instance().evaluationDate = ref_date
    dc = ql.Actual365Fixed()
    calendar = ql.TARGET()

    # Create underlying term structures
    spot = 100.0
    risk_free_rate = 0.05
    dividend_yield = 0.02
    black_vol = 0.20

    spot_quote = ql.SimpleQuote(spot)
    risk_free = ql.FlatForward(ref_date, risk_free_rate, dc)
    dividend = ql.FlatForward(ref_date, dividend_yield, dc)
    black_vol_surface = ql.BlackConstantVol(ref_date, calendar, black_vol, dc)

    spot_handle = ql.QuoteHandle(spot_quote)
    risk_free_handle = ql.YieldTermStructureHandle(risk_free)
    dividend_handle = ql.YieldTermStructureHandle(dividend)
    black_vol_handle = ql.BlackVolTermStructureHandle(black_vol_surface)

    lvs = ql.LocalVolSurface(black_vol_handle, risk_free_handle,
                              dividend_handle, spot_handle)

    assert lvs.referenceDate() == ref_date


def test_localvolsurface_inheritance():
    """Test LocalVolSurface inheritance hierarchy."""
    ref_date = ql.Date(15, 6, 2024)
    ql.Settings.instance().evaluationDate = ref_date
    dc = ql.Actual365Fixed()

    risk_free = ql.FlatForward(ref_date, 0.05, dc)
    dividend = ql.FlatForward(ref_date, 0.02, dc)
    black_vol = ql.BlackConstantVol(ref_date, ql.TARGET(), 0.20, dc)

    lvs = ql.LocalVolSurface(
        ql.BlackVolTermStructureHandle(black_vol),
        ql.YieldTermStructureHandle(risk_free),
        ql.YieldTermStructureHandle(dividend),
        100.0
    )

    assert isinstance(lvs, ql.LocalVolSurface)
    assert isinstance(lvs, ql.base.LocalVolTermStructure)
    assert isinstance(lvs, ql.base.VolatilityTermStructure)


def test_localvolsurface_flat_vol():
    """Test local vol equals Black vol for constant Black vol surface."""
    ref_date = ql.Date(15, 6, 2024)
    ql.Settings.instance().evaluationDate = ref_date
    dc = ql.Actual365Fixed()
    calendar = ql.TARGET()

    black_vol = 0.20
    risk_free = ql.FlatForward(ref_date, 0.05, dc)
    dividend = ql.FlatForward(ref_date, 0.02, dc)
    black_vol_surface = ql.BlackConstantVol(ref_date, calendar, black_vol, dc)

    lvs = ql.LocalVolSurface(
        ql.BlackVolTermStructureHandle(black_vol_surface),
        ql.YieldTermStructureHandle(risk_free),
        ql.YieldTermStructureHandle(dividend),
        100.0
    )

    # For flat Black vol, local vol equals Black vol
    future_date = ref_date + ql.Period(1, ql.Years)
    assert lvs.localVol(future_date, 100.0) == pytest.approx(black_vol)


def test_localvolsurface_updates_with_quote():
    """Test LocalVolSurface updates when Black vol quote changes."""
    ref_date = ql.Date(15, 6, 2024)
    ql.Settings.instance().evaluationDate = ref_date
    dc = ql.Actual365Fixed()
    calendar = ql.TARGET()

    initial_vol = 0.20
    vol_quote = ql.SimpleQuote(initial_vol)
    vol_handle = ql.QuoteHandle(vol_quote)

    risk_free = ql.FlatForward(ref_date, 0.05, dc)
    dividend = ql.FlatForward(ref_date, 0.02, dc)
    black_vol_surface = ql.BlackConstantVol(ref_date, calendar, vol_handle, dc)

    lvs = ql.LocalVolSurface(
        ql.BlackVolTermStructureHandle(black_vol_surface),
        ql.YieldTermStructureHandle(risk_free),
        ql.YieldTermStructureHandle(dividend),
        100.0
    )

    future_date = ref_date + ql.Period(1, ql.Years)
    assert lvs.localVol(future_date, 100.0) == pytest.approx(initial_vol)

    # Change vol quote
    new_vol = 0.25
    vol_quote.setValue(new_vol)
    assert lvs.localVol(future_date, 100.0) == pytest.approx(new_vol)


def test_localvolsurface_with_fixed_underlying():
    """Test LocalVolSurface construction with fixed underlying value."""
    ref_date = ql.Date(15, 6, 2024)
    ql.Settings.instance().evaluationDate = ref_date
    dc = ql.Actual365Fixed()

    risk_free = ql.FlatForward(ref_date, 0.05, dc)
    dividend = ql.FlatForward(ref_date, 0.02, dc)
    black_vol = ql.BlackConstantVol(ref_date, ql.TARGET(), 0.20, dc)

    # Use fixed Real value instead of quote handle
    lvs = ql.LocalVolSurface(
        ql.BlackVolTermStructureHandle(black_vol),
        ql.YieldTermStructureHandle(risk_free),
        ql.YieldTermStructureHandle(dividend),
        100.0  # Fixed underlying
    )

    assert lvs is not None
    assert lvs.localVol(1.0, 100.0) == pytest.approx(0.20)


def test_localvolsurface_in_handle():
    """Test LocalVolSurface works with LocalVolTermStructureHandle."""
    ref_date = ql.Date(15, 6, 2024)
    ql.Settings.instance().evaluationDate = ref_date
    dc = ql.Actual365Fixed()

    risk_free = ql.FlatForward(ref_date, 0.05, dc)
    dividend = ql.FlatForward(ref_date, 0.02, dc)
    black_vol = ql.BlackConstantVol(ref_date, ql.TARGET(), 0.20, dc)

    lvs = ql.LocalVolSurface(
        ql.BlackVolTermStructureHandle(black_vol),
        ql.YieldTermStructureHandle(risk_free),
        ql.YieldTermStructureHandle(dividend),
        100.0
    )

    handle = ql.LocalVolTermStructureHandle(lvs)
    assert not handle.empty()

    retrieved = handle.currentLink()
    assert retrieved.localVol(1.0, 100.0) == pytest.approx(0.20)


def test_localvolsurface_hidden_handles_with_quote():
    """Test LocalVolSurface with term structures (hidden handles) and quote."""
    ref_date = ql.Date(15, 6, 2024)
    ql.Settings.instance().evaluationDate = ref_date
    dc = ql.Actual365Fixed()

    spot_quote = ql.SimpleQuote(100.0)
    risk_free = ql.FlatForward(ref_date, 0.05, dc)
    dividend = ql.FlatForward(ref_date, 0.02, dc)
    black_vol = ql.BlackConstantVol(ref_date, ql.TARGET(), 0.20, dc)

    # Hidden handles: pass term structures directly
    lvs = ql.LocalVolSurface(black_vol, risk_free, dividend, spot_quote)

    assert lvs.localVol(1.0, 100.0) == pytest.approx(0.20)

    # Quote changes propagate
    spot_quote.setValue(110.0)
    # Local vol should still work (may differ slightly due to spot change)
    assert lvs.localVol(1.0, 100.0) == pytest.approx(0.20, rel=0.01)


def test_localvolsurface_hidden_handles_with_fixed_value():
    """Test LocalVolSurface with term structures (hidden handles) and fixed value."""
    ref_date = ql.Date(15, 6, 2024)
    ql.Settings.instance().evaluationDate = ref_date
    dc = ql.Actual365Fixed()

    risk_free = ql.FlatForward(ref_date, 0.05, dc)
    dividend = ql.FlatForward(ref_date, 0.02, dc)
    black_vol = ql.BlackConstantVol(ref_date, ql.TARGET(), 0.20, dc)

    # Hidden handles with fixed underlying value
    lvs = ql.LocalVolSurface(black_vol, risk_free, dividend, 100.0)

    assert lvs.localVol(1.0, 100.0) == pytest.approx(0.20)


# =============================================================================
# FixedLocalVolSurface
# =============================================================================


def test_fixedlocalvolsurface_exists():
    """Verify FixedLocalVolSurface is in main module."""
    assert hasattr(ql, 'FixedLocalVolSurface')


def test_fixedlocalvolsurface_extrapolation_enum():
    """Test extrapolation enum values are accessible."""
    assert hasattr(ql, 'FixedLocalVolExtrapolation')

    const_extrap = ql.FixedLocalVolExtrapolation.ConstantExtrapolation
    interp_extrap = ql.FixedLocalVolExtrapolation.InterpolatorDefaultExtrapolation

    assert const_extrap is not None
    assert interp_extrap is not None
    assert const_extrap != interp_extrap


def test_fixedlocalvolsurface_with_dates():
    """Test FixedLocalVolSurface construction with dates."""
    ref_date = ql.Date(15, 6, 2024)
    ql.Settings.instance().evaluationDate = ref_date
    dc = ql.Actual365Fixed()

    dates = [
        ref_date + ql.Period(1, ql.Months),
        ref_date + ql.Period(3, ql.Months),
        ref_date + ql.Period(6, ql.Months),
        ref_date + ql.Period(1, ql.Years)
    ]

    strikes = [90.0, 100.0, 110.0, 120.0]

    # Matrix: rows = strikes, columns = time points
    local_vol_data = [
        [0.25, 0.24, 0.23, 0.22],  # Strike 90
        [0.23, 0.22, 0.21, 0.20],  # Strike 100
        [0.22, 0.21, 0.20, 0.19],  # Strike 110
        [0.24, 0.23, 0.22, 0.21]   # Strike 120
    ]
    local_vol_matrix = ql.Matrix(local_vol_data)

    flvs = ql.FixedLocalVolSurface(
        ref_date, dates, strikes, local_vol_matrix, dc,
        ql.FixedLocalVolExtrapolation.ConstantExtrapolation,
        ql.FixedLocalVolExtrapolation.ConstantExtrapolation
    )

    assert isinstance(flvs, ql.base.LocalVolTermStructure)
    assert flvs.referenceDate() == ref_date
    assert flvs.maxDate() > ref_date
    assert flvs.minStrike() == pytest.approx(min(strikes))
    assert flvs.maxStrike() == pytest.approx(max(strikes))


def test_fixedlocalvolsurface_with_times():
    """Test FixedLocalVolSurface construction with times."""
    ref_date = ql.Date(15, 6, 2024)
    ql.Settings.instance().evaluationDate = ref_date
    dc = ql.Actual365Fixed()

    times = [0.25, 0.5, 1.0, 2.0]  # years
    strikes = [80.0, 90.0, 100.0, 110.0, 120.0]

    local_vol_data = [
        [0.26, 0.25, 0.24, 0.23],  # Strike 80
        [0.24, 0.23, 0.22, 0.21],  # Strike 90
        [0.23, 0.22, 0.21, 0.20],  # Strike 100
        [0.24, 0.23, 0.22, 0.21],  # Strike 110
        [0.25, 0.24, 0.23, 0.22]   # Strike 120
    ]
    local_vol_matrix = ql.Matrix(local_vol_data)

    flvs = ql.FixedLocalVolSurface(
        ref_date, times, strikes, local_vol_matrix, dc
    )

    assert isinstance(flvs, ql.base.LocalVolTermStructure)

    # Test local vol at grid point
    # times[1] = 0.5, strikes[2] = 100.0 -> matrix[2][1] = 0.22
    assert flvs.localVol(0.5, 100.0) == pytest.approx(0.22)


def test_fixedlocalvolsurface_with_varying_strikes():
    """Test FixedLocalVolSurface with different strikes per time point."""
    ref_date = ql.Date(15, 6, 2024)
    ql.Settings.instance().evaluationDate = ref_date
    dc = ql.Actual365Fixed()

    times = [0.25, 0.5, 1.0]

    # Different strikes for each time point
    strikes_per_time = [
        [90.0, 100.0, 110.0],   # 0.25 years
        [85.0, 95.0, 105.0],   # 0.5 years
        [80.0, 90.0, 100.0]    # 1.0 years
    ]

    local_vol_data = [
        [0.25, 0.26, 0.27],  # Row 0
        [0.23, 0.24, 0.25],  # Row 1
        [0.22, 0.23, 0.24]   # Row 2
    ]
    local_vol_matrix = ql.Matrix(local_vol_data)

    flvs = ql.FixedLocalVolSurface(
        ref_date, times, strikes_per_time, local_vol_matrix, dc,
        ql.FixedLocalVolExtrapolation.InterpolatorDefaultExtrapolation,
        ql.FixedLocalVolExtrapolation.InterpolatorDefaultExtrapolation
    )

    assert isinstance(flvs, ql.base.LocalVolTermStructure)

    # Test at grid point: time=0.5, strike=95.0 -> matrix[1][1] = 0.24
    assert flvs.localVol(0.5, 95.0) == pytest.approx(0.24)


def test_fixedlocalvolsurface_inheritance():
    """Test FixedLocalVolSurface inheritance hierarchy."""
    ref_date = ql.Date(15, 6, 2024)
    ql.Settings.instance().evaluationDate = ref_date
    dc = ql.Actual365Fixed()

    times = [0.5]
    strikes = [100.0, 110.0]
    local_vol_matrix = ql.Matrix([[0.22], [0.21]])

    flvs = ql.FixedLocalVolSurface(
        ref_date, times, strikes, local_vol_matrix, dc
    )

    assert isinstance(flvs, ql.FixedLocalVolSurface)
    assert isinstance(flvs, ql.base.LocalVolTermStructure)
    assert isinstance(flvs, ql.base.VolatilityTermStructure)


def test_fixedlocalvolsurface_in_handle():
    """Test FixedLocalVolSurface works with LocalVolTermStructureHandle."""
    ref_date = ql.Date(15, 6, 2024)
    ql.Settings.instance().evaluationDate = ref_date
    dc = ql.Actual365Fixed()

    times = [0.5, 1.0]
    strikes = [100.0, 110.0]
    local_vol_matrix = ql.Matrix([[0.22, 0.21], [0.21, 0.20]])

    flvs = ql.FixedLocalVolSurface(
        ref_date, times, strikes, local_vol_matrix, dc
    )

    handle = ql.LocalVolTermStructureHandle(flvs)
    assert not handle.empty()

    retrieved = handle.currentLink()
    assert retrieved.localVol(0.5, 100.0) == pytest.approx(0.22)


# =============================================================================
# NoExceptLocalVolSurface
# =============================================================================


def test_noexceptlocalvolsurface_exists():
    """Verify NoExceptLocalVolSurface is in main module."""
    assert hasattr(ql, 'NoExceptLocalVolSurface')


def test_noexceptlocalvolsurface_construction():
    """Test NoExceptLocalVolSurface construction."""
    ref_date = ql.Date(15, 6, 2024)
    ql.Settings.instance().evaluationDate = ref_date
    dc = ql.Actual365Fixed()
    calendar = ql.TARGET()

    # Create underlying term structures
    spot = 100.0
    risk_free_rate = 0.05
    dividend_yield = 0.02
    black_vol = 0.20
    fallback_vol = 0.15

    spot_quote = ql.SimpleQuote(spot)
    risk_free = ql.FlatForward(ref_date, risk_free_rate, dc)
    dividend = ql.FlatForward(ref_date, dividend_yield, dc)
    black_vol_surface = ql.BlackConstantVol(ref_date, calendar, black_vol, dc)

    spot_handle = ql.QuoteHandle(spot_quote)
    risk_free_handle = ql.YieldTermStructureHandle(risk_free)
    dividend_handle = ql.YieldTermStructureHandle(dividend)
    black_vol_handle = ql.BlackVolTermStructureHandle(black_vol_surface)

    nelvs = ql.NoExceptLocalVolSurface(
        black_vol_handle, risk_free_handle, dividend_handle,
        spot_handle, fallback_vol
    )

    assert nelvs.referenceDate() == ref_date


def test_noexceptlocalvolsurface_inheritance():
    """Test NoExceptLocalVolSurface inheritance hierarchy."""
    ref_date = ql.Date(15, 6, 2024)
    ql.Settings.instance().evaluationDate = ref_date
    dc = ql.Actual365Fixed()

    risk_free = ql.FlatForward(ref_date, 0.05, dc)
    dividend = ql.FlatForward(ref_date, 0.02, dc)
    black_vol = ql.BlackConstantVol(ref_date, ql.TARGET(), 0.20, dc)

    nelvs = ql.NoExceptLocalVolSurface(
        ql.BlackVolTermStructureHandle(black_vol),
        ql.YieldTermStructureHandle(risk_free),
        ql.YieldTermStructureHandle(dividend),
        100.0, 0.15
    )

    assert isinstance(nelvs, ql.NoExceptLocalVolSurface)
    assert isinstance(nelvs, ql.LocalVolSurface)
    assert isinstance(nelvs, ql.base.LocalVolTermStructure)


def test_noexceptlocalvolsurface_localvol():
    """Test local vol calculation with fallback."""
    ref_date = ql.Date(15, 6, 2024)
    ql.Settings.instance().evaluationDate = ref_date
    dc = ql.Actual365Fixed()
    calendar = ql.TARGET()

    black_vol = 0.20
    fallback_vol = 0.15

    risk_free = ql.FlatForward(ref_date, 0.05, dc)
    dividend = ql.FlatForward(ref_date, 0.02, dc)
    black_vol_surface = ql.BlackConstantVol(ref_date, calendar, black_vol, dc)

    nelvs = ql.NoExceptLocalVolSurface(
        ql.BlackVolTermStructureHandle(black_vol_surface),
        ql.YieldTermStructureHandle(risk_free),
        ql.YieldTermStructureHandle(dividend),
        100.0, fallback_vol
    )

    # For flat Black vol, local vol equals Black vol
    future_date = ref_date + ql.Period(1, ql.Years)
    vol = nelvs.localVol(future_date, 100.0)
    assert vol == pytest.approx(black_vol)


def test_noexceptlocalvolsurface_with_quote_handle():
    """Test NoExceptLocalVolSurface with quote handle for underlying."""
    ref_date = ql.Date(15, 6, 2024)
    ql.Settings.instance().evaluationDate = ref_date
    dc = ql.Actual365Fixed()

    spot_quote = ql.SimpleQuote(100.0)
    risk_free = ql.FlatForward(ref_date, 0.05, dc)
    dividend = ql.FlatForward(ref_date, 0.02, dc)
    black_vol = ql.BlackConstantVol(ref_date, ql.TARGET(), 0.20, dc)

    nelvs = ql.NoExceptLocalVolSurface(
        ql.BlackVolTermStructureHandle(black_vol),
        ql.YieldTermStructureHandle(risk_free),
        ql.YieldTermStructureHandle(dividend),
        ql.QuoteHandle(spot_quote),
        0.15
    )

    assert nelvs is not None
    assert nelvs.localVol(1.0, 100.0) == pytest.approx(0.20)


def test_noexceptlocalvolsurface_in_handle():
    """Test NoExceptLocalVolSurface works with LocalVolTermStructureHandle."""
    ref_date = ql.Date(15, 6, 2024)
    ql.Settings.instance().evaluationDate = ref_date
    dc = ql.Actual365Fixed()

    risk_free = ql.FlatForward(ref_date, 0.05, dc)
    dividend = ql.FlatForward(ref_date, 0.02, dc)
    black_vol = ql.BlackConstantVol(ref_date, ql.TARGET(), 0.20, dc)

    nelvs = ql.NoExceptLocalVolSurface(
        ql.BlackVolTermStructureHandle(black_vol),
        ql.YieldTermStructureHandle(risk_free),
        ql.YieldTermStructureHandle(dividend),
        100.0, 0.15
    )

    handle = ql.LocalVolTermStructureHandle(nelvs)
    assert not handle.empty()

    retrieved = handle.currentLink()
    assert retrieved.localVol(1.0, 100.0) == pytest.approx(0.20)


def test_noexceptlocalvolsurface_hidden_handles_with_quote():
    """Test NoExceptLocalVolSurface with term structures (hidden handles) and quote."""
    ref_date = ql.Date(15, 6, 2024)
    ql.Settings.instance().evaluationDate = ref_date
    dc = ql.Actual365Fixed()

    spot_quote = ql.SimpleQuote(100.0)
    risk_free = ql.FlatForward(ref_date, 0.05, dc)
    dividend = ql.FlatForward(ref_date, 0.02, dc)
    black_vol = ql.BlackConstantVol(ref_date, ql.TARGET(), 0.20, dc)

    # Hidden handles: pass term structures directly
    nelvs = ql.NoExceptLocalVolSurface(black_vol, risk_free, dividend, spot_quote, 0.15)

    assert nelvs.localVol(1.0, 100.0) == pytest.approx(0.20)


def test_noexceptlocalvolsurface_hidden_handles_with_fixed_value():
    """Test NoExceptLocalVolSurface with term structures (hidden handles) and fixed value."""
    ref_date = ql.Date(15, 6, 2024)
    ql.Settings.instance().evaluationDate = ref_date
    dc = ql.Actual365Fixed()

    risk_free = ql.FlatForward(ref_date, 0.05, dc)
    dividend = ql.FlatForward(ref_date, 0.02, dc)
    black_vol = ql.BlackConstantVol(ref_date, ql.TARGET(), 0.20, dc)

    # Hidden handles with fixed underlying value
    nelvs = ql.NoExceptLocalVolSurface(black_vol, risk_free, dividend, 100.0, 0.15)

    assert nelvs.localVol(1.0, 100.0) == pytest.approx(0.20)


# =============================================================================
# SABR Formula Free Functions
# =============================================================================


def test_sabrvolatility_atm():
    """Test SABR formula at the ATM forward."""
    alpha, beta, nu, rho = 0.05, 0.5, 0.4, -0.1
    forward = 0.03
    T = 1.0
    vol = ql.sabrVolatility(forward, forward, T, alpha, beta, nu, rho)
    assert vol > 0.0
    assert vol == pytest.approx(0.29230, rel=1e-3)


def test_sabrvolatility_otm():
    """Test SABR formula for out-of-the-money strikes."""
    alpha, beta, nu, rho = 0.05, 0.5, 0.4, -0.1
    forward = 0.03
    T = 1.0
    vol_low = ql.sabrVolatility(0.01, forward, T, alpha, beta, nu, rho)
    vol_atm = ql.sabrVolatility(forward, forward, T, alpha, beta, nu, rho)
    vol_high = ql.sabrVolatility(0.05, forward, T, alpha, beta, nu, rho)
    # SABR with negative rho produces a skew
    assert vol_low > vol_atm  # downside skew
    assert vol_high > 0.0


def test_shiftedsabrvolatility():
    """Test shifted SABR formula."""
    alpha, beta, nu, rho = 0.05, 0.5, 0.4, -0.1
    forward = 0.03
    T = 1.0
    shift = 0.02
    vol = ql.shiftedSabrVolatility(forward, forward, T, alpha, beta, nu, rho, shift)
    assert vol > 0.0


def test_validatesabrparameters_valid():
    """Test SABR parameter validation with valid params."""
    ql.validateSabrParameters(0.05, 0.5, 0.4, -0.1)


def test_validatesabrparameters_invalid():
    """Test SABR parameter validation with invalid params."""
    with pytest.raises(ql.Error):
        ql.validateSabrParameters(-0.05, 0.5, 0.4, -0.1)  # negative alpha
    with pytest.raises(ql.Error):
        ql.validateSabrParameters(0.05, 0.5, -0.4, -0.1)  # negative nu
    with pytest.raises(ql.Error):
        ql.validateSabrParameters(0.05, 0.5, 0.4, -1.5)  # |rho| > 1


# =============================================================================
# SabrSmileSection
# =============================================================================


def test_sabrsmilesection_time_constructor():
    """Test SabrSmileSection construction from exercise time."""
    params = [0.05, 0.5, 0.4, -0.1]  # alpha, beta, nu, rho
    section = ql.SabrSmileSection(1.0, 0.03, params)
    assert section is not None
    assert isinstance(section, SmileSection)
    assert section.exerciseTime() == pytest.approx(1.0)


def test_sabrsmilesection_date_constructor():
    """Test SabrSmileSection construction from expiry date."""
    ql.Settings.evaluationDate = datetime.date(2025, 1, 15)
    params = [0.05, 0.5, 0.4, -0.1]
    section = ql.SabrSmileSection(
        ql.Date(15, 7, 2025), 0.03, params
    )
    assert section is not None
    assert section.exerciseTime() > 0.0


def test_sabrsmilesection_volatility():
    """Test SabrSmileSection volatility computation."""
    params = [0.05, 0.5, 0.4, -0.1]
    forward = 0.03
    section = ql.SabrSmileSection(1.0, forward, params)
    vol_atm = section.volatility(forward)
    assert vol_atm > 0.0
    assert vol_atm == pytest.approx(0.29230, rel=1e-3)


def test_sabrsmilesection_accessors():
    """Test SabrSmileSection parameter accessors."""
    alpha, beta, nu, rho = 0.05, 0.5, 0.4, -0.1
    section = ql.SabrSmileSection(1.0, 0.03, [alpha, beta, nu, rho])
    assert section.alpha() == pytest.approx(alpha)
    assert section.beta() == pytest.approx(beta)
    assert section.nu() == pytest.approx(nu)
    assert section.rho() == pytest.approx(rho)


def test_sabrsmilesection_smile_shape():
    """Test SabrSmileSection produces expected smile shape."""
    params = [0.05, 0.5, 0.4, -0.1]
    forward = 0.03
    section = ql.SabrSmileSection(1.0, forward, params)
    vol_low = section.volatility(0.01)
    vol_atm = section.volatility(forward)
    vol_high = section.volatility(0.05)
    # Negative rho -> downside skew
    assert vol_low > vol_atm


def test_sabrsmilesection_shifted():
    """Test SabrSmileSection with shift."""
    params = [0.05, 0.5, 0.4, -0.1]
    section = ql.SabrSmileSection(1.0, 0.03, params, shift=0.02)
    vol = section.volatility(0.03)
    assert vol > 0.0


def test_sabrsmilesection_consistency_with_formula():
    """Test SabrSmileSection matches sabrVolatility free function."""
    alpha, beta, nu, rho = 0.05, 0.5, 0.4, -0.1
    forward = 0.03
    T = 1.0
    section = ql.SabrSmileSection(T, forward, [alpha, beta, nu, rho])
    strike = 0.025
    vol_section = section.volatility(strike)
    vol_formula = ql.sabrVolatility(strike, forward, T, alpha, beta, nu, rho)
    assert vol_section == pytest.approx(vol_formula, rel=1e-6)


# =============================================================================
# SabrInterpolatedSmileSection
# =============================================================================


@pytest.fixture
def sabr_market_data():
    """Market data for SABR interpolation tests."""
    ql.Settings.evaluationDate = datetime.date(2025, 1, 15)
    return {
        "optionDate": ql.Date(15, 7, 2025),
        "forward": 0.03,
        "strikes": [0.01, 0.02, 0.025, 0.03, 0.035, 0.04, 0.05],
        "vols": [0.30, 0.22, 0.19, 0.18, 0.185, 0.20, 0.25],
    }


def test_sabrinterpolatedsmilesection_construction(sabr_market_data):
    """Test SabrInterpolatedSmileSection construction and calibration."""
    d = sabr_market_data
    section = ql.SabrInterpolatedSmileSection(
        d["optionDate"], d["forward"], d["strikes"],
        hasFloatingStrikes=False,
        atmVolatility=0.18,
        vols=d["vols"],
        alpha=0.05, beta=0.5, nu=0.4, rho=-0.1
    )
    assert section is not None


def test_sabrinterpolatedsmilesection_isinstance(sabr_market_data):
    """Test SabrInterpolatedSmileSection inheritance checks."""
    d = sabr_market_data
    section = ql.SabrInterpolatedSmileSection(
        d["optionDate"], d["forward"], d["strikes"],
        False, 0.18, d["vols"],
        0.05, 0.5, 0.4, -0.1
    )
    assert isinstance(section, SmileSection)
    assert isinstance(section, LazyObject)


def test_sabrinterpolatedsmilesection_calibration(sabr_market_data):
    """Test SabrInterpolatedSmileSection calibration results."""
    d = sabr_market_data
    section = ql.SabrInterpolatedSmileSection(
        d["optionDate"], d["forward"], d["strikes"],
        False, 0.18, d["vols"],
        0.05, 0.5, 0.4, -0.1
    )
    section.recalculate()
    # Calibrated parameters should be reasonable
    assert 0.0 < section.alpha() < 1.0
    assert 0.0 <= section.beta() <= 1.0
    assert section.nu() >= 0.0
    assert -1.0 <= section.rho() <= 1.0
    # Calibration should have small error
    assert section.rmsError() < 0.05
    assert section.maxError() < 0.1


def test_sabrinterpolatedsmilesection_volatility(sabr_market_data):
    """Test calibrated volatility at market strikes."""
    d = sabr_market_data
    section = ql.SabrInterpolatedSmileSection(
        d["optionDate"], d["forward"], d["strikes"],
        False, 0.18, d["vols"],
        0.05, 0.5, 0.4, -0.1
    )
    section.recalculate()
    # Calibrated vol at ATM should be close to market ATM vol
    vol_atm = section.volatility(d["forward"])
    assert vol_atm == pytest.approx(d["vols"][3], abs=0.02)


def test_sabrinterpolatedsmilesection_fixed_beta(sabr_market_data):
    """Test calibration with fixed beta."""
    d = sabr_market_data
    section = ql.SabrInterpolatedSmileSection(
        d["optionDate"], d["forward"], d["strikes"],
        False, 0.18, d["vols"],
        0.05, 0.5, 0.4, -0.1,
        isBetaFixed=True
    )
    section.recalculate()
    assert section.beta() == pytest.approx(0.5)


def test_sabrinterpolatedsmilesection_lazyobject_methods(sabr_market_data):
    """Test LazyObject methods (recalculate, freeze, unfreeze)."""
    d = sabr_market_data
    section = ql.SabrInterpolatedSmileSection(
        d["optionDate"], d["forward"], d["strikes"],
        False, 0.18, d["vols"],
        0.05, 0.5, 0.4, -0.1
    )
    section.recalculate()
    alpha1 = section.alpha()
    # Freeze and recalculate should give same result
    section.freeze()
    section.recalculate()
    assert section.alpha() == pytest.approx(alpha1)
    # Unfreeze
    section.unfreeze()


def test_sabrinterpolatedsmilesection_endcriteria(sabr_market_data):
    """Test end criteria reporting after calibration."""
    d = sabr_market_data
    section = ql.SabrInterpolatedSmileSection(
        d["optionDate"], d["forward"], d["strikes"],
        False, 0.18, d["vols"],
        0.05, 0.5, 0.4, -0.1
    )
    section.recalculate()
    ec = section.endCriteria()
    assert ec is not None


def test_sabrinterpolatedsmilesection_smilesection_methods(sabr_market_data):
    """Test inherited SmileSection methods."""
    d = sabr_market_data
    section = ql.SabrInterpolatedSmileSection(
        d["optionDate"], d["forward"], d["strikes"],
        False, 0.18, d["vols"],
        0.05, 0.5, 0.4, -0.1
    )
    section.recalculate()
    # SmileSection methods
    assert section.exerciseTime() > 0.0
    assert section.volatility(0.03) > 0.0
    assert section.variance(0.03) > 0.0
    price = section.optionPrice(0.03)
    assert price >= 0.0


# =============================================================================
# SwaptionVolatilityStructure (ABC)
# =============================================================================


def test_swaptionvolstructure_abc_exists():
    """Test SwaptionVolatilityStructure ABC is accessible."""
    assert hasattr(ql.base, "SwaptionVolatilityStructure")


def test_swaptionvolstructure_handle_types():
    """Test swaption vol handle and relinkable handle types exist."""
    assert hasattr(ql, "SwaptionVolatilityStructureHandle")
    assert hasattr(ql, "RelinkableSwaptionVolatilityStructureHandle")


# =============================================================================
# ConstantSwaptionVolatility
# =============================================================================


@pytest.fixture(scope="module")
def swaption_vol_env():
    """Common data for swaption volatility tests."""
    original_date = ql.Settings.instance().evaluationDate
    today = ql.Date(15, ql.January, 2025)
    ql.Settings.instance().evaluationDate = today
    yield {
        "today": today,
        "calendar": ql.TARGET(),
        "dc": ql.Actual365Fixed(),
    }
    ql.Settings.instance().evaluationDate = original_date


def test_constantswaptionvol_construction(swaption_vol_env):
    """Test ConstantSwaptionVolatility construction."""
    d = swaption_vol_env
    vol = ql.ConstantSwaptionVolatility(
        2, d["calendar"], ql.ModifiedFollowing, 0.20, d["dc"]
    )
    assert vol is not None
    assert vol.volatilityType() == ql.VolatilityType.ShiftedLognormal


def test_constantswaptionvol_query(swaption_vol_env):
    """Test querying ConstantSwaptionVolatility."""
    d = swaption_vol_env
    vol = ql.ConstantSwaptionVolatility(
        2, d["calendar"], ql.ModifiedFollowing, 0.20, d["dc"]
    )
    # Query volatility for 1Y option, 5Y swap
    v = vol.volatility(ql.Period("1Y"), ql.Period("5Y"), 0.03)
    assert v == pytest.approx(0.20, abs=1e-12)


def test_constantswaptionvol_handle(swaption_vol_env):
    """Test ConstantSwaptionVolatility with handle."""
    d = swaption_vol_env
    vol = ql.ConstantSwaptionVolatility(
        2, d["calendar"], ql.ModifiedFollowing, 0.20, d["dc"]
    )
    handle = ql.SwaptionVolatilityStructureHandle(vol)
    assert not handle.empty()


def test_constantswaptionvol_relinkable_handle(swaption_vol_env):
    """Test relinkable swaption vol handle."""
    d = swaption_vol_env
    vol1 = ql.ConstantSwaptionVolatility(
        2, d["calendar"], ql.ModifiedFollowing, 0.20, d["dc"]
    )
    vol2 = ql.ConstantSwaptionVolatility(
        2, d["calendar"], ql.ModifiedFollowing, 0.30, d["dc"]
    )
    handle = ql.RelinkableSwaptionVolatilityStructureHandle(vol1)
    v1 = handle.get().volatility(ql.Period("1Y"), ql.Period("5Y"), 0.03)
    handle.linkTo(vol2)
    v2 = handle.get().volatility(ql.Period("1Y"), ql.Period("5Y"), 0.03)
    assert v1 == pytest.approx(0.20, abs=1e-12)
    assert v2 == pytest.approx(0.30, abs=1e-12)


# =============================================================================
# SwaptionVolatilityMatrix
# =============================================================================


def test_swaptionvolmatrix_construction(swaption_vol_env):
    """Test SwaptionVolatilityMatrix construction from Matrix."""
    d = swaption_vol_env
    option_tenors = [ql.Period("1Y"), ql.Period("2Y"), ql.Period("5Y")]
    swap_tenors = [ql.Period("2Y"), ql.Period("5Y"), ql.Period("10Y")]
    vols = ql.Matrix(3, 3)
    for i in range(3):
        for j in range(3):
            vols[i][j] = 0.20 + 0.01 * i - 0.005 * j
    matrix = ql.SwaptionVolatilityMatrix(
        d["calendar"], ql.ModifiedFollowing,
        option_tenors, swap_tenors, vols, d["dc"]
    )
    assert matrix is not None
    assert len(matrix.optionTenors()) == 3
    assert len(matrix.swapTenors()) == 3


def test_swaptionvolmatrix_query(swaption_vol_env):
    """Test querying SwaptionVolatilityMatrix."""
    d = swaption_vol_env
    option_tenors = [ql.Period("1Y"), ql.Period("5Y")]
    swap_tenors = [ql.Period("5Y"), ql.Period("10Y")]
    vols = ql.Matrix(2, 2)
    vols[0][0] = 0.20
    vols[0][1] = 0.18
    vols[1][0] = 0.22
    vols[1][1] = 0.19
    matrix = ql.SwaptionVolatilityMatrix(
        d["calendar"], ql.ModifiedFollowing,
        option_tenors, swap_tenors, vols, d["dc"]
    )
    v = matrix.volatility(ql.Period("1Y"), ql.Period("5Y"), 0.03)
    assert v == pytest.approx(0.20, abs=1e-10)


# =============================================================================
# OptionletVolatilityStructure (ABC)
# =============================================================================


def test_optionletvolstructure_abc_exists():
    """Test OptionletVolatilityStructure ABC is accessible."""
    assert hasattr(ql.base, "OptionletVolatilityStructure")


def test_optionletvolstructure_handle_types():
    """Test optionlet vol handle types exist."""
    assert hasattr(ql, "OptionletVolatilityStructureHandle")
    assert hasattr(ql, "RelinkableOptionletVolatilityStructureHandle")


# =============================================================================
# ConstantOptionletVolatility
# =============================================================================


def test_constantoptionletvol_construction(swaption_vol_env):
    """Test ConstantOptionletVolatility construction."""
    d = swaption_vol_env
    vol = ql.ConstantOptionletVolatility(
        2, d["calendar"], ql.ModifiedFollowing, 0.20, d["dc"]
    )
    assert vol is not None
    assert vol.volatilityType() == ql.VolatilityType.ShiftedLognormal


def test_constantoptionletvol_query(swaption_vol_env):
    """Test querying ConstantOptionletVolatility."""
    d = swaption_vol_env
    vol = ql.ConstantOptionletVolatility(
        2, d["calendar"], ql.ModifiedFollowing, 0.20, d["dc"]
    )
    v = vol.volatility(ql.Period("1Y"), 0.03)
    assert v == pytest.approx(0.20, abs=1e-12)


def test_constantoptionletvol_handle(swaption_vol_env):
    """Test ConstantOptionletVolatility with handle."""
    d = swaption_vol_env
    vol = ql.ConstantOptionletVolatility(
        2, d["calendar"], ql.ModifiedFollowing, 0.20, d["dc"]
    )
    handle = ql.OptionletVolatilityStructureHandle(vol)
    assert not handle.empty()


# =============================================================================
# CapFloorTermVolatilityStructure (ABC)
# =============================================================================


def test_capfloortermvolstructure_abc_exists():
    """Test CapFloorTermVolatilityStructure ABC is accessible."""
    assert hasattr(ql.base, "CapFloorTermVolatilityStructure")


# =============================================================================
# CapFloorTermVolSurface
# =============================================================================


@pytest.fixture(scope="module")
def capfloor_vol_env():
    """Common data for cap/floor volatility tests."""
    original_date = ql.Settings.instance().evaluationDate
    today = ql.Date(15, ql.January, 2025)
    ql.Settings.instance().evaluationDate = today

    calendar = ql.TARGET()
    dc = ql.Actual365Fixed()

    option_tenors = [ql.Period("1Y"), ql.Period("2Y"), ql.Period("3Y"),
                     ql.Period("5Y")]
    strikes = [0.01, 0.02, 0.03, 0.04, 0.05]

    # Build a 4x5 volatility matrix (tenors x strikes)
    vols = ql.Matrix(4, 5)
    vol_data = [
        [0.25, 0.22, 0.20, 0.22, 0.25],  # 1Y
        [0.24, 0.21, 0.19, 0.21, 0.24],  # 2Y
        [0.23, 0.20, 0.18, 0.20, 0.23],  # 3Y
        [0.22, 0.19, 0.17, 0.19, 0.22],  # 5Y
    ]
    for i in range(4):
        for j in range(5):
            vols[i][j] = vol_data[i][j]

    surface = ql.CapFloorTermVolSurface(
        2, calendar, ql.ModifiedFollowing,
        option_tenors, strikes, vols, dc
    )

    yield {
        "today": today,
        "calendar": calendar,
        "dc": dc,
        "option_tenors": option_tenors,
        "strikes": strikes,
        "vols": vols,
        "surface": surface,
    }
    ql.Settings.instance().evaluationDate = original_date


def test_capfloortermvolsurface_construction(capfloor_vol_env):
    """Test CapFloorTermVolSurface construction."""
    surface = capfloor_vol_env["surface"]
    assert surface is not None


def test_capfloortermvolsurface_inspectors(capfloor_vol_env):
    """Test CapFloorTermVolSurface inspector methods."""
    surface = capfloor_vol_env["surface"]
    assert len(surface.optionTenors()) == 4
    assert len(surface.strikes()) == 5
    assert len(surface.optionDates()) == 4
    assert len(surface.optionTimes()) == 4


def test_capfloortermvolsurface_volatility(capfloor_vol_env):
    """Test CapFloorTermVolSurface volatility query."""
    surface = capfloor_vol_env["surface"]
    # Query at a grid point: 1Y tenor, 0.03 strike
    v = surface.volatility(ql.Period("1Y"), 0.03, True)
    assert v == pytest.approx(0.20, abs=1e-4)


def test_capfloortermvolsurface_strike_range(capfloor_vol_env):
    """Test CapFloorTermVolSurface strike range."""
    surface = capfloor_vol_env["surface"]
    assert surface.minStrike() == pytest.approx(0.01)
    assert surface.maxStrike() == pytest.approx(0.05)


# =============================================================================
# StrippedOptionletBase (ABC)
# =============================================================================


def test_strippedoptionletbase_abc_exists():
    """Test StrippedOptionletBase ABC is accessible."""
    assert hasattr(ql.base, "StrippedOptionletBase")


# =============================================================================
# OptionletStripper (ABC)
# =============================================================================


def test_optionletstripper_abc_exists():
    """Test OptionletStripper ABC is accessible."""
    assert hasattr(ql.base, "OptionletStripper")


# =============================================================================
# OptionletStripper1
# =============================================================================


@pytest.fixture(scope="module")
def optionlet_strip_env():
    """Common data for optionlet stripping tests."""
    original_date = ql.Settings.instance().evaluationDate
    today = ql.Date(15, ql.January, 2025)
    ql.Settings.instance().evaluationDate = today

    calendar = ql.TARGET()
    dc = ql.Actual365Fixed()

    # Yield curve
    flat_rate = ql.FlatForward(today, 0.03, dc)
    ts_handle = ql.YieldTermStructureHandle(flat_rate)

    # Ibor index
    index = ql.Euribor(ql.Period("6M"), ts_handle)

    # Cap/floor vol surface
    option_tenors = [ql.Period("1Y"), ql.Period("2Y"), ql.Period("3Y"),
                     ql.Period("5Y")]
    strikes = [0.01, 0.02, 0.03, 0.04, 0.05]

    vols = ql.Matrix(4, 5)
    vol_data = [
        [0.25, 0.22, 0.20, 0.22, 0.25],
        [0.24, 0.21, 0.19, 0.21, 0.24],
        [0.23, 0.20, 0.18, 0.20, 0.23],
        [0.22, 0.19, 0.17, 0.19, 0.22],
    ]
    for i in range(4):
        for j in range(5):
            vols[i][j] = vol_data[i][j]

    surface = ql.CapFloorTermVolSurface(
        2, calendar, ql.ModifiedFollowing,
        option_tenors, strikes, vols, dc
    )

    yield {
        "today": today,
        "calendar": calendar,
        "dc": dc,
        "ts_handle": ts_handle,
        "index": index,
        "surface": surface,
    }
    ql.Settings.instance().evaluationDate = original_date


def test_optionletstripper1_construction(optionlet_strip_env):
    """Test OptionletStripper1 construction."""
    d = optionlet_strip_env
    stripper = ql.OptionletStripper1(
        d["surface"], d["index"],
        accuracy=1e-6, maxIter=100, discount=d["ts_handle"]
    )
    assert stripper is not None


def test_optionletstripper1_results(optionlet_strip_env):
    """Test OptionletStripper1 produces stripping results."""
    d = optionlet_strip_env
    stripper = ql.OptionletStripper1(
        d["surface"], d["index"],
        discount=d["ts_handle"]
    )
    # Access results (triggers lazy calculation)
    n = stripper.optionletMaturities()
    assert n > 0

    dates = stripper.optionletFixingDates()
    assert len(dates) == n

    times = stripper.optionletFixingTimes()
    assert len(times) == n

    for i in range(n):
        strikes_i = stripper.optionletStrikes(i)
        vols_i = stripper.optionletVolatilities(i)
        assert len(strikes_i) > 0
        assert len(vols_i) == len(strikes_i)
        # Volatilities should be positive
        for v in vols_i:
            assert v > 0


def test_optionletstripper1_matrices(optionlet_strip_env):
    """Test OptionletStripper1 matrix accessors."""
    d = optionlet_strip_env
    stripper = ql.OptionletStripper1(
        d["surface"], d["index"],
        discount=d["ts_handle"]
    )
    capfloor_prices = stripper.capFloorPrices()
    assert capfloor_prices.rows() > 0
    assert capfloor_prices.columns() > 0

    optionlet_prices = stripper.optionletPrices()
    assert optionlet_prices.rows() > 0

    caplet_vols = stripper.capletVols()
    assert caplet_vols.rows() > 0


def test_optionletstripper1_base_class_methods(optionlet_strip_env):
    """Test OptionletStripper base class methods accessible via OptionletStripper1."""
    d = optionlet_strip_env
    stripper = ql.OptionletStripper1(
        d["surface"], d["index"],
        discount=d["ts_handle"]
    )
    assert len(stripper.optionletFixingTenors()) > 0
    assert len(stripper.optionletPaymentDates()) > 0
    assert len(stripper.optionletAccrualPeriods()) > 0
    assert stripper.termVolSurface() is not None
    assert stripper.iborIndex() is not None
    assert stripper.volatilityType() == ql.VolatilityType.ShiftedLognormal
    assert stripper.displacement() == pytest.approx(0.0)


def test_optionletstripper1_hidden_handle(optionlet_strip_env):
    """Test OptionletStripper1 with shared_ptr discount (hidden handle)."""
    d = optionlet_strip_env
    flat_rate = ql.FlatForward(d["today"], 0.03, d["dc"])
    stripper = ql.OptionletStripper1(
        d["surface"], d["index"],
        discount=flat_rate
    )
    assert stripper.optionletMaturities() > 0


# =============================================================================
# StrippedOptionletAdapter
# =============================================================================


def test_strippedoptionletadapter_construction(optionlet_strip_env):
    """Test StrippedOptionletAdapter construction from stripper."""
    d = optionlet_strip_env
    stripper = ql.OptionletStripper1(
        d["surface"], d["index"],
        discount=d["ts_handle"]
    )
    adapter = ql.StrippedOptionletAdapter(stripper)
    assert adapter is not None


def test_strippedoptionletadapter_volatility(optionlet_strip_env):
    """Test StrippedOptionletAdapter volatility query."""
    d = optionlet_strip_env
    stripper = ql.OptionletStripper1(
        d["surface"], d["index"],
        discount=d["ts_handle"]
    )
    adapter = ql.StrippedOptionletAdapter(stripper)
    # Query volatility at a point within the surface
    vol = adapter.volatility(ql.Period("1Y"), 0.03)
    assert vol > 0
    assert vol < 1.0  # reasonable vol range


def test_strippedoptionletadapter_properties(optionlet_strip_env):
    """Test StrippedOptionletAdapter properties."""
    d = optionlet_strip_env
    stripper = ql.OptionletStripper1(
        d["surface"], d["index"],
        discount=d["ts_handle"]
    )
    adapter = ql.StrippedOptionletAdapter(stripper)
    assert adapter.maxDate() > d["today"]
    assert adapter.minStrike() > 0
    assert adapter.maxStrike() > adapter.minStrike()
    assert adapter.volatilityType() == ql.VolatilityType.ShiftedLognormal
    assert adapter.displacement() == pytest.approx(0.0)


def test_strippedoptionletadapter_handle(optionlet_strip_env):
    """Test StrippedOptionletAdapter works with OptionletVolatilityStructureHandle."""
    d = optionlet_strip_env
    stripper = ql.OptionletStripper1(
        d["surface"], d["index"],
        discount=d["ts_handle"]
    )
    adapter = ql.StrippedOptionletAdapter(stripper)
    handle = ql.OptionletVolatilityStructureHandle(adapter)
    assert not handle.empty()
