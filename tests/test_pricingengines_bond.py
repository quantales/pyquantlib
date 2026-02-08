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


# =============================================================================
# DurationType
# =============================================================================


def test_durationtype_values():
    """Test DurationType enum values."""
    assert ql.DurationType.Simple is not None
    assert ql.DurationType.Macaulay is not None
    assert ql.DurationType.Modified is not None


# =============================================================================
# BondFunctions
# =============================================================================


def test_bondfunctions_exists():
    """Test BondFunctions class exists."""
    assert hasattr(ql, "BondFunctions")


def test_bondfunctions_cleanprice(bond_env):
    """Test BondFunctions.cleanPrice."""
    bond = ql.FixedRateBond(
        2, 100.0, bond_env["schedule"], [0.05],
        ql.Thirty360(ql.Thirty360.BondBasis),
    )
    price = ql.BondFunctions.cleanPrice(
        bond, bond_env["flat_curve"], bond_env["today"],
    )
    assert price == pytest.approx(104.07, abs=0.1)


def test_bondfunctions_dirtyprice(bond_env):
    """Test BondFunctions.dirtyPrice."""
    bond = ql.FixedRateBond(
        2, 100.0, bond_env["schedule"], [0.05],
        ql.Thirty360(ql.Thirty360.BondBasis),
    )
    price = ql.BondFunctions.dirtyPrice(
        bond, bond_env["flat_curve"], bond_env["today"],
    )
    assert price > 0


def test_bondfunctions_bps(bond_env):
    """Test BondFunctions.bps."""
    bond = ql.FixedRateBond(
        2, 100.0, bond_env["schedule"], [0.05],
        ql.Thirty360(ql.Thirty360.BondBasis),
    )
    bps = ql.BondFunctions.bps(
        bond, bond_env["flat_curve"], bond_env["today"],
    )
    assert bps > 0


def test_bondfunctions_bond_yield(bond_env):
    """Test BondFunctions.bondYield."""
    bond = ql.FixedRateBond(
        2, 100.0, bond_env["schedule"], [0.05],
        ql.Thirty360(ql.Thirty360.BondBasis),
    )
    engine = ql.DiscountingBondEngine(bond_env["curve_handle"])
    bond.setPricingEngine(engine)

    price = ql.BondPrice(bond.cleanPrice(), ql.BondPriceType.Clean)
    y = ql.BondFunctions.bondYield(
        bond, price, ql.Actual365Fixed(), ql.Compounded, ql.Annual,
    )
    assert 0 < y < 0.2


def test_bondfunctions_duration(bond_env):
    """Test BondFunctions.duration."""
    bond = ql.FixedRateBond(
        2, 100.0, bond_env["schedule"], [0.05],
        ql.Thirty360(ql.Thirty360.BondBasis),
    )
    dur = ql.BondFunctions.duration(
        bond, 0.04, ql.Actual365Fixed(), ql.Compounded, ql.Annual,
        ql.DurationType.Modified,
    )
    assert dur > 0
    assert dur < 10  # 5Y bond, duration < 10


def test_bondfunctions_convexity(bond_env):
    """Test BondFunctions.convexity."""
    bond = ql.FixedRateBond(
        2, 100.0, bond_env["schedule"], [0.05],
        ql.Thirty360(ql.Thirty360.BondBasis),
    )
    conv = ql.BondFunctions.convexity(
        bond, 0.04, ql.Actual365Fixed(), ql.Compounded, ql.Annual,
    )
    assert conv > 0


def test_bondfunctions_basis_point_value(bond_env):
    """Test BondFunctions.basisPointValue."""
    bond = ql.FixedRateBond(
        2, 100.0, bond_env["schedule"], [0.05],
        ql.Thirty360(ql.Thirty360.BondBasis),
    )
    bpv = ql.BondFunctions.basisPointValue(
        bond, 0.04, ql.Actual365Fixed(), ql.Compounded, ql.Annual,
    )
    assert bpv == pytest.approx(-0.04574, abs=1e-4)


def test_bondfunctions_yield_value_basis_point(bond_env):
    """Test BondFunctions.yieldValueBasisPoint."""
    bond = ql.FixedRateBond(
        2, 100.0, bond_env["schedule"], [0.05],
        ql.Thirty360(ql.Thirty360.BondBasis),
    )
    yvbp = ql.BondFunctions.yieldValueBasisPoint(
        bond, 0.04, ql.Actual365Fixed(), ql.Compounded, ql.Annual,
    )
    assert yvbp == pytest.approx(-2.186e-5, abs=1e-7)


def test_bondfunctions_macaulay_vs_modified(bond_env):
    """Test Macaulay duration > Modified duration."""
    bond = ql.FixedRateBond(
        2, 100.0, bond_env["schedule"], [0.05],
        ql.Thirty360(ql.Thirty360.BondBasis),
    )
    mac = ql.BondFunctions.duration(
        bond, 0.04, ql.Actual365Fixed(), ql.Compounded, ql.Annual,
        ql.DurationType.Macaulay,
    )
    mod = ql.BondFunctions.duration(
        bond, 0.04, ql.Actual365Fixed(), ql.Compounded, ql.Annual,
        ql.DurationType.Modified,
    )
    assert mac > mod


def test_bondfunctions_zspread(bond_env):
    """Test BondFunctions.zSpread."""
    bond = ql.FixedRateBond(
        2, 100.0, bond_env["schedule"], [0.05],
        ql.Thirty360(ql.Thirty360.BondBasis),
    )
    engine = ql.DiscountingBondEngine(bond_env["curve_handle"])
    bond.setPricingEngine(engine)

    price = ql.BondPrice(bond.cleanPrice(), ql.BondPriceType.Clean)
    z = ql.BondFunctions.zSpread(
        bond, price, bond_env["flat_curve"],
        ql.Actual365Fixed(), ql.Compounded, ql.Annual,
    )
    # z-spread over the same curve used for pricing should be ~0
    assert abs(z) < 0.001
