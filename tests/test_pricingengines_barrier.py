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


# =============================================================================
# AnalyticBinaryBarrierEngine
# =============================================================================


def test_analyticbinarybarrierengine_pricing(barrier_engine_env):
    """Test AnalyticBinaryBarrierEngine pricing."""
    am_exercise = ql.AmericanExercise(
        ql.Date(15, ql.January, 2025),
        ql.Date(15, ql.January, 2025) + ql.Period("1Y"),
        payoffAtExpiry=True,
    )
    binary_payoff = ql.CashOrNothingPayoff(ql.Call, 100.0, 1.0)
    opt = ql.BarrierOption(
        ql.BarrierType.DownOut, 80.0, 0.0, binary_payoff, am_exercise,
    )
    opt.setPricingEngine(ql.AnalyticBinaryBarrierEngine(barrier_engine_env["process"]))
    assert opt.NPV() == pytest.approx(0.4821800827386251, rel=1e-6)


def test_analyticbinarybarrierengine_knockin(barrier_engine_env):
    """Test AnalyticBinaryBarrierEngine knock-in pricing."""
    am_exercise = ql.AmericanExercise(
        ql.Date(15, ql.January, 2025),
        ql.Date(15, ql.January, 2025) + ql.Period("1Y"),
        payoffAtExpiry=True,
    )
    binary_payoff = ql.CashOrNothingPayoff(ql.Call, 100.0, 1.0)
    opt = ql.BarrierOption(
        ql.BarrierType.DownIn, 80.0, 0.0, binary_payoff, am_exercise,
    )
    opt.setPricingEngine(ql.AnalyticBinaryBarrierEngine(barrier_engine_env["process"]))
    assert opt.NPV() == pytest.approx(0.012401008314598444, rel=1e-6)


# =============================================================================
# BinomialBarrierEngine
# =============================================================================


def test_binomialbarrierengine_crr(barrier_engine_env):
    """Test BinomialBarrierEngine with CRR tree."""
    opt = ql.BarrierOption(
        ql.BarrierType.DownOut, 80.0, 0.0,
        barrier_engine_env["payoff"], barrier_engine_env["exercise"],
    )
    opt.setPricingEngine(
        ql.BinomialBarrierEngine(barrier_engine_env["process"], "crr", 200)
    )
    assert opt.NPV() == pytest.approx(9.143885847791243, rel=1e-6)


def test_binomialbarrierengine_jr(barrier_engine_env):
    """Test BinomialBarrierEngine with JR tree."""
    opt = ql.BarrierOption(
        ql.BarrierType.DownOut, 80.0, 0.0,
        barrier_engine_env["payoff"], barrier_engine_env["exercise"],
    )
    opt.setPricingEngine(
        ql.BinomialBarrierEngine(barrier_engine_env["process"], "jr", 200)
    )
    assert opt.NPV() == pytest.approx(9.160286051475572, rel=1e-6)


def test_binomialbarrierengine_dermankani(barrier_engine_env):
    """Test BinomialBarrierEngine with Derman-Kani discretization."""
    opt = ql.BarrierOption(
        ql.BarrierType.DownOut, 80.0, 0.0,
        barrier_engine_env["payoff"], barrier_engine_env["exercise"],
    )
    opt.setPricingEngine(
        ql.BinomialBarrierEngine(
            barrier_engine_env["process"], "crr", 200, discretization="dermankani",
        )
    )
    assert opt.NPV() == pytest.approx(9.142520528763514, rel=1e-6)


def test_binomialbarrierengine_vs_analytic(barrier_engine_env):
    """Test binomial barrier engine converges to analytic."""
    payoff = barrier_engine_env["payoff"]
    exercise = barrier_engine_env["exercise"]
    process = barrier_engine_env["process"]

    analytic = ql.BarrierOption(ql.BarrierType.DownOut, 80.0, 0.0, payoff, exercise)
    analytic.setPricingEngine(ql.AnalyticBarrierEngine(process))

    binom = ql.BarrierOption(ql.BarrierType.DownOut, 80.0, 0.0, payoff, exercise)
    binom.setPricingEngine(ql.BinomialBarrierEngine(process, "crr", 200))

    assert binom.NPV() == pytest.approx(analytic.NPV(), rel=1e-2)


# =============================================================================
# FdHestonBarrierEngine
# =============================================================================


@pytest.fixture(scope="module")
def heston_barrier_env():
    """Setup for Heston barrier engine tests."""
    today = ql.Date(15, ql.January, 2025)
    ql.Settings.evaluationDate = today

    spot = ql.SimpleQuote(100.0)
    rate = ql.FlatForward(today, 0.05, ql.Actual365Fixed())
    div = ql.FlatForward(today, 0.02, ql.Actual365Fixed())

    heston_process = ql.HestonProcess(
        ql.YieldTermStructureHandle(rate),
        ql.YieldTermStructureHandle(div),
        ql.QuoteHandle(spot),
        0.04, 2.0, 0.04, 0.5, -0.7,
    )
    heston_model = ql.HestonModel(heston_process)

    expiry = today + ql.Period("1Y")
    exercise = ql.EuropeanExercise(expiry)
    payoff = ql.PlainVanillaPayoff(ql.Call, 100.0)

    return {
        "model": heston_model,
        "exercise": exercise,
        "payoff": payoff,
    }


def test_fdhestonbarrierengine_pricing(heston_barrier_env):
    """Test FdHestonBarrierEngine pricing."""
    opt = ql.BarrierOption(
        ql.BarrierType.DownOut, 80.0, 0.0,
        heston_barrier_env["payoff"], heston_barrier_env["exercise"],
    )
    opt.setPricingEngine(
        ql.FdHestonBarrierEngine(heston_barrier_env["model"], 50, 100, 50)
    )
    assert opt.NPV() == pytest.approx(8.491695384530761, rel=1e-4)


# =============================================================================
# FdHestonDoubleBarrierEngine
# =============================================================================


def test_fdhestondoublebarrierengine_pricing(heston_barrier_env):
    """Test FdHestonDoubleBarrierEngine pricing."""
    opt = ql.DoubleBarrierOption(
        ql.DoubleBarrierType.KnockOut, 80.0, 120.0, 0.0,
        heston_barrier_env["payoff"], heston_barrier_env["exercise"],
    )
    opt.setPricingEngine(
        ql.FdHestonDoubleBarrierEngine(heston_barrier_env["model"], 50, 100, 50)
    )
    assert opt.NPV() == pytest.approx(2.9932595843170007, rel=1e-4)


# =============================================================================
# FdHestonRebateEngine
# =============================================================================


def test_fdhestonrebateengine_pricing(heston_barrier_env):
    """Test FdHestonRebateEngine pricing with rebate."""
    opt = ql.BarrierOption(
        ql.BarrierType.DownOut, 80.0, 5.0,
        heston_barrier_env["payoff"], heston_barrier_env["exercise"],
    )
    opt.setPricingEngine(
        ql.FdHestonRebateEngine(heston_barrier_env["model"], 50, 100, 50)
    )
    assert opt.NPV() == pytest.approx(4.79105607818244, rel=1e-4)


# =============================================================================
# AnalyticPartialTimeBarrierOptionEngine
# =============================================================================


def test_analyticpartialtimebarrieroptionengine_pricing(barrier_engine_env):
    """Test AnalyticPartialTimeBarrierOptionEngine pricing."""
    today = ql.Date(15, ql.January, 2025)
    cover_date = today + ql.Period("6M")
    opt = ql.PartialTimeBarrierOption(
        ql.BarrierType.DownOut, ql.PartialBarrierRange.Start,
        80.0, 0.0, cover_date,
        barrier_engine_env["payoff"], barrier_engine_env["exercise"],
    )
    opt.setPricingEngine(
        ql.AnalyticPartialTimeBarrierOptionEngine(barrier_engine_env["process"])
    )
    assert opt.NPV() == pytest.approx(9.14972425417782, rel=1e-6)


# =============================================================================
# AnalyticSoftBarrierEngine
# =============================================================================


def test_analyticsoftbarrierengine_pricing(barrier_engine_env):
    """Test AnalyticSoftBarrierEngine pricing."""
    opt = ql.SoftBarrierOption(
        ql.BarrierType.DownOut, 70.0, 80.0,
        barrier_engine_env["payoff"], barrier_engine_env["exercise"],
    )
    opt.setPricingEngine(
        ql.AnalyticSoftBarrierEngine(barrier_engine_env["process"])
    )
    assert opt.NPV() == pytest.approx(9.204022684248903, rel=1e-6)


def test_analyticsoftbarrierengine_knockin(barrier_engine_env):
    """Test AnalyticSoftBarrierEngine knock-in pricing."""
    opt = ql.SoftBarrierOption(
        ql.BarrierType.DownIn, 80.0, 90.0,
        barrier_engine_env["payoff"], barrier_engine_env["exercise"],
    )
    opt.setPricingEngine(
        ql.AnalyticSoftBarrierEngine(barrier_engine_env["process"])
    )
    assert opt.NPV() == pytest.approx(0.599188319787428, rel=1e-6)


# =============================================================================
# AnalyticTwoAssetBarrierEngine
# =============================================================================


def test_analytictwoassetbarrierengine_pricing(barrier_engine_env):
    """Test AnalyticTwoAssetBarrierEngine pricing."""
    today = ql.Date(15, ql.January, 2025)
    spot2 = ql.SimpleQuote(110.0)
    rate = ql.FlatForward(today, 0.05, ql.Actual365Fixed())
    div = ql.FlatForward(today, 0.02, ql.Actual365Fixed())
    vol2 = ql.BlackConstantVol(today, ql.TARGET(), 0.25, ql.Actual365Fixed())
    process2 = ql.BlackScholesMertonProcess(
        ql.QuoteHandle(spot2),
        ql.YieldTermStructureHandle(div),
        ql.YieldTermStructureHandle(rate),
        ql.BlackVolTermStructureHandle(vol2),
    )

    opt = ql.TwoAssetBarrierOption(
        ql.BarrierType.DownOut, 80.0,
        barrier_engine_env["payoff"], barrier_engine_env["exercise"],
    )
    rho_quote = ql.SimpleQuote(0.5)
    opt.setPricingEngine(
        ql.AnalyticTwoAssetBarrierEngine(
            barrier_engine_env["process"], process2, rho_quote,
        )
    )
    assert opt.NPV() == pytest.approx(8.600164075254149, rel=1e-6)
