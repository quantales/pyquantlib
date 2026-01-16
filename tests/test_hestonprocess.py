import pytest

import pyquantlib as ql
from pyquantlib.base import StochasticProcess


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


def test_heston_process_creation(heston_env):
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


def test_heston_discretization_enum():
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


def test_heston_with_discretization(heston_env):
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


def test_heston_term_structure_handles(heston_env):
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


def test_heston_pdf():
    """Test HestonProcess probability density function exists."""
    # Just verify the method is accessible (numerical stability varies by params)
    assert hasattr(ql.HestonProcess, "pdf")


# --- Hidden handle constructors ---


def test_heston_hidden_handles(heston_env):
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


def test_heston_hidden_vs_explicit_handles(heston_env):
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
