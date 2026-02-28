"""
Tests for vanilla option pricing engines.

Corresponds to src/pricingengines/vanilla/*.cpp bindings.
"""

import pytest

import pyquantlib as ql
from pyquantlib.base import PricingEngine


# =============================================================================
# PricingEngine ABC
# =============================================================================


class MyArguments(PricingEngine.arguments):
    """Custom arguments class for testing."""
    def __init__(self):
        super().__init__()
        self.spot_price = None

    def validate(self):
        if self.spot_price is None or self.spot_price <= 0:
            raise ql.Error("Spot price must be positive.")


class MyResults(PricingEngine.results):
    """Custom results class for testing."""
    def __init__(self):
        super().__init__()
        self.value = None

    def reset(self):
        self.value = None


class MyPricingEngine(PricingEngine):
    """Custom pricing engine for testing."""
    def __init__(self, multiplier):
        super().__init__()
        self._multiplier = multiplier
        self._arguments = MyArguments()
        self._results = MyResults()

    def getArguments(self):
        return self._arguments

    def getResults(self):
        return self._results

    def calculate(self):
        self.getArguments().validate()
        self.getResults().value = self.getArguments().spot_price * self._multiplier

    def reset(self):
        self.getResults().reset()

    def update(self):
        self.notifyObservers()


def test_pricingengine_custom_calculate():
    """Test custom engine calculate method."""
    engine = MyPricingEngine(multiplier=1.5)
    engine.getArguments().spot_price = 100.0

    engine.calculate()

    assert engine.getResults().value == pytest.approx(150.0)


def test_pricingengine_custom_reset():
    """Test custom engine reset method."""
    engine = MyPricingEngine(multiplier=1.5)
    engine.getArguments().spot_price = 100.0
    engine.calculate()

    engine.reset()

    assert engine.getResults().value is None


def test_pricingengine_arguments_validate():
    """Test custom arguments validation."""
    engine = MyPricingEngine(multiplier=1.5)
    engine.getArguments().spot_price = -10.0

    with pytest.raises(ql.Error, match="Spot price must be positive"):
        engine.calculate()


def test_pricingengine_inheritance_hierarchy():
    """Test PricingEngine inheritance hierarchy."""
    engine = MyPricingEngine(multiplier=1.0)

    assert isinstance(engine, PricingEngine)
    assert isinstance(engine.getArguments(), PricingEngine.arguments)
    assert isinstance(engine.getResults(), PricingEngine.results)


# =============================================================================
# American Option Environment
# =============================================================================


@pytest.fixture
def american_env():
    """Market environment for American option engine tests."""
    today = ql.Date(15, ql.May, 1998)
    settlement = ql.Date(17, ql.May, 1998)
    ql.Settings.instance().evaluationDate = today

    dc = ql.Actual365Fixed()
    cal = ql.TARGET()

    spot = ql.SimpleQuote(36.0)
    risk_free_ts = ql.FlatForward(settlement, 0.06, dc)
    dividend_ts = ql.FlatForward(settlement, 0.00, dc)
    vol_ts = ql.BlackConstantVol(settlement, cal, 0.20, dc)

    process = ql.BlackScholesMertonProcess(
        ql.QuoteHandle(spot),
        ql.YieldTermStructureHandle(dividend_ts),
        ql.YieldTermStructureHandle(risk_free_ts),
        ql.BlackVolTermStructureHandle(vol_ts),
    )

    # American put option
    payoff = ql.PlainVanillaPayoff(ql.OptionType.Put, 40.0)
    maturity = ql.Date(17, ql.May, 1999)
    exercise = ql.AmericanExercise(settlement, maturity)
    option = ql.VanillaOption(payoff, exercise)

    return {"option": option, "process": process, "payoff": payoff}


# =============================================================================
# Barone-Adesi-Whaley
# =============================================================================


def test_baw_construction(american_env):
    """Test BaroneAdesiWhaleyApproximationEngine construction."""
    engine = ql.BaroneAdesiWhaleyApproximationEngine(american_env["process"])
    assert engine is not None


def test_baw_pricing(american_env):
    """Test BAW engine produces reasonable price."""
    option = american_env["option"]
    engine = ql.BaroneAdesiWhaleyApproximationEngine(american_env["process"])
    option.setPricingEngine(engine)

    npv = option.NPV()
    assert npv == pytest.approx(4.459, abs=0.01)


# =============================================================================
# Bjerksund-Stensland
# =============================================================================


def test_bjerksund_stensland_construction(american_env):
    """Test BjerksundStenslandApproximationEngine construction."""
    engine = ql.BjerksundStenslandApproximationEngine(american_env["process"])
    assert engine is not None


def test_bjerksund_stensland_pricing(american_env):
    """Test Bjerksund-Stensland engine produces reasonable price."""
    option = american_env["option"]
    engine = ql.BjerksundStenslandApproximationEngine(american_env["process"])
    option.setPricingEngine(engine)

    npv = option.NPV()
    assert npv == pytest.approx(4.453, abs=0.01)


# =============================================================================
# Finite Differences
# =============================================================================


def test_fd_construction(american_env):
    """Test FdBlackScholesVanillaEngine construction."""
    engine = ql.FdBlackScholesVanillaEngine(american_env["process"])
    assert engine is not None


def test_fd_construction_with_params(american_env):
    """Test FD engine construction with custom parameters."""
    engine = ql.FdBlackScholesVanillaEngine(
        american_env["process"],
        tGrid=200,
        xGrid=200,
        dampingSteps=0,
        schemeDesc=ql.FdmSchemeDesc.Douglas(),
    )
    assert engine is not None


def test_fd_pricing(american_env):
    """Test FD engine produces reasonable price."""
    option = american_env["option"]
    engine = ql.FdBlackScholesVanillaEngine(
        american_env["process"], tGrid=801, xGrid=800
    )
    option.setPricingEngine(engine)

    npv = option.NPV()
    assert npv == pytest.approx(4.486, abs=0.01)


def test_fd_schemes(american_env):
    """Test FD engine with different schemes."""
    schemes = [
        ql.FdmSchemeDesc.Douglas(),
        ql.FdmSchemeDesc.CrankNicolson(),
        ql.FdmSchemeDesc.ImplicitEuler(),
    ]
    for scheme in schemes:
        engine = ql.FdBlackScholesVanillaEngine(
            american_env["process"], tGrid=100, xGrid=100, schemeDesc=scheme
        )
        american_env["option"].setPricingEngine(engine)
        npv = american_env["option"].NPV()
        assert npv == pytest.approx(4.48, rel=1e-2)


# =============================================================================
# Binomial
# =============================================================================


def test_binomial_construction(american_env):
    """Test BinomialVanillaEngine construction."""
    engine = ql.BinomialVanillaEngine(american_env["process"], "crr", 801)
    assert engine is not None


def test_binomial_all_tree_types(american_env):
    """Test all binomial tree types."""
    tree_types = ["jr", "crr", "eqp", "trigeorgis", "tian", "lr", "joshi"]

    for tree_type in tree_types:
        engine = ql.BinomialVanillaEngine(american_env["process"], tree_type, 100)
        american_env["option"].setPricingEngine(engine)
        npv = american_env["option"].NPV()
        assert 4.0 < npv < 5.0, f"Tree type {tree_type} gave NPV {npv}"


def test_binomial_pricing_crr(american_env):
    """Test CRR binomial pricing."""
    option = american_env["option"]
    engine = ql.BinomialVanillaEngine(american_env["process"], "crr", 801)
    option.setPricingEngine(engine)

    npv = option.NPV()
    assert npv == pytest.approx(4.486, abs=0.01)


def test_binomial_pricing_lr(american_env):
    """Test Leisen-Reimer binomial pricing."""
    option = american_env["option"]
    engine = ql.BinomialVanillaEngine(american_env["process"], "lr", 801)
    option.setPricingEngine(engine)

    npv = option.NPV()
    assert npv == pytest.approx(4.486, abs=0.01)


def test_binomial_invalid_tree_type(american_env):
    """Test error handling for invalid tree type."""
    with pytest.raises(RuntimeError, match="Unknown tree type"):
        ql.BinomialVanillaEngine(american_env["process"], "invalid", 100)


def test_binomial_case_insensitive(american_env):
    """Test tree type is case insensitive."""
    engine1 = ql.BinomialVanillaEngine(american_env["process"], "CRR", 100)
    engine2 = ql.BinomialVanillaEngine(american_env["process"], "crr", 100)
    engine3 = ql.BinomialVanillaEngine(american_env["process"], "CoxRossRubinstein", 100)

    assert engine1 is not None
    assert engine2 is not None
    assert engine3 is not None


# =============================================================================
# MCAmericanEngine (Longstaff-Schwartz)
# =============================================================================


def test_mc_american_construction(american_env):
    """Test MCAmericanEngine construction."""
    engine = ql.MCAmericanEngine(
        american_env["process"], timeSteps=100, requiredSamples=1000, seed=42
    )
    assert engine is not None


def test_mc_american_pricing(american_env):
    """Test MC American engine produces reasonable price."""
    option = american_env["option"]
    engine = ql.MCAmericanEngine(
        american_env["process"],
        timeSteps=100,
        antitheticVariate=True,
        requiredTolerance=0.02,
        calibrationSamples=4096,
        seed=42,
    )
    option.setPricingEngine(engine)

    npv = option.NPV()
    assert npv == pytest.approx(4.48, abs=0.1)


def test_mc_american_polynomial_types(american_env):
    """Test MC American with different polynomial basis types."""
    poly_types = [
        ql.PolynomialType.Monomial,
        ql.PolynomialType.Laguerre,
        ql.PolynomialType.Hermite,
    ]

    for poly_type in poly_types:
        engine = ql.MCAmericanEngine(
            american_env["process"],
            timeSteps=50,
            requiredSamples=2000,
            polynomialType=poly_type,
            seed=42,
        )
        american_env["option"].setPricingEngine(engine)
        npv = american_env["option"].NPV()
        assert 3.5 < npv < 5.5


def test_mc_american_lowdiscrepancy(american_env):
    """Test MC American with low discrepancy RNG."""
    engine = ql.MCAmericanEngine(
        american_env["process"],
        rngType="lowdiscrepancy",
        timeSteps=100,
        requiredSamples=4096,
    )
    american_env["option"].setPricingEngine(engine)
    npv = american_env["option"].NPV()
    assert 3.5 < npv < 5.5


def test_mc_american_invalid_rng(american_env):
    """Test error handling for invalid RNG type."""
    with pytest.raises(RuntimeError, match="Unsupported RNG type"):
        ql.MCAmericanEngine(
            american_env["process"], rngType="invalid", timeSteps=100, requiredSamples=1000
        )


# =============================================================================
# European Option Environment
# =============================================================================


@pytest.fixture
def european_env():
    """Market environment for European option engine tests."""
    today = ql.Date(15, ql.May, 1998)
    settlement = ql.Date(17, ql.May, 1998)
    ql.Settings.instance().evaluationDate = today

    dc = ql.Actual365Fixed()
    cal = ql.TARGET()

    spot = ql.SimpleQuote(36.0)
    risk_free_ts = ql.FlatForward(settlement, 0.06, dc)
    dividend_ts = ql.FlatForward(settlement, 0.00, dc)
    vol_ts = ql.BlackConstantVol(settlement, cal, 0.20, dc)

    process = ql.BlackScholesMertonProcess(
        ql.QuoteHandle(spot),
        ql.YieldTermStructureHandle(dividend_ts),
        ql.YieldTermStructureHandle(risk_free_ts),
        ql.BlackVolTermStructureHandle(vol_ts),
    )

    # European put option
    payoff = ql.PlainVanillaPayoff(ql.OptionType.Put, 40.0)
    maturity = ql.Date(17, ql.May, 1999)
    exercise = ql.EuropeanExercise(maturity)
    option = ql.VanillaOption(payoff, exercise)

    return {"option": option, "process": process, "settlement": settlement}


# =============================================================================
# IntegralEngine
# =============================================================================


def test_integral_engine_construction(european_env):
    """Test IntegralEngine construction."""
    engine = ql.IntegralEngine(european_env["process"])
    assert engine is not None


def test_integral_engine_pricing(european_env):
    """Test IntegralEngine produces reasonable price."""
    option = european_env["option"]
    engine = ql.IntegralEngine(european_env["process"])
    option.setPricingEngine(engine)

    npv = option.NPV()
    # European put should be close to but less than American put (~4.486)
    assert 3.8 < npv < 4.5


# =============================================================================
# MCEuropeanEngine
# =============================================================================


@pytest.fixture
def mc_env():
    """Market environment for MC engine tests."""
    today = ql.Date(20, 2, 2025)
    ql.Settings.instance().evaluationDate = today

    dc = ql.Actual365Fixed()
    cal = ql.TARGET()

    risk_free_ts = ql.FlatForward(today, 0.05, dc)
    dividend_ts = ql.FlatForward(today, 0.01, dc)
    vol_ts = ql.BlackConstantVol(today, cal, 0.20, dc)

    spot = ql.SimpleQuote(100.0)
    process = ql.BlackScholesMertonProcess(
        ql.QuoteHandle(spot),
        ql.YieldTermStructureHandle(dividend_ts),
        ql.YieldTermStructureHandle(risk_free_ts),
        ql.BlackVolTermStructureHandle(vol_ts),
    )

    payoff = ql.PlainVanillaPayoff(ql.OptionType.Call, 100.0)
    exercise_date = today + ql.Period(1, ql.Years)
    exercise = ql.EuropeanExercise(exercise_date)
    option = ql.VanillaOption(payoff, exercise)

    return {"option": option, "process": process}


def test_mc_european_pseudorandom(mc_env):
    """Test MCEuropeanEngine with pseudorandom RNG."""
    engine = ql.MCEuropeanEngine(
        process=mc_env["process"],
        rngType="pseudorandom",
        timeSteps=10,
        requiredSamples=1000,
        seed=42,
    )

    assert engine is not None


def test_mc_european_lowdiscrepancy(mc_env):
    """Test MCEuropeanEngine with low discrepancy RNG."""
    engine = ql.MCEuropeanEngine(
        process=mc_env["process"],
        rngType="lowdiscrepancy",
        timeSteps=10,
        requiredSamples=1000,
    )

    assert engine is not None


def test_mc_european_pricing(mc_env):
    """Test MC engine produces reasonable prices."""
    option = mc_env["option"]

    engine = ql.MCEuropeanEngine(
        process=mc_env["process"],
        rngType="pseudorandom",
        timeSteps=52,
        requiredSamples=10000,
        seed=12345,
    )

    option.setPricingEngine(engine)
    npv = option.NPV()

    expected_npv = 9.687424197269415
    assert npv == pytest.approx(expected_npv, abs=1e-4)


def test_mc_european_lowdiscrepancy_pricing(mc_env):
    """Test low discrepancy MC pricing."""
    option = mc_env["option"]

    engine = ql.MCEuropeanEngine(
        process=mc_env["process"],
        rngType="lowdiscrepancy",
        timeSteps=1,
        requiredSamples=10000,
        seed=12345,
    )

    option.setPricingEngine(engine)
    npv = option.NPV()

    expected_npv = 9.818793862668565
    assert npv == pytest.approx(expected_npv, abs=1e-4)


def test_mc_european_antithetic(mc_env):
    """Test MC engine with antithetic variates."""
    option = mc_env["option"]

    engine = ql.MCEuropeanEngine(
        process=mc_env["process"],
        rngType="pseudorandom",
        timeSteps=10,
        antitheticVariate=True,
        requiredSamples=5000,
        maxSamples=100000,
        seed=8675309,
    )

    option.setPricingEngine(engine)
    npv = option.NPV()

    expected_npv = 9.8862132025707
    assert npv == pytest.approx(expected_npv, abs=1e-2)


def test_mc_european_invalid_rng(mc_env):
    """Test error handling for invalid RNG type."""
    with pytest.raises(RuntimeError, match="Unsupported RNG type"):
        ql.MCEuropeanEngine(
            mc_env["process"], "invalid_rng", timeSteps=10, requiredSamples=1000
        )


def test_mc_european_seed_reproducibility(mc_env):
    """Test same seed produces reproducible results."""
    engine1 = ql.MCEuropeanEngine(
        mc_env["process"], "pseudorandom", timeSteps=10, requiredSamples=1000, seed=42
    )
    engine2 = ql.MCEuropeanEngine(
        mc_env["process"], "pseudorandom", timeSteps=10, requiredSamples=1000, seed=42
    )

    payoff = ql.PlainVanillaPayoff(ql.OptionType.Call, 100.0)
    exercise = mc_env["option"].exercise()

    option1 = ql.VanillaOption(payoff, exercise)
    option2 = ql.VanillaOption(payoff, exercise)

    option1.setPricingEngine(engine1)
    option2.setPricingEngine(engine2)

    assert option1.NPV() == pytest.approx(option2.NPV(), abs=1e-10)


# =============================================================================
# QdFpAmericanEngine
# =============================================================================


def test_qdfp_construction(american_env):
    """Test QdFpAmericanEngine construction."""
    engine = ql.QdFpAmericanEngine(american_env["process"])
    assert engine is not None


@pytest.mark.skip(reason="Access violation on Windows during calculate()")
def test_qdfp_pricing(american_env):
    """Test QdFpAmericanEngine pricing with default scheme."""
    engine = ql.QdFpAmericanEngine(american_env["process"])
    american_env["option"].setPricingEngine(engine)
    npv = american_env["option"].NPV()
    assert 4.0 < npv < 5.5


@pytest.mark.skip(reason="Access violation on Windows during calculate()")
def test_qdfp_fast_scheme(american_env):
    """Test QdFpAmericanEngine with fast scheme."""
    scheme = ql.QdFpAmericanEngine.fastScheme()
    engine = ql.QdFpAmericanEngine(
        american_env["process"],
        scheme,
    )
    american_env["option"].setPricingEngine(engine)
    npv = american_env["option"].NPV()
    assert npv == pytest.approx(4.486, abs=0.1)


@pytest.mark.skip(reason="Access violation on Windows during calculate()")
def test_qdfp_accurate_scheme(american_env):
    """Test QdFpAmericanEngine with accurate scheme."""
    scheme = ql.QdFpAmericanEngine.accurateScheme()
    engine = ql.QdFpAmericanEngine(
        american_env["process"],
        scheme,
    )
    american_env["option"].setPricingEngine(engine)
    npv = american_env["option"].NPV()
    assert npv == pytest.approx(4.486, abs=0.1)


@pytest.mark.skip(reason="Access violation on Windows during calculate()")
def test_qdfp_high_precision_scheme(american_env):
    """Test QdFpAmericanEngine with high precision scheme."""
    scheme = ql.QdFpAmericanEngine.highPrecisionScheme()
    engine = ql.QdFpAmericanEngine(
        american_env["process"],
        scheme,
    )
    american_env["option"].setPricingEngine(engine)
    npv = american_env["option"].NPV()
    assert npv == pytest.approx(4.486, abs=0.01)


def test_qdfp_scheme_factories():
    """Test QdFpAmericanEngine scheme factory methods exist."""
    assert ql.QdFpAmericanEngine.fastScheme() is not None
    assert ql.QdFpAmericanEngine.accurateScheme() is not None
    assert ql.QdFpAmericanEngine.highPrecisionScheme() is not None


def test_qdfp_fixed_point_equation_enum():
    """Test QdFpFixedPointEquation enum values."""
    assert ql.QdFpFixedPointEquation.FP_A is not None
    assert ql.QdFpFixedPointEquation.FP_B is not None
    assert ql.QdFpFixedPointEquation.Auto is not None


# =============================================================================
# AnalyticBlackVasicekEngine
# =============================================================================


def test_analytic_vasicek_construction(european_env):
    """Test AnalyticBlackVasicekEngine construction."""
    vasicek = ql.Vasicek(r0=0.06, a=0.3, b=0.06, sigma=0.01)
    engine = ql.AnalyticBlackVasicekEngine(
        european_env["process"],
        vasicek,
        correlation=0.5,
    )
    assert engine is not None


def test_analytic_vasicek_pricing(european_env):
    """Test AnalyticBlackVasicekEngine produces reasonable price."""
    option = european_env["option"]
    vasicek = ql.Vasicek(r0=0.06, a=0.3, b=0.06, sigma=0.01)
    engine = ql.AnalyticBlackVasicekEngine(
        european_env["process"],
        vasicek,
        correlation=0.5,
    )
    option.setPricingEngine(engine)

    npv = option.NPV()
    assert npv == pytest.approx(3.87770155721401, rel=1e-5)


# =============================================================================
# AnalyticHestonEngine
# =============================================================================


@pytest.fixture
def heston_env():
    """Standard Heston market environment."""
    today = ql.Date(20, 2, 2025)
    ql.Settings.instance().evaluationDate = today

    dc = ql.Actual365Fixed()

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


# =============================================================================
# BatesEngine
# =============================================================================


@pytest.fixture
def bates_env():
    """Market environment for Bates engine tests."""
    today = ql.Date(15, ql.May, 1998)
    settlement = ql.Date(17, ql.May, 1998)
    ql.Settings.instance().evaluationDate = today

    dc = ql.Actual365Fixed()

    spot = ql.SimpleQuote(36.0)
    risk_free_ts = ql.FlatForward(settlement, 0.06, dc)
    dividend_ts = ql.FlatForward(settlement, 0.00, dc)

    # Bates process parameters
    v0 = 0.04
    kappa = 1.0
    theta = 0.04
    sigma = 0.3
    rho = -0.5
    lambda_ = 0.1
    nu = -0.05
    delta = 0.1

    process = ql.BatesProcess(
        ql.YieldTermStructureHandle(risk_free_ts),
        ql.YieldTermStructureHandle(dividend_ts),
        ql.QuoteHandle(spot),
        v0, kappa, theta, sigma, rho,
        lambda_, nu, delta,
    )

    model = ql.BatesModel(process)

    # European put option
    payoff = ql.PlainVanillaPayoff(ql.OptionType.Put, 40.0)
    maturity = ql.Date(17, ql.May, 1999)
    exercise = ql.EuropeanExercise(maturity)
    option = ql.VanillaOption(payoff, exercise)

    return {"option": option, "model": model, "process": process}


def test_bates_model_construction(bates_env):
    """Test BatesModel construction."""
    assert bates_env["model"] is not None


def test_bates_model_parameters(bates_env):
    """Test BatesModel parameter accessors."""
    model = bates_env["model"]

    assert model.nu() == pytest.approx(-0.05)
    assert model.delta() == pytest.approx(0.1)
    assert model.lambda_() == pytest.approx(0.1)


def test_bates_engine_construction(bates_env):
    """Test BatesEngine construction."""
    engine = ql.BatesEngine(bates_env["model"])
    assert engine is not None


def test_bates_engine_with_integration_order(bates_env):
    """Test BatesEngine construction with integration order."""
    engine = ql.BatesEngine(bates_env["model"], 144)
    assert engine is not None


def test_bates_engine_pricing(bates_env):
    """Test BatesEngine produces reasonable price."""
    option = bates_env["option"]
    engine = ql.BatesEngine(bates_env["model"])
    option.setPricingEngine(engine)

    npv = option.NPV()
    assert npv == pytest.approx(3.6379571568095876, rel=1e-5)


# =============================================================================
# FdHestonVanillaEngine
# =============================================================================


@pytest.fixture
def fd_heston_env():
    """Market environment for FD Heston engine tests."""
    import datetime

    today = datetime.date(2024, 1, 15)
    ql.Settings.evaluationDate = today
    maturity = datetime.date(2025, 1, 15)

    dc = ql.Actual365Fixed()
    spot = ql.SimpleQuote(100.0)
    risk_free_ts = ql.FlatForward(today, ql.SimpleQuote(0.05), dc)
    div_ts = ql.FlatForward(today, ql.SimpleQuote(0.02), dc)

    process = ql.HestonProcess(
        risk_free_ts, div_ts, spot,
        0.04, 1.5, 0.04, 0.3, -0.7,
    )
    model = ql.HestonModel(process)

    call_payoff = ql.PlainVanillaPayoff(ql.OptionType.Call, 100.0)
    put_payoff = ql.PlainVanillaPayoff(ql.OptionType.Put, 100.0)
    euro_exercise = ql.EuropeanExercise(maturity)
    amer_exercise = ql.AmericanExercise(today, maturity)

    return {
        "model": model,
        "call_payoff": call_payoff,
        "put_payoff": put_payoff,
        "euro_exercise": euro_exercise,
        "amer_exercise": amer_exercise,
    }


def test_fdhestonvanilla_construction(fd_heston_env):
    """Test FdHestonVanillaEngine construction."""
    engine = ql.FdHestonVanillaEngine(fd_heston_env["model"])
    assert engine is not None


def test_fdhestonvanilla_european_call(fd_heston_env):
    """Test FD Heston European call pricing."""
    env = fd_heston_env
    option = ql.VanillaOption(env["call_payoff"], env["euro_exercise"])
    engine = ql.FdHestonVanillaEngine(env["model"], tGrid=100, xGrid=100, vGrid=50)
    option.setPricingEngine(engine)
    assert option.NPV() == pytest.approx(9.028582, rel=1e-4)


def test_fdhestonvanilla_american_put(fd_heston_env):
    """Test FD Heston American put pricing."""
    env = fd_heston_env
    option = ql.VanillaOption(env["put_payoff"], env["amer_exercise"])
    engine = ql.FdHestonVanillaEngine(env["model"], tGrid=100, xGrid=100, vGrid=50)
    option.setPricingEngine(engine)
    assert option.NPV() == pytest.approx(6.448334, rel=1e-4)


def test_fdhestonvanilla_multiple_strikes_caching(fd_heston_env):
    """Test enableMultipleStrikesCaching method."""
    env = fd_heston_env
    engine = ql.FdHestonVanillaEngine(env["model"], tGrid=50, xGrid=50, vGrid=25)
    engine.enableMultipleStrikesCaching([90.0, 100.0, 110.0])

    option = ql.VanillaOption(env["call_payoff"], env["euro_exercise"])
    option.setPricingEngine(engine)
    assert option.NPV() == pytest.approx(9.046529, rel=1e-4)


def test_make_fdhestonvanilla_builder(fd_heston_env):
    """Test MakeFdHestonVanillaEngine Python wrapper."""
    env = fd_heston_env
    engine = ql.MakeFdHestonVanillaEngine(
        env["model"], tGrid=50, xGrid=50, vGrid=25,
    )
    option = ql.VanillaOption(env["call_payoff"], env["euro_exercise"])
    option.setPricingEngine(engine)
    assert option.NPV() == pytest.approx(9.040718, rel=1e-4)


# =============================================================================
# FdBatesVanillaEngine
# =============================================================================


@pytest.fixture
def fd_bates_env():
    """Market environment for FD Bates engine tests."""
    import datetime

    today = datetime.date(2024, 1, 15)
    ql.Settings.evaluationDate = today
    maturity = datetime.date(2025, 1, 15)

    dc = ql.Actual365Fixed()
    spot = ql.SimpleQuote(100.0)
    risk_free_ts = ql.FlatForward(today, ql.SimpleQuote(0.05), dc)
    div_ts = ql.FlatForward(today, ql.SimpleQuote(0.02), dc)

    process = ql.BatesProcess(
        risk_free_ts, div_ts, spot,
        0.04, 1.5, 0.04, 0.3, -0.7,
        0.1, -0.5, 0.1,
    )
    model = ql.BatesModel(process)

    call_payoff = ql.PlainVanillaPayoff(ql.OptionType.Call, 100.0)
    euro_exercise = ql.EuropeanExercise(maturity)

    return {
        "model": model,
        "call_payoff": call_payoff,
        "euro_exercise": euro_exercise,
    }


def test_fdbatesvanilla_construction(fd_bates_env):
    """Test FdBatesVanillaEngine construction."""
    engine = ql.FdBatesVanillaEngine(fd_bates_env["model"])
    assert engine is not None


def test_fdbatesvanilla_european_call(fd_bates_env):
    """Test FD Bates European call pricing."""
    env = fd_bates_env
    option = ql.VanillaOption(env["call_payoff"], env["euro_exercise"])
    engine = ql.FdBatesVanillaEngine(env["model"], tGrid=100, xGrid=100, vGrid=50)
    option.setPricingEngine(engine)
    assert option.NPV() == pytest.approx(10.646633, rel=1e-4)


# =============================================================================
# FdSabrVanillaEngine
# =============================================================================


def test_fdsabrvanilla_construction():
    """Test FdSabrVanillaEngine construction."""
    import datetime

    today = datetime.date(2024, 1, 15)
    ql.Settings.evaluationDate = today

    dc = ql.Actual365Fixed()
    rts = ql.FlatForward(today, ql.SimpleQuote(0.05), dc)

    engine = ql.FdSabrVanillaEngine(100.0, 0.3, 0.5, 0.4, -0.3, rts)
    assert engine is not None


def test_fdsabrvanilla_european_call():
    """Test FD SABR European call pricing."""
    import datetime

    today = datetime.date(2024, 1, 15)
    ql.Settings.evaluationDate = today
    maturity = datetime.date(2025, 1, 15)

    dc = ql.Actual365Fixed()
    rts = ql.FlatForward(today, ql.SimpleQuote(0.05), dc)

    payoff = ql.PlainVanillaPayoff(ql.OptionType.Call, 100.0)
    exercise = ql.EuropeanExercise(maturity)
    option = ql.VanillaOption(payoff, exercise)

    engine = ql.FdSabrVanillaEngine(
        100.0, 0.3, 0.5, 0.4, -0.3, rts,
        tGrid=50, fGrid=400, xGrid=50,
    )
    option.setPricingEngine(engine)
    assert option.NPV() == pytest.approx(1.152418, rel=1e-4)


# =============================================================================
# FdCEVVanillaEngine
# =============================================================================


def test_fdcevvanilla_construction():
    """Test FdCEVVanillaEngine construction."""
    import datetime

    today = datetime.date(2024, 1, 15)
    ql.Settings.evaluationDate = today

    dc = ql.Actual365Fixed()
    rts = ql.FlatForward(today, ql.SimpleQuote(0.05), dc)

    engine = ql.FdCEVVanillaEngine(100.0, 0.3, 0.5, rts)
    assert engine is not None


def test_fdcevvanilla_european_call():
    """Test FD CEV European call pricing."""
    import datetime

    today = datetime.date(2024, 1, 15)
    ql.Settings.evaluationDate = today
    maturity = datetime.date(2025, 1, 15)

    dc = ql.Actual365Fixed()
    rts = ql.FlatForward(today, ql.SimpleQuote(0.05), dc)

    payoff = ql.PlainVanillaPayoff(ql.OptionType.Call, 100.0)
    exercise = ql.EuropeanExercise(maturity)
    option = ql.VanillaOption(payoff, exercise)

    engine = ql.FdCEVVanillaEngine(100.0, 0.3, 0.5, rts, tGrid=50, xGrid=400)
    option.setPricingEngine(engine)
    assert option.NPV() == pytest.approx(1.141919, rel=1e-4)


# =============================================================================
# FdBlackScholesShoutEngine
# =============================================================================


def test_fdblackscholesshout_construction():
    """Test FdBlackScholesShoutEngine construction."""
    import datetime

    today = datetime.date(2024, 1, 15)
    ql.Settings.evaluationDate = today

    dc = ql.Actual365Fixed()
    spot = ql.SimpleQuote(100.0)
    rts = ql.FlatForward(today, ql.SimpleQuote(0.05), dc)
    dts = ql.FlatForward(today, ql.SimpleQuote(0.02), dc)
    vol = ql.BlackConstantVol(today, ql.NullCalendar(), ql.SimpleQuote(0.20), dc)
    process = ql.GeneralizedBlackScholesProcess(spot, dts, rts, vol)

    engine = ql.FdBlackScholesShoutEngine(process)
    assert engine is not None


def test_fdblackscholesshout_european_call():
    """Test FD Black-Scholes shout option pricing."""
    import datetime

    today = datetime.date(2024, 1, 15)
    ql.Settings.evaluationDate = today
    maturity = datetime.date(2025, 1, 15)

    dc = ql.Actual365Fixed()
    spot = ql.SimpleQuote(100.0)
    rts = ql.FlatForward(today, ql.SimpleQuote(0.05), dc)
    dts = ql.FlatForward(today, ql.SimpleQuote(0.02), dc)
    vol = ql.BlackConstantVol(today, ql.NullCalendar(), ql.SimpleQuote(0.20), dc)
    process = ql.GeneralizedBlackScholesProcess(spot, dts, rts, vol)

    payoff = ql.PlainVanillaPayoff(ql.OptionType.Call, 100.0)
    exercise = ql.EuropeanExercise(maturity)
    option = ql.VanillaOption(payoff, exercise)

    engine = ql.FdBlackScholesShoutEngine(process, tGrid=100, xGrid=100)
    option.setPricingEngine(engine)
    assert option.NPV() == pytest.approx(9.239281, rel=1e-4)


# =============================================================================
# COSHestonEngine
# =============================================================================


def test_coshestonengine_construction(fd_heston_env):
    """Test COSHestonEngine construction."""
    engine = ql.COSHestonEngine(fd_heston_env["model"])
    assert engine is not None


def test_coshestonengine_pricing(fd_heston_env):
    """Test COS Heston European call pricing."""
    env = fd_heston_env
    option = ql.VanillaOption(env["call_payoff"], env["euro_exercise"])
    option.setPricingEngine(ql.COSHestonEngine(env["model"]))
    assert option.NPV() == pytest.approx(9.024861, rel=1e-4)


def test_coshestonengine_moments(fd_heston_env):
    """Test COS Heston cumulant accessors."""
    engine = ql.COSHestonEngine(fd_heston_env["model"])
    assert engine.c1(1.0) == pytest.approx(-0.020000, abs=1e-5)
    assert engine.c2(1.0) == pytest.approx(0.042812, rel=1e-4)


# =============================================================================
# ExponentialFittingHestonEngine
# =============================================================================


def test_exponentialfittingheston_construction(fd_heston_env):
    """Test ExponentialFittingHestonEngine construction."""
    engine = ql.ExponentialFittingHestonEngine(fd_heston_env["model"])
    assert engine is not None


def test_exponentialfittingheston_pricing(fd_heston_env):
    """Test exponential fitting Heston European call pricing."""
    env = fd_heston_env
    option = ql.VanillaOption(env["call_payoff"], env["euro_exercise"])
    option.setPricingEngine(ql.ExponentialFittingHestonEngine(env["model"]))
    assert option.NPV() == pytest.approx(9.024861, rel=1e-4)


# =============================================================================
# AnalyticPTDHestonEngine
# =============================================================================


def test_analyticptdheston_pricing():
    """Test piecewise time-dependent Heston pricing."""
    import datetime

    today = datetime.date(2024, 1, 15)
    ql.Settings.evaluationDate = today
    maturity = datetime.date(2025, 1, 15)
    dc = ql.Actual365Fixed()

    spot = ql.SimpleQuote(100.0)
    rts = ql.FlatForward(today, ql.SimpleQuote(0.05), dc)
    dts = ql.FlatForward(today, ql.SimpleQuote(0.02), dc)

    noC = ql.NoConstraint()
    tg = ql.TimeGrid(2.0, 10)
    ptd_model = ql.PiecewiseTimeDependentHestonModel(
        ql.YieldTermStructureHandle(rts),
        ql.YieldTermStructureHandle(dts),
        ql.QuoteHandle(spot), 0.04,
        ql.ConstantParameter(0.04, noC),
        ql.ConstantParameter(1.5, noC),
        ql.ConstantParameter(0.3, noC),
        ql.ConstantParameter(-0.7, noC), tg,
    )

    payoff = ql.PlainVanillaPayoff(ql.OptionType.Call, 100.0)
    exercise = ql.EuropeanExercise(maturity)
    option = ql.VanillaOption(payoff, exercise)
    option.setPricingEngine(ql.AnalyticPTDHestonEngine(ptd_model))
    assert option.NPV() == pytest.approx(9.024861, rel=1e-4)


# =============================================================================
# AnalyticPDFHestonEngine
# =============================================================================


def test_analyticpdfheston_construction(fd_heston_env):
    """Test AnalyticPDFHestonEngine construction."""
    engine = ql.AnalyticPDFHestonEngine(fd_heston_env["model"])
    assert engine is not None


def test_analyticpdfheston_pricing(fd_heston_env):
    """Test PDF-based Heston pricing."""
    env = fd_heston_env
    option = ql.VanillaOption(env["call_payoff"], env["euro_exercise"])
    option.setPricingEngine(ql.AnalyticPDFHestonEngine(env["model"]))
    assert option.NPV() == pytest.approx(9.024861, rel=1e-4)


# =============================================================================
# AnalyticHestonHullWhiteEngine
# =============================================================================


def test_analytichestonhw_pricing(fd_heston_env):
    """Test Heston + Hull-White stochastic rates pricing."""
    import datetime

    today = datetime.date(2024, 1, 15)
    ql.Settings.evaluationDate = today
    maturity = datetime.date(2025, 1, 15)
    dc = ql.Actual365Fixed()
    rts = ql.FlatForward(today, ql.SimpleQuote(0.05), dc)

    hw = ql.HullWhite(rts, a=0.1, sigma=0.01)

    env = fd_heston_env
    option = ql.VanillaOption(env["call_payoff"], env["euro_exercise"])
    option.setPricingEngine(ql.AnalyticHestonHullWhiteEngine(env["model"], hw))
    assert option.NPV() == pytest.approx(9.027719, rel=1e-4)


# =============================================================================
# AnalyticH1HWEngine
# =============================================================================


def test_analytich1hw_pricing(fd_heston_env):
    """Test H1-HW approximation with equity-rate correlation."""
    import datetime

    today = datetime.date(2024, 1, 15)
    ql.Settings.evaluationDate = today
    maturity = datetime.date(2025, 1, 15)
    dc = ql.Actual365Fixed()
    rts = ql.FlatForward(today, ql.SimpleQuote(0.05), dc)

    hw = ql.HullWhite(rts, a=0.1, sigma=0.01)

    env = fd_heston_env
    option = ql.VanillaOption(env["call_payoff"], env["euro_exercise"])
    option.setPricingEngine(ql.AnalyticH1HWEngine(env["model"], hw, rhoSr=0.3))
    assert option.NPV() == pytest.approx(9.078273, rel=1e-4)


# =============================================================================
# HestonExpansionEngine
# =============================================================================


def test_hestonexpansion_lpp2(fd_heston_env):
    """Test Heston expansion engine with LPP2 formula."""
    env = fd_heston_env
    option = ql.VanillaOption(env["call_payoff"], env["euro_exercise"])
    option.setPricingEngine(
        ql.HestonExpansionEngine(env["model"], ql.HestonExpansionFormula.LPP2))
    assert option.NPV() == pytest.approx(9.013539, rel=1e-3)


def test_hestonexpansion_lpp3(fd_heston_env):
    """Test Heston expansion engine with LPP3 formula."""
    env = fd_heston_env
    option = ql.VanillaOption(env["call_payoff"], env["euro_exercise"])
    option.setPricingEngine(
        ql.HestonExpansionEngine(env["model"], ql.HestonExpansionFormula.LPP3))
    assert option.NPV() == pytest.approx(9.023003, rel=1e-3)


# =============================================================================
# JuQuadraticApproximationEngine
# =============================================================================


@pytest.fixture(scope="module")
def bsm_american_env():
    """Common BSM setup for American option engines."""
    import datetime

    ql.Settings.evaluationDate = datetime.date(2024, 1, 15)
    spot = ql.SimpleQuote(100.0)
    rf = ql.FlatForward(datetime.date(2024, 1, 15), 0.05, ql.Actual365Fixed())
    dy = ql.FlatForward(datetime.date(2024, 1, 15), 0.02, ql.Actual365Fixed())
    vol = ql.BlackConstantVol(
        datetime.date(2024, 1, 15), ql.NullCalendar(), 0.20, ql.Actual365Fixed()
    )
    process = ql.BlackScholesMertonProcess(
        ql.QuoteHandle(spot),
        ql.YieldTermStructureHandle(dy),
        ql.YieldTermStructureHandle(rf),
        ql.BlackVolTermStructureHandle(vol),
    )
    exercise = ql.AmericanExercise(
        datetime.date(2024, 1, 15), datetime.date(2025, 1, 15)
    )
    put_payoff = ql.PlainVanillaPayoff(ql.OptionType.Put, 100.0)
    call_payoff = ql.PlainVanillaPayoff(ql.OptionType.Call, 100.0)
    euro_exercise = ql.EuropeanExercise(datetime.date(2025, 1, 15))
    return {
        "process": process,
        "exercise": exercise,
        "put_payoff": put_payoff,
        "call_payoff": call_payoff,
        "euro_exercise": euro_exercise,
        "rf": rf,
    }


def test_juquadratic_put(bsm_american_env):
    """Test Ju quadratic approximation for American put."""
    env = bsm_american_env
    option = ql.VanillaOption(env["put_payoff"], env["exercise"])
    option.setPricingEngine(ql.JuQuadraticApproximationEngine(env["process"]))
    assert option.NPV() == pytest.approx(6.6449563746, rel=1e-4)


# =============================================================================
# QdPlusAmericanEngine
# =============================================================================


def test_qdplus_put_default(bsm_american_env):
    """Test QD+ American engine with default Halley solver."""
    env = bsm_american_env
    option = ql.VanillaOption(env["put_payoff"], env["exercise"])
    option.setPricingEngine(ql.QdPlusAmericanEngine(env["process"]))
    assert option.NPV() == pytest.approx(6.6755387218, rel=1e-4)


def test_qdplus_solver_types(bsm_american_env):
    """Test QD+ American engine with different solver types."""
    env = bsm_american_env
    option = ql.VanillaOption(env["put_payoff"], env["exercise"])
    for solver in [
        ql.QdPlusAmericanEngineSolverType.Brent,
        ql.QdPlusAmericanEngineSolverType.Newton,
        ql.QdPlusAmericanEngineSolverType.Ridder,
    ]:
        option.setPricingEngine(
            ql.QdPlusAmericanEngine(env["process"], solverType=solver)
        )
        assert option.NPV() == pytest.approx(6.6755387218, rel=1e-3)


# =============================================================================
# AnalyticDigitalAmericanEngine
# =============================================================================


def test_digital_american_ki(bsm_american_env):
    """Test analytic digital American engine (knock-in)."""
    env = bsm_american_env
    payoff = ql.CashOrNothingPayoff(ql.OptionType.Call, 110.0, 10.0)
    option = ql.VanillaOption(payoff, env["exercise"])
    option.setPricingEngine(ql.AnalyticDigitalAmericanEngine(env["process"]))
    assert option.NPV() == pytest.approx(6.3928324784, rel=1e-4)


def test_digital_american_ko(bsm_american_env):
    """Test analytic digital American engine (knock-out)."""
    env = bsm_american_env
    payoff = ql.CashOrNothingPayoff(ql.OptionType.Call, 110.0, 10.0)
    option = ql.VanillaOption(payoff, env["exercise"])
    option.setPricingEngine(ql.AnalyticDigitalAmericanKOEngine(env["process"]))
    assert option.NPV() == pytest.approx(6.3928324784, rel=1e-4)


# =============================================================================
# MCDigitalEngine
# =============================================================================


def test_mcdigital_pseudorandom(bsm_american_env):
    """Test MC digital engine with pseudo-random RNG."""
    env = bsm_american_env
    payoff = ql.CashOrNothingPayoff(ql.OptionType.Call, 110.0, 10.0)
    option = ql.VanillaOption(payoff, env["exercise"])
    engine = ql.MCDigitalEngine(
        env["process"], rngType="pseudorandom",
        timeSteps=100, requiredSamples=50000, seed=42,
    )
    option.setPricingEngine(engine)
    assert option.NPV() == pytest.approx(6.3728859335, rel=1e-4)


def test_mcdigital_lowdiscrepancy(bsm_american_env):
    """Test MC digital engine with low-discrepancy RNG."""
    env = bsm_american_env
    payoff = ql.CashOrNothingPayoff(ql.OptionType.Call, 110.0, 10.0)
    option = ql.VanillaOption(payoff, env["exercise"])
    engine = ql.MCDigitalEngine(
        env["process"], rngType="lowdiscrepancy",
        timeSteps=100, requiredSamples=50000, seed=42,
    )
    option.setPricingEngine(engine)
    assert option.NPV() == pytest.approx(6.3894913325, rel=1e-4)


# =============================================================================
# AnalyticDividendEuropeanEngine
# =============================================================================


def test_dividend_european(bsm_american_env):
    """Test European engine with discrete dividends."""
    import datetime

    env = bsm_american_env
    payoff = ql.PlainVanillaPayoff(ql.OptionType.Call, 100.0)
    exercise = ql.EuropeanExercise(datetime.date(2025, 1, 15))
    dividends = [ql.FixedDividend(2.0, datetime.date(2024, 7, 15))]
    engine = ql.AnalyticDividendEuropeanEngine(env["process"], dividends)
    option = ql.VanillaOption(payoff, exercise)
    option.setPricingEngine(engine)
    assert option.NPV() == pytest.approx(8.1217220283, rel=1e-4)


# =============================================================================
# AnalyticBSMHullWhiteEngine
# =============================================================================


def test_bsm_hullwhite(bsm_american_env):
    """Test BSM + Hull-White stochastic rates engine."""
    env = bsm_american_env
    hw = ql.HullWhite(ql.YieldTermStructureHandle(env["rf"]), 0.1, 0.01)
    engine = ql.AnalyticBSMHullWhiteEngine(0.3, env["process"], hw)
    option = ql.VanillaOption(env["call_payoff"], env["euro_exercise"])
    option.setPricingEngine(engine)
    assert option.NPV() == pytest.approx(9.2988899168, rel=1e-4)


# =============================================================================
# AnalyticGJRGARCHEngine
# =============================================================================


def test_gjrgarch_engine_construction():
    """Test AnalyticGJRGARCHEngine construction."""
    import datetime

    today = datetime.date(2024, 1, 15)
    ql.Settings.evaluationDate = today

    dc = ql.Actual365Fixed()
    spot = ql.SimpleQuote(100.0)
    rts = ql.FlatForward(today, ql.SimpleQuote(0.05), dc)
    dts = ql.FlatForward(today, ql.SimpleQuote(0.02), dc)

    process = ql.GJRGARCHProcess(
        rts, dts, spot,
        v0=0.04 / 252.0, omega=2e-6, alpha=0.04,
        beta=0.94, gamma=0.02, lambda_=0.0, daysPerYear=252.0,
    )
    model = ql.GJRGARCHModel(process)
    engine = ql.AnalyticGJRGARCHEngine(model)
    assert engine is not None


def test_gjrgarch_engine_pricing():
    """Test GJR-GARCH engine produces reasonable price."""
    import datetime

    today = datetime.date(2024, 1, 15)
    ql.Settings.evaluationDate = today
    maturity = datetime.date(2025, 1, 15)

    dc = ql.Actual365Fixed()
    spot = ql.SimpleQuote(100.0)
    rts = ql.FlatForward(today, ql.SimpleQuote(0.05), dc)
    dts = ql.FlatForward(today, ql.SimpleQuote(0.02), dc)

    process = ql.GJRGARCHProcess(
        rts, dts, spot,
        v0=0.04 / 252.0, omega=2e-6, alpha=0.04,
        beta=0.94, gamma=0.02, lambda_=0.0, daysPerYear=252.0,
    )
    model = ql.GJRGARCHModel(process)

    payoff = ql.PlainVanillaPayoff(ql.OptionType.Call, 100.0)
    exercise = ql.EuropeanExercise(maturity)
    option = ql.VanillaOption(payoff, exercise)

    option.setPricingEngine(ql.AnalyticGJRGARCHEngine(model))
    assert option.NPV() == pytest.approx(9.8903, rel=1e-4)


# =============================================================================
# FdHestonHullWhiteVanillaEngine
# =============================================================================


def test_fdhestonhullwhitevanillaengine_pricing():
    """FdHestonHullWhiteVanillaEngine prices European option."""
    today = ql.Date(15, 1, 2026)
    ql.Settings.instance().evaluationDate = today
    dc = ql.Actual365Fixed()
    maturity = ql.Date(15, 1, 2027)

    spot = ql.SimpleQuote(100.0)
    rts = ql.FlatForward(today, 0.05, dc)
    dts = ql.FlatForward(today, 0.02, dc)

    heston_process = ql.HestonProcess(
        rts, dts, spot, v0=0.04, kappa=1.0, theta=0.04, sigma=0.5, rho=-0.7,
    )
    heston_model = ql.HestonModel(heston_process)
    hw_process = ql.HullWhiteProcess(rts, a=0.1, sigma=0.01)

    payoff = ql.PlainVanillaPayoff(ql.OptionType.Call, 100.0)
    exercise = ql.EuropeanExercise(maturity)
    option = ql.VanillaOption(payoff, exercise)

    engine = ql.FdHestonHullWhiteVanillaEngine(
        heston_model, hw_process, corrEquityShortRate=0.3,
        tGrid=25, xGrid=50, vGrid=20, rGrid=10,
    )
    option.setPricingEngine(engine)
    npv = option.NPV()
    assert npv == pytest.approx(8.5065, rel=1e-2)


# =============================================================================
# FdOrnsteinUhlenbeckVanillaEngine
# =============================================================================


def test_fdornsteinuhlenbeckvanillaengine_pricing():
    """FdOrnsteinUhlenbeckVanillaEngine prices European option on OU process."""
    today = ql.Date(15, 1, 2026)
    ql.Settings.instance().evaluationDate = today
    dc = ql.Actual365Fixed()
    maturity = ql.Date(15, 1, 2027)

    ou_process = ql.OrnsteinUhlenbeckProcess(
        speed=1.0, volatility=0.2, x0=100.0, level=100.0,
    )
    rts = ql.FlatForward(today, 0.05, dc)

    payoff = ql.PlainVanillaPayoff(ql.OptionType.Call, 100.0)
    exercise = ql.EuropeanExercise(maturity)
    option = ql.VanillaOption(payoff, exercise)

    engine = ql.FdOrnsteinUhlenbeckVanillaEngine(
        ou_process, rts, tGrid=50, xGrid=100,
    )
    option.setPricingEngine(engine)
    npv = option.NPV()
    assert npv > 0.0  # OU model, no exact BS comparison available
    assert isinstance(npv, float)


# =============================================================================
# MCEuropeanHestonEngine
# =============================================================================


def test_mceuropeanhestonengine_pseudorandom():
    """MCEuropeanHestonEngine with pseudo-random sampling."""
    today = ql.Date(15, 1, 2026)
    ql.Settings.instance().evaluationDate = today
    dc = ql.Actual365Fixed()
    maturity = ql.Date(15, 1, 2027)

    spot = ql.SimpleQuote(100.0)
    rts = ql.FlatForward(today, 0.05, dc)
    dts = ql.FlatForward(today, 0.02, dc)

    process = ql.HestonProcess(
        rts, dts, spot, v0=0.04, kappa=1.0, theta=0.04, sigma=0.5, rho=-0.7,
    )

    payoff = ql.PlainVanillaPayoff(ql.OptionType.Call, 100.0)
    exercise = ql.EuropeanExercise(maturity)
    option = ql.VanillaOption(payoff, exercise)

    engine = ql.MCEuropeanHestonEngine(
        process, rngType="pseudorandom",
        timeSteps=50, requiredSamples=10000, seed=42,
    )
    option.setPricingEngine(engine)

    # Compare against analytic Heston
    model = ql.HestonModel(process)
    option2 = ql.VanillaOption(payoff, exercise)
    option2.setPricingEngine(ql.AnalyticHestonEngine(model))
    analytic_npv = option2.NPV()

    assert option.NPV() == pytest.approx(analytic_npv, rel=0.05)


def test_mceuropeanhestonengine_lowdiscrepancy():
    """MCEuropeanHestonEngine with low-discrepancy sampling."""
    today = ql.Date(15, 1, 2026)
    ql.Settings.instance().evaluationDate = today
    dc = ql.Actual365Fixed()
    maturity = ql.Date(15, 1, 2027)

    spot = ql.SimpleQuote(100.0)
    rts = ql.FlatForward(today, 0.05, dc)
    dts = ql.FlatForward(today, 0.02, dc)

    process = ql.HestonProcess(
        rts, dts, spot, v0=0.04, kappa=1.0, theta=0.04, sigma=0.5, rho=-0.7,
    )

    payoff = ql.PlainVanillaPayoff(ql.OptionType.Call, 100.0)
    exercise = ql.EuropeanExercise(maturity)
    option = ql.VanillaOption(payoff, exercise)

    engine = ql.MCEuropeanHestonEngine(
        process, rngType="lowdiscrepancy",
        timeSteps=50, requiredSamples=8191,
    )
    option.setPricingEngine(engine)

    model = ql.HestonModel(process)
    option2 = ql.VanillaOption(payoff, exercise)
    option2.setPricingEngine(ql.AnalyticHestonEngine(model))
    analytic_npv = option2.NPV()

    assert option.NPV() == pytest.approx(analytic_npv, rel=0.05)
