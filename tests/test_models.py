"""
Tests for models module.

Corresponds to src/models/*.cpp bindings.
"""

import pytest

import pyquantlib as ql


def test_constant_parameter():
    """Test ConstantParameter creation and usage."""
    constraint = ql.PositiveConstraint()
    param = ql.ConstantParameter(0.5, constraint)

    assert param.size() == 1
    assert param(0.0) == pytest.approx(0.5)
    assert param(1.0) == pytest.approx(0.5)


def test_constant_parameter_constraint_only():
    """Test ConstantParameter with constraint only."""
    constraint = ql.NoConstraint()
    param = ql.ConstantParameter(constraint)

    assert param.size() == 1


def test_parameter_methods():
    """Test Parameter methods."""
    constraint = ql.BoundaryConstraint(0.0, 1.0)
    param = ql.ConstantParameter(0.5, constraint)

    params = param.params()
    assert len(params) == 1
    assert params[0] == pytest.approx(0.5)

    assert param.testParams(ql.Array([0.3]))
    assert not param.testParams(ql.Array([1.5]))  # Outside bounds


@pytest.fixture
def piecewise_heston_env():
    """Environment for PiecewiseTimeDependentHestonModel tests."""
    today = ql.Date(20, 2, 2025)
    ql.Settings.instance().evaluationDate = today

    dc = ql.Actual365Fixed()

    risk_free_ts = ql.FlatForward(today, 0.05, dc)
    dividend_ts = ql.FlatForward(today, 0.02, dc)
    spot = ql.SimpleQuote(100.0)

    return {
        "risk_free": ql.YieldTermStructureHandle(risk_free_ts),
        "dividend": ql.YieldTermStructureHandle(dividend_ts),
        "spot": ql.QuoteHandle(spot),
        "today": today,
    }


def test_piecewise_heston_model(piecewise_heston_env):
    """Test PiecewiseTimeDependentHestonModel construction."""
    env = piecewise_heston_env

    times = [0.0, 0.5, 1.0, 2.0]
    time_grid = ql.TimeGrid(times)

    constraint = ql.PositiveConstraint()
    theta = ql.ConstantParameter(0.04, constraint)
    kappa = ql.ConstantParameter(2.0, constraint)
    sigma = ql.ConstantParameter(0.3, constraint)

    rho_constraint = ql.BoundaryConstraint(-1.0, 1.0)
    rho = ql.ConstantParameter(-0.7, rho_constraint)

    v0 = 0.04

    model = ql.PiecewiseTimeDependentHestonModel(
        env["risk_free"],
        env["dividend"],
        env["spot"],
        v0,
        theta,
        kappa,
        sigma,
        rho,
        time_grid,
    )

    assert model.v0() == pytest.approx(0.04)
    assert model.theta(0.5) == pytest.approx(0.04)
    assert model.kappa(0.5) == pytest.approx(2.0)
    assert model.sigma(0.5) == pytest.approx(0.3)
    assert model.rho(0.5) == pytest.approx(-0.7)
