"""
Tests for processes module.

Corresponds to src/processes/*.cpp bindings.
"""

import math

import pytest

import pyquantlib as ql
from pyquantlib.base import Observer, StochasticProcess, StochasticProcess1D


# =============================================================================
# StochasticProcess (ABC)
# =============================================================================


def test_stochasticprocess_zombie():
    """Test direct instantiation creates zombie."""
    zombie = StochasticProcess()
    with pytest.raises(RuntimeError, match="pure virtual"):
        zombie.size()


def test_stochasticprocess1d_zombie():
    """Test direct instantiation creates zombie."""
    zombie = StochasticProcess1D()
    with pytest.raises(RuntimeError, match="pure virtual"):
        zombie.x0()


def test_stochasticprocess1d_subclass():
    """Test Python subclass implementing StochasticProcess1D."""

    class ConstantProcess(StochasticProcess1D):
        def x0(self):
            return 100.0

        def drift(self, t, x):
            return 0.0

        def diffusion(self, t, x):
            return 0.0

        def evolve(self, t0, x0, dt, dw):
            return x0

    proc = ConstantProcess()
    assert proc.x0() == 100.0
    assert proc.drift(0.0, 100.0) == 0.0
    assert proc.evolve(0.0, 100.0, 0.01, 0.1) == 100.0


def test_stochasticprocess1d_discretization_exists():
    """Test discretization attribute exists."""
    assert hasattr(StochasticProcess1D, 'discretization')


# =============================================================================
# GeneralizedBlackScholesProcess
# =============================================================================


@pytest.fixture
def market_env():
    """Market environment for Black-Scholes process tests."""
    today = ql.Date(20, 2, 2025)
    ql.Settings.instance().evaluationDate = today

    spot = ql.SimpleQuote(100.0)
    rate = ql.SimpleQuote(0.05)
    vol = ql.SimpleQuote(0.20)

    dc = ql.Actual365Fixed()
    cal = ql.TARGET()

    risk_free_ts = ql.FlatForward(today, ql.QuoteHandle(rate), dc)
    dividend_ts = ql.FlatForward(today, 0.0, dc)
    vol_ts = ql.BlackConstantVol(today, cal, ql.QuoteHandle(vol), dc)

    return {
        "spot": ql.QuoteHandle(spot),
        "dividend": ql.YieldTermStructureHandle(dividend_ts),
        "risk_free": ql.YieldTermStructureHandle(risk_free_ts),
        "vol": ql.BlackVolTermStructureHandle(vol_ts),
    }


def test_generalizedblackscholesprocess_creation(market_env):
    """Test GeneralizedBlackScholesProcess creation and inheritance."""
    process = ql.GeneralizedBlackScholesProcess(
        market_env["spot"],
        market_env["dividend"],
        market_env["risk_free"],
        market_env["vol"],
    )

    assert process is not None
    assert isinstance(process, ql.GeneralizedBlackScholesProcess)
    assert isinstance(process, StochasticProcess1D)
    assert isinstance(process, StochasticProcess)
    assert isinstance(process, Observer)
    assert isinstance(process, ql.Observable)
    assert process.x0() == 100.0


def test_generalizedblackscholesprocess_evolve(market_env):
    """Test evolve method of GeneralizedBlackScholesProcess."""
    process = ql.GeneralizedBlackScholesProcess(
        market_env["spot"],
        market_env["dividend"],
        market_env["risk_free"],
        market_env["vol"],
    )

    t0, x0, dt = 0.0, process.x0(), 1.0

    r = process.riskFreeRate().get().zeroRate(dt, ql.Continuous).rate()
    q = process.dividendYield().get().zeroRate(dt, ql.Continuous).rate()
    sigma = process.localVolatility().get().localVol(dt, x0)

    # No shock (dw = 0)
    evolved = process.evolve(t0, x0, dt, 0.0)
    expected = x0 * math.exp((r - q - 0.5 * sigma**2) * dt)
    assert evolved == pytest.approx(expected)

    # With shock (dw = 1)
    evolved_shock = process.evolve(t0, x0, dt, 1.0)
    expected_shock = expected * math.exp(sigma * math.sqrt(dt))
    assert evolved_shock == pytest.approx(expected_shock)


def test_blackscholesmerton_alias():
    """Test BlackScholesMertonProcess is alias for GeneralizedBlackScholesProcess."""
    assert ql.BlackScholesMertonProcess is ql.GeneralizedBlackScholesProcess


def test_generalizedblackscholesprocess_euler_discretization(market_env):
    """Test EulerDiscretization with process."""
    euler = ql.EulerDiscretization()

    process = ql.GeneralizedBlackScholesProcess(
        market_env["spot"],
        market_env["dividend"],
        market_env["risk_free"],
        market_env["vol"],
        euler,
    )

    assert process is not None
    evolved = process.evolve(0.0, 100.0, 1.0, 0.0)
    assert isinstance(evolved, float)


# --- GeneralizedBlackScholesProcess hidden handle constructors ---


@pytest.fixture
def raw_market_data():
    """Raw market data (no handles) for hidden handle tests."""
    today = ql.Date(20, 2, 2025)
    ql.Settings.instance().evaluationDate = today

    dc = ql.Actual365Fixed()
    cal = ql.TARGET()

    spot = ql.SimpleQuote(100.0)
    rate = ql.SimpleQuote(0.05)
    div = ql.SimpleQuote(0.02)
    vol = ql.SimpleQuote(0.20)

    return {
        "spot": spot,
        "risk_free_ts": ql.FlatForward(today, ql.QuoteHandle(rate), dc),
        "dividend_ts": ql.FlatForward(today, ql.QuoteHandle(div), dc),
        "vol_ts": ql.BlackConstantVol(today, cal, ql.QuoteHandle(vol), dc),
        "today": today,
        "dc": dc,
    }


def test_generalizedblackscholesprocess_hidden_handles(raw_market_data):
    """Test GeneralizedBlackScholesProcess with hidden handles."""
    process = ql.GeneralizedBlackScholesProcess(
        raw_market_data["spot"],
        raw_market_data["dividend_ts"],
        raw_market_data["risk_free_ts"],
        raw_market_data["vol_ts"],
    )

    assert process is not None
    assert process.x0() == 100.0


def test_generalizedblackscholesprocess_hidden_vs_explicit_handles(raw_market_data):
    """Compare hidden and explicit handle constructors."""
    # Hidden handles
    process_hidden = ql.GeneralizedBlackScholesProcess(
        raw_market_data["spot"],
        raw_market_data["dividend_ts"],
        raw_market_data["risk_free_ts"],
        raw_market_data["vol_ts"],
    )

    # Explicit handles
    process_explicit = ql.GeneralizedBlackScholesProcess(
        ql.QuoteHandle(raw_market_data["spot"]),
        ql.YieldTermStructureHandle(raw_market_data["dividend_ts"]),
        ql.YieldTermStructureHandle(raw_market_data["risk_free_ts"]),
        ql.BlackVolTermStructureHandle(raw_market_data["vol_ts"]),
    )

    # Both should price identically
    payoff = ql.PlainVanillaPayoff(ql.OptionType.Call, 100.0)
    exercise = ql.EuropeanExercise(raw_market_data["today"] + ql.Period(1, ql.Years))

    option1 = ql.VanillaOption(payoff, exercise)
    option1.setPricingEngine(ql.AnalyticEuropeanEngine(process_hidden))

    option2 = ql.VanillaOption(payoff, exercise)
    option2.setPricingEngine(ql.AnalyticEuropeanEngine(process_explicit))

    assert option1.NPV() == pytest.approx(option2.NPV(), rel=1e-10)


def test_generalizedblackscholesprocess_with_local_vol(raw_market_data):
    """Test GeneralizedBlackScholesProcess with external local vol."""
    local_vol = ql.LocalConstantVol(
        raw_market_data["today"],
        0.20,
        raw_market_data["dc"],
    )
    local_vol_handle = ql.LocalVolTermStructureHandle(local_vol)

    process = ql.GeneralizedBlackScholesProcess(
        ql.QuoteHandle(raw_market_data["spot"]),
        ql.YieldTermStructureHandle(raw_market_data["dividend_ts"]),
        ql.YieldTermStructureHandle(raw_market_data["risk_free_ts"]),
        ql.BlackVolTermStructureHandle(raw_market_data["vol_ts"]),
        local_vol_handle,
    )

    assert process is not None
    assert isinstance(process, ql.GeneralizedBlackScholesProcess)
    assert process.localVolatility() is not None


def test_generalizedblackscholesprocess_with_local_vol_hidden_handle(raw_market_data):
    """Test GeneralizedBlackScholesProcess with local vol using hidden handles."""
    local_vol = ql.LocalConstantVol(
        raw_market_data["today"],
        0.20,
        raw_market_data["dc"],
    )

    process = ql.GeneralizedBlackScholesProcess(
        raw_market_data["spot"],
        raw_market_data["dividend_ts"],
        raw_market_data["risk_free_ts"],
        raw_market_data["vol_ts"],
        local_vol,
    )

    assert process is not None
    assert isinstance(process, ql.GeneralizedBlackScholesProcess)


# =============================================================================
# BlackScholesProcess
# =============================================================================


def test_blackscholesprocess_creation(market_env):
    """Test BlackScholesProcess (no dividend)."""
    process = ql.BlackScholesProcess(
        market_env["spot"],
        market_env["risk_free"],
        market_env["vol"],
    )

    assert isinstance(process, ql.BlackScholesProcess)
    assert isinstance(process, ql.GeneralizedBlackScholesProcess)
    assert process.x0() == 100.0


def test_blackscholesprocess_hidden_handles(raw_market_data):
    """Test BlackScholesProcess with hidden handles."""
    process = ql.BlackScholesProcess(
        raw_market_data["spot"],
        raw_market_data["risk_free_ts"],
        raw_market_data["vol_ts"],
    )

    assert process is not None
    assert isinstance(process, ql.BlackScholesProcess)


# =============================================================================
# BlackProcess
# =============================================================================


def test_blackprocess_creation(market_env):
    """Test BlackProcess (forward price dynamics)."""
    process = ql.BlackProcess(
        market_env["spot"],
        market_env["risk_free"],
        market_env["vol"],
    )

    assert isinstance(process, ql.BlackProcess)
    assert isinstance(process, ql.GeneralizedBlackScholesProcess)


def test_blackprocess_hidden_handles(raw_market_data):
    """Test BlackProcess with hidden handles."""
    forward = ql.SimpleQuote(100.0)
    process = ql.BlackProcess(
        forward,
        raw_market_data["risk_free_ts"],
        raw_market_data["vol_ts"],
    )

    assert process is not None
    assert isinstance(process, ql.BlackProcess)


# =============================================================================
# GarmanKohlhagenProcess
# =============================================================================


def test_garmankohlhagenprocess_creation(market_env):
    """Test GarmanKohlhagenProcess (FX options)."""
    process = ql.GarmanKohlhagenProcess(
        market_env["spot"],
        market_env["dividend"],  # foreign rate
        market_env["risk_free"],  # domestic rate
        market_env["vol"],
    )

    assert isinstance(process, ql.GarmanKohlhagenProcess)
    assert isinstance(process, ql.GeneralizedBlackScholesProcess)


def test_garmankohlhagenprocess_hidden_handles(raw_market_data):
    """Test GarmanKohlhagenProcess with hidden handles."""
    foreign_ts = ql.FlatForward(raw_market_data["today"], 0.03, raw_market_data["dc"])

    process = ql.GarmanKohlhagenProcess(
        raw_market_data["spot"],
        foreign_ts,
        raw_market_data["risk_free_ts"],
        raw_market_data["vol_ts"],
    )

    assert process is not None
    assert isinstance(process, ql.GarmanKohlhagenProcess)


# =============================================================================
# HestonProcess
# =============================================================================


@pytest.fixture
def heston_env():
    """Market environment for Heston process tests."""
    today = ql.Date(20, 6, 2025)
    ql.Settings.instance().evaluationDate = today

    spot = ql.SimpleQuote(100.0)
    rate = ql.SimpleQuote(0.03)
    dividend = ql.SimpleQuote(0.01)

    dc = ql.Actual365Fixed()
    risk_free_ts = ql.FlatForward(today, ql.QuoteHandle(rate), dc)
    dividend_ts = ql.FlatForward(today, ql.QuoteHandle(dividend), dc)

    return {
        "spot": ql.QuoteHandle(spot),
        "risk_free": ql.YieldTermStructureHandle(risk_free_ts),
        "dividend": ql.YieldTermStructureHandle(dividend_ts),
        "v0": 0.04,
        "kappa": 1.0,
        "theta": 0.09,
        "sigma": 0.2,
        "rho": -0.75,
    }


def test_hestonprocess_creation(heston_env):
    """Test HestonProcess creation and parameter inspectors."""
    process = ql.HestonProcess(
        heston_env["risk_free"],
        heston_env["dividend"],
        heston_env["spot"],
        heston_env["v0"],
        heston_env["kappa"],
        heston_env["theta"],
        heston_env["sigma"],
        heston_env["rho"],
    )

    assert process is not None
    assert isinstance(process, ql.HestonProcess)
    assert isinstance(process, StochasticProcess)

    assert process.s0().get().value() == 100.0
    assert process.v0() == heston_env["v0"]
    assert process.kappa() == heston_env["kappa"]
    assert process.theta() == heston_env["theta"]
    assert process.sigma() == heston_env["sigma"]
    assert process.rho() == heston_env["rho"]


def test_hestonprocess_discretization_enum():
    """Test HestonProcess.Discretization enum values."""
    D = ql.HestonProcess.Discretization

    assert hasattr(D, "PartialTruncation")
    assert hasattr(D, "FullTruncation")
    assert hasattr(D, "Reflection")
    assert hasattr(D, "NonCentralChiSquareVariance")
    assert hasattr(D, "QuadraticExponential")
    assert hasattr(D, "QuadraticExponentialMartingale")
    assert hasattr(D, "BroadieKayaExactSchemeLobatto")
    assert hasattr(D, "BroadieKayaExactSchemeLaguerre")
    assert hasattr(D, "BroadieKayaExactSchemeTrapezoidal")


def test_hestonprocess_with_discretization(heston_env):
    """Test HestonProcess with explicit discretization scheme."""
    process = ql.HestonProcess(
        heston_env["risk_free"],
        heston_env["dividend"],
        heston_env["spot"],
        heston_env["v0"],
        heston_env["kappa"],
        heston_env["theta"],
        heston_env["sigma"],
        heston_env["rho"],
        ql.HestonProcess.FullTruncation,
    )

    assert process is not None


def test_hestonprocess_term_structure_handles(heston_env):
    """Test term structure handle accessors."""
    process = ql.HestonProcess(
        heston_env["risk_free"],
        heston_env["dividend"],
        heston_env["spot"],
        heston_env["v0"],
        heston_env["kappa"],
        heston_env["theta"],
        heston_env["sigma"],
        heston_env["rho"],
    )

    rf = process.riskFreeRate()
    div = process.dividendYield()

    assert rf is not None
    assert div is not None
    assert rf.get().zeroRate(1.0, ql.Continuous).rate() == pytest.approx(0.03)
    assert div.get().zeroRate(1.0, ql.Continuous).rate() == pytest.approx(0.01)


def test_hestonprocess_pdf():
    """Test HestonProcess probability density function exists."""
    # Just verify the method is accessible (numerical stability varies by params)
    assert hasattr(ql.HestonProcess, "pdf")


# --- HestonProcess hidden handle constructors ---


def test_hestonprocess_hidden_handles(heston_env):
    """Test HestonProcess with hidden handles."""
    today = ql.Date(20, 6, 2025)
    ql.Settings.instance().evaluationDate = today

    spot = ql.SimpleQuote(100.0)
    dc = ql.Actual365Fixed()
    risk_free_ts = ql.FlatForward(today, 0.03, dc)
    dividend_ts = ql.FlatForward(today, 0.01, dc)

    process = ql.HestonProcess(
        risk_free_ts,
        dividend_ts,
        spot,
        v0=0.04,
        kappa=1.0,
        theta=0.09,
        sigma=0.2,
        rho=-0.75,
    )

    assert process is not None
    assert process.v0() == 0.04
    assert process.kappa() == 1.0
    assert process.theta() == 0.09
    assert process.sigma() == 0.2
    assert process.rho() == -0.75


def test_hestonprocess_hidden_vs_explicit_handles(heston_env):
    """Compare hidden and explicit handle constructors."""
    today = ql.Date(20, 6, 2025)
    ql.Settings.instance().evaluationDate = today

    spot = ql.SimpleQuote(100.0)
    dc = ql.Actual365Fixed()
    risk_free_ts = ql.FlatForward(today, 0.03, dc)
    dividend_ts = ql.FlatForward(today, 0.01, dc)

    # Hidden handles
    process_hidden = ql.HestonProcess(
        risk_free_ts, dividend_ts, spot,
        0.04, 1.0, 0.09, 0.2, -0.75,
    )

    # Explicit handles
    process_explicit = ql.HestonProcess(
        ql.YieldTermStructureHandle(risk_free_ts),
        ql.YieldTermStructureHandle(dividend_ts),
        ql.QuoteHandle(spot),
        0.04, 1.0, 0.09, 0.2, -0.75,
    )

    assert process_hidden.v0() == process_explicit.v0()
    assert process_hidden.kappa() == process_explicit.kappa()
    assert process_hidden.theta() == process_explicit.theta()
    assert process_hidden.sigma() == process_explicit.sigma()
    assert process_hidden.rho() == process_explicit.rho()


# =============================================================================
# BatesProcess
# =============================================================================


@pytest.fixture
def bates_env():
    """Market environment for Bates process tests."""
    today = ql.Date(20, 6, 2025)
    ql.Settings.instance().evaluationDate = today

    spot = ql.SimpleQuote(100.0)
    rate = ql.SimpleQuote(0.03)
    dividend = ql.SimpleQuote(0.01)

    dc = ql.Actual365Fixed()
    risk_free_ts = ql.FlatForward(today, ql.QuoteHandle(rate), dc)
    dividend_ts = ql.FlatForward(today, ql.QuoteHandle(dividend), dc)

    return {
        "spot": ql.QuoteHandle(spot),
        "risk_free": ql.YieldTermStructureHandle(risk_free_ts),
        "dividend": ql.YieldTermStructureHandle(dividend_ts),
        "v0": 0.04,
        "kappa": 1.0,
        "theta": 0.04,
        "sigma": 0.3,
        "rho": -0.7,
        "lambda": 0.1,
        "nu": -0.05,
        "delta": 0.1,
    }


def test_batesprocess_creation(bates_env):
    """Test BatesProcess creation."""
    process = ql.BatesProcess(
        bates_env["risk_free"],
        bates_env["dividend"],
        bates_env["spot"],
        bates_env["v0"],
        bates_env["kappa"],
        bates_env["theta"],
        bates_env["sigma"],
        bates_env["rho"],
        bates_env["lambda"],
        bates_env["nu"],
        bates_env["delta"],
    )

    assert process is not None
    assert isinstance(process, ql.BatesProcess)
    assert isinstance(process, ql.HestonProcess)


def test_batesprocess_heston_parameters(bates_env):
    """Test BatesProcess inherits Heston parameter accessors."""
    process = ql.BatesProcess(
        bates_env["risk_free"],
        bates_env["dividend"],
        bates_env["spot"],
        bates_env["v0"],
        bates_env["kappa"],
        bates_env["theta"],
        bates_env["sigma"],
        bates_env["rho"],
        bates_env["lambda"],
        bates_env["nu"],
        bates_env["delta"],
    )

    assert process.v0() == bates_env["v0"]
    assert process.kappa() == bates_env["kappa"]
    assert process.theta() == bates_env["theta"]
    assert process.sigma() == bates_env["sigma"]
    assert process.rho() == bates_env["rho"]


def test_batesprocess_jump_parameters(bates_env):
    """Test BatesProcess jump parameter accessors."""
    process = ql.BatesProcess(
        bates_env["risk_free"],
        bates_env["dividend"],
        bates_env["spot"],
        bates_env["v0"],
        bates_env["kappa"],
        bates_env["theta"],
        bates_env["sigma"],
        bates_env["rho"],
        bates_env["lambda"],
        bates_env["nu"],
        bates_env["delta"],
    )

    assert process.lambda_() == pytest.approx(bates_env["lambda"])
    assert process.nu() == pytest.approx(bates_env["nu"])
    assert process.delta() == pytest.approx(bates_env["delta"])


def test_batesprocess_with_discretization(bates_env):
    """Test BatesProcess with explicit discretization scheme."""
    process = ql.BatesProcess(
        bates_env["risk_free"],
        bates_env["dividend"],
        bates_env["spot"],
        bates_env["v0"],
        bates_env["kappa"],
        bates_env["theta"],
        bates_env["sigma"],
        bates_env["rho"],
        bates_env["lambda"],
        bates_env["nu"],
        bates_env["delta"],
        ql.HestonProcess.FullTruncation,
    )

    assert process is not None
