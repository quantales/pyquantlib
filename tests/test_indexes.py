"""
Tests for indexes module.

Corresponds to src/indexes/*.cpp bindings.
"""

import pytest

import pyquantlib as ql


# =============================================================================
# Index (ABC)
# =============================================================================


def test_index_abc_exists():
    """Tests that Index ABC is accessible."""
    assert hasattr(ql.base, 'Index')


def test_index_zombie():
    """Tests that direct instantiation creates a zombie object."""
    zombie = ql.base.Index()

    with pytest.raises(RuntimeError, match="Tried to call pure virtual function"):
        zombie.name()

    with pytest.raises(RuntimeError, match="Tried to call pure virtual function"):
        zombie.fixingCalendar()


def test_index_python_inheritance():
    """Tests creating a custom Index class in Python."""

    class CustomIndex(ql.base.Index):
        def __init__(self, name, calendar):
            super().__init__()
            self._name = name
            self._calendar = calendar
            self._fixings = {}

        def name(self):
            return self._name

        def fixingCalendar(self):
            return self._calendar

        def isValidFixingDate(self, date):
            return self._calendar.isBusinessDay(date)

        def fixing(self, date, forecastTodaysFixing=False):
            return self._fixings.get(date.serialNumber(), 0.0)

        def update(self):
            pass

    idx = CustomIndex("TEST", ql.TARGET())

    assert idx.name() == "TEST"
    assert idx.fixingCalendar().name() == "TARGET"


# =============================================================================
# InterestRateIndex (ABC)
# =============================================================================


def test_interestrateindex_abc_exists():
    """Test InterestRateIndex ABC is accessible."""
    assert hasattr(ql.base, 'InterestRateIndex')


def test_interestrateindex_zombie():
    """Direct instantiation creates a zombie that fails on pure virtual calls."""
    calendar = ql.TARGET()
    day_counter = ql.Actual360()
    eur = ql.EURCurrency()
    tenor = ql.Period(6, ql.Months)

    zombie = ql.base.InterestRateIndex("DUMMY", tenor, 2, eur, calendar, day_counter)
    assert zombie is not None

    with pytest.raises(RuntimeError, match="Tried to call pure virtual function"):
        zombie.maturityDate(ql.Date.todaysDate())


def test_interestrateindex_python_custom():
    """Test Python subclass implementing pure virtual methods."""

    class MyIndex(ql.base.InterestRateIndex):
        def __init__(self, family_name, tenor, fixing_days, currency, calendar, day_counter):
            super().__init__(family_name, tenor, fixing_days, currency, calendar, day_counter)
            self._fixings = {}

        def maturityDate(self, valueDate):
            return self.fixingCalendar().advance(valueDate, self.tenor())

        def forecastFixing(self, fixingDate):
            return 0.05

        def fixing(self, d, forecastTodaysFixing=False):
            if d in self._fixings:
                return self._fixings[d]
            if forecastTodaysFixing:
                return self.forecastFixing(d)
            raise ql.Error(f"Fixing not available for {self.name()} on {d}")

        def update(self):
            pass

        def addFixing(self, d, value):
            self._fixings[d] = value

    calendar = ql.TARGET()
    day_counter = ql.Actual360()
    eur = ql.EURCurrency()
    tenor = ql.Period(6, ql.Months)

    my_index = MyIndex("MyEUR6M", tenor, 2, eur, calendar, day_counter)

    assert my_index.familyName() == "MyEUR6M"
    assert my_index.tenor() == tenor
    assert my_index.currency() == eur
    assert my_index.dayCounter().name() == day_counter.name()


def test_interestrateindex_python_fixing():
    """Test fixing logic in Python subclass."""

    class MyIndex(ql.base.InterestRateIndex):
        def __init__(self, family_name, tenor, fixing_days, currency, calendar, day_counter):
            super().__init__(family_name, tenor, fixing_days, currency, calendar, day_counter)
            self._fixings = {}

        def maturityDate(self, valueDate):
            return self.fixingCalendar().advance(valueDate, self.tenor())

        def forecastFixing(self, fixingDate):
            return 0.05

        def fixing(self, d, forecastTodaysFixing=False):
            if d in self._fixings:
                return self._fixings[d]
            if forecastTodaysFixing:
                return self.forecastFixing(d)
            raise ql.Error("No fixing")

        def update(self):
            pass

        def addFixing(self, d, value):
            self._fixings[d] = value

    calendar = ql.TARGET()
    my_index = MyIndex("TEST", ql.Period(6, ql.Months), 2, ql.EURCurrency(), calendar, ql.Actual360())

    today = ql.Date(14, 6, 2024)
    fixing_date = my_index.fixingDate(today)

    my_index.addFixing(fixing_date, 0.045)
    assert my_index.fixing(fixing_date) == pytest.approx(0.045)

    future_date = calendar.advance(today, 1, ql.Years)
    assert my_index.fixing(future_date, True) == pytest.approx(0.05)


# =============================================================================
# IborIndex
# =============================================================================


@pytest.fixture
def yield_curve():
    """Simple flat yield curve for index tests."""
    today = ql.Date(15, ql.June, 2025)
    ql.Settings.instance().evaluationDate = today
    dc = ql.Actual365Fixed()
    return ql.FlatForward(today, 0.05, dc)


def test_iborindex_construction():
    """Test IborIndex construction."""
    today = ql.Date(15, ql.June, 2025)
    ql.Settings.instance().evaluationDate = today

    index = ql.IborIndex(
        "TestIbor",
        ql.Period(3, ql.Months),
        2,  # settlement days
        ql.EURCurrency(),
        ql.TARGET(),
        ql.ModifiedFollowing,
        False,  # end of month
        ql.Actual360(),
    )

    assert index is not None
    assert index.familyName() == "TestIbor"
    assert index.tenor() == ql.Period(3, ql.Months)


def test_iborindex_with_curve(yield_curve):
    """Test IborIndex with forwarding term structure."""
    index = ql.IborIndex(
        "TestIbor",
        ql.Period(6, ql.Months),
        2,
        ql.EURCurrency(),
        ql.TARGET(),
        ql.ModifiedFollowing,
        True,
        ql.Actual360(),
        yield_curve,
    )

    assert index is not None
    assert index.endOfMonth() is True


def test_iborindex_clone(yield_curve):
    """Test IborIndex clone method."""
    index = ql.IborIndex(
        "TestIbor",
        ql.Period(3, ql.Months),
        2,
        ql.EURCurrency(),
        ql.TARGET(),
        ql.ModifiedFollowing,
        False,
        ql.Actual360(),
    )

    cloned = index.clone(ql.YieldTermStructureHandle(yield_curve))
    assert cloned is not None


# =============================================================================
# Euribor
# =============================================================================


def test_euribor_construction():
    """Test Euribor construction with tenor."""
    today = ql.Date(15, ql.June, 2025)
    ql.Settings.instance().evaluationDate = today

    euribor = ql.Euribor(ql.Period(6, ql.Months))

    assert euribor is not None
    assert euribor.tenor() == ql.Period(6, ql.Months)
    assert "Euribor" in euribor.name()


def test_euribor_with_curve(yield_curve):
    """Test Euribor with forwarding term structure."""
    euribor = ql.Euribor(ql.Period(3, ql.Months), yield_curve)

    assert euribor is not None


def test_euribor6m(yield_curve):
    """Test Euribor6M convenience class."""
    euribor = ql.Euribor6M(yield_curve)

    assert euribor is not None
    assert euribor.tenor() == ql.Period(6, ql.Months)


def test_euribor6m_no_curve():
    """Test Euribor6M without forwarding curve."""
    today = ql.Date(15, ql.June, 2025)
    ql.Settings.instance().evaluationDate = today

    euribor = ql.Euribor6M()

    assert euribor is not None
    assert euribor.tenor() == ql.Period(6, ql.Months)


def test_euribor3m(yield_curve):
    """Test Euribor3M convenience class."""
    euribor = ql.Euribor3M(yield_curve)

    assert euribor is not None
    assert euribor.tenor() == ql.Period(3, ql.Months)


def test_euribor1m(yield_curve):
    """Test Euribor1M convenience class."""
    euribor = ql.Euribor1M(yield_curve)

    assert euribor is not None
    assert euribor.tenor() == ql.Period(1, ql.Months)


def test_euribor1y(yield_curve):
    """Test Euribor1Y convenience class."""
    euribor = ql.Euribor1Y(yield_curve)

    assert euribor is not None
    assert euribor.tenor() == ql.Period(1, ql.Years)


def test_euribor_fixing(yield_curve):
    """Test Euribor fixing calculation."""
    today = ql.Date(15, ql.June, 2025)
    ql.Settings.instance().evaluationDate = today

    euribor = ql.Euribor6M(yield_curve)

    # Get a valid fixing date
    fixing_date = euribor.fixingCalendar().advance(
        today, ql.Period(2, ql.Days), ql.Following
    )

    # Should be able to forecast fixing
    if euribor.isValidFixingDate(fixing_date):
        rate = euribor.fixing(fixing_date, True)
        assert rate == pytest.approx(0.04993839342800618, rel=1e-5)


# =============================================================================
# OvernightIndex (RFR): SOFR, ESTR, SONIA
# =============================================================================


@pytest.fixture(scope="module")
def flat_curve():
    """Flat yield curve for RFR index tests."""
    today = ql.Date(15, ql.January, 2025)
    ql.Settings.evaluationDate = today
    curve = ql.FlatForward(today, 0.035, ql.Actual365Fixed())
    return {"today": today, "curve": curve}


def test_sofr_construction():
    """Test Sofr construction without curve."""
    sofr = ql.Sofr()
    assert sofr is not None
    assert "SOFR" in sofr.name()


def test_sofr_with_curve(flat_curve):
    """Test Sofr construction with forwarding curve."""
    sofr = ql.Sofr(flat_curve["curve"])
    assert sofr is not None
    assert "SOFR" in sofr.name()


def test_sofr_properties():
    """Test Sofr index properties."""
    sofr = ql.Sofr()
    assert sofr.fixingDays() == 0
    assert sofr.dayCounter() == ql.Actual360()


def test_estr_construction():
    """Test Estr construction without curve."""
    estr = ql.Estr()
    assert estr is not None
    assert "ESTR" in estr.name()


def test_estr_with_curve(flat_curve):
    """Test Estr construction with forwarding curve."""
    estr = ql.Estr(flat_curve["curve"])
    assert estr is not None


def test_estr_properties():
    """Test Estr index properties."""
    estr = ql.Estr()
    assert estr.fixingDays() == 0
    assert estr.dayCounter() == ql.Actual360()


def test_sonia_construction():
    """Test Sonia construction without curve."""
    sonia = ql.Sonia()
    assert sonia is not None
    assert "Sonia" in sonia.name()


def test_sonia_with_curve(flat_curve):
    """Test Sonia construction with forwarding curve."""
    sonia = ql.Sonia(flat_curve["curve"])
    assert sonia is not None


def test_sonia_properties():
    """Test Sonia index properties."""
    sonia = ql.Sonia()
    assert sonia.fixingDays() == 0
    assert sonia.dayCounter() == ql.Actual365Fixed()


# =============================================================================
# SwapIndex
# =============================================================================


def test_swapindex_construction(flat_curve):
    """Test SwapIndex construction."""
    euribor6m = ql.Euribor(ql.Period(6, ql.Months), flat_curve["curve"])
    swap_index = ql.SwapIndex(
        "EurSwap", ql.Period(5, ql.Years), 2,
        ql.EURCurrency(), ql.TARGET(),
        ql.Period(1, ql.Years), ql.Unadjusted,
        ql.Thirty360(ql.Thirty360.BondBasis),
        euribor6m,
    )
    assert swap_index is not None
    assert swap_index.fixedLegConvention() == ql.Unadjusted


def test_swapindex_with_discount(flat_curve):
    """Test SwapIndex construction with discounting curve."""
    euribor6m = ql.Euribor(ql.Period(6, ql.Months), flat_curve["curve"])
    swap_index = ql.SwapIndex(
        "EurSwap", ql.Period(5, ql.Years), 2,
        ql.EURCurrency(), ql.TARGET(),
        ql.Period(1, ql.Years), ql.Unadjusted,
        ql.Thirty360(ql.Thirty360.BondBasis),
        euribor6m, flat_curve["curve"],
    )
    assert swap_index is not None
    assert swap_index.exogenousDiscount()


def test_swapindex_properties(flat_curve):
    """Test SwapIndex property accessors."""
    euribor6m = ql.Euribor(ql.Period(6, ql.Months), flat_curve["curve"])
    swap_index = ql.SwapIndex(
        "EurSwap", ql.Period(5, ql.Years), 2,
        ql.EURCurrency(), ql.TARGET(),
        ql.Period(1, ql.Years), ql.Unadjusted,
        ql.Thirty360(ql.Thirty360.BondBasis),
        euribor6m,
    )
    assert swap_index.fixedLegTenor() == ql.Period(1, ql.Years)
    assert swap_index.iborIndex() is not None
    assert not swap_index.exogenousDiscount()


# =============================================================================
# OvernightIndexedSwapIndex
# =============================================================================


def test_overnightindexedswapindex_construction(flat_curve):
    """Test OvernightIndexedSwapIndex construction."""
    estr = ql.Estr(flat_curve["curve"])
    ois_index = ql.OvernightIndexedSwapIndex(
        "EstrSwap", ql.Period(1, ql.Years), 2,
        ql.EURCurrency(), estr,
    )
    assert ois_index is not None


def test_overnightindexedswapindex_with_averaging(flat_curve):
    """Test OvernightIndexedSwapIndex with explicit averaging."""
    sofr = ql.Sofr(flat_curve["curve"])
    ois_index = ql.OvernightIndexedSwapIndex(
        "SofrSwap", ql.Period(2, ql.Years), 2,
        ql.USDCurrency(), sofr,
        telescopicValueDates=True,
        averagingMethod=ql.RateAveraging.Type.Simple,
    )
    assert ois_index is not None
