"""
Tests for experimental callable bonds module.

Corresponds to src/experimental/callablebonds/*.cpp bindings.
"""

import pytest

import pyquantlib as ql


# =============================================================================
# Fixtures
# =============================================================================


@pytest.fixture
def callable_bond_env():
    """Common environment for callable bond tests (multi-call, tree engine)."""
    today = ql.Date(15, ql.January, 2025)
    ql.Settings.evaluationDate = today
    calendar = ql.TARGET()
    dc = ql.Actual365Fixed()

    # Flat yield curve at 4%
    r_ts = ql.FlatForward(today, 0.04, dc)
    r_handle = ql.YieldTermStructureHandle(r_ts)

    # Call schedule: callable annually from year 3 to year 9
    call_schedule = []
    for y in range(2028, 2035):
        call_date = ql.Date(15, ql.January, y)
        call_price = ql.BondPrice(100.0, ql.BondPriceType.Clean)
        call_schedule.append(
            ql.Callability(call_price, ql.CallabilityType.Call, call_date)
        )

    # Callable fixed rate bond: 5% coupon, 10yr
    bond_schedule = ql.MakeSchedule(
        effectiveDate=ql.Date(15, ql.January, 2025),
        terminationDate=ql.Date(15, ql.January, 2035),
        tenor=ql.Period(1, ql.Years),
        calendar=calendar,
        convention=ql.Unadjusted,
    )
    bond = ql.CallableFixedRateBond(
        2, 100.0, bond_schedule, [0.05], dc,
        ql.Following, 100.0, ql.Date(), call_schedule,
    )

    # Hull-White model
    hw_model = ql.HullWhite(r_handle, 0.03, 0.01)

    return {
        "today": today,
        "calendar": calendar,
        "dc": dc,
        "r_ts": r_ts,
        "r_handle": r_handle,
        "call_schedule": call_schedule,
        "bond_schedule": bond_schedule,
        "bond": bond,
        "hw_model": hw_model,
    }


@pytest.fixture
def single_call_bond_env():
    """Environment for Black engine tests (requires exactly one call date)."""
    today = ql.Date(15, ql.January, 2025)
    ql.Settings.evaluationDate = today
    calendar = ql.TARGET()
    dc = ql.Actual365Fixed()

    r_ts = ql.FlatForward(today, 0.04, dc)
    r_handle = ql.YieldTermStructureHandle(r_ts)

    # Single call date for Black engine
    single_call = [
        ql.Callability(
            ql.BondPrice(100.0, ql.BondPriceType.Clean),
            ql.CallabilityType.Call,
            ql.Date(15, ql.January, 2030),
        )
    ]

    bond_schedule = ql.MakeSchedule(
        effectiveDate=ql.Date(15, ql.January, 2025),
        terminationDate=ql.Date(15, ql.January, 2035),
        tenor=ql.Period(1, ql.Years),
        calendar=calendar,
        convention=ql.Unadjusted,
    )
    bond = ql.CallableFixedRateBond(
        2, 100.0, bond_schedule, [0.05], dc,
        ql.Following, 100.0, ql.Date(), single_call,
    )

    return {
        "today": today,
        "dc": dc,
        "r_ts": r_ts,
        "r_handle": r_handle,
        "bond": bond,
    }


# =============================================================================
# CallableFixedRateBond
# =============================================================================


def test_callable_fixed_rate_bond_construction(callable_bond_env):
    """CallableFixedRateBond can be constructed."""
    bond = callable_bond_env["bond"]
    assert bond is not None
    assert bond.isExpired() is False


def test_callable_fixed_rate_bond_callability(callable_bond_env):
    """CallableFixedRateBond callability returns the put/call schedule."""
    bond = callable_bond_env["bond"]
    schedule = bond.callability()
    assert len(schedule) == 7
    assert schedule[0].type() == ql.CallabilityType.Call
    assert schedule[0].date() == ql.Date(15, ql.January, 2028)


def test_callable_fixed_rate_bond_tree_engine_npv(callable_bond_env):
    """CallableFixedRateBond priced with TreeCallableFixedRateBondEngine."""
    env = callable_bond_env
    engine = ql.TreeCallableFixedRateBondEngine(env["hw_model"], 100)
    env["bond"].setPricingEngine(engine)

    assert env["bond"].NPV() == pytest.approx(100.4673, rel=1e-4)
    assert env["bond"].cleanPrice() == pytest.approx(100.4620, rel=1e-4)


def test_callable_fixed_rate_bond_oas(callable_bond_env):
    """CallableFixedRateBond OAS calculation."""
    env = callable_bond_env
    engine = ql.TreeCallableFixedRateBondEngine(env["hw_model"], 100)
    env["bond"].setPricingEngine(engine)

    clean = env["bond"].cleanPrice()
    oas = env["bond"].OAS(clean, env["r_handle"], env["dc"],
                          ql.Continuous, ql.Annual)
    assert oas == pytest.approx(-4.641e-5, abs=1e-4)


def test_callable_fixed_rate_bond_effective_duration(callable_bond_env):
    """CallableFixedRateBond effective duration."""
    env = callable_bond_env
    engine = ql.TreeCallableFixedRateBondEngine(env["hw_model"], 100)
    env["bond"].setPricingEngine(engine)

    clean = env["bond"].cleanPrice()
    oas = env["bond"].OAS(clean, env["r_handle"], env["dc"],
                          ql.Continuous, ql.Annual)
    eff_dur = env["bond"].effectiveDuration(
        oas, env["r_handle"], env["dc"], ql.Continuous, ql.Annual,
    )
    assert eff_dur == pytest.approx(4.7054, rel=1e-3)


def test_callable_fixed_rate_bond_effective_convexity(callable_bond_env):
    """CallableFixedRateBond effective convexity."""
    env = callable_bond_env
    engine = ql.TreeCallableFixedRateBondEngine(env["hw_model"], 100)
    env["bond"].setPricingEngine(engine)

    clean = env["bond"].cleanPrice()
    oas = env["bond"].OAS(clean, env["r_handle"], env["dc"],
                          ql.Continuous, ql.Annual)
    eff_conv = env["bond"].effectiveConvexity(
        oas, env["r_handle"], env["dc"], ql.Continuous, ql.Annual,
    )
    assert eff_conv == pytest.approx(-369.5886, rel=1e-3)


def test_callable_fixed_rate_bond_clean_price_oas(callable_bond_env):
    """CallableFixedRateBond cleanPriceOAS roundtrips with OAS."""
    env = callable_bond_env
    engine = ql.TreeCallableFixedRateBondEngine(env["hw_model"], 100)
    env["bond"].setPricingEngine(engine)

    clean = env["bond"].cleanPrice()
    oas = env["bond"].OAS(clean, env["r_handle"], env["dc"],
                          ql.Continuous, ql.Annual)
    recovered = env["bond"].cleanPriceOAS(
        oas, env["r_handle"], env["dc"], ql.Continuous, ql.Annual,
    )
    assert recovered == pytest.approx(clean, rel=1e-6)


# =============================================================================
# BlackCallableFixedRateBondEngine (requires single call date)
# =============================================================================


def test_callable_fixed_rate_bond_black_engine_npv(single_call_bond_env):
    """CallableFixedRateBond priced with BlackCallableFixedRateBondEngine."""
    env = single_call_bond_env
    vol = ql.CallableBondConstantVolatility(env["today"], 0.10, env["dc"])
    engine = ql.BlackCallableFixedRateBondEngine(vol, env["r_ts"])
    env["bond"].setPricingEngine(engine)

    assert env["bond"].NPV() == pytest.approx(103.7888, rel=1e-4)
    assert env["bond"].cleanPrice() == pytest.approx(103.7841, rel=1e-4)


def test_callable_fixed_rate_bond_implied_vol(single_call_bond_env):
    """CallableFixedRateBond impliedVolatility roundtrips."""
    env = single_call_bond_env
    vol = ql.CallableBondConstantVolatility(env["today"], 0.10, env["dc"])
    engine = ql.BlackCallableFixedRateBondEngine(vol, env["r_ts"])
    env["bond"].setPricingEngine(engine)

    target_price = ql.BondPrice(env["bond"].cleanPrice(), ql.BondPriceType.Clean)
    implied = env["bond"].impliedVolatility(
        target_price, env["r_handle"], 1e-8, 200, 0.001, 0.50,
    )
    assert implied == pytest.approx(0.10, rel=1e-3)


# =============================================================================
# CallableZeroCouponBond
# =============================================================================


def test_callable_zero_coupon_bond_construction():
    """CallableZeroCouponBond can be constructed."""
    today = ql.Date(15, ql.January, 2025)
    ql.Settings.evaluationDate = today
    dc = ql.Actual365Fixed()

    call_schedule = [
        ql.Callability(
            ql.BondPrice(60.0, ql.BondPriceType.Clean),
            ql.CallabilityType.Call,
            ql.Date(15, ql.January, y),
        )
        for y in range(2028, 2035)
    ]

    bond = ql.CallableZeroCouponBond(
        2, 100.0, ql.TARGET(), ql.Date(15, ql.January, 2035),
        dc, ql.Following, 100.0, ql.Date(), call_schedule,
    )
    assert bond is not None
    assert bond.isExpired() is False


def test_callable_zero_coupon_bond_tree_engine():
    """CallableZeroCouponBond priced with TreeCallableZeroCouponBondEngine."""
    today = ql.Date(15, ql.January, 2025)
    ql.Settings.evaluationDate = today
    dc = ql.Actual365Fixed()

    r_ts = ql.FlatForward(today, 0.04, dc)
    r_handle = ql.YieldTermStructureHandle(r_ts)

    call_schedule = [
        ql.Callability(
            ql.BondPrice(60.0, ql.BondPriceType.Clean),
            ql.CallabilityType.Call,
            ql.Date(15, ql.January, y),
        )
        for y in range(2028, 2035)
    ]

    bond = ql.CallableZeroCouponBond(
        2, 100.0, ql.TARGET(), ql.Date(15, ql.January, 2035),
        dc, ql.Following, 100.0, ql.Date(), call_schedule,
    )

    hw_model = ql.HullWhite(r_handle, 0.03, 0.01)
    engine = ql.TreeCallableZeroCouponBondEngine(hw_model, 100)
    bond.setPricingEngine(engine)

    assert bond.NPV() == pytest.approx(41.7928, rel=1e-4)
    assert bond.cleanPrice() == pytest.approx(41.8019, rel=1e-4)


def test_callable_zero_coupon_bond_black_engine():
    """CallableZeroCouponBond priced with BlackCallableZeroCouponBondEngine."""
    today = ql.Date(15, ql.January, 2025)
    ql.Settings.evaluationDate = today
    dc = ql.Actual365Fixed()

    r_ts = ql.FlatForward(today, 0.04, dc)

    # Black engine: single call date
    single_call = [
        ql.Callability(
            ql.BondPrice(60.0, ql.BondPriceType.Clean),
            ql.CallabilityType.Call,
            ql.Date(15, ql.January, 2030),
        )
    ]

    bond = ql.CallableZeroCouponBond(
        2, 100.0, ql.TARGET(), ql.Date(15, ql.January, 2035),
        dc, ql.Following, 100.0, ql.Date(), single_call,
    )

    vol_quote = ql.SimpleQuote(0.10)
    engine = ql.BlackCallableZeroCouponBondEngine(vol_quote, r_ts)
    bond.setPricingEngine(engine)

    assert bond.NPV() == pytest.approx(49.1038, rel=1e-4)


# =============================================================================
# CallableBondConstantVolatility
# =============================================================================


def test_callable_bond_constant_vol_date_scalar():
    """CallableBondConstantVolatility from reference date and scalar vol."""
    today = ql.Date(15, ql.January, 2025)
    dc = ql.Actual365Fixed()
    vol = ql.CallableBondConstantVolatility(today, 0.20, dc)
    assert vol is not None
    assert vol.referenceDate() == today


def test_callable_bond_constant_vol_settlement_scalar():
    """CallableBondConstantVolatility from settlement days and scalar vol."""
    today = ql.Date(15, ql.January, 2025)
    ql.Settings.evaluationDate = today
    dc = ql.Actual365Fixed()
    vol = ql.CallableBondConstantVolatility(0, ql.TARGET(), 0.15, dc)
    assert vol is not None


def test_callable_bond_constant_vol_date_quote():
    """CallableBondConstantVolatility from reference date and Quote."""
    today = ql.Date(15, ql.January, 2025)
    dc = ql.Actual365Fixed()
    quote = ql.SimpleQuote(0.25)
    vol = ql.CallableBondConstantVolatility(today, quote, dc)
    assert vol is not None


def test_callable_bond_constant_vol_settlement_quote():
    """CallableBondConstantVolatility from settlement days and Quote."""
    today = ql.Date(15, ql.January, 2025)
    ql.Settings.evaluationDate = today
    dc = ql.Actual365Fixed()
    quote = ql.SimpleQuote(0.18)
    vol = ql.CallableBondConstantVolatility(0, ql.TARGET(), quote, dc)
    assert vol is not None


# =============================================================================
# CallableBondVolatilityStructure (ABC)
# =============================================================================


def test_callable_bond_vol_structure_abc_exists():
    """CallableBondVolatilityStructure ABC is accessible on base."""
    assert hasattr(ql.base, "CallableBondVolatilityStructure")


def test_callable_bond_vol_structure_methods():
    """CallableBondVolatilityStructure methods accessible through concrete subclass."""
    today = ql.Date(15, ql.January, 2025)
    ql.Settings.evaluationDate = today
    dc = ql.Actual365Fixed()
    vol = ql.CallableBondConstantVolatility(today, 0.20, dc)

    assert vol.maxBondLength() == pytest.approx(1.7976931348623157e+308)


# =============================================================================
# TreeCallableFixedRateBondEngine constructors
# =============================================================================


def test_tree_callable_engine_with_term_structure(callable_bond_env):
    """TreeCallableFixedRateBondEngine with explicit term structure."""
    env = callable_bond_env
    engine = ql.TreeCallableFixedRateBondEngine(
        env["hw_model"], 100, env["r_handle"],
    )
    env["bond"].setPricingEngine(engine)
    assert env["bond"].NPV() == pytest.approx(100.4673, rel=1e-4)


# =============================================================================
# BlackCallableFixedRateBondEngine hidden handle
# =============================================================================


def test_black_callable_engine_hidden_handle(single_call_bond_env):
    """BlackCallableFixedRateBondEngine with raw objects (hidden handles)."""
    env = single_call_bond_env
    vol = ql.CallableBondConstantVolatility(env["today"], 0.10, env["dc"])
    engine = ql.BlackCallableFixedRateBondEngine(vol, env["r_ts"])
    env["bond"].setPricingEngine(engine)

    assert env["bond"].NPV() == pytest.approx(103.7888, rel=1e-4)
