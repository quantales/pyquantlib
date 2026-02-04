"""
Tests for termstructures module.

Corresponds to src/termstructures/*.cpp bindings (excluding volatility).
"""

import math

import pytest

import pyquantlib as ql


# =============================================================================
# TermStructure
# =============================================================================


def test_termstructure_abstract_creates_zombie():
    """Test abstract TermStructure creates zombie object."""
    zombie = ql.base.TermStructure(ql.Actual365Fixed())
    assert zombie is not None

    assert zombie.calendar().empty()
    assert zombie.referenceDate() == ql.Date()

    with pytest.raises(RuntimeError, match="Tried to call pure virtual function"):
        zombie.maxDate()


def test_termstructure_python_inheritance():
    """Test Python subclass implementing TermStructure."""

    class MyTermStructure(ql.base.TermStructure):
        """A concrete implementation of TermStructure in Python."""
        def __init__(self, reference_date, calendar, day_counter):
            super().__init__(reference_date, calendar, day_counter)

        def maxDate(self):
            return self.referenceDate() + ql.Period(30, ql.Years)

        def update(self):
            pass

    ref_date = ql.Date(8, 2, 2025)
    calendar = ql.TARGET()
    day_counter = ql.Actual365Fixed()

    my_ts = MyTermStructure(ref_date, calendar, day_counter)

    assert my_ts.referenceDate() == ref_date
    assert my_ts.dayCounter().name() == day_counter.name()
    assert my_ts.calendar().name() == "TARGET"

    expected_max_date = ref_date + ql.Period(30, ql.Years)
    assert my_ts.maxDate() == expected_max_date

    target_date = ref_date + ql.Period(1, ql.Years)
    assert my_ts.timeFromReference(target_date) == pytest.approx(1.0)


# =============================================================================
# YieldTermStructure
# =============================================================================


def test_yieldtermstructure_abc_exists():
    """Test YieldTermStructure is in base submodule."""
    assert hasattr(ql.base, 'YieldTermStructure')


def test_yieldtermstructure_zombie():
    """Test direct instantiation creates zombie."""
    zombie = ql.base.YieldTermStructure(ql.Actual365Fixed())
    assert zombie is not None

    with pytest.raises(RuntimeError, match="Tried to call pure virtual function"):
        zombie.maxDate()


def test_yieldtermstructure_default_daycounter():
    """Test default dayCounter is Actual365Fixed."""
    zombie = ql.base.YieldTermStructure()
    assert zombie.dayCounter().name() == "Actual/365 (Fixed)"


def test_yieldtermstructure_handle_exists():
    """Test handle types exist."""
    assert hasattr(ql, 'YieldTermStructureHandle')
    assert hasattr(ql, 'RelinkableYieldTermStructureHandle')


def test_yieldtermstructure_python_inheritance():
    """Test Python subclass implementing YieldTermStructure."""

    class FlatYieldCurve(ql.base.YieldTermStructure):
        def __init__(self, reference_date, flat_rate, day_counter):
            super().__init__(reference_date, ql.NullCalendar(), day_counter)
            self._flat_rate = flat_rate
            self._reference_date = reference_date

        def maxDate(self):
            return ql.Date(31, 12, 2199)

        def discountImpl(self, t):
            return math.exp(-self._flat_rate * t)

        def update(self):
            pass

    ref_date = ql.Date(15, 6, 2024)
    flat_rate = 0.05
    dc = ql.Actual365Fixed()

    curve = FlatYieldCurve(ref_date, flat_rate, dc)

    assert curve.referenceDate() == ref_date
    assert curve.dayCounter().name() == dc.name()
    assert curve.maxDate() == ql.Date(31, 12, 2199)


def test_yieldtermstructure_python_discount():
    """Test discount factor calculation in Python subclass."""

    class FlatYieldCurve(ql.base.YieldTermStructure):
        def __init__(self, reference_date, flat_rate, day_counter):
            super().__init__(reference_date, ql.NullCalendar(), day_counter)
            self._flat_rate = flat_rate

        def maxDate(self):
            return ql.Date(31, 12, 2199)

        def discountImpl(self, t):
            return math.exp(-self._flat_rate * t)

        def update(self):
            pass

    ref_date = ql.Date(15, 6, 2024)
    flat_rate = 0.05
    dc = ql.Actual365Fixed()

    curve = FlatYieldCurve(ref_date, flat_rate, dc)

    assert curve.discount(0.0) == pytest.approx(1.0)
    assert curve.discount(1.0) == pytest.approx(math.exp(-0.05))

    one_year = ref_date + ql.Period(1, ql.Years)
    expected = math.exp(-flat_rate * dc.yearFraction(ref_date, one_year))
    assert curve.discount(one_year) == pytest.approx(expected, rel=1e-10)


def test_yieldtermstructure_python_zero_rate():
    """Test zero rate calculation in Python subclass."""

    class FlatYieldCurve(ql.base.YieldTermStructure):
        def __init__(self, reference_date, flat_rate, day_counter):
            super().__init__(reference_date, ql.NullCalendar(), day_counter)
            self._flat_rate = flat_rate

        def maxDate(self):
            return ql.Date(31, 12, 2199)

        def discountImpl(self, t):
            return math.exp(-self._flat_rate * t)

        def update(self):
            pass

    ref_date = ql.Date(15, 6, 2024)
    flat_rate = 0.05
    dc = ql.Actual365Fixed()

    curve = FlatYieldCurve(ref_date, flat_rate, dc)

    one_year = ref_date + ql.Period(1, ql.Years)
    zero_rate = curve.zeroRate(one_year, dc, ql.Continuous, ql.Annual)

    assert zero_rate.rate() == pytest.approx(flat_rate, rel=1e-10)


def test_yieldtermstructure_python_forward_rate():
    """Test forward rate calculation in Python subclass."""

    class FlatYieldCurve(ql.base.YieldTermStructure):
        def __init__(self, reference_date, flat_rate, day_counter):
            super().__init__(reference_date, ql.NullCalendar(), day_counter)
            self._flat_rate = flat_rate

        def maxDate(self):
            return ql.Date(31, 12, 2199)

        def discountImpl(self, t):
            return math.exp(-self._flat_rate * t)

        def update(self):
            pass

    ref_date = ql.Date(15, 6, 2024)
    flat_rate = 0.05
    dc = ql.Actual365Fixed()

    curve = FlatYieldCurve(ref_date, flat_rate, dc)

    date1 = ref_date + ql.Period(1, ql.Years)
    date2 = ref_date + ql.Period(2, ql.Years)
    fwd_rate = curve.forwardRate(date1, date2, dc, ql.Continuous, ql.Annual)

    assert fwd_rate.rate() == pytest.approx(flat_rate, rel=1e-10)


def test_yieldtermstructure_relinkable_handle():
    """Test relinkable handle functionality."""

    class FlatYieldCurve(ql.base.YieldTermStructure):
        def __init__(self, reference_date, flat_rate, day_counter):
            super().__init__(reference_date, ql.NullCalendar(), day_counter)
            self._flat_rate = flat_rate

        def maxDate(self):
            return ql.Date(31, 12, 2199)

        def discountImpl(self, t):
            return math.exp(-self._flat_rate * t)

        def update(self):
            pass

    ref_date = ql.Date(15, 6, 2024)
    dc = ql.Actual365Fixed()

    curve1 = FlatYieldCurve(ref_date, 0.05, dc)
    curve2 = FlatYieldCurve(ref_date, 0.03, dc)

    handle = ql.RelinkableYieldTermStructureHandle(curve1)
    assert handle.currentLink().discount(1.0) == pytest.approx(math.exp(-0.05))

    handle.linkTo(curve2)
    assert handle.currentLink().discount(1.0) == pytest.approx(math.exp(-0.03))


def test_yieldtermstructure_handle_empty():
    """Test empty handle behavior."""
    handle = ql.YieldTermStructureHandle()
    assert handle.empty()


# =============================================================================
# FlatForward
# =============================================================================


def test_flatforward_exists():
    """Test FlatForward is in main module."""
    assert hasattr(ql, 'FlatForward')


def test_flatforward_with_rate():
    """Test FlatForward construction with fixed rate."""
    today = ql.Date(15, 6, 2024)
    dc = ql.Actual365Fixed()
    rate = 0.05
    compounding = ql.Compounded
    frequency = ql.Semiannual

    ff = ql.FlatForward(today, rate, dc, compounding, frequency)

    assert ff.compounding() == compounding
    assert ff.compoundingFrequency() == frequency
    assert ff.referenceDate() == today

    future_date = today + ql.Period(2, ql.Years)
    zero_rate = ff.zeroRate(future_date, dc, compounding, frequency)
    assert zero_rate.rate() == pytest.approx(rate)


def test_flatforward_continuous_discount():
    """Test discount factor with continuous compounding (default)."""
    today = ql.Date(15, 6, 2024)
    dc = ql.Actual365Fixed()
    rate = 0.05

    ff = ql.FlatForward(today, rate, dc)

    future_date = today + ql.Period(1, ql.Years)
    time = dc.yearFraction(today, future_date)
    expected_discount = math.exp(-rate * time)

    assert ff.discount(future_date) == pytest.approx(expected_discount)


def test_flatforward_compounded_discount():
    """Test discount factor with compounded interest."""
    today = ql.Date(15, 6, 2024)
    dc = ql.Actual365Fixed()
    rate = 0.05
    frequency = ql.Semiannual

    ff = ql.FlatForward(today, rate, dc, ql.Compounded, frequency)

    future_date = today + ql.Period(2, ql.Years)
    time = dc.yearFraction(today, future_date)
    f = int(frequency)
    expected_discount = math.pow(1.0 + rate / f, -f * time)

    assert ff.discount(future_date) == pytest.approx(expected_discount)


def test_flatforward_with_quote_handle():
    """Test FlatForward linked to Quote via Handle updates automatically."""
    today = ql.Date(15, 6, 2024)
    dc = ql.Actual365Fixed()

    initial_rate = 0.03
    rate_quote = ql.SimpleQuote(initial_rate)
    rate_handle = ql.QuoteHandle(rate_quote)

    ff = ql.FlatForward(today, rate_handle, dc, ql.Continuous)

    one_year = today + ql.Period(1, ql.Years)
    zero_rate = ff.zeroRate(one_year, dc, ql.Continuous)
    assert zero_rate.rate() == pytest.approx(initial_rate)

    new_rate = 0.04
    rate_quote.setValue(new_rate)

    zero_rate_updated = ff.zeroRate(one_year, dc, ql.Continuous)
    assert zero_rate_updated.rate() == pytest.approx(new_rate)


def test_flatforward_with_settlement_days():
    """Test FlatForward construction with settlement days."""
    dc = ql.Actual365Fixed()
    calendar = ql.TARGET()
    rate = 0.05

    ff = ql.FlatForward(2, calendar, rate, dc)

    assert ff.settlementDays() == 2
    assert ff.calendar().name() == calendar.name()


def test_flatforward_in_yts_handle():
    """Test FlatForward works with YieldTermStructureHandle."""
    today = ql.Date(15, 6, 2024)
    dc = ql.Actual365Fixed()
    rate = 0.04

    ff = ql.FlatForward(today, rate, dc)
    handle = ql.YieldTermStructureHandle(ff)

    assert not handle.empty()

    retrieved = handle.currentLink()
    future_date = today + ql.Period(1, ql.Years)
    expected_discount = math.exp(-rate * 1.0)

    assert retrieved.discount(future_date) == pytest.approx(expected_discount)


def test_flatforward_hidden_handle_reference_date():
    """Test FlatForward with Quote (hidden handle) using reference date."""
    today = ql.Date(15, 6, 2024)
    dc = ql.Actual365Fixed()

    rate_quote = ql.SimpleQuote(0.05)
    ff = ql.FlatForward(today, rate_quote, dc)

    one_year = today + ql.Period(1, ql.Years)
    zero_rate = ff.zeroRate(one_year, dc, ql.Continuous)
    assert zero_rate.rate() == pytest.approx(0.05)

    rate_quote.setValue(0.06)
    zero_rate_updated = ff.zeroRate(one_year, dc, ql.Continuous)
    assert zero_rate_updated.rate() == pytest.approx(0.06)


def test_flatforward_hidden_handle_settlement_days():
    """Test FlatForward with Quote (hidden handle) using settlement days."""
    dc = ql.Actual365Fixed()
    calendar = ql.TARGET()

    rate_quote = ql.SimpleQuote(0.04)
    ff = ql.FlatForward(2, calendar, rate_quote, dc, ql.Compounded, ql.Annual)

    assert ff.settlementDays() == 2
    assert ff.compounding() == ql.Compounded
