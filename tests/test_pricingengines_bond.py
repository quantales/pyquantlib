"""
Tests for bond pricing engine bindings.

Corresponds to src/pricingengines/bond/*.cpp bindings.
"""

import pytest

import pyquantlib as ql


# =============================================================================
# Fixtures
# =============================================================================


@pytest.fixture(scope="module")
def bond_env():
    """Common data for bond engine tests."""
    original_date = ql.Settings.instance().evaluationDate
    today = ql.Date(15, ql.January, 2025)
    ql.Settings.instance().evaluationDate = today

    day_counter = ql.Actual365Fixed()

    flat_curve = ql.FlatForward(today, 0.04, day_counter)
    curve_handle = ql.YieldTermStructureHandle(flat_curve)

    calendar = ql.TARGET()
    maturity_date = ql.Date(15, ql.January, 2030)

    schedule = ql.Schedule(
        today, maturity_date,
        ql.Period(ql.Annual), calendar,
        ql.Unadjusted, ql.Unadjusted,
        ql.DateGeneration.Backward, False
    )

    yield {
        "today": today,
        "flat_curve": flat_curve,
        "curve_handle": curve_handle,
        "schedule": schedule,
        "maturity_date": maturity_date,
        "calendar": calendar,
    }

    ql.Settings.instance().evaluationDate = original_date


# =============================================================================
# DiscountingBondEngine
# =============================================================================


def test_discountingbondengine_exists():
    """Test DiscountingBondEngine class exists."""
    assert hasattr(ql, "DiscountingBondEngine")


def test_discountingbondengine_handle(bond_env):
    """Test DiscountingBondEngine with handle."""
    engine = ql.DiscountingBondEngine(bond_env["curve_handle"])
    assert engine is not None


def test_discountingbondengine_hidden_handle(bond_env):
    """Test DiscountingBondEngine with term structure (hidden handle)."""
    engine = ql.DiscountingBondEngine(bond_env["flat_curve"])
    assert engine is not None


def test_discountingbondengine_discount_curve(bond_env):
    """Test DiscountingBondEngine discount curve accessor."""
    engine = ql.DiscountingBondEngine(bond_env["curve_handle"])
    curve = engine.discountCurve()
    assert curve is not None


def test_discountingbondengine_pricing(bond_env):
    """Test DiscountingBondEngine prices a bond correctly."""
    bond = ql.FixedRateBond(
        2, 100.0, bond_env["schedule"], [0.05],
        ql.Thirty360(ql.Thirty360.BondBasis)
    )
    engine = ql.DiscountingBondEngine(bond_env["curve_handle"])
    bond.setPricingEngine(engine)

    # 5% coupon, 4% discount -> price above par
    assert bond.NPV() == pytest.approx(104.0707, abs=0.01)
    assert bond.cleanPrice() == pytest.approx(104.0658, abs=0.01)
    assert bond.dirtyPrice() == pytest.approx(104.0935, abs=0.01)
