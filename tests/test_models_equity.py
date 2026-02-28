"""
Tests for equity models module.

Corresponds to src/models/equity/*.cpp bindings.
"""

import pytest

import pyquantlib as ql


# =============================================================================
# GJRGARCHModel
# =============================================================================


@pytest.fixture()
def gjrgarch_model_env():
    ql.Settings.evaluationDate = ql.Date(15, 5, 2025)
    rate = ql.FlatForward(ql.Date(15, 5, 2025), 0.05, ql.Actual365Fixed())
    div = ql.FlatForward(ql.Date(15, 5, 2025), 0.02, ql.Actual365Fixed())
    spot = ql.SimpleQuote(100.0)
    process = ql.GJRGARCHProcess(
        rate, div, spot,
        0.04 / 252.0, 2e-6, 0.04, 0.94, 0.02, 0.0, 252.0,
    )
    return {"process": process}


def test_gjrgarchmodel_construction(gjrgarch_model_env):
    """GJRGARCHModel can be constructed."""
    model = ql.GJRGARCHModel(gjrgarch_model_env["process"])
    assert model is not None


def test_gjrgarchmodel_inherits_calibratedmodel(gjrgarch_model_env):
    """GJRGARCHModel inherits from CalibratedModel."""
    model = ql.GJRGARCHModel(gjrgarch_model_env["process"])
    assert isinstance(model, ql.base.CalibratedModel)


def test_gjrgarchmodel_accessors(gjrgarch_model_env):
    """GJRGARCHModel accessors return correct values."""
    model = ql.GJRGARCHModel(gjrgarch_model_env["process"])
    assert model.omega() == pytest.approx(2e-6)
    assert model.alpha() == pytest.approx(0.04)
    assert model.beta() == pytest.approx(0.94)
    assert model.gamma() == pytest.approx(0.02)
    assert model.lambda_() == pytest.approx(0.0)
    assert model.v0() == pytest.approx(0.04 / 252.0)


def test_gjrgarchmodel_process(gjrgarch_model_env):
    """GJRGARCHModel returns its underlying process."""
    model = ql.GJRGARCHModel(gjrgarch_model_env["process"])
    process = model.process()
    assert process is not None
    assert isinstance(process, ql.GJRGARCHProcess)


# =============================================================================
# HestonModelHelper
# =============================================================================


@pytest.fixture
def heston_helper_env():
    """Environment for HestonModelHelper tests."""
    today = ql.Date(15, ql.January, 2026)
    ql.Settings.instance().evaluationDate = today

    dc = ql.Actual365Fixed()
    risk_free = ql.FlatForward(today, 0.05, dc)
    dividend = ql.FlatForward(today, 0.02, dc)
    vol_quote = ql.SimpleQuote(0.20)

    return {
        "today": today,
        "risk_free": risk_free,
        "dividend": dividend,
        "vol_quote": vol_quote,
    }


def test_hestonmodelhelper_construction_real_s0(heston_helper_env):
    """Test HestonModelHelper construction with Real spot price."""
    env = heston_helper_env

    helper = ql.HestonModelHelper(
        maturity=ql.Period(1, ql.Years),
        calendar=ql.TARGET(),
        s0=100.0,
        strikePrice=105.0,
        volatility=env["vol_quote"],
        riskFreeRate=env["risk_free"],
        dividendYield=env["dividend"],
    )
    assert helper is not None
    assert isinstance(helper, ql.base.BlackCalibrationHelper)


def test_hestonmodelhelper_construction_handle_s0(heston_helper_env):
    """Test HestonModelHelper construction with Handle<Quote> spot price."""
    env = heston_helper_env

    helper = ql.HestonModelHelper(
        maturity=ql.Period(1, ql.Years),
        calendar=ql.TARGET(),
        s0=ql.QuoteHandle(ql.SimpleQuote(100.0)),
        strikePrice=105.0,
        volatility=ql.QuoteHandle(env["vol_quote"]),
        riskFreeRate=ql.YieldTermStructureHandle(env["risk_free"]),
        dividendYield=ql.YieldTermStructureHandle(env["dividend"]),
    )
    assert helper is not None
    assert isinstance(helper, ql.base.BlackCalibrationHelper)


def test_hestonmodelhelper_maturity(heston_helper_env):
    """Test HestonModelHelper maturity accessor."""
    env = heston_helper_env

    helper = ql.HestonModelHelper(
        maturity=ql.Period(1, ql.Years),
        calendar=ql.TARGET(),
        s0=100.0,
        strikePrice=105.0,
        volatility=env["vol_quote"],
        riskFreeRate=env["risk_free"],
        dividendYield=env["dividend"],
    )
    assert helper.maturity() == pytest.approx(1.0, abs=0.01)
