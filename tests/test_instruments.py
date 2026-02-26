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


def test_cashornothingpayoff():
    """Test CashOrNothingPayoff construction and evaluation."""
    payoff = ql.CashOrNothingPayoff(ql.OptionType.Call, 100.0, 10.0)
    assert payoff.optionType() == ql.OptionType.Call
    assert payoff.strike() == 100.0
    assert payoff.cashPayoff() == 10.0
    assert payoff(110.0) == 10.0
    assert payoff(90.0) == 0.0


def test_assetornothingpayoff():
    """Test AssetOrNothingPayoff construction and evaluation."""
    payoff = ql.AssetOrNothingPayoff(ql.OptionType.Put, 100.0)
    assert payoff.optionType() == ql.OptionType.Put
    assert payoff.strike() == 100.0
    assert payoff(90.0) == 90.0
    assert payoff(110.0) == 0.0


def test_gappayoff():
    """Test GapPayoff construction and evaluation."""
    payoff = ql.GapPayoff(ql.OptionType.Call, 100.0, 90.0)
    assert payoff.strike() == 100.0
    assert payoff.secondStrike() == 90.0
    # Call gap payoff at S=110: S - secondStrike = 110 - 90 = 20
    assert payoff(110.0) == 20.0
    assert payoff(90.0) == 0.0


def test_percentagestrikepayoff():
    """Test PercentageStrikePayoff construction and evaluation."""
    payoff = ql.PercentageStrikePayoff(ql.OptionType.Call, 1.1)
    assert payoff.optionType() == ql.OptionType.Call
    assert payoff.strike() == 1.1
    # Call at moneyness 1.1: max(S - 1.1*S, 0) = max(-0.1*S, 0) = 0 for S>0
    assert payoff(100.0) == 0.0
    # Put at moneyness 0.9: max(0.9*S - S, 0) = 0 for S>0
    put_payoff = ql.PercentageStrikePayoff(ql.OptionType.Put, 0.9)
    assert put_payoff(100.0) == 0.0


def test_superfundpayoff():
    """Test SuperFundPayoff construction and evaluation."""
    payoff = ql.SuperFundPayoff(90.0, 110.0)
    assert payoff.strike() == 90.0
    assert payoff.secondStrike() == 110.0
    # Between strikes: S/lowerStrike
    assert payoff(100.0) == pytest.approx(100.0 / 90.0)
    # Below lower strike: 0
    assert payoff(80.0) == 0.0
    # Above upper strike: 0
    assert payoff(120.0) == 0.0


def test_supersharepayoff():
    """Test SuperSharePayoff construction and evaluation."""
    payoff = ql.SuperSharePayoff(90.0, 110.0, 5.0)
    assert payoff.strike() == 90.0
    assert payoff.secondStrike() == 110.0
    assert payoff.cashPayoff() == 5.0
    # Between strikes: cashPayoff
    assert payoff(100.0) == 5.0
    # Outside strikes: 0
    assert payoff(80.0) == 0.0
    assert payoff(120.0) == 0.0


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
    assert npv == pytest.approx(10.4506, rel=1e-4)


def test_vanillaoption_greeks(option_market_env):
    """Test Greeks calculation."""
    payoff = ql.PlainVanillaPayoff(ql.OptionType.Call, 100.0)
    exercise_date = option_market_env["today"] + ql.Period(1, ql.Years)
    exercise = ql.EuropeanExercise(exercise_date)

    option = ql.VanillaOption(payoff, exercise)
    engine = ql.AnalyticEuropeanEngine(option_market_env["process"])
    option.setPricingEngine(engine)

    # Check all Greeks
    assert option.delta() == pytest.approx(0.6368, rel=1e-4)
    assert option.gamma() == pytest.approx(0.018762, rel=1e-4)
    assert option.vega() == pytest.approx(37.5240, rel=1e-4)
    assert option.theta() == pytest.approx(-6.4140, rel=1e-4)
    assert option.rho() == pytest.approx(53.2325, rel=1e-4)


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
    assert npv == pytest.approx(5.5735, rel=1e-4)
    assert option.delta() == pytest.approx(-0.3632, rel=1e-4)


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

    assert option.NPV() == pytest.approx(9.9409, rel=1e-4)


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

    assert npv == pytest.approx(5339.5428, rel=1e-4)
    assert fair_rate == pytest.approx(0.05130, rel=1e-4)


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
    assert sv == pytest.approx(100.0278, rel=1e-4)


# =============================================================================
# OvernightIndexedSwap
# =============================================================================


@pytest.fixture(scope="module")
def ois_setup():
    """Setup for OIS tests: curve, index, schedule."""
    today = ql.Date(15, ql.January, 2025)
    ql.Settings.evaluationDate = today

    curve = ql.FlatForward(today, 0.035, ql.Actual365Fixed())
    sofr = ql.Sofr(curve)

    schedule = ql.Schedule(
        ql.Date(17, ql.January, 2025),
        ql.Date(17, ql.January, 2026),
        ql.Period(3, ql.Months),
        ql.UnitedStates(ql.UnitedStates.GovernmentBond),
        ql.ModifiedFollowing,
        ql.ModifiedFollowing,
        ql.DateGeneration.Forward,
        False,
    )

    return {
        "today": today,
        "curve": curve,
        "sofr": sofr,
        "schedule": schedule,
    }


def test_overnightindexedswap_construction(ois_setup):
    """Test OvernightIndexedSwap single-schedule construction."""
    ois = ql.OvernightIndexedSwap(
        ql.SwapType.Receiver,
        1_000_000.0,
        ois_setup["schedule"],
        0.035,
        ql.Actual360(),
        ois_setup["sofr"],
    )
    assert ois is not None


def test_overnightindexedswap_two_schedules(ois_setup):
    """Test OvernightIndexedSwap with separate fixed and overnight schedules."""
    ois = ql.OvernightIndexedSwap(
        ql.SwapType.Payer,
        1_000_000.0,
        ois_setup["schedule"],
        0.035,
        ql.Actual360(),
        ois_setup["schedule"],
        ois_setup["sofr"],
    )
    assert ois is not None


def test_overnightindexedswap_overnight_index(ois_setup):
    """Test overnightIndex accessor."""
    ois = ql.OvernightIndexedSwap(
        ql.SwapType.Receiver,
        1_000_000.0,
        ois_setup["schedule"],
        0.035,
        ql.Actual360(),
        ois_setup["sofr"],
    )
    idx = ois.overnightIndex()
    assert idx is not None
    assert "SOFR" in idx.name()


def test_overnightindexedswap_averaging_method(ois_setup):
    """Test averagingMethod accessor."""
    ois = ql.OvernightIndexedSwap(
        ql.SwapType.Receiver,
        1_000_000.0,
        ois_setup["schedule"],
        0.035,
        ql.Actual360(),
        ois_setup["sofr"],
        averagingMethod=ql.RateAveraging.Type.Simple,
    )
    assert ois.averagingMethod() == ql.RateAveraging.Type.Simple


def test_overnightindexedswap_default_averaging(ois_setup):
    """Test that default averaging method is Compound."""
    ois = ql.OvernightIndexedSwap(
        ql.SwapType.Receiver,
        1_000_000.0,
        ois_setup["schedule"],
        0.035,
        ql.Actual360(),
        ois_setup["sofr"],
    )
    assert ois.averagingMethod() == ql.RateAveraging.Type.Compound


def test_overnightindexedswap_pricing(ois_setup):
    """Test OIS pricing with DiscountingSwapEngine."""
    ois = ql.OvernightIndexedSwap(
        ql.SwapType.Receiver,
        1_000_000.0,
        ois_setup["schedule"],
        0.035,
        ql.Actual360(),
        ois_setup["sofr"],
    )
    engine = ql.DiscountingSwapEngine(ois_setup["curve"])
    ois.setPricingEngine(engine)

    npv = ois.NPV()
    # With at-market rate ~= curve rate, NPV should be small but well-defined
    assert isinstance(npv, float)
    assert abs(npv) < 50_000  # reasonable bound for 1M notional

    fair_rate = ois.fairRate()
    assert fair_rate == pytest.approx(0.035, abs=0.005)


def test_overnightindexedswap_leg_npv(ois_setup):
    """Test fixed and overnight leg NPV accessors."""
    ois = ql.OvernightIndexedSwap(
        ql.SwapType.Receiver,
        1_000_000.0,
        ois_setup["schedule"],
        0.035,
        ql.Actual360(),
        ois_setup["sofr"],
    )
    engine = ql.DiscountingSwapEngine(ois_setup["curve"])
    ois.setPricingEngine(engine)

    fixed_npv = ois.fixedLegNPV()
    overnight_npv = ois.overnightLegNPV()
    assert isinstance(fixed_npv, float)
    assert isinstance(overnight_npv, float)
    # NPV = fixedLegNPV + overnightLegNPV (for receiver: +fixed -float)
    assert ois.NPV() == pytest.approx(fixed_npv + overnight_npv, abs=1e-6)


def test_overnightindexedswap_overnight_leg(ois_setup):
    """Test overnightLeg returns cash flows."""
    ois = ql.OvernightIndexedSwap(
        ql.SwapType.Receiver,
        1_000_000.0,
        ois_setup["schedule"],
        0.035,
        ql.Actual360(),
        ois_setup["sofr"],
    )
    leg = ois.overnightLeg()
    assert len(leg) > 0


# =============================================================================
# MakeOIS
# =============================================================================


def test_makeois_kwargs(ois_setup):
    """Test MakeOIS kwargs wrapper."""
    ois = ql.MakeOIS(
        ql.Period(1, ql.Years),
        ois_setup["sofr"],
        0.035,
    )
    assert ois.fixedRate() == pytest.approx(0.035)


def test_makeois_builder_chaining(ois_setup):
    """Test MakeOIS C++ builder chaining."""
    from pyquantlib._pyquantlib import MakeOIS as MakeOISBuilder
    engine = ql.DiscountingSwapEngine(ois_setup["curve"])
    ois = (
        MakeOISBuilder(ql.Period(1, ql.Years), ois_setup["sofr"], 0.035)
        .withNominal(2_000_000.0)
        .withPaymentLag(2)
        .withPricingEngine(engine)
        .ois()
    )
    assert ois.nominal() == pytest.approx(2_000_000.0)


def test_makeois_atm(ois_setup):
    """Test MakeOIS with no fixed rate (ATM)."""
    ois = ql.MakeOIS(ql.Period(1, ql.Years), ois_setup["sofr"])
    assert isinstance(ois, ql.OvernightIndexedSwap)


def test_makeois_kwargs_nominal(ois_setup):
    """Test MakeOIS with nominal kwarg."""
    ois = ql.MakeOIS(
        ql.Period(1, ql.Years), ois_setup["sofr"], 0.035,
        nominal=5_000_000.0,
    )
    assert ois.nominal() == pytest.approx(5_000_000.0)


def test_makeois_kwargs_swap_type(ois_setup):
    """Test MakeOIS with swapType kwarg."""
    ois = ql.MakeOIS(
        ql.Period(1, ql.Years), ois_setup["sofr"], 0.035,
        swapType=ql.SwapType.Receiver,
    )
    assert ois.type() == ql.SwapType.Receiver


def test_makeois_kwargs_receive_fixed(ois_setup):
    """Test MakeOIS with receiveFixed kwarg."""
    ois = ql.MakeOIS(
        ql.Period(1, ql.Years), ois_setup["sofr"], 0.035,
        receiveFixed=True,
    )
    assert ois.type() == ql.SwapType.Receiver


def test_makeois_kwargs_pricing_engine(ois_setup):
    """Test MakeOIS with pricingEngine kwarg."""
    engine = ql.DiscountingSwapEngine(ois_setup["curve"])
    ois = ql.MakeOIS(
        ql.Period(1, ql.Years), ois_setup["sofr"], 0.035,
        pricingEngine=engine,
    )
    assert isinstance(ois.NPV(), float)


def test_makeois_kwargs_multiple(ois_setup):
    """Test MakeOIS with multiple kwargs."""
    engine = ql.DiscountingSwapEngine(ois_setup["curve"])
    ois = ql.MakeOIS(
        ql.Period(1, ql.Years), ois_setup["sofr"], 0.035,
        nominal=2_000_000.0, paymentLag=2, pricingEngine=engine,
    )
    assert ois.nominal() == pytest.approx(2_000_000.0)


def test_makeois_kwargs_forward_start(ois_setup):
    """Test MakeOIS with forward start."""
    ois = ql.MakeOIS(
        ql.Period(1, ql.Years), ois_setup["sofr"], 0.035,
        fwdStart=ql.Period(3, ql.Months),
    )
    assert ois.startDate() > ois_setup["today"]


def test_makeois_kwargs_fixed_leg_daycount(ois_setup):
    """Test MakeOIS with fixedLegDayCount kwarg."""
    ois = ql.MakeOIS(
        ql.Period(1, ql.Years), ois_setup["sofr"], 0.035,
        fixedLegDayCount=ql.Actual365Fixed(),
    )
    assert isinstance(ois, ql.OvernightIndexedSwap)


def test_makeois_kwargs_overnight_spread(ois_setup):
    """Test MakeOIS with overnightLegSpread kwarg."""
    ois = ql.MakeOIS(
        ql.Period(1, ql.Years), ois_setup["sofr"], 0.035,
        overnightLegSpread=0.001,
    )
    assert isinstance(ois, ql.OvernightIndexedSwap)


def test_makeois_kwargs_averaging_method(ois_setup):
    """Test MakeOIS with averagingMethod kwarg."""
    ois = ql.MakeOIS(
        ql.Period(1, ql.Years), ois_setup["sofr"], 0.035,
        averagingMethod=ql.RateAveraging.Type.Simple,
    )
    assert ois.averagingMethod() == ql.RateAveraging.Type.Simple


def test_makeois_kwargs_telescopic_dates(ois_setup):
    """Test MakeOIS with telescopicValueDates kwarg."""
    ois = ql.MakeOIS(
        ql.Period(1, ql.Years), ois_setup["sofr"], 0.035,
        telescopicValueDates=True,
    )
    assert isinstance(ois, ql.OvernightIndexedSwap)


def test_makeois_kwargs_bad_kwarg(ois_setup):
    """Test MakeOIS raises TypeError for unknown kwarg."""
    with pytest.raises(TypeError, match="unexpected keyword argument"):
        ql.MakeOIS(
            ql.Period(1, ql.Years), ois_setup["sofr"], 0.035,
            badKwarg=42,
        )


# =============================================================================
# CapFloor, Cap, Floor, Collar
# =============================================================================


@pytest.fixture(scope="module")
def capfloor_env():
    """Setup for cap/floor tests: curve, index, floating leg."""
    today = ql.Date(15, ql.January, 2025)
    ql.Settings.evaluationDate = today

    dc = ql.Actual365Fixed()
    curve = ql.FlatForward(today, 0.04, dc)
    euribor = ql.Euribor6M(curve)

    schedule = ql.Schedule(
        ql.Date(17, ql.January, 2025),
        ql.Date(17, ql.January, 2030),
        ql.Period(6, ql.Months),
        ql.TARGET(),
        ql.ModifiedFollowing,
        ql.ModifiedFollowing,
        ql.DateGeneration.Forward,
        False,
    )

    leg = ql.IborLeg(schedule, euribor).withNotionals([1_000_000.0]).build()

    return {
        "today": today,
        "curve": curve,
        "euribor": euribor,
        "leg": leg,
    }


def test_cap_construction(capfloor_env):
    """Test Cap construction."""
    cap = ql.Cap(capfloor_env["leg"], [0.05])
    assert cap is not None
    assert cap.type() == ql.CapFloorType.Cap


def test_floor_construction(capfloor_env):
    """Test Floor construction."""
    floor = ql.Floor(capfloor_env["leg"], [0.03])
    assert floor is not None
    assert floor.type() == ql.CapFloorType.Floor


def test_collar_construction(capfloor_env):
    """Test Collar construction."""
    collar = ql.Collar(capfloor_env["leg"], [0.05], [0.03])
    assert collar is not None
    assert collar.type() == ql.CapFloorType.Collar


def test_capfloor_generic_construction(capfloor_env):
    """Test CapFloor generic constructor with strikes."""
    cf = ql.CapFloor(ql.CapFloorType.Cap, capfloor_env["leg"], [0.05])
    assert cf is not None
    assert cf.type() == ql.CapFloorType.Cap


def test_cap_inspectors(capfloor_env):
    """Test Cap inspector methods."""
    cap = ql.Cap(capfloor_env["leg"], [0.05])
    assert cap.startDate() == ql.Date(17, ql.January, 2025)
    assert cap.maturityDate() == ql.Date(17, ql.January, 2030)
    assert not cap.isExpired()
    assert all(r == pytest.approx(0.05) for r in cap.capRates())


def test_cap_pricing(capfloor_env):
    """Test Cap pricing with BlackCapFloorEngine."""
    cap = ql.Cap(capfloor_env["leg"], [0.05])
    engine = ql.BlackCapFloorEngine(capfloor_env["curve"], 0.20)
    cap.setPricingEngine(engine)
    assert cap.NPV() == pytest.approx(7405.716086124158, rel=1e-6)


def test_floor_pricing(capfloor_env):
    """Test Floor pricing with BlackCapFloorEngine."""
    floor = ql.Floor(capfloor_env["leg"], [0.03])
    engine = ql.BlackCapFloorEngine(capfloor_env["curve"], 0.20)
    floor.setPricingEngine(engine)
    assert floor.NPV() == pytest.approx(4272.838146959026, rel=1e-6)


def test_collar_pricing(capfloor_env):
    """Test Collar pricing with BlackCapFloorEngine."""
    collar = ql.Collar(capfloor_env["leg"], [0.05], [0.03])
    engine = ql.BlackCapFloorEngine(capfloor_env["curve"], 0.20)
    collar.setPricingEngine(engine)
    assert collar.NPV() == pytest.approx(3132.877939165133, rel=1e-6)


def test_capfloor_parity(capfloor_env):
    """Test cap-floor parity: collar NPV = cap NPV - floor NPV."""
    engine = ql.BlackCapFloorEngine(capfloor_env["curve"], 0.20)

    cap = ql.Cap(capfloor_env["leg"], [0.05])
    cap.setPricingEngine(engine)
    floor = ql.Floor(capfloor_env["leg"], [0.03])
    floor.setPricingEngine(engine)
    collar = ql.Collar(capfloor_env["leg"], [0.05], [0.03])
    collar.setPricingEngine(engine)

    assert collar.NPV() == pytest.approx(cap.NPV() - floor.NPV(), abs=1e-6)


def test_cap_atm_rate(capfloor_env):
    """Test Cap ATM rate calculation."""
    cap = ql.Cap(capfloor_env["leg"], [0.05])
    engine = ql.BlackCapFloorEngine(capfloor_env["curve"], 0.20)
    cap.setPricingEngine(engine)
    atm = cap.atmRate(capfloor_env["curve"])
    assert atm == pytest.approx(0.03985, abs=0.001)


def test_cap_implied_volatility(capfloor_env):
    """Test Cap implied volatility recovery."""
    cap = ql.Cap(capfloor_env["leg"], [0.05])
    engine = ql.BlackCapFloorEngine(capfloor_env["curve"], 0.20)
    cap.setPricingEngine(engine)
    implied = cap.impliedVolatility(
        cap.NPV(), ql.YieldTermStructureHandle(capfloor_env["curve"]), 0.20
    )
    assert implied == pytest.approx(0.20, abs=1e-4)


def test_cap_bachelier_pricing(capfloor_env):
    """Test Cap pricing with BachelierCapFloorEngine."""
    cap = ql.Cap(capfloor_env["leg"], [0.05])
    engine = ql.BachelierCapFloorEngine(capfloor_env["curve"], 0.005)
    cap.setPricingEngine(engine)
    assert cap.NPV() == pytest.approx(1606.1185633197292, rel=1e-6)


# =============================================================================
# MakeCapFloor
# =============================================================================


def test_makecapfloor_kwargs(capfloor_env):
    """Test MakeCapFloor kwargs wrapper."""
    cap = ql.MakeCapFloor(
        ql.CapFloorType.Cap,
        ql.Period(5, ql.Years),
        capfloor_env["euribor"],
        0.05,
    )
    assert cap is not None
    assert cap.type() == ql.CapFloorType.Cap


def test_makecapfloor_builder_chaining(capfloor_env):
    """Test MakeCapFloor C++ builder chaining."""
    from pyquantlib._pyquantlib import MakeCapFloor as MakeCapFloorBuilder
    engine = ql.BlackCapFloorEngine(capfloor_env["curve"], 0.20)
    cap = (
        MakeCapFloorBuilder(
            ql.CapFloorType.Cap,
            ql.Period(5, ql.Years),
            capfloor_env["euribor"],
            0.05,
        )
        .withNominal(2_000_000.0)
        .withPricingEngine(engine)
        .capFloor()
    )
    assert cap.NPV() == pytest.approx(14811.4322, rel=1e-4)


def test_makecapfloor_floor(capfloor_env):
    """Test MakeCapFloor for floor type."""
    floor = ql.MakeCapFloor(
        ql.CapFloorType.Floor,
        ql.Period(5, ql.Years),
        capfloor_env["euribor"],
        0.03,
    )
    assert floor.type() == ql.CapFloorType.Floor


def test_makecapfloor_atm(capfloor_env):
    """Test MakeCapFloor with no strike (ATM) requires engine."""
    engine = ql.BlackCapFloorEngine(capfloor_env["curve"], 0.20)
    cap = ql.MakeCapFloor(
        ql.CapFloorType.Cap,
        ql.Period(5, ql.Years),
        capfloor_env["euribor"],
        pricingEngine=engine,
    )
    assert cap is not None
    assert cap.type() == ql.CapFloorType.Cap


def test_makecapfloor_kwargs_nominal(capfloor_env):
    """Test MakeCapFloor with nominal kwarg."""
    cap = ql.MakeCapFloor(
        ql.CapFloorType.Cap,
        ql.Period(5, ql.Years),
        capfloor_env["euribor"],
        0.05,
        nominal=5_000_000.0,
    )
    assert cap.type() == ql.CapFloorType.Cap


def test_makecapfloor_kwargs_pricing_engine(capfloor_env):
    """Test MakeCapFloor with pricingEngine kwarg."""
    engine = ql.BlackCapFloorEngine(capfloor_env["curve"], 0.20)
    cap = ql.MakeCapFloor(
        ql.CapFloorType.Cap,
        ql.Period(5, ql.Years),
        capfloor_env["euribor"],
        0.05,
        pricingEngine=engine,
    )
    assert cap.NPV() == pytest.approx(0.007406, rel=1e-3)


def test_makecapfloor_kwargs_multiple(capfloor_env):
    """Test MakeCapFloor with multiple kwargs."""
    engine = ql.BlackCapFloorEngine(capfloor_env["curve"], 0.20)
    cap = ql.MakeCapFloor(
        ql.CapFloorType.Cap,
        ql.Period(5, ql.Years),
        capfloor_env["euribor"],
        0.05,
        nominal=2_000_000.0,
        pricingEngine=engine,
    )
    assert cap.NPV() == pytest.approx(14811.4322, rel=1e-4)


def test_makecapfloor_kwargs_forward_start(capfloor_env):
    """Test MakeCapFloor with forward start."""
    cap = ql.MakeCapFloor(
        ql.CapFloorType.Cap,
        ql.Period(5, ql.Years),
        capfloor_env["euribor"],
        0.05,
        forwardStart=ql.Period(1, ql.Years),
    )
    assert cap.startDate() > capfloor_env["today"]


def test_makecapfloor_kwargs_as_optionlet(capfloor_env):
    """Test MakeCapFloor as single optionlet via kwarg."""
    engine = ql.BlackCapFloorEngine(capfloor_env["curve"], 0.20)
    caplet = ql.MakeCapFloor(
        ql.CapFloorType.Cap,
        ql.Period(5, ql.Years),
        capfloor_env["euribor"],
        0.05,
        asOptionlet=True,
        pricingEngine=engine,
    )
    assert caplet is not None
    assert len(caplet.floatingLeg()) == 1


def test_makecapfloor_kwargs_bad_kwarg(capfloor_env):
    """Test MakeCapFloor raises TypeError for unknown kwarg."""
    with pytest.raises(TypeError, match="unexpected keyword argument"):
        ql.MakeCapFloor(
            ql.CapFloorType.Cap,
            ql.Period(5, ql.Years),
            capfloor_env["euribor"],
            0.05,
            badKwarg=42,
        )


# =============================================================================
# ForwardRateAgreement
# =============================================================================


def test_forwardrateagreement_construction(capfloor_env):
    """Test ForwardRateAgreement construction."""
    fra = ql.ForwardRateAgreement(
        capfloor_env["euribor"],
        ql.Date(15, ql.September, 2025),
        ql.PositionType.Long,
        0.04,
        1_000_000.0,
        capfloor_env["curve"],
    )
    assert fra is not None
    assert not fra.isExpired()


def test_forwardrateagreement_npv(capfloor_env):
    """Test FRA NPV calculation."""
    fra = ql.ForwardRateAgreement(
        capfloor_env["euribor"],
        ql.Date(15, ql.September, 2025),
        ql.PositionType.Long,
        0.04,
        1_000_000.0,
        capfloor_env["curve"],
    )
    assert fra.NPV() == pytest.approx(-73.2880, rel=1e-3)


def test_forwardrateagreement_amount(capfloor_env):
    """Test FRA payoff amount."""
    fra = ql.ForwardRateAgreement(
        capfloor_env["euribor"],
        ql.Date(15, ql.September, 2025),
        ql.PositionType.Long,
        0.04,
        1_000_000.0,
        capfloor_env["curve"],
    )
    assert fra.amount() == pytest.approx(-75.2658, rel=1e-3)


def test_forwardrateagreement_forward_rate(capfloor_env):
    """Test FRA forward rate."""
    fra = ql.ForwardRateAgreement(
        capfloor_env["euribor"],
        ql.Date(15, ql.September, 2025),
        ql.PositionType.Long,
        0.04,
        1_000_000.0,
        capfloor_env["curve"],
    )
    fwd = fra.forwardRate()
    assert fwd.rate() == pytest.approx(0.03985, abs=0.001)


def test_forwardrateagreement_fixing_date(capfloor_env):
    """Test FRA fixing date."""
    fra = ql.ForwardRateAgreement(
        capfloor_env["euribor"],
        ql.Date(15, ql.September, 2025),
        ql.PositionType.Long,
        0.04,
        1_000_000.0,
        capfloor_env["curve"],
    )
    assert fra.fixingDate() == ql.Date(11, ql.September, 2025)


def test_forwardrateagreement_par_rate(capfloor_env):
    """Test FRA with par-rate approximation constructor."""
    fra = ql.ForwardRateAgreement(
        capfloor_env["euribor"],
        ql.Date(15, ql.September, 2025),
        ql.Date(15, ql.March, 2026),
        ql.PositionType.Short,
        0.04,
        1_000_000.0,
        ql.YieldTermStructureHandle(capfloor_env["curve"]),
    )
    # Short position: opposite sign to long
    assert fra.NPV() == pytest.approx(73.2880, rel=1e-3)


# =============================================================================
# ForwardTypePayoff
# =============================================================================


def test_forwardtypepayoff_long():
    """ForwardTypePayoff long position pays price - strike."""
    payoff = ql.ForwardTypePayoff(ql.PositionType.Long, 100.0)
    assert payoff.forwardType() == ql.PositionType.Long
    assert payoff.strike() == pytest.approx(100.0, rel=1e-15)
    assert payoff(110.0) == pytest.approx(10.0, rel=1e-15)
    assert payoff(90.0) == pytest.approx(-10.0, rel=1e-15)


def test_forwardtypepayoff_short():
    """ForwardTypePayoff short position pays strike - price."""
    payoff = ql.ForwardTypePayoff(ql.PositionType.Short, 100.0)
    assert payoff.forwardType() == ql.PositionType.Short
    assert payoff(110.0) == pytest.approx(-10.0, rel=1e-15)
    assert payoff(90.0) == pytest.approx(10.0, rel=1e-15)


def test_forwardtypepayoff_description():
    """ForwardTypePayoff has name and description."""
    payoff = ql.ForwardTypePayoff(ql.PositionType.Long, 105.0)
    assert payoff.name() == "Forward"
    assert "105" in payoff.description()


# =============================================================================
# BondForward
# =============================================================================


@pytest.fixture(scope="module")
def bond_forward_env():
    """Common environment for BondForward tests."""
    today = ql.Date(15, ql.January, 2025)
    ql.Settings.evaluationDate = today
    calendar = ql.TARGET()
    dc = ql.Actual365Fixed()

    r_ts = ql.FlatForward(today, 0.04, dc)
    r_handle = ql.YieldTermStructureHandle(r_ts)

    # Create a fixed rate bond
    issue_date = ql.Date(15, ql.January, 2024)
    maturity_date = ql.Date(15, ql.January, 2029)
    schedule = ql.MakeSchedule(
        effectiveDate=issue_date, terminationDate=maturity_date,
        tenor=ql.Period("1Y"), calendar=calendar,
        convention=ql.ModifiedFollowing,
    )
    bond = ql.FixedRateBond(
        2, 100.0, schedule, [0.05],
        ql.Thirty360(ql.Thirty360.BondBasis),
    )
    bond_engine = ql.DiscountingBondEngine(r_handle)
    bond.setPricingEngine(bond_engine)

    # Forward delivery date: 6 months from today
    delivery_date = calendar.advance(today, ql.Period("6M"))

    return {
        "today": today,
        "calendar": calendar,
        "dc": dc,
        "r_ts": r_ts,
        "r_handle": r_handle,
        "bond": bond,
        "delivery_date": delivery_date,
    }


def test_bondforward_construction(bond_forward_env):
    """BondForward construction with discount curve."""
    env = bond_forward_env
    fwd = ql.BondForward(
        env["today"], env["delivery_date"],
        ql.PositionType.Long, 0.0,
        2, env["dc"], env["calendar"],
        ql.ModifiedFollowing,
        env["bond"],
        env["r_handle"],
        env["r_handle"],
    )
    assert fwd is not None
    assert fwd.isExpired() is False


def test_bondforward_forward_price(bond_forward_env):
    """BondForward forwardPrice returns dirty forward price."""
    env = bond_forward_env
    fwd = ql.BondForward(
        env["today"], env["delivery_date"],
        ql.PositionType.Long, 0.0,
        2, env["dc"], env["calendar"],
        ql.ModifiedFollowing,
        env["bond"],
        env["r_handle"],
        env["r_handle"],
    )
    dirty_fwd = fwd.forwardPrice()
    assert dirty_fwd == pytest.approx(105.4124, rel=1e-4)


def test_bondforward_clean_forward_price(bond_forward_env):
    """BondForward cleanForwardPrice subtracts accrued interest."""
    env = bond_forward_env
    fwd = ql.BondForward(
        env["today"], env["delivery_date"],
        ql.PositionType.Long, 0.0,
        2, env["dc"], env["calendar"],
        ql.ModifiedFollowing,
        env["bond"],
        env["r_handle"],
        env["r_handle"],
    )
    clean_fwd = fwd.cleanForwardPrice()
    dirty_fwd = fwd.forwardPrice()
    assert clean_fwd < dirty_fwd


def test_bondforward_npv(bond_forward_env):
    """BondForward NPV with nonzero strike."""
    env = bond_forward_env
    strike = 100.0
    fwd = ql.BondForward(
        env["today"], env["delivery_date"],
        ql.PositionType.Long, strike,
        2, env["dc"], env["calendar"],
        ql.ModifiedFollowing,
        env["bond"],
        env["r_handle"],
        env["r_handle"],
    )
    assert fwd.NPV() == pytest.approx(5.3061, rel=1e-4)


def test_bondforward_short_position(bond_forward_env):
    """BondForward short position has opposite NPV to long."""
    env = bond_forward_env
    strike = 100.0
    long_fwd = ql.BondForward(
        env["today"], env["delivery_date"],
        ql.PositionType.Long, strike,
        2, env["dc"], env["calendar"],
        ql.ModifiedFollowing,
        env["bond"],
        env["r_handle"],
        env["r_handle"],
    )
    short_fwd = ql.BondForward(
        env["today"], env["delivery_date"],
        ql.PositionType.Short, strike,
        2, env["dc"], env["calendar"],
        ql.ModifiedFollowing,
        env["bond"],
        env["r_handle"],
        env["r_handle"],
    )
    assert long_fwd.NPV() == pytest.approx(-short_fwd.NPV(), rel=1e-10)


def test_bondforward_inspectors(bond_forward_env):
    """BondForward inherits Forward inspectors."""
    env = bond_forward_env
    fwd = ql.BondForward(
        env["today"], env["delivery_date"],
        ql.PositionType.Long, 100.0,
        2, env["dc"], env["calendar"],
        ql.ModifiedFollowing,
        env["bond"],
        env["r_handle"],
        env["r_handle"],
    )
    assert fwd.settlementDate() is not None
    assert fwd.calendar() is not None
    assert fwd.dayCounter() is not None
    assert fwd.businessDayConvention() == ql.ModifiedFollowing
    assert fwd.spotValue() == pytest.approx(103.3421, rel=1e-4)
    assert fwd.forwardValue() == pytest.approx(105.4124, rel=1e-4)


def test_bondforward_hidden_handle(bond_forward_env):
    """BondForward hidden handle constructor accepts raw term structures."""
    env = bond_forward_env
    fwd = ql.BondForward(
        env["today"], env["delivery_date"],
        ql.PositionType.Long, 100.0,
        2, env["dc"], env["calendar"],
        ql.ModifiedFollowing,
        env["bond"],
        env["r_ts"],
        env["r_ts"],
    )
    assert fwd.NPV() == pytest.approx(5.3061, rel=1e-4)


# =============================================================================
# BarrierType enum
# =============================================================================


@pytest.fixture(scope="module")
def barrier_env():
    """Setup for barrier option tests."""
    today = ql.Date(15, ql.January, 2025)
    ql.Settings.evaluationDate = today

    expiry = today + ql.Period("1Y")
    exercise = ql.EuropeanExercise(expiry)
    call_payoff = ql.PlainVanillaPayoff(ql.Call, 100.0)

    return {
        "exercise": exercise,
        "call_payoff": call_payoff,
    }


def test_barriertype_values():
    """Test BarrierType enum values."""
    assert ql.BarrierType.DownIn is not None
    assert ql.BarrierType.UpIn is not None
    assert ql.BarrierType.DownOut is not None
    assert ql.BarrierType.UpOut is not None


# =============================================================================
# BarrierOption
# =============================================================================


def test_barrieroption_construction(barrier_env):
    """Test BarrierOption construction with various barrier types."""
    for bt in [ql.BarrierType.DownOut, ql.BarrierType.DownIn,
               ql.BarrierType.UpOut, ql.BarrierType.UpIn]:
        opt = ql.BarrierOption(
            bt, 80.0, 0.0,
            barrier_env["call_payoff"], barrier_env["exercise"],
        )
        assert opt is not None
        assert not opt.isExpired()


def test_barrieroption_with_rebate(barrier_env):
    """Test BarrierOption construction with non-zero rebate."""
    opt = ql.BarrierOption(
        ql.BarrierType.DownOut, 80.0, 5.0,
        barrier_env["call_payoff"], barrier_env["exercise"],
    )
    assert opt is not None


# =============================================================================
# DoubleBarrierType enum
# =============================================================================


def test_doublebarriertype_values():
    """Test DoubleBarrierType enum values."""
    assert ql.DoubleBarrierType.KnockIn is not None
    assert ql.DoubleBarrierType.KnockOut is not None
    assert ql.DoubleBarrierType.KIKO is not None
    assert ql.DoubleBarrierType.KOKI is not None


# =============================================================================
# DoubleBarrierOption
# =============================================================================


def test_doublebarrieroption_construction(barrier_env):
    """Test DoubleBarrierOption construction."""
    for bt in [ql.DoubleBarrierType.KnockOut, ql.DoubleBarrierType.KnockIn,
               ql.DoubleBarrierType.KIKO, ql.DoubleBarrierType.KOKI]:
        opt = ql.DoubleBarrierOption(
            bt, 80.0, 120.0, 0.0,
            barrier_env["call_payoff"], barrier_env["exercise"],
        )
        assert opt is not None
        assert not opt.isExpired()


# =============================================================================
# AverageType enum
# =============================================================================


@pytest.fixture(scope="module")
def asian_env():
    """Setup for Asian option tests."""
    today = ql.Date(15, ql.January, 2025)
    ql.Settings.evaluationDate = today

    expiry = today + ql.Period("1Y")
    exercise = ql.EuropeanExercise(expiry)
    payoff = ql.PlainVanillaPayoff(ql.Call, 100.0)

    # Monthly fixing dates
    fixing_dates = []
    d = today + ql.Period("1M")
    while d <= expiry:
        fixing_dates.append(d)
        d = d + ql.Period("1M")

    return {
        "exercise": exercise,
        "payoff": payoff,
        "fixing_dates": fixing_dates,
    }


def test_averagetype_values():
    """Test AverageType enum values."""
    assert ql.AverageType.Arithmetic is not None
    assert ql.AverageType.Geometric is not None


# =============================================================================
# ContinuousAveragingAsianOption
# =============================================================================


def test_continuous_asian_construction(asian_env):
    """Test ContinuousAveragingAsianOption construction."""
    for avg in [ql.AverageType.Geometric, ql.AverageType.Arithmetic]:
        opt = ql.ContinuousAveragingAsianOption(
            avg, asian_env["payoff"], asian_env["exercise"],
        )
        assert opt is not None
        assert not opt.isExpired()


# =============================================================================
# DiscreteAveragingAsianOption
# =============================================================================


def test_discrete_asian_accumulator_constructor(asian_env):
    """Test DiscreteAveragingAsianOption with accumulator constructor."""
    opt = ql.DiscreteAveragingAsianOption(
        ql.AverageType.Geometric, 0.0, 0,
        asian_env["fixing_dates"], asian_env["payoff"], asian_env["exercise"],
    )
    assert opt is not None
    assert not opt.isExpired()


def test_discrete_asian_fixingdates_constructor(asian_env):
    """Test DiscreteAveragingAsianOption with all-fixing-dates constructor."""
    opt = ql.DiscreteAveragingAsianOption(
        ql.AverageType.Geometric, asian_env["fixing_dates"],
        asian_env["payoff"], asian_env["exercise"],
    )
    assert opt is not None
    assert not opt.isExpired()


def test_discrete_asian_with_past_fixings(asian_env):
    """Test DiscreteAveragingAsianOption with past fixings."""
    opt = ql.DiscreteAveragingAsianOption(
        ql.AverageType.Arithmetic, asian_env["fixing_dates"],
        asian_env["payoff"], asian_env["exercise"],
        allPastFixings=[100.0, 101.0],
    )
    assert opt is not None


# =============================================================================
# MakeVanillaSwap
# =============================================================================


@pytest.fixture(scope="module")
def mvs_env():
    """Setup for MakeVanillaSwap tests."""
    today = ql.Date(15, ql.January, 2025)
    ql.Settings.evaluationDate = today

    dc = ql.Actual365Fixed()
    curve = ql.FlatForward(today, 0.05, dc)
    euribor = ql.Euribor6M(curve)

    return {
        "today": today,
        "curve": curve,
        "euribor": euribor,
    }


def test_makevanillaswap_kwargs(mvs_env):
    """Test MakeVanillaSwap kwargs wrapper."""
    swap = ql.MakeVanillaSwap(
        ql.Period(5, ql.Years),
        mvs_env["euribor"],
        0.05,
    )
    assert swap is not None
    assert isinstance(swap, ql.VanillaSwap)


def test_makevanillaswap_atm(mvs_env):
    """Test MakeVanillaSwap with no fixed rate (ATM)."""
    swap = ql.MakeVanillaSwap(
        ql.Period(5, ql.Years),
        mvs_env["euribor"],
    )
    assert swap is not None


def test_makevanillaswap_kwargs_nominal(mvs_env):
    """Test MakeVanillaSwap with nominal kwarg."""
    swap = ql.MakeVanillaSwap(
        ql.Period(5, ql.Years),
        mvs_env["euribor"],
        0.05,
        nominal=5_000_000.0,
    )
    assert swap is not None
    assert swap.nominal() == 5_000_000.0


def test_makevanillaswap_kwargs_receive_fixed(mvs_env):
    """Test MakeVanillaSwap with receiveFixed kwarg."""
    swap = ql.MakeVanillaSwap(
        ql.Period(5, ql.Years),
        mvs_env["euribor"],
        0.05,
        receiveFixed=True,
    )
    assert swap.type() == ql.SwapType.Receiver


def test_makevanillaswap_kwargs_swap_type(mvs_env):
    """Test MakeVanillaSwap with swapType kwarg."""
    swap = ql.MakeVanillaSwap(
        ql.Period(5, ql.Years),
        mvs_env["euribor"],
        0.05,
        swapType=ql.SwapType.Receiver,
    )
    assert swap.type() == ql.SwapType.Receiver


def test_makevanillaswap_kwargs_forward_start(mvs_env):
    """Test MakeVanillaSwap with forward start."""
    swap = ql.MakeVanillaSwap(
        ql.Period(5, ql.Years),
        mvs_env["euribor"],
        0.05,
        forwardStart=ql.Period(3, ql.Months),
    )
    assert swap is not None


def test_makevanillaswap_kwargs_pricing_engine(mvs_env):
    """Test MakeVanillaSwap with pricingEngine kwarg."""
    engine = ql.DiscountingSwapEngine(mvs_env["curve"])
    swap = ql.MakeVanillaSwap(
        ql.Period(5, ql.Years),
        mvs_env["euribor"],
        0.05,
        pricingEngine=engine,
    )
    assert swap.NPV() == pytest.approx(0.005600, rel=1e-3)


def test_makevanillaswap_kwargs_multiple(mvs_env):
    """Test MakeVanillaSwap with multiple kwargs."""
    engine = ql.DiscountingSwapEngine(mvs_env["curve"])
    swap = ql.MakeVanillaSwap(
        ql.Period(5, ql.Years),
        mvs_env["euribor"],
        0.05,
        nominal=2_000_000.0,
        floatingLegSpread=0.001,
        pricingEngine=engine,
    )
    assert swap.nominal() == 2_000_000.0
    assert swap.spread() == 0.001


def test_makevanillaswap_builder_chaining(mvs_env):
    """Test MakeVanillaSwap C++ builder chaining."""
    from pyquantlib._pyquantlib import MakeVanillaSwap as MakeVanillaSwapBuilder
    engine = ql.DiscountingSwapEngine(mvs_env["curve"])
    swap = (
        MakeVanillaSwapBuilder(
            ql.Period(5, ql.Years), mvs_env["euribor"], 0.05)
        .withNominal(2_000_000.0)
        .withPricingEngine(engine)
        .swap()
    )
    assert swap is not None
    assert swap.nominal() == 2_000_000.0


def test_makevanillaswap_kwargs_bad_kwarg(mvs_env):
    """Test MakeVanillaSwap raises TypeError for unknown kwarg."""
    with pytest.raises(TypeError, match="unexpected keyword argument"):
        ql.MakeVanillaSwap(
            ql.Period(5, ql.Years),
            mvs_env["euribor"],
            0.05,
            badKwarg=42,
        )


# =============================================================================
# MakeSwaption
# =============================================================================


@pytest.fixture(scope="module")
def mswn_env():
    """Setup for MakeSwaption tests."""
    today = ql.Date(15, ql.January, 2025)
    ql.Settings.evaluationDate = today

    dc = ql.Actual365Fixed()
    curve = ql.FlatForward(today, 0.05, dc)
    euribor = ql.Euribor6M(curve)

    swap_index = ql.SwapIndex(
        "EuriborSwapIsdaFixA", ql.Period(5, ql.Years),
        2, ql.EURCurrency(), ql.TARGET(),
        ql.Period(1, ql.Years), ql.Unadjusted,
        ql.Thirty360(ql.Thirty360.BondBasis), euribor,
    )

    return {
        "today": today,
        "curve": curve,
        "euribor": euribor,
        "swap_index": swap_index,
    }


def test_makeswaption_kwargs(mswn_env):
    """Test MakeSwaption kwargs wrapper."""
    swaption = ql.MakeSwaption(
        mswn_env["swap_index"],
        ql.Period(1, ql.Years),
        0.05,
    )
    assert swaption is not None
    assert isinstance(swaption, ql.Swaption)


def test_makeswaption_atm(mswn_env):
    """Test MakeSwaption with no strike (ATM)."""
    swaption = ql.MakeSwaption(
        mswn_env["swap_index"],
        ql.Period(1, ql.Years),
    )
    assert isinstance(swaption, ql.Swaption)


def test_makeswaption_kwargs_nominal(mswn_env):
    """Test MakeSwaption with nominal kwarg."""
    swaption = ql.MakeSwaption(
        mswn_env["swap_index"],
        ql.Period(1, ql.Years),
        0.05,
        nominal=5_000_000.0,
    )
    assert isinstance(swaption, ql.Swaption)


def test_makeswaption_kwargs_settlement_type(mswn_env):
    """Test MakeSwaption with settlementType kwarg."""
    swaption = ql.MakeSwaption(
        mswn_env["swap_index"],
        ql.Period(1, ql.Years),
        0.05,
        settlementType=ql.SettlementType.Cash,
        settlementMethod=ql.SettlementMethod.ParYieldCurve,
    )
    assert swaption.settlementType() == ql.SettlementType.Cash


def test_makeswaption_kwargs_underlying_type(mswn_env):
    """Test MakeSwaption with underlyingType kwarg."""
    swaption = ql.MakeSwaption(
        mswn_env["swap_index"],
        ql.Period(1, ql.Years),
        0.05,
        underlyingType=ql.SwapType.Receiver,
    )
    assert swaption.type() == ql.SwapType.Receiver


def test_makeswaption_kwargs_bad_kwarg(mswn_env):
    """Test MakeSwaption raises TypeError for unknown kwarg."""
    with pytest.raises(TypeError, match="unexpected keyword argument"):
        ql.MakeSwaption(
            mswn_env["swap_index"],
            ql.Period(1, ql.Years),
            0.05,
            badKwarg=42,
        )


# =============================================================================
# ZeroCouponSwap
# =============================================================================


@pytest.fixture(scope="module")
def zcs_env():
    """Setup for ZeroCouponSwap tests."""
    today = ql.Date(15, ql.January, 2025)
    ql.Settings.evaluationDate = today

    dc = ql.Actual365Fixed()
    curve = ql.FlatForward(today, 0.04, dc)
    euribor = ql.Euribor6M(curve)
    calendar = ql.TARGET()

    start = calendar.advance(today, ql.Period(2, ql.Days))
    maturity = calendar.advance(start, ql.Period(5, ql.Years))

    return {
        "today": today,
        "curve": curve,
        "euribor": euribor,
        "calendar": calendar,
        "start": start,
        "maturity": maturity,
    }


def test_zerocouponswap_fixed_payment(zcs_env):
    """Test ZeroCouponSwap with fixed payment amount."""
    zcs = ql.ZeroCouponSwap(
        ql.SwapType.Payer,
        1_000_000.0,
        zcs_env["start"],
        zcs_env["maturity"],
        1_200_000.0,
        zcs_env["euribor"],
        zcs_env["calendar"],
    )
    assert zcs is not None
    assert zcs.type() == ql.SwapType.Payer
    assert zcs.baseNominal() == 1_000_000.0
    assert zcs.fixedPayment() == pytest.approx(1_200_000.0)


def test_zerocouponswap_fixed_rate(zcs_env):
    """Test ZeroCouponSwap with fixed rate."""
    zcs = ql.ZeroCouponSwap(
        ql.SwapType.Receiver,
        1_000_000.0,
        zcs_env["start"],
        zcs_env["maturity"],
        0.04,
        ql.Actual365Fixed(),
        zcs_env["euribor"],
        zcs_env["calendar"],
    )
    assert zcs.type() == ql.SwapType.Receiver
    assert zcs.baseNominal() == 1_000_000.0


def test_zerocouponswap_pricing(zcs_env):
    """Test ZeroCouponSwap pricing."""
    zcs = ql.ZeroCouponSwap(
        ql.SwapType.Payer,
        1_000_000.0,
        zcs_env["start"],
        zcs_env["maturity"],
        0.04,
        ql.Actual365Fixed(),
        zcs_env["euribor"],
        zcs_env["calendar"],
    )
    engine = ql.DiscountingSwapEngine(zcs_env["curve"])
    zcs.setPricingEngine(engine)

    npv = zcs.NPV()
    assert isinstance(npv, float)
    fair_payment = zcs.fairFixedPayment()
    assert fair_payment == pytest.approx(221543.1842, rel=1e-4)


def test_zerocouponswap_legs(zcs_env):
    """Test ZeroCouponSwap leg accessors."""
    zcs = ql.ZeroCouponSwap(
        ql.SwapType.Payer,
        1_000_000.0,
        zcs_env["start"],
        zcs_env["maturity"],
        1_200_000.0,
        zcs_env["euribor"],
        zcs_env["calendar"],
    )
    assert len(zcs.fixedLeg()) > 0
    assert len(zcs.floatingLeg()) > 0
    assert zcs.startDate() == zcs_env["start"]
    assert zcs.maturityDate() == zcs_env["maturity"]


# =============================================================================
# CompositeInstrument
# =============================================================================


def test_compositeinstrument_construction():
    """Test CompositeInstrument construction."""
    ci = ql.CompositeInstrument()
    assert ci is not None


def test_compositeinstrument_add_subtract(option_market_env):
    """Test CompositeInstrument add and subtract."""
    payoff_call = ql.PlainVanillaPayoff(ql.OptionType.Call, 100.0)
    payoff_put = ql.PlainVanillaPayoff(ql.OptionType.Put, 100.0)
    exercise_date = option_market_env["today"] + ql.Period(1, ql.Years)
    exercise = ql.EuropeanExercise(exercise_date)

    call = ql.VanillaOption(payoff_call, exercise)
    put = ql.VanillaOption(payoff_put, exercise)

    engine = ql.AnalyticEuropeanEngine(option_market_env["process"])
    call.setPricingEngine(engine)
    put.setPricingEngine(engine)

    ci = ql.CompositeInstrument()
    ci.add(call)
    ci.subtract(put)

    # Composite NPV = call - put
    assert ci.NPV() == pytest.approx(call.NPV() - put.NPV(), abs=1e-6)


def test_compositeinstrument_multiplier(option_market_env):
    """Test CompositeInstrument with multiplier."""
    payoff = ql.PlainVanillaPayoff(ql.OptionType.Call, 100.0)
    exercise_date = option_market_env["today"] + ql.Period(1, ql.Years)
    exercise = ql.EuropeanExercise(exercise_date)

    call = ql.VanillaOption(payoff, exercise)
    engine = ql.AnalyticEuropeanEngine(option_market_env["process"])
    call.setPricingEngine(engine)

    ci = ql.CompositeInstrument()
    ci.add(call, 2.0)

    assert ci.NPV() == pytest.approx(2.0 * call.NPV(), abs=1e-6)


# =============================================================================
# AssetSwap
# =============================================================================


@pytest.fixture(scope="module")
def assetswap_env():
    """Setup for AssetSwap tests."""
    today = ql.Date(15, ql.January, 2025)
    ql.Settings.evaluationDate = today

    dc = ql.Actual365Fixed()
    curve = ql.FlatForward(today, 0.04, dc)
    euribor = ql.Euribor6M(curve)

    calendar = ql.TARGET()
    issue = ql.Date(15, ql.January, 2024)
    maturity = ql.Date(15, ql.January, 2029)

    schedule = ql.Schedule(
        issue, maturity,
        ql.Period(ql.Annual), calendar,
        ql.Unadjusted, ql.Unadjusted,
        ql.DateGeneration.Backward, False,
    )
    bond = ql.FixedRateBond(
        2, 100.0, schedule, [0.05],
        ql.Thirty360(ql.Thirty360.BondBasis),
    )
    bond_engine = ql.DiscountingBondEngine(curve)
    bond.setPricingEngine(bond_engine)

    return {
        "today": today,
        "curve": curve,
        "euribor": euribor,
        "bond": bond,
    }


def test_assetswap_construction(assetswap_env):
    """Test AssetSwap construction."""
    asw = ql.AssetSwap(
        True,
        assetswap_env["bond"],
        100.0,
        assetswap_env["euribor"],
        0.0,
    )
    assert asw is not None
    assert asw.parSwap() is True


def test_assetswap_pricing(assetswap_env):
    """Test AssetSwap pricing."""
    asw = ql.AssetSwap(
        True,
        assetswap_env["bond"],
        100.0,
        assetswap_env["euribor"],
        0.0,
    )
    engine = ql.DiscountingSwapEngine(assetswap_env["curve"])
    asw.setPricingEngine(engine)

    npv = asw.NPV()
    assert isinstance(npv, float)
    fair_spread = asw.fairSpread()
    assert isinstance(fair_spread, float)


def test_assetswap_inspectors(assetswap_env):
    """Test AssetSwap inspector methods."""
    asw = ql.AssetSwap(
        True,
        assetswap_env["bond"],
        100.0,
        assetswap_env["euribor"],
        0.001,
    )
    assert asw.payBondCoupon() is True
    assert asw.spread() == 0.001
    assert asw.cleanPrice() == 100.0
    assert asw.bond() is not None
    assert len(asw.bondLeg()) > 0
    assert len(asw.floatingLeg()) > 0


# =============================================================================
# ProtectionSide enum
# =============================================================================


def test_protectionside_values():
    """Test ProtectionSide enum values."""
    assert ql.ProtectionSide.Buyer is not None
    assert ql.ProtectionSide.Seller is not None


# =============================================================================
# CdsPricingModel enum
# =============================================================================


def test_cdspricingmodel_values():
    """Test CdsPricingModel enum values."""
    assert ql.CdsPricingModel.Midpoint is not None
    assert ql.CdsPricingModel.ISDA is not None


# =============================================================================
# CreditDefaultSwap
# =============================================================================


@pytest.fixture(scope="module")
def cds_env():
    """Setup for CDS tests."""
    today = ql.Date(15, ql.January, 2025)
    ql.Settings.evaluationDate = today

    calendar = ql.TARGET()
    dc = ql.Actual365Fixed()

    # Discount curve
    discount_curve = ql.FlatForward(today, 0.02, dc)

    # Default probability curve
    hazard_rate = 0.01  # 1% annual hazard rate
    default_curve = ql.FlatHazardRate(today, hazard_rate, dc)

    # CDS schedule
    start = calendar.advance(today, ql.Period(1, ql.Days))
    maturity = calendar.advance(start, ql.Period(5, ql.Years))
    schedule = ql.Schedule(
        start, maturity,
        ql.Period(ql.Quarterly), calendar,
        ql.Following, ql.Unadjusted,
        ql.DateGeneration.TwentiethIMM, False,
    )

    return {
        "today": today,
        "discount_curve": discount_curve,
        "default_curve": default_curve,
        "schedule": schedule,
        "calendar": calendar,
    }


def test_creditdefaultswap_running_spread(cds_env):
    """Test CDS construction with running spread only."""
    cds = ql.CreditDefaultSwap(
        ql.ProtectionSide.Buyer,
        10_000_000.0,
        0.01,  # 100 bps running spread
        cds_env["schedule"],
        ql.Following,
        ql.Actual360(),
    )
    assert cds is not None
    assert cds.side() == ql.ProtectionSide.Buyer
    assert cds.notional() == 10_000_000.0
    assert cds.runningSpread() == 0.01


def test_creditdefaultswap_upfront(cds_env):
    """Test CDS construction with upfront and running spread."""
    cds = ql.CreditDefaultSwap(
        ql.ProtectionSide.Seller,
        10_000_000.0,
        0.02,   # 2% upfront
        0.005,  # 50 bps running spread
        cds_env["schedule"],
        ql.Following,
        ql.Actual360(),
    )
    assert cds.side() == ql.ProtectionSide.Seller
    assert cds.notional() == 10_000_000.0


def test_creditdefaultswap_inspectors(cds_env):
    """Test CDS inspector methods."""
    cds = ql.CreditDefaultSwap(
        ql.ProtectionSide.Buyer,
        10_000_000.0,
        0.01,
        cds_env["schedule"],
        ql.Following,
        ql.Actual360(),
    )
    assert cds.settlesAccrual() is True
    assert cds.paysAtDefaultTime() is True
    assert cds.rebatesAccrual() is True
    assert not cds.isExpired()
    assert len(cds.coupons()) > 0
    assert cds.protectionStartDate() < cds.protectionEndDate()


def test_creditdefaultswap_pricing(cds_env):
    """Test CDS pricing with MidPointCdsEngine."""
    cds = ql.CreditDefaultSwap(
        ql.ProtectionSide.Buyer,
        10_000_000.0,
        0.01,
        cds_env["schedule"],
        ql.Following,
        ql.Actual360(),
    )
    engine = ql.MidPointCdsEngine(
        cds_env["default_curve"],
        0.4,
        cds_env["discount_curve"],
    )
    cds.setPricingEngine(engine)

    npv = cds.NPV()
    assert isinstance(npv, float)
    fair_spread = cds.fairSpread()
    assert fair_spread == pytest.approx(0.005933, rel=1e-4)
    assert cds.couponLegNPV() == pytest.approx(-484773.1637, rel=1e-4)
    assert cds.defaultLegNPV() == pytest.approx(287595.2454, rel=1e-4)


def test_creditdefaultswap_fair_spread(cds_env):
    """Test CDS at fair spread has near-zero NPV."""
    cds = ql.CreditDefaultSwap(
        ql.ProtectionSide.Buyer,
        10_000_000.0,
        0.01,
        cds_env["schedule"],
        ql.Following,
        ql.Actual360(),
    )
    engine = ql.MidPointCdsEngine(
        cds_env["default_curve"],
        0.4,
        cds_env["discount_curve"],
    )
    cds.setPricingEngine(engine)

    fair_spread = cds.fairSpread()

    # Create CDS at fair spread
    fair_cds = ql.CreditDefaultSwap(
        ql.ProtectionSide.Buyer,
        10_000_000.0,
        fair_spread,
        cds_env["schedule"],
        ql.Following,
        ql.Actual360(),
    )
    fair_cds.setPricingEngine(engine)

    assert abs(fair_cds.NPV()) < 1.0  # near zero for 10M notional


def test_cdsmaturity():
    """Test cdsMaturity free function."""
    trade_date = ql.Date(15, ql.January, 2025)
    tenor = ql.Period(5, ql.Years)
    maturity = ql.cdsMaturity(trade_date, tenor, ql.DateGeneration.CDS)
    assert maturity > trade_date


# ---------------------------------------------------------------------------
# Claim
# ---------------------------------------------------------------------------


def test_facevalueclaim_construction():
    """Test FaceValueClaim construction."""
    claim = ql.FaceValueClaim()
    assert claim is not None


def test_facevalueclaim_amount():
    """Test FaceValueClaim returns notional * (1 - recoveryRate)."""
    claim = ql.FaceValueClaim()
    d = ql.Date(15, ql.May, 2007)
    assert claim.amount(d, 1_000_000.0, 0.4) == pytest.approx(600_000.0)
    assert claim.amount(d, 1_000_000.0, 0.0) == pytest.approx(1_000_000.0)
    assert claim.amount(d, 1_000_000.0, 1.0) == pytest.approx(0.0)


def test_facevalueaccrualclaim_construction():
    """Test FaceValueAccrualClaim construction with reference bond."""
    ql.Settings.evaluationDate = ql.Date(15, ql.January, 2025)
    schedule = ql.Schedule(
        ql.Date(15, ql.January, 2025), ql.Date(15, ql.January, 2030),
        ql.Period(ql.Annual), ql.TARGET(),
        ql.Unadjusted, ql.Unadjusted, ql.DateGeneration.Backward, False,
    )
    bond = ql.FixedRateBond(2, 1_000_000.0, schedule, [0.05],
                            ql.Actual365Fixed())
    claim = ql.FaceValueAccrualClaim(bond)
    assert claim is not None


def test_creditdefaultswap_with_claim(cds_env):
    """Test CDS construction with explicit claim parameter."""
    claim = ql.FaceValueClaim()
    cds = ql.CreditDefaultSwap(
        ql.ProtectionSide.Seller,
        10_000_000.0,
        0.0150,
        cds_env["schedule"],
        ql.Following,
        ql.Actual365Fixed(),
        claim=claim,
    )
    assert cds is not None
    assert cds.notional() == 10_000_000.0


# ---------------------------------------------------------------------------
# Inflation instruments (Session 3)
# ---------------------------------------------------------------------------


@pytest.fixture()
def inflation_env():
    """Common setup for inflation instrument tests."""
    saved = ql.Settings.instance().evaluationDate
    today = ql.Date(15, ql.January, 2025)
    ql.Settings.instance().evaluationDate = today
    calendar = ql.TARGET()
    dc = ql.Actual365Fixed()
    obs_lag = ql.Period(3, ql.Months)
    maturity = today + ql.Period(5, ql.Years)

    # Zero-coupon inflation index
    zero_idx = ql.USCPI()
    zero_idx.addFixing(ql.Date(1, ql.October, 2024), 315.0)

    # Year-on-year inflation index
    yoy_idx = ql.YoYInflationIndex(ql.USCPI())

    # Schedules
    fixed_schedule = ql.MakeSchedule(
        today, maturity, tenor=ql.Period(1, ql.Years), calendar=calendar,
    )
    yoy_schedule = ql.MakeSchedule(
        today, maturity, tenor=ql.Period(1, ql.Years), calendar=calendar,
    )

    env = {
        "today": today,
        "calendar": calendar,
        "dc": dc,
        "obs_lag": obs_lag,
        "maturity": maturity,
        "zero_idx": zero_idx,
        "yoy_idx": yoy_idx,
        "fixed_schedule": fixed_schedule,
        "yoy_schedule": yoy_schedule,
        "nominal": 1_000_000.0,
        "fixed_rate": 0.025,
    }
    yield env
    ql.Settings.instance().evaluationDate = saved


# -- ZeroCouponInflationSwap ------------------------------------------------


def test_zerocouponinflationswap_construction(inflation_env):
    """ZeroCouponInflationSwap can be constructed."""
    e = inflation_env
    zcis = ql.ZeroCouponInflationSwap(
        ql.SwapType.Payer,
        e["nominal"],
        e["today"],
        e["maturity"],
        e["calendar"],
        ql.ModifiedFollowing,
        e["dc"],
        e["fixed_rate"],
        e["zero_idx"],
        e["obs_lag"],
        ql.CPI.Flat,
    )
    assert zcis is not None


def test_zerocouponinflationswap_type(inflation_env):
    """ZeroCouponInflationSwap reports correct swap type."""
    e = inflation_env
    payer = ql.ZeroCouponInflationSwap(
        ql.SwapType.Payer,
        e["nominal"],
        e["today"],
        e["maturity"],
        e["calendar"],
        ql.ModifiedFollowing,
        e["dc"],
        e["fixed_rate"],
        e["zero_idx"],
        e["obs_lag"],
        ql.CPI.Flat,
    )
    receiver = ql.ZeroCouponInflationSwap(
        ql.SwapType.Receiver,
        e["nominal"],
        e["today"],
        e["maturity"],
        e["calendar"],
        ql.ModifiedFollowing,
        e["dc"],
        e["fixed_rate"],
        e["zero_idx"],
        e["obs_lag"],
        ql.CPI.Flat,
    )
    assert payer.type() == ql.SwapType.Payer
    assert receiver.type() == ql.SwapType.Receiver


def test_zerocouponinflationswap_inspectors(inflation_env):
    """ZeroCouponInflationSwap inspectors return expected values."""
    e = inflation_env
    zcis = ql.ZeroCouponInflationSwap(
        ql.SwapType.Payer,
        e["nominal"],
        e["today"],
        e["maturity"],
        e["calendar"],
        ql.ModifiedFollowing,
        e["dc"],
        e["fixed_rate"],
        e["zero_idx"],
        e["obs_lag"],
        ql.CPI.Flat,
    )
    assert zcis.nominal() == pytest.approx(e["nominal"])
    assert zcis.fixedRate() == pytest.approx(e["fixed_rate"])
    assert zcis.observationLag() == e["obs_lag"]
    assert zcis.observationInterpolation() == ql.CPI.Flat
    assert zcis.dayCounter() == e["dc"]
    assert zcis.inflationIndex() is not None


def test_zerocouponinflationswap_legs(inflation_env):
    """ZeroCouponInflationSwap has fixed and inflation legs."""
    e = inflation_env
    zcis = ql.ZeroCouponInflationSwap(
        ql.SwapType.Payer,
        e["nominal"],
        e["today"],
        e["maturity"],
        e["calendar"],
        ql.ModifiedFollowing,
        e["dc"],
        e["fixed_rate"],
        e["zero_idx"],
        e["obs_lag"],
        ql.CPI.Flat,
    )
    assert len(zcis.fixedLeg()) > 0
    assert len(zcis.inflationLeg()) > 0


# -- YearOnYearInflationSwap ------------------------------------------------


def _make_yoy_swap(e, swap_type=None, spread=0.0):
    """Helper to build a YearOnYearInflationSwap from the inflation_env."""
    if swap_type is None:
        swap_type = ql.SwapType.Payer
    return ql.YearOnYearInflationSwap(
        swap_type,
        e["nominal"],
        e["fixed_schedule"],
        e["fixed_rate"],
        e["dc"],
        e["yoy_schedule"],
        e["yoy_idx"],
        e["obs_lag"],
        ql.CPI.Flat,
        spread,
        e["dc"],
        e["calendar"],
    )


def test_yearonyearinflationswap_construction(inflation_env):
    """YearOnYearInflationSwap can be constructed."""
    yoyswap = _make_yoy_swap(inflation_env)
    assert yoyswap is not None


def test_yearonyearinflationswap_type(inflation_env):
    """YearOnYearInflationSwap reports correct swap type."""
    payer = _make_yoy_swap(inflation_env, ql.SwapType.Payer)
    receiver = _make_yoy_swap(inflation_env, ql.SwapType.Receiver)
    assert payer.type() == ql.SwapType.Payer
    assert receiver.type() == ql.SwapType.Receiver


def test_yearonyearinflationswap_inspectors(inflation_env):
    """YearOnYearInflationSwap inspectors return expected values."""
    e = inflation_env
    yoyswap = _make_yoy_swap(e, spread=0.005)
    assert yoyswap.nominal() == pytest.approx(e["nominal"])
    assert yoyswap.fixedRate() == pytest.approx(e["fixed_rate"])
    assert yoyswap.spread() == pytest.approx(0.005)
    assert yoyswap.observationLag() == e["obs_lag"]
    assert yoyswap.yoyInflationIndex() is not None


def test_yearonyearinflationswap_schedules(inflation_env):
    """YearOnYearInflationSwap returns fixed and yoy schedules."""
    yoyswap = _make_yoy_swap(inflation_env)
    assert yoyswap.fixedSchedule() is not None
    assert yoyswap.yoySchedule() is not None


def test_yearonyearinflationswap_legs(inflation_env):
    """YearOnYearInflationSwap has fixed and yoy legs."""
    yoyswap = _make_yoy_swap(inflation_env)
    assert len(yoyswap.fixedLeg()) > 0
    assert len(yoyswap.yoyLeg()) > 0


# -- YoYInflationCapFloorType enum ------------------------------------------


def test_yoyinflationcapfloortype_values():
    """YoYInflationCapFloorType enum has Cap, Floor, Collar."""
    assert ql.YoYInflationCapFloorType.Cap is not None
    assert ql.YoYInflationCapFloorType.Floor is not None
    assert ql.YoYInflationCapFloorType.Collar is not None
    # Enum values should be distinct
    assert ql.YoYInflationCapFloorType.Cap != ql.YoYInflationCapFloorType.Floor
    assert ql.YoYInflationCapFloorType.Cap != ql.YoYInflationCapFloorType.Collar
    assert ql.YoYInflationCapFloorType.Floor != ql.YoYInflationCapFloorType.Collar


# -- YoYInflationCapFloor ---------------------------------------------------


def _make_yoy_leg(e):
    """Build a YoY inflation leg from inflation_env."""
    leg = ql.yoyInflationLeg(
        e["yoy_schedule"], e["calendar"], e["yoy_idx"], e["obs_lag"], ql.CPI.Flat
    )
    leg.withNotionals([e["nominal"]])
    leg.withPaymentDayCounter(e["dc"])
    return leg.build()


def test_yoyinflationcapfloor_cap_construction(inflation_env):
    """YoYInflationCapFloor can be constructed as a cap."""
    built_leg = _make_yoy_leg(inflation_env)
    capfloor = ql.YoYInflationCapFloor(
        ql.YoYInflationCapFloorType.Cap, built_leg, [0.03]
    )
    assert capfloor is not None
    assert capfloor.type() == ql.YoYInflationCapFloorType.Cap


def test_yoyinflationcapfloor_floor_construction(inflation_env):
    """YoYInflationCapFloor can be constructed as a floor."""
    built_leg = _make_yoy_leg(inflation_env)
    capfloor = ql.YoYInflationCapFloor(
        ql.YoYInflationCapFloorType.Floor, built_leg, [], [0.01]
    )
    assert capfloor is not None
    assert capfloor.type() == ql.YoYInflationCapFloorType.Floor


def test_yoyinflationcapfloor_collar_construction(inflation_env):
    """YoYInflationCapFloor can be constructed as a collar."""
    built_leg = _make_yoy_leg(inflation_env)
    capfloor = ql.YoYInflationCapFloor(
        ql.YoYInflationCapFloorType.Collar, built_leg, [0.03], [0.01]
    )
    assert capfloor is not None
    assert capfloor.type() == ql.YoYInflationCapFloorType.Collar


def test_yoyinflationcapfloor_inspectors(inflation_env):
    """YoYInflationCapFloor inspectors return expected values."""
    e = inflation_env
    built_leg = _make_yoy_leg(e)
    capfloor = ql.YoYInflationCapFloor(
        ql.YoYInflationCapFloorType.Collar, built_leg, [0.03], [0.01]
    )
    assert all(r == pytest.approx(0.03) for r in capfloor.capRates())
    assert all(r == pytest.approx(0.01) for r in capfloor.floorRates())
    assert len(capfloor.capRates()) > 0
    assert len(capfloor.floorRates()) > 0
    assert len(capfloor.yoyLeg()) > 0
    assert capfloor.startDate() is not None
    assert capfloor.maturityDate() is not None


def test_yoyinflationcapfloor_isexpired(inflation_env):
    """YoYInflationCapFloor reports not expired for future-dated instrument."""
    built_leg = _make_yoy_leg(inflation_env)
    capfloor = ql.YoYInflationCapFloor(
        ql.YoYInflationCapFloorType.Cap, built_leg, [0.03]
    )
    assert capfloor.isExpired() is False


# -- YoYInflationCap / Floor / Collar convenience classes --------------------


def test_yoyinflationcap_construction(inflation_env):
    """YoYInflationCap convenience class constructs a cap."""
    built_leg = _make_yoy_leg(inflation_env)
    cap = ql.YoYInflationCap(built_leg, [0.03])
    assert cap is not None
    assert cap.type() == ql.YoYInflationCapFloorType.Cap


def test_yoyinflationfloor_construction(inflation_env):
    """YoYInflationFloor convenience class constructs a floor."""
    built_leg = _make_yoy_leg(inflation_env)
    floor = ql.YoYInflationFloor(built_leg, [0.01])
    assert floor is not None
    assert floor.type() == ql.YoYInflationCapFloorType.Floor


def test_yoyinflationcollar_construction(inflation_env):
    """YoYInflationCollar convenience class constructs a collar."""
    built_leg = _make_yoy_leg(inflation_env)
    collar = ql.YoYInflationCollar(built_leg, [0.03], [0.01])
    assert collar is not None
    assert collar.type() == ql.YoYInflationCapFloorType.Collar


def test_yoyinflationcap_inherits_capfloor(inflation_env):
    """YoYInflationCap is a YoYInflationCapFloor."""
    built_leg = _make_yoy_leg(inflation_env)
    cap = ql.YoYInflationCap(built_leg, [0.03])
    assert isinstance(cap, ql.YoYInflationCapFloor)


def test_yoyinflationfloor_inherits_capfloor(inflation_env):
    """YoYInflationFloor is a YoYInflationCapFloor."""
    built_leg = _make_yoy_leg(inflation_env)
    floor = ql.YoYInflationFloor(built_leg, [0.01])
    assert isinstance(floor, ql.YoYInflationCapFloor)


def test_yoyinflationcollar_inherits_capfloor(inflation_env):
    """YoYInflationCollar is a YoYInflationCapFloor."""
    built_leg = _make_yoy_leg(inflation_env)
    collar = ql.YoYInflationCollar(built_leg, [0.03], [0.01])
    assert isinstance(collar, ql.YoYInflationCapFloor)


# -- MakeYoYInflationCapFloor (Python wrapper) ------------------------------


def test_makeyoyinflationcapfloor_cap(inflation_env):
    """MakeYoYInflationCapFloor constructs a cap."""
    e = inflation_env
    cap = ql.MakeYoYInflationCapFloor(
        ql.YoYInflationCapFloorType.Cap,
        e["yoy_idx"],
        5,
        e["calendar"],
        e["obs_lag"],
        ql.CPI.Flat,
        strike=0.03,
    )
    assert cap is not None
    assert isinstance(cap, ql.YoYInflationCapFloor)
    assert cap.type() == ql.YoYInflationCapFloorType.Cap


def test_makeyoyinflationcapfloor_floor(inflation_env):
    """MakeYoYInflationCapFloor constructs a floor."""
    e = inflation_env
    floor = ql.MakeYoYInflationCapFloor(
        ql.YoYInflationCapFloorType.Floor,
        e["yoy_idx"],
        5,
        e["calendar"],
        e["obs_lag"],
        ql.CPI.Flat,
        strike=0.01,
    )
    assert floor is not None
    assert isinstance(floor, ql.YoYInflationCapFloor)
    assert floor.type() == ql.YoYInflationCapFloorType.Floor


# =============================================================================
# VarianceSwap
# =============================================================================


@pytest.fixture
def variance_swap_env():
    """Common environment for VarianceSwap tests."""
    today = ql.Date(15, ql.January, 2025)
    ql.Settings.evaluationDate = today
    dc = ql.Actual365Fixed()
    calendar = ql.TARGET()

    spot = ql.SimpleQuote(100.0)
    r_rate = ql.SimpleQuote(0.05)
    q_rate = ql.SimpleQuote(0.02)
    vol = ql.SimpleQuote(0.20)

    r_ts = ql.FlatForward(today, ql.QuoteHandle(r_rate), dc)
    q_ts = ql.FlatForward(today, ql.QuoteHandle(q_rate), dc)
    vol_ts = ql.BlackConstantVol(today, calendar, ql.QuoteHandle(vol), dc)

    process = ql.BlackScholesMertonProcess(
        ql.QuoteHandle(spot),
        ql.YieldTermStructureHandle(q_ts),
        ql.YieldTermStructureHandle(r_ts),
        ql.BlackVolTermStructureHandle(vol_ts),
    )

    maturity = calendar.advance(today, ql.Period("1Y"))
    call_strikes = [float(x) for x in range(100, 150, 5)]
    put_strikes = [float(x) for x in range(55, 105, 5)]
    engine = ql.ReplicatingVarianceSwapEngine(process, 5.0, call_strikes, put_strikes)

    return {
        "today": today,
        "calendar": calendar,
        "maturity": maturity,
        "engine": engine,
    }


def test_varianceswap_construction(variance_swap_env):
    """VarianceSwap constructs and inspectors return correct values."""
    env = variance_swap_env
    vs = ql.VarianceSwap(
        ql.PositionType.Long, 0.04, 10000.0, env["today"], env["maturity"],
    )
    assert vs.position() == ql.PositionType.Long
    assert vs.strike() == 0.04
    assert vs.notional() == 10000.0
    assert vs.startDate() == env["today"]
    assert vs.maturityDate() == env["maturity"]


def test_varianceswap_pricing(variance_swap_env):
    """VarianceSwap prices correctly with ReplicatingVarianceSwapEngine."""
    env = variance_swap_env
    vs = ql.VarianceSwap(
        ql.PositionType.Long, 0.04, 10000.0, env["today"], env["maturity"],
    )
    vs.setPricingEngine(env["engine"])
    assert vs.NPV() == pytest.approx(-14.5142243643, rel=1e-4)
    assert vs.variance() == pytest.approx(0.0384741615, rel=1e-6)


def test_varianceswap_is_instrument(variance_swap_env):
    """VarianceSwap inherits from Instrument."""
    env = variance_swap_env
    vs = ql.VarianceSwap(
        ql.PositionType.Long, 0.04, 10000.0, env["today"], env["maturity"],
    )
    assert isinstance(vs, ql.base.Instrument)


# =============================================================================
# NonstandardSwap
# =============================================================================


@pytest.fixture
def nonstandard_swap_env():
    """Common environment for NonstandardSwap tests."""
    today = ql.Date(15, ql.January, 2025)
    ql.Settings.evaluationDate = today
    calendar = ql.TARGET()
    dc = ql.Actual365Fixed()

    r_ts = ql.FlatForward(today, 0.03, dc)
    r_handle = ql.YieldTermStructureHandle(r_ts)

    start = calendar.advance(today, ql.Period("6M"))
    maturity = calendar.advance(start, ql.Period("5Y"))

    fixed_schedule = ql.MakeSchedule(
        effectiveDate=start, terminationDate=maturity,
        tenor=ql.Period("1Y"), calendar=calendar,
        convention=ql.ModifiedFollowing,
    )
    float_schedule = ql.MakeSchedule(
        effectiveDate=start, terminationDate=maturity,
        tenor=ql.Period("6M"), calendar=calendar,
        convention=ql.ModifiedFollowing,
    )

    n_fixed = len(fixed_schedule) - 1
    n_float = len(float_schedule) - 1

    euribor = ql.Euribor6M(r_handle)
    engine = ql.DiscountingSwapEngine(r_handle)

    return {
        "today": today,
        "calendar": calendar,
        "r_handle": r_handle,
        "fixed_schedule": fixed_schedule,
        "float_schedule": float_schedule,
        "n_fixed": n_fixed,
        "n_float": n_float,
        "euribor": euribor,
        "engine": engine,
    }


def test_nonstandardswap_vector_construction(nonstandard_swap_env):
    """NonstandardSwap vector constructor produces correct NPV."""
    env = nonstandard_swap_env
    ns = ql.NonstandardSwap(
        ql.SwapType.Payer,
        [1000000.0] * env["n_fixed"],
        [1000000.0] * env["n_float"],
        env["fixed_schedule"],
        [0.02] * env["n_fixed"],
        ql.Thirty360(ql.Thirty360.BondBasis),
        env["float_schedule"],
        env["euribor"],
        [1.0] * env["n_float"],
        [0.0] * env["n_float"],
        ql.Actual360(),
    )
    ns.setPricingEngine(env["engine"])
    assert ns.NPV() == pytest.approx(47184.5644691210, rel=1e-4)
    assert ns.type() == ql.SwapType.Payer
    assert len(ns.fixedNominal()) == env["n_fixed"]
    assert len(ns.floatingNominal()) == env["n_float"]
    assert len(ns.fixedRate()) == env["n_fixed"]
    assert len(ns.gearings()) == env["n_float"]
    assert len(ns.spreads()) == env["n_float"]


def test_nonstandardswap_scalar_construction(nonstandard_swap_env):
    """NonstandardSwap scalar gearing/spread constructor works."""
    env = nonstandard_swap_env
    ns = ql.NonstandardSwap(
        ql.SwapType.Payer,
        [1000000.0] * env["n_fixed"],
        [1000000.0] * env["n_float"],
        env["fixed_schedule"],
        [0.02] * env["n_fixed"],
        ql.Thirty360(ql.Thirty360.BondBasis),
        env["float_schedule"],
        env["euribor"],
        1.0,
        0.0,
        ql.Actual360(),
    )
    ns.setPricingEngine(env["engine"])
    assert ns.NPV() == pytest.approx(47184.5644691210, rel=1e-4)
    assert ns.spread() == pytest.approx(0.0, abs=1e-15)
    assert ns.gearing() == pytest.approx(1.0, rel=1e-15)


def test_nonstandardswap_from_vanilla(nonstandard_swap_env):
    """NonstandardSwap constructed from VanillaSwap matches its NPV."""
    env = nonstandard_swap_env
    vanilla = ql.MakeVanillaSwap(ql.Period("5Y"), env["euribor"], fixedRate=0.02)
    vanilla.setPricingEngine(env["engine"])

    ns = ql.NonstandardSwap(vanilla)
    ns.setPricingEngine(env["engine"])
    assert ns.NPV() == pytest.approx(vanilla.NPV(), rel=1e-10)


def test_nonstandardswap_inspectors(nonstandard_swap_env):
    """NonstandardSwap inspectors return schedules and day counters."""
    env = nonstandard_swap_env
    ns = ql.NonstandardSwap(
        ql.SwapType.Payer,
        [1000000.0] * env["n_fixed"],
        [1000000.0] * env["n_float"],
        env["fixed_schedule"],
        [0.02] * env["n_fixed"],
        ql.Thirty360(ql.Thirty360.BondBasis),
        env["float_schedule"],
        env["euribor"],
        [1.0] * env["n_float"],
        [0.0] * env["n_float"],
        ql.Actual360(),
    )
    assert ns.fixedSchedule() is not None
    assert ns.floatingSchedule() is not None
    assert ns.fixedDayCount() is not None
    assert ns.floatingDayCount() is not None
    assert ns.iborIndex() is not None
    assert len(ns.fixedLeg()) == env["n_fixed"]
    assert len(ns.floatingLeg()) == env["n_float"]


# =============================================================================
# FloatFloatSwap
# =============================================================================


@pytest.fixture
def floatfloat_swap_env():
    """Common environment for FloatFloatSwap tests."""
    today = ql.Date(15, ql.January, 2025)
    ql.Settings.evaluationDate = today
    calendar = ql.TARGET()
    dc = ql.Actual365Fixed()

    r_ts = ql.FlatForward(today, 0.03, dc)
    r_handle = ql.YieldTermStructureHandle(r_ts)

    start = calendar.advance(today, ql.Period("6M"))
    maturity = calendar.advance(start, ql.Period("5Y"))

    schedule = ql.MakeSchedule(
        effectiveDate=start, terminationDate=maturity,
        tenor=ql.Period("6M"), calendar=calendar,
        convention=ql.ModifiedFollowing,
    )

    euribor = ql.Euribor6M(r_handle)
    engine = ql.DiscountingSwapEngine(r_handle)
    n = len(schedule) - 1

    return {
        "today": today,
        "schedule": schedule,
        "euribor": euribor,
        "engine": engine,
        "n": n,
    }


def test_floatfloatswap_no_spread(floatfloat_swap_env):
    """FloatFloatSwap with same index both legs and no spread has zero NPV."""
    env = floatfloat_swap_env
    ffs = ql.FloatFloatSwap(
        ql.SwapType.Payer,
        1000000.0, 1000000.0,
        env["schedule"], env["euribor"], ql.Actual360(),
        env["schedule"], env["euribor"], ql.Actual360(),
    )
    ffs.setPricingEngine(env["engine"])
    assert ffs.NPV() == pytest.approx(0.0, abs=1e-8)


def test_floatfloatswap_with_spread(floatfloat_swap_env):
    """FloatFloatSwap with spread on leg 1 has nonzero NPV."""
    env = floatfloat_swap_env
    ffs = ql.FloatFloatSwap(
        ql.SwapType.Payer,
        1000000.0, 1000000.0,
        env["schedule"], env["euribor"], ql.Actual360(),
        env["schedule"], env["euribor"], ql.Actual360(),
        spread1=0.005,
    )
    ffs.setPricingEngine(env["engine"])
    assert ffs.NPV() == pytest.approx(-23028.2725428915, rel=1e-4)


def test_floatfloatswap_vector_construction(floatfloat_swap_env):
    """FloatFloatSwap vector constructor produces zero NPV for symmetric legs."""
    env = floatfloat_swap_env
    n = env["n"]
    ffs = ql.FloatFloatSwap(
        ql.SwapType.Payer,
        [1000000.0] * n, [1000000.0] * n,
        env["schedule"], env["euribor"], ql.Actual360(),
        env["schedule"], env["euribor"], ql.Actual360(),
    )
    ffs.setPricingEngine(env["engine"])
    assert ffs.NPV() == pytest.approx(0.0, abs=1e-8)


def test_floatfloatswap_inspectors(floatfloat_swap_env):
    """FloatFloatSwap inspectors return correct values."""
    env = floatfloat_swap_env
    ffs = ql.FloatFloatSwap(
        ql.SwapType.Payer,
        1000000.0, 1000000.0,
        env["schedule"], env["euribor"], ql.Actual360(),
        env["schedule"], env["euribor"], ql.Actual360(),
    )
    assert ffs.type() == ql.SwapType.Payer
    assert len(ffs.nominal1()) == env["n"]
    assert ffs.nominal1()[0] == 1000000.0
    assert len(ffs.nominal2()) == env["n"]
    assert len(ffs.leg1()) == env["n"]
    assert len(ffs.leg2()) == env["n"]
    assert ffs.schedule1() is not None
    assert ffs.schedule2() is not None
    assert ffs.index1() is not None
    assert ffs.index2() is not None
    assert ffs.dayCount1() is not None
    assert ffs.dayCount2() is not None


# =============================================================================
# NonstandardSwaption
# =============================================================================


def test_nonstandardswaption_construction(nonstandard_swap_env):
    """NonstandardSwaption construction with default settlement."""
    env = nonstandard_swap_env
    ns = ql.NonstandardSwap(
        ql.SwapType.Payer,
        [1000000.0] * env["n_fixed"],
        [1000000.0] * env["n_float"],
        env["fixed_schedule"],
        [0.02] * env["n_fixed"],
        ql.Thirty360(ql.Thirty360.BondBasis),
        env["float_schedule"],
        env["euribor"],
        [1.0] * env["n_float"],
        [0.0] * env["n_float"],
        ql.Actual360(),
    )
    exercise_date = env["fixed_schedule"].dates()[0]
    exercise = ql.EuropeanExercise(exercise_date)

    swaption = ql.NonstandardSwaption(ns, exercise)
    assert swaption is not None
    assert swaption.settlementType() == ql.SettlementType.Physical
    assert swaption.settlementMethod() == ql.SettlementMethod.PhysicalOTC
    assert swaption.type() == ql.SwapType.Payer


def test_nonstandardswaption_cash_settlement(nonstandard_swap_env):
    """NonstandardSwaption with cash settlement."""
    env = nonstandard_swap_env
    ns = ql.NonstandardSwap(
        ql.SwapType.Receiver,
        [1000000.0] * env["n_fixed"],
        [1000000.0] * env["n_float"],
        env["fixed_schedule"],
        [0.04] * env["n_fixed"],
        ql.Thirty360(ql.Thirty360.BondBasis),
        env["float_schedule"],
        env["euribor"],
        1.0, 0.0,
        ql.Actual360(),
    )
    exercise_date = env["fixed_schedule"].dates()[0]
    exercise = ql.EuropeanExercise(exercise_date)

    swaption = ql.NonstandardSwaption(
        ns, exercise,
        ql.SettlementType.Cash,
        ql.SettlementMethod.ParYieldCurve,
    )
    assert swaption.settlementType() == ql.SettlementType.Cash
    assert swaption.settlementMethod() == ql.SettlementMethod.ParYieldCurve
    assert swaption.type() == ql.SwapType.Receiver


def test_nonstandardswaption_underlying(nonstandard_swap_env):
    """NonstandardSwaption underlying accessor returns the swap."""
    env = nonstandard_swap_env
    ns = ql.NonstandardSwap(
        ql.SwapType.Payer,
        [1000000.0] * env["n_fixed"],
        [1000000.0] * env["n_float"],
        env["fixed_schedule"],
        [0.03] * env["n_fixed"],
        ql.Thirty360(ql.Thirty360.BondBasis),
        env["float_schedule"],
        env["euribor"],
        1.0, 0.0,
        ql.Actual360(),
    )
    exercise_date = env["fixed_schedule"].dates()[0]
    exercise = ql.EuropeanExercise(exercise_date)

    swaption = ql.NonstandardSwaption(ns, exercise)
    underlying = swaption.underlyingSwap()
    assert underlying is not None
    assert underlying.fixedRate()[0] == pytest.approx(0.03, rel=1e-15)


def test_nonstandardswaption_from_swaption(nonstandard_swap_env):
    """NonstandardSwaption constructed from a standard Swaption."""
    env = nonstandard_swap_env
    vanilla = ql.MakeVanillaSwap(ql.Period("5Y"), env["euribor"], fixedRate=0.02)
    exercise_date = env["fixed_schedule"].dates()[0]
    exercise = ql.EuropeanExercise(exercise_date)

    std_swaption = ql.Swaption(vanilla, exercise)
    ns_swaption = ql.NonstandardSwaption(std_swaption)
    assert ns_swaption is not None
    assert ns_swaption.type() == ql.SwapType.Payer


def test_nonstandardswaption_is_expired(nonstandard_swap_env):
    """NonstandardSwaption isExpired returns False for future exercise."""
    env = nonstandard_swap_env
    ns = ql.NonstandardSwap(
        ql.SwapType.Payer,
        [1000000.0] * env["n_fixed"],
        [1000000.0] * env["n_float"],
        env["fixed_schedule"],
        [0.02] * env["n_fixed"],
        ql.Thirty360(ql.Thirty360.BondBasis),
        env["float_schedule"],
        env["euribor"],
        1.0, 0.0,
        ql.Actual360(),
    )
    exercise_date = env["fixed_schedule"].dates()[0]
    exercise = ql.EuropeanExercise(exercise_date)

    swaption = ql.NonstandardSwaption(ns, exercise)
    assert swaption.isExpired() is False


# =============================================================================
# FloatFloatSwaption
# =============================================================================


def test_floatfloatswaption_construction(floatfloat_swap_env):
    """FloatFloatSwaption construction with default settlement."""
    env = floatfloat_swap_env
    ffs = ql.FloatFloatSwap(
        ql.SwapType.Payer,
        1000000.0, 1000000.0,
        env["schedule"], env["euribor"], ql.Actual360(),
        env["schedule"], env["euribor"], ql.Actual360(),
    )
    exercise_date = env["schedule"].dates()[0]
    exercise = ql.EuropeanExercise(exercise_date)

    swaption = ql.FloatFloatSwaption(ffs, exercise)
    assert swaption is not None
    assert swaption.settlementType() == ql.SettlementType.Physical
    assert swaption.settlementMethod() == ql.SettlementMethod.PhysicalOTC
    assert swaption.type() == ql.SwapType.Payer


def test_floatfloatswaption_cash_settlement(floatfloat_swap_env):
    """FloatFloatSwaption with cash settlement."""
    env = floatfloat_swap_env
    ffs = ql.FloatFloatSwap(
        ql.SwapType.Receiver,
        1000000.0, 1000000.0,
        env["schedule"], env["euribor"], ql.Actual360(),
        env["schedule"], env["euribor"], ql.Actual360(),
    )
    exercise_date = env["schedule"].dates()[0]
    exercise = ql.EuropeanExercise(exercise_date)

    swaption = ql.FloatFloatSwaption(
        ffs, exercise,
        ql.SettlementType.Cash,
        ql.SettlementMethod.CollateralizedCashPrice,
    )
    assert swaption.settlementType() == ql.SettlementType.Cash
    assert swaption.settlementMethod() == ql.SettlementMethod.CollateralizedCashPrice
    assert swaption.type() == ql.SwapType.Receiver


def test_floatfloatswaption_underlying(floatfloat_swap_env):
    """FloatFloatSwaption underlying accessor returns the swap."""
    env = floatfloat_swap_env
    ffs = ql.FloatFloatSwap(
        ql.SwapType.Payer,
        1000000.0, 1000000.0,
        env["schedule"], env["euribor"], ql.Actual360(),
        env["schedule"], env["euribor"], ql.Actual360(),
        spread1=0.005,
    )
    exercise_date = env["schedule"].dates()[0]
    exercise = ql.EuropeanExercise(exercise_date)

    swaption = ql.FloatFloatSwaption(ffs, exercise)
    underlying = swaption.underlyingSwap()
    assert underlying is not None
    assert underlying.type() == ql.SwapType.Payer


def test_floatfloatswaption_is_expired(floatfloat_swap_env):
    """FloatFloatSwaption isExpired returns False for future exercise."""
    env = floatfloat_swap_env
    ffs = ql.FloatFloatSwap(
        ql.SwapType.Payer,
        1000000.0, 1000000.0,
        env["schedule"], env["euribor"], ql.Actual360(),
        env["schedule"], env["euribor"], ql.Actual360(),
    )
    exercise_date = env["schedule"].dates()[0]
    exercise = ql.EuropeanExercise(exercise_date)

    swaption = ql.FloatFloatSwaption(ffs, exercise)
    assert swaption.isExpired() is False


# =============================================================================
# EquityTotalReturnSwap
# =============================================================================


@pytest.fixture
def equity_trs_env():
    """Shared setup for EquityTotalReturnSwap tests."""
    ql.Settings.evaluationDate = ql.Date(15, ql.January, 2025)
    rate_curve = ql.FlatForward(
        ql.Date(15, ql.January, 2025), 0.05, ql.Actual365Fixed()
    )
    div_curve = ql.FlatForward(
        ql.Date(15, ql.January, 2025), 0.02, ql.Actual365Fixed()
    )
    spot = ql.SimpleQuote(100.0)
    ei = ql.EquityIndex(
        "SPX", ql.TARGET(), ql.USDCurrency(), rate_curve, div_curve, spot
    )
    ei.addFixing(ql.Date(15, ql.January, 2025), 100.0)

    euribor = ql.Euribor6M(rate_curve)
    euribor.addFixing(ql.Date(13, ql.January, 2025), 0.04)

    schedule = ql.MakeSchedule(
        effectiveDate=ql.Date(15, ql.January, 2025),
        terminationDate=ql.Date(15, ql.January, 2026),
        tenor=ql.Period(6, ql.Months),
        calendar=ql.TARGET(),
        convention=ql.ModifiedFollowing,
    )

    return {
        "rate_curve": rate_curve,
        "div_curve": div_curve,
        "spot": spot,
        "ei": ei,
        "euribor": euribor,
        "schedule": schedule,
    }


def test_equitytrs_ibor_construction(equity_trs_env):
    """EquityTotalReturnSwap constructs with IborIndex."""
    env = equity_trs_env
    trs = ql.EquityTotalReturnSwap(
        ql.SwapType.Payer,
        1000000.0,
        env["schedule"],
        env["ei"],
        env["euribor"],
        ql.Actual360(),
        0.005,
    )
    assert trs.type() == ql.SwapType.Payer
    assert trs.nominal() == pytest.approx(1000000.0)
    assert trs.margin() == pytest.approx(0.005)
    assert trs.gearing() == pytest.approx(1.0)
    assert trs.paymentDelay() == 0


def test_equitytrs_ibor_npv(equity_trs_env):
    """EquityTotalReturnSwap NPV with IborIndex and DiscountingSwapEngine."""
    env = equity_trs_env
    trs = ql.EquityTotalReturnSwap(
        ql.SwapType.Payer,
        1000000.0,
        env["schedule"],
        env["ei"],
        env["euribor"],
        ql.Actual360(),
        0.005,
    )
    engine = ql.DiscountingSwapEngine(env["rate_curve"])
    trs.setPricingEngine(engine)

    assert trs.NPV() == pytest.approx(19813.5065, rel=1e-4)
    assert trs.equityLegNPV() == pytest.approx(-28969.2488, rel=1e-4)
    assert trs.interestRateLegNPV() == pytest.approx(48782.7553, rel=1e-4)


def test_equitytrs_fair_margin(equity_trs_env):
    """EquityTotalReturnSwap fairMargin computation."""
    env = equity_trs_env
    trs = ql.EquityTotalReturnSwap(
        ql.SwapType.Payer,
        1000000.0,
        env["schedule"],
        env["ei"],
        env["euribor"],
        ql.Actual360(),
        0.005,
    )
    engine = ql.DiscountingSwapEngine(env["rate_curve"])
    trs.setPricingEngine(engine)

    assert trs.fairMargin() == pytest.approx(-0.01529, rel=1e-3)


def test_equitytrs_inspectors(equity_trs_env):
    """EquityTotalReturnSwap inspectors return correct values."""
    env = equity_trs_env
    trs = ql.EquityTotalReturnSwap(
        ql.SwapType.Payer,
        1000000.0,
        env["schedule"],
        env["ei"],
        env["euribor"],
        ql.Actual360(),
        0.005,
    )
    assert trs.equityIndex().name() == "SPX"
    assert "Euribor" in trs.interestRateIndex().name()
    assert trs.dayCounter().name() == "Actual/360"
    assert len(trs.equityLeg()) == 1
    assert len(trs.interestRateLeg()) == 2


def test_equitytrs_overnight_index():
    """EquityTotalReturnSwap constructs with OvernightIndex (SOFR)."""
    ql.Settings.evaluationDate = ql.Date(15, ql.January, 2025)
    rate_curve = ql.FlatForward(
        ql.Date(15, ql.January, 2025), 0.05, ql.Actual365Fixed()
    )
    div_curve = ql.FlatForward(
        ql.Date(15, ql.January, 2025), 0.02, ql.Actual365Fixed()
    )
    spot = ql.SimpleQuote(100.0)
    ei = ql.EquityIndex(
        "SPX", ql.TARGET(), ql.USDCurrency(), rate_curve, div_curve, spot
    )
    ei.addFixing(ql.Date(15, ql.January, 2025), 100.0)

    sofr = ql.Sofr(rate_curve)
    schedule = ql.MakeSchedule(
        effectiveDate=ql.Date(15, ql.January, 2025),
        terminationDate=ql.Date(15, ql.January, 2026),
        tenor=ql.Period(3, ql.Months),
        calendar=ql.UnitedStates(ql.UnitedStates.GovernmentBond),
        convention=ql.ModifiedFollowing,
    )

    trs = ql.EquityTotalReturnSwap(
        ql.SwapType.Receiver,
        1000000.0,
        schedule,
        ei,
        sofr,
        ql.Actual360(),
        0.01,
    )
    engine = ql.DiscountingSwapEngine(rate_curve)
    trs.setPricingEngine(engine)

    assert trs.NPV() == pytest.approx(-29629.2367, rel=1e-4)
    assert trs.type() == ql.SwapType.Receiver
    assert trs.fairMargin() == pytest.approx(-0.02015, rel=1e-3)


def test_equitytrs_receiver_vs_payer(equity_trs_env):
    """Receiver and Payer TRS have opposite NPVs."""
    env = equity_trs_env
    engine = ql.DiscountingSwapEngine(env["rate_curve"])

    payer_trs = ql.EquityTotalReturnSwap(
        ql.SwapType.Payer, 1000000.0,
        env["schedule"], env["ei"], env["euribor"],
        ql.Actual360(), 0.005,
    )
    payer_trs.setPricingEngine(engine)

    receiver_trs = ql.EquityTotalReturnSwap(
        ql.SwapType.Receiver, 1000000.0,
        env["schedule"], env["ei"], env["euribor"],
        ql.Actual360(), 0.005,
    )
    receiver_trs.setPricingEngine(engine)

    assert payer_trs.NPV() == pytest.approx(-receiver_trs.NPV(), rel=1e-10)


# =============================================================================
# Callability
# =============================================================================


def test_callability_type_enum():
    """CallabilityType enum exposes Call and Put."""
    assert ql.CallabilityType.Call is not None
    assert ql.CallabilityType.Put is not None
    assert ql.CallabilityType.Call != ql.CallabilityType.Put


def test_callability_call_construction():
    """Callability can be constructed as a Call."""
    price = ql.BondPrice(100.0, ql.BondPriceType.Clean)
    call = ql.Callability(price, ql.CallabilityType.Call, ql.Date(15, ql.June, 2030))

    assert call.type() == ql.CallabilityType.Call
    assert call.date() == ql.Date(15, ql.June, 2030)
    assert call.price().amount() == pytest.approx(100.0)
    assert call.price().type() == ql.BondPriceType.Clean


def test_callability_put_construction():
    """Callability can be constructed as a Put."""
    price = ql.BondPrice(95.0, ql.BondPriceType.Dirty)
    put = ql.Callability(price, ql.CallabilityType.Put, ql.Date(15, ql.March, 2028))

    assert put.type() == ql.CallabilityType.Put
    assert put.date() == ql.Date(15, ql.March, 2028)
    assert put.price().amount() == pytest.approx(95.0)
    assert put.price().type() == ql.BondPriceType.Dirty


def test_callability_schedule_list():
    """A list of Callability objects can be used as CallabilitySchedule."""
    dates = [ql.Date(15, ql.June, y) for y in range(2027, 2031)]
    schedule = [
        ql.Callability(ql.BondPrice(100.0, ql.BondPriceType.Clean),
                       ql.CallabilityType.Call, d)
        for d in dates
    ]
    assert len(schedule) == 4
    assert schedule[0].date() == ql.Date(15, ql.June, 2027)
    assert schedule[-1].date() == ql.Date(15, ql.June, 2030)


# =============================================================================
# FloatingTypePayoff
# =============================================================================


def test_floatingtypepayoff_construction():
    """FloatingTypePayoff can be constructed with Call or Put."""
    call = ql.FloatingTypePayoff(ql.Call)
    put = ql.FloatingTypePayoff(ql.Put)
    assert call is not None
    assert put is not None


# =============================================================================
# ContinuousFloatingLookbackOption
# =============================================================================


def test_continuousfloatinglookback_construction():
    """ContinuousFloatingLookbackOption can be constructed."""
    payoff = ql.FloatingTypePayoff(ql.Call)
    exercise = ql.EuropeanExercise(ql.Date(15, ql.January, 2026))
    option = ql.ContinuousFloatingLookbackOption(100.0, payoff, exercise)
    assert option is not None


# =============================================================================
# ContinuousFixedLookbackOption
# =============================================================================


def test_continuousfixedlookback_construction():
    """ContinuousFixedLookbackOption can be constructed."""
    payoff = ql.PlainVanillaPayoff(ql.Call, 100.0)
    exercise = ql.EuropeanExercise(ql.Date(15, ql.January, 2026))
    option = ql.ContinuousFixedLookbackOption(100.0, payoff, exercise)
    assert option is not None


# =============================================================================
# ContinuousPartialFloatingLookbackOption
# =============================================================================


def test_continuouspartialfloatinglookback_construction():
    """ContinuousPartialFloatingLookbackOption can be constructed."""
    payoff = ql.FloatingTypePayoff(ql.Call)
    exercise = ql.EuropeanExercise(ql.Date(15, ql.January, 2026))
    lookback_end = ql.Date(15, ql.July, 2025)
    option = ql.ContinuousPartialFloatingLookbackOption(
        100.0, 1.0, lookback_end, payoff, exercise
    )
    assert option is not None


# =============================================================================
# ContinuousPartialFixedLookbackOption
# =============================================================================


def test_continuouspartialfixedlookback_construction():
    """ContinuousPartialFixedLookbackOption can be constructed."""
    payoff = ql.PlainVanillaPayoff(ql.Call, 100.0)
    exercise = ql.EuropeanExercise(ql.Date(15, ql.January, 2026))
    lookback_start = ql.Date(15, ql.July, 2025)
    option = ql.ContinuousPartialFixedLookbackOption(
        lookback_start, payoff, exercise
    )
    assert option is not None


# =============================================================================
# CliquetOption
# =============================================================================


def test_cliquetoption_construction():
    """CliquetOption can be constructed with reset dates."""
    payoff = ql.PercentageStrikePayoff(ql.Call, 1.0)
    exercise = ql.EuropeanExercise(ql.Date(15, ql.January, 2026))
    reset_dates = [
        ql.Date(15, ql.April, 2025),
        ql.Date(15, ql.July, 2025),
        ql.Date(15, ql.October, 2025),
    ]
    option = ql.CliquetOption(payoff, exercise, reset_dates)
    assert option is not None


# =============================================================================
# CompoundOption
# =============================================================================


def test_compoundoption_construction():
    """CompoundOption can be constructed with mother/daughter pairs."""
    mother_payoff = ql.PlainVanillaPayoff(ql.Call, 5.0)
    mother_exercise = ql.EuropeanExercise(ql.Date(15, ql.July, 2025))
    daughter_payoff = ql.PlainVanillaPayoff(ql.Call, 100.0)
    daughter_exercise = ql.EuropeanExercise(ql.Date(15, ql.January, 2026))

    option = ql.CompoundOption(
        mother_payoff, mother_exercise, daughter_payoff, daughter_exercise
    )
    assert option is not None


# =============================================================================
# SimpleChooserOption
# =============================================================================


def test_simplechooseroption_construction():
    """SimpleChooserOption can be constructed."""
    choosing_date = ql.Date(15, ql.July, 2025)
    exercise = ql.EuropeanExercise(ql.Date(15, ql.January, 2026))
    option = ql.SimpleChooserOption(choosing_date, 100.0, exercise)
    assert option is not None


# =============================================================================
# ComplexChooserOption
# =============================================================================


def test_complexchooseroption_construction():
    """ComplexChooserOption can be constructed."""
    choosing_date = ql.Date(15, ql.July, 2025)
    call_exercise = ql.EuropeanExercise(ql.Date(15, ql.January, 2026))
    put_exercise = ql.EuropeanExercise(ql.Date(15, ql.July, 2026))
    option = ql.ComplexChooserOption(
        choosing_date, 100.0, 105.0, call_exercise, put_exercise
    )
    assert option is not None
