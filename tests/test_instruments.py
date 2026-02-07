"""
Tests for instruments module.

Corresponds to src/instruments/*.cpp bindings.
"""

import pytest

import pyquantlib as ql
from pyquantlib.base import Payoff


# =============================================================================
# Payoff (ABC)
# =============================================================================


def test_payoff_abc_exists():
    """Test Payoff ABC is accessible."""
    assert hasattr(ql.base, 'Payoff')


def test_payoff_zombie():
    """Test direct instantiation creates zombie."""
    zombie = Payoff()

    with pytest.raises(RuntimeError, match="Tried to call pure virtual function"):
        zombie.name()


def test_payoff_custom_subclass():
    """Test Python subclass implementing Payoff."""

    class MyPayoff(Payoff):
        def __init__(self, strike):
            super().__init__()
            self._strike = strike

        def name(self):
            return "MyPayoff"

        def description(self):
            return f"Custom payoff with strike {self._strike}"

        def __call__(self, price):
            return max(price - self._strike, 0.0)

    payoff = MyPayoff(100.0)

    assert payoff.name() == "MyPayoff"
    assert "strike 100" in payoff.description()
    assert payoff(110.0) == 10.0
    assert payoff(90.0) == 0.0


def test_plainvanillapayoff_creation():
    """Test PlainVanillaPayoff creation."""
    call = ql.PlainVanillaPayoff(ql.OptionType.Call, 100.0)
    put = ql.PlainVanillaPayoff(ql.OptionType.Put, 100.0)

    assert call.optionType() == ql.OptionType.Call
    assert call.strike() == 100.0
    assert put.optionType() == ql.OptionType.Put
    assert put.strike() == 100.0


# =============================================================================
# Exercise
# =============================================================================


def test_europeanexercise_creation():
    """Test EuropeanExercise creation."""
    exercise_date = ql.Date(15, 6, 2025)
    exercise = ql.EuropeanExercise(exercise_date)

    assert isinstance(exercise, ql.EuropeanExercise)
    assert isinstance(exercise, ql.Exercise)
    assert len(exercise.dates()) == 1
    assert exercise.dates()[0] == exercise_date
    assert exercise.lastDate() == exercise_date


def test_americanexercise_creation():
    """Test AmericanExercise creation."""
    earliest_date = ql.Date(15, 2, 2025)
    latest_date = ql.Date(15, 8, 2025)
    exercise = ql.AmericanExercise(earliest_date, latest_date)

    assert isinstance(exercise, ql.AmericanExercise)
    assert exercise.dates() == [earliest_date, latest_date]
    assert exercise.lastDate() == latest_date


def test_bermudanexercise_creation():
    """Test BermudanExercise creation."""
    dates = [
        ql.Date(1, 3, 2025),
        ql.Date(1, 6, 2025),
        ql.Date(1, 9, 2025),
        ql.Date(1, 12, 2025)
    ]
    exercise = ql.BermudanExercise(dates)

    assert isinstance(exercise, ql.BermudanExercise)
    assert exercise.dates() == dates
    assert exercise.lastDate() == ql.Date(1, 12, 2025)


# =============================================================================
# Option types
# =============================================================================


def test_optiontype_enum():
    """Test OptionType enum values."""
    assert ql.OptionType.Call == ql.Call
    assert ql.OptionType.Put == ql.Put
    assert ql.Call != ql.Put


def test_option_abc_exists():
    """Test Option ABC is accessible."""
    assert hasattr(ql.base, 'Option')


def test_greeks_class():
    """Test Greeks class."""
    greeks = ql.Greeks()

    greeks.delta = 0.5
    greeks.gamma = 0.1
    greeks.theta = -0.02
    greeks.vega = 0.25
    greeks.rho = 0.03
    greeks.dividendRho = 0.01

    assert greeks.delta == 0.5
    assert greeks.gamma == 0.1
    assert greeks.theta == -0.02
    assert greeks.vega == 0.25
    assert greeks.rho == 0.03
    assert greeks.dividendRho == 0.01


def test_moregreeks_class():
    """Test MoreGreeks class."""
    more_greeks = ql.MoreGreeks()

    more_greeks.itmCashProbability = 0.6
    more_greeks.strikeSensitivity = -0.5

    assert more_greeks.itmCashProbability == 0.6
    assert more_greeks.strikeSensitivity == -0.5


# =============================================================================
# VanillaOption
# =============================================================================


@pytest.fixture
def option_market_env():
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


def test_vanillaoption_creation(option_market_env):
    """Test VanillaOption creation."""
    payoff = ql.PlainVanillaPayoff(ql.OptionType.Call, 100.0)
    exercise_date = option_market_env["today"] + ql.Period(1, ql.Years)
    exercise = ql.EuropeanExercise(exercise_date)

    option = ql.VanillaOption(payoff, exercise)
    assert option is not None


def test_vanillaoption_analytic_european_engine(option_market_env):
    """Test AnalyticEuropeanEngine pricing."""
    payoff = ql.PlainVanillaPayoff(ql.OptionType.Call, 100.0)
    exercise_date = option_market_env["today"] + ql.Period(1, ql.Years)
    exercise = ql.EuropeanExercise(exercise_date)

    option = ql.VanillaOption(payoff, exercise)
    engine = ql.AnalyticEuropeanEngine(option_market_env["process"])
    option.setPricingEngine(engine)

    # ATM call with 20% vol, 5% rate, 1Y maturity
    npv = option.NPV()
    assert npv > 0
    assert npv == pytest.approx(10.45, abs=0.1)


def test_vanillaoption_greeks(option_market_env):
    """Test Greeks calculation."""
    payoff = ql.PlainVanillaPayoff(ql.OptionType.Call, 100.0)
    exercise_date = option_market_env["today"] + ql.Period(1, ql.Years)
    exercise = ql.EuropeanExercise(exercise_date)

    option = ql.VanillaOption(payoff, exercise)
    engine = ql.AnalyticEuropeanEngine(option_market_env["process"])
    option.setPricingEngine(engine)

    # Check all Greeks are available
    assert 0 < option.delta() < 1
    assert option.gamma() > 0
    assert option.vega() > 0
    assert option.theta() < 0  # Time decay
    assert option.rho() > 0


def test_vanillaoption_analytic_engine_with_discount_curve():
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


def test_vanillaoption_put(option_market_env):
    """Test put option pricing."""
    payoff = ql.PlainVanillaPayoff(ql.OptionType.Put, 100.0)
    exercise_date = option_market_env["today"] + ql.Period(1, ql.Years)
    exercise = ql.EuropeanExercise(exercise_date)

    option = ql.VanillaOption(payoff, exercise)
    engine = ql.AnalyticEuropeanEngine(option_market_env["process"])
    option.setPricingEngine(engine)

    npv = option.NPV()
    assert npv > 0
    assert option.delta() < 0  # Put has negative delta


def test_vanillaoption_analytic_engine_hidden_discount_curve():
    """Test AnalyticEuropeanEngine with hidden handle discount curve."""
    today = ql.Date(26, 6, 2025)
    ql.Settings.instance().evaluationDate = today

    spot = ql.SimpleQuote(100.0)
    dc = ql.Actual365Fixed()
    cal = ql.TARGET()

    risk_free_ts = ql.FlatForward(today, 0.05, dc)
    dividend_ts = ql.FlatForward(today, 0.0, dc)
    vol_ts = ql.BlackConstantVol(today, cal, 0.20, dc)
    discount_ts = ql.FlatForward(today, 0.10, dc)

    process = ql.GeneralizedBlackScholesProcess(
        spot, dividend_ts, risk_free_ts, vol_ts
    )

    # Hidden handle for discount curve
    engine = ql.AnalyticEuropeanEngine(process, discount_ts)

    payoff = ql.PlainVanillaPayoff(ql.OptionType.Call, 100.0)
    exercise = ql.EuropeanExercise(today + ql.Period(1, ql.Years))
    option = ql.VanillaOption(payoff, exercise)
    option.setPricingEngine(engine)

    assert option.NPV() > 0


def test_vanillaoption_analytic_engine_hidden_vs_explicit_discount():
    """Compare hidden and explicit discount curve constructors."""
    today = ql.Date(26, 6, 2025)
    ql.Settings.instance().evaluationDate = today

    spot = ql.SimpleQuote(100.0)
    dc = ql.Actual365Fixed()
    cal = ql.TARGET()

    risk_free_ts = ql.FlatForward(today, 0.05, dc)
    dividend_ts = ql.FlatForward(today, 0.0, dc)
    vol_ts = ql.BlackConstantVol(today, cal, 0.20, dc)
    discount_ts = ql.FlatForward(today, 0.10, dc)

    process = ql.GeneralizedBlackScholesProcess(
        spot, dividend_ts, risk_free_ts, vol_ts
    )

    # Explicit handle
    engine_explicit = ql.AnalyticEuropeanEngine(
        process, ql.YieldTermStructureHandle(discount_ts)
    )

    # Hidden handle
    engine_hidden = ql.AnalyticEuropeanEngine(process, discount_ts)

    payoff = ql.PlainVanillaPayoff(ql.OptionType.Call, 100.0)
    exercise = ql.EuropeanExercise(today + ql.Period(1, ql.Years))

    option1 = ql.VanillaOption(payoff, exercise)
    option1.setPricingEngine(engine_explicit)

    option2 = ql.VanillaOption(payoff, exercise)
    option2.setPricingEngine(engine_hidden)

    assert option1.NPV() == pytest.approx(option2.NPV(), rel=1e-10)


# =============================================================================
# Swap
# =============================================================================


def test_swap_type_enum():
    """Test SwapType enum values."""
    assert ql.SwapType.Payer is not None
    assert ql.SwapType.Receiver is not None
    assert int(ql.SwapType.Payer) == 1
    assert int(ql.SwapType.Receiver) == -1


def test_swap_arguments():
    """Test SwapArguments class."""
    args = ql.SwapArguments()
    assert args is not None
    assert args.legs == []
    assert args.payer == []


def test_swap_results():
    """Test SwapResults class."""
    results = ql.SwapResults()
    assert results is not None
    results.reset()


def test_swap_engine_class():
    """Test Swap.engine base class exists."""
    assert hasattr(ql.Swap, "engine")


def test_swap_generic_engine_class():
    """Test SwapGenericEngine exists in base module."""
    assert hasattr(ql.base, "SwapGenericEngine")


def test_fixedvsfloatingswap_arguments():
    """Test FixedVsFloatingSwapArguments class."""
    args = ql.FixedVsFloatingSwapArguments()
    assert args is not None


def test_fixedvsfloatingswap_results():
    """Test FixedVsFloatingSwapResults class."""
    results = ql.FixedVsFloatingSwapResults()
    assert results is not None


def test_swap_construction_two_legs():
    """Test Swap construction from two legs."""
    today = ql.Date(15, ql.June, 2025)
    ql.Settings.instance().evaluationDate = today

    leg1 = [ql.SimpleCashFlow(100.0, today + ql.Period(1, ql.Years))]
    leg2 = [ql.SimpleCashFlow(105.0, today + ql.Period(1, ql.Years))]

    swap = ql.Swap(leg1, leg2)

    assert swap is not None
    assert swap.numberOfLegs() == 2
    assert not swap.isExpired()


def test_swap_construction_multi_leg():
    """Test Swap multi-leg construction."""
    today = ql.Date(15, ql.June, 2025)
    ql.Settings.instance().evaluationDate = today

    leg1 = [ql.SimpleCashFlow(100.0, today + ql.Period(1, ql.Years))]
    leg2 = [ql.SimpleCashFlow(50.0, today + ql.Period(1, ql.Years))]
    leg3 = [ql.SimpleCashFlow(50.0, today + ql.Period(1, ql.Years))]

    swap = ql.Swap([leg1, leg2, leg3], [True, False, False])

    assert swap.numberOfLegs() == 3
    assert swap.payer(0) is True
    assert swap.payer(1) is False
    assert swap.payer(2) is False


def test_swap_dates():
    """Test Swap date inspectors."""
    today = ql.Date(15, ql.June, 2025)
    ql.Settings.instance().evaluationDate = today

    date1 = today + ql.Period(6, ql.Months)
    date2 = today + ql.Period(1, ql.Years)

    leg1 = [
        ql.SimpleCashFlow(50.0, date1),
        ql.SimpleCashFlow(50.0, date2),
    ]
    leg2 = [
        ql.SimpleCashFlow(52.5, date1),
        ql.SimpleCashFlow(52.5, date2),
    ]

    swap = ql.Swap(leg1, leg2)

    assert swap.startDate() == date1
    assert swap.maturityDate() == date2


def test_swap_legs_accessor():
    """Test Swap legs accessor."""
    today = ql.Date(15, ql.June, 2025)
    ql.Settings.instance().evaluationDate = today

    leg1 = [ql.SimpleCashFlow(100.0, today + ql.Period(1, ql.Years))]
    leg2 = [ql.SimpleCashFlow(105.0, today + ql.Period(1, ql.Years))]

    swap = ql.Swap(leg1, leg2)

    legs = swap.legs()
    assert len(legs) == 2

    leg0 = swap.leg(0)
    assert len(leg0) == 1

    leg1_retrieved = swap.leg(1)
    assert len(leg1_retrieved) == 1


# =============================================================================
# VanillaSwap
# =============================================================================


@pytest.fixture
def swap_env():
    """Market environment for VanillaSwap tests."""
    today = ql.Date(15, ql.February, 2025)
    ql.Settings.instance().evaluationDate = today

    calendar = ql.TARGET()
    settlement = calendar.advance(today, ql.Period(2, ql.Days))

    # Yield curve
    dc = ql.Actual365Fixed()
    rate = 0.05
    flat_curve = ql.FlatForward(settlement, rate, dc)

    # Index
    euribor = ql.Euribor6M(flat_curve)

    # Schedules
    start = calendar.advance(settlement, ql.Period(1, ql.Years))
    maturity = calendar.advance(start, ql.Period(5, ql.Years))

    fixed_schedule = ql.Schedule(
        start, maturity,
        ql.Period(ql.Annual),
        calendar,
        ql.Unadjusted, ql.Unadjusted,
        ql.DateGeneration.Forward, False,
    )

    float_schedule = ql.Schedule(
        start, maturity,
        ql.Period(ql.Semiannual),
        calendar,
        ql.ModifiedFollowing, ql.ModifiedFollowing,
        ql.DateGeneration.Forward, False,
    )

    return {
        "calendar": calendar,
        "settlement": settlement,
        "flat_curve": flat_curve,
        "euribor": euribor,
        "fixed_schedule": fixed_schedule,
        "float_schedule": float_schedule,
        "fixed_dc": ql.Thirty360(ql.Thirty360.European),
        "float_dc": euribor.dayCounter(),
    }


def test_vanillaswap_construction(swap_env):
    """Test VanillaSwap construction."""
    swap = ql.VanillaSwap(
        ql.SwapType.Payer,
        1000000.0,
        swap_env["fixed_schedule"],
        0.05,
        swap_env["fixed_dc"],
        swap_env["float_schedule"],
        swap_env["euribor"],
        0.0,
        swap_env["float_dc"],
    )

    assert swap is not None
    assert swap.type() == ql.SwapType.Payer
    assert swap.nominal() == 1000000.0
    assert swap.fixedRate() == 0.05
    assert swap.spread() == 0.0


def test_vanillaswap_inspectors(swap_env):
    """Test VanillaSwap inspectors."""
    swap = ql.VanillaSwap(
        ql.SwapType.Receiver,
        1000000.0,
        swap_env["fixed_schedule"],
        0.04,
        swap_env["fixed_dc"],
        swap_env["float_schedule"],
        swap_env["euribor"],
        0.001,
        swap_env["float_dc"],
    )

    assert swap.type() == ql.SwapType.Receiver
    assert swap.fixedRate() == 0.04
    assert swap.spread() == 0.001
    assert len(swap.fixedLeg()) > 0
    assert len(swap.floatingLeg()) > 0


def test_vanillaswap_legs(swap_env):
    """Test VanillaSwap leg accessors."""
    swap = ql.VanillaSwap(
        ql.SwapType.Payer,
        1000000.0,
        swap_env["fixed_schedule"],
        0.05,
        swap_env["fixed_dc"],
        swap_env["float_schedule"],
        swap_env["euribor"],
        0.0,
        swap_env["float_dc"],
    )

    fixed_leg = swap.fixedLeg()
    floating_leg = swap.floatingLeg()

    # 5-year swap with annual fixed payments = 5 coupons
    assert len(fixed_leg) == 5
    # 5-year swap with semiannual float payments = 10 coupons
    assert len(floating_leg) == 10


def test_vanillaswap_pricing(swap_env):
    """Test VanillaSwap pricing with DiscountingSwapEngine."""
    swap = ql.VanillaSwap(
        ql.SwapType.Payer,
        1000000.0,
        swap_env["fixed_schedule"],
        0.05,
        swap_env["fixed_dc"],
        swap_env["float_schedule"],
        swap_env["euribor"],
        0.0,
        swap_env["float_dc"],
    )

    engine = ql.DiscountingSwapEngine(swap_env["flat_curve"])
    swap.setPricingEngine(engine)

    npv = swap.NPV()
    fair_rate = swap.fairRate()

    assert npv != 0  # Should have some value
    assert 0 < fair_rate < 0.2  # Reasonable rate range


def test_vanillaswap_fair_rate(swap_env):
    """Test that swap at fair rate has zero NPV."""
    swap = ql.VanillaSwap(
        ql.SwapType.Payer,
        1000000.0,
        swap_env["fixed_schedule"],
        0.05,  # dummy rate
        swap_env["fixed_dc"],
        swap_env["float_schedule"],
        swap_env["euribor"],
        0.0,
        swap_env["float_dc"],
    )

    engine = ql.DiscountingSwapEngine(swap_env["flat_curve"])
    swap.setPricingEngine(engine)

    fair_rate = swap.fairRate()

    # Create swap at fair rate
    fair_swap = ql.VanillaSwap(
        ql.SwapType.Payer,
        1000000.0,
        swap_env["fixed_schedule"],
        fair_rate,
        swap_env["fixed_dc"],
        swap_env["float_schedule"],
        swap_env["euribor"],
        0.0,
        swap_env["float_dc"],
    )
    fair_swap.setPricingEngine(engine)

    # NPV should be approximately zero
    assert abs(fair_swap.NPV()) < 1e-6


# =============================================================================
# Swaption
# =============================================================================


def test_swaption_settlementtype_enum():
    """Test SettlementType enum values."""
    assert ql.SettlementType.Physical is not None
    assert ql.SettlementType.Cash is not None


def test_swaption_settlementmethod_enum():
    """Test SettlementMethod enum values."""
    assert ql.SettlementMethod.PhysicalOTC is not None
    assert ql.SettlementMethod.PhysicalCleared is not None
    assert ql.SettlementMethod.CollateralizedCashPrice is not None
    assert ql.SettlementMethod.ParYieldCurve is not None


def test_swaption_pricetype_enum():
    """Test SwaptionPriceType enum values."""
    assert ql.SwaptionPriceType.Spot is not None
    assert ql.SwaptionPriceType.Forward is not None


def test_volatilitytype_enum():
    """Test VolatilityType enum values."""
    assert ql.VolatilityType.ShiftedLognormal is not None
    assert ql.VolatilityType.Normal is not None


def test_swaption_arguments():
    """Test SwaptionArguments class."""
    args = ql.SwaptionArguments()
    assert args is not None


def test_swaption_construction(swap_env):
    """Test Swaption construction."""
    swap = ql.VanillaSwap(
        ql.SwapType.Payer,
        1000000.0,
        swap_env["fixed_schedule"],
        0.05,
        swap_env["fixed_dc"],
        swap_env["float_schedule"],
        swap_env["euribor"],
        0.0,
        swap_env["float_dc"],
    )

    exercise_date = swap_env["fixed_schedule"].dates()[0]
    exercise = ql.EuropeanExercise(exercise_date)

    swaption = ql.Swaption(swap, exercise)

    assert swaption is not None
    assert swaption.settlementType() == ql.SettlementType.Physical
    assert swaption.type() == ql.SwapType.Payer


def test_swaption_with_settlement(swap_env):
    """Test Swaption with cash settlement."""
    swap = ql.VanillaSwap(
        ql.SwapType.Receiver,
        1000000.0,
        swap_env["fixed_schedule"],
        0.04,
        swap_env["fixed_dc"],
        swap_env["float_schedule"],
        swap_env["euribor"],
        0.0,
        swap_env["float_dc"],
    )

    exercise_date = swap_env["fixed_schedule"].dates()[0]
    exercise = ql.EuropeanExercise(exercise_date)

    swaption = ql.Swaption(
        swap, exercise,
        ql.SettlementType.Cash,
        ql.SettlementMethod.ParYieldCurve
    )

    assert swaption.settlementType() == ql.SettlementType.Cash
    assert swaption.settlementMethod() == ql.SettlementMethod.ParYieldCurve
    assert swaption.type() == ql.SwapType.Receiver


def test_swaption_underlying(swap_env):
    """Test Swaption underlying accessor."""
    swap = ql.VanillaSwap(
        ql.SwapType.Payer,
        1000000.0,
        swap_env["fixed_schedule"],
        0.05,
        swap_env["fixed_dc"],
        swap_env["float_schedule"],
        swap_env["euribor"],
        0.0,
        swap_env["float_dc"],
    )

    exercise_date = swap_env["fixed_schedule"].dates()[0]
    exercise = ql.EuropeanExercise(exercise_date)

    swaption = ql.Swaption(swap, exercise)

    underlying = swaption.underlying()
    assert underlying is not None
    assert underlying.fixedRate() == 0.05


def test_swaption_bermudan(swap_env):
    """Test Bermudan swaption construction."""
    swap = ql.VanillaSwap(
        ql.SwapType.Payer,
        1000000.0,
        swap_env["fixed_schedule"],
        0.05,
        swap_env["fixed_dc"],
        swap_env["float_schedule"],
        swap_env["euribor"],
        0.0,
        swap_env["float_dc"],
    )

    exercise_dates = list(swap_env["fixed_schedule"].dates())[:-1]  # Exclude maturity
    exercise = ql.BermudanExercise(exercise_dates)

    swaption = ql.Swaption(swap, exercise)

    assert swaption is not None
    assert not swaption.isExpired()


# =============================================================================
# Bond (base class)
# =============================================================================


@pytest.fixture(scope="module")
def bond_env():
    """Common data for bond base class tests."""
    original_date = ql.Settings.instance().evaluationDate
    today = ql.Date(15, ql.January, 2025)
    ql.Settings.instance().evaluationDate = today

    calendar = ql.TARGET()

    issue_date = ql.Date(15, ql.January, 2025)
    maturity_date = ql.Date(15, ql.January, 2030)

    schedule = ql.Schedule(
        issue_date, maturity_date,
        ql.Period(ql.Annual), calendar,
        ql.Unadjusted, ql.Unadjusted,
        ql.DateGeneration.Backward, False
    )

    yield {
        "today": today,
        "schedule": schedule,
    }

    ql.Settings.instance().evaluationDate = original_date


def test_bondpricetype_exists():
    """Test BondPriceType enum values exist."""
    assert hasattr(ql, "BondPriceType")
    assert ql.BondPriceType.Clean is not None
    assert ql.BondPriceType.Dirty is not None


def test_bondprice_construction():
    """Test BondPrice construction."""
    price = ql.BondPrice(99.5, ql.BondPriceType.Clean)
    assert price.amount() == pytest.approx(99.5)
    assert price.type() == ql.BondPriceType.Clean


def test_bond_exists():
    """Test Bond class exists."""
    assert hasattr(ql, "Bond")


def test_bond_is_tradable(bond_env):
    """Test Bond isTradable method."""
    bond = ql.FixedRateBond(
        2, 100.0, bond_env["schedule"], [0.05],
        ql.Thirty360(ql.Thirty360.BondBasis)
    )
    assert bond.isTradable() is True


def test_bond_is_expired(bond_env):
    """Test Bond isExpired method."""
    bond = ql.FixedRateBond(
        2, 100.0, bond_env["schedule"], [0.05],
        ql.Thirty360(ql.Thirty360.BondBasis)
    )
    assert bond.isExpired() is False


def test_bond_notionals(bond_env):
    """Test Bond notionals method."""
    bond = ql.FixedRateBond(
        2, 100.0, bond_env["schedule"], [0.05],
        ql.Thirty360(ql.Thirty360.BondBasis)
    )
    notionals = bond.notionals()
    assert len(notionals) > 0
    assert notionals[0] == pytest.approx(100.0)


def test_bond_settlement_value(bond_env):
    """Test Bond settlementValue from clean price."""
    bond = ql.FixedRateBond(
        2, 100.0, bond_env["schedule"], [0.05],
        ql.Thirty360(ql.Thirty360.BondBasis)
    )
    sv = bond.settlementValue(100.0)
    assert sv > 0.0
