import pytest
import pyquantlib as ql


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


def test_python_custom_volatilitytermstructure():
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
