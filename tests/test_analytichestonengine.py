import pytest

import pyquantlib as ql


@pytest.fixture
def heston_env():
    """Standard Heston market environment."""
    today = ql.Date(20, 2, 2025)
    ql.Settings.instance().evaluationDate = today

    dc = ql.Actual365Fixed()
    cal = ql.TARGET()

    spot = ql.SimpleQuote(100.0)
    rate = ql.SimpleQuote(0.05)
    div = ql.SimpleQuote(0.02)

    risk_free_ts = ql.FlatForward(today, ql.QuoteHandle(rate), dc)
    dividend_ts = ql.FlatForward(today, ql.QuoteHandle(div), dc)

    # Heston parameters
    v0 = 0.04      # Initial variance
    kappa = 2.0    # Mean reversion
    theta = 0.04   # Long-term variance
    sigma = 0.3    # Vol of vol
    rho = -0.7     # Correlation

    process = ql.HestonProcess(
        ql.YieldTermStructureHandle(risk_free_ts),
        ql.YieldTermStructureHandle(dividend_ts),
        ql.QuoteHandle(spot),
        v0, kappa, theta, sigma, rho,
    )

    model = ql.HestonModel(process)

    return {"model": model, "process": process, "today": today}


def test_heston_model_parameters(heston_env):
    """Test HestonModel parameter accessors."""
    model = heston_env["model"]

    assert model.v0() == pytest.approx(0.04)
    assert model.kappa() == pytest.approx(2.0)
    assert model.theta() == pytest.approx(0.04)
    assert model.sigma() == pytest.approx(0.3)
    assert model.rho() == pytest.approx(-0.7)


def test_analytic_heston_engine_lobatto(heston_env):
    """Test AnalyticHestonEngine with Gauss-Lobatto integration."""
    model = heston_env["model"]
    today = heston_env["today"]

    payoff = ql.PlainVanillaPayoff(ql.OptionType.Call, 100.0)
    exercise = ql.EuropeanExercise(today + ql.Period(1, ql.Years))
    option = ql.VanillaOption(payoff, exercise)

    engine = ql.AnalyticHestonEngine(model, 1e-8, 1000)
    option.setPricingEngine(engine)

    npv = option.NPV()
    assert npv == pytest.approx(9.0595, abs=0.01)


def test_analytic_heston_engine_laguerre(heston_env):
    """Test AnalyticHestonEngine with Gauss-Laguerre integration."""
    model = heston_env["model"]
    today = heston_env["today"]

    payoff = ql.PlainVanillaPayoff(ql.OptionType.Call, 100.0)
    exercise = ql.EuropeanExercise(today + ql.Period(1, ql.Years))
    option = ql.VanillaOption(payoff, exercise)

    engine = ql.AnalyticHestonEngine(model, 144)
    option.setPricingEngine(engine)

    npv = option.NPV()
    assert npv == pytest.approx(9.0595, abs=0.01)


def test_analytic_heston_engine_full_control(heston_env):
    """Test AnalyticHestonEngine with full control constructor."""
    model = heston_env["model"]
    today = heston_env["today"]

    payoff = ql.PlainVanillaPayoff(ql.OptionType.Call, 100.0)
    exercise = ql.EuropeanExercise(today + ql.Period(1, ql.Years))
    option = ql.VanillaOption(payoff, exercise)

    integration = ql.Integration.gaussLaguerre(128)
    engine = ql.AnalyticHestonEngine(
        model,
        ql.ComplexLogFormula.Gatheral,
        integration,
    )
    option.setPricingEngine(engine)

    npv = option.NPV()
    assert npv == pytest.approx(9.0595, abs=0.01)


def test_integration_methods():
    """Test various integration method constructors."""
    assert ql.Integration.gaussLaguerre(128) is not None
    assert ql.Integration.gaussLegendre(128) is not None
    assert ql.Integration.gaussChebyshev(128) is not None
    assert ql.Integration.gaussLobatto(1e-8, 1e-8, 1000) is not None
    assert ql.Integration.gaussKronrod(1e-8, 1000) is not None
    assert ql.Integration.simpson(1e-8, 1000) is not None
    assert ql.Integration.discreteSimpson(1000) is not None
    assert ql.Integration.expSinh(1e-8) is not None


def test_complex_log_formula_enum():
    """Test ComplexLogFormula enum values."""
    assert ql.ComplexLogFormula.Gatheral is not None
    assert ql.ComplexLogFormula.BranchCorrection is not None
    assert ql.ComplexLogFormula.AndersenPiterbarg is not None


def test_heston_model_handle(heston_env):
    """Test HestonModelHandle."""
    model = heston_env["model"]
    handle = ql.HestonModelHandle(model)

    assert handle.currentLink() is not None
    assert handle.currentLink().v0() == pytest.approx(0.04)
