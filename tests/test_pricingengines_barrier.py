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


# =============================================================================
# AnalyticDoubleBarrierBinaryEngine
# =============================================================================


def test_analyticdoublebarrierbinaryengine_construction(barrier_engine_env):
    """Test AnalyticDoubleBarrierBinaryEngine construction."""
    engine = ql.AnalyticDoubleBarrierBinaryEngine(barrier_engine_env["process"])
    assert engine is not None


def test_analyticdoublebarrierbinaryengine_pricing(barrier_engine_env):
    """Test AnalyticDoubleBarrierBinaryEngine pricing."""
    payoff = ql.CashOrNothingPayoff(ql.Call, 100.0, 1.0)
    opt = ql.DoubleBarrierOption(
        ql.DoubleBarrierType.KnockOut, 80.0, 120.0, 0.0,
        payoff, barrier_engine_env["exercise"],
    )
    opt.setPricingEngine(
        ql.AnalyticDoubleBarrierBinaryEngine(barrier_engine_env["process"])
    )
    assert opt.NPV() == pytest.approx(0.35787453145602244, rel=1e-6)


# =============================================================================
# FdBlackScholesRebateEngine
# =============================================================================


def test_fdblackscholesrebateengine_construction(barrier_engine_env):
    """Test FdBlackScholesRebateEngine construction."""
    engine = ql.FdBlackScholesRebateEngine(barrier_engine_env["process"])
    assert engine is not None


def test_fdblackscholesrebateengine_pricing(barrier_engine_env):
    """Test FdBlackScholesRebateEngine pricing with rebate."""
    payoff = barrier_engine_env["payoff"]
    exercise = barrier_engine_env["exercise"]
    rebate = 5.0

    opt = ql.BarrierOption(
        ql.BarrierType.DownOut, 80.0, rebate, payoff, exercise,
    )
    opt.setPricingEngine(
        ql.FdBlackScholesRebateEngine(barrier_engine_env["process"], 100, 100, 0)
    )
    assert opt.NPV() == pytest.approx(4.782663637316863, rel=1e-4)


def test_fdblackscholesrebateengine_params(barrier_engine_env):
    """Test FdBlackScholesRebateEngine with custom parameters."""
    engine = ql.FdBlackScholesRebateEngine(
        barrier_engine_env["process"],
        tGrid=50, xGrid=50, dampingSteps=1,
    )
    assert engine is not None


# =============================================================================
# MCBarrierEngine
# =============================================================================


def test_mcbarrierengine_construction(barrier_engine_env):
    """Test MCBarrierEngine construction."""
    engine = ql.MCBarrierEngine(
        barrier_engine_env["process"], timeSteps=10, requiredSamples=1000, seed=42,
    )
    assert engine is not None


def test_mcbarrierengine_pricing(barrier_engine_env):
    """Test MCBarrierEngine produces reasonable price."""
    payoff = barrier_engine_env["payoff"]
    exercise = barrier_engine_env["exercise"]
    process = barrier_engine_env["process"]

    opt = ql.BarrierOption(
        ql.BarrierType.DownOut, 80.0, 0.0, payoff, exercise,
    )
    opt.setPricingEngine(
        ql.MCBarrierEngine(process, timeSteps=50, requiredSamples=10000, seed=42)
    )
    assert opt.NPV() == pytest.approx(9.246989568419083, rel=1e-6)


def test_mcbarrierengine_biased(barrier_engine_env):
    """Test MCBarrierEngine with biased path pricer."""
    payoff = barrier_engine_env["payoff"]
    exercise = barrier_engine_env["exercise"]

    opt = ql.BarrierOption(
        ql.BarrierType.DownOut, 80.0, 0.0, payoff, exercise,
    )
    opt.setPricingEngine(
        ql.MCBarrierEngine(
            barrier_engine_env["process"],
            timeSteps=50, requiredSamples=10000, isBiased=True, seed=42,
        )
    )
    assert opt.NPV() > 0.0


def test_mcbarrierengine_lowdiscrepancy(barrier_engine_env):
    """Test MCBarrierEngine with low-discrepancy RNG."""
    payoff = barrier_engine_env["payoff"]
    exercise = barrier_engine_env["exercise"]

    opt = ql.BarrierOption(
        ql.BarrierType.DownOut, 80.0, 0.0, payoff, exercise,
    )
    opt.setPricingEngine(
        ql.MCBarrierEngine(
            barrier_engine_env["process"],
            rngType="lowdiscrepancy", timeSteps=50, requiredSamples=10000,
        )
    )
    assert opt.NPV() > 0.0


# =============================================================================
# MCDoubleBarrierEngine
# =============================================================================


def test_mcdoublebarrierengine_construction(barrier_engine_env):
    """Test MCDoubleBarrierEngine construction."""
    engine = ql.MCDoubleBarrierEngine(
        barrier_engine_env["process"], timeSteps=10, requiredSamples=1000, seed=42,
    )
    assert engine is not None


def test_mcdoublebarrierengine_pricing(barrier_engine_env):
    """Test MCDoubleBarrierEngine produces reasonable price."""
    payoff = barrier_engine_env["payoff"]
    exercise = barrier_engine_env["exercise"]
    process = barrier_engine_env["process"]

    opt = ql.DoubleBarrierOption(
        ql.DoubleBarrierType.KnockOut, 80.0, 120.0, 0.0, payoff, exercise,
    )
    opt.setPricingEngine(
        ql.MCDoubleBarrierEngine(process, timeSteps=50, requiredSamples=10000, seed=42)
    )
    assert opt.NPV() == pytest.approx(1.4141439594643788, rel=1e-6)


def test_mcdoublebarrierengine_lowdiscrepancy(barrier_engine_env):
    """Test MCDoubleBarrierEngine with low-discrepancy RNG."""
    payoff = barrier_engine_env["payoff"]
    exercise = barrier_engine_env["exercise"]

    opt = ql.DoubleBarrierOption(
        ql.DoubleBarrierType.KnockOut, 80.0, 120.0, 0.0, payoff, exercise,
    )
    opt.setPricingEngine(
        ql.MCDoubleBarrierEngine(
            barrier_engine_env["process"],
            rngType="lowdiscrepancy", timeSteps=50, requiredSamples=10000,
        )
    )
    assert opt.NPV() > 0.0
