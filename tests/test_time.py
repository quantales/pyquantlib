"""
Tests for time module.

Corresponds to src/time/*.cpp bindings.
"""

import pytest
from datetime import date, datetime

import pyquantlib as ql


# =============================================================================
# Date
# =============================================================================


def test_date_construction():
    """Test Date construction with day, month, year."""
    d1 = ql.Date(15, ql.Month.May, 2024)
    assert d1.dayOfMonth() == 15
    assert d1.month() == ql.Month.May
    assert d1.year() == 2024


def test_date_default_constructor():
    """Test Date default constructor creates null date."""
    d = ql.Date()
    assert d.serialNumber() == 0


def test_date_serial_constructor():
    """Test Date construction from serial number."""
    d = ql.Date(10000)
    assert d.serialNumber() == 10000


def test_date_arithmetic():
    """Test Date arithmetic operations."""
    d = ql.Date(1, ql.Month.January, 2000)
    d2 = d + 30
    assert d2.serialNumber() == d.serialNumber() + 30

    d3 = d2 - 15
    assert d3.serialNumber() == d2.serialNumber() - 15


def test_date_static_methods():
    """Test Date static methods."""
    assert isinstance(ql.Date.todaysDate(), ql.Date)
    assert ql.Date.isLeap(2020) is True
    assert ql.Date.isLeap(2021) is False


def test_date_start_end_of_month():
    """Test Date start/end of month static methods."""
    d = ql.Date(15, ql.Month.May, 2024)
    start = ql.Date.startOfMonth(d)
    end = ql.Date.endOfMonth(d)
    assert start.dayOfMonth() == 1
    assert end.dayOfMonth() == 31


def test_date_is_start_end_of_month():
    """Test Date.isStartOfMonth and isEndOfMonth."""
    start = ql.Date(1, ql.Month.June, 2024)
    end = ql.Date(30, ql.Month.June, 2024)
    assert ql.Date.isStartOfMonth(start)
    assert ql.Date.isEndOfMonth(end)


def test_date_next_weekday():
    """Test Date.nextWeekday static method."""
    d = ql.Date(12, ql.Month.January, 2024)  # Friday
    next_monday = ql.Date.nextWeekday(d, ql.Weekday.Monday)
    assert next_monday.weekday() == ql.Weekday.Monday
    assert next_monday.serialNumber() > d.serialNumber()


def test_date_nth_weekday():
    """Test Date.nthWeekday static method."""
    # 4th Thursday of March 2024
    d = ql.Date.nthWeekday(4, ql.Weekday.Thursday, ql.Month.March, 2024)
    assert d.dayOfMonth() == 28
    assert d.month() == ql.Month.March
    assert d.year() == 2024
    assert d.weekday() == ql.Weekday.Thursday


def test_date_days_between():
    """Test daysBetween free function."""
    d1 = ql.Date(1, ql.Month.May, 2024)
    d2 = ql.Date(10, ql.Month.May, 2024)
    delta = ql.daysBetween(d1, d2)
    assert delta == 9


def test_date_from_datetime():
    """Test Date construction from datetime.date."""
    py_date = date(2024, 6, 15)
    ql_date = ql.Date(py_date)
    assert ql_date.year() == 2024
    assert ql_date.month() == ql.Month.June
    assert ql_date.dayOfMonth() == 15


def test_date_to_datetime():
    """Test Date conversion to datetime.date."""
    ql_date = ql.Date(15, ql.Month.June, 2024)
    py_date = ql_date.to_date()
    assert py_date == date(2024, 6, 15)


def test_date_from_date_static():
    """Test Date.from_date static method."""
    py_date = date(2024, 6, 15)
    ql_date = ql.Date.from_date(py_date)
    assert isinstance(ql_date, ql.Date)
    assert ql_date.year() == 2024


def test_date_settings_evaluation_date_datetime():
    """Test Settings.evaluationDate accepts datetime.date."""
    py_date = date(2024, 6, 15)
    ql.Settings.instance().evaluationDate = ql.Date(py_date)
    result = ql.Settings.instance().evaluationDate
    assert isinstance(result, ql.Date)
    assert result.year() == 2024


def test_date_days_between_datetime_direct():
    """Test daysBetween with datetime.date arguments."""
    d1 = date(2024, 5, 1)
    d2 = date(2024, 5, 10)
    delta = ql.daysBetween(d1, d2)
    assert delta == 9


def test_date_from_datetime_datetime():
    """Test Date construction from datetime.datetime."""
    dt = datetime(2024, 6, 15, 10, 30, 0)
    ql_date = ql.Date(dt)
    assert ql_date.year() == 2024
    assert ql_date.month() == ql.Month.June
    assert ql_date.dayOfMonth() == 15


# =============================================================================
# Calendar
# =============================================================================


def test_calendar_empty():
    """Test empty Calendar."""
    calendar = ql.Calendar()
    assert calendar.empty()


def test_calendar_name():
    """Test Calendar.name method."""
    calendar = ql.TARGET()
    assert calendar.name() == "TARGET"


def test_calendar_add_and_remove_holidays():
    """Test Calendar.addHoliday and removeHoliday."""
    calendar = ql.TARGET()
    d = ql.Date(8, ql.January, 2025)  # Normally a business day

    assert calendar.isBusinessDay(d)
    calendar.addHoliday(d)
    assert not calendar.isBusinessDay(d)
    assert calendar.isHoliday(d)

    calendar.removeHoliday(d)
    assert calendar.isBusinessDay(d)
    assert not calendar.isHoliday(d)


def test_calendar_reset_holidays():
    """Test Calendar.resetAddedAndRemovedHolidays."""
    calendar = ql.TARGET()
    d = ql.Date(8, ql.January, 2025)

    calendar.addHoliday(d)
    assert calendar.isHoliday(d)

    calendar.resetAddedAndRemovedHolidays()
    assert calendar.isBusinessDay(d)


def test_calendar_is_holiday_and_business_day():
    """Test Calendar.isHoliday and isBusinessDay."""
    calendar = ql.TARGET()

    new_years = ql.Date(1, ql.January, 2025)
    assert calendar.isHoliday(new_years)
    assert not calendar.isBusinessDay(new_years)

    regular_day = ql.Date(8, ql.January, 2025)
    assert not calendar.isHoliday(regular_day)
    assert calendar.isBusinessDay(regular_day)


def test_calendar_is_weekend():
    """Test Calendar.isWeekend."""
    calendar = ql.TARGET()
    assert calendar.isWeekend(ql.Saturday)
    assert calendar.isWeekend(ql.Sunday)
    assert not calendar.isWeekend(ql.Monday)


def test_calendar_start_end_of_month():
    """Test Calendar start/end of month methods."""
    calendar = ql.TARGET()
    d = ql.Date(15, ql.January, 2025)

    start = calendar.startOfMonth(d)
    assert start.month() == ql.January
    assert calendar.isBusinessDay(start)

    end = calendar.endOfMonth(d)
    assert end.month() == ql.January
    assert calendar.isBusinessDay(end)


def test_calendar_adjust_and_advance():
    """Test Calendar.adjust and advance."""
    calendar = ql.TARGET()

    saturday = ql.Date(4, ql.January, 2025)
    adjusted = calendar.adjust(saturday, ql.Following)
    assert calendar.isBusinessDay(adjusted)
    assert adjusted > saturday

    start = ql.Date(2, ql.January, 2025)
    advanced = calendar.advance(start, 5, ql.Days)
    assert calendar.isBusinessDay(advanced)


def test_calendar_business_days_and_holiday_list():
    """Test Calendar.businessDayList and holidayList."""
    calendar = ql.TARGET()
    start = ql.Date(1, ql.January, 2025)
    end = ql.Date(31, ql.January, 2025)

    holidays = calendar.holidayList(start, end, False)
    business_days = calendar.businessDayList(start, end)

    assert len(holidays) > 0
    assert len(business_days) > 0

    for d in business_days:
        assert calendar.isBusinessDay(d)


def test_calendar_business_days_between():
    """Test Calendar.businessDaysBetween."""
    calendar = ql.TARGET()
    start = ql.Date(2, ql.January, 2025)
    end = ql.Date(10, ql.January, 2025)

    count = calendar.businessDaysBetween(start, end, True, False)
    assert count == 6


def test_calendar_united_states():
    """Test UnitedStates calendar."""
    us_govt = ql.UnitedStates(ql.UnitedStates.GovernmentBond)
    assert us_govt.name() == "US government bond market"


def test_calendar_poland():
    """Test Poland calendar."""
    poland = ql.Poland()
    assert poland.name() == "Poland Settlement"


def test_calendar_joint():
    """Test JointCalendar."""
    us_govt = ql.UnitedStates(ql.UnitedStates.GovernmentBond)
    target = ql.TARGET()
    joint = ql.JointCalendar(us_govt, target)

    assert "US government bond market" in joint.name() or "TARGET" in joint.name()


def test_calendar_hash():
    """Test Calendar equality and hashing."""
    empty1, empty2 = ql.CalendarVector(2)
    for cal1 in (ql.BespokeCalendar("one"), ql.BespokeCalendar("two"), empty1):
        for cal2 in (ql.BespokeCalendar("one"), ql.BespokeCalendar("two"), empty2):
            if cal1.empty() or cal2.empty():
                expected = cal1.empty() == cal2.empty()
            else:
                expected = cal1.name() == cal2.name()
            assert (cal1 == cal2) == expected
            assert (cal1 != cal2) != expected
            assert (hash(cal1) == hash(cal2)) == expected


def test_calendar_bespoke_reset():
    """Test BespokeCalendar holiday reset."""
    calendar = ql.BespokeCalendar("bespoke thing")
    test_date = ql.Date(1, ql.January, 2024)
    assert not calendar.isHoliday(test_date)

    calendar.addHoliday(test_date)
    assert calendar.isHoliday(test_date)

    calendar.resetAddedAndRemovedHolidays()
    assert not calendar.isHoliday(test_date)


# =============================================================================
# DayCounter
# =============================================================================


def test_daycounter_base():
    """Test empty DayCounter raises on method calls."""
    dc = ql.DayCounter()
    assert dc.empty()
    with pytest.raises(ql.Error):
        dc.name()
    with pytest.raises(ql.Error):
        dc.dayCount(ql.Date(1, 1, 2020), ql.Date(2, 1, 2020))


def test_daycounter_actual360():
    """Test Actual360 day counter."""
    act360 = ql.Actual360()

    assert isinstance(act360, ql.DayCounter)
    assert not act360.empty()

    d1 = ql.Date(1, 1, 2023)
    d2 = ql.Date(1, 2, 2023)

    day_count = act360.dayCount(d1, d2)
    yf = act360.yearFraction(d1, d2)

    assert isinstance(day_count, int)
    assert day_count == 31
    assert isinstance(yf, float)
    assert yf == pytest.approx(31 / 360, rel=1e-6)


def test_daycounter_variants():
    """Test various day counter implementations."""
    dc_30_360 = ql.Thirty360(ql.Thirty360.Convention.ISDA)
    dc_actual_actual = ql.ActualActual(ql.ActualActual.Convention.ISDA)
    dc_actual_360 = ql.Actual360()

    assert not dc_30_360.empty()
    assert not dc_actual_actual.empty()
    assert not dc_actual_360.empty()

    assert "30E/360 (ISDA)" == dc_30_360.name()
    assert "Actual/Actual" in dc_actual_actual.name()
    assert "Actual/360" in dc_actual_360.name()

    d1 = ql.Date(1, 1, 2020)
    d2 = ql.Date(1, 2, 2020)
    assert dc_30_360.dayCount(d1, d2) > 0
    assert dc_actual_actual.dayCount(d1, d2) > 0
    assert dc_actual_360.dayCount(d1, d2) > 0

    assert dc_30_360.yearFraction(d1, d2) > 0.0
    assert dc_actual_actual.yearFraction(d1, d2) > 0.0
    assert dc_actual_360.yearFraction(d1, d2) > 0.0

    assert dc_30_360 == dc_30_360
    assert dc_30_360 != dc_actual_360


# =============================================================================
# Period
# =============================================================================


def test_period_constructors():
    """Test Period constructors."""
    p_default = ql.Period()
    assert str(p_default) == "0D"

    p_3m = ql.Period(3, ql.Months)
    assert p_3m.length() == 3
    assert p_3m.units() == ql.Months

    p_2y = ql.Period(2, ql.Years)
    assert p_2y.length() == 2
    assert p_2y.units() == ql.Years

    p_7d = ql.Period(7, ql.Days)
    assert p_7d.length() == 7
    assert p_7d.units() == ql.Days

    p_4w = ql.Period(4, ql.Weeks)
    assert p_4w.length() == 4
    assert p_4w.units() == ql.Weeks


def test_period_from_frequency():
    """Test Period construction from Frequency."""
    p_annual = ql.Period(ql.Annual)
    assert p_annual.length() == 1
    assert p_annual.units() == ql.Years
    assert p_annual.frequency() == ql.Annual

    p_semiannual = ql.Period(ql.Semiannual)
    assert p_semiannual.length() == 6
    assert p_semiannual.units() == ql.Months
    assert p_semiannual.frequency() == ql.Semiannual

    p_quarterly = ql.Period(ql.Quarterly)
    assert p_quarterly.length() == 3
    assert p_quarterly.units() == ql.Months
    assert p_quarterly.frequency() == ql.Quarterly

    p_monthly = ql.Period(ql.Monthly)
    assert p_monthly.length() == 1
    assert p_monthly.units() == ql.Months
    assert p_monthly.frequency() == ql.Monthly

    p_weekly = ql.Period(ql.Weekly)
    assert p_weekly.length() == 1
    assert p_weekly.units() == ql.Weeks
    assert p_weekly.frequency() == ql.Weekly

    p_daily = ql.Period(ql.Daily)
    assert p_daily.length() == 1
    assert p_daily.units() == ql.Days
    assert p_daily.frequency() == ql.Daily

    p_once = ql.Period(ql.Once)
    assert p_once.length() == 0
    assert p_once.units() == ql.Years
    assert p_once.frequency() == ql.Once

    p_nofreq = ql.Period(ql.NoFrequency)
    assert p_nofreq.length() == 0
    assert p_nofreq.units() == ql.Days
    assert p_nofreq.frequency() == ql.NoFrequency


@pytest.mark.parametrize("period_str, length, unit", [
    ("1D", 1, ql.Days), ("1d", 1, ql.Days),
    ("1W", 1, ql.Weeks), ("1w", 1, ql.Weeks),
    ("1M", 1, ql.Months), ("1m", 1, ql.Months),
    ("1Y", 1, ql.Years), ("1y", 1, ql.Years),
    ("0D", 0, ql.Days), ("0M", 0, ql.Months),
    ("12M", 12, ql.Months),
    ("52W", 52, ql.Weeks),
    ("365D", 365, ql.Days),
    ("18M", 18, ql.Months),
    ("2Y6M", 30, ql.Months),
    ("1W2D", 9, ql.Days),
])
def test_period_from_string_valid(period_str, length, unit):
    """Test Period construction from string."""
    p = ql.Period(period_str)
    expected_p = ql.Period(length, unit)
    assert p == expected_p
    assert p.length() == length
    assert p.units() == unit


@pytest.mark.parametrize("invalid_str", [
    "1X", "ABC", "1", "M", "1M2", "1D1M", "Y1", ""
])
def test_period_from_string_invalid(invalid_str):
    """Test Period rejects invalid strings."""
    with pytest.raises(ValueError, match="Invalid period string"):
        ql.Period(invalid_str)


def test_period_members():
    """Test Period member functions."""
    p_6m = ql.Period(6, ql.Months)
    assert p_6m.length() == 6
    assert p_6m.units() == ql.Months
    assert p_6m.frequency() == ql.Semiannual

    p_1y = ql.Period(1, ql.Years)
    assert p_1y.length() == 1
    assert p_1y.units() == ql.Years
    assert p_1y.frequency() == ql.Annual


def test_period_normalize():
    """Test Period normalization."""
    p_12m = ql.Period(12, ql.Months)
    p_12m_normalized_copy = p_12m.normalized()

    assert p_12m_normalized_copy.length() == 1
    assert p_12m_normalized_copy.units() == ql.Years
    assert p_12m.length() == 12
    assert p_12m.units() == ql.Months

    p_12m.normalize()
    assert p_12m.length() == 1
    assert p_12m.units() == ql.Years

    p_13m = ql.Period(13, ql.Months)
    p_13m.normalize()
    assert p_13m.length() == 13
    assert p_13m.units() == ql.Months

    p_7d = ql.Period(7, ql.Days)
    p_7d_norm_copy = p_7d.normalized()
    assert p_7d_norm_copy.length() == 1
    assert p_7d_norm_copy.units() == ql.Weeks

    p_7d.normalize()
    assert p_7d.length() == 1
    assert p_7d.units() == ql.Weeks


def test_period_inplace_operators():
    """Test Period in-place operators."""
    p1 = ql.Period(3, ql.Months)
    p2 = ql.Period(6, ql.Months)
    p1 += p2
    assert p1 == ql.Period(9, ql.Months)

    p3 = ql.Period(1, ql.Years)
    p1 += p3
    p1.normalize()
    assert p1 == ql.Period(21, ql.Months)

    p4 = ql.Period(1, ql.Years)
    p5 = ql.Period(3, ql.Months)
    p4 -= p5
    assert p4 == ql.Period(9, ql.Months)

    p6 = ql.Period(2, ql.Weeks)
    p6 *= 3
    assert p6 == ql.Period(6, ql.Weeks)

    p7 = ql.Period(10, ql.Months)
    p7 /= 2
    assert p7 == ql.Period(5, ql.Months)

    p8 = ql.Period(1, ql.Years)
    with pytest.raises(ql.Error):
        p8 /= 0


def test_period_comparisons():
    """Test Period comparison operators."""
    p6m = ql.Period(6, ql.Months)
    p1y = ql.Period(1, ql.Years)
    p12m = ql.Period(12, ql.Months)

    assert p6m == ql.Period(6, ql.Months)
    assert p1y == p12m.normalized()
    assert p1y != p6m

    assert p6m < p1y
    assert p1y > p6m
    assert p6m <= p1y
    assert p6m <= ql.Period(6, ql.Months)
    assert p1y >= p6m
    assert p1y >= p12m.normalized()

    assert ql.Period("1Y") > ql.Period("11M")
    assert ql.Period("12M") == ql.Period("1Y").normalized()

    assert ql.Period(12, ql.Months) == ql.Period(1, ql.Years)
    assert ql.Period(2, ql.Weeks) == ql.Period(14, ql.Days)


def test_period_arithmetic():
    """Test Period arithmetic operators."""
    p3m = ql.Period(3, ql.Months)
    p6m = ql.Period(6, ql.Months)

    neg_p3m = -p3m
    assert neg_p3m.length() == -3
    assert neg_p3m.units() == ql.Months

    p9m = p3m + p6m
    assert p9m == ql.Period(9, ql.Months)

    p1y = ql.Period(1, ql.Years)
    p1y3m = p1y + p3m
    assert p1y3m.units() == ql.Months
    assert p1y3m.length() == 15

    p_minus_3m = p6m - p3m
    assert p_minus_3m == ql.Period(3, ql.Months)

    p_mult = p3m * 4
    assert p_mult.length() == 12
    assert p_mult.units() == ql.Months
    p_mult.normalize()
    assert p_mult == ql.Period(1, ql.Years)

    p_rmult = 2 * p6m
    assert p_rmult.length() == 12
    assert p_rmult.units() == ql.Months
    p_rmult.normalize()
    assert p_rmult == ql.Period(1, ql.Years)

    p_div = ql.Period(2, ql.Years) / 2
    assert p_div == ql.Period(1, ql.Years)

    p_div_months = ql.Period(18, ql.Months) / 3
    assert p_div_months == ql.Period(6, ql.Months)

    with pytest.raises(ql.Error):
        _ = ql.Period(1, ql.Years) / 0


def test_period_str_repr():
    """Test Period string representations."""
    p_5w = ql.Period(5, ql.Weeks)
    assert str(p_5w) == "5W"
    assert repr(p_5w).startswith("<Period: ")
    assert str(p_5w) in repr(p_5w)
    assert repr(p_5w).endswith(">")

    p_10d = ql.Period("10d")
    assert str(p_10d) == "10D"
    assert repr(p_10d) == "<Period: 10D>"

    p_30m_from_str = ql.Period("2Y6M")
    assert str(p_30m_from_str) == "30M"
    assert repr(p_30m_from_str) == "<Period: 30M>"


def test_period_hash():
    """Test Period hashing."""
    p1 = ql.Period(1, ql.Years)
    p2 = ql.Period(12, ql.Months).normalized()
    p3 = ql.Period(1, ql.Years)
    p4 = ql.Period(6, ql.Months)

    assert hash(p1) == hash(p2)
    assert hash(p1) == hash(p3)
    assert hash(p1) != hash(p4)

    period_set = {p1, p2, p3, p4}
    assert len(period_set) == 2

    period_dict = {p1: "one_year", p4: "six_months"}
    assert period_dict[p2] == "one_year"


def test_period_free_functions():
    """Test Period-related free functions."""
    p_1y = ql.Period(1, ql.Years)
    p_2m = ql.Period(2, ql.Months)
    p_3w = ql.Period(3, ql.Weeks)
    p_10d = ql.Period(10, ql.Days)
    p_18m = ql.Period(18, ql.Months)

    assert ql.years(p_1y) == 1
    assert ql.years(p_18m) == 1.5

    assert ql.months(p_1y) == 12
    assert ql.months(p_2m) == 2
    assert ql.months(p_18m) == 18

    assert ql.weeks(p_3w) == 3
    assert int(ql.weeks(p_10d)) == 1

    assert ql.days(p_3w) == 21
    assert ql.days(p_10d) == 10

    p_zero = ql.Period(0, ql.Days)
    assert ql.years(p_zero) == 0
    assert ql.months(p_zero) == 0
    assert ql.weeks(p_zero) == 0
    assert ql.days(p_zero) == 0


# =============================================================================
# TimeUnit
# =============================================================================


def test_timeunit_enum_values():
    """Test TimeUnit enum values."""
    assert ql.TimeUnit.Days.name == "Days"
    assert ql.TimeUnit.Weeks.name == "Weeks"
    assert ql.TimeUnit.Months.name == "Months"
    assert ql.TimeUnit.Years.name == "Years"
    assert ql.TimeUnit.Hours.name == "Hours"
    assert ql.TimeUnit.Minutes.name == "Minutes"
    assert ql.TimeUnit.Seconds.name == "Seconds"
    assert ql.TimeUnit.Milliseconds.name == "Milliseconds"
    assert ql.TimeUnit.Microseconds.name == "Microseconds"


def test_timeunit_enum_type():
    """Test TimeUnit enum type and comparisons."""
    assert isinstance(ql.TimeUnit.Days, ql.TimeUnit)
    assert ql.TimeUnit.Hours != ql.TimeUnit.Minutes
    assert ql.TimeUnit.Seconds.value != ql.TimeUnit.Milliseconds.value


# =============================================================================
# Frequency
# =============================================================================


def test_frequency_enum_members():
    """Test Frequency enum members exist."""
    expected_members = [
        "NoFrequency",
        "Once",
        "Annual",
        "Semiannual",
        "EveryFourthMonth",
        "Quarterly",
        "Bimonthly",
        "Monthly",
        "EveryFourthWeek",
        "Biweekly",
        "Weekly",
        "Daily",
        "OtherFrequency",
    ]

    for member in expected_members:
        assert hasattr(ql.Frequency, member), f"Frequency missing: {member}"


def test_frequency_enum_values():
    """Test Frequency enum integer values."""
    assert int(ql.Frequency.NoFrequency) == -1
    assert int(ql.Frequency.Once) == 0
    assert int(ql.Frequency.Annual) == 1
    assert int(ql.Frequency.Semiannual) == 2
    assert int(ql.Frequency.EveryFourthMonth) == 3
    assert int(ql.Frequency.Quarterly) == 4
    assert int(ql.Frequency.Bimonthly) == 6
    assert int(ql.Frequency.Monthly) == 12
    assert int(ql.Frequency.EveryFourthWeek) == 13
    assert int(ql.Frequency.Biweekly) == 26
    assert int(ql.Frequency.Weekly) == 52
    assert int(ql.Frequency.Daily) == 365
    assert int(ql.Frequency.OtherFrequency) == 999


# =============================================================================
# Weekday
# =============================================================================


def test_weekday_enum_values():
    """Test Weekday enum values and abbreviations."""
    assert ql.Weekday.Sun == ql.Weekday.Sunday
    assert ql.Weekday.Mon == ql.Weekday.Monday
    assert ql.Weekday.Tue == ql.Weekday.Tuesday
    assert ql.Weekday.Wed == ql.Weekday.Wednesday
    assert ql.Weekday.Thu == ql.Weekday.Thursday
    assert ql.Weekday.Fri == ql.Weekday.Friday
    assert ql.Weekday.Sat == ql.Weekday.Saturday


def test_weekday_enum_as_int():
    """Test Weekday enum integer values."""
    assert int(ql.Weekday.Sunday) == 1
    assert int(ql.Weekday.Monday) == 2
    assert int(ql.Weekday.Saturday) == 7

    monday = int(ql.Weekday.Monday)
    tuesday = int(ql.Weekday.Tuesday)
    assert (tuesday - monday) == 1


# =============================================================================
# TimeGrid
# =============================================================================


def test_timegrid_regular_constructor():
    """Test TimeGrid regular spaced constructor."""
    end_time = 2.0
    steps = 4
    grid = ql.TimeGrid(end_time, steps)

    assert not grid.empty()
    assert len(grid) == steps + 1
    assert grid.size() == 5

    expected_times = [0.0, 0.5, 1.0, 1.5, 2.0]
    for i, t in enumerate(grid):
        assert t == pytest.approx(expected_times[i])

    assert grid[0] == 0.0
    assert grid[4] == 2.0
    assert grid.back() == 2.0

    assert grid.dt(0) == pytest.approx(0.5)
    assert grid.dt(1) == pytest.approx(0.5)


def test_timegrid_from_list_constructor():
    """Test TimeGrid constructor with mandatory times."""
    mandatory_times = [0.5, 1.0, 1.5]

    grid = ql.TimeGrid(mandatory_times)
    expected_times = [0.0, 0.5, 1.0, 1.5]
    assert list(grid) == pytest.approx(expected_times)
    assert grid.mandatoryTimes() == pytest.approx(mandatory_times)

    steps = 6
    grid_with_steps = ql.TimeGrid(mandatory_times, steps)
    assert len(grid_with_steps) > len(mandatory_times)
    assert grid_with_steps.size() == 7
    assert grid_with_steps.back() == 1.5

    for t in mandatory_times:
        assert grid_with_steps.closestTime(t) == pytest.approx(t)


def test_timegrid_utility_methods():
    """Test TimeGrid utility methods."""
    grid = ql.TimeGrid(1.0, 4)

    assert grid.index(0.5) == 2

    assert grid.closestIndex(0.51) == 2
    assert grid.closestIndex(0.60) == 2
    assert grid.closestIndex(0.63) == 3
    assert grid.closestIndex(-0.1) == 0

    assert grid.closestTime(0.6) == pytest.approx(0.5)


# =============================================================================
# Schedule
# =============================================================================


def test_schedule_basic_construction():
    """Test Schedule construction from explicit dates."""
    dates = [ql.Date(1, 1, 2025), ql.Date(1, 7, 2025), ql.Date(1, 1, 2026)]
    calendar = ql.NullCalendar()
    convention = ql.Unadjusted

    schedule = ql.Schedule(dates, calendar, convention)

    assert len(schedule) == 3
    assert not schedule.empty()
    assert schedule.at(0) == ql.Date(1, 1, 2025)
    assert schedule.front() == ql.Date(1, 1, 2025)
    assert schedule.back() == ql.Date(1, 1, 2026)
    assert schedule[1] == ql.Date(1, 7, 2025)
    assert schedule.dates() == dates


def test_schedule_rule_based_construction():
    """Test Schedule rule-based construction."""
    effective = ql.Date(1, 1, 2025)
    termination = ql.Date(1, 1, 2026)
    tenor = ql.Period(ql.Semiannual)
    calendar = ql.NullCalendar()
    convention = ql.Unadjusted
    term_date_convention = ql.Unadjusted
    rule = ql.DateGeneration.Backward
    end_of_month = False

    schedule = ql.Schedule(effective, termination, tenor, calendar,
                           convention, term_date_convention, rule, end_of_month)

    assert schedule.startDate() == effective
    assert schedule.endDate() == termination
    assert schedule.hasTenor()
    assert schedule.tenor() == tenor
    assert schedule.hasRule()
    assert schedule.rule() == rule
    assert not schedule.endOfMonth()


def test_schedule_iterators():
    """Test Schedule iteration."""
    dates = [ql.Date(1, 1, 2025), ql.Date(1, 7, 2025), ql.Date(1, 1, 2026)]
    schedule = ql.Schedule(dates)

    dates_from_iter = list(schedule)
    assert dates_from_iter == dates


def test_schedule_boundaries():
    """Test Schedule previousDate and nextDate."""
    dates = [ql.Date(1, 1, 2025), ql.Date(1, 7, 2025), ql.Date(1, 1, 2026)]
    schedule = ql.Schedule(dates)

    assert schedule.previousDate(ql.Date(15, 6, 2025)) == ql.Date(1, 1, 2025)
    assert schedule.nextDate(ql.Date(15, 6, 2025)) == ql.Date(1, 7, 2025)


def test_schedule_out_of_range_access():
    """Test Schedule raises on out-of-range access."""
    dates = [ql.Date(1, 1, 2025), ql.Date(1, 7, 2025)]
    schedule = ql.Schedule(dates)

    with pytest.raises(IndexError):
        _ = schedule[len(schedule)]


def test_schedule_is_regular_and_calendar():
    """Test Schedule isRegular and calendar."""
    dates = [ql.Date(1, 1, 2025), ql.Date(1, 7, 2025), ql.Date(1, 1, 2026)]
    is_regular = [True, False]
    schedule = ql.Schedule(dates, ql.NullCalendar(), ql.Unadjusted, None, None, None, None, is_regular)

    assert schedule.hasIsRegular()
    assert schedule.isRegular(1) is True
    assert schedule.isRegular(2) is False
    assert schedule.calendar() == ql.NullCalendar()
    assert schedule.isRegular() == is_regular


# =============================================================================
# MakeSchedule
# =============================================================================


@pytest.fixture
def schedule_dates():
    """Common dates for MakeSchedule tests."""
    return {
        "effective": ql.Date(15, ql.January, 2024),
        "termination": ql.Date(15, ql.January, 2025),
        "first": ql.Date(20, ql.January, 2024),
        "next_to_last": ql.Date(10, ql.January, 2025),
    }


def test_makeschedule_kwargs():
    """Test MakeSchedule kwargs API with all options."""
    effective = ql.Date(1, 1, 2025)
    termination = ql.Date(1, 1, 2026)
    tenor = ql.Period(ql.Monthly)
    calendar = ql.NullCalendar()
    convention = ql.ModifiedFollowing
    termination_convention = ql.Unadjusted
    rule = ql.DateGeneration.Forward
    first_date = ql.Date(15, 1, 2025)
    next_to_last_date = ql.Date(15, 12, 2025)

    schedule = ql.MakeSchedule(
        effectiveDate=effective,
        terminationDate=termination,
        forwards=True,
        tenor=tenor,
        calendar=calendar,
        convention=convention,
        terminationDateConvention=termination_convention,
        rule=rule,
        endOfMonth=True,
        firstDate=first_date,
        nextToLastDate=next_to_last_date,
    )

    assert isinstance(schedule, ql.Schedule)
    assert schedule.startDate() == effective
    assert schedule.endDate() == termination
    assert schedule.hasTenor()
    assert schedule.tenor() == tenor
    assert schedule.calendar() == calendar
    assert schedule.businessDayConvention() == convention
    assert schedule.hasRule()
    assert schedule.rule() == rule
    assert schedule.endOfMonth()


def test_makeschedule_kwargs_backwards():
    """Test MakeSchedule backwards generation via kwargs."""
    schedule = ql.MakeSchedule(
        effectiveDate=ql.Date(1, 1, 2025),
        terminationDate=ql.Date(1, 1, 2026),
        backwards=True,
        tenor=ql.Period("1M"),
    )

    assert schedule.hasRule()
    assert schedule.rule() == ql.DateGeneration.Backward
    assert not schedule.endOfMonth()


def test_makeschedule_kwargs_basic(schedule_dates):
    """Test MakeSchedule kwargs initialization and conversion to Schedule."""
    calendar = ql.TARGET()

    schedule = ql.MakeSchedule(
        effectiveDate=schedule_dates["effective"],
        terminationDate=schedule_dates["termination"],
        tenor=ql.Period("6M"),
        calendar=calendar,
        convention=ql.Following,
    )
    assert isinstance(schedule, ql.Schedule)

    assert schedule.startDate() == schedule_dates["effective"]
    assert schedule.endDate() == schedule_dates["termination"]
    assert schedule.hasTenor()
    assert schedule.tenor() == ql.Period("6M")
    assert schedule.calendar() == calendar
    assert schedule.businessDayConvention() == ql.Following
    assert schedule.hasRule()


def test_makeschedule_kwargs_frequency(schedule_dates):
    """Test MakeSchedule frequency-tenor conversion via kwargs."""
    schedule = ql.MakeSchedule(
        effectiveDate=schedule_dates["effective"],
        terminationDate=schedule_dates["termination"],
        forwards=True,
        frequency=ql.Semiannual,
        calendar=ql.TARGET(),
        convention=ql.Following,
        terminationDateConvention=ql.Following,
    )

    assert schedule.tenor() == ql.Period("6M")


def test_makeschedule_kwargs_forward_properties(schedule_dates):
    """Test forward-generated schedule properties via kwargs."""
    eff_date = schedule_dates["effective"]
    term_date = schedule_dates["termination"]
    calendar = ql.TARGET()
    tenor = ql.Period(6, ql.Months)
    convention = ql.Following
    term_convention = ql.Following

    schedule = ql.MakeSchedule(
        effectiveDate=eff_date,
        terminationDate=term_date,
        forwards=True,
        tenor=tenor,
        calendar=calendar,
        convention=convention,
        terminationDateConvention=term_convention,
    )

    assert isinstance(schedule, ql.Schedule)
    assert schedule.rule() == ql.DateGeneration.Forward
    assert schedule.calendar() == calendar
    assert schedule.businessDayConvention() == convention
    assert schedule.terminationDateBusinessDayConvention() == term_convention
    assert len(schedule) > 0

    adjusted_eff_date = calendar.adjust(eff_date, convention)
    assert schedule.startDate() == adjusted_eff_date

    adjusted_term_date = calendar.adjust(term_date, term_convention)
    assert schedule.endDate() <= adjusted_term_date


def test_makeschedule_kwargs_backward_properties(schedule_dates):
    """Test backward-generated schedule properties via kwargs."""
    eff_date = schedule_dates["effective"]
    term_date = schedule_dates["termination"]
    calendar = ql.TARGET()
    tenor = ql.Period(3, ql.Months)
    convention = ql.ModifiedFollowing
    term_convention = ql.ModifiedFollowing

    schedule = ql.MakeSchedule(
        effectiveDate=eff_date,
        terminationDate=term_date,
        backwards=True,
        tenor=tenor,
        frequency=ql.Quarterly,
        calendar=calendar,
        convention=convention,
        terminationDateConvention=term_convention,
    )

    assert isinstance(schedule, ql.Schedule)
    assert schedule.rule() == ql.DateGeneration.Backward
    assert schedule.calendar().name() == calendar.name()
    assert schedule.businessDayConvention() == convention

    adjusted_eff_date = calendar.adjust(eff_date, convention)
    adjusted_term_date = calendar.adjust(term_date, term_convention)

    assert schedule.endDate() == adjusted_term_date
    assert schedule.startDate() >= adjusted_eff_date


def test_makeschedule_kwargs_end_of_month():
    """Test end-of-month convention via kwargs."""
    eff_date = ql.Date(31, ql.January, 2024)
    term_date = ql.Date(31, ql.July, 2024)
    calendar = ql.TARGET()
    convention = ql.Unadjusted

    schedule = ql.MakeSchedule(
        effectiveDate=eff_date,
        terminationDate=term_date,
        forwards=True,
        tenor=ql.Period(1, ql.Months),
        frequency=ql.Monthly,
        calendar=calendar,
        convention=convention,
        terminationDateConvention=convention,
        endOfMonth=True,
    )

    assert isinstance(schedule, ql.Schedule)
    assert schedule.endOfMonth()

    dates_in_schedule = schedule.dates()
    for i, dt_in_sched in enumerate(dates_in_schedule):
        is_eom = ql.Date.isEndOfMonth(dt_in_sched)
        assert is_eom, f"Date {dt_in_sched} at index {i} is not end-of-month"


def test_makeschedule_kwargs_first_and_next_to_last_date(schedule_dates):
    """Test setting first and next-to-last dates via kwargs."""
    eff_date = schedule_dates["effective"]
    term_date = schedule_dates["termination"]
    first_date_override = schedule_dates["first"]
    next_to_last_date_override = schedule_dates["next_to_last"]

    assert first_date_override >= eff_date
    assert next_to_last_date_override <= term_date

    calendar = ql.TARGET()
    convention = ql.Following

    schedule = ql.MakeSchedule(
        effectiveDate=eff_date,
        terminationDate=term_date,
        forwards=True,
        tenor=ql.Period(3, ql.Months),
        calendar=calendar,
        convention=convention,
        firstDate=first_date_override,
        nextToLastDate=next_to_last_date_override,
    )
    assert isinstance(schedule, ql.Schedule)

    dates_in_schedule = schedule.dates()
    assert len(schedule) >= 2

    if len(schedule) >= 2:
        adjusted_next_to_last_date = calendar.adjust(next_to_last_date_override, convention)
        assert dates_in_schedule[-2] == adjusted_next_to_last_date


def test_makeschedule_builder_chaining(schedule_dates):
    """Test MakeSchedule C++ builder chaining."""
    from pyquantlib._pyquantlib import MakeSchedule as MakeScheduleBuilder

    maker = MakeScheduleBuilder()

    assert maker.from_(schedule_dates["effective"]) is maker
    assert maker.to(schedule_dates["termination"]) is maker
    assert maker.withTenor(ql.Period(1, ql.Years)) is maker
    assert maker.forwards() is maker
    assert maker.endOfMonth(True) is maker

    schedule = maker.schedule()
    assert isinstance(schedule, ql.Schedule)


def test_makeschedule_kwargs_bad_kwarg():
    """Test MakeSchedule rejects unknown kwargs."""
    import pytest

    with pytest.raises(TypeError, match="unexpected keyword argument"):
        ql.MakeSchedule(
            effectiveDate=ql.Date(1, 1, 2025),
            terminationDate=ql.Date(1, 1, 2026),
            bogusKwarg=42,
        )
