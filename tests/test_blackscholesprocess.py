import math

import pytest

import pyquantlib as ql
from pyquantlib.base import Observer, StochasticProcess, StochasticProcess1D


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


def test_generalized_bs_process_creation(market_env):
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


def test_generalized_bs_process_evolve(market_env):
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


def test_bs_merton_alias():
    """Test BlackScholesMertonProcess is alias for GeneralizedBlackScholesProcess."""
    assert ql.BlackScholesMertonProcess is ql.GeneralizedBlackScholesProcess


def test_blackscholes_process(market_env):
    """Test BlackScholesProcess (no dividend)."""
    process = ql.BlackScholesProcess(
        market_env["spot"],
        market_env["risk_free"],
        market_env["vol"],
    )

    assert isinstance(process, ql.BlackScholesProcess)
    assert isinstance(process, ql.GeneralizedBlackScholesProcess)
    assert process.x0() == 100.0


def test_black_process(market_env):
    """Test BlackProcess (forward price dynamics)."""
    process = ql.BlackProcess(
        market_env["spot"],
        market_env["risk_free"],
        market_env["vol"],
    )

    assert isinstance(process, ql.BlackProcess)
    assert isinstance(process, ql.GeneralizedBlackScholesProcess)


def test_garman_kohlhagen_process(market_env):
    """Test GarmanKohlhagenProcess (FX options)."""
    process = ql.GarmanKohlhagenProcess(
        market_env["spot"],
        market_env["dividend"],  # foreign rate
        market_env["risk_free"],  # domestic rate
        market_env["vol"],
    )

    assert isinstance(process, ql.GarmanKohlhagenProcess)
    assert isinstance(process, ql.GeneralizedBlackScholesProcess)


def test_euler_discretization(market_env):
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
