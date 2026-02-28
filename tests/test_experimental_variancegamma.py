"""
Tests for experimental variance gamma module.

Corresponds to src/experimental/variancegamma/*.cpp bindings.
"""

import pytest

import pyquantlib as ql


# =============================================================================
# Common fixtures
# =============================================================================


@pytest.fixture()
def vg_env():
    ql.Settings.evaluationDate = ql.Date(15, 5, 2025)
    spot = ql.SimpleQuote(100.0)
    rate = ql.FlatForward(ql.Date(15, 5, 2025), 0.05, ql.Actual365Fixed())
    div = ql.FlatForward(ql.Date(15, 5, 2025), 0.02, ql.Actual365Fixed())
    return {
        "spot": spot,
        "rate": rate,
        "div": div,
        "sigma": 0.20,
        "nu": 0.50,
        "theta": -0.10,
    }


# =============================================================================
# VarianceGammaProcess
# =============================================================================


def test_variancegammaprocess_construction(vg_env):
    """VarianceGammaProcess can be constructed."""
    env = vg_env
    process = ql.VarianceGammaProcess(
        env["spot"], env["div"], env["rate"],
        env["sigma"], env["nu"], env["theta"],
    )
    assert process is not None


def test_variancegammaprocess_hidden_handle(vg_env):
    """VarianceGammaProcess constructed with shared_ptr (hidden handles)."""
    env = vg_env
    process = ql.VarianceGammaProcess(
        env["spot"], env["div"], env["rate"],
        env["sigma"], env["nu"], env["theta"],
    )
    assert process is not None


def test_variancegammaprocess_accessors(vg_env):
    """VarianceGammaProcess accessors return correct values."""
    env = vg_env
    process = ql.VarianceGammaProcess(
        env["spot"], env["div"], env["rate"],
        env["sigma"], env["nu"], env["theta"],
    )
    assert process.sigma() == pytest.approx(0.20)
    assert process.nu() == pytest.approx(0.50)
    assert process.theta() == pytest.approx(-0.10)


def test_variancegammaprocess_handles(vg_env):
    """VarianceGammaProcess provides handle accessors."""
    env = vg_env
    process = ql.VarianceGammaProcess(
        env["spot"], env["div"], env["rate"],
        env["sigma"], env["nu"], env["theta"],
    )
    assert process.s0() is not None
    assert process.dividendYield() is not None
    assert process.riskFreeRate() is not None


# =============================================================================
# VarianceGammaModel
# =============================================================================


def test_variancegammamodel_construction(vg_env):
    """VarianceGammaModel can be constructed."""
    env = vg_env
    process = ql.VarianceGammaProcess(
        env["spot"], env["div"], env["rate"],
        env["sigma"], env["nu"], env["theta"],
    )
    model = ql.VarianceGammaModel(process)
    assert model is not None


def test_variancegammamodel_inherits_calibratedmodel(vg_env):
    """VarianceGammaModel inherits from CalibratedModel."""
    env = vg_env
    process = ql.VarianceGammaProcess(
        env["spot"], env["div"], env["rate"],
        env["sigma"], env["nu"], env["theta"],
    )
    model = ql.VarianceGammaModel(process)
    assert isinstance(model, ql.base.CalibratedModel)


def test_variancegammamodel_accessors(vg_env):
    """VarianceGammaModel accessors return correct values."""
    env = vg_env
    process = ql.VarianceGammaProcess(
        env["spot"], env["div"], env["rate"],
        env["sigma"], env["nu"], env["theta"],
    )
    model = ql.VarianceGammaModel(process)
    assert model.sigma() == pytest.approx(0.20)
    assert model.nu() == pytest.approx(0.50)
    assert model.theta() == pytest.approx(-0.10)


def test_variancegammamodel_process(vg_env):
    """VarianceGammaModel returns its underlying process."""
    env = vg_env
    process = ql.VarianceGammaProcess(
        env["spot"], env["div"], env["rate"],
        env["sigma"], env["nu"], env["theta"],
    )
    model = ql.VarianceGammaModel(process)
    p = model.process()
    assert p is not None
    assert isinstance(p, ql.VarianceGammaProcess)


# =============================================================================
# VarianceGammaEngine (analytic)
# =============================================================================


def test_variancegammaengine_construction(vg_env):
    """VarianceGammaEngine can be constructed."""
    env = vg_env
    process = ql.VarianceGammaProcess(
        env["spot"], env["div"], env["rate"],
        env["sigma"], env["nu"], env["theta"],
    )
    engine = ql.VarianceGammaEngine(process)
    assert engine is not None


def test_variancegammaengine_pricing(vg_env):
    """VarianceGammaEngine prices a vanilla option correctly."""
    env = vg_env
    process = ql.VarianceGammaProcess(
        env["spot"], env["div"], env["rate"],
        env["sigma"], env["nu"], env["theta"],
    )
    payoff = ql.PlainVanillaPayoff(ql.Call, 100.0)
    exercise = ql.EuropeanExercise(ql.Date(15, 5, 2026))
    option = ql.VanillaOption(payoff, exercise)
    option.setPricingEngine(ql.VarianceGammaEngine(process))
    assert option.NPV() == pytest.approx(9.136692, rel=1e-4)


def test_variancegammaengine_custom_tolerance(vg_env):
    """VarianceGammaEngine accepts custom absolute error tolerance."""
    env = vg_env
    process = ql.VarianceGammaProcess(
        env["spot"], env["div"], env["rate"],
        env["sigma"], env["nu"], env["theta"],
    )
    engine = ql.VarianceGammaEngine(process, 1e-8)
    assert engine is not None


# =============================================================================
# FFTVarianceGammaEngine
# =============================================================================


def test_fftvariancegammaengine_construction(vg_env):
    """FFTVarianceGammaEngine can be constructed."""
    env = vg_env
    process = ql.VarianceGammaProcess(
        env["spot"], env["div"], env["rate"],
        env["sigma"], env["nu"], env["theta"],
    )
    engine = ql.FFTVarianceGammaEngine(process)
    assert engine is not None


def test_fftvariancegammaengine_pricing(vg_env):
    """FFTVarianceGammaEngine prices a vanilla option correctly."""
    env = vg_env
    process = ql.VarianceGammaProcess(
        env["spot"], env["div"], env["rate"],
        env["sigma"], env["nu"], env["theta"],
    )
    payoff = ql.PlainVanillaPayoff(ql.Call, 100.0)
    exercise = ql.EuropeanExercise(ql.Date(15, 5, 2026))
    option = ql.VanillaOption(payoff, exercise)
    option.setPricingEngine(ql.FFTVarianceGammaEngine(process, 0.001))
    assert option.NPV() == pytest.approx(9.135540, rel=1e-4)


def test_fftvariancegammaengine_custom_spacing(vg_env):
    """FFTVarianceGammaEngine accepts custom log-strike spacing."""
    env = vg_env
    process = ql.VarianceGammaProcess(
        env["spot"], env["div"], env["rate"],
        env["sigma"], env["nu"], env["theta"],
    )
    engine = ql.FFTVarianceGammaEngine(process, 0.01)
    assert engine is not None
