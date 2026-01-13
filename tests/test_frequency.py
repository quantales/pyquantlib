import pyquantlib as ql


def test_frequency_enum_members_exist():
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
