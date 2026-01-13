import pytest

import pyquantlib as ql


def test_yieldtermstructure_abc_exists():
    """Verify YieldTermStructure is in base submodule."""
    assert hasattr(ql.base, 'YieldTermStructure')


def test_yieldtermstructure_zombie():
    """Direct instantiation creates a zombie that fails on pure virtual calls."""
    zombie = ql.base.YieldTermStructure(ql.Actual365Fixed())
    assert zombie is not None

    with pytest.raises(RuntimeError, match="Tried to call pure virtual function"):
        zombie.maxDate()


def test_yieldtermstructure_default_daycounter():
    """Default dayCounter is Actual365Fixed."""
    zombie = ql.base.YieldTermStructure()
    assert zombie.dayCounter().name() == "Actual/365 (Fixed)"


def test_yieldtermstructure_handle_exists():
    """Verify handle types exist."""
    assert hasattr(ql, 'YieldTermStructureHandle')
    assert hasattr(ql, 'RelinkableYieldTermStructureHandle')


def test_python_custom_yieldtermstructure():
    """Test Python subclass implementing pure virtual methods."""

    class FlatYieldCurve(ql.base.YieldTermStructure):
        def __init__(self, reference_date, flat_rate, day_counter):
            super().__init__(reference_date, ql.NullCalendar(), day_counter)
            self._flat_rate = flat_rate
            self._reference_date = reference_date

        def maxDate(self):
            return ql.Date(31, 12, 2199)

        def discountImpl(self, t):
            import math
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


def test_python_custom_yieldtermstructure_discount():
    """Test discount factor calculation in Python subclass."""
    import math

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

    # Test discount at time 0
    assert curve.discount(0.0) == pytest.approx(1.0)

    # Test discount at time 1 year
    assert curve.discount(1.0) == pytest.approx(math.exp(-0.05))

    # Test discount by date
    one_year = ref_date + ql.Period(1, ql.Years)
    expected = math.exp(-flat_rate * dc.yearFraction(ref_date, one_year))
    assert curve.discount(one_year) == pytest.approx(expected, rel=1e-10)


def test_python_custom_yieldtermstructure_zero_rate():
    """Test zero rate calculation in Python subclass."""
    import math

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

    # Test zero rate at 1 year with continuous compounding
    one_year = ref_date + ql.Period(1, ql.Years)
    zero_rate = curve.zeroRate(one_year, dc, ql.Continuous, ql.Annual)

    assert zero_rate.rate() == pytest.approx(flat_rate, rel=1e-10)


def test_python_custom_yieldtermstructure_forward_rate():
    """Test forward rate calculation in Python subclass."""
    import math

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

    # For a flat curve, forward rate equals spot rate
    date1 = ref_date + ql.Period(1, ql.Years)
    date2 = ref_date + ql.Period(2, ql.Years)
    fwd_rate = curve.forwardRate(date1, date2, dc, ql.Continuous, ql.Annual)

    assert fwd_rate.rate() == pytest.approx(flat_rate, rel=1e-10)


def test_relinkable_yieldtermstructure_handle():
    """Test relinkable handle functionality."""
    import math

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
