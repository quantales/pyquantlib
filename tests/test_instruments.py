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
    assert ois is not None


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
    assert ois is not None


def test_makeois_atm(ois_setup):
    """Test MakeOIS with no fixed rate (ATM)."""
    ois = ql.MakeOIS(ql.Period(1, ql.Years), ois_setup["sofr"])
    assert ois is not None


def test_makeois_kwargs_nominal(ois_setup):
    """Test MakeOIS with nominal kwarg."""
    ois = ql.MakeOIS(
        ql.Period(1, ql.Years), ois_setup["sofr"], 0.035,
        nominal=5_000_000.0,
    )
    assert ois is not None


def test_makeois_kwargs_swap_type(ois_setup):
    """Test MakeOIS with swapType kwarg."""
    ois = ql.MakeOIS(
        ql.Period(1, ql.Years), ois_setup["sofr"], 0.035,
        swapType=ql.SwapType.Receiver,
    )
    assert ois is not None


def test_makeois_kwargs_receive_fixed(ois_setup):
    """Test MakeOIS with receiveFixed kwarg."""
    ois = ql.MakeOIS(
        ql.Period(1, ql.Years), ois_setup["sofr"], 0.035,
        receiveFixed=True,
    )
    assert ois is not None


def test_makeois_kwargs_pricing_engine(ois_setup):
    """Test MakeOIS with pricingEngine kwarg."""
    engine = ql.DiscountingSwapEngine(ois_setup["curve"])
    ois = ql.MakeOIS(
        ql.Period(1, ql.Years), ois_setup["sofr"], 0.035,
        pricingEngine=engine,
    )
    assert ois is not None


def test_makeois_kwargs_multiple(ois_setup):
    """Test MakeOIS with multiple kwargs."""
    engine = ql.DiscountingSwapEngine(ois_setup["curve"])
    ois = ql.MakeOIS(
        ql.Period(1, ql.Years), ois_setup["sofr"], 0.035,
        nominal=2_000_000.0, paymentLag=2, pricingEngine=engine,
    )
    assert ois is not None


def test_makeois_kwargs_forward_start(ois_setup):
    """Test MakeOIS with forward start."""
    ois = ql.MakeOIS(
        ql.Period(1, ql.Years), ois_setup["sofr"], 0.035,
        fwdStart=ql.Period(3, ql.Months),
    )
    assert ois is not None


def test_makeois_kwargs_fixed_leg_daycount(ois_setup):
    """Test MakeOIS with fixedLegDayCount kwarg."""
    ois = ql.MakeOIS(
        ql.Period(1, ql.Years), ois_setup["sofr"], 0.035,
        fixedLegDayCount=ql.Actual365Fixed(),
    )
    assert ois is not None


def test_makeois_kwargs_overnight_spread(ois_setup):
    """Test MakeOIS with overnightLegSpread kwarg."""
    ois = ql.MakeOIS(
        ql.Period(1, ql.Years), ois_setup["sofr"], 0.035,
        overnightLegSpread=0.001,
    )
    assert ois is not None


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
    assert ois is not None


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
    assert cap.NPV() > 0


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
    assert cap is not None


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
    assert cap.NPV() > 0


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
    assert cap.NPV() > 0


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
    assert swap.NPV() != 0


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
    assert swaption is not None


def test_makeswaption_kwargs_nominal(mswn_env):
    """Test MakeSwaption with nominal kwarg."""
    swaption = ql.MakeSwaption(
        mswn_env["swap_index"],
        ql.Period(1, ql.Years),
        0.05,
        nominal=5_000_000.0,
    )
    assert swaption is not None


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
    assert fair_payment > 0


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
    assert fair_spread > 0
    assert cds.couponLegNPV() != 0
    assert cds.defaultLegNPV() != 0


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
