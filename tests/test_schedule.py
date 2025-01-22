import pyquantlib as ql
import pytest

print("ql.Date is", ql.Date)
print("type(ql.Date) =", type(ql.Date))

# @pytest.mark.skip 
def test_schedule_basic_construction():
    # Prepare inputs
    dates = [ql.Date(1, 1, 2025), ql.Date(1, 7, 2025), ql.Date(1, 1, 2026)]
    calendar = ql.NullCalendar()
    convention = ql.Unadjusted

    # Construct Schedule from explicit dates
    schedule = ql.Schedule(dates, calendar, convention)

    assert len(schedule) == 3
    assert schedule.empty() == False
    assert schedule.at(0) == ql.Date(1, 1, 2025)
    assert schedule.front() == ql.Date(1, 1, 2025)
    assert schedule.back() == ql.Date(1, 1, 2026)
    assert schedule[1] == ql.Date(1, 7, 2025)
    assert schedule.dates() == dates

def test_schedule_rule_based_construction():
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

# @pytest.mark.skip 
def test_schedule_iterators():
    dates = [ql.Date(1, 1, 2025), ql.Date(1, 7, 2025), ql.Date(1, 1, 2026)]
    schedule = ql.Schedule(dates)

    dates_from_iter = list(date for date in schedule)
    assert dates_from_iter == dates

# @pytest.mark.skip 
def test_schedule_boundaries():
    dates = [ql.Date(1, 1, 2025), ql.Date(1, 7, 2025), ql.Date(1, 1, 2026)]
    schedule = ql.Schedule(dates)

    # previousDate and nextDate returns correct dates relative to input
    assert schedule.previousDate(ql.Date(15, 6, 2025)) == ql.Date(1, 1, 2025)
    assert schedule.nextDate(ql.Date(15, 6, 2025)) == ql.Date(1, 7, 2025)

# @pytest.mark.skip 
def test_schedule_out_of_range_access():
    dates = [ql.Date(1, 1, 2025), ql.Date(1, 7, 2025)]
    schedule = ql.Schedule(dates)

    with pytest.raises(IndexError):
        _ = schedule[len(schedule)]  # access out of range

def test_schedule_isRegular_and_calendar():
    # Construct with regular flags
    dates = [ql.Date(1, 1, 2025), ql.Date(1, 7, 2025), ql.Date(1, 1, 2026)]
    is_regular = [True, False]
    schedule = ql.Schedule(dates, ql.NullCalendar(), ql.Unadjusted, None, None, None, None, is_regular)

    assert schedule.hasIsRegular()
    assert schedule.isRegular(1) is True
    assert schedule.isRegular(2) is False
    assert schedule.calendar() == ql.NullCalendar()
    assert schedule.isRegular() == is_regular
