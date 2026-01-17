import pyquantlib as ql


def test_date_construction():
    d1 = ql.Date(15, ql.Month.May, 2024)
    assert d1.dayOfMonth() == 15
    assert d1.month() == ql.Month.May
    assert d1.year() == 2024

def test_default_constructor():
    d = ql.Date()
    assert d.serialNumber() == 0  # Null date has serial 0 in QuantLib

def test_serial_constructor():
    d = ql.Date(10000)
    assert d.serialNumber() == 10000

def test_date_arithmetic():
    d = ql.Date(1, ql.Month.January, 2000)
    d2 = d + 30
    assert d2.serialNumber() == d.serialNumber() + 30

    d3 = d2 - 15
    assert d3.serialNumber() == d2.serialNumber() - 15

def test_static_methods():
    assert isinstance(ql.Date.todaysDate(), ql.Date)
    assert ql.Date.isLeap(2020) is True
    assert ql.Date.isLeap(2021) is False

def test_start_end_of_month():
    d = ql.Date(15, ql.Month.May, 2024)
    start = ql.Date.startOfMonth(d)
    end = ql.Date.endOfMonth(d)
    assert start.dayOfMonth() == 1
    assert end.dayOfMonth() == 31

def test_is_start_end_of_month():
    start = ql.Date(1, ql.Month.June, 2024)
    end = ql.Date(30, ql.Month.June, 2024)
    assert ql.Date.isStartOfMonth(start)
    assert ql.Date.isEndOfMonth(end)

def test_next_weekday():
    from pyquantlib import Date, Weekday
    d = Date(12, ql.Month.January, 2024)  # Friday
    next_monday = Date.nextWeekday(d, Weekday.Monday)
    assert next_monday.weekday() == Weekday.Monday
    assert next_monday.serialNumber() > d.serialNumber()

def test_nth_weekday():
    from pyquantlib import Weekday
    # 4th Thursday of March 2024
    d = ql.Date.nthWeekday(4, Weekday.Thursday, ql.Month.March, 2024)
    assert d.dayOfMonth() == 28
    assert d.month() == ql.Month.March
    assert d.year() == 2024
    assert d.weekday() == Weekday.Thursday

def test_days_between():
    d1 = ql.Date(1, ql.Month.May, 2024)
    d2 = ql.Date(10, ql.Month.May, 2024)
    delta = ql.daysBetween(d1, d2)
    assert delta == 9


# --- datetime.date interoperability ---

def test_date_from_datetime():
    """datetime.date can be passed to Date constructor."""
    from datetime import date
    py_date = date(2024, 6, 15)
    ql_date = ql.Date(py_date)
    assert ql_date.year() == 2024
    assert ql_date.month() == ql.Month.June
    assert ql_date.dayOfMonth() == 15


def test_date_to_datetime():
    """Date can be converted to datetime.date."""
    from datetime import date
    ql_date = ql.Date(15, ql.Month.June, 2024)
    py_date = ql_date.to_date()
    assert py_date == date(2024, 6, 15)


def test_date_from_date_static():
    """Date.from_date() converts datetime.date to Date."""
    from datetime import date
    py_date = date(2024, 6, 15)
    ql_date = ql.Date.from_date(py_date)
    assert isinstance(ql_date, ql.Date)
    assert ql_date.year() == 2024


def test_settings_evaluation_date_datetime():
    """Settings.evaluationDate accepts datetime.date."""
    from datetime import date
    py_date = date(2024, 6, 15)
    ql.Settings.instance().evaluationDate = ql.Date(py_date)
    result = ql.Settings.instance().evaluationDate
    assert isinstance(result, ql.Date)
    assert result.year() == 2024


def test_days_between_datetime_direct():
    """datetime.date can be passed directly to daysBetween."""
    from datetime import date
    d1 = date(2024, 5, 1)
    d2 = date(2024, 5, 10)
    delta = ql.daysBetween(d1, d2)
    assert delta == 9


def test_date_from_datetime_datetime():
    """datetime.datetime can also be passed (time part ignored)."""
    from datetime import datetime
    dt = datetime(2024, 6, 15, 10, 30, 0)
    ql_date = ql.Date(dt)
    assert ql_date.year() == 2024
    assert ql_date.month() == ql.Month.June
    assert ql_date.dayOfMonth() == 15
