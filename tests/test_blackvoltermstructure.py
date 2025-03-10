import pytest
import math
import pyquantlib as ql


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


def test_python_custom_blackvoltermstructure():
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


def test_python_custom_blackvoltermstructure_blackvol():
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


def test_python_custom_blackvoltermstructure_variance():
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


def test_python_custom_blackvoltermstructure_forward_vol():
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


def test_relinkable_blackvoltermstructure_handle():
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
