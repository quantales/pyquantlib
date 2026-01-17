import pytest

import pyquantlib as ql


def test_localvolsurface_exists():
    """Verify LocalVolSurface is in main module."""
    assert hasattr(ql, 'LocalVolSurface')


def test_localvolsurface_construction():
    """Test LocalVolSurface construction from Black vol surface."""
    ref_date = ql.Date(15, 6, 2024)
    ql.Settings.instance().evaluationDate = ref_date
    dc = ql.Actual365Fixed()
    calendar = ql.TARGET()

    # Create underlying term structures
    spot = 100.0
    risk_free_rate = 0.05
    dividend_yield = 0.02
    black_vol = 0.20

    spot_quote = ql.SimpleQuote(spot)
    risk_free = ql.FlatForward(ref_date, risk_free_rate, dc)
    dividend = ql.FlatForward(ref_date, dividend_yield, dc)
    black_vol_surface = ql.BlackConstantVol(ref_date, calendar, black_vol, dc)

    spot_handle = ql.QuoteHandle(spot_quote)
    risk_free_handle = ql.YieldTermStructureHandle(risk_free)
    dividend_handle = ql.YieldTermStructureHandle(dividend)
    black_vol_handle = ql.BlackVolTermStructureHandle(black_vol_surface)

    lvs = ql.LocalVolSurface(black_vol_handle, risk_free_handle,
                              dividend_handle, spot_handle)

    assert lvs.referenceDate() == ref_date


def test_localvolsurface_inheritance():
    """Test LocalVolSurface inheritance hierarchy."""
    ref_date = ql.Date(15, 6, 2024)
    ql.Settings.instance().evaluationDate = ref_date
    dc = ql.Actual365Fixed()

    risk_free = ql.FlatForward(ref_date, 0.05, dc)
    dividend = ql.FlatForward(ref_date, 0.02, dc)
    black_vol = ql.BlackConstantVol(ref_date, ql.TARGET(), 0.20, dc)

    lvs = ql.LocalVolSurface(
        ql.BlackVolTermStructureHandle(black_vol),
        ql.YieldTermStructureHandle(risk_free),
        ql.YieldTermStructureHandle(dividend),
        100.0
    )

    assert isinstance(lvs, ql.LocalVolSurface)
    assert isinstance(lvs, ql.base.LocalVolTermStructure)
    assert isinstance(lvs, ql.base.VolatilityTermStructure)


def test_localvolsurface_flat_vol():
    """Test local vol equals Black vol for constant Black vol surface."""
    ref_date = ql.Date(15, 6, 2024)
    ql.Settings.instance().evaluationDate = ref_date
    dc = ql.Actual365Fixed()
    calendar = ql.TARGET()

    black_vol = 0.20
    risk_free = ql.FlatForward(ref_date, 0.05, dc)
    dividend = ql.FlatForward(ref_date, 0.02, dc)
    black_vol_surface = ql.BlackConstantVol(ref_date, calendar, black_vol, dc)

    lvs = ql.LocalVolSurface(
        ql.BlackVolTermStructureHandle(black_vol_surface),
        ql.YieldTermStructureHandle(risk_free),
        ql.YieldTermStructureHandle(dividend),
        100.0
    )

    # For flat Black vol, local vol equals Black vol
    future_date = ref_date + ql.Period(1, ql.Years)
    assert lvs.localVol(future_date, 100.0) == pytest.approx(black_vol)


def test_localvolsurface_updates_with_quote():
    """Test LocalVolSurface updates when Black vol quote changes."""
    ref_date = ql.Date(15, 6, 2024)
    ql.Settings.instance().evaluationDate = ref_date
    dc = ql.Actual365Fixed()
    calendar = ql.TARGET()

    initial_vol = 0.20
    vol_quote = ql.SimpleQuote(initial_vol)
    vol_handle = ql.QuoteHandle(vol_quote)

    risk_free = ql.FlatForward(ref_date, 0.05, dc)
    dividend = ql.FlatForward(ref_date, 0.02, dc)
    black_vol_surface = ql.BlackConstantVol(ref_date, calendar, vol_handle, dc)

    lvs = ql.LocalVolSurface(
        ql.BlackVolTermStructureHandle(black_vol_surface),
        ql.YieldTermStructureHandle(risk_free),
        ql.YieldTermStructureHandle(dividend),
        100.0
    )

    future_date = ref_date + ql.Period(1, ql.Years)
    assert lvs.localVol(future_date, 100.0) == pytest.approx(initial_vol)

    # Change vol quote
    new_vol = 0.25
    vol_quote.setValue(new_vol)
    assert lvs.localVol(future_date, 100.0) == pytest.approx(new_vol)


def test_localvolsurface_with_fixed_underlying():
    """Test LocalVolSurface construction with fixed underlying value."""
    ref_date = ql.Date(15, 6, 2024)
    ql.Settings.instance().evaluationDate = ref_date
    dc = ql.Actual365Fixed()

    risk_free = ql.FlatForward(ref_date, 0.05, dc)
    dividend = ql.FlatForward(ref_date, 0.02, dc)
    black_vol = ql.BlackConstantVol(ref_date, ql.TARGET(), 0.20, dc)

    # Use fixed Real value instead of quote handle
    lvs = ql.LocalVolSurface(
        ql.BlackVolTermStructureHandle(black_vol),
        ql.YieldTermStructureHandle(risk_free),
        ql.YieldTermStructureHandle(dividend),
        100.0  # Fixed underlying
    )

    assert lvs is not None
    assert lvs.localVol(1.0, 100.0) == pytest.approx(0.20)


def test_localvolsurface_in_handle():
    """Test LocalVolSurface works with LocalVolTermStructureHandle."""
    ref_date = ql.Date(15, 6, 2024)
    ql.Settings.instance().evaluationDate = ref_date
    dc = ql.Actual365Fixed()

    risk_free = ql.FlatForward(ref_date, 0.05, dc)
    dividend = ql.FlatForward(ref_date, 0.02, dc)
    black_vol = ql.BlackConstantVol(ref_date, ql.TARGET(), 0.20, dc)

    lvs = ql.LocalVolSurface(
        ql.BlackVolTermStructureHandle(black_vol),
        ql.YieldTermStructureHandle(risk_free),
        ql.YieldTermStructureHandle(dividend),
        100.0
    )

    handle = ql.LocalVolTermStructureHandle(lvs)
    assert not handle.empty()

    retrieved = handle.currentLink()
    assert retrieved.localVol(1.0, 100.0) == pytest.approx(0.20)


def test_localvolsurface_hidden_handles_with_quote():
    """Test LocalVolSurface with term structures (hidden handles) and quote."""
    ref_date = ql.Date(15, 6, 2024)
    ql.Settings.instance().evaluationDate = ref_date
    dc = ql.Actual365Fixed()

    spot_quote = ql.SimpleQuote(100.0)
    risk_free = ql.FlatForward(ref_date, 0.05, dc)
    dividend = ql.FlatForward(ref_date, 0.02, dc)
    black_vol = ql.BlackConstantVol(ref_date, ql.TARGET(), 0.20, dc)

    # Hidden handles: pass term structures directly
    lvs = ql.LocalVolSurface(black_vol, risk_free, dividend, spot_quote)

    assert lvs.localVol(1.0, 100.0) == pytest.approx(0.20)

    # Quote changes propagate
    spot_quote.setValue(110.0)
    # Local vol should still work (may differ slightly due to spot change)
    assert lvs.localVol(1.0, 100.0) == pytest.approx(0.20, rel=0.01)


def test_localvolsurface_hidden_handles_with_fixed_value():
    """Test LocalVolSurface with term structures (hidden handles) and fixed value."""
    ref_date = ql.Date(15, 6, 2024)
    ql.Settings.instance().evaluationDate = ref_date
    dc = ql.Actual365Fixed()

    risk_free = ql.FlatForward(ref_date, 0.05, dc)
    dividend = ql.FlatForward(ref_date, 0.02, dc)
    black_vol = ql.BlackConstantVol(ref_date, ql.TARGET(), 0.20, dc)

    # Hidden handles with fixed underlying value
    lvs = ql.LocalVolSurface(black_vol, risk_free, dividend, 100.0)

    assert lvs.localVol(1.0, 100.0) == pytest.approx(0.20)
