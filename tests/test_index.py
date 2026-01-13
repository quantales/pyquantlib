import pytest

import pyquantlib as ql


def test_index_abc_exists():
    """Tests that Index ABC is accessible."""
    assert hasattr(ql.base, 'Index')


def test_abstract_index_zombie():
    """Tests that direct instantiation creates a zombie object."""
    zombie = ql.base.Index()

    with pytest.raises(RuntimeError, match="Tried to call pure virtual function"):
        zombie.name()

    with pytest.raises(RuntimeError, match="Tried to call pure virtual function"):
        zombie.fixingCalendar()


def test_python_custom_index_inheritance():
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
