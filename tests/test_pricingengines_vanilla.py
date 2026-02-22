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
