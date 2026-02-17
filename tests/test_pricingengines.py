"""
Tests for pricing engines module.

Corresponds to src/pricingengines/*.cpp bindings.
"""

import pytest

import pyquantlib as ql


# =============================================================================
# Black Formula
# =============================================================================


def test_black_formula_call():
    """blackFormula returns correct call price."""
    price = ql.blackFormula(ql.OptionType.Call, 100.0, 100.0, 0.2, 1.0)
    assert price == pytest.approx(7.965567455405804, rel=1e-10)


def test_black_formula_put():
    """blackFormula returns correct put price."""
    price = ql.blackFormula(ql.OptionType.Put, 100.0, 100.0, 0.2, 1.0)
    # ATM: call = put
    assert price == pytest.approx(7.965567455405804, rel=1e-10)


def test_black_formula_displacement():
    """blackFormula accepts displacement parameter."""
    price = ql.blackFormula(ql.OptionType.Call, 100.0, 100.0, 0.2, 1.0, 50.0)
    assert price == pytest.approx(11.948351183108684, rel=1e-10)


def test_black_implied_stddev():
    """blackFormulaImpliedStdDev returns correct value."""
    price = ql.blackFormula(ql.OptionType.Call, 100.0, 100.0, 0.2, 1.0)
    implied = ql.blackFormulaImpliedStdDev(ql.OptionType.Call, 100.0, 100.0, price, 1.0)
    assert implied == pytest.approx(0.2, rel=1e-10)


def test_black_implied_stddev_approximation():
    """blackFormulaImpliedStdDevApproximation returns correct value."""
    price = ql.blackFormula(ql.OptionType.Call, 100.0, 100.0, 0.2, 1.0)
    approx = ql.blackFormulaImpliedStdDevApproximation(
        ql.OptionType.Call, 100.0, 100.0, price, 1.0
    )
    assert approx == pytest.approx(0.199667166072007, rel=1e-10)


def test_black_stddev_derivative():
    """blackFormulaStdDevDerivative returns correct vega component."""
    vega = ql.blackFormulaStdDevDerivative(100.0, 100.0, 0.2)
    assert vega == pytest.approx(39.69525474770118, rel=1e-10)


def test_black_vol_derivative():
    """blackFormulaVolDerivative returns correct vega."""
    vega = ql.blackFormulaVolDerivative(100.0, 100.0, 0.2, 1.0)
    assert vega == pytest.approx(39.69525474770118, rel=1e-10)


def test_black_forward_derivative():
    """blackFormulaForwardDerivative returns value."""
    delta = ql.blackFormulaForwardDerivative(ql.OptionType.Call, 100.0, 100.0, 0.2)
    assert delta == pytest.approx(0.539827837277029, rel=1e-10)


def test_black_cash_itm_probability():
    """blackFormulaCashItmProbability returns correct value."""
    prob = ql.blackFormulaCashItmProbability(ql.OptionType.Call, 100.0, 100.0, 0.2)
    assert prob == pytest.approx(0.460172162722971, rel=1e-10)


def test_black_asset_itm_probability():
    """blackFormulaAssetItmProbability returns correct value."""
    prob = ql.blackFormulaAssetItmProbability(ql.OptionType.Call, 100.0, 100.0, 0.2)
    assert prob == pytest.approx(0.539827837277029, rel=1e-10)


def test_bachelier_formula():
    """bachelierBlackFormula returns correct price."""
    price = ql.bachelierBlackFormula(ql.OptionType.Call, 100.0, 100.0, 10.0)
    assert price == pytest.approx(3.989422804014327, rel=1e-10)


def test_bachelier_implied_vol():
    """bachelierBlackFormulaImpliedVol returns correct value."""
    price = ql.bachelierBlackFormula(ql.OptionType.Call, 100.0, 100.0, 10.0)
    implied = ql.bachelierBlackFormulaImpliedVol(
        ql.OptionType.Call, 100.0, 100.0, 1.0, price
    )
    assert implied == pytest.approx(10.0, rel=1e-10)


def test_bachelier_stddev_derivative():
    """bachelierBlackFormulaStdDevDerivative returns correct value."""
    vega = ql.bachelierBlackFormulaStdDevDerivative(100.0, 100.0, 10.0)
    assert vega == pytest.approx(0.3989422804014327, rel=1e-10)


# ---------------------------------------------------------------------------
# YoY inflation cap/floor engines
# ---------------------------------------------------------------------------


@pytest.fixture
def yoy_engine_env():
    """Common environment for YoY inflation engine tests."""
    today = ql.Date(15, ql.January, 2025)
    ql.Settings.evaluationDate = today
    calendar = ql.TARGET()
    dc = ql.Actual365Fixed()
    obs_lag = ql.Period(3, ql.Months)

    nominal_curve = ql.FlatForward(today, 0.03, dc)
    yts_handle = ql.YieldTermStructureHandle(nominal_curve)

    yoy_idx = ql.YoYInflationIndex(ql.USCPI())

    vol = ql.ConstantYoYOptionletVolatility(
        0.10, 2, calendar, ql.ModifiedFollowing, dc,
        obs_lag, ql.Monthly, False,
    )
    vol_handle = ql.YoYOptionletVolatilitySurfaceHandle(vol)

    class Env:
        pass

    env = Env()
    env.today = today
    env.calendar = calendar
    env.dc = dc
    env.obs_lag = obs_lag
    env.nominal_curve = nominal_curve
    env.yts_handle = yts_handle
    env.yoy_idx = yoy_idx
    env.vol = vol
    env.vol_handle = vol_handle
    return env


# --- YoYInflationBlackCapFloorEngine ---


def test_yoy_black_engine_handle_construction(yoy_engine_env):
    """YoYInflationBlackCapFloorEngine constructed with handles."""
    env = yoy_engine_env
    engine = ql.YoYInflationBlackCapFloorEngine(
        env.yoy_idx, env.vol_handle, env.yts_handle,
    )
    assert engine is not None


def test_yoy_black_engine_hidden_handle_construction(yoy_engine_env):
    """YoYInflationBlackCapFloorEngine constructed with raw shared_ptr args."""
    env = yoy_engine_env
    engine = ql.YoYInflationBlackCapFloorEngine(
        env.yoy_idx, env.vol, env.nominal_curve,
    )
    assert engine is not None


def test_yoy_black_engine_is_pricing_engine(yoy_engine_env):
    """YoYInflationBlackCapFloorEngine inherits from PricingEngine."""
    env = yoy_engine_env
    engine = ql.YoYInflationBlackCapFloorEngine(
        env.yoy_idx, env.vol_handle, env.yts_handle,
    )
    assert isinstance(engine, ql.base.PricingEngine)


# --- YoYInflationUnitDisplacedBlackCapFloorEngine ---


def test_yoy_unit_displaced_black_engine_handle_construction(yoy_engine_env):
    """YoYInflationUnitDisplacedBlackCapFloorEngine constructed with handles."""
    env = yoy_engine_env
    engine = ql.YoYInflationUnitDisplacedBlackCapFloorEngine(
        env.yoy_idx, env.vol_handle, env.yts_handle,
    )
    assert engine is not None


def test_yoy_unit_displaced_black_engine_hidden_handle_construction(yoy_engine_env):
    """YoYInflationUnitDisplacedBlackCapFloorEngine constructed with raw shared_ptr args."""
    env = yoy_engine_env
    engine = ql.YoYInflationUnitDisplacedBlackCapFloorEngine(
        env.yoy_idx, env.vol, env.nominal_curve,
    )
    assert engine is not None


def test_yoy_unit_displaced_black_engine_is_pricing_engine(yoy_engine_env):
    """YoYInflationUnitDisplacedBlackCapFloorEngine inherits from PricingEngine."""
    env = yoy_engine_env
    engine = ql.YoYInflationUnitDisplacedBlackCapFloorEngine(
        env.yoy_idx, env.vol_handle, env.yts_handle,
    )
    assert isinstance(engine, ql.base.PricingEngine)


# --- YoYInflationBachelierCapFloorEngine ---


def test_yoy_bachelier_engine_handle_construction(yoy_engine_env):
    """YoYInflationBachelierCapFloorEngine constructed with handles."""
    env = yoy_engine_env
    engine = ql.YoYInflationBachelierCapFloorEngine(
        env.yoy_idx, env.vol_handle, env.yts_handle,
    )
    assert engine is not None


def test_yoy_bachelier_engine_hidden_handle_construction(yoy_engine_env):
    """YoYInflationBachelierCapFloorEngine constructed with raw shared_ptr args."""
    env = yoy_engine_env
    engine = ql.YoYInflationBachelierCapFloorEngine(
        env.yoy_idx, env.vol, env.nominal_curve,
    )
    assert engine is not None


def test_yoy_bachelier_engine_is_pricing_engine(yoy_engine_env):
    """YoYInflationBachelierCapFloorEngine inherits from PricingEngine."""
    env = yoy_engine_env
    engine = ql.YoYInflationBachelierCapFloorEngine(
        env.yoy_idx, env.vol_handle, env.yts_handle,
    )
    assert isinstance(engine, ql.base.PricingEngine)
