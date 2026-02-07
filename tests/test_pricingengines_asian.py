"""
Tests for Asian option pricing engines.

Corresponds to src/pricingengines/asian/*.cpp bindings.
"""

import pytest

import pyquantlib as ql


@pytest.fixture(scope="module")
def asian_engine_env():
    """Setup for Asian engine tests."""
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

    # Monthly fixing dates
    fixing_dates = []
    d = today + ql.Period("1M")
    while d <= expiry:
        fixing_dates.append(d)
        d = d + ql.Period("1M")

    return {
        "process": process,
        "exercise": exercise,
        "payoff": payoff,
        "fixing_dates": fixing_dates,
    }


# =============================================================================
# AnalyticContinuousGeometricAveragePriceAsianEngine
# =============================================================================


def test_analytic_cont_geom_asian_engine(asian_engine_env):
    """Test analytic continuous geometric Asian engine."""
    opt = ql.ContinuousAveragingAsianOption(
        ql.AverageType.Geometric,
        asian_engine_env["payoff"],
        asian_engine_env["exercise"],
    )
    opt.setPricingEngine(
        ql.AnalyticContinuousGeometricAveragePriceAsianEngine(
            asian_engine_env["process"]
        )
    )
    assert opt.NPV() == pytest.approx(4.985759827210373, rel=1e-6)


# =============================================================================
# AnalyticDiscreteGeometricAveragePriceAsianEngine
# =============================================================================


def test_analytic_discr_geom_asian_engine(asian_engine_env):
    """Test analytic discrete geometric Asian engine."""
    opt = ql.DiscreteAveragingAsianOption(
        ql.AverageType.Geometric, 0.0, 0,
        asian_engine_env["fixing_dates"],
        asian_engine_env["payoff"],
        asian_engine_env["exercise"],
    )
    opt.setPricingEngine(
        ql.AnalyticDiscreteGeometricAveragePriceAsianEngine(
            asian_engine_env["process"]
        )
    )
    assert opt.NPV() == pytest.approx(5.307977902914936, rel=1e-6)


# =============================================================================
# TurnbullWakemanAsianEngine
# =============================================================================


def test_turnbullwakeman_engine(asian_engine_env):
    """Test Turnbull-Wakeman moment-matching engine."""
    opt = ql.DiscreteAveragingAsianOption(
        ql.AverageType.Arithmetic, 0.0, 0,
        asian_engine_env["fixing_dates"],
        asian_engine_env["payoff"],
        asian_engine_env["exercise"],
    )
    opt.setPricingEngine(
        ql.TurnbullWakemanAsianEngine(asian_engine_env["process"])
    )
    assert opt.NPV() == pytest.approx(5.515312691660706, rel=1e-6)


# =============================================================================
# MCDiscreteArithmeticAPEngine
# =============================================================================


def test_mc_discrete_arithmetic_engine(asian_engine_env):
    """Test MC discrete arithmetic average price Asian engine."""
    opt = ql.DiscreteAveragingAsianOption(
        ql.AverageType.Arithmetic, 0.0, 0,
        asian_engine_env["fixing_dates"],
        asian_engine_env["payoff"],
        asian_engine_env["exercise"],
    )
    engine = ql.MCDiscreteArithmeticAPEngine(
        asian_engine_env["process"],
        requiredSamples=100000,
        seed=42,
        controlVariate=True,
    )
    opt.setPricingEngine(engine)
    # MC result with tolerance
    assert opt.NPV() == pytest.approx(5.5, abs=0.2)


def test_mc_discrete_arithmetic_vs_turnbullwakeman(asian_engine_env):
    """Test MC and Turnbull-Wakeman give similar results."""
    fixing_dates = asian_engine_env["fixing_dates"]
    payoff = asian_engine_env["payoff"]
    exercise = asian_engine_env["exercise"]
    process = asian_engine_env["process"]

    mc_opt = ql.DiscreteAveragingAsianOption(
        ql.AverageType.Arithmetic, 0.0, 0, fixing_dates, payoff, exercise,
    )
    mc_opt.setPricingEngine(ql.MCDiscreteArithmeticAPEngine(
        process, requiredSamples=100000, seed=42, controlVariate=True,
    ))

    tw_opt = ql.DiscreteAveragingAsianOption(
        ql.AverageType.Arithmetic, 0.0, 0, fixing_dates, payoff, exercise,
    )
    tw_opt.setPricingEngine(ql.TurnbullWakemanAsianEngine(process))

    assert mc_opt.NPV() == pytest.approx(tw_opt.NPV(), rel=0.05)


def test_geometric_less_than_arithmetic(asian_engine_env):
    """Geometric average price is always <= arithmetic average price."""
    fixing_dates = asian_engine_env["fixing_dates"]
    payoff = asian_engine_env["payoff"]
    exercise = asian_engine_env["exercise"]
    process = asian_engine_env["process"]

    geom = ql.DiscreteAveragingAsianOption(
        ql.AverageType.Geometric, 0.0, 0, fixing_dates, payoff, exercise,
    )
    geom.setPricingEngine(
        ql.AnalyticDiscreteGeometricAveragePriceAsianEngine(process)
    )

    arith = ql.DiscreteAveragingAsianOption(
        ql.AverageType.Arithmetic, 0.0, 0, fixing_dates, payoff, exercise,
    )
    arith.setPricingEngine(ql.TurnbullWakemanAsianEngine(process))

    assert geom.NPV() < arith.NPV()
