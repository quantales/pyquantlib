"""
Tests for credit pricing engine bindings.

Corresponds to src/pricingengines/credit/*.cpp bindings.
"""

import pytest

import pyquantlib as ql


# =============================================================================
# Fixtures
# =============================================================================


@pytest.fixture(scope="module")
def cds_pricing_env():
    """Common environment for CDS engine tests."""
    original_date = ql.Settings.instance().evaluationDate
    today = ql.Date(15, ql.January, 2025)
    ql.Settings.instance().evaluationDate = today

    dc = ql.Actual365Fixed()
    calendar = ql.TARGET()

    # Discount curve
    discount_curve = ql.FlatForward(today, 0.02, dc)

    # Default probability curve (1% flat hazard rate)
    default_curve = ql.FlatHazardRate(today, 0.01, dc)

    # CDS schedule
    start = calendar.advance(today, ql.Period(1, ql.Days))
    maturity = calendar.advance(start, ql.Period(5, ql.Years))
    schedule = ql.Schedule(
        start, maturity,
        ql.Period(ql.Quarterly), calendar,
        ql.Following, ql.Unadjusted,
        ql.DateGeneration.TwentiethIMM, False,
    )

    # CDS instrument
    cds = ql.CreditDefaultSwap(
        ql.ProtectionSide.Buyer,
        10_000_000.0,
        0.01,
        schedule,
        ql.Following,
        ql.Actual360(),
    )

    yield {
        "today": today,
        "dc": dc,
        "discount_curve": discount_curve,
        "default_curve": default_curve,
        "schedule": schedule,
        "cds": cds,
    }

    ql.Settings.instance().evaluationDate = original_date


# =============================================================================
# MidPointCdsEngine
# =============================================================================


def test_midpointcdsengine_construction_handle(cds_pricing_env):
    """Test MidPointCdsEngine construction with handles."""
    env = cds_pricing_env
    engine = ql.MidPointCdsEngine(
        ql.DefaultProbabilityTermStructureHandle(env["default_curve"]),
        0.4,
        ql.YieldTermStructureHandle(env["discount_curve"]),
    )
    assert engine is not None


def test_midpointcdsengine_hidden_handle(cds_pricing_env):
    """Test MidPointCdsEngine with hidden handles."""
    env = cds_pricing_env
    engine = ql.MidPointCdsEngine(
        env["default_curve"],
        0.4,
        env["discount_curve"],
    )
    assert engine is not None


def test_midpointcdsengine_pricing(cds_pricing_env):
    """Test MidPointCdsEngine pricing."""
    env = cds_pricing_env
    engine = ql.MidPointCdsEngine(
        env["default_curve"], 0.4, env["discount_curve"],
    )
    env["cds"].setPricingEngine(engine)

    npv = env["cds"].NPV()
    assert isinstance(npv, float)

    fair_spread = env["cds"].fairSpread()
    assert fair_spread > 0

    coupon_npv = env["cds"].couponLegNPV()
    default_npv = env["cds"].defaultLegNPV()
    assert coupon_npv != 0
    assert default_npv != 0


def test_midpointcdsengine_recovery_rate_effect(cds_pricing_env):
    """Test that recovery rate affects NPV."""
    env = cds_pricing_env
    cds = ql.CreditDefaultSwap(
        ql.ProtectionSide.Buyer,
        10_000_000.0,
        0.01,
        env["schedule"],
        ql.Following,
        ql.Actual360(),
    )

    engine_low = ql.MidPointCdsEngine(
        env["default_curve"], 0.2, env["discount_curve"],
    )
    cds.setPricingEngine(engine_low)
    npv_low_recovery = cds.NPV()

    engine_high = ql.MidPointCdsEngine(
        env["default_curve"], 0.6, env["discount_curve"],
    )
    cds.setPricingEngine(engine_high)
    npv_high_recovery = cds.NPV()

    # Higher recovery -> lower default leg -> lower NPV for buyer
    assert npv_low_recovery > npv_high_recovery


# =============================================================================
# IsdaCdsEngine
# =============================================================================


def test_isdacdsengine_enums():
    """Test IsdaCdsEngine enum values."""
    assert ql.IsdaNumericalFix.IsdaNone is not None
    assert ql.IsdaNumericalFix.Taylor is not None
    assert ql.IsdaAccrualBias.HalfDayBias is not None
    assert ql.IsdaAccrualBias.NoBias is not None
    assert ql.IsdaForwardsInCouponPeriod.Flat is not None
    assert ql.IsdaForwardsInCouponPeriod.Piecewise is not None


def test_isdacdsengine_construction_handle(cds_pricing_env):
    """Test IsdaCdsEngine construction with handles."""
    env = cds_pricing_env
    engine = ql.IsdaCdsEngine(
        ql.DefaultProbabilityTermStructureHandle(env["default_curve"]),
        0.4,
        ql.YieldTermStructureHandle(env["discount_curve"]),
    )
    assert engine is not None


def test_isdacdsengine_hidden_handle(cds_pricing_env):
    """Test IsdaCdsEngine with hidden handles."""
    env = cds_pricing_env
    engine = ql.IsdaCdsEngine(
        env["default_curve"], 0.4, env["discount_curve"],
    )
    assert engine is not None


def test_isdacdsengine_pricing(cds_pricing_env):
    """Test IsdaCdsEngine pricing."""
    env = cds_pricing_env
    engine = ql.IsdaCdsEngine(
        env["default_curve"], 0.4, env["discount_curve"],
    )
    env["cds"].setPricingEngine(engine)

    npv = env["cds"].NPV()
    assert isinstance(npv, float)

    fair_spread = env["cds"].fairSpread()
    assert fair_spread > 0


def test_isdacdsengine_vs_midpoint(cds_pricing_env):
    """Test IsdaCdsEngine and MidPointCdsEngine give similar results."""
    env = cds_pricing_env
    cds = ql.CreditDefaultSwap(
        ql.ProtectionSide.Buyer,
        10_000_000.0,
        0.01,
        env["schedule"],
        ql.Following,
        ql.Actual360(),
    )

    mid_engine = ql.MidPointCdsEngine(
        env["default_curve"], 0.4, env["discount_curve"],
    )
    cds.setPricingEngine(mid_engine)
    npv_mid = cds.NPV()

    isda_engine = ql.IsdaCdsEngine(
        env["default_curve"], 0.4, env["discount_curve"],
    )
    cds.setPricingEngine(isda_engine)
    npv_isda = cds.NPV()

    # Both should agree within reasonable tolerance
    assert npv_mid == pytest.approx(npv_isda, rel=0.05)


def test_isdacdsengine_with_custom_params(cds_pricing_env):
    """Test IsdaCdsEngine with custom parameters."""
    env = cds_pricing_env
    engine = ql.IsdaCdsEngine(
        env["default_curve"],
        0.4,
        env["discount_curve"],
        numericalFix=ql.IsdaNumericalFix.IsdaNone,
        accrualBias=ql.IsdaAccrualBias.NoBias,
        forwardsInCouponPeriod=ql.IsdaForwardsInCouponPeriod.Flat,
    )
    env["cds"].setPricingEngine(engine)
    npv = env["cds"].NPV()
    assert isinstance(npv, float)


def test_isdacdsengine_curves(cds_pricing_env):
    """Test IsdaCdsEngine curve accessors."""
    env = cds_pricing_env
    engine = ql.IsdaCdsEngine(
        env["default_curve"], 0.4, env["discount_curve"],
    )
    assert engine.isdaRateCurve() is not None
    assert engine.isdaCreditCurve() is not None
