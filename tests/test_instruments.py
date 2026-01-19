"""Tests for ql/instruments/*.hpp bindings."""

import pytest

import pyquantlib as ql


# --- Swap ---


def test_swap_type_enum():
    """Test SwapType enum values."""
    assert ql.SwapType.Payer is not None
    assert ql.SwapType.Receiver is not None
    assert int(ql.SwapType.Payer) == 1
    assert int(ql.SwapType.Receiver) == -1


def test_swap_arguments():
    """Test SwapArguments class."""
    args = ql.SwapArguments()
    assert args is not None
    assert args.legs == []
    assert args.payer == []


def test_swap_results():
    """Test SwapResults class."""
    results = ql.SwapResults()
    assert results is not None
    results.reset()


def test_swap_engine_class():
    """Test Swap.engine base class exists."""
    assert hasattr(ql.Swap, "engine")


def test_swap_generic_engine_class():
    """Test SwapGenericEngine exists in base module."""
    assert hasattr(ql.base, "SwapGenericEngine")


def test_fixedvsfloatingswap_arguments():
    """Test FixedVsFloatingSwapArguments class."""
    args = ql.FixedVsFloatingSwapArguments()
    assert args is not None


def test_fixedvsfloatingswap_results():
    """Test FixedVsFloatingSwapResults class."""
    results = ql.FixedVsFloatingSwapResults()
    assert results is not None


def test_swap_construction_two_legs():
    """Test Swap construction from two legs."""
    # Create simple fixed cash flows as legs
    today = ql.Date(15, ql.June, 2025)
    ql.Settings.instance().evaluationDate = today

    # Simple legs with fixed cash flows
    leg1 = [ql.SimpleCashFlow(100.0, today + ql.Period(1, ql.Years))]
    leg2 = [ql.SimpleCashFlow(105.0, today + ql.Period(1, ql.Years))]

    swap = ql.Swap(leg1, leg2)

    assert swap is not None
    assert swap.numberOfLegs() == 2
    assert not swap.isExpired()


def test_swap_construction_multi_leg():
    """Test Swap multi-leg construction."""
    today = ql.Date(15, ql.June, 2025)
    ql.Settings.instance().evaluationDate = today

    leg1 = [ql.SimpleCashFlow(100.0, today + ql.Period(1, ql.Years))]
    leg2 = [ql.SimpleCashFlow(50.0, today + ql.Period(1, ql.Years))]
    leg3 = [ql.SimpleCashFlow(50.0, today + ql.Period(1, ql.Years))]

    # payer[i] = True means leg i is paid
    swap = ql.Swap([leg1, leg2, leg3], [True, False, False])

    assert swap.numberOfLegs() == 3
    assert swap.payer(0) is True
    assert swap.payer(1) is False
    assert swap.payer(2) is False


def test_swap_dates():
    """Test Swap date inspectors."""
    today = ql.Date(15, ql.June, 2025)
    ql.Settings.instance().evaluationDate = today

    date1 = today + ql.Period(6, ql.Months)
    date2 = today + ql.Period(1, ql.Years)

    leg1 = [
        ql.SimpleCashFlow(50.0, date1),
        ql.SimpleCashFlow(50.0, date2),
    ]
    leg2 = [
        ql.SimpleCashFlow(52.5, date1),
        ql.SimpleCashFlow(52.5, date2),
    ]

    swap = ql.Swap(leg1, leg2)

    assert swap.startDate() == date1
    assert swap.maturityDate() == date2


def test_swap_legs_accessor():
    """Test Swap legs accessor."""
    today = ql.Date(15, ql.June, 2025)
    ql.Settings.instance().evaluationDate = today

    leg1 = [ql.SimpleCashFlow(100.0, today + ql.Period(1, ql.Years))]
    leg2 = [ql.SimpleCashFlow(105.0, today + ql.Period(1, ql.Years))]

    swap = ql.Swap(leg1, leg2)

    legs = swap.legs()
    assert len(legs) == 2

    leg0 = swap.leg(0)
    assert len(leg0) == 1

    leg1_retrieved = swap.leg(1)
    assert len(leg1_retrieved) == 1


# --- VanillaSwap ---


@pytest.fixture
def swap_env():
    """Market environment for VanillaSwap tests."""
    today = ql.Date(15, ql.February, 2025)
    ql.Settings.instance().evaluationDate = today

    calendar = ql.TARGET()
    settlement = calendar.advance(today, ql.Period(2, ql.Days))

    # Yield curve
    dc = ql.Actual365Fixed()
    rate = 0.05
    flat_curve = ql.FlatForward(settlement, rate, dc)

    # Index
    euribor = ql.Euribor6M(flat_curve)

    # Schedules
    start = calendar.advance(settlement, ql.Period(1, ql.Years))
    maturity = calendar.advance(start, ql.Period(5, ql.Years))

    fixed_schedule = ql.Schedule(
        start, maturity,
        ql.Period(ql.Annual),
        calendar,
        ql.Unadjusted, ql.Unadjusted,
        ql.DateGeneration.Forward, False,
    )

    float_schedule = ql.Schedule(
        start, maturity,
        ql.Period(ql.Semiannual),
        calendar,
        ql.ModifiedFollowing, ql.ModifiedFollowing,
        ql.DateGeneration.Forward, False,
    )

    return {
        "calendar": calendar,
        "settlement": settlement,
        "flat_curve": flat_curve,
        "euribor": euribor,
        "fixed_schedule": fixed_schedule,
        "float_schedule": float_schedule,
        "fixed_dc": ql.Thirty360(ql.Thirty360.European),
        "float_dc": euribor.dayCounter(),
    }


def test_vanillaswap_construction(swap_env):
    """Test VanillaSwap construction."""
    swap = ql.VanillaSwap(
        ql.SwapType.Payer,
        1000000.0,
        swap_env["fixed_schedule"],
        0.05,
        swap_env["fixed_dc"],
        swap_env["float_schedule"],
        swap_env["euribor"],
        0.0,
        swap_env["float_dc"],
    )

    assert swap is not None
    assert swap.type() == ql.SwapType.Payer
    assert swap.nominal() == 1000000.0
    assert swap.fixedRate() == 0.05
    assert swap.spread() == 0.0


def test_vanillaswap_inspectors(swap_env):
    """Test VanillaSwap inspectors."""
    swap = ql.VanillaSwap(
        ql.SwapType.Receiver,
        1000000.0,
        swap_env["fixed_schedule"],
        0.04,
        swap_env["fixed_dc"],
        swap_env["float_schedule"],
        swap_env["euribor"],
        0.001,
        swap_env["float_dc"],
    )

    assert swap.type() == ql.SwapType.Receiver
    assert swap.fixedRate() == 0.04
    assert swap.spread() == 0.001
    assert len(swap.fixedLeg()) > 0
    assert len(swap.floatingLeg()) > 0


def test_vanillaswap_legs(swap_env):
    """Test VanillaSwap leg accessors."""
    swap = ql.VanillaSwap(
        ql.SwapType.Payer,
        1000000.0,
        swap_env["fixed_schedule"],
        0.05,
        swap_env["fixed_dc"],
        swap_env["float_schedule"],
        swap_env["euribor"],
        0.0,
        swap_env["float_dc"],
    )

    fixed_leg = swap.fixedLeg()
    floating_leg = swap.floatingLeg()

    # 5-year swap with annual fixed payments = 5 coupons
    assert len(fixed_leg) == 5
    # 5-year swap with semiannual float payments = 10 coupons
    assert len(floating_leg) == 10


def test_vanillaswap_pricing(swap_env):
    """Test VanillaSwap pricing with DiscountingSwapEngine."""
    swap = ql.VanillaSwap(
        ql.SwapType.Payer,
        1000000.0,
        swap_env["fixed_schedule"],
        0.05,
        swap_env["fixed_dc"],
        swap_env["float_schedule"],
        swap_env["euribor"],
        0.0,
        swap_env["float_dc"],
    )

    engine = ql.DiscountingSwapEngine(swap_env["flat_curve"])
    swap.setPricingEngine(engine)

    npv = swap.NPV()
    fair_rate = swap.fairRate()

    assert npv == pytest.approx(5339.542841940245, abs=1e-6)
    assert fair_rate == pytest.approx(0.051301228549385104, rel=1e-5)


def test_vanillaswap_fair_rate(swap_env):
    """Test that swap at fair rate has zero NPV."""
    # First get fair rate
    swap = ql.VanillaSwap(
        ql.SwapType.Payer,
        1000000.0,
        swap_env["fixed_schedule"],
        0.05,  # dummy rate
        swap_env["fixed_dc"],
        swap_env["float_schedule"],
        swap_env["euribor"],
        0.0,
        swap_env["float_dc"],
    )

    engine = ql.DiscountingSwapEngine(swap_env["flat_curve"])
    swap.setPricingEngine(engine)

    fair_rate = swap.fairRate()

    # Create swap at fair rate
    fair_swap = ql.VanillaSwap(
        ql.SwapType.Payer,
        1000000.0,
        swap_env["fixed_schedule"],
        fair_rate,
        swap_env["fixed_dc"],
        swap_env["float_schedule"],
        swap_env["euribor"],
        0.0,
        swap_env["float_dc"],
    )
    fair_swap.setPricingEngine(engine)

    # NPV should be approximately zero
    assert abs(fair_swap.NPV()) < 1e-6