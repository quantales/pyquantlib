"""
Tests for barrier option pricing engines.

Corresponds to src/pricingengines/barrier/*.cpp bindings.
"""

import pytest

import pyquantlib as ql


@pytest.fixture(scope="module")
def barrier_engine_env():
    """Setup for barrier engine tests."""
    today = ql.Date(15, ql.January, 2025)
    ql.Settings.evaluationDate = today

    spot = ql.SimpleQuote(100.0)
    rate = ql.FlatForward(today, 0.05, ql.Actual365Fixed())
    div = ql.FlatForward(today, 0.02, ql.Actual365Fixed())
    vol = ql.BlackConstantVol(today, ql.TARGET(), 0.20, ql.Actual365Fixed())

    process = ql.BlackScholesMertonProcess(
        ql.QuoteHandle(spot),
        ql.YieldTermStructureHandle(div),
        ql.YieldTermStructureHandle(rate),
        ql.BlackVolTermStructureHandle(vol),
    )

    expiry = today + ql.Period("1Y")
    exercise = ql.EuropeanExercise(expiry)
    payoff = ql.PlainVanillaPayoff(ql.Call, 100.0)

    option = ql.BarrierOption(ql.BarrierType.DownOut, 80.0, 0.0, payoff, exercise)

    return {
        "process": process,
        "option": option,
        "payoff": payoff,
        "exercise": exercise,
    }


# =============================================================================
# AnalyticBarrierEngine
# =============================================================================


def test_analyticbarrierengine_pricing(barrier_engine_env):
    """Test AnalyticBarrierEngine pricing."""
    opt = ql.BarrierOption(
        ql.BarrierType.DownOut, 80.0, 0.0,
        barrier_engine_env["payoff"], barrier_engine_env["exercise"],
    )
    opt.setPricingEngine(ql.AnalyticBarrierEngine(barrier_engine_env["process"]))
    assert opt.NPV() == pytest.approx(9.133306436498122, rel=1e-6)


# =============================================================================
# AnalyticDoubleBarrierEngine
# =============================================================================


def test_analyticdoublebarrierengine_pricing(barrier_engine_env):
    """Test AnalyticDoubleBarrierEngine pricing."""
    opt = ql.DoubleBarrierOption(
        ql.DoubleBarrierType.KnockOut, 80.0, 120.0, 0.0,
        barrier_engine_env["payoff"], barrier_engine_env["exercise"],
    )
    opt.setPricingEngine(
        ql.AnalyticDoubleBarrierEngine(barrier_engine_env["process"])
    )
    assert opt.NPV() == pytest.approx(1.073096658542509, rel=1e-6)


def test_analyticdoublebarrierengine_series(barrier_engine_env):
    """Test AnalyticDoubleBarrierEngine with custom series parameter."""
    opt = ql.DoubleBarrierOption(
        ql.DoubleBarrierType.KnockOut, 80.0, 120.0, 0.0,
        barrier_engine_env["payoff"], barrier_engine_env["exercise"],
    )
    opt.setPricingEngine(
        ql.AnalyticDoubleBarrierEngine(barrier_engine_env["process"], series=10)
    )
    assert opt.NPV() == pytest.approx(1.073096658542509, rel=1e-4)


# =============================================================================
# FdBlackScholesBarrierEngine
# =============================================================================


def test_fdblackscholesbarrierengine_pricing(barrier_engine_env):
    """Test FdBlackScholesBarrierEngine pricing."""
    opt = ql.BarrierOption(
        ql.BarrierType.DownOut, 80.0, 0.0,
        barrier_engine_env["payoff"], barrier_engine_env["exercise"],
    )
    opt.setPricingEngine(
        ql.FdBlackScholesBarrierEngine(barrier_engine_env["process"], 100, 100, 0)
    )
    assert opt.NPV() == pytest.approx(9.1332096241239, rel=1e-4)


def test_fdblackscholesbarrierengine_vs_analytic(barrier_engine_env):
    """Test FD barrier engine matches analytic closely."""
    payoff = barrier_engine_env["payoff"]
    exercise = barrier_engine_env["exercise"]
    process = barrier_engine_env["process"]

    analytic = ql.BarrierOption(ql.BarrierType.DownOut, 80.0, 0.0, payoff, exercise)
    analytic.setPricingEngine(ql.AnalyticBarrierEngine(process))

    fd = ql.BarrierOption(ql.BarrierType.DownOut, 80.0, 0.0, payoff, exercise)
    fd.setPricingEngine(ql.FdBlackScholesBarrierEngine(process, 100, 100, 0))

    assert fd.NPV() == pytest.approx(analytic.NPV(), rel=1e-3)


def test_doublebarrier_in_out_parity(barrier_engine_env):
    """Test KnockIn + KnockOut = Vanilla for double barrier."""
    payoff = barrier_engine_env["payoff"]
    exercise = barrier_engine_env["exercise"]
    process = barrier_engine_env["process"]

    ko = ql.DoubleBarrierOption(
        ql.DoubleBarrierType.KnockOut, 80.0, 120.0, 0.0, payoff, exercise,
    )
    ki = ql.DoubleBarrierOption(
        ql.DoubleBarrierType.KnockIn, 80.0, 120.0, 0.0, payoff, exercise,
    )
    engine = ql.AnalyticDoubleBarrierEngine(process)
    ko.setPricingEngine(engine)
    ki.setPricingEngine(engine)

    vanilla = ql.VanillaOption(payoff, exercise)
    vanilla.setPricingEngine(ql.AnalyticEuropeanEngine(process))

    assert ko.NPV() + ki.NPV() == pytest.approx(vanilla.NPV(), rel=1e-6)
