import pyquantlib as ql


def test_weekday_enum_values():

    # Abbreviations (should match full names)
    assert ql.Weekday.Sun == ql.Weekday.Sunday
    assert ql.Weekday.Mon == ql.Weekday.Monday
    assert ql.Weekday.Tue == ql.Weekday.Tuesday
    assert ql.Weekday.Wed == ql.Weekday.Wednesday
    assert ql.Weekday.Thu == ql.Weekday.Thursday
    assert ql.Weekday.Fri == ql.Weekday.Friday
    assert ql.Weekday.Sat == ql.Weekday.Saturday

def test_weekday_enum_as_int():
    assert int(ql.Weekday.Sunday) == 1
    assert int(ql.Weekday.Monday) == 2
    assert int(ql.Weekday.Saturday) == 7

    monday = int(ql.Weekday.Monday)
    tuesday = int(ql.Weekday.Tuesday)
    assert (tuesday - monday) == 1
