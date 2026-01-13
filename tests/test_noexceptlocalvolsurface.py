import pytest

import pyquantlib as ql


def test_noexceptlocalvolsurface_exists():
    """Verify NoExceptLocalVolSurface is in main module."""
    assert hasattr(ql, 'NoExceptLocalVolSurface')


def test_noexceptlocalvolsurface_construction():
    """Test NoExceptLocalVolSurface construction."""
    ref_date = ql.Date(15, 6, 2024)
    ql.Settings.instance().evaluationDate = ref_date
    dc = ql.Actual365Fixed()
    calendar = ql.TARGET()

    # Create underlying term structures
    spot = 100.0
    risk_free_rate = 0.05
    dividend_yield = 0.02
    black_vol = 0.20
    fallback_vol = 0.15

    spot_quote = ql.SimpleQuote(spot)
    risk_free = ql.FlatForward(ref_date, risk_free_rate, dc)
    dividend = ql.FlatForward(ref_date, dividend_yield, dc)
    black_vol_surface = ql.BlackConstantVol(ref_date, calendar, black_vol, dc)

    spot_handle = ql.QuoteHandle(spot_quote)
    risk_free_handle = ql.YieldTermStructureHandle(risk_free)
    dividend_handle = ql.YieldTermStructureHandle(dividend)
    black_vol_handle = ql.BlackVolTermStructureHandle(black_vol_surface)

    nelvs = ql.NoExceptLocalVolSurface(
        black_vol_handle, risk_free_handle, dividend_handle,
        spot_handle, fallback_vol
    )

    assert nelvs.referenceDate() == ref_date


def test_noexceptlocalvolsurface_inheritance():
    """Test NoExceptLocalVolSurface inheritance hierarchy."""
    ref_date = ql.Date(15, 6, 2024)
    ql.Settings.instance().evaluationDate = ref_date
    dc = ql.Actual365Fixed()

    risk_free = ql.FlatForward(ref_date, 0.05, dc)
    dividend = ql.FlatForward(ref_date, 0.02, dc)
    black_vol = ql.BlackConstantVol(ref_date, ql.TARGET(), 0.20, dc)

    nelvs = ql.NoExceptLocalVolSurface(
        ql.BlackVolTermStructureHandle(black_vol),
        ql.YieldTermStructureHandle(risk_free),
        ql.YieldTermStructureHandle(dividend),
        100.0, 0.15
    )

    assert isinstance(nelvs, ql.NoExceptLocalVolSurface)
    assert isinstance(nelvs, ql.LocalVolSurface)
    assert isinstance(nelvs, ql.base.LocalVolTermStructure)


def test_noexceptlocalvolsurface_localvol():
    """Test local vol calculation with fallback."""
    ref_date = ql.Date(15, 6, 2024)
    ql.Settings.instance().evaluationDate = ref_date
    dc = ql.Actual365Fixed()
    calendar = ql.TARGET()

    black_vol = 0.20
    fallback_vol = 0.15

    risk_free = ql.FlatForward(ref_date, 0.05, dc)
    dividend = ql.FlatForward(ref_date, 0.02, dc)
    black_vol_surface = ql.BlackConstantVol(ref_date, calendar, black_vol, dc)

    nelvs = ql.NoExceptLocalVolSurface(
        ql.BlackVolTermStructureHandle(black_vol_surface),
        ql.YieldTermStructureHandle(risk_free),
        ql.YieldTermStructureHandle(dividend),
        100.0, fallback_vol
    )

    # For flat Black vol, local vol equals Black vol
    future_date = ref_date + ql.Period(1, ql.Years)
    vol = nelvs.localVol(future_date, 100.0)
    assert vol == pytest.approx(black_vol)


def test_noexceptlocalvolsurface_with_quote_handle():
    """Test NoExceptLocalVolSurface with quote handle for underlying."""
    ref_date = ql.Date(15, 6, 2024)
    ql.Settings.instance().evaluationDate = ref_date
    dc = ql.Actual365Fixed()

    spot_quote = ql.SimpleQuote(100.0)
    risk_free = ql.FlatForward(ref_date, 0.05, dc)
    dividend = ql.FlatForward(ref_date, 0.02, dc)
    black_vol = ql.BlackConstantVol(ref_date, ql.TARGET(), 0.20, dc)

    nelvs = ql.NoExceptLocalVolSurface(
        ql.BlackVolTermStructureHandle(black_vol),
        ql.YieldTermStructureHandle(risk_free),
        ql.YieldTermStructureHandle(dividend),
        ql.QuoteHandle(spot_quote),
        0.15
    )

    assert nelvs is not None
    assert nelvs.localVol(1.0, 100.0) == pytest.approx(0.20)


def test_noexceptlocalvolsurface_in_handle():
    """Test NoExceptLocalVolSurface works with LocalVolTermStructureHandle."""
    ref_date = ql.Date(15, 6, 2024)
    ql.Settings.instance().evaluationDate = ref_date
    dc = ql.Actual365Fixed()

    risk_free = ql.FlatForward(ref_date, 0.05, dc)
    dividend = ql.FlatForward(ref_date, 0.02, dc)
    black_vol = ql.BlackConstantVol(ref_date, ql.TARGET(), 0.20, dc)

    nelvs = ql.NoExceptLocalVolSurface(
        ql.BlackVolTermStructureHandle(black_vol),
        ql.YieldTermStructureHandle(risk_free),
        ql.YieldTermStructureHandle(dividend),
        100.0, 0.15
    )

    handle = ql.LocalVolTermStructureHandle(nelvs)
    assert not handle.empty()

    retrieved = handle.currentLink()
    assert retrieved.localVol(1.0, 100.0) == pytest.approx(0.20)
