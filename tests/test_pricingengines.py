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


# =============================================================================
# ReplicatingVarianceSwapEngine
# =============================================================================


def test_replicating_variance_swap_engine_construction():
    """ReplicatingVarianceSwapEngine constructs and prices a VarianceSwap."""
    today = ql.Date(15, ql.January, 2025)
    ql.Settings.evaluationDate = today
    dc = ql.Actual365Fixed()
    calendar = ql.TARGET()

    spot = ql.SimpleQuote(100.0)
    r_ts = ql.FlatForward(today, ql.QuoteHandle(ql.SimpleQuote(0.05)), dc)
    q_ts = ql.FlatForward(today, ql.QuoteHandle(ql.SimpleQuote(0.02)), dc)
    vol_ts = ql.BlackConstantVol(
        today, calendar, ql.QuoteHandle(ql.SimpleQuote(0.20)), dc,
    )

    process = ql.BlackScholesMertonProcess(
        ql.QuoteHandle(spot),
        ql.YieldTermStructureHandle(q_ts),
        ql.YieldTermStructureHandle(r_ts),
        ql.BlackVolTermStructureHandle(vol_ts),
    )

    call_strikes = [float(x) for x in range(100, 150, 5)]
    put_strikes = [float(x) for x in range(55, 105, 5)]
    engine = ql.ReplicatingVarianceSwapEngine(process, 5.0, call_strikes, put_strikes)

    maturity = calendar.advance(today, ql.Period("1Y"))
    vs = ql.VarianceSwap(ql.PositionType.Long, 0.04, 10000.0, today, maturity)
    vs.setPricingEngine(engine)

    assert vs.NPV() == pytest.approx(-14.5142243643, rel=1e-4)
    assert vs.variance() == pytest.approx(0.0384741615, rel=1e-6)


def test_replicating_variance_swap_engine_is_pricing_engine():
    """ReplicatingVarianceSwapEngine inherits from PricingEngine."""
    today = ql.Date(15, ql.January, 2025)
    ql.Settings.evaluationDate = today
    dc = ql.Actual365Fixed()
    calendar = ql.TARGET()

    spot = ql.SimpleQuote(100.0)
    r_ts = ql.FlatForward(today, ql.QuoteHandle(ql.SimpleQuote(0.05)), dc)
    q_ts = ql.FlatForward(today, ql.QuoteHandle(ql.SimpleQuote(0.02)), dc)
    vol_ts = ql.BlackConstantVol(
        today, calendar, ql.QuoteHandle(ql.SimpleQuote(0.20)), dc,
    )

    process = ql.BlackScholesMertonProcess(
        ql.QuoteHandle(spot),
        ql.YieldTermStructureHandle(q_ts),
        ql.YieldTermStructureHandle(r_ts),
        ql.BlackVolTermStructureHandle(vol_ts),
    )

    call_strikes = [float(x) for x in range(100, 150, 5)]
    put_strikes = [float(x) for x in range(55, 105, 5)]
    engine = ql.ReplicatingVarianceSwapEngine(process, 5.0, call_strikes, put_strikes)
    assert isinstance(engine, ql.base.PricingEngine)


# =============================================================================
# BlackCalculator
# =============================================================================


def test_blackcalculator_call_value():
    """Test BlackCalculator call value with type/strike constructor."""
    bc = ql.BlackCalculator(ql.OptionType.Call, 100.0, 105.0, 0.20, 0.95)
    assert bc.value() == pytest.approx(10.360313797977716, rel=1e-10)


def test_blackcalculator_put_value():
    """Test BlackCalculator put value."""
    bc = ql.BlackCalculator(ql.OptionType.Put, 100.0, 105.0, 0.20, 0.95)
    assert bc.value() == pytest.approx(5.6103137979777165, rel=1e-10)


def test_blackcalculator_payoff_constructor():
    """Test BlackCalculator with payoff constructor."""
    payoff = ql.PlainVanillaPayoff(ql.OptionType.Call, 100.0)
    bc = ql.BlackCalculator(payoff, 105.0, 0.20, 0.95)
    assert bc.value() == pytest.approx(10.360313797977716, rel=1e-10)


def test_blackcalculator_greeks():
    """Test BlackCalculator Greeks."""
    bc = ql.BlackCalculator(ql.OptionType.Call, 100.0, 105.0, 0.20, 0.95)

    assert bc.deltaForward() == pytest.approx(0.6028304461173745, rel=1e-10)
    assert bc.delta(105.0) == pytest.approx(0.6028304461173745, rel=1e-10)
    assert bc.gammaForward() == pytest.approx(0.017010825407788567, rel=1e-10)
    assert bc.gamma(105.0) == pytest.approx(0.017010825407788567, rel=1e-10)
    assert bc.theta(105.0, 1.0) == pytest.approx(-3.219472376830307, rel=1e-10)
    assert bc.thetaPerDay(105.0, 1.0) == pytest.approx(-0.008820472265288513, rel=1e-10)
    assert bc.vega(1.0) == pytest.approx(37.5088700241738, rel=1e-10)
    assert bc.rho(1.0) == pytest.approx(52.93688304434661, rel=1e-10)
    assert bc.dividendRho(1.0) == pytest.approx(-63.297196842324325, rel=1e-10)


def test_blackcalculator_probabilities():
    """Test BlackCalculator ITM probabilities."""
    bc = ql.BlackCalculator(ql.OptionType.Call, 100.0, 105.0, 0.20, 0.95)

    assert bc.itmCashProbability() == pytest.approx(0.5572303478352276, rel=1e-10)
    assert bc.itmAssetProbability() == pytest.approx(0.6345583643340786, rel=1e-10)


def test_blackcalculator_strike_sensitivity():
    """Test BlackCalculator strike sensitivity."""
    bc = ql.BlackCalculator(ql.OptionType.Call, 100.0, 105.0, 0.20, 0.95)

    assert bc.strikeSensitivity() == pytest.approx(-0.5293688304434662, rel=1e-10)
    assert bc.alpha() == pytest.approx(0.6345583643340786, rel=1e-10)
    assert bc.beta() == pytest.approx(-0.5572303478352276, rel=1e-10)


def test_blackcalculator_put_call_parity():
    """Test put-call parity: C - P = discount * (F - K)."""
    call = ql.BlackCalculator(ql.OptionType.Call, 100.0, 105.0, 0.20, 0.95)
    put = ql.BlackCalculator(ql.OptionType.Put, 100.0, 105.0, 0.20, 0.95)

    expected = 0.95 * (105.0 - 100.0)
    assert call.value() - put.value() == pytest.approx(expected, rel=1e-10)


# =============================================================================
# BachelierCalculator
# =============================================================================


def test_bacheliercalculator_call_value():
    """Test BachelierCalculator call value."""
    bc = ql.BachelierCalculator(ql.OptionType.Call, 100.0, 105.0, 5.0, 0.95)
    assert bc.value() == pytest.approx(5.14574848529151, rel=1e-10)


def test_bacheliercalculator_put_value():
    """Test BachelierCalculator put value."""
    bc = ql.BachelierCalculator(ql.OptionType.Put, 100.0, 105.0, 5.0, 0.95)
    assert bc.value() == pytest.approx(0.3957484852915104, rel=1e-10)


def test_bacheliercalculator_greeks():
    """Test BachelierCalculator Greeks."""
    bc = ql.BachelierCalculator(ql.OptionType.Call, 100.0, 105.0, 5.0, 0.95)

    assert bc.deltaForward() == pytest.approx(0.7992775087651158, rel=1e-10)
    assert bc.delta(105.0) == pytest.approx(0.7992775087651158, rel=1e-10)
    assert bc.vega(1.0) == pytest.approx(0.22987218829318617, rel=1e-10)
    assert bc.theta(105.0, 1.0) == pytest.approx(-0.31073807883261556, rel=1e-10)


def test_bacheliercalculator_payoff_constructor():
    """Test BachelierCalculator with payoff constructor."""
    payoff = ql.PlainVanillaPayoff(ql.OptionType.Call, 100.0)
    bc = ql.BachelierCalculator(payoff, 105.0, 5.0, 0.95)
    assert bc.value() == pytest.approx(5.14574848529151, rel=1e-10)


def test_bacheliercalculator_put_call_parity():
    """Test Bachelier put-call parity: C - P = discount * (F - K)."""
    call = ql.BachelierCalculator(ql.OptionType.Call, 100.0, 105.0, 5.0, 0.95)
    put = ql.BachelierCalculator(ql.OptionType.Put, 100.0, 105.0, 5.0, 0.95)

    expected = 0.95 * (105.0 - 100.0)
    assert call.value() - put.value() == pytest.approx(expected, rel=1e-10)
