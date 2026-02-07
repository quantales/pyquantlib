"""
Tests for RFR (risk-free rate) index bindings.

Corresponds to src/indexes/ibor/*.cpp bindings:
- sofr.cpp (Sofr)
- estr.cpp (Estr)
- sonia.cpp (Sonia)

And src/indexes/swapindex.cpp:
- SwapIndex
- OvernightIndexedSwapIndex
"""

import pytest

import pyquantlib as ql


# =============================================================================
# Fixtures
# =============================================================================


@pytest.fixture(scope="module")
def flat_curve():
    """Flat yield curve for index tests."""
    today = ql.Date(15, ql.January, 2025)
    ql.Settings.evaluationDate = today
    curve = ql.FlatForward(today, 0.035, ql.Actual365Fixed())
    return {"today": today, "curve": curve}


# =============================================================================
# SOFR
# =============================================================================


def test_sofr_construction():
    """Test Sofr construction without curve."""
    sofr = ql.Sofr()
    assert sofr is not None
    assert "SOFR" in sofr.name()


def test_sofr_with_curve(flat_curve):
    """Test Sofr construction with forwarding curve."""
    sofr = ql.Sofr(flat_curve["curve"])
    assert sofr is not None
    assert "SOFR" in sofr.name()


def test_sofr_properties():
    """Test Sofr index properties."""
    sofr = ql.Sofr()
    assert sofr.fixingDays() == 0
    assert sofr.dayCounter() == ql.Actual360()


# =============================================================================
# ESTR
# =============================================================================


def test_estr_construction():
    """Test Estr construction without curve."""
    estr = ql.Estr()
    assert estr is not None
    assert "ESTR" in estr.name()


def test_estr_with_curve(flat_curve):
    """Test Estr construction with forwarding curve."""
    estr = ql.Estr(flat_curve["curve"])
    assert estr is not None


def test_estr_properties():
    """Test Estr index properties."""
    estr = ql.Estr()
    assert estr.fixingDays() == 0
    assert estr.dayCounter() == ql.Actual360()


# =============================================================================
# SONIA
# =============================================================================


def test_sonia_construction():
    """Test Sonia construction without curve."""
    sonia = ql.Sonia()
    assert sonia is not None
    assert "Sonia" in sonia.name()


def test_sonia_with_curve(flat_curve):
    """Test Sonia construction with forwarding curve."""
    sonia = ql.Sonia(flat_curve["curve"])
    assert sonia is not None


def test_sonia_properties():
    """Test Sonia index properties."""
    sonia = ql.Sonia()
    assert sonia.fixingDays() == 0
    assert sonia.dayCounter() == ql.Actual365Fixed()


# =============================================================================
# SwapIndex
# =============================================================================


def test_swapindex_construction(flat_curve):
    """Test SwapIndex construction."""
    euribor6m = ql.Euribor(ql.Period(6, ql.Months), flat_curve["curve"])
    swap_index = ql.SwapIndex(
        "EurSwap", ql.Period(5, ql.Years), 2,
        ql.EURCurrency(), ql.TARGET(),
        ql.Period(1, ql.Years), ql.Unadjusted,
        ql.Thirty360(ql.Thirty360.BondBasis),
        euribor6m,
    )
    assert swap_index is not None
    assert swap_index.fixedLegConvention() == ql.Unadjusted


def test_swapindex_with_discount(flat_curve):
    """Test SwapIndex construction with discounting curve."""
    euribor6m = ql.Euribor(ql.Period(6, ql.Months), flat_curve["curve"])
    swap_index = ql.SwapIndex(
        "EurSwap", ql.Period(5, ql.Years), 2,
        ql.EURCurrency(), ql.TARGET(),
        ql.Period(1, ql.Years), ql.Unadjusted,
        ql.Thirty360(ql.Thirty360.BondBasis),
        euribor6m, flat_curve["curve"],
    )
    assert swap_index is not None
    assert swap_index.exogenousDiscount()


def test_swapindex_properties(flat_curve):
    """Test SwapIndex property accessors."""
    euribor6m = ql.Euribor(ql.Period(6, ql.Months), flat_curve["curve"])
    swap_index = ql.SwapIndex(
        "EurSwap", ql.Period(5, ql.Years), 2,
        ql.EURCurrency(), ql.TARGET(),
        ql.Period(1, ql.Years), ql.Unadjusted,
        ql.Thirty360(ql.Thirty360.BondBasis),
        euribor6m,
    )
    assert swap_index.fixedLegTenor() == ql.Period(1, ql.Years)
    assert swap_index.iborIndex() is not None
    assert not swap_index.exogenousDiscount()


# =============================================================================
# OvernightIndexedSwapIndex
# =============================================================================


def test_overnightindexedswapindex_construction(flat_curve):
    """Test OvernightIndexedSwapIndex construction."""
    estr = ql.Estr(flat_curve["curve"])
    ois_index = ql.OvernightIndexedSwapIndex(
        "EstrSwap", ql.Period(1, ql.Years), 2,
        ql.EURCurrency(), estr,
    )
    assert ois_index is not None


def test_overnightindexedswapindex_with_averaging(flat_curve):
    """Test OvernightIndexedSwapIndex with explicit averaging."""
    sofr = ql.Sofr(flat_curve["curve"])
    ois_index = ql.OvernightIndexedSwapIndex(
        "SofrSwap", ql.Period(2, ql.Years), 2,
        ql.USDCurrency(), sofr,
        telescopicValueDates=True,
        averagingMethod=ql.RateAveraging.Type.Simple,
    )
    assert ois_index is not None
