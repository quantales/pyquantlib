# Minimal test to verify Settings singleton fix with static QuantLib build.

import pyquantlib as ql


def test_settings_evaluationdate_persists():
    """Test that evaluationDate persists when creating term structures."""
    # Set a specific evaluation date
    test_date = ql.Date(15, 1, 2025)
    ql.Settings.instance().evaluationDate = test_date
    
    # Verify it's set
    assert ql.Settings.instance().evaluationDate == test_date, \
        "evaluationDate not set correctly"
    
    # Create a term structure that reads evaluationDate internally
    # This is where the singleton issue manifests
    calendar = ql.TARGET()
    settlement_days = 2
    
    # BlackConstantVol with settlement days reads Settings.evaluationDate
    bcv = ql.BlackConstantVol(settlement_days, calendar, 0.25, ql.Actual365Fixed())
    
    # Reference date should be: evaluationDate + settlement_days (business days)
    expected_ref = calendar.advance(test_date, settlement_days, ql.Days)
    actual_ref = bcv.referenceDate()
    
    # This assertion fails if singleton is broken:
    # - With shared lib: actual_ref uses real today's date
    # - With static lib: actual_ref uses our test_date
    assert actual_ref == expected_ref, \
        f"Singleton issue detected! Expected {expected_ref}, got {actual_ref}. " \
        f"Term structure used wrong evaluationDate."


def test_settings_persists_across_multiple_objects():
    """Test Settings persists when creating multiple QuantLib objects."""
    test_date = ql.Date(20, 6, 2025)
    ql.Settings.instance().evaluationDate = test_date
    
    # Create several objects that might trigger singleton access
    calendar = ql.TARGET()
    dc = ql.Actual365Fixed()
    
    ts1 = ql.FlatForward(test_date, 0.05, dc)
    ts2 = ql.BlackConstantVol(2, calendar, 0.20, dc)
    ts3 = ql.FlatForward(test_date, 0.03, dc)
    
    # Verify evaluationDate still correct
    assert ql.Settings.instance().evaluationDate == test_date
    
    # Verify ts2 used correct date
    expected_ref = calendar.advance(test_date, 2, ql.Days)
    assert ts2.referenceDate() == expected_ref
