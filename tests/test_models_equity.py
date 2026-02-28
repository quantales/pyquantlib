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
