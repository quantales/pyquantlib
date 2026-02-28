"""
Tests for short-rate models.

Corresponds to src/models/shortrate/*.cpp bindings.
"""

import pytest

import pyquantlib as ql


# --- ShortRateModel base classes ---


def test_shortratemodel_base_exists():
    """Test ShortRateModel base class exists."""
    assert hasattr(ql.base, "ShortRateModel")


def test_onefactormodel_base_exists():
    """Test OneFactorModel base class exists."""
    assert hasattr(ql.base, "OneFactorModel")


def test_onefactoraffinemodel_base_exists():
    """Test OneFactorAffineModel base class exists."""
    assert hasattr(ql.base, "OneFactorAffineModel")


def test_affinemodel_base_exists():
    """Test AffineModel base class exists."""
    assert hasattr(ql.base, "AffineModel")


def test_termstructureconsistentmodel_base_exists():
    """Test TermStructureConsistentModel base class exists."""
    assert hasattr(ql.base, "TermStructureConsistentModel")


def test_shortratemodel_handle():
    """Test ShortRateModelHandle construction."""
    handle = ql.ShortRateModelHandle()
    assert handle.empty()


def test_relinkable_shortratemodel_handle():
    """Test RelinkableShortRateModelHandle."""
    handle = ql.RelinkableShortRateModelHandle()
    assert handle.empty()


def test_shortratemodel_handle_with_model():
    """Test ShortRateModelHandle with a model."""
    model = ql.Vasicek()
    handle = ql.ShortRateModelHandle(model)
    assert not handle.empty()
    assert handle.currentLink() is not None


def test_relinkable_handle_linkto():
    """Test RelinkableShortRateModelHandle linkTo."""
    model1 = ql.Vasicek(r0=0.03)
    model2 = ql.Vasicek(r0=0.05)

    handle = ql.RelinkableShortRateModelHandle(model1)
    assert handle.currentLink().r0() == pytest.approx(0.03)

    handle.linkTo(model2)
    assert handle.currentLink().r0() == pytest.approx(0.05)


# --- Vasicek ---


def test_vasicek_construction():
    """Test Vasicek model construction with defaults."""
    model = ql.Vasicek()
    assert model is not None


def test_vasicek_construction_with_params():
    """Test Vasicek model construction with parameters."""
    model = ql.Vasicek(
        r0=0.05,
        a=0.3,
        b=0.03,
        sigma=0.01,
    )
    assert model is not None


def test_vasicek_parameter_accessors():
    """Test Vasicek parameter accessors."""
    r0 = 0.05
    a = 0.3
    b = 0.03
    sigma = 0.01

    model = ql.Vasicek(r0=r0, a=a, b=b, sigma=sigma)

    assert model.r0() == pytest.approx(r0)
    assert model.a() == pytest.approx(a)
    assert model.b() == pytest.approx(b)
    assert model.sigma() == pytest.approx(sigma)


def test_vasicek_params_method():
    """Test Vasicek params() returns calibratable parameters."""
    model = ql.Vasicek(r0=0.05, a=0.3, b=0.03, sigma=0.01)

    params = model.params()
    assert len(params) == 4


def test_vasicek_discount_bond_option():
    """Test Vasicek discountBondOption."""
    model = ql.Vasicek(r0=0.05, a=0.3, b=0.03, sigma=0.01)

    # Price a call option on a discount bond
    option_type = ql.OptionType.Call
    strike = 0.95
    maturity = 1.0
    bond_maturity = 2.0

    price = model.discountBondOption(option_type, strike, maturity, bond_maturity)
    assert price == pytest.approx(0.008224876865848496, rel=1e-5)


def test_vasicek_inheritance():
    """Test Vasicek inherits from expected base classes."""
    model = ql.Vasicek()
    assert isinstance(model, ql.base.OneFactorAffineModel)
    assert isinstance(model, ql.base.OneFactorModel)
    assert isinstance(model, ql.base.ShortRateModel)
    assert isinstance(model, ql.base.CalibratedModel)
    assert isinstance(model, ql.base.AffineModel)
    assert isinstance(model, ql.Observable)


# --- HullWhite ---


@pytest.fixture
def flat_curve():
    """Create flat yield term structure."""
    today = ql.Date(15, ql.January, 2026)
    ql.Settings.instance().evaluationDate = today
    rate = 0.05
    dc = ql.Actual365Fixed()
    return ql.FlatForward(today, rate, dc)


def test_hullwhite_construction(flat_curve):
    """Test HullWhite model construction with defaults."""
    model = ql.HullWhite(flat_curve)
    assert model is not None


def test_hullwhite_construction_with_params(flat_curve):
    """Test HullWhite model construction with parameters."""
    model = ql.HullWhite(flat_curve, a=0.1, sigma=0.01)
    assert model is not None


def test_hullwhite_inherits_vasicek(flat_curve):
    """Test HullWhite inherits Vasicek methods."""
    a = 0.15
    sigma = 0.02

    model = ql.HullWhite(flat_curve, a=a, sigma=sigma)

    # a() and sigma() come from Vasicek base
    assert model.a() == pytest.approx(a)
    assert model.sigma() == pytest.approx(sigma)


def test_hullwhite_inheritance(flat_curve):
    """Test HullWhite inherits from expected base classes."""
    model = ql.HullWhite(flat_curve)
    assert isinstance(model, ql.Vasicek)
    assert isinstance(model, ql.base.OneFactorAffineModel)
    assert isinstance(model, ql.base.AffineModel)
    assert isinstance(model, ql.base.TermStructureConsistentModel)
    assert isinstance(model, ql.Observable)


def test_hullwhite_discount_bond_option(flat_curve):
    """Test HullWhite discountBondOption."""
    model = ql.HullWhite(flat_curve, a=0.1, sigma=0.01)

    # Price a call option on a discount bond
    option_type = ql.OptionType.Call
    strike = 0.95
    maturity = 1.0
    bond_maturity = 2.0

    price = model.discountBondOption(option_type, strike, maturity, bond_maturity)
    assert price == pytest.approx(0.003886199071324481, rel=1e-5)


def test_hullwhite_convexity_bias():
    """Test HullWhite static convexityBias method."""
    future_price = 95.0
    t = 0.25
    T = 0.50
    sigma = 0.01
    a = 0.1

    bias = ql.HullWhite.convexityBias(future_price, t, T, sigma, a)
    assert bias == pytest.approx(9.068274594736803e-06, rel=1e-5)


def test_hullwhite_params(flat_curve):
    """Test HullWhite params() returns calibratable parameters."""
    model = ql.HullWhite(flat_curve, a=0.1, sigma=0.01)

    params = model.params()
    assert len(params) == 2


def test_hullwhite_term_structure(flat_curve):
    """Test HullWhite termStructure accessor."""
    model = ql.HullWhite(flat_curve, a=0.1, sigma=0.01)

    ts_handle = model.termStructure()
    assert not ts_handle.empty()


# --- BlackKarasinski ---


def test_blackkarasinski_construction(flat_curve):
    """Test BlackKarasinski model construction with defaults."""
    model = ql.BlackKarasinski(flat_curve)
    assert model is not None


def test_blackkarasinski_construction_with_params(flat_curve):
    """Test BlackKarasinski model construction with parameters."""
    model = ql.BlackKarasinski(flat_curve, a=0.1, sigma=0.1)
    assert model is not None


def test_blackkarasinski_params(flat_curve):
    """Test BlackKarasinski params() returns calibratable parameters."""
    model = ql.BlackKarasinski(flat_curve, a=0.1, sigma=0.1)

    params = model.params()
    # BlackKarasinski has 2 parameters: a (mean reversion) and sigma (volatility)
    assert len(params) == 2
    assert params[0] == pytest.approx(0.1)  # a
    assert params[1] == pytest.approx(0.1)  # sigma


def test_blackkarasinski_inheritance(flat_curve):
    """Test BlackKarasinski inherits from expected base classes."""
    model = ql.BlackKarasinski(flat_curve)
    assert isinstance(model, ql.base.OneFactorModel)
    assert isinstance(model, ql.base.ShortRateModel)
    assert isinstance(model, ql.base.CalibratedModel)
    assert isinstance(model, ql.base.TermStructureConsistentModel)
    assert isinstance(model, ql.Observable)


def test_blackkarasinski_term_structure(flat_curve):
    """Test BlackKarasinski termStructure accessor."""
    model = ql.BlackKarasinski(flat_curve, a=0.1, sigma=0.1)

    ts_handle = model.termStructure()
    assert not ts_handle.empty()


# --- TwoFactorModel base classes ---


def test_twofactormodel_base_exists():
    """Test TwoFactorModel base class exists."""
    assert hasattr(ql.base, "TwoFactorModel")


# --- G2 ---


def test_g2_construction(flat_curve):
    """Test G2 model construction with defaults."""
    model = ql.G2(flat_curve)
    assert model is not None


def test_g2_construction_with_params(flat_curve):
    """Test G2 model construction with parameters."""
    model = ql.G2(flat_curve, a=0.1, sigma=0.01, b=0.1, eta=0.01, rho=-0.75)
    assert model is not None


def test_g2_parameter_accessors(flat_curve):
    """Test G2 parameter accessors."""
    a, sigma, b, eta, rho = 0.1, 0.02, 0.15, 0.03, -0.5

    model = ql.G2(flat_curve, a=a, sigma=sigma, b=b, eta=eta, rho=rho)

    assert model.a() == pytest.approx(a)
    assert model.sigma() == pytest.approx(sigma)
    assert model.b() == pytest.approx(b)
    assert model.eta() == pytest.approx(eta)
    assert model.rho() == pytest.approx(rho)


def test_g2_params(flat_curve):
    """Test G2 params() returns calibratable parameters."""
    model = ql.G2(flat_curve, a=0.1, sigma=0.01, b=0.1, eta=0.01, rho=-0.75)

    params = model.params()
    # G2 has 5 parameters: a, sigma, b, eta, rho
    assert len(params) == 5


def test_g2_inheritance(flat_curve):
    """Test G2 inherits from expected base classes."""
    model = ql.G2(flat_curve)
    assert isinstance(model, ql.base.TwoFactorModel)
    assert isinstance(model, ql.base.ShortRateModel)
    assert isinstance(model, ql.base.CalibratedModel)
    assert isinstance(model, ql.base.AffineModel)
    assert isinstance(model, ql.base.TermStructureConsistentModel)
    assert isinstance(model, ql.Observable)


def test_g2_term_structure(flat_curve):
    """Test G2 termStructure accessor."""
    model = ql.G2(flat_curve, a=0.1, sigma=0.01, b=0.1, eta=0.01, rho=-0.75)

    ts_handle = model.termStructure()
    assert not ts_handle.empty()


def test_g2_discount_bond_option(flat_curve):
    """Test G2 discountBondOption."""
    model = ql.G2(flat_curve, a=0.1, sigma=0.01, b=0.1, eta=0.01, rho=-0.75)

    # Price a call option on a discount bond
    option_type = ql.OptionType.Call
    strike = 0.95
    maturity = 1.0
    bond_maturity = 2.0

    price = model.discountBondOption(option_type, strike, maturity, bond_maturity)
    assert price == pytest.approx(0.002942653462519429, rel=1e-5)


# --- CalibrationHelper base classes ---


def test_calibrationhelper_base_exists():
    """Test CalibrationHelper base class exists."""
    assert hasattr(ql.base, "CalibrationHelper")


def test_blackcalibrationhelper_base_exists():
    """Test BlackCalibrationHelper base class exists."""
    assert hasattr(ql.base, "BlackCalibrationHelper")


def test_calibration_error_type_enum():
    """Test CalibrationErrorType enum values."""
    assert hasattr(ql, "CalibrationErrorType")
    assert hasattr(ql.CalibrationErrorType, "RelativePriceError")
    assert hasattr(ql.CalibrationErrorType, "PriceError")
    assert hasattr(ql.CalibrationErrorType, "ImpliedVolError")


# --- RateAveraging ---


def test_rate_averaging_type_enum():
    """Test RateAveraging.Type enum values."""
    assert hasattr(ql, "RateAveraging")
    assert hasattr(ql.RateAveraging, "Type")
    assert hasattr(ql.RateAveraging.Type, "Simple")
    assert hasattr(ql.RateAveraging.Type, "Compound")


# --- SwaptionHelper ---


@pytest.fixture
def swaption_helper_env():
    """Environment for SwaptionHelper tests."""
    today = ql.Date(15, ql.January, 2026)
    ql.Settings.instance().evaluationDate = today

    dc = ql.Actual365Fixed()
    curve = ql.FlatForward(today, 0.05, dc)

    index = ql.Euribor6M(curve)
    vol = ql.SimpleQuote(0.20)

    return {
        "today": today,
        "curve": curve,
        "index": index,
        "vol": vol,
        "fixed_leg_tenor": ql.Period(1, ql.Years),
        "fixed_leg_dc": ql.Thirty360(ql.Thirty360.BondBasis),
        "floating_leg_dc": ql.Actual360(),
    }


def test_swaptionhelper_construction_period_period(swaption_helper_env):
    """Test SwaptionHelper construction with period maturity and length."""
    env = swaption_helper_env

    helper = ql.SwaptionHelper(
        maturity=ql.Period(1, ql.Years),
        length=ql.Period(5, ql.Years),
        volatility=env["vol"],
        index=env["index"],
        fixedLegTenor=env["fixed_leg_tenor"],
        fixedLegDayCounter=env["fixed_leg_dc"],
        floatingLegDayCounter=env["floating_leg_dc"],
        termStructure=env["curve"],
    )
    assert helper is not None


def test_swaptionhelper_construction_date_period(swaption_helper_env):
    """Test SwaptionHelper construction with exercise date and length."""
    env = swaption_helper_env

    exercise_date = env["today"] + ql.Period(1, ql.Years)

    helper = ql.SwaptionHelper(
        exerciseDate=exercise_date,
        length=ql.Period(5, ql.Years),
        volatility=env["vol"],
        index=env["index"],
        fixedLegTenor=env["fixed_leg_tenor"],
        fixedLegDayCounter=env["fixed_leg_dc"],
        floatingLegDayCounter=env["floating_leg_dc"],
        termStructure=env["curve"],
    )
    assert helper is not None


def test_swaptionhelper_construction_date_date(swaption_helper_env):
    """Test SwaptionHelper construction with exercise and end dates."""
    env = swaption_helper_env

    exercise_date = env["today"] + ql.Period(1, ql.Years)
    end_date = env["today"] + ql.Period(6, ql.Years)

    helper = ql.SwaptionHelper(
        exerciseDate=exercise_date,
        endDate=end_date,
        volatility=env["vol"],
        index=env["index"],
        fixedLegTenor=env["fixed_leg_tenor"],
        fixedLegDayCounter=env["fixed_leg_dc"],
        floatingLegDayCounter=env["floating_leg_dc"],
        termStructure=env["curve"],
    )
    assert helper is not None


def test_swaptionhelper_inheritance(swaption_helper_env):
    """Test SwaptionHelper inherits from expected base classes."""
    env = swaption_helper_env

    helper = ql.SwaptionHelper(
        maturity=ql.Period(1, ql.Years),
        length=ql.Period(5, ql.Years),
        volatility=env["vol"],
        index=env["index"],
        fixedLegTenor=env["fixed_leg_tenor"],
        fixedLegDayCounter=env["fixed_leg_dc"],
        floatingLegDayCounter=env["floating_leg_dc"],
        termStructure=env["curve"],
    )
    assert isinstance(helper, ql.base.BlackCalibrationHelper)
    assert isinstance(helper, ql.base.CalibrationHelper)


def test_swaptionhelper_underlying(swaption_helper_env):
    """Test SwaptionHelper underlying accessor."""
    env = swaption_helper_env

    helper = ql.SwaptionHelper(
        maturity=ql.Period(1, ql.Years),
        length=ql.Period(5, ql.Years),
        volatility=env["vol"],
        index=env["index"],
        fixedLegTenor=env["fixed_leg_tenor"],
        fixedLegDayCounter=env["fixed_leg_dc"],
        floatingLegDayCounter=env["floating_leg_dc"],
        termStructure=env["curve"],
    )
    swap = helper.underlying()
    assert swap is not None
    assert isinstance(swap, ql.FixedVsFloatingSwap)


def test_swaptionhelper_swaption(swaption_helper_env):
    """Test SwaptionHelper swaption accessor."""
    env = swaption_helper_env

    helper = ql.SwaptionHelper(
        maturity=ql.Period(1, ql.Years),
        length=ql.Period(5, ql.Years),
        volatility=env["vol"],
        index=env["index"],
        fixedLegTenor=env["fixed_leg_tenor"],
        fixedLegDayCounter=env["fixed_leg_dc"],
        floatingLegDayCounter=env["floating_leg_dc"],
        termStructure=env["curve"],
    )
    swaption = helper.swaption()
    assert swaption is not None
    assert isinstance(swaption, ql.Swaption)


# --- CapHelper ---


@pytest.fixture
def cap_helper_env():
    """Environment for CapHelper tests."""
    today = ql.Date(15, ql.January, 2026)
    ql.Settings.instance().evaluationDate = today

    dc = ql.Actual365Fixed()
    curve = ql.FlatForward(today, 0.05, dc)

    index = ql.Euribor6M(ql.YieldTermStructureHandle(curve))

    return {
        "today": today,
        "curve": curve,
        "index": index,
    }


def test_caphelper_construction_handle(cap_helper_env):
    """Test CapHelper construction with handles."""
    env = cap_helper_env

    helper = ql.CapHelper(
        length=ql.Period(5, ql.Years),
        volatility=ql.QuoteHandle(ql.SimpleQuote(0.20)),
        index=env["index"],
        fixedLegFrequency=ql.Annual,
        fixedLegDayCounter=ql.Thirty360(ql.Thirty360.BondBasis),
        includeFirstSwaplet=False,
        termStructure=ql.YieldTermStructureHandle(env["curve"]),
    )
    assert helper is not None
    assert isinstance(helper, ql.base.BlackCalibrationHelper)


def test_caphelper_construction_hidden_handle(cap_helper_env):
    """Test CapHelper construction with hidden handles."""
    env = cap_helper_env

    helper = ql.CapHelper(
        length=ql.Period(5, ql.Years),
        volatility=ql.SimpleQuote(0.20),
        index=env["index"],
        fixedLegFrequency=ql.Annual,
        fixedLegDayCounter=ql.Thirty360(ql.Thirty360.BondBasis),
        includeFirstSwaplet=False,
        termStructure=env["curve"],
    )
    assert helper is not None
    assert isinstance(helper, ql.base.BlackCalibrationHelper)


# =============================================================================
# CoxIngersollRoss
# =============================================================================


def test_cir_construction():
    """Test CoxIngersollRoss model construction."""
    cir = ql.CoxIngersollRoss(0.05, 0.1, 0.3, 0.1, True)
    assert cir is not None
    params = cir.params()
    assert params[0] == pytest.approx(0.1, rel=1e-10)  # theta
    assert params[1] == pytest.approx(0.3, rel=1e-10)  # k
    assert params[2] == pytest.approx(0.1, rel=1e-10)  # sigma
    assert params[3] == pytest.approx(0.05, rel=1e-10)  # r0


def test_cir_discount_bond_option():
    """Test CIR discount bond option pricing."""
    cir = ql.CoxIngersollRoss(0.05, 0.1, 0.3, 0.1, True)
    price = cir.discountBondOption(ql.OptionType.Call, 0.95, 1.0, 2.0)
    assert price == pytest.approx(0.0011559245, rel=1e-4)


def test_cir_default_params():
    """Test CIR with default parameters."""
    cir = ql.CoxIngersollRoss()
    params = cir.params()
    assert params[0] == pytest.approx(0.1, rel=1e-10)  # theta
    assert params[1] == pytest.approx(0.1, rel=1e-10)  # k
    assert params[2] == pytest.approx(0.1, rel=1e-10)  # sigma
    assert params[3] == pytest.approx(0.05, rel=1e-10)  # r0


# =============================================================================
# ExtendedCoxIngersollRoss
# =============================================================================


def test_extcir_construction(flat_curve):
    """Test ExtendedCoxIngersollRoss model construction."""
    ecir = ql.ExtendedCoxIngersollRoss(
        ql.YieldTermStructureHandle(flat_curve), 0.1, 0.3, 0.1, 0.05, True
    )
    assert ecir is not None


def test_extcir_discount_bond_option(flat_curve):
    """Test extended CIR discount bond option pricing."""
    ecir = ql.ExtendedCoxIngersollRoss(
        ql.YieldTermStructureHandle(flat_curve), 0.1, 0.3, 0.1, 0.05, True
    )
    price = ecir.discountBondOption(ql.OptionType.Call, 0.95, 1.0, 2.0)
    assert price == pytest.approx(0.0070466566, rel=1e-4)


def test_extcir_hidden_handle(flat_curve):
    """Test ExtendedCoxIngersollRoss with hidden handle constructor."""
    ecir = ql.ExtendedCoxIngersollRoss(flat_curve, 0.1, 0.3, 0.1, 0.05, True)
    price = ecir.discountBondOption(ql.OptionType.Call, 0.95, 1.0, 2.0)
    assert price == pytest.approx(0.0070466566, rel=1e-4)


# =============================================================================
# Gaussian1dModel ABC
# =============================================================================


def test_gaussian1dmodel_base_exists():
    """Test Gaussian1dModel base class exists."""
    assert hasattr(ql.base, "Gaussian1dModel")


def test_gaussian1dmodel_handle():
    """Test Gaussian1dModelHandle construction."""
    handle = ql.Gaussian1dModelHandle()
    assert handle.empty()


# =============================================================================
# Gsr
# =============================================================================


@pytest.fixture
def gsr_env():
    """Environment for GSR model tests."""
    import datetime

    ql.Settings.evaluationDate = datetime.date(2024, 1, 15)
    rf = ql.FlatForward(datetime.date(2024, 1, 15), 0.05, ql.Actual365Fixed())
    ts_handle = ql.YieldTermStructureHandle(rf)
    return {"rf": rf, "ts_handle": ts_handle}


def test_gsr_construction(gsr_env):
    """Test GSR model construction with constant reversion."""
    gsr = ql.Gsr(gsr_env["ts_handle"], [], [0.01], 0.1)
    assert gsr is not None


def test_gsr_accessors(gsr_env):
    """Test GSR model parameter accessors."""
    gsr = ql.Gsr(gsr_env["ts_handle"], [], [0.01], 0.1)
    assert list(gsr.reversion()) == pytest.approx([0.1])
    assert list(gsr.volatility()) == pytest.approx([0.01])
    assert gsr.numeraireTime() == pytest.approx(60.0)


def test_gsr_piecewise_reversion(gsr_env):
    """Test GSR model with piecewise mean reversion."""
    gsr = ql.Gsr(
        gsr_env["ts_handle"],
        [ql.Date(15, ql.January, 2026)],
        [0.01, 0.02],
        [0.1, 0.15],
    )
    assert list(gsr.reversion()) == pytest.approx([0.1, 0.15])
    assert list(gsr.volatility()) == pytest.approx([0.01, 0.02])


def test_gsr_hidden_handle(gsr_env):
    """Test GSR with hidden handle constructor."""
    gsr = ql.Gsr(gsr_env["rf"], [], [0.01], 0.1)
    assert list(gsr.reversion()) == pytest.approx([0.1])
    assert list(gsr.volatility()) == pytest.approx([0.01])


def test_gsr_fixed_reversions(gsr_env):
    """Test GSR FixedReversions calibration mask."""
    gsr = ql.Gsr(
        gsr_env["ts_handle"],
        [ql.Date(15, ql.January, 2026)],
        [0.01, 0.02],
        [0.1, 0.15],
    )
    mask = gsr.FixedReversions()
    # 2 reversions fixed (True), 2 volatilities free (False)
    assert mask == [True, True, False, False]


def test_gsr_fixed_volatilities(gsr_env):
    """Test GSR FixedVolatilities calibration mask."""
    gsr = ql.Gsr(
        gsr_env["ts_handle"],
        [ql.Date(15, ql.January, 2026)],
        [0.01, 0.02],
        [0.1, 0.15],
    )
    mask = gsr.FixedVolatilities()
    # 2 reversions free (False), 2 volatilities fixed (True)
    assert mask == [False, False, True, True]


def test_gsr_move_volatility(gsr_env):
    """Test GSR MoveVolatility calibration mask."""
    gsr = ql.Gsr(
        gsr_env["ts_handle"],
        [ql.Date(15, ql.January, 2026)],
        [0.01, 0.02],
        [0.1, 0.15],
    )
    mask = gsr.MoveVolatility(0)
    # Only vol[0] is free, rest fixed
    assert mask == [True, True, False, True]


def test_gsr_inheritance(gsr_env):
    """Test GSR inherits from expected base classes."""
    gsr = ql.Gsr(gsr_env["ts_handle"], [], [0.01], 0.1)
    assert isinstance(gsr, ql.base.Gaussian1dModel)
    assert isinstance(gsr, ql.base.CalibratedModel)
    assert isinstance(gsr, ql.base.TermStructureConsistentModel)
    assert isinstance(gsr, ql.Observable)


def test_gsr_numeraire(gsr_env):
    """Test GSR numeraire computation."""
    gsr = ql.Gsr(gsr_env["ts_handle"], [], [0.01], 0.1)
    num = gsr.numeraire(1.0)
    assert num == pytest.approx(0.0525761300444786, rel=1e-6)


def test_gsr_zerobond(gsr_env):
    """Test GSR zero-coupon bond price."""
    gsr = ql.Gsr(gsr_env["ts_handle"], [], [0.01], 0.1)
    zb = gsr.zerobond(2.0, 1.0)
    assert zb == pytest.approx(0.9520088963957148, rel=1e-6)


def test_gsr_ygrid(gsr_env):
    """Test GSR state variable grid generation."""
    gsr = ql.Gsr(gsr_env["ts_handle"], [], [0.01], 0.1)
    grid = gsr.yGrid(3.0, 5)
    assert len(grid) == 11
    assert grid[0] == pytest.approx(-3.0)
    assert grid[5] == pytest.approx(0.0)
    assert grid[10] == pytest.approx(3.0)


def test_gsr_zerobond_option(gsr_env):
    """Test GSR zero-coupon bond option pricing."""
    gsr = ql.Gsr(gsr_env["ts_handle"], [], [0.01], 0.1)
    expiry = ql.Date(15, ql.January, 2026)
    valueDate = ql.Date(17, ql.January, 2026)
    maturity = ql.Date(15, ql.January, 2030)
    price = gsr.zerobondOption(ql.OptionType.Call, expiry, valueDate, maturity, 0.85)
    assert price == pytest.approx(0.0033040135838971123, rel=1e-4)


def test_gsr_forward_rate(gsr_env):
    """Test GSR forward rate computation."""
    gsr = ql.Gsr(gsr_env["ts_handle"], [], [0.01], 0.1)
    euribor = ql.Euribor6M(gsr_env["ts_handle"])
    fixing = ql.Date(15, ql.July, 2025)
    rate = gsr.forwardRate(fixing, iborIdx=euribor)
    assert rate == pytest.approx(0.04994869902850878, rel=1e-6)


def test_gsr_static_polynomial_integral():
    """Test Gaussian1dModel static gaussianPolynomialIntegral."""
    result = ql.base.Gaussian1dModel.gaussianPolynomialIntegral(
        1.0, 0.0, 0.0, 0.0, 1.0, -1.0, 1.0
    )
    assert result == pytest.approx(0.7949921723951971, rel=1e-6)


def test_gsr_static_shifted_polynomial_integral():
    """Test Gaussian1dModel static gaussianShiftedPolynomialIntegral."""
    result = ql.base.Gaussian1dModel.gaussianShiftedPolynomialIntegral(
        1.0, 0.0, 0.0, 0.0, 1.0, 0.0, -1.0, 1.0
    )
    assert result == pytest.approx(0.7949921723951971, rel=1e-6)


# =============================================================================
# MarkovFunctional
# =============================================================================


@pytest.fixture
def mf_env():
    """Environment for MarkovFunctional model tests."""
    import datetime

    ql.Settings.evaluationDate = datetime.date(2024, 1, 15)
    rf = ql.FlatForward(datetime.date(2024, 1, 15), 0.05, ql.Actual365Fixed())
    ts_handle = ql.YieldTermStructureHandle(rf)

    swaptionVol = ql.ConstantSwaptionVolatility(
        datetime.date(2024, 1, 15),
        ql.TARGET(),
        ql.ModifiedFollowing,
        0.20,
        ql.Actual365Fixed(),
    )
    swaptionVolHandle = ql.SwaptionVolatilityStructureHandle(swaptionVol)
    swapIdx = ql.EuriborSwapIsdaFixA(ql.Period("5Y"), ts_handle)
    expiries = [ql.Date(15, ql.January, 2025)]
    tenors = [ql.Period("5Y")]

    return {
        "rf": rf,
        "ts_handle": ts_handle,
        "swaptionVolHandle": swaptionVolHandle,
        "swapIdx": swapIdx,
        "expiries": expiries,
        "tenors": tenors,
    }


def test_markovfunctional_model_settings_defaults():
    """Test MarkovFunctionalModelSettings default construction."""
    settings = ql.MarkovFunctionalModelSettings()
    assert settings.yGridPoints == 64
    assert settings.yStdDevs == pytest.approx(7.0)
    assert settings.gaussHermitePoints == 32


def test_markovfunctional_model_settings_builder():
    """Test MarkovFunctionalModelSettings builder pattern."""
    settings = (
        ql.MarkovFunctionalModelSettings()
        .withYGridPoints(128)
        .withYStdDevs(8.0)
        .withGaussHermitePoints(48)
    )
    assert settings.yGridPoints == 128
    assert settings.yStdDevs == pytest.approx(8.0)
    assert settings.gaussHermitePoints == 48


def test_markovfunctional_adjustments_enum():
    """Test MarkovFunctionalAdjustments enum values."""
    assert int(ql.MarkovFunctionalAdjustments.AdjustNone) == 0
    assert int(ql.MarkovFunctionalAdjustments.AdjustDigitals) == 1
    assert int(ql.MarkovFunctionalAdjustments.KahaleSmile) == 16
    assert int(ql.MarkovFunctionalAdjustments.SabrSmile) == 256


def test_markovfunctional_construction(mf_env):
    """Test MarkovFunctional model construction."""
    mf = ql.MarkovFunctional(
        mf_env["ts_handle"],
        0.01,
        [],
        [0.01],
        mf_env["swaptionVolHandle"],
        mf_env["expiries"],
        mf_env["tenors"],
        mf_env["swapIdx"],
    )
    assert mf is not None
    assert list(mf.volatility()) == pytest.approx([0.01])


def test_markovfunctional_hidden_handle(mf_env):
    """Test MarkovFunctional with hidden handle constructor."""
    mf = ql.MarkovFunctional(
        mf_env["rf"],
        0.01,
        [],
        [0.01],
        mf_env["swaptionVolHandle"],
        mf_env["expiries"],
        mf_env["tenors"],
        mf_env["swapIdx"],
    )
    assert mf is not None


def test_markovfunctional_inheritance(mf_env):
    """Test MarkovFunctional inherits from expected base classes."""
    mf = ql.MarkovFunctional(
        mf_env["ts_handle"],
        0.01,
        [],
        [0.01],
        mf_env["swaptionVolHandle"],
        mf_env["expiries"],
        mf_env["tenors"],
        mf_env["swapIdx"],
    )
    assert isinstance(mf, ql.base.Gaussian1dModel)
    assert isinstance(mf, ql.base.CalibratedModel)


def test_markovfunctional_model_outputs(mf_env):
    """Test MarkovFunctional modelOutputs diagnostics."""
    mf = ql.MarkovFunctional(
        mf_env["ts_handle"],
        0.01,
        [],
        [0.01],
        mf_env["swaptionVolHandle"],
        mf_env["expiries"],
        mf_env["tenors"],
        mf_env["swapIdx"],
    )
    outputs = mf.modelOutputs()
    assert outputs is not None
    assert len(outputs.expiries) > 0
