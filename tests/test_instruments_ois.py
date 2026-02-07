"""
Tests for OvernightIndexedSwap binding.

Corresponds to src/instruments/overnightindexedswap.cpp.
"""

import pytest

import pyquantlib as ql


# =============================================================================
# Fixtures
# =============================================================================


@pytest.fixture(scope="module")
def ois_setup():
    """Setup for OIS tests: curve, index, schedule."""
    today = ql.Date(15, ql.January, 2025)
    ql.Settings.evaluationDate = today

    curve = ql.FlatForward(today, 0.035, ql.Actual365Fixed())
    sofr = ql.Sofr(curve)

    schedule = ql.Schedule(
        ql.Date(17, ql.January, 2025),
        ql.Date(17, ql.January, 2026),
        ql.Period(3, ql.Months),
        ql.UnitedStates(ql.UnitedStates.GovernmentBond),
        ql.ModifiedFollowing,
        ql.ModifiedFollowing,
        ql.DateGeneration.Forward,
        False,
    )

    return {
        "today": today,
        "curve": curve,
        "sofr": sofr,
        "schedule": schedule,
    }


# =============================================================================
# OvernightIndexedSwap
# =============================================================================


def test_overnightindexedswap_construction(ois_setup):
    """Test OvernightIndexedSwap single-schedule construction."""
    ois = ql.OvernightIndexedSwap(
        ql.SwapType.Receiver,
        1_000_000.0,
        ois_setup["schedule"],
        0.035,
        ql.Actual360(),
        ois_setup["sofr"],
    )
    assert ois is not None


def test_overnightindexedswap_two_schedules(ois_setup):
    """Test OvernightIndexedSwap with separate fixed and overnight schedules."""
    ois = ql.OvernightIndexedSwap(
        ql.SwapType.Payer,
        1_000_000.0,
        ois_setup["schedule"],
        0.035,
        ql.Actual360(),
        ois_setup["schedule"],
        ois_setup["sofr"],
    )
    assert ois is not None


def test_overnightindexedswap_overnight_index(ois_setup):
    """Test overnightIndex accessor."""
    ois = ql.OvernightIndexedSwap(
        ql.SwapType.Receiver,
        1_000_000.0,
        ois_setup["schedule"],
        0.035,
        ql.Actual360(),
        ois_setup["sofr"],
    )
    idx = ois.overnightIndex()
    assert idx is not None
    assert "SOFR" in idx.name()


def test_overnightindexedswap_averaging_method(ois_setup):
    """Test averagingMethod accessor."""
    ois = ql.OvernightIndexedSwap(
        ql.SwapType.Receiver,
        1_000_000.0,
        ois_setup["schedule"],
        0.035,
        ql.Actual360(),
        ois_setup["sofr"],
        averagingMethod=ql.RateAveraging.Type.Simple,
    )
    assert ois.averagingMethod() == ql.RateAveraging.Type.Simple


def test_overnightindexedswap_default_averaging(ois_setup):
    """Test that default averaging method is Compound."""
    ois = ql.OvernightIndexedSwap(
        ql.SwapType.Receiver,
        1_000_000.0,
        ois_setup["schedule"],
        0.035,
        ql.Actual360(),
        ois_setup["sofr"],
    )
    assert ois.averagingMethod() == ql.RateAveraging.Type.Compound


def test_overnightindexedswap_pricing(ois_setup):
    """Test OIS pricing with DiscountingSwapEngine."""
    ois = ql.OvernightIndexedSwap(
        ql.SwapType.Receiver,
        1_000_000.0,
        ois_setup["schedule"],
        0.035,
        ql.Actual360(),
        ois_setup["sofr"],
    )
    engine = ql.DiscountingSwapEngine(ois_setup["curve"])
    ois.setPricingEngine(engine)

    npv = ois.NPV()
    # With at-market rate ~= curve rate, NPV should be small but well-defined
    assert isinstance(npv, float)
    assert abs(npv) < 50_000  # reasonable bound for 1M notional

    fair_rate = ois.fairRate()
    assert fair_rate == pytest.approx(0.035, abs=0.005)


def test_overnightindexedswap_leg_npv(ois_setup):
    """Test fixed and overnight leg NPV accessors."""
    ois = ql.OvernightIndexedSwap(
        ql.SwapType.Receiver,
        1_000_000.0,
        ois_setup["schedule"],
        0.035,
        ql.Actual360(),
        ois_setup["sofr"],
    )
    engine = ql.DiscountingSwapEngine(ois_setup["curve"])
    ois.setPricingEngine(engine)

    fixed_npv = ois.fixedLegNPV()
    overnight_npv = ois.overnightLegNPV()
    assert isinstance(fixed_npv, float)
    assert isinstance(overnight_npv, float)
    # NPV = fixedLegNPV + overnightLegNPV (for receiver: +fixed -float)
    assert ois.NPV() == pytest.approx(fixed_npv + overnight_npv, abs=1e-6)


def test_overnightindexedswap_overnight_leg(ois_setup):
    """Test overnightLeg returns cash flows."""
    ois = ql.OvernightIndexedSwap(
        ql.SwapType.Receiver,
        1_000_000.0,
        ois_setup["schedule"],
        0.035,
        ql.Actual360(),
        ois_setup["sofr"],
    )
    leg = ois.overnightLeg()
    assert len(leg) > 0
