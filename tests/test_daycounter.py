import pytest
import pyquantlib as ql

def test_daycounter_base():
    dc = ql.DayCounter()
    # Base DayCounter should be empty (no impl)
    assert dc.empty()
    # Calling name() or dayCount() should raise due to no implementation
    with pytest.raises(ql.Error):
        dc.name()
    with pytest.raises(ql.Error):
        dc.dayCount(ql.Date(1, 1, 2020), ql.Date(2, 1, 2020))

def test_actual360_shared_ptr():
    # Create an Actual360 instance
    act360 = ql.Actual360()
    
    # Check it's a DayCounter too (inherits correctly)
    assert isinstance(act360, ql.DayCounter)
    
    # It should not be empty (has implementation)
    assert not act360.empty()
    
    # Call a method from DayCounter base class
    d1 = ql.Date(1, 1, 2023)
    d2 = ql.Date(1, 2, 2023)
    
    day_count = act360.dayCount(d1, d2)
    yf = act360.yearFraction(d1, d2)
    
    assert isinstance(day_count, int)
    assert day_count > 0
    
    assert isinstance(yf, float)
    assert yf > 0.0

#@pytest.mark.skip   
def test_daycounters():
    # Example concrete day counters
    dc_30_360 = ql.Thirty360(ql.Thirty360.Convention.ISDA)
    dc_actual_actual = ql.ActualActual(ql.ActualActual.Convention.ISDA)
    dc_actual_360 = ql.Actual360()

    # Check not empty
    assert not dc_30_360.empty()
    assert not dc_actual_actual.empty()
    assert not dc_actual_360.empty()

    # Check names
    assert "30E/360 (ISDA)" == dc_30_360.name()
    assert "Actual/Actual" in dc_actual_actual.name()
    assert "Actual/360" in dc_actual_360.name()

    # Check dayCount returns expected positive integer
    d1 = ql.Date(1, 1, 2020)
    d2 = ql.Date(1, 2, 2020)
    assert dc_30_360.dayCount(d1, d2) > 0
    assert dc_actual_actual.dayCount(d1, d2) > 0
    assert dc_actual_360.dayCount(d1, d2) > 0

    # Check yearFraction returns float > 0
    yf1 = dc_30_360.yearFraction(d1, d2)
    yf2 = dc_actual_actual.yearFraction(d1, d2)
    yf3 = dc_actual_360.yearFraction(d1, d2)
    assert yf1 > 0.0
    assert yf2 > 0.0
    assert yf3 > 0.0

    # Equality operators on same instances
    assert dc_30_360 == dc_30_360
    assert dc_30_360 != dc_actual_360