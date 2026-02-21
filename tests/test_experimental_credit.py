"""
Tests for experimental credit module.

Corresponds to src/experimental/credit/*.cpp bindings.
"""

import pytest

import pyquantlib as ql


# =============================================================================
# Fixtures
# =============================================================================


@pytest.fixture
def cds_option_env():
    """Common environment for CdsOption and BlackCdsOptionEngine tests."""
    today = ql.Date(15, ql.January, 2025)
    ql.Settings.evaluationDate = today
    calendar = ql.TARGET()
    dc = ql.Actual365Fixed()

    r_ts = ql.FlatForward(today, 0.03, dc)
    r_handle = ql.YieldTermStructureHandle(r_ts)

    dp_ts = ql.FlatHazardRate(today, 0.01, dc)
    dp_handle = ql.DefaultProbabilityTermStructureHandle(dp_ts)

    recovery = 0.4

    exercise_date = calendar.advance(today, ql.Period("6M"))
    exercise = ql.EuropeanExercise(exercise_date)

    cds_maturity = calendar.advance(exercise_date, ql.Period("5Y"))
    cds_schedule = ql.Schedule(
        exercise_date, cds_maturity,
        ql.Period(ql.Quarterly), calendar,
        ql.Following, ql.Unadjusted,
        ql.DateGeneration.TwentiethIMM, False,
    )

    cds = ql.CreditDefaultSwap(
        ql.ProtectionSide.Buyer,
        1000000.0,
        0.01,
        cds_schedule,
        ql.ModifiedFollowing,
        dc,
    )
    cds_engine = ql.MidPointCdsEngine(dp_handle, recovery, r_handle)
    cds.setPricingEngine(cds_engine)

    vol_quote = ql.SimpleQuote(0.40)

    return {
        "today": today,
        "r_ts": r_ts,
        "r_handle": r_handle,
        "dp_ts": dp_ts,
        "dp_handle": dp_handle,
        "recovery": recovery,
        "exercise": exercise,
        "cds": cds,
        "vol_quote": vol_quote,
    }


# =============================================================================
# CdsOption
# =============================================================================


def test_cdsoption_construction(cds_option_env):
    """CdsOption constructs and returns correct underlying swap."""
    env = cds_option_env
    option = ql.CdsOption(env["cds"], env["exercise"])
    assert isinstance(option, ql.base.Option)
    assert isinstance(option.underlyingSwap(), ql.CreditDefaultSwap)


def test_cdsoption_pricing(cds_option_env):
    """CdsOption prices correctly with BlackCdsOptionEngine."""
    env = cds_option_env
    option = ql.CdsOption(env["cds"], env["exercise"])
    engine = ql.BlackCdsOptionEngine(
        env["dp_handle"], env["recovery"], env["r_handle"],
        ql.QuoteHandle(env["vol_quote"]),
    )
    option.setPricingEngine(engine)
    assert option.NPV() == pytest.approx(141.5903225168, rel=1e-4)
    assert option.atmRate() == pytest.approx(0.0060224540, rel=1e-4)
    assert option.riskyAnnuity() == pytest.approx(4574668.9257, rel=1e-4)


def test_cdsoption_knocksout_default(cds_option_env):
    """CdsOption knocksOut defaults to True."""
    env = cds_option_env
    option = ql.CdsOption(env["cds"], env["exercise"])
    engine = ql.BlackCdsOptionEngine(
        env["dp_handle"], env["recovery"], env["r_handle"],
        ql.QuoteHandle(env["vol_quote"]),
    )
    option.setPricingEngine(engine)
    # Explicit knocksOut=True gives same result
    option2 = ql.CdsOption(env["cds"], env["exercise"], True)
    option2.setPricingEngine(engine)
    assert option2.NPV() == pytest.approx(option.NPV(), rel=1e-10)


# =============================================================================
# BlackCdsOptionEngine
# =============================================================================


def test_blackcdsoptionengine_handle_construction(cds_option_env):
    """BlackCdsOptionEngine constructs with Handle arguments."""
    env = cds_option_env
    engine = ql.BlackCdsOptionEngine(
        env["dp_handle"], env["recovery"], env["r_handle"],
        ql.QuoteHandle(env["vol_quote"]),
    )
    assert isinstance(engine, ql.base.PricingEngine)
    assert engine.termStructure() is not None
    assert engine.volatility() is not None


def test_blackcdsoptionengine_hidden_handle(cds_option_env):
    """BlackCdsOptionEngine hidden-handle constructor gives same NPV."""
    env = cds_option_env

    # Handle-based
    engine1 = ql.BlackCdsOptionEngine(
        env["dp_handle"], env["recovery"], env["r_handle"],
        ql.QuoteHandle(env["vol_quote"]),
    )
    option1 = ql.CdsOption(env["cds"], env["exercise"])
    option1.setPricingEngine(engine1)

    # Hidden handle (shared_ptr args)
    engine2 = ql.BlackCdsOptionEngine(
        env["dp_ts"], env["recovery"], env["r_ts"], env["vol_quote"],
    )
    option2 = ql.CdsOption(env["cds"], env["exercise"])
    option2.setPricingEngine(engine2)

    assert option2.NPV() == pytest.approx(option1.NPV(), rel=1e-10)
