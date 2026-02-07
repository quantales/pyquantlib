"""
Tests for bond subtype bindings.

Corresponds to src/instruments/bonds/*.cpp bindings.
"""

import pytest

import pyquantlib as ql


# =============================================================================
# Fixtures
# =============================================================================


@pytest.fixture(scope="module")
def bond_env():
    """Common data for bond tests."""
    original_date = ql.Settings.instance().evaluationDate
    today = ql.Date(15, ql.January, 2025)
    ql.Settings.instance().evaluationDate = today

    calendar = ql.TARGET()
    day_counter = ql.Actual365Fixed()

    # Flat curve at 4%
    flat_curve = ql.FlatForward(today, 0.04, day_counter)
    curve_handle = ql.YieldTermStructureHandle(flat_curve)

    # Schedule for a 5-year bond
    issue_date = ql.Date(15, ql.January, 2025)
    maturity_date = ql.Date(15, ql.January, 2030)

    schedule = ql.Schedule(
        issue_date, maturity_date,
        ql.Period(ql.Annual), calendar,
        ql.Unadjusted, ql.Unadjusted,
        ql.DateGeneration.Backward, False
    )

    yield {
        "today": today,
        "calendar": calendar,
        "day_counter": day_counter,
        "flat_curve": flat_curve,
        "curve_handle": curve_handle,
        "issue_date": issue_date,
        "maturity_date": maturity_date,
        "schedule": schedule,
    }

    ql.Settings.instance().evaluationDate = original_date


# =============================================================================
# ZeroCouponBond
# =============================================================================


def test_zerocouponbond_construction(bond_env):
    """Test ZeroCouponBond construction."""
    bond = ql.ZeroCouponBond(
        2, bond_env["calendar"], 100.0, bond_env["maturity_date"],
        ql.Following, 100.0, bond_env["issue_date"]
    )
    assert bond is not None
    assert bond.maturityDate() == bond_env["maturity_date"]
    assert bond.issueDate() == bond_env["issue_date"]


def test_zerocouponbond_pricing(bond_env):
    """Test ZeroCouponBond pricing with DiscountingBondEngine."""
    bond = ql.ZeroCouponBond(
        2, bond_env["calendar"], 100.0, bond_env["maturity_date"],
        ql.Following, 100.0, bond_env["issue_date"]
    )
    engine = ql.DiscountingBondEngine(bond_env["curve_handle"])
    bond.setPricingEngine(engine)

    # 5-year zero at 4% discount
    assert bond.NPV() == pytest.approx(81.8641, abs=0.01)
    assert bond.cleanPrice() == pytest.approx(81.8820, abs=0.01)
    assert bond.dirtyPrice() == pytest.approx(81.8820, abs=0.01)


def test_zerocouponbond_settlement(bond_env):
    """Test ZeroCouponBond settlement properties."""
    bond = ql.ZeroCouponBond(
        2, bond_env["calendar"], 100.0, bond_env["maturity_date"],
        ql.Following, 100.0, bond_env["issue_date"]
    )
    assert bond.settlementDays() == 2
    assert bond.settlementDate() > bond_env["today"]


def test_zerocouponbond_notional(bond_env):
    """Test ZeroCouponBond notional."""
    bond = ql.ZeroCouponBond(
        2, bond_env["calendar"], 100.0, bond_env["maturity_date"]
    )
    assert bond.notional() == pytest.approx(100.0)


def test_zerocouponbond_cashflows(bond_env):
    """Test ZeroCouponBond has a redemption cashflow."""
    bond = ql.ZeroCouponBond(
        2, bond_env["calendar"], 100.0, bond_env["maturity_date"]
    )
    cashflows = bond.cashflows()
    assert len(cashflows) > 0

    redemption = bond.redemption()
    assert redemption.amount() == pytest.approx(100.0)


# =============================================================================
# FixedRateBond
# =============================================================================


def test_fixedratebond_construction(bond_env):
    """Test FixedRateBond construction."""
    bond = ql.FixedRateBond(
        2, 100.0, bond_env["schedule"], [0.05],
        ql.Thirty360(ql.Thirty360.BondBasis),
        issueDate=bond_env["issue_date"]
    )
    assert bond is not None
    assert bond.maturityDate() == bond_env["maturity_date"]
    assert bond.issueDate() == bond_env["issue_date"]


def test_fixedratebond_frequency(bond_env):
    """Test FixedRateBond frequency and day counter."""
    bond = ql.FixedRateBond(
        2, 100.0, bond_env["schedule"], [0.05],
        ql.Thirty360(ql.Thirty360.BondBasis)
    )
    assert bond.frequency() == ql.Annual
    assert "30/360" in bond.dayCounter().name()


def test_fixedratebond_pricing(bond_env):
    """Test FixedRateBond pricing."""
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


def test_fixedratebond_cleanprice_from_yield(bond_env):
    """Test FixedRateBond clean price from yield."""
    bond = ql.FixedRateBond(
        2, 100.0, bond_env["schedule"], [0.05],
        ql.Thirty360(ql.Thirty360.BondBasis)
    )

    # Price at par when yield == coupon
    price_at_par = bond.cleanPrice(
        0.05, ql.Thirty360(ql.Thirty360.BondBasis),
        ql.Compounded, ql.Annual
    )
    assert price_at_par == pytest.approx(100.0, abs=0.5)


def test_fixedratebond_yield(bond_env):
    """Test FixedRateBond yield calculation."""
    bond = ql.FixedRateBond(
        2, 100.0, bond_env["schedule"], [0.05],
        ql.Thirty360(ql.Thirty360.BondBasis)
    )
    engine = ql.DiscountingBondEngine(bond_env["curve_handle"])
    bond.setPricingEngine(engine)

    ytm = bond.bondYield(
        ql.Thirty360(ql.Thirty360.BondBasis),
        ql.Compounded, ql.Annual
    )
    # Yield should be close to the flat rate (4%)
    assert ytm == pytest.approx(0.04, abs=0.005)


def test_fixedratebond_yield_from_price(bond_env):
    """Test FixedRateBond yield from explicit price."""
    bond = ql.FixedRateBond(
        2, 100.0, bond_env["schedule"], [0.05],
        ql.Thirty360(ql.Thirty360.BondBasis)
    )

    price = ql.BondPrice(100.0, ql.BondPriceType.Clean)
    ytm = bond.bondYield(
        price, ql.Thirty360(ql.Thirty360.BondBasis),
        ql.Compounded, ql.Annual
    )
    # Yield at par should be close to coupon rate
    assert ytm == pytest.approx(0.05, abs=0.005)


def test_fixedratebond_accrued(bond_env):
    """Test FixedRateBond accrued amount."""
    bond = ql.FixedRateBond(
        2, 100.0, bond_env["schedule"], [0.05],
        ql.Thirty360(ql.Thirty360.BondBasis)
    )
    accrued = bond.accruedAmount()
    assert accrued >= 0.0


def test_fixedratebond_cashflows(bond_env):
    """Test FixedRateBond cashflows."""
    bond = ql.FixedRateBond(
        2, 100.0, bond_env["schedule"], [0.05],
        ql.Thirty360(ql.Thirty360.BondBasis)
    )
    cashflows = bond.cashflows()
    # 5 annual coupons + 1 redemption = 6 cashflows
    assert len(cashflows) == 6

    redemptions = bond.redemptions()
    assert len(redemptions) == 1
    assert redemptions[0].amount() == pytest.approx(100.0)


def test_fixedratebond_with_redemption(bond_env):
    """Test FixedRateBond with custom redemption."""
    bond = ql.FixedRateBond(
        2, 100.0, bond_env["schedule"], [0.05],
        ql.Thirty360(ql.Thirty360.BondBasis),
        ql.Following, 105.0  # premium redemption
    )
    redemption = bond.redemption()
    assert redemption.amount() == pytest.approx(105.0)


# =============================================================================
# FloatingRateBond
# =============================================================================


@pytest.fixture(scope="module")
def float_bond_env():
    """Environment for floating rate bond tests."""
    original_date = ql.Settings.instance().evaluationDate
    today = ql.Date(15, ql.January, 2025)
    ql.Settings.instance().evaluationDate = today

    calendar = ql.TARGET()
    day_counter = ql.Actual365Fixed()

    flat_curve = ql.FlatForward(today, 0.04, day_counter)
    curve_handle = ql.YieldTermStructureHandle(flat_curve)

    euribor6m = ql.Euribor6M(curve_handle)

    # Use future dates to avoid needing past fixings
    issue_date = calendar.advance(today, ql.Period("6M"))
    maturity_date = calendar.advance(issue_date, ql.Period("5Y"))

    schedule = ql.Schedule(
        issue_date, maturity_date,
        ql.Period(ql.Semiannual), calendar,
        ql.ModifiedFollowing, ql.ModifiedFollowing,
        ql.DateGeneration.Backward, False
    )

    yield {
        "today": today,
        "calendar": calendar,
        "curve_handle": curve_handle,
        "euribor6m": euribor6m,
        "schedule": schedule,
        "issue_date": issue_date,
        "maturity_date": maturity_date,
    }

    ql.Settings.instance().evaluationDate = original_date


def test_floatingratebond_construction(float_bond_env):
    """Test FloatingRateBond construction."""
    bond = ql.FloatingRateBond(
        2, 100.0, float_bond_env["schedule"],
        float_bond_env["euribor6m"], ql.Actual360()
    )
    assert bond is not None
    assert bond.maturityDate() == float_bond_env["maturity_date"]


def test_floatingratebond_with_spread(float_bond_env):
    """Test FloatingRateBond with spread."""
    bond = ql.FloatingRateBond(
        2, 100.0, float_bond_env["schedule"],
        float_bond_env["euribor6m"], ql.Actual360(),
        spreads=[0.005]
    )
    assert bond is not None


def test_floatingratebond_pricing(float_bond_env):
    """Test FloatingRateBond pricing."""
    bond = ql.FloatingRateBond(
        2, 100.0, float_bond_env["schedule"],
        float_bond_env["euribor6m"], ql.Actual360()
    )
    engine = ql.DiscountingBondEngine(float_bond_env["curve_handle"])
    bond.setPricingEngine(engine)

    # Floating rate bond at flat curve with no spread prices near par
    assert bond.NPV() == pytest.approx(98.04, abs=0.1)
    assert bond.cleanPrice() == pytest.approx(98.06, abs=0.1)


def test_floatingratebond_cashflows(float_bond_env):
    """Test FloatingRateBond has coupons and redemption."""
    bond = ql.FloatingRateBond(
        2, 100.0, float_bond_env["schedule"],
        float_bond_env["euribor6m"], ql.Actual360()
    )
    cashflows = bond.cashflows()
    # 10 semiannual coupons + 1 redemption
    assert len(cashflows) == 11
