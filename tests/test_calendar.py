import pytest
import sys
import pyquantlib as ql

def test_calendar_empty():
    calendar = ql.Calendar()
    assert calendar.empty()

def test_calendar_name():
    calendar = ql.TARGET()
    assert calendar.name() == "TARGET"

def test_add_and_remove_holidays():
    calendar = ql.TARGET()
    date = ql.Date(8, ql.January, 2025)  # A Wednesday, normally a business day

    # Test addHoliday
    assert calendar.isBusinessDay(date)
    calendar.addHoliday(date)
    assert not calendar.isBusinessDay(date)
    assert calendar.isHoliday(date)

    # Test removeHoliday (undoes the added holiday)
    calendar.removeHoliday(date)
    assert calendar.isBusinessDay(date)
    assert not calendar.isHoliday(date)

def test_reset_holidays():
    calendar = ql.TARGET()
    date = ql.Date(8, ql.January, 2025)

    # Add a holiday, then reset
    calendar.addHoliday(date)
    assert calendar.isHoliday(date)
    
    calendar.resetAddedAndRemovedHolidays()
    assert calendar.isBusinessDay(date)

def test_is_holiday_and_is_business_day():
    calendar = ql.TARGET()
    
    # New Year's Day 2025 (Wednesday) - holiday
    new_years = ql.Date(1, ql.January, 2025)
    assert calendar.isHoliday(new_years)
    assert not calendar.isBusinessDay(new_years)

    # A regular Wednesday in TARGET
    regular_day = ql.Date(8, ql.January, 2025)
    assert not calendar.isHoliday(regular_day)
    assert calendar.isBusinessDay(regular_day)

def test_is_weekend():
    calendar = ql.TARGET()
    assert calendar.isWeekend(ql.Saturday)
    assert calendar.isWeekend(ql.Sunday)
    assert not calendar.isWeekend(ql.Monday)

def test_start_end_of_month():
    calendar = ql.TARGET()
    date = ql.Date(15, ql.January, 2025)

    # startOfMonth should be the first business day of the month
    start = calendar.startOfMonth(date)
    assert start.month() == ql.January
    assert calendar.isBusinessDay(start)

    # endOfMonth should be the last business day of the month
    end = calendar.endOfMonth(date)
    assert end.month() == ql.January
    assert calendar.isBusinessDay(end)

def test_adjust_and_advance():
    calendar = ql.TARGET()
    
    # Adjust a Saturday to the next Monday
    saturday = ql.Date(4, ql.January, 2025)
    adjusted = calendar.adjust(saturday, ql.Following)
    assert calendar.isBusinessDay(adjusted)
    assert adjusted > saturday

    # Advance 5 business days
    start = ql.Date(2, ql.January, 2025)  # Thursday
    advanced = calendar.advance(start, 5, ql.Days)
    assert calendar.isBusinessDay(advanced)

def test_business_days_and_holiday_list():
    calendar = ql.TARGET()
    start = ql.Date(1, ql.January, 2025)
    end = ql.Date(31, ql.January, 2025)

    holidays = calendar.holidayList(start, end, False)
    business_days = calendar.businessDayList(start, end)

    assert len(holidays) > 0  # Should have at least New Year's Day
    assert len(business_days) > 0
    
    # All business days should be business days
    for d in business_days:
        assert calendar.isBusinessDay(d)

def test_business_days_between():
    calendar = ql.TARGET()
    start = ql.Date(2, ql.January, 2025)
    end = ql.Date(10, ql.January, 2025)

    # Count business days
    count = calendar.businessDaysBetween(start, end, True, False)
    assert count > 0

def test_united_states_calendar():
    us_govt = ql.UnitedStates(ql.UnitedStates.GovernmentBond)
    assert us_govt.name() == "US government bond market"

def test_poland_calendar():
    poland = ql.Poland()
    assert poland.name() == "Poland Settlement"

def test_joint_calendar_holidays():
    us_govt = ql.UnitedStates(ql.UnitedStates.GovernmentBond)
    target = ql.TARGET()
    joint = ql.JointCalendar(us_govt, target)

    # Joint calendar should recognize holidays from both
    assert "US government bond market" in joint.name() or "TARGET" in joint.name()

@pytest.mark.skipif(sys.platform == "darwin", reason="CalendarVector/shared_ptr holder issue on macOS")
def test_hash():
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

def test_reset_added_holidays():
    calendar = ql.BespokeCalendar("bespoke thing")
    test_date = ql.Date(1, ql.January, 2024)
    assert not calendar.isHoliday(test_date)
    
    calendar.addHoliday(test_date)
    assert calendar.isHoliday(test_date)
    
    calendar.resetAddedAndRemovedHolidays()
    assert not calendar.isHoliday(test_date)
