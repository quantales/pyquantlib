import pytest

import pyquantlib as ql


def test_interestrateindex_abc_exists():
    assert hasattr(ql.base, 'InterestRateIndex')


def test_abstract_interestrateindex_zombie():
    """Direct instantiation creates a zombie that fails on pure virtual calls."""
    calendar = ql.TARGET()
    day_counter = ql.Actual360()
    eur = ql.EURCurrency()
    tenor = ql.Period(6, ql.Months)

    zombie = ql.base.InterestRateIndex("DUMMY", tenor, 2, eur, calendar, day_counter)
    assert zombie is not None

    with pytest.raises(RuntimeError, match="Tried to call pure virtual function"):
        zombie.maturityDate(ql.Date.todaysDate())


def test_python_custom_interestrateindex():
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


def test_python_custom_interestrateindex_fixing():
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
