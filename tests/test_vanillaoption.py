import pytest

import pyquantlib as ql


@pytest.fixture
def market_env():
    """Standard market environment for option pricing."""
    today = ql.Date(20, 2, 2025)
    ql.Settings.instance().evaluationDate = today

    spot = ql.SimpleQuote(100.0)
    rate = ql.SimpleQuote(0.05)
    vol = ql.SimpleQuote(0.20)

    dc = ql.Actual365Fixed()
    cal = ql.TARGET()

    risk_free_ts = ql.FlatForward(today, ql.QuoteHandle(rate), dc)
    dividend_ts = ql.FlatForward(today, 0.0, dc)
    vol_ts = ql.BlackConstantVol(today, cal, ql.QuoteHandle(vol), dc)

    process = ql.GeneralizedBlackScholesProcess(
        ql.QuoteHandle(spot),
        ql.YieldTermStructureHandle(dividend_ts),
        ql.YieldTermStructureHandle(risk_free_ts),
        ql.BlackVolTermStructureHandle(vol_ts),
    )

    return {"today": today, "process": process}


def test_plain_vanilla_payoff():
    """Test PlainVanillaPayoff creation."""
    call = ql.PlainVanillaPayoff(ql.OptionType.Call, 100.0)
    put = ql.PlainVanillaPayoff(ql.OptionType.Put, 100.0)

    assert call.optionType() == ql.OptionType.Call
    assert call.strike() == 100.0
    assert put.optionType() == ql.OptionType.Put
    assert put.strike() == 100.0


def test_vanilla_option_creation(market_env):
    """Test VanillaOption creation."""
    payoff = ql.PlainVanillaPayoff(ql.OptionType.Call, 100.0)
    exercise_date = market_env["today"] + ql.Period(1, ql.Years)
    exercise = ql.EuropeanExercise(exercise_date)

    option = ql.VanillaOption(payoff, exercise)
    assert option is not None


def test_analytic_european_engine(market_env):
    """Test AnalyticEuropeanEngine pricing."""
    payoff = ql.PlainVanillaPayoff(ql.OptionType.Call, 100.0)
    exercise_date = market_env["today"] + ql.Period(1, ql.Years)
    exercise = ql.EuropeanExercise(exercise_date)

    option = ql.VanillaOption(payoff, exercise)
    engine = ql.AnalyticEuropeanEngine(market_env["process"])
    option.setPricingEngine(engine)

    # ATM call with 20% vol, 5% rate, 1Y maturity
    npv = option.NPV()
    assert npv > 0
    assert npv == pytest.approx(10.45, abs=0.1)


def test_option_greeks(market_env):
    """Test Greeks calculation."""
    payoff = ql.PlainVanillaPayoff(ql.OptionType.Call, 100.0)
    exercise_date = market_env["today"] + ql.Period(1, ql.Years)
    exercise = ql.EuropeanExercise(exercise_date)

    option = ql.VanillaOption(payoff, exercise)
    engine = ql.AnalyticEuropeanEngine(market_env["process"])
    option.setPricingEngine(engine)

    # Check all Greeks are available
    assert 0 < option.delta() < 1
    assert option.gamma() > 0
    assert option.vega() > 0
    assert option.theta() < 0  # Time decay
    assert option.rho() > 0


def test_analytic_engine_with_discount_curve():
    """Test AnalyticEuropeanEngine with separate discount curve."""
    today = ql.Date(26, 6, 2025)
    ql.Settings.instance().evaluationDate = today

    spot = ql.SimpleQuote(100.0)
    process_rate = ql.SimpleQuote(0.05)
    discount_rate = ql.SimpleQuote(0.10)
    vol = ql.SimpleQuote(0.20)

    dc = ql.Actual365Fixed()
    cal = ql.TARGET()

    process_ts = ql.FlatForward(today, ql.QuoteHandle(process_rate), dc)
    discount_ts = ql.FlatForward(today, ql.QuoteHandle(discount_rate), dc)
    dividend_ts = ql.FlatForward(today, 0.0, dc)
    vol_ts = ql.BlackConstantVol(today, cal, ql.QuoteHandle(vol), dc)

    process = ql.GeneralizedBlackScholesProcess(
        ql.QuoteHandle(spot),
        ql.YieldTermStructureHandle(dividend_ts),
        ql.YieldTermStructureHandle(process_ts),
        ql.BlackVolTermStructureHandle(vol_ts),
    )

    payoff = ql.PlainVanillaPayoff(ql.OptionType.Call, 100.0)
    exercise_date = today + ql.Period(1, ql.Years)
    exercise = ql.EuropeanExercise(exercise_date)
    option = ql.VanillaOption(payoff, exercise)

    # Engine with separate discount curve
    engine = ql.AnalyticEuropeanEngine(
        process, ql.YieldTermStructureHandle(discount_ts)
    )
    option.setPricingEngine(engine)

    # Expected values from dev repo test
    assert option.NPV() == pytest.approx(9.9409, abs=1e-4)
    assert option.delta() == pytest.approx(0.6058, abs=1e-4)
    assert option.vega() == pytest.approx(35.6940, abs=1e-4)
    assert option.gamma() == pytest.approx(0.0178, abs=1e-4)
    assert option.theta() == pytest.approx(-5.6042, abs=1e-4)


def test_put_option(market_env):
    """Test put option pricing."""
    payoff = ql.PlainVanillaPayoff(ql.OptionType.Put, 100.0)
    exercise_date = market_env["today"] + ql.Period(1, ql.Years)
    exercise = ql.EuropeanExercise(exercise_date)

    option = ql.VanillaOption(payoff, exercise)
    engine = ql.AnalyticEuropeanEngine(market_env["process"])
    option.setPricingEngine(engine)

    npv = option.NPV()
    assert npv > 0
    assert option.delta() < 0  # Put has negative delta
