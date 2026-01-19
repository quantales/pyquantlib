"""Tests for ql/processes/*.hpp bindings."""

import pytest

import pyquantlib as ql


# --- BatesProcess ---


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


def test_bates_process_creation(bates_env):
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


def test_bates_process_heston_parameters(bates_env):
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


def test_bates_process_jump_parameters(bates_env):
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


def test_bates_process_with_discretization(bates_env):
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
