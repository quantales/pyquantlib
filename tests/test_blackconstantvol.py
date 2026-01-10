import pytest
import pyquantlib as ql


def test_blackconstantvol_exists():
    """Verify BlackConstantVol is in main module."""
    assert hasattr(ql, 'BlackConstantVol')


def test_blackconstantvol_construction():
    """Test BlackConstantVol construction with reference date."""
    ref_date = ql.Date(15, 6, 2024)
    calendar = ql.TARGET()
    volatility = 0.25
    dc = ql.Actual365Fixed()

    bcv = ql.BlackConstantVol(ref_date, calendar, volatility, dc)

    assert bcv.referenceDate() == ref_date
    assert bcv.dayCounter().name() == dc.name()


def test_blackconstantvol_inheritance():
    """Test BlackConstantVol inheritance hierarchy."""
    ref_date = ql.Date(15, 6, 2024)
    bcv = ql.BlackConstantVol(ref_date, ql.TARGET(), 0.20, ql.Actual365Fixed())

    assert isinstance(bcv, ql.BlackConstantVol)
    assert isinstance(bcv, ql.base.BlackVolTermStructure)
    assert isinstance(bcv, ql.base.VolatilityTermStructure)
    assert isinstance(bcv, ql.base.TermStructure)


def test_blackconstantvol_blackvol():
    """Test blackVol returns constant volatility."""
    ref_date = ql.Date(15, 6, 2024)
    volatility = 0.25
    bcv = ql.BlackConstantVol(ref_date, ql.TARGET(), volatility, ql.Actual365Fixed())

    future_date = ref_date + ql.Period(1, ql.Years)
    strike = 100.0

    assert bcv.blackVol(future_date, strike) == pytest.approx(volatility)
    assert bcv.blackVol(2.0, strike) == pytest.approx(volatility)


def test_blackconstantvol_blackvariance():
    """Test blackVariance calculation."""
    ref_date = ql.Date(15, 6, 2024)
    volatility = 0.20
    dc = ql.Actual365Fixed()
    bcv = ql.BlackConstantVol(ref_date, ql.TARGET(), volatility, dc)

    future_date = ref_date + ql.Period(2, ql.Years)
    time = dc.yearFraction(ref_date, future_date)
    strike = 100.0

    expected_variance = volatility * volatility * time
    assert bcv.blackVariance(future_date, strike) == pytest.approx(expected_variance)


def test_blackconstantvol_with_quote_handle():
    """Test BlackConstantVol with quote handle updates automatically."""
    ref_date = ql.Date(15, 6, 2024)
    dc = ql.Actual365Fixed()

    initial_vol = 0.20
    vol_quote = ql.SimpleQuote(initial_vol)
    vol_handle = ql.QuoteHandle(vol_quote)

    bcv = ql.BlackConstantVol(ref_date, ql.TARGET(), vol_handle, dc)

    strike = 100.0
    assert bcv.blackVol(1.0, strike) == pytest.approx(initial_vol)

    # Change quote value
    new_vol = 0.30
    vol_quote.setValue(new_vol)

    assert bcv.blackVol(1.0, strike) == pytest.approx(new_vol)


def test_blackconstantvol_settlement_days():
    """Test BlackConstantVol construction with settlement days."""
    today = ql.Date(15, 6, 2024)
    ql.Settings.instance().evaluationDate = today
    
    calendar = ql.TARGET()
    volatility = 0.25
    dc = ql.Actual365Fixed()

    bcv = ql.BlackConstantVol(2, calendar, volatility, dc)

    # Reference date should be 2 business days from evaluation date
    expected_ref = calendar.advance(today, 2, ql.Days)
    assert bcv.referenceDate() == expected_ref


def test_blackconstantvol_in_handle():
    """Test BlackConstantVol works with BlackVolTermStructureHandle."""
    ref_date = ql.Date(15, 6, 2024)
    volatility = 0.25
    bcv = ql.BlackConstantVol(ref_date, ql.TARGET(), volatility, ql.Actual365Fixed())

    handle = ql.BlackVolTermStructureHandle(bcv)
    assert not handle.empty()

    retrieved = handle.currentLink()
    assert retrieved.blackVol(1.0, 100.0) == pytest.approx(volatility)
