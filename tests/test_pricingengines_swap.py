"""
Tests for swap pricing engines.

Corresponds to src/pricingengines/swap/*.cpp bindings.
"""

import pytest

import pyquantlib as ql


@pytest.fixture
def ccyswap_engine_env():
    today = ql.Date(4, ql.June, 2025)
    ql.Settings.evaluationDate = today
    dc = ql.Actual365Fixed()
    eur_curve = ql.YieldTermStructureHandle(ql.FlatForward(today, 0.025, dc))
    usd_curve = ql.YieldTermStructureHandle(ql.FlatForward(today, 0.045, dc))
    spot_fx = ql.QuoteHandle(ql.SimpleQuote(1.05))  # USD per EUR

    start = ql.TARGET().advance(today, ql.Period(2, ql.Days))
    end = ql.TARGET().advance(start, ql.Period(2, ql.Years))
    us = ql.UnitedStates(ql.UnitedStates.Settlement)
    swap = ql.ConstNotionalCrossCurrencyFixedVsFloatingSwap(
        ql.SwapType.Payer,
        10_000_000.0, ql.EURCurrency(),
        ql.Schedule(start, end, ql.Period(3, ql.Months), ql.TARGET(),
                    ql.ModifiedFollowing, ql.ModifiedFollowing,
                    ql.DateGeneration.Forward, False),
        0.025, ql.Thirty360(ql.Thirty360.BondBasis), ql.ModifiedFollowing, 0,
        ql.TARGET(),
        10_500_000.0, ql.USDCurrency(),
        ql.Schedule(start, end, ql.Period(3, ql.Months), us,
                    ql.ModifiedFollowing, ql.ModifiedFollowing,
                    ql.DateGeneration.Forward, False),
        ql.USDLibor(ql.Period(3, ql.Months), usd_curve), 0.0,
        ql.ModifiedFollowing, 0, us,
    )
    return {
        "today": today,
        "dc": dc,
        "eur_curve": eur_curve,
        "usd_curve": usd_curve,
        "spot_fx": spot_fx,
        "swap": swap,
    }


def test_discountingconstnotionalcrosscurrencyswapengine_pricing(ccyswap_engine_env):
    """The NPV is reported in the engine's domestic currency (USD here)."""
    env = ccyswap_engine_env
    engine = ql.DiscountingConstNotionalCrossCurrencySwapEngine(
        ql.USDCurrency(), env["usd_curve"],
        ql.EURCurrency(), env["eur_curve"],
        env["spot_fx"],
    )
    swap = env["swap"]
    swap.setPricingEngine(engine)

    assert swap.NPV() == pytest.approx(1597.6101761822, rel=1e-4)
    assert swap.inCcyLegBPS(0) == pytest.approx(-1947.0753300395, rel=1e-4)
    assert swap.npvDateDiscounts(0) == pytest.approx(1.0)


def test_discountingconstnotionalcrosscurrencyswapengine_inspectors(ccyswap_engine_env):
    env = ccyswap_engine_env
    engine = ql.DiscountingConstNotionalCrossCurrencySwapEngine(
        ql.USDCurrency(), env["usd_curve"],
        ql.EURCurrency(), env["eur_curve"],
        env["spot_fx"],
    )

    assert engine.domesticCurrency().code() == "USD"
    assert engine.foreignCurrency().code() == "EUR"
    assert engine.spotFX().currentLink().value() == pytest.approx(1.05)
    assert engine.domesticCcyDiscountCurve().currentLink().referenceDate() == (
        ql.Date(4, ql.June, 2025)
    )
    assert engine.foreignCcyDiscountCurve().currentLink().referenceDate() == (
        ql.Date(4, ql.June, 2025)
    )


def test_discountingconstnotionalcrosscurrencyswapengine_hidden_handles(ccyswap_engine_env):
    """The hidden-handle constructor prices identically to the handle one."""
    env = ccyswap_engine_env
    engine = ql.DiscountingConstNotionalCrossCurrencySwapEngine(
        ql.USDCurrency(), ql.FlatForward(env["today"], 0.045, env["dc"]),
        ql.EURCurrency(), ql.FlatForward(env["today"], 0.025, env["dc"]),
        ql.SimpleQuote(1.05),
    )
    swap = env["swap"]
    swap.setPricingEngine(engine)

    assert swap.NPV() == pytest.approx(1597.6101761822, rel=1e-4)


def test_discountingconstnotionalcrosscurrencyswapengine_npv_date(ccyswap_engine_env):
    """A later NPV date moves the valuation point of both legs."""
    env = ccyswap_engine_env
    engine = ql.DiscountingConstNotionalCrossCurrencySwapEngine(
        ql.USDCurrency(), env["usd_curve"],
        ql.EURCurrency(), env["eur_curve"],
        env["spot_fx"],
        npvDate=ql.Date(4, ql.December, 2025),
    )
    swap = env["swap"]
    swap.setPricingEngine(engine)

    assert swap.NPV() == pytest.approx(1617.7610401908, rel=1e-4)
    assert swap.npvDateDiscounts(0) == pytest.approx(0.9875439799, rel=1e-6)
