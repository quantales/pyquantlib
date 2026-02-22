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


# =============================================================================
# AmortizingFixedRateBond
# =============================================================================


def test_amortizingfixedratebond_construction(bond_env):
    """Test AmortizingFixedRateBond construction."""
    notionals = [100.0, 80.0, 60.0, 40.0, 20.0]
    bond = ql.AmortizingFixedRateBond(
        2, notionals, bond_env["schedule"], [0.05],
        ql.Thirty360(ql.Thirty360.BondBasis),
        issueDate=bond_env["issue_date"],
    )
    assert bond is not None
    assert bond.maturityDate() == bond_env["maturity_date"]
    assert bond.issueDate() == bond_env["issue_date"]


def test_amortizingfixedratebond_frequency(bond_env):
    """Test AmortizingFixedRateBond frequency and day counter."""
    notionals = [100.0, 80.0, 60.0, 40.0, 20.0]
    bond = ql.AmortizingFixedRateBond(
        2, notionals, bond_env["schedule"], [0.05],
        ql.Thirty360(ql.Thirty360.BondBasis),
    )
    assert bond.frequency() == ql.Annual
    assert "30/360" in bond.dayCounter().name()


def test_amortizingfixedratebond_notionals(bond_env):
    """Test AmortizingFixedRateBond has declining notionals."""
    notionals = [100.0, 80.0, 60.0, 40.0, 20.0]
    bond = ql.AmortizingFixedRateBond(
        2, notionals, bond_env["schedule"], [0.05],
        ql.Thirty360(ql.Thirty360.BondBasis),
    )
    # First notional should be 100
    assert bond.notional() == pytest.approx(100.0)


def test_amortizingfixedratebond_cashflows(bond_env):
    """Test AmortizingFixedRateBond cashflows."""
    notionals = [100.0, 80.0, 60.0, 40.0, 20.0]
    bond = ql.AmortizingFixedRateBond(
        2, notionals, bond_env["schedule"], [0.05],
        ql.Thirty360(ql.Thirty360.BondBasis),
    )
    cashflows = bond.cashflows()
    # Should have coupons + redemptions (multiple redemptions for amortizing)
    assert len(cashflows) > 5


def test_amortizingfixedratebond_pricing(bond_env):
    """Test AmortizingFixedRateBond pricing with DiscountingBondEngine."""
    notionals = [100.0, 80.0, 60.0, 40.0, 20.0]
    bond = ql.AmortizingFixedRateBond(
        2, notionals, bond_env["schedule"], [0.05],
        ql.Thirty360(ql.Thirty360.BondBasis),
    )
    engine = ql.DiscountingBondEngine(bond_env["curve_handle"])
    bond.setPricingEngine(engine)
    assert bond.NPV() == pytest.approx(102.5058, abs=0.01)
    assert bond.cleanPrice() == pytest.approx(102.5005, abs=0.01)


# =============================================================================
# sinkingSchedule / sinkingNotionals helpers
# =============================================================================


def test_sinkingschedule(bond_env):
    """Test sinkingSchedule returns a valid Schedule."""
    schedule = ql.sinkingSchedule(
        bond_env["issue_date"],
        ql.Period(5, ql.Years),
        ql.Annual,
        bond_env["calendar"],
    )
    assert isinstance(schedule, ql.Schedule)
    assert len(schedule) > 1


def test_sinkingnotionals():
    """Test sinkingNotionals returns a declining vector."""
    notionals = ql.sinkingNotionals(
        ql.Period(5, ql.Years), ql.Annual, 0.05, 100.0,
    )
    assert len(notionals) > 0
    # Notionals should be declining (French amortization)
    assert notionals[0] == pytest.approx(100.0)
    for i in range(1, len(notionals)):
        assert notionals[i] < notionals[i - 1]


def test_sinkingschedule_with_amortizing_bond(bond_env):
    """Test combining sinkingSchedule/sinkingNotionals with AmortizingFixedRateBond."""
    schedule = ql.sinkingSchedule(
        bond_env["issue_date"],
        ql.Period(5, ql.Years),
        ql.Annual,
        bond_env["calendar"],
    )
    notionals = ql.sinkingNotionals(
        ql.Period(5, ql.Years), ql.Annual, 0.05, 100.0,
    )
    bond = ql.AmortizingFixedRateBond(
        2, notionals, schedule, [0.05],
        ql.Thirty360(ql.Thirty360.BondBasis),
    )
    engine = ql.DiscountingBondEngine(bond_env["curve_handle"])
    bond.setPricingEngine(engine)
    assert bond.NPV() == pytest.approx(102.5834, abs=0.01)


# =============================================================================
# AmortizingFloatingRateBond
# =============================================================================


def test_amortizingfloatingratebond_construction(float_bond_env):
    """Test AmortizingFloatingRateBond construction."""
    notionals = [100.0, 80.0, 60.0, 40.0, 20.0,
                 100.0, 80.0, 60.0, 40.0, 20.0]
    bond = ql.AmortizingFloatingRateBond(
        2, notionals, float_bond_env["schedule"],
        float_bond_env["euribor6m"], ql.Actual360(),
    )
    assert bond is not None
    assert bond.maturityDate() == float_bond_env["maturity_date"]


def test_amortizingfloatingratebond_with_spread(float_bond_env):
    """Test AmortizingFloatingRateBond with spread."""
    notionals = [100.0, 80.0, 60.0, 40.0, 20.0,
                 100.0, 80.0, 60.0, 40.0, 20.0]
    bond = ql.AmortizingFloatingRateBond(
        2, notionals, float_bond_env["schedule"],
        float_bond_env["euribor6m"], ql.Actual360(),
        spreads=[0.005],
    )
    assert bond is not None


def test_amortizingfloatingratebond_cashflows(float_bond_env):
    """Test AmortizingFloatingRateBond cashflows."""
    notionals = [100.0, 80.0, 60.0, 40.0, 20.0,
                 100.0, 80.0, 60.0, 40.0, 20.0]
    bond = ql.AmortizingFloatingRateBond(
        2, notionals, float_bond_env["schedule"],
        float_bond_env["euribor6m"], ql.Actual360(),
    )
    cashflows = bond.cashflows()
    assert len(cashflows) > 5


def test_amortizingfloatingratebond_pricing(float_bond_env):
    """Test AmortizingFloatingRateBond pricing."""
    notionals = [100.0, 80.0, 60.0, 40.0, 20.0,
                 100.0, 80.0, 60.0, 40.0, 20.0]
    bond = ql.AmortizingFloatingRateBond(
        2, notionals, float_bond_env["schedule"],
        float_bond_env["euribor6m"], ql.Actual360(),
    )
    engine = ql.DiscountingBondEngine(float_bond_env["curve_handle"])
    bond.setPricingEngine(engine)
    assert bond.NPV() == pytest.approx(98.04, abs=0.01)


# =============================================================================
# CmsRateBond
# =============================================================================


@pytest.fixture(scope="module")
def cms_bond_env():
    """Environment for CMS rate bond tests."""
    original_date = ql.Settings.instance().evaluationDate
    today = ql.Date(15, ql.January, 2025)
    ql.Settings.instance().evaluationDate = today

    calendar = ql.TARGET()
    day_counter = ql.Actual365Fixed()

    flat_curve = ql.FlatForward(today, 0.04, day_counter)
    curve_handle = ql.YieldTermStructureHandle(flat_curve)

    swap_index = ql.EuriborSwapIsdaFixA(ql.Period(10, ql.Years), curve_handle)

    # Use future dates
    issue_date = calendar.advance(today, ql.Period("6M"))
    maturity_date = calendar.advance(issue_date, ql.Period("5Y"))

    schedule = ql.Schedule(
        issue_date, maturity_date,
        ql.Period(ql.Annual), calendar,
        ql.ModifiedFollowing, ql.ModifiedFollowing,
        ql.DateGeneration.Backward, False,
    )

    yield {
        "today": today,
        "calendar": calendar,
        "curve_handle": curve_handle,
        "swap_index": swap_index,
        "schedule": schedule,
        "issue_date": issue_date,
        "maturity_date": maturity_date,
    }

    ql.Settings.instance().evaluationDate = original_date


def test_cmsratebond_construction(cms_bond_env):
    """Test CmsRateBond construction."""
    bond = ql.CmsRateBond(
        2, 100.0, cms_bond_env["schedule"],
        cms_bond_env["swap_index"], ql.Thirty360(ql.Thirty360.BondBasis),
    )
    assert bond is not None
    assert bond.maturityDate() == cms_bond_env["maturity_date"]


def test_cmsratebond_with_spread(cms_bond_env):
    """Test CmsRateBond with gearings and spreads."""
    bond = ql.CmsRateBond(
        2, 100.0, cms_bond_env["schedule"],
        cms_bond_env["swap_index"], ql.Thirty360(ql.Thirty360.BondBasis),
        gearings=[1.0], spreads=[0.001],
    )
    assert bond is not None


def test_cmsratebond_cashflows(cms_bond_env):
    """Test CmsRateBond has coupons and redemption."""
    bond = ql.CmsRateBond(
        2, 100.0, cms_bond_env["schedule"],
        cms_bond_env["swap_index"], ql.Thirty360(ql.Thirty360.BondBasis),
    )
    cashflows = bond.cashflows()
    # 5 annual CMS coupons + 1 redemption
    assert len(cashflows) == 6


def test_cmsratebond_pricing(cms_bond_env):
    """Test CmsRateBond pricing (requires CMS coupon pricer)."""
    bond = ql.CmsRateBond(
        2, 100.0, cms_bond_env["schedule"],
        cms_bond_env["swap_index"], ql.Thirty360(ql.Thirty360.BondBasis),
    )
    engine = ql.DiscountingBondEngine(cms_bond_env["curve_handle"])
    bond.setPricingEngine(engine)

    # Set CMS coupon pricer on the bond leg
    vol = ql.ConstantSwaptionVolatility(
        0, ql.TARGET(), ql.ModifiedFollowing,
        0.20, ql.Actual365Fixed(),
    )
    vol_handle = ql.SwaptionVolatilityStructureHandle(vol)
    mean_reversion = ql.QuoteHandle(ql.SimpleQuote(0.01))
    pricer = ql.LinearTsrPricer(vol_handle, mean_reversion)
    ql.setCouponPricer(bond.cashflows(), pricer)

    assert bond.NPV() == pytest.approx(98.34, abs=0.01)


# =============================================================================
# CPIBond
# =============================================================================


@pytest.fixture(scope="module")
def cpi_bond_env():
    """Environment for CPI bond tests."""
    original_date = ql.Settings.instance().evaluationDate
    today = ql.Date(15, ql.January, 2025)
    ql.Settings.instance().evaluationDate = today

    calendar = ql.TARGET()
    day_counter = ql.Actual365Fixed()

    flat_curve = ql.FlatForward(today, 0.04, day_counter)
    curve_handle = ql.YieldTermStructureHandle(flat_curve)

    # CPI index with fixings
    cpi = ql.USCPI()
    # Add fixings for the observation lag period
    cpi.addFixing(ql.Date(1, ql.October, 2024), 315.0)
    cpi.addFixing(ql.Date(1, ql.November, 2024), 316.0)
    cpi.addFixing(ql.Date(1, ql.December, 2024), 317.0)

    issue_date = ql.Date(15, ql.January, 2025)
    maturity_date = ql.Date(15, ql.January, 2030)

    schedule = ql.Schedule(
        issue_date, maturity_date,
        ql.Period(ql.Annual), calendar,
        ql.ModifiedFollowing, ql.ModifiedFollowing,
        ql.DateGeneration.Backward, False,
    )

    yield {
        "today": today,
        "calendar": calendar,
        "curve_handle": curve_handle,
        "cpi": cpi,
        "issue_date": issue_date,
        "maturity_date": maturity_date,
        "schedule": schedule,
    }

    cpi.clearFixings()
    ql.Settings.instance().evaluationDate = original_date


def test_cpibond_construction(cpi_bond_env):
    """Test CPIBond construction."""
    bond = ql.CPIBond(
        2, 100.0, 315.0,
        ql.Period(3, ql.Months),
        cpi_bond_env["cpi"],
        ql.CPI.Flat,
        cpi_bond_env["schedule"],
        [0.02],
        ql.Actual365Fixed(),
        issueDate=cpi_bond_env["issue_date"],
    )
    assert bond is not None
    assert bond.maturityDate() == cpi_bond_env["maturity_date"]


def test_cpibond_frequency(cpi_bond_env):
    """Test CPIBond frequency and day counter."""
    bond = ql.CPIBond(
        2, 100.0, 315.0,
        ql.Period(3, ql.Months),
        cpi_bond_env["cpi"],
        ql.CPI.Flat,
        cpi_bond_env["schedule"],
        [0.02],
        ql.Actual365Fixed(),
    )
    assert bond.frequency() == ql.Annual
    assert "Actual/365" in bond.dayCounter().name()


def test_cpibond_inspectors(cpi_bond_env):
    """Test CPIBond inspector methods."""
    bond = ql.CPIBond(
        2, 100.0, 315.0,
        ql.Period(3, ql.Months),
        cpi_bond_env["cpi"],
        ql.CPI.Flat,
        cpi_bond_env["schedule"],
        [0.02],
        ql.Actual365Fixed(),
    )
    assert bond.baseCPI() == pytest.approx(315.0)
    assert bond.observationLag() == ql.Period(3, ql.Months)
    assert bond.cpiIndex() is not None
    assert bond.observationInterpolation() == ql.CPI.Flat
    assert bond.growthOnly() is False


def test_cpibond_cashflows(cpi_bond_env):
    """Test CPIBond cashflows."""
    bond = ql.CPIBond(
        2, 100.0, 315.0,
        ql.Period(3, ql.Months),
        cpi_bond_env["cpi"],
        ql.CPI.Flat,
        cpi_bond_env["schedule"],
        [0.02],
        ql.Actual365Fixed(),
    )
    cashflows = bond.cashflows()
    # 5 CPI coupons + 1 CPI redemption = 6 cashflows
    assert len(cashflows) == 6


def test_cpibond_pricing(cpi_bond_env):
    """Test CPIBond pricing with DiscountingBondEngine."""
    # Build a flat zero inflation curve via bootstrap
    cpi = ql.USCPI()
    cpi.addFixing(ql.Date(1, ql.October, 2024), 315.0)
    cpi.addFixing(ql.Date(1, ql.November, 2024), 316.0)
    cpi.addFixing(ql.Date(1, ql.December, 2024), 317.0)

    helpers = [
        ql.ZeroCouponInflationSwapHelper(
            rate, ql.Period(3, ql.Months),
            cpi_bond_env["today"] + ql.Period(i, ql.Years),
            ql.TARGET(), ql.ModifiedFollowing,
            ql.Actual365Fixed(), cpi, ql.CPI.Flat,
        )
        for i, rate in [(1, 0.025), (3, 0.025), (5, 0.025)]
    ]
    base_date = ql.Date(1, ql.October, 2024)
    inflation_curve = ql.PiecewiseZeroInflationCurve(
        cpi_bond_env["today"], base_date,
        ql.Monthly, ql.Actual365Fixed(), helpers,
    )
    inflation_handle = ql.ZeroInflationTermStructureHandle(inflation_curve)

    cpi_with_curve = ql.USCPI(inflation_handle)
    cpi_with_curve.addFixing(ql.Date(1, ql.October, 2024), 315.0)
    cpi_with_curve.addFixing(ql.Date(1, ql.November, 2024), 316.0)
    cpi_with_curve.addFixing(ql.Date(1, ql.December, 2024), 317.0)

    bond = ql.CPIBond(
        2, 100.0, 315.0,
        ql.Period(3, ql.Months),
        cpi_with_curve,
        ql.CPI.Flat,
        cpi_bond_env["schedule"],
        [0.02],
        ql.Actual365Fixed(),
    )
    engine = ql.DiscountingBondEngine(cpi_bond_env["curve_handle"])
    bond.setPricingEngine(engine)
    assert bond.NPV() == pytest.approx(102.19, abs=0.01)

    cpi.clearFixings()
    cpi_with_curve.clearFixings()


# =============================================================================
# SoftCallability
# =============================================================================


def test_soft_callability_construction():
    """SoftCallability with trigger level."""
    sc = ql.SoftCallability(
        ql.BondPrice(110.0, ql.BondPriceType.Clean),
        ql.Date(15, ql.January, 2028),
        120.0,
    )
    assert sc.trigger() == pytest.approx(120.0)
    assert sc.type() == ql.CallabilityType.Call
    assert sc.date() == ql.Date(15, ql.January, 2028)


# =============================================================================
# Convertible Bonds Fixtures
# =============================================================================


@pytest.fixture
def convertible_env():
    """Environment for convertible bond pricing tests."""
    today = ql.Date(15, ql.January, 2025)
    ql.Settings.evaluationDate = today
    dc = ql.Actual365Fixed()
    calendar = ql.TARGET()

    r_ts = ql.FlatForward(today, 0.04, dc)
    r_handle = ql.YieldTermStructureHandle(r_ts)

    div_ts = ql.FlatForward(today, 0.02, dc)
    div_handle = ql.YieldTermStructureHandle(div_ts)

    vol_ts = ql.BlackConstantVol(today, calendar, 0.30, dc)
    vol_handle = ql.BlackVolTermStructureHandle(vol_ts)

    spot = ql.SimpleQuote(100.0)
    spot_handle = ql.QuoteHandle(spot)

    process = ql.GeneralizedBlackScholesProcess(
        spot_handle, div_handle, r_handle, vol_handle,
    )

    cs = ql.SimpleQuote(0.02)
    exercise = ql.AmericanExercise(today, ql.Date(15, ql.January, 2030))
    engine = ql.BinomialConvertibleEngine(process, "crr", 200, cs)

    schedule = ql.MakeSchedule(
        effectiveDate=ql.Date(15, ql.January, 2025),
        terminationDate=ql.Date(15, ql.January, 2030),
        tenor=ql.Period(1, ql.Years),
        calendar=calendar,
        convention=ql.Unadjusted,
    )

    return {
        "today": today,
        "dc": dc,
        "r_handle": r_handle,
        "process": process,
        "cs": cs,
        "exercise": exercise,
        "engine": engine,
        "schedule": schedule,
    }


# =============================================================================
# ConvertibleZeroCouponBond
# =============================================================================


def test_convertible_zcb_construction(convertible_env):
    """ConvertibleZeroCouponBond can be constructed."""
    env = convertible_env
    zcb = ql.ConvertibleZeroCouponBond(
        env["exercise"], 1.0, [], env["today"], 2,
        env["dc"], env["schedule"], 100.0,
    )
    assert zcb is not None
    assert zcb.conversionRatio() == pytest.approx(1.0)
    assert zcb.isExpired() is False


def test_convertible_zcb_npv(convertible_env):
    """ConvertibleZeroCouponBond priced with BinomialConvertibleEngine."""
    env = convertible_env
    zcb = ql.ConvertibleZeroCouponBond(
        env["exercise"], 1.0, [], env["today"], 2,
        env["dc"], env["schedule"], 100.0,
    )
    zcb.setPricingEngine(env["engine"])
    assert zcb.NPV() == pytest.approx(106.6868, rel=1e-4)


def test_convertible_zcb_callability(convertible_env):
    """ConvertibleZeroCouponBond callability returns the schedule."""
    env = convertible_env
    zcb = ql.ConvertibleZeroCouponBond(
        env["exercise"], 1.0, [], env["today"], 2,
        env["dc"], env["schedule"], 100.0,
    )
    assert len(zcb.callability()) == 0


# =============================================================================
# ConvertibleFixedCouponBond
# =============================================================================


def test_convertible_fixed_coupon_construction(convertible_env):
    """ConvertibleFixedCouponBond can be constructed."""
    env = convertible_env
    fcb = ql.ConvertibleFixedCouponBond(
        env["exercise"], 1.0, [], env["today"], 2,
        [0.05], env["dc"], env["schedule"], 100.0,
    )
    assert fcb is not None
    assert fcb.conversionRatio() == pytest.approx(1.0)


def test_convertible_fixed_coupon_npv(convertible_env):
    """ConvertibleFixedCouponBond priced with BinomialConvertibleEngine."""
    env = convertible_env
    fcb = ql.ConvertibleFixedCouponBond(
        env["exercise"], 1.0, [], env["today"], 2,
        [0.05], env["dc"], env["schedule"], 100.0,
    )
    fcb.setPricingEngine(env["engine"])
    assert fcb.NPV() == pytest.approx(124.3526, rel=1e-4)


def test_convertible_fixed_coupon_with_calls(convertible_env):
    """ConvertibleFixedCouponBond with call schedule."""
    env = convertible_env
    call_schedule = [
        ql.Callability(
            ql.BondPrice(110.0, ql.BondPriceType.Clean),
            ql.CallabilityType.Call,
            ql.Date(15, ql.January, y),
        )
        for y in range(2027, 2030)
    ]
    fcb = ql.ConvertibleFixedCouponBond(
        env["exercise"], 1.0, call_schedule, env["today"], 2,
        [0.05], env["dc"], env["schedule"], 100.0,
    )
    fcb.setPricingEngine(env["engine"])
    assert fcb.NPV() == pytest.approx(119.2989, rel=1e-4)
    assert len(fcb.callability()) == 3


def test_convertible_fixed_coupon_with_soft_call(convertible_env):
    """ConvertibleFixedCouponBond with SoftCallability."""
    env = convertible_env
    soft_calls = [
        ql.SoftCallability(
            ql.BondPrice(110.0, ql.BondPriceType.Clean),
            ql.Date(15, ql.January, 2028),
            130.0,
        )
    ]
    fcb = ql.ConvertibleFixedCouponBond(
        env["exercise"], 1.0, soft_calls, env["today"], 2,
        [0.05], env["dc"], env["schedule"], 100.0,
    )
    fcb.setPricingEngine(env["engine"])
    assert fcb.NPV() == pytest.approx(124.3526, rel=1e-4)
    assert len(fcb.callability()) == 1


# =============================================================================
# ConvertibleFloatingRateBond
# =============================================================================


def test_convertible_floating_rate_construction(convertible_env):
    """ConvertibleFloatingRateBond can be constructed."""
    env = convertible_env
    euribor = ql.Euribor(ql.Period(6, ql.Months), env["r_handle"])
    euribor.addFixing(ql.Date(13, ql.January, 2025), 0.04)
    frb = ql.ConvertibleFloatingRateBond(
        env["exercise"], 1.0, [], env["today"], 2,
        euribor, 2, [0.005], env["dc"], env["schedule"], 100.0,
    )
    assert frb is not None
    assert frb.conversionRatio() == pytest.approx(1.0)


def test_convertible_floating_rate_npv(convertible_env):
    """ConvertibleFloatingRateBond priced with BinomialConvertibleEngine."""
    env = convertible_env
    euribor = ql.Euribor(ql.Period(6, ql.Months), env["r_handle"])
    euribor.addFixing(ql.Date(13, ql.January, 2025), 0.04)
    frb = ql.ConvertibleFloatingRateBond(
        env["exercise"], 1.0, [], env["today"], 2,
        euribor, 2, [0.005], env["dc"], env["schedule"], 100.0,
    )
    frb.setPricingEngine(env["engine"])
    assert frb.NPV() == pytest.approx(122.4706, rel=1e-4)
