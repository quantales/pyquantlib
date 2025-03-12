import pytest
import pyquantlib as ql


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


def test_python_custom_localvoltermstructure():
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


def test_python_custom_localvoltermstructure_localvol():
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


def test_python_custom_localvoltermstructure_strike_dependent():
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


def test_relinkable_localvoltermstructure_handle():
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
