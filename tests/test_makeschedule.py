import pytest
import pyquantlib as ql 

@pytest.fixture
def common_dates():
    """Provides common dates for tests."""
    return {
        "effective": ql.Date(15, ql.January, 2024),
        "termination": ql.Date(15, ql.January, 2025),
        "first": ql.Date(20, ql.January, 2024),
        "next_to_last": ql.Date(10, ql.January, 2025),
    }

@pytest.fixture
def common_calendar():
    """Provides a common calendar for tests."""
    return ql.TARGET()


def test_make_schedule_basic():
    maker = ql.MakeSchedule()
    
    # Use chaining to set schedule parameters
    effective = ql.Date(1, 1, 2025)
    termination = ql.Date(1, 1, 2026)
    tenor = ql.Period(ql.Monthly)
    calendar = ql.NullCalendar()
    convention = ql.ModifiedFollowing
    termination_convention = ql.Unadjusted
    rule = ql.DateGeneration.Forward
    first_date = ql.Date(15, 1, 2025)
    next_to_last_date = ql.Date(15, 12, 2025)
    
    # Chain methods
    maker = (maker.from_(effective)
            .to(termination)
            .withTenor(tenor)
            .withCalendar(calendar)
            .withConvention(convention)
            .withTerminationDateConvention(termination_convention)
            .withRule(rule)
            .endOfMonth(True)
            .withFirstDate(first_date)
            .withNextToLastDate(next_to_last_date)
            .forwards())
    
    # Convert to Schedule
    schedule = maker.schedule()
    
    # Basic assertions
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


def test_make_schedule_backwards_and_default_endOfMonth():
    maker = ql.MakeSchedule()
    maker = (maker.from_(ql.Date(1, 1, 2025))
        .to(ql.Date(1, 1, 2026))
        .withTenor(ql.Period("1M"))
        .backwards())
    schedule = maker.schedule()
    
    assert schedule.hasRule()
    assert schedule.rule() == ql.DateGeneration.Backward
    # Default endOfMonth should be False unless set
    assert not schedule.endOfMonth()


def test_make_schedule_initialization_and_conversion(common_dates, common_calendar):
    """Tests basic initialization and conversion to Schedule."""
    maker = ql.MakeSchedule()

    maker.from_(common_dates["effective"])
    maker.to(common_dates["termination"])
    maker.withTenor(ql.Period("6M"))
    maker.withCalendar(common_calendar)
    maker.withConvention(ql.Following)
    
    schedule = maker.schedule()
    assert isinstance(schedule, ql.Schedule), "Conversion did not produce a ql.Schedule object"

    # Basic assertions
    assert schedule.startDate() == common_dates["effective"]
    assert schedule.endDate() == common_dates["termination"]
    assert schedule.hasTenor()
    assert schedule.tenor() == ql.Period("6M")
    assert schedule.calendar() == common_calendar
    assert schedule.businessDayConvention() == ql.Following
    assert schedule.hasRule()


def test_make_schedule_frequency_tenor_conversion(common_dates, common_calendar):
    """Tests frequency-tenor conversion."""
    eff_date = common_dates["effective"]
    term_date = common_dates["termination"]
    calendar = common_calendar
    convention = ql.Following
    term_convention = ql.Following
    frequency = ql.Semiannual

    maker = ql.MakeSchedule()
    (
    maker.from_(eff_date) 
         .to(term_date) 
         .withFrequency(frequency) # -> tenor = ql.Period(6, ql.Months) 
         .withCalendar(calendar) 
         .withConvention(convention) 
         .withTerminationDateConvention(term_convention) 
         .forwards() 
    )
    
    assert maker.schedule().tenor() == ql.Period("6M")
    

def test_forward_schedule_properties(common_dates, common_calendar):
    """Tests a forward-generated schedule and its properties."""
    eff_date = common_dates["effective"]
    term_date = common_dates["termination"]
    calendar = common_calendar
    tenor = ql.Period(6, ql.Months)
    convention = ql.Following
    term_convention = ql.Following

    maker = ql.MakeSchedule()
    maker.from_(eff_date) \
         .to(term_date) \
         .withTenor(tenor) \
         .withCalendar(calendar) \
         .withConvention(convention) \
         .withTerminationDateConvention(term_convention) \
         .forwards() # Equivalent to .withRule(ql.DateGeneration.Forward)

    schedule = maker.schedule()

    assert isinstance(schedule, ql.Schedule)
    
    # Check rule
    assert schedule.rule() == ql.DateGeneration.Forward, "Schedule rule should be Forward"
    
    # Check calendar
    assert schedule.calendar() == calendar, "Schedule calendar mismatch"
    
    # Check business day convention
    assert schedule.businessDayConvention() == convention, "Schedule convention mismatch"
    assert schedule.terminationDateBusinessDayConvention() == term_convention, "Schedule termination convention mismatch"

    # Check dates (basic checks)
    assert len(schedule) > 0, "Schedule should have at least one date"
    
    # The first date of the schedule should be the (potentially adjusted) effective date.
    # Adjusting the effective_date manually for the test if it's on a non-business day:
    adjusted_eff_date = calendar.adjust(eff_date, convention)
    assert schedule.startDate() == adjusted_eff_date, \
        f"Schedule start date {schedule.startDate()} does not match expected {adjusted_eff_date}"

    # The last date of the schedule should be the (potentially adjusted) termination date.
    adjusted_term_date = calendar.adjust(term_date, term_convention)
    # For forward generation, the schedule might not end exactly on terminationDate
    # if it doesn't align with the tenor. It will be on or before.
    # More robust check: schedule.endDate() <= adjusted_term_date
    # and the schedule includes the period up to termination.
    # For simplicity, let's check it's not after the adjusted termination date.
    assert schedule.endDate() <= adjusted_term_date, \
         f"Schedule end date {schedule.endDate()} is after expected {adjusted_term_date}"
    

def test_backward_schedule_properties(common_dates, common_calendar):
    """Tests a backward-generated schedule and its properties."""
    eff_date = common_dates["effective"]
    term_date = common_dates["termination"]
    calendar = common_calendar
    tenor = ql.Period(3, ql.Months) # Using a different tenor
    convention = ql.ModifiedFollowing
    term_convention = ql.ModifiedFollowing
    frequency = ql.Quarterly

    maker = ql.MakeSchedule()
    maker.from_(eff_date) \
         .to(term_date) \
         .withTenor(tenor) \
         .withFrequency(frequency) \
         .withCalendar(calendar) \
         .withConvention(convention) \
         .withTerminationDateConvention(term_convention) \
         .backwards() # Equivalent to .withRule(ql.DateGeneration.Backward)

    schedule = maker.schedule()

    assert isinstance(schedule, ql.Schedule)
    assert schedule.rule() == ql.DateGeneration.Backward, "Schedule rule should be Backward"
    assert schedule.calendar().name() == calendar.name(), "Schedule calendar mismatch"
    assert schedule.businessDayConvention() == convention, "Schedule convention mismatch"
    
    adjusted_eff_date = calendar.adjust(eff_date, convention)
    adjusted_term_date = calendar.adjust(term_date, term_convention)

    # For backward generation, the schedule will try to end on terminationDate (adjusted)
    # and start on or after effectiveDate (adjusted).
    assert schedule.endDate() == adjusted_term_date, \
        f"Schedule end date {schedule.endDate()} does not match expected {adjusted_term_date}"
    assert schedule.startDate() >= adjusted_eff_date, \
        f"Schedule start date {schedule.startDate()} is before expected {adjusted_eff_date}"


def test_end_of_month_convention(common_dates, common_calendar):
    """Tests the end-of-month convention."""
    # Effective date that is end of month
    eff_date = ql.Date(31, ql.January, 2024)
    # Termination date also end of month for simplicity in this test
    term_date = ql.Date(31, ql.July, 2024) 
    calendar = common_calendar
    tenor = ql.Period(1, ql.Months)
    convention = ql.Unadjusted # Use Unadjusted to make EOM behavior more predictable for test
    frequency = ql.Monthly

    maker = ql.MakeSchedule()
    maker.from_(eff_date) \
         .to(term_date) \
         .withTenor(tenor) \
         .withFrequency(frequency) \
         .withCalendar(calendar) \
         .withConvention(convention) \
         .withTerminationDateConvention(convention) \
         .forwards() \
         .endOfMonth(True) # Enable end-of-month

    schedule = maker.schedule()

    assert isinstance(schedule, ql.Schedule)
    assert schedule.endOfMonth(), "Schedule should have endOfMonth flag set to True"

    # Verify all generated dates are end-of-month
    # (except possibly the first/last if they were not EOM and convention was not Unadjusted)
    # With Unadjusted and EOM rule, intermediate dates should be EOM.
    dates_in_schedule = schedule.dates()
    for i, dt_in_sched in enumerate(dates_in_schedule):
        # The first date is the effective date, which we set to EOM.
        # The last date is the termination date, which we set to EOM.
        # All intermediate dates should also be EOM.
        is_eom = ql.Date.isEndOfMonth(dt_in_sched)
        # If convention is not Unadjusted, EOM dates might be rolled.
        # This assertion is strongest with Unadjusted.
        assert is_eom, f"Date {dt_in_sched} at index {i} is not end-of-month, but EOM rule was applied."

def test_with_first_and_next_to_last_date(common_dates, common_calendar):
    """Tests setting specific first and next-to-last dates."""
    eff_date = common_dates["effective"]
    term_date = common_dates["termination"]
    first_date_override = common_dates["first"] # Must be >= effectiveDate
    next_to_last_date_override = common_dates["next_to_last"] # Must be <= terminationDate and < last regular date

    # Ensure overrides are within bounds for this test
    assert first_date_override >= eff_date
    assert next_to_last_date_override <= term_date
    
    calendar = common_calendar
    tenor = ql.Period(3, ql.Months)
    convention = ql.Following

    maker = ql.MakeSchedule()
    maker.from_(eff_date) \
         .to(term_date) \
         .withTenor(tenor) \
         .withCalendar(calendar) \
         .withConvention(convention) \
         .forwards() \
         .withFirstDate(first_date_override) \
         .withNextToLastDate(next_to_last_date_override)

    schedule = maker.schedule()
    assert isinstance(schedule, ql.Schedule)

    dates_in_schedule = schedule.dates()
    assert len(schedule) >= 2, "Schedule should have at least two dates for this test"

    # The next-to-last date in the schedule should be the overridden next_to_last_date (adjusted)
    if len(schedule) > 1 : # only makes sense if there are at least 2 dates
        adjusted_next_to_last_date = calendar.adjust(next_to_last_date_override, convention)
        # This check is tricky because the actual next-to-last date might be different
        # if the override forces an irregular period.
        # A simpler check is that this date is *present* if it fits the schedule logic.
        # QuantLib's Schedule constructor with first/nextToLastDate uses them to override
        # the regularly generated dates if they fall within the schedule.
        
        # A more robust check: is the next_to_last_date_override (adjusted) present in the schedule
        # and is it indeed the next to last one?
        # For this test, let's check if it's the actual next-to-last date.
        # This assumes the override was effective and resulted in at least 2 dates.
        if len(schedule) >= 2:
             assert dates_in_schedule[-2] == adjusted_next_to_last_date, \
                f"Schedule's next-to-last date {dates_in_schedule[-2]} doesn't match overridden {adjusted_next_to_last_date}"
        else:
            pytest.skip("Schedule too small to check next-to-last date override meaningfully.")


def test_chaining_and_return_self(common_dates):
    """Test that builder methods return the MakeSchedule instance for chaining."""
    maker = ql.MakeSchedule()
    
    # Test a few methods. If one works, others likely do too due to consistent binding.
    assert maker.from_(common_dates["effective"]) is maker, "'from_' method did not return self"
    assert maker.to(common_dates["termination"]) is maker, "'to' method did not return self"
    assert maker.withTenor(ql.Period(1, ql.Years)) is maker, "'withTenor' method did not return self"
    assert maker.forwards() is maker, "'forwards' method did not return self"
    assert maker.endOfMonth(True) is maker, "'endOfMonth' method did not return self"
