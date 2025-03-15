import pytest
import pyquantlib as ql


def test_localconstantvol_exists():
    """Verify LocalConstantVol is in main module."""
    assert hasattr(ql, 'LocalConstantVol')


def test_localconstantvol_construction():
    """Test LocalConstantVol construction with reference date."""
    ref_date = ql.Date(15, 6, 2024)
    volatility = 0.25
    dc = ql.Actual365Fixed()

    lcv = ql.LocalConstantVol(ref_date, volatility, dc)

    assert lcv.referenceDate() == ref_date
    assert lcv.dayCounter().name() == dc.name()


def test_localconstantvol_inheritance():
    """Test LocalConstantVol inheritance hierarchy."""
    ref_date = ql.Date(15, 6, 2024)
    lcv = ql.LocalConstantVol(ref_date, 0.20, ql.Actual365Fixed())

    assert isinstance(lcv, ql.LocalConstantVol)
    assert isinstance(lcv, ql.base.LocalVolTermStructure)
    assert isinstance(lcv, ql.base.VolatilityTermStructure)
    assert isinstance(lcv, ql.base.TermStructure)


def test_localconstantvol_localvol():
    """Test localVol returns constant volatility."""
    ref_date = ql.Date(15, 6, 2024)
    volatility = 0.25
    lcv = ql.LocalConstantVol(ref_date, volatility, ql.Actual365Fixed())

    future_date = ref_date + ql.Period(1, ql.Years)
    underlying = 100.0

    assert lcv.localVol(future_date, underlying) == pytest.approx(volatility)
    assert lcv.localVol(2.0, underlying) == pytest.approx(volatility)


def test_localconstantvol_strike_independent():
    """Test localVol is independent of underlying level."""
    ref_date = ql.Date(15, 6, 2024)
    volatility = 0.20
    lcv = ql.LocalConstantVol(ref_date, volatility, ql.Actual365Fixed())

    # Same vol for different underlying levels
    assert lcv.localVol(1.0, 50.0) == pytest.approx(volatility)
    assert lcv.localVol(1.0, 100.0) == pytest.approx(volatility)
    assert lcv.localVol(1.0, 200.0) == pytest.approx(volatility)


def test_localconstantvol_with_quote_handle():
    """Test LocalConstantVol with quote handle updates automatically."""
    ref_date = ql.Date(15, 6, 2024)
    dc = ql.Actual365Fixed()

    initial_vol = 0.20
    vol_quote = ql.SimpleQuote(initial_vol)
    vol_handle = ql.QuoteHandle(vol_quote)

    lcv = ql.LocalConstantVol(ref_date, vol_handle, dc)

    underlying = 100.0
    assert lcv.localVol(1.0, underlying) == pytest.approx(initial_vol)

    # Change quote value
    new_vol = 0.30
    vol_quote.setValue(new_vol)

    assert lcv.localVol(1.0, underlying) == pytest.approx(new_vol)


def test_localconstantvol_settlement_days():
    """Test LocalConstantVol construction with settlement days."""
    today = ql.Date(15, 6, 2024)
    ql.Settings.instance().evaluationDate = today
    
    # Verify evaluationDate was set correctly
    assert ql.Settings.instance().evaluationDate == today, \
        f"evaluationDate not set: expected {today}, got {ql.Settings.instance().evaluationDate}"
    
    calendar = ql.TARGET()
    volatility = 0.25
    dc = ql.Actual365Fixed()

    lcv = ql.LocalConstantVol(2, calendar, volatility, dc)

    # Reference date should be 2 business days from evaluation date
    expected_ref = calendar.advance(today, 2, ql.Days)
    assert lcv.referenceDate() == expected_ref


def test_localconstantvol_in_handle():
    """Test LocalConstantVol works with LocalVolTermStructureHandle."""
    ref_date = ql.Date(15, 6, 2024)
    volatility = 0.25
    lcv = ql.LocalConstantVol(ref_date, volatility, ql.Actual365Fixed())

    handle = ql.LocalVolTermStructureHandle(lcv)
    assert not handle.empty()

    retrieved = handle.currentLink()
    assert retrieved.localVol(1.0, 100.0) == pytest.approx(volatility)
