import pyquantlib as ql


def test_timeunit_enum_values():
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
    assert isinstance(ql.TimeUnit.Days, ql.TimeUnit)
    assert ql.TimeUnit.Hours != ql.TimeUnit.Minutes
    assert ql.TimeUnit.Seconds.value != ql.TimeUnit.Milliseconds.value
