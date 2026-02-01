"""Tests for ql/models/shortrate/*.hpp bindings."""

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
