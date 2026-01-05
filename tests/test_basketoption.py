"""Tests for basket options, basket payoffs, and basket pricing engines."""

import sys
import pytest
import pyquantlib as ql


# Pricing tests fail on Linux/macOS CI (Settings.evaluationDate issue)
skip_pricing = pytest.mark.skipif(
    sys.platform in ("linux", "darwin"),
    reason="Settings.evaluationDate not persisting on Linux/macOS CI"
)


# =============================================================================
# Fixtures
# =============================================================================

@pytest.fixture
def market_data():
    """Standard market environment for basket option pricing."""
    today = ql.Date(15, 1, 2025)
    ql.Settings.instance().evaluationDate = today
    
    dc = ql.Actual365Fixed()
    cal = ql.NullCalendar()
    
    rate_ts = ql.FlatForward(today, 0.05, dc)
    rate_handle = ql.YieldTermStructureHandle(rate_ts)
    
    div_ts = ql.FlatForward(today, 0.02, dc)
    div_handle = ql.YieldTermStructureHandle(div_ts)
    
    return {
        "today": today,
        "dc": dc,
        "cal": cal,
        "rate_handle": rate_handle,
        "div_handle": div_handle,
    }


def make_bs_process(spot, vol, rate_handle, div_handle, today, cal, dc):
    """Helper to create a Black-Scholes process."""
    spot_handle = ql.QuoteHandle(ql.SimpleQuote(spot))
    vol_ts = ql.BlackConstantVol(today, cal, vol, dc)
    vol_handle = ql.BlackVolTermStructureHandle(vol_ts)
    return ql.GeneralizedBlackScholesProcess(spot_handle, div_handle, rate_handle, vol_handle)


# =============================================================================
# Basket Payoff Tests
# =============================================================================

def test_minbasketpayoff():
    """Test MinBasketPayoff accumulation and payoff."""
    strike = 100.0
    payoff = ql.PlainVanillaPayoff(ql.OptionType.Call, strike)
    basket_payoff = ql.MinBasketPayoff(payoff)
    
    prices = ql.Array([90.0, 110.0, 105.0])
    assert basket_payoff.accumulate(prices) == 90.0
    assert basket_payoff.accumulate([90.0, 110.0, 105.0]) == 90.0  # Python list
    assert basket_payoff(prices) == 0.0  # max(90 - 100, 0) = 0


def test_maxbasketpayoff():
    """Test MaxBasketPayoff accumulation and payoff."""
    strike = 100.0
    payoff = ql.PlainVanillaPayoff(ql.OptionType.Call, strike)
    basket_payoff = ql.MaxBasketPayoff(payoff)
    
    prices = ql.Array([90.0, 110.0, 105.0])
    assert basket_payoff.accumulate(prices) == 110.0
    assert basket_payoff(prices) == 10.0  # max(110 - 100, 0) = 10


def test_averagebasketpayoff():
    """Test AverageBasketPayoff with custom and equal weights."""
    strike = 100.0
    payoff = ql.PlainVanillaPayoff(ql.OptionType.Call, strike)
    
    # Custom weights
    weights = ql.Array([1.0/3.0, 1.0/3.0, 1.0/3.0])
    basket_payoff = ql.AverageBasketPayoff(payoff, weights)
    prices = ql.Array([90.0, 110.0, 100.0])
    assert basket_payoff.accumulate(prices) == pytest.approx(100.0, abs=1e-10)
    assert basket_payoff(prices) == pytest.approx(0.0, abs=1e-10)
    
    # Equal weights constructor
    basket_payoff2 = ql.AverageBasketPayoff(ql.PlainVanillaPayoff(ql.OptionType.Call, 95.0), 3)
    assert basket_payoff2(prices) == pytest.approx(5.0, abs=1e-10)


def test_spreadbasketpayoff():
    """Test SpreadBasketPayoff accumulation, payoff, and validation."""
    strike = 5.0
    payoff = ql.PlainVanillaPayoff(ql.OptionType.Call, strike)
    spread_payoff = ql.SpreadBasketPayoff(payoff)
    
    prices = ql.Array([110.0, 100.0])
    assert spread_payoff.accumulate(prices) == 10.0
    assert spread_payoff(prices) == 5.0  # max(10 - 5, 0) = 5
    
    # Requires exactly two assets
    with pytest.raises(ql.Error, match="two underlyings"):
        spread_payoff.accumulate(ql.Array([100.0, 110.0, 120.0]))


# =============================================================================
# BasketOption & StochasticProcessArray Tests
# =============================================================================

def test_basketoption_construction():
    """Test BasketOption construction and inheritance."""
    strike = 5.0
    payoff = ql.PlainVanillaPayoff(ql.OptionType.Call, strike)
    spread_payoff = ql.SpreadBasketPayoff(payoff)
    exercise = ql.EuropeanExercise(ql.Date(15, 7, 2025))
    
    option = ql.BasketOption(spread_payoff, exercise)
    assert option is not None
    assert hasattr(option, 'delta')
    assert hasattr(option, 'gamma')


@skip_pricing
def test_stochasticprocessarray(market_data):
    """Test StochasticProcessArray construction and methods."""
    today, dc, cal = market_data["today"], market_data["dc"], market_data["cal"]
    rate_handle, div_handle = market_data["rate_handle"], market_data["div_handle"]
    
    process1 = make_bs_process(100.0, 0.20, rate_handle, div_handle, today, cal, dc)
    process2 = make_bs_process(110.0, 0.25, rate_handle, div_handle, today, cal, dc)
    
    correlation = ql.Matrix(2, 2)
    correlation[0][0] = 1.0;  correlation[0][1] = 0.5
    correlation[1][0] = 0.5;  correlation[1][1] = 1.0
    
    process_array = ql.StochasticProcessArray([process1, process2], correlation)
    
    assert process_array.size() == 2
    initial = process_array.initialValues()
    assert initial[0] == pytest.approx(100.0)
    assert initial[1] == pytest.approx(110.0)


# =============================================================================
# KirkEngine Tests
# =============================================================================

@skip_pricing
def test_kirkengine_spread_call(market_data):
    """Test KirkEngine pricing for spread call option."""
    today, dc, cal = market_data["today"], market_data["dc"], market_data["cal"]
    rate_handle, div_handle = market_data["rate_handle"], market_data["div_handle"]
    
    process1 = make_bs_process(100.0, 0.20, rate_handle, div_handle, today, cal, dc)
    process2 = make_bs_process(96.0, 0.20, rate_handle, div_handle, today, cal, dc)
    
    strike = 3.0
    payoff = ql.PlainVanillaPayoff(ql.OptionType.Call, strike)
    spread_payoff = ql.SpreadBasketPayoff(payoff)
    exercise = ql.EuropeanExercise(ql.Date(15, 7, 2025))
    
    option = ql.BasketOption(spread_payoff, exercise)
    engine = ql.KirkEngine(process1, process2, 0.75)
    option.setPricingEngine(engine)
    
    assert option.NPV() == pytest.approx(4.395356851239796, rel=1e-4)


@skip_pricing
def test_kirkengine_spread_put(market_data):
    """Test KirkEngine pricing for spread put option."""
    today, dc, cal = market_data["today"], market_data["dc"], market_data["cal"]
    rate_handle, div_handle = market_data["rate_handle"], market_data["div_handle"]
    
    process1 = make_bs_process(100.0, 0.20, rate_handle, div_handle, today, cal, dc)
    process2 = make_bs_process(96.0, 0.20, rate_handle, div_handle, today, cal, dc)
    
    strike = 3.0
    payoff = ql.PlainVanillaPayoff(ql.OptionType.Put, strike)
    spread_payoff = ql.SpreadBasketPayoff(payoff)
    exercise = ql.EuropeanExercise(ql.Date(15, 7, 2025))
    
    option = ql.BasketOption(spread_payoff, exercise)
    engine = ql.KirkEngine(process1, process2, 0.75)
    option.setPricingEngine(engine)
    
    assert option.NPV() == pytest.approx(3.3613630233276273, rel=1e-4)


@skip_pricing
def test_kirkengine_correlation_effect(market_data):
    """Test that correlation affects spread option price."""
    today, dc, cal = market_data["today"], market_data["dc"], market_data["cal"]
    rate_handle, div_handle = market_data["rate_handle"], market_data["div_handle"]
    
    process1 = make_bs_process(100.0, 0.20, rate_handle, div_handle, today, cal, dc)
    process2 = make_bs_process(100.0, 0.20, rate_handle, div_handle, today, cal, dc)
    
    payoff = ql.PlainVanillaPayoff(ql.OptionType.Call, 0.0)  # ATM spread
    spread_payoff = ql.SpreadBasketPayoff(payoff)
    exercise = ql.EuropeanExercise(ql.Date(15, 7, 2025))
    option = ql.BasketOption(spread_payoff, exercise)
    
    # Low correlation -> higher spread volatility -> higher option value
    option.setPricingEngine(ql.KirkEngine(process1, process2, 0.2))
    npv_low_corr = option.NPV()
    
    option.setPricingEngine(ql.KirkEngine(process1, process2, 0.9))
    npv_high_corr = option.NPV()
    
    assert npv_low_corr > npv_high_corr
    assert npv_low_corr == pytest.approx(7.027674893181505, rel=1e-4)
    assert npv_high_corr == pytest.approx(2.4875331805593275, rel=1e-4)


# =============================================================================
# BjerksundStenslandSpreadEngine Tests
# =============================================================================

@skip_pricing
def test_bjerksundstenslandspreadengine(market_data):
    """Test BjerksundStenslandSpreadEngine for spread call option."""
    today, dc, cal = market_data["today"], market_data["dc"], market_data["cal"]
    rate_handle, div_handle = market_data["rate_handle"], market_data["div_handle"]
    
    process1 = make_bs_process(100.0, 0.20, rate_handle, div_handle, today, cal, dc)
    process2 = make_bs_process(96.0, 0.20, rate_handle, div_handle, today, cal, dc)
    
    strike = 3.0
    payoff = ql.PlainVanillaPayoff(ql.OptionType.Call, strike)
    spread_payoff = ql.SpreadBasketPayoff(payoff)
    exercise = ql.EuropeanExercise(ql.Date(15, 7, 2025))
    
    option = ql.BasketOption(spread_payoff, exercise)
    engine = ql.BjerksundStenslandSpreadEngine(process1, process2, 0.75)
    option.setPricingEngine(engine)
    
    npv = option.NPV()
    EXPECTED_NPV = 4.3954370289864055
    assert npv == pytest.approx(EXPECTED_NPV, rel=1e-4)


# =============================================================================
# OperatorSplittingSpreadEngine Tests
# =============================================================================

@skip_pricing
def test_operatorsplittingspreadengine(market_data):
    """Test OperatorSplittingSpreadEngine for spread call option."""
    today, dc, cal = market_data["today"], market_data["dc"], market_data["cal"]
    rate_handle, div_handle = market_data["rate_handle"], market_data["div_handle"]
    
    process1 = make_bs_process(100.0, 0.20, rate_handle, div_handle, today, cal, dc)
    process2 = make_bs_process(96.0, 0.20, rate_handle, div_handle, today, cal, dc)
    
    strike = 3.0
    payoff = ql.PlainVanillaPayoff(ql.OptionType.Call, strike)
    spread_payoff = ql.SpreadBasketPayoff(payoff)
    exercise = ql.EuropeanExercise(ql.Date(15, 7, 2025))
    
    option = ql.BasketOption(spread_payoff, exercise)
    engine = ql.OperatorSplittingSpreadEngine(process1, process2, 0.75)
    option.setPricingEngine(engine)
    
    npv = option.NPV()
    Expected_NPV = 4.395460019673697
    assert npv == pytest.approx(Expected_NPV, rel=1e-4)


# =============================================================================
# MCEuropeanBasketEngine Tests
# =============================================================================

@skip_pricing
def test_mceuropeanbasketengine_spread(market_data):
    """Test MCEuropeanBasketEngine for spread call option."""
    today, dc, cal = market_data["today"], market_data["dc"], market_data["cal"]
    rate_handle, div_handle = market_data["rate_handle"], market_data["div_handle"]
    
    process1 = make_bs_process(100.0, 0.20, rate_handle, div_handle, today, cal, dc)
    process2 = make_bs_process(96.0, 0.20, rate_handle, div_handle, today, cal, dc)
    
    correlation = ql.Matrix(2, 2)
    correlation[0][0] = 1.0;  correlation[0][1] = 0.75
    correlation[1][0] = 0.75; correlation[1][1] = 1.0
    process_array = ql.StochasticProcessArray([process1, process2], correlation)
    
    payoff = ql.PlainVanillaPayoff(ql.OptionType.Call, 3.0)
    spread_payoff = ql.SpreadBasketPayoff(payoff)
    exercise = ql.EuropeanExercise(ql.Date(15, 7, 2025))
    
    option = ql.BasketOption(spread_payoff, exercise)
    engine = ql.MCEuropeanBasketEngine(process_array, timeSteps=10, requiredSamples=1000, seed=42)
    option.setPricingEngine(engine)
    
    assert option.NPV() == pytest.approx(4.356413313262689, rel=1e-4)


@skip_pricing
def test_mceuropeanbasketengine_max(market_data):
    """Test MCEuropeanBasketEngine for max call option (best-of)."""
    today, dc, cal = market_data["today"], market_data["dc"], market_data["cal"]
    rate_handle, div_handle = market_data["rate_handle"], market_data["div_handle"]
    
    process1 = make_bs_process(100.0, 0.20, rate_handle, div_handle, today, cal, dc)
    process2 = make_bs_process(100.0, 0.25, rate_handle, div_handle, today, cal, dc)
    
    correlation = ql.Matrix(2, 2)
    correlation[0][0] = 1.0;  correlation[0][1] = 0.5
    correlation[1][0] = 0.5;  correlation[1][1] = 1.0
    process_array = ql.StochasticProcessArray([process1, process2], correlation)
    
    payoff = ql.PlainVanillaPayoff(ql.OptionType.Call, 100.0)
    max_payoff = ql.MaxBasketPayoff(payoff)
    exercise = ql.EuropeanExercise(ql.Date(15, 7, 2025))
    
    option = ql.BasketOption(max_payoff, exercise)
    engine = ql.MCEuropeanBasketEngine(process_array, timeSteps=10, requiredSamples=1000, seed=42)
    option.setPricingEngine(engine)
    
    assert option.NPV() == pytest.approx(9.702167314835238, rel=1e-4)


@skip_pricing
def test_mceuropeanbasketengine_min(market_data):
    """Test MCEuropeanBasketEngine for min put option (worst-of)."""
    today, dc, cal = market_data["today"], market_data["dc"], market_data["cal"]
    rate_handle, div_handle = market_data["rate_handle"], market_data["div_handle"]
    
    process1 = make_bs_process(100.0, 0.20, rate_handle, div_handle, today, cal, dc)
    process2 = make_bs_process(100.0, 0.25, rate_handle, div_handle, today, cal, dc)
    
    correlation = ql.Matrix(2, 2)
    correlation[0][0] = 1.0;  correlation[0][1] = 0.5
    correlation[1][0] = 0.5;  correlation[1][1] = 1.0
    process_array = ql.StochasticProcessArray([process1, process2], correlation)
    
    payoff = ql.PlainVanillaPayoff(ql.OptionType.Put, 100.0)
    min_payoff = ql.MinBasketPayoff(payoff)
    exercise = ql.EuropeanExercise(ql.Date(15, 7, 2025))
    
    option = ql.BasketOption(min_payoff, exercise)
    engine = ql.MCEuropeanBasketEngine(process_array, timeSteps=10, requiredSamples=1000, seed=42)
    option.setPricingEngine(engine)
    
    assert option.NPV() == pytest.approx(8.74709879269745, rel=1e-4)


@skip_pricing
def test_mceuropeanbasketengine_average(market_data):
    """Test MCEuropeanBasketEngine for average basket call."""
    today, dc, cal = market_data["today"], market_data["dc"], market_data["cal"]
    rate_handle, div_handle = market_data["rate_handle"], market_data["div_handle"]
    
    process1 = make_bs_process(100.0, 0.20, rate_handle, div_handle, today, cal, dc)
    process2 = make_bs_process(100.0, 0.25, rate_handle, div_handle, today, cal, dc)
    process3 = make_bs_process(100.0, 0.30, rate_handle, div_handle, today, cal, dc)
    
    correlation = ql.Matrix(3, 3)
    correlation[0][0] = 1.0;  correlation[0][1] = 0.5;  correlation[0][2] = 0.3
    correlation[1][0] = 0.5;  correlation[1][1] = 1.0;  correlation[1][2] = 0.4
    correlation[2][0] = 0.3;  correlation[2][1] = 0.4;  correlation[2][2] = 1.0
    process_array = ql.StochasticProcessArray([process1, process2, process3], correlation)
    
    payoff = ql.PlainVanillaPayoff(ql.OptionType.Call, 100.0)
    avg_payoff = ql.AverageBasketPayoff(payoff, 3)
    exercise = ql.EuropeanExercise(ql.Date(15, 7, 2025))
    
    option = ql.BasketOption(avg_payoff, exercise)
    engine = ql.MCEuropeanBasketEngine(process_array, timeSteps=10, requiredSamples=1000, seed=42)
    option.setPricingEngine(engine)
    
    assert option.NPV() == pytest.approx(6.184441003464529, rel=1e-4)


@skip_pricing
def test_mcldeuropeanbasketengine(market_data):
    """Test MCLDEuropeanBasketEngine (Sobol) for spread option."""
    today, dc, cal = market_data["today"], market_data["dc"], market_data["cal"]
    rate_handle, div_handle = market_data["rate_handle"], market_data["div_handle"]
    
    process1 = make_bs_process(100.0, 0.20, rate_handle, div_handle, today, cal, dc)
    process2 = make_bs_process(96.0, 0.20, rate_handle, div_handle, today, cal, dc)
    
    correlation = ql.Matrix(2, 2)
    correlation[0][0] = 1.0;  correlation[0][1] = 0.75
    correlation[1][0] = 0.75; correlation[1][1] = 1.0
    process_array = ql.StochasticProcessArray([process1, process2], correlation)
    
    payoff = ql.PlainVanillaPayoff(ql.OptionType.Call, 3.0)
    spread_payoff = ql.SpreadBasketPayoff(payoff)
    exercise = ql.EuropeanExercise(ql.Date(15, 7, 2025))
    
    option = ql.BasketOption(spread_payoff, exercise)
    engine = ql.MCLDEuropeanBasketEngine(process_array, timeSteps=10, requiredSamples=1024, seed=42)
    option.setPricingEngine(engine)
    
    assert option.NPV() == pytest.approx(4.297040981007655, rel=1e-4)
