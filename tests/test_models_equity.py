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


# =============================================================================
# HestonSLVFokkerPlanckFdmParams
# =============================================================================


def test_fokkerplanckfdmparams_defaults():
    """HestonSLVFokkerPlanckFdmParams has sensible defaults."""
    params = ql.HestonSLVFokkerPlanckFdmParams()
    assert params.xGrid == 301
    assert params.vGrid == 601
    assert params.tMaxStepsPerYear == 2000
    assert params.tMinStepsPerYear == 30
    assert params.tStepNumberDecay == pytest.approx(2.0)
    assert params.nRannacherTimeSteps == 2
    assert params.predictionCorrectionSteps == 2
    assert params.x0Density == pytest.approx(0.1)
    assert params.localVolEpsProb == pytest.approx(1e-4)
    assert params.maxIntegrationIterations == 10000
    assert params.vLowerEps == pytest.approx(1e-6)
    assert params.vUpperEps == pytest.approx(1e-6)
    assert params.vMin == pytest.approx(1e-6)
    assert params.leverageFctPropEps == pytest.approx(1e-5)


def test_fokkerplanckfdmparams_readwrite():
    """HestonSLVFokkerPlanckFdmParams fields are read-writable."""
    params = ql.HestonSLVFokkerPlanckFdmParams()
    params.xGrid = 101
    params.vGrid = 201
    params.predictionCorrectionSteps = 4
    assert params.xGrid == 101
    assert params.vGrid == 201
    assert params.predictionCorrectionSteps == 4


def test_fokkerplanckfdmparams_enums():
    """HestonSLVFokkerPlanckFdmParams enum fields work."""
    params = ql.HestonSLVFokkerPlanckFdmParams(
        greensAlgorithm=ql.FdmHestonGreensFctAlgorithm.SemiAnalytical,
        trafoType=ql.FdmSquareRootFwdOpTransformationType.Power,
    )
    assert params.greensAlgorithm == ql.FdmHestonGreensFctAlgorithm.SemiAnalytical
    assert params.trafoType == ql.FdmSquareRootFwdOpTransformationType.Power


def test_fokkerplanckfdmparams_schemedesc():
    """HestonSLVFokkerPlanckFdmParams accepts FdmSchemeDesc."""
    params = ql.HestonSLVFokkerPlanckFdmParams(
        schemeDesc=ql.FdmSchemeDesc.Hundsdorfer(),
    )
    assert params.schemeDesc.type == ql.FdmSchemeType.Hundsdorfer


# =============================================================================
# FdmHestonGreensFctAlgorithm & FdmSquareRootFwdOpTransformationType enums
# =============================================================================


def test_fdmhestongreensfctalgorithm_values():
    """FdmHestonGreensFctAlgorithm enum has all expected values."""
    assert ql.FdmHestonGreensFctAlgorithm.ZeroCorrelation is not None
    assert ql.FdmHestonGreensFctAlgorithm.Gaussian is not None
    assert ql.FdmHestonGreensFctAlgorithm.SemiAnalytical is not None


def test_fdmsquarerootfwdoptransformationtype_values():
    """FdmSquareRootFwdOpTransformationType enum has all expected values."""
    assert ql.FdmSquareRootFwdOpTransformationType.Plain is not None
    assert ql.FdmSquareRootFwdOpTransformationType.Power is not None
    assert ql.FdmSquareRootFwdOpTransformationType.Log is not None


# =============================================================================
# HestonSLVMCModel
# =============================================================================


@pytest.fixture()
def slv_model_env():
    today = ql.Date(15, 1, 2026)
    ql.Settings.instance().evaluationDate = today
    dc = ql.Actual365Fixed()
    risk_free = ql.FlatForward(today, 0.05, dc)
    dividend = ql.FlatForward(today, 0.02, dc)
    spot = ql.SimpleQuote(100.0)
    heston_process = ql.HestonProcess(
        risk_free, dividend, spot,
        v0=0.04, kappa=1.0, theta=0.04, sigma=0.5, rho=-0.7,
    )
    heston_model = ql.HestonModel(heston_process)
    local_vol = ql.LocalConstantVol(today, 0.20, dc)
    end_date = today + ql.Period(1, ql.Years)
    return {
        "today": today,
        "heston_model": heston_model,
        "local_vol": local_vol,
        "end_date": end_date,
    }


def test_hestonslvmcmodel_construction(slv_model_env):
    """HestonSLVMCModel can be constructed with hidden handles."""
    env = slv_model_env
    bgf = ql.MTBrownianGeneratorFactory(42)
    model = ql.HestonSLVMCModel(
        env["local_vol"], env["heston_model"], bgf, env["end_date"],
        timeStepsPerYear=100, nBins=51, calibrationPaths=1024,
    )
    assert model is not None


def test_hestonslvmcmodel_leverage_function(slv_model_env):
    """HestonSLVMCModel computes leverage function."""
    env = slv_model_env
    bgf = ql.MTBrownianGeneratorFactory(42)
    model = ql.HestonSLVMCModel(
        env["local_vol"], env["heston_model"], bgf, env["end_date"],
        timeStepsPerYear=100, nBins=51, calibrationPaths=1024,
    )
    lev = model.leverageFunction()
    assert lev is not None


def test_hestonslvmcmodel_heston_process(slv_model_env):
    """HestonSLVMCModel returns the underlying Heston process."""
    env = slv_model_env
    bgf = ql.MTBrownianGeneratorFactory(42)
    model = ql.HestonSLVMCModel(
        env["local_vol"], env["heston_model"], bgf, env["end_date"],
        timeStepsPerYear=100, nBins=51, calibrationPaths=1024,
    )
    proc = model.hestonProcess()
    assert proc is not None
    assert isinstance(proc, ql.HestonProcess)


def test_hestonslvmcmodel_local_vol(slv_model_env):
    """HestonSLVMCModel returns the local vol surface."""
    env = slv_model_env
    bgf = ql.MTBrownianGeneratorFactory(42)
    model = ql.HestonSLVMCModel(
        env["local_vol"], env["heston_model"], bgf, env["end_date"],
        timeStepsPerYear=100, nBins=51, calibrationPaths=1024,
    )
    lv = model.localVol()
    assert lv is not None


def test_hestonslvmcmodel_handle_constructor(slv_model_env):
    """HestonSLVMCModel works with explicit Handle constructors."""
    env = slv_model_env
    bgf = ql.MTBrownianGeneratorFactory(42)
    model = ql.HestonSLVMCModel(
        ql.LocalVolTermStructureHandle(env["local_vol"]),
        ql.HestonModelHandle(env["heston_model"]),
        bgf, env["end_date"],
        timeStepsPerYear=100, nBins=51, calibrationPaths=1024,
    )
    assert model.leverageFunction() is not None


# =============================================================================
# HestonSLVFDMModel
# =============================================================================


def test_hestonslvfdmmodel_construction(slv_model_env):
    """HestonSLVFDMModel can be constructed with hidden handles."""
    env = slv_model_env
    params = ql.HestonSLVFokkerPlanckFdmParams(
        xGrid=51, vGrid=51,
        tMaxStepsPerYear=100, tMinStepsPerYear=10,
    )
    model = ql.HestonSLVFDMModel(
        env["local_vol"], env["heston_model"],
        env["end_date"], params,
    )
    assert model is not None


def test_hestonslvfdmmodel_leverage_function(slv_model_env):
    """HestonSLVFDMModel computes leverage function."""
    env = slv_model_env
    params = ql.HestonSLVFokkerPlanckFdmParams(
        xGrid=51, vGrid=51,
        tMaxStepsPerYear=100, tMinStepsPerYear=10,
    )
    model = ql.HestonSLVFDMModel(
        env["local_vol"], env["heston_model"],
        env["end_date"], params,
    )
    lev = model.leverageFunction()
    assert lev is not None


def test_hestonslvfdmmodel_heston_process(slv_model_env):
    """HestonSLVFDMModel returns the underlying Heston process."""
    env = slv_model_env
    params = ql.HestonSLVFokkerPlanckFdmParams(
        xGrid=51, vGrid=51,
        tMaxStepsPerYear=100, tMinStepsPerYear=10,
    )
    model = ql.HestonSLVFDMModel(
        env["local_vol"], env["heston_model"],
        env["end_date"], params,
    )
    proc = model.hestonProcess()
    assert proc is not None
    assert isinstance(proc, ql.HestonProcess)


def test_hestonslvfdmmodel_handle_constructor(slv_model_env):
    """HestonSLVFDMModel works with explicit Handle constructors."""
    env = slv_model_env
    params = ql.HestonSLVFokkerPlanckFdmParams(
        xGrid=51, vGrid=51,
        tMaxStepsPerYear=100, tMinStepsPerYear=10,
    )
    model = ql.HestonSLVFDMModel(
        ql.LocalVolTermStructureHandle(env["local_vol"]),
        ql.HestonModelHandle(env["heston_model"]),
        env["end_date"], params,
    )
    assert model.leverageFunction() is not None


# =============================================================================
# HestonSLV end-to-end pricing
# =============================================================================


@pytest.fixture()
def slv_pricing_env():
    today = ql.Date(15, 1, 2026)
    ql.Settings.instance().evaluationDate = today
    dc = ql.Actual365Fixed()
    risk_free = ql.FlatForward(today, 0.05, dc)
    dividend = ql.FlatForward(today, 0.02, dc)
    spot = ql.SimpleQuote(100.0)
    heston_process = ql.HestonProcess(
        risk_free, dividend, spot,
        v0=0.04, kappa=1.0, theta=0.04, sigma=0.5, rho=-0.7,
    )
    heston_model = ql.HestonModel(heston_process)
    local_vol = ql.LocalConstantVol(today, 0.20, dc)
    maturity_date = today + ql.Period(1, ql.Years)
    payoff = ql.PlainVanillaPayoff(ql.OptionType.Call, 100.0)
    exercise = ql.EuropeanExercise(maturity_date)
    option = ql.VanillaOption(payoff, exercise)
    return {
        "heston_model": heston_model,
        "local_vol": local_vol,
        "maturity_date": maturity_date,
        "option": option,
    }


def test_hestonslv_mc_pricing(slv_pricing_env):
    """Calibrate leverage via MC and price with FdHestonVanillaEngine."""
    env = slv_pricing_env
    bgf = ql.MTBrownianGeneratorFactory(42)
    slv = ql.HestonSLVMCModel(
        env["local_vol"], env["heston_model"], bgf,
        env["maturity_date"],
        timeStepsPerYear=100, nBins=51, calibrationPaths=4096,
    )
    lev = slv.leverageFunction()
    engine = ql.FdHestonVanillaEngine(
        env["heston_model"], 50, 101, 51,
        leverageFct=lev,
    )
    env["option"].setPricingEngine(engine)
    npv = env["option"].NPV()
    assert npv == pytest.approx(9.1983, rel=1e-2)


def test_hestonslv_fdm_pricing(slv_pricing_env):
    """Calibrate leverage via FDM and price with FdHestonVanillaEngine."""
    env = slv_pricing_env
    params = ql.HestonSLVFokkerPlanckFdmParams(
        xGrid=51, vGrid=51,
        tMaxStepsPerYear=100, tMinStepsPerYear=10,
    )
    slv = ql.HestonSLVFDMModel(
        env["local_vol"], env["heston_model"],
        env["maturity_date"], params,
    )
    lev = slv.leverageFunction()
    engine = ql.FdHestonVanillaEngine(
        env["heston_model"], 50, 101, 51,
        leverageFct=lev,
    )
    env["option"].setPricingEngine(engine)
    npv = env["option"].NPV()
    assert npv == pytest.approx(8.3575, rel=1e-2)
