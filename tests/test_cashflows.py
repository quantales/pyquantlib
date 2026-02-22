"""
Tests for cashflows module.

Corresponds to src/cashflows/*.cpp bindings.
"""

import pytest

import pyquantlib as ql

# =============================================================================
# Event / CashFlow (ABC)
# =============================================================================


def test_event_abc_exists():
    """Test Event ABC is accessible."""
    assert hasattr(ql.base, 'Event')


def test_cashflow_abc_exists():
    """Test CashFlow ABC is accessible."""
    assert hasattr(ql.base, 'CashFlow')


def test_cashflow_zombie():
    """Direct instantiation creates a zombie object."""
    zombie = ql.base.CashFlow()

    with pytest.raises(RuntimeError, match="Tried to call pure virtual function"):
        zombie.amount()

    with pytest.raises(RuntimeError, match="Tried to call pure virtual function"):
        zombie.date()


def test_cashflow_python_custom():
    """Test Python subclass implementing virtual methods."""

    class CustomCashFlow(ql.base.CashFlow):
        def __init__(self, amount, date):
            super().__init__()
            self._amount = amount
            self._date = date

        def amount(self):
            return self._amount

        def date(self):
            return self._date

    cf = CustomCashFlow(100.0, ql.Date(15, 5, 2024))

    assert cf.amount() == pytest.approx(100.0)
    assert cf.date() == ql.Date(15, 5, 2024)
    assert cf.hasOccurred(ql.Date(16, 5, 2024))


def test_cashflow_incomplete_python_raises():
    """Test incomplete Python subclass raises error."""

    class IncompleteCashFlow(ql.base.CashFlow):
        def __init__(self, date):
            super().__init__()
            self._date = date

        def date(self):
            return self._date

    cf = IncompleteCashFlow(ql.Date(1, 1, 2025))

    assert cf.date() == ql.Date(1, 1, 2025)

    with pytest.raises(RuntimeError, match="Tried to call pure virtual function"):
        cf.amount()


# =============================================================================
# SimpleCashFlow
# =============================================================================


def test_simplecashflow_construction():
    """Test SimpleCashFlow construction."""
    cf = ql.SimpleCashFlow(100.0, ql.Date(15, 5, 2024))

    assert cf.amount() == pytest.approx(100.0)
    assert cf.date() == ql.Date(15, 5, 2024)


def test_simplecashflow_isinstance():
    """Test SimpleCashFlow inheritance."""
    cf = ql.SimpleCashFlow(100.0, ql.Date(15, 5, 2024))
    assert isinstance(cf, ql.base.CashFlow)


def test_simplecashflow_has_occurred():
    """Test SimpleCashFlow hasOccurred method."""
    date = ql.Date(15, 5, 2024)
    cf = ql.SimpleCashFlow(100.0, date)

    # Default includeRefDate=false: date() <= refDate
    assert cf.hasOccurred(date)

    # includeRefDate=true: date() < refDate (strict)
    assert not cf.hasOccurred(date, True)

    # After/before event date
    assert cf.hasOccurred(date + ql.Period("1D"))
    assert not cf.hasOccurred(date - ql.Period("1D"))


# =============================================================================
# Redemption
# =============================================================================


def test_redemption_construction():
    """Test Redemption construction."""
    cf = ql.Redemption(1000.0, ql.Date(31, 12, 2025))

    assert cf.amount() == pytest.approx(1000.0)
    assert cf.date() == ql.Date(31, 12, 2025)


def test_redemption_inheritance():
    """Test Redemption inheritance hierarchy."""
    cf = ql.Redemption(1000.0, ql.Date(31, 12, 2025))
    assert isinstance(cf, ql.SimpleCashFlow)
    assert isinstance(cf, ql.base.CashFlow)


# =============================================================================
# AmortizingPayment
# =============================================================================


def test_amortizingpayment_construction():
    """Test AmortizingPayment construction."""
    cf = ql.AmortizingPayment(75.50, ql.Date(30, 6, 2025))

    assert cf.amount() == pytest.approx(75.50)
    assert cf.date() == ql.Date(30, 6, 2025)


def test_amortizingpayment_inheritance():
    """Test AmortizingPayment inheritance hierarchy."""
    cf = ql.AmortizingPayment(75.50, ql.Date(30, 6, 2025))
    assert isinstance(cf, ql.SimpleCashFlow)
    assert isinstance(cf, ql.base.CashFlow)


# =============================================================================
# CashFlow Polymorphism
# =============================================================================


def test_cashflow_polymorphism():
    """Test CashFlow polymorphism with Python and C++ classes."""

    def get_amount(cf: ql.base.CashFlow) -> float:
        return cf.amount()

    date = ql.Date(1, 1, 2025)

    simple = ql.SimpleCashFlow(100.0, date)
    redemption = ql.Redemption(1000.0, date)
    amortizing = ql.AmortizingPayment(75.50, date)

    class PythonCashFlow(ql.base.CashFlow):
        def amount(self):
            return 250.0

        def date(self):
            return ql.Date(1, 1, 2025)

    python_cf = PythonCashFlow()

    assert get_amount(simple) == pytest.approx(100.0)
    assert get_amount(redemption) == pytest.approx(1000.0)
    assert get_amount(amortizing) == pytest.approx(75.50)
    assert get_amount(python_cf) == pytest.approx(250.0)


# =============================================================================
# Coupon (ABC)
# =============================================================================


def test_coupon_abc_exists():
    """Test Coupon ABC is accessible."""
    assert hasattr(ql.base, 'Coupon')


def test_coupon_python_custom():
    """Test Python subclass implementing virtual methods only."""
    day_counter = ql.Actual365Fixed()

    class MyCoupon(ql.base.Coupon):
        def __init__(self, nom, rate_val, dc):
            super().__init__()
            self._nominal = nom
            self._rate = rate_val
            self._daycounter = dc

        # Virtual methods only
        def date(self):
            return ql.Date(1, 1, 2024)

        def amount(self):
            return self._nominal * self._rate

        def nominal(self):
            return self._nominal

        def rate(self):
            return self._rate

        def dayCounter(self):
            return self._daycounter

        def accruedAmount(self, date):
            return self._nominal * self._rate * 0.5

    nominal_val = 1000.0
    rate_val = 0.05

    coupon = MyCoupon(nominal_val, rate_val, day_counter)

    assert coupon.nominal() == pytest.approx(nominal_val)
    assert coupon.rate() == pytest.approx(rate_val)
    assert coupon.dayCounter().name() == day_counter.name()
    assert coupon.date() == ql.Date(1, 1, 2024)
    assert coupon.amount() == pytest.approx(nominal_val * rate_val)
    assert coupon.accruedAmount(ql.Date(1, 7, 2023)) == pytest.approx(nominal_val * rate_val * 0.5)


def test_coupon_incomplete_python_raises():
    """Test that missing virtual method raises error."""

    class IncompleteCoupon(ql.base.Coupon):
        def __init__(self):
            super().__init__()

        def date(self):
            return ql.Date(1, 1, 2025)

        def amount(self):
            return 100.0

        def rate(self):
            return 0.05

        def dayCounter(self):
            return ql.Actual365Fixed()

        def accruedAmount(self, date):
            return 50.0

        # Missing: nominal()

    coupon = IncompleteCoupon()

    assert coupon.rate() == 0.05

    with pytest.raises(RuntimeError, match="Tried to call pure virtual function"):
        coupon.nominal()


# =============================================================================
# FixedRateCoupon
# =============================================================================


@pytest.fixture(scope="module")
def leg_data():
    """Common data for fixed rate leg tests."""
    calendar = ql.TARGET()
    effective_date = ql.Date(15, 1, 2022)
    termination_date = ql.Date(15, 1, 2024)
    tenor = ql.Period("6M")

    schedule = ql.Schedule(
        effective_date, termination_date, tenor, calendar,
        ql.Unadjusted, ql.Unadjusted, ql.DateGeneration.Forward, False
    )

    return {
        "schedule": schedule,
        "nominal": 1000000.0,
        "rate": 0.05,
        "day_counter": ql.Actual360()
    }


def test_fixedratecoupon_construction(leg_data):
    """Test FixedRateCoupon construction."""
    nominal = leg_data["nominal"]
    rate = leg_data["rate"]
    dc = leg_data["day_counter"]

    interest_rate = ql.InterestRate(rate, dc, ql.Simple, ql.Semiannual)

    start_date = leg_data["schedule"][0]
    end_date = leg_data["schedule"][1]

    coupon = ql.FixedRateCoupon(
        end_date, nominal, interest_rate, start_date, end_date
    )

    assert coupon.nominal() == pytest.approx(nominal)
    assert coupon.rate() == pytest.approx(rate)
    assert coupon.date() == end_date
    assert coupon.accrualStartDate() == start_date
    assert coupon.accrualEndDate() == end_date
    assert coupon.dayCounter().name() == dc.name()


def test_fixedratecoupon_inheritance(leg_data):
    """Test FixedRateCoupon inheritance hierarchy."""
    interest_rate = ql.InterestRate(0.05, ql.Actual360(), ql.Simple, ql.Annual)
    start_date = leg_data["schedule"][0]
    end_date = leg_data["schedule"][1]

    coupon = ql.FixedRateCoupon(end_date, 1000.0, interest_rate, start_date, end_date)

    assert isinstance(coupon, ql.base.Coupon)
    assert isinstance(coupon, ql.base.CashFlow)
    assert isinstance(coupon, ql.base.Event)
    assert isinstance(coupon, ql.Observable)


# =============================================================================
# FixedRateLeg
# =============================================================================


def test_fixedrateleg_builder(leg_data):
    """Test FixedRateLeg builder pattern."""
    schedule = leg_data["schedule"]
    nominal = leg_data["nominal"]
    rate = leg_data["rate"]
    day_counter = leg_data["day_counter"]

    leg_builder = ql.FixedRateLeg(schedule)
    leg_builder.withNotionals(nominal)
    leg_builder.withCouponRates(rate, day_counter)
    leg_builder.withPaymentAdjustment(ql.Following)

    fixed_leg = leg_builder.build()

    assert len(fixed_leg) == 4

    first_coupon = fixed_leg[0]
    assert isinstance(first_coupon, ql.FixedRateCoupon)
    assert first_coupon.nominal() == pytest.approx(nominal)
    assert first_coupon.rate() == pytest.approx(rate)


def test_fixedrateleg_chaining(leg_data):
    """Test FixedRateLeg method chaining."""
    schedule = leg_data["schedule"]

    leg = ql.FixedRateLeg(schedule) \
            .withNotionals(leg_data["nominal"]) \
            .withCouponRates(leg_data["rate"], leg_data["day_counter"]) \
            .build()

    assert len(leg) == 4
    assert leg[0].nominal() == pytest.approx(leg_data["nominal"])
    assert leg[0].rate() == pytest.approx(leg_data["rate"])


def test_fixedrateleg_multiple_rates(leg_data):
    """Test FixedRateLeg with multiple rates."""
    schedule = leg_data["schedule"]
    nominal = leg_data["nominal"]
    day_counter = leg_data["day_counter"]
    rates = [0.05, 0.06, 0.07, 0.08]

    leg = ql.FixedRateLeg(schedule) \
            .withNotionals(nominal) \
            .withCouponRates(rates, day_counter) \
            .build()

    assert len(leg) == 4
    for i, coupon in enumerate(leg):
        assert coupon.rate() == pytest.approx(rates[i])


def test_fixedrateleg_multiple_notionals(leg_data):
    """Test FixedRateLeg with multiple notionals."""
    schedule = leg_data["schedule"]
    rate = leg_data["rate"]
    day_counter = leg_data["day_counter"]
    notionals = [1000000.0, 2000000.0, 5000000.0, 8000000.0]

    leg = ql.FixedRateLeg(schedule) \
            .withNotionals(notionals) \
            .withCouponRates(rate, day_counter) \
            .build()

    assert len(leg) == 4
    for i, coupon in enumerate(leg):
        assert coupon.nominal() == pytest.approx(notionals[i])


# =============================================================================
# FloatingRateCouponPricer (ABC)
# =============================================================================


def test_floatingratecouponpricer_base_exists():
    """Test FloatingRateCouponPricer ABC is accessible."""
    assert hasattr(ql.base, "FloatingRateCouponPricer")


# =============================================================================
# BlackIborCouponPricer
# =============================================================================


def test_blackiborcouponpricer_construction():
    """Test BlackIborCouponPricer default construction."""
    pricer = ql.BlackIborCouponPricer()
    assert pricer is not None
    assert isinstance(pricer, ql.base.FloatingRateCouponPricer)


# =============================================================================
# FloatingRateCoupon
# =============================================================================


@pytest.fixture(scope="module")
def ibor_data():
    """Common data for floating rate coupon tests."""
    original_date = ql.Settings.instance().evaluationDate
    today = ql.Date(15, ql.May, 2025)
    ql.Settings.instance().evaluationDate = today

    calendar = ql.TARGET()
    day_counter = ql.Actual360()

    rate_curve = ql.FlatForward(today, 0.03, ql.Actual365Fixed())
    index = ql.Euribor6M(rate_curve)

    effective_date = ql.Date(15, ql.May, 2025)
    termination_date = ql.Date(15, ql.May, 2027)
    tenor = ql.Period("6M")

    schedule = ql.Schedule(
        effective_date, termination_date, tenor, calendar,
        ql.ModifiedFollowing, ql.ModifiedFollowing,
        ql.DateGeneration.Forward, False
    )

    yield {
        "schedule": schedule,
        "index": index,
        "nominal": 1_000_000.0,
        "day_counter": day_counter,
        "rate_curve": rate_curve,
        "calendar": calendar,
        "today": today,
    }

    ql.Settings.instance().evaluationDate = original_date


def test_floatingratecoupon_construction(ibor_data):
    """Test FloatingRateCoupon construction."""
    schedule = ibor_data["schedule"]
    index = ibor_data["index"]
    nominal = ibor_data["nominal"]

    coupon = ql.FloatingRateCoupon(
        schedule[1], nominal, schedule[0], schedule[1],
        2, index
    )

    assert coupon.nominal() == pytest.approx(nominal)
    assert coupon.fixingDays() == 2
    assert coupon.gearing() == pytest.approx(1.0)
    assert coupon.spread() == pytest.approx(0.0)
    assert not coupon.isInArrears()


def test_floatingratecoupon_inheritance(ibor_data):
    """Test FloatingRateCoupon inheritance hierarchy."""
    schedule = ibor_data["schedule"]
    coupon = ql.FloatingRateCoupon(
        schedule[1], 1_000_000.0, schedule[0], schedule[1],
        2, ibor_data["index"]
    )
    assert isinstance(coupon, ql.base.Coupon)
    assert isinstance(coupon, ql.base.CashFlow)


def test_floatingratecoupon_with_gearing_spread(ibor_data):
    """Test FloatingRateCoupon with gearing and spread."""
    schedule = ibor_data["schedule"]
    coupon = ql.FloatingRateCoupon(
        schedule[1], 1_000_000.0, schedule[0], schedule[1],
        2, ibor_data["index"],
        gearing=0.5, spread=0.01
    )
    assert coupon.gearing() == pytest.approx(0.5)
    assert coupon.spread() == pytest.approx(0.01)


def test_floatingratecoupon_set_pricer(ibor_data):
    """Test FloatingRateCoupon setPricer."""
    schedule = ibor_data["schedule"]
    coupon = ql.FloatingRateCoupon(
        schedule[1], 1_000_000.0, schedule[0], schedule[1],
        2, ibor_data["index"]
    )
    pricer = ql.BlackIborCouponPricer()
    coupon.setPricer(pricer)
    assert coupon.pricer() is not None


# =============================================================================
# IborCoupon
# =============================================================================


def test_iborcoupon_construction(ibor_data):
    """Test IborCoupon construction."""
    schedule = ibor_data["schedule"]
    index = ibor_data["index"]
    nominal = ibor_data["nominal"]

    coupon = ql.IborCoupon(
        schedule[1], nominal, schedule[0], schedule[1],
        2, index
    )

    assert coupon.nominal() == pytest.approx(nominal)
    assert coupon.fixingDays() == 2
    assert isinstance(coupon, ql.FloatingRateCoupon)
    assert isinstance(coupon, ql.base.Coupon)


def test_iborcoupon_ibor_index(ibor_data):
    """Test IborCoupon iborIndex accessor."""
    schedule = ibor_data["schedule"]
    index = ibor_data["index"]

    coupon = ql.IborCoupon(
        schedule[1], 1_000_000.0, schedule[0], schedule[1],
        2, index
    )

    assert coupon.iborIndex() is not None
    assert coupon.fixingDate() is not None


def test_iborcoupon_fixing_dates(ibor_data):
    """Test IborCoupon fixing date methods."""
    schedule = ibor_data["schedule"]
    coupon = ql.IborCoupon(
        schedule[1], 1_000_000.0, schedule[0], schedule[1],
        2, ibor_data["index"]
    )
    pricer = ql.BlackIborCouponPricer()
    coupon.setPricer(pricer)

    fixing_date = coupon.fixingDate()
    value_date = coupon.fixingValueDate()
    maturity_date = coupon.fixingMaturityDate()
    end_date = coupon.fixingEndDate()

    assert fixing_date < value_date
    assert value_date < maturity_date
    assert end_date <= maturity_date


def test_iborcoupon_rate(ibor_data):
    """Test IborCoupon rate computation with future fixing."""
    # Use a schedule entirely in the future so no past fixings needed
    today = ibor_data["today"]
    calendar = ibor_data["calendar"]
    future_start = calendar.advance(today, ql.Period("6M"))
    future_end = calendar.advance(future_start, ql.Period("6M"))

    coupon = ql.IborCoupon(
        future_end, 1_000_000.0, future_start, future_end,
        2, ibor_data["index"]
    )
    pricer = ql.BlackIborCouponPricer()
    coupon.setPricer(pricer)

    rate = coupon.rate()
    assert rate == pytest.approx(0.029811, rel=1e-4)


# =============================================================================
# IborCoupon::Settings
# =============================================================================


def test_iborcouponsettings_singleton():
    """Test IborCouponSettings singleton access."""
    settings = ql.IborCouponSettings.instance()
    assert settings is not None


def test_iborcouponsettings_par_coupons():
    """Test IborCouponSettings par/indexed coupon switching."""
    settings = ql.IborCouponSettings.instance()

    settings.createAtParCoupons()
    assert settings.usingAtParCoupons()

    settings.createIndexedCoupons()
    assert not settings.usingAtParCoupons()

    # Restore default
    settings.createAtParCoupons()


# =============================================================================
# IborLeg
# =============================================================================


def test_iborleg_builder(ibor_data):
    """Test IborLeg builder pattern."""
    schedule = ibor_data["schedule"]
    index = ibor_data["index"]
    nominal = ibor_data["nominal"]

    leg = ql.IborLeg(schedule, index) \
            .withNotionals(nominal) \
            .build()

    assert len(leg) == 4  # 2 years / 6M = 4 coupons
    first = leg[0]
    assert isinstance(first, ql.IborCoupon)
    assert first.nominal() == pytest.approx(nominal)


def test_iborleg_with_spread(ibor_data):
    """Test IborLeg with spread."""
    schedule = ibor_data["schedule"]
    index = ibor_data["index"]

    leg = ql.IborLeg(schedule, index) \
            .withNotionals(1_000_000.0) \
            .withSpreads(0.005) \
            .build()

    for cf in leg:
        coupon = cf
        assert coupon.spread() == pytest.approx(0.005)


def test_iborleg_with_gearing(ibor_data):
    """Test IborLeg with gearing."""
    schedule = ibor_data["schedule"]
    index = ibor_data["index"]

    leg = ql.IborLeg(schedule, index) \
            .withNotionals(1_000_000.0) \
            .withGearings(0.75) \
            .build()

    for cf in leg:
        coupon = cf
        assert coupon.gearing() == pytest.approx(0.75)


def test_iborleg_with_payment_lag(ibor_data):
    """Test IborLeg with payment lag."""
    schedule = ibor_data["schedule"]
    index = ibor_data["index"]

    leg = ql.IborLeg(schedule, index) \
            .withNotionals(1_000_000.0) \
            .withPaymentLag(2) \
            .build()

    assert len(leg) == 4


def test_iborleg_in_arrears(ibor_data):
    """Test IborLeg in-arrears flag."""
    schedule = ibor_data["schedule"]
    index = ibor_data["index"]

    leg = ql.IborLeg(schedule, index) \
            .withNotionals(1_000_000.0) \
            .inArrears() \
            .build()

    for cf in leg:
        coupon = cf
        assert coupon.isInArrears()


# =============================================================================
# setCouponPricer
# =============================================================================


def test_setcouponpricer(ibor_data):
    """Test setCouponPricer function."""
    # Use a schedule entirely in the future so no past fixings needed
    today = ibor_data["today"]
    calendar = ibor_data["calendar"]
    future_start = calendar.advance(today, ql.Period("6M"))
    future_end = calendar.advance(future_start, ql.Period("2Y"))
    tenor = ql.Period("6M")

    schedule = ql.Schedule(
        future_start, future_end, tenor, calendar,
        ql.ModifiedFollowing, ql.ModifiedFollowing,
        ql.DateGeneration.Forward, False
    )
    index = ibor_data["index"]

    leg = ql.IborLeg(schedule, index) \
            .withNotionals(1_000_000.0) \
            .build()

    pricer = ql.BlackIborCouponPricer()
    ql.setCouponPricer(leg, pricer)

    # Verify pricer was set by computing rate
    for cf in leg:
        coupon = cf
        rate = coupon.rate()
        assert rate == pytest.approx(0.02981, rel=1e-3)


# =============================================================================
# OvernightIndexedCoupon
# =============================================================================


@pytest.fixture(scope="module")
def overnight_data():
    """Common data for overnight coupon tests."""
    original_date = ql.Settings.instance().evaluationDate
    today = ql.Date(15, ql.May, 2025)
    ql.Settings.instance().evaluationDate = today

    calendar = ql.TARGET()
    rate_curve = ql.FlatForward(today, 0.035, ql.Actual365Fixed())
    handle = ql.YieldTermStructureHandle(rate_curve)
    index = ql.OvernightIndex(
        "TESTON", 0, ql.EURCurrency(), calendar,
        ql.Actual360(), handle
    )

    # Use future dates to avoid needing past fixings
    effective_date = calendar.advance(today, ql.Period("6M"))
    termination_date = calendar.advance(effective_date, ql.Period("1Y"))
    tenor = ql.Period("3M")

    schedule = ql.Schedule(
        effective_date, termination_date, tenor, calendar,
        ql.ModifiedFollowing, ql.ModifiedFollowing,
        ql.DateGeneration.Forward, False
    )

    yield {
        "schedule": schedule,
        "index": index,
        "nominal": 10_000_000.0,
        "rate_curve": rate_curve,
        "calendar": calendar,
        "today": today,
    }

    ql.Settings.instance().evaluationDate = original_date


def test_overnightindexedcoupon_construction(overnight_data):
    """Test OvernightIndexedCoupon construction."""
    schedule = overnight_data["schedule"]
    index = overnight_data["index"]
    nominal = overnight_data["nominal"]

    coupon = ql.OvernightIndexedCoupon(
        schedule[1], nominal, schedule[0], schedule[1],
        index
    )

    assert coupon.nominal() == pytest.approx(nominal)
    assert isinstance(coupon, ql.FloatingRateCoupon)
    assert isinstance(coupon, ql.base.Coupon)


def test_overnightindexedcoupon_averaging(overnight_data):
    """Test OvernightIndexedCoupon averaging method."""
    schedule = overnight_data["schedule"]
    index = overnight_data["index"]

    coupon_compound = ql.OvernightIndexedCoupon(
        schedule[1], 10_000_000.0, schedule[0], schedule[1],
        index, averagingMethod=ql.RateAveraging.Type.Compound
    )
    assert coupon_compound.averagingMethod() == ql.RateAveraging.Type.Compound

    coupon_simple = ql.OvernightIndexedCoupon(
        schedule[1], 10_000_000.0, schedule[0], schedule[1],
        index, averagingMethod=ql.RateAveraging.Type.Simple
    )
    assert coupon_simple.averagingMethod() == ql.RateAveraging.Type.Simple


def test_overnightindexedcoupon_fixing_dates(overnight_data):
    """Test OvernightIndexedCoupon fixing dates."""
    schedule = overnight_data["schedule"]
    index = overnight_data["index"]

    coupon = ql.OvernightIndexedCoupon(
        schedule[1], 10_000_000.0, schedule[0], schedule[1],
        index
    )

    fixing_dates = coupon.fixingDates()
    value_dates = coupon.valueDates()
    dt = coupon.dt()

    assert len(fixing_dates) > 0
    assert len(value_dates) > 0
    assert len(dt) > 0


def test_overnightindexedcoupon_with_spread(overnight_data):
    """Test OvernightIndexedCoupon with spread."""
    schedule = overnight_data["schedule"]
    index = overnight_data["index"]

    coupon = ql.OvernightIndexedCoupon(
        schedule[1], 10_000_000.0, schedule[0], schedule[1],
        index, spread=0.002
    )
    assert coupon.spread() == pytest.approx(0.002)


# =============================================================================
# OvernightLeg
# =============================================================================


def test_overnightleg_builder(overnight_data):
    """Test OvernightLeg builder pattern."""
    schedule = overnight_data["schedule"]
    index = overnight_data["index"]
    nominal = overnight_data["nominal"]

    leg = ql.OvernightLeg(schedule, index) \
            .withNotionals(nominal) \
            .build()

    assert len(leg) == 4  # 1 year / 3M = 4 coupons
    first = leg[0]
    assert isinstance(first, ql.OvernightIndexedCoupon)
    assert first.nominal() == pytest.approx(nominal)


def test_overnightleg_with_spread(overnight_data):
    """Test OvernightLeg with spread."""
    schedule = overnight_data["schedule"]
    index = overnight_data["index"]

    leg = ql.OvernightLeg(schedule, index) \
            .withNotionals(10_000_000.0) \
            .withSpreads(0.001) \
            .build()

    for cf in leg:
        coupon = cf
        assert coupon.spread() == pytest.approx(0.001)


def test_overnightleg_simple_averaging(overnight_data):
    """Test OvernightLeg with simple averaging."""
    schedule = overnight_data["schedule"]
    index = overnight_data["index"]

    leg = ql.OvernightLeg(schedule, index) \
            .withNotionals(10_000_000.0) \
            .withAveragingMethod(ql.RateAveraging.Type.Simple) \
            .build()

    for cf in leg:
        coupon = cf
        assert coupon.averagingMethod() == ql.RateAveraging.Type.Simple


# =============================================================================
# CmsCoupon
# =============================================================================


@pytest.fixture(scope="module")
def cms_env():
    """Common data for CMS tests."""
    original_date = ql.Settings.instance().evaluationDate
    today = ql.Date(15, ql.January, 2025)
    ql.Settings.instance().evaluationDate = today
    calendar = ql.TARGET()
    dc = ql.Actual365Fixed()
    flat_curve = ql.FlatForward(today, 0.03, dc)
    curve_handle = ql.YieldTermStructureHandle(flat_curve)

    euribor6m = ql.Euribor6M(curve_handle)
    swap_index = ql.SwapIndex(
        "EuriborSwapIsdaFixA", ql.Period("10Y"), 2,
        ql.EURCurrency(), calendar, ql.Period("1Y"),
        ql.Unadjusted, ql.Thirty360(ql.Thirty360.BondBasis),
        euribor6m, curve_handle,
    )

    yield {
        "today": today,
        "calendar": calendar,
        "dc": dc,
        "flat_curve": flat_curve,
        "curve_handle": curve_handle,
        "euribor6m": euribor6m,
        "swap_index": swap_index,
    }
    ql.Settings.instance().evaluationDate = original_date


def test_cmscoupon_construction(cms_env):
    """Test CmsCoupon construction."""
    d = cms_env
    coupon = ql.CmsCoupon(
        ql.Date(15, ql.July, 2025), 1_000_000.0,
        ql.Date(15, ql.January, 2025), ql.Date(15, ql.July, 2025),
        2, d["swap_index"]
    )
    assert coupon is not None
    assert coupon.nominal() == pytest.approx(1_000_000.0)


def test_cmscoupon_swap_index(cms_env):
    """Test CmsCoupon returns the swap index."""
    d = cms_env
    coupon = ql.CmsCoupon(
        ql.Date(15, ql.July, 2025), 1_000_000.0,
        ql.Date(15, ql.January, 2025), ql.Date(15, ql.July, 2025),
        2, d["swap_index"]
    )
    idx = coupon.swapIndex()
    assert idx is not None


def test_cmscoupon_is_floatingratecoupon(cms_env):
    """Test CmsCoupon inherits FloatingRateCoupon."""
    d = cms_env
    coupon = ql.CmsCoupon(
        ql.Date(15, ql.July, 2025), 1_000_000.0,
        ql.Date(15, ql.January, 2025), ql.Date(15, ql.July, 2025),
        2, d["swap_index"]
    )
    assert coupon.gearing() == pytest.approx(1.0)
    assert coupon.spread() == pytest.approx(0.0)


# =============================================================================
# CmsLeg
# =============================================================================


def test_cmsleg_construction(cms_env):
    """Test CmsLeg builder constructs a leg."""
    d = cms_env
    schedule = ql.Schedule(
        d["today"], d["today"] + ql.Period("2Y"),
        ql.Period("6M"), d["calendar"],
        ql.ModifiedFollowing, ql.ModifiedFollowing,
        ql.DateGeneration.Forward, False
    )
    leg = ql.CmsLeg(schedule, d["swap_index"]) \
            .withNotionals(1_000_000.0) \
            .build()
    assert len(leg) > 0


def test_cmsleg_with_spread(cms_env):
    """Test CmsLeg with spread."""
    d = cms_env
    schedule = ql.Schedule(
        d["today"], d["today"] + ql.Period("2Y"),
        ql.Period("6M"), d["calendar"],
        ql.ModifiedFollowing, ql.ModifiedFollowing,
        ql.DateGeneration.Forward, False
    )
    leg = ql.CmsLeg(schedule, d["swap_index"]) \
            .withNotionals(1_000_000.0) \
            .withSpreads(0.005) \
            .build()
    for cf in leg:
        assert cf.spread() == pytest.approx(0.005)


# =============================================================================
# CmsCouponPricer / MeanRevertingPricer / LinearTsrPricer
# =============================================================================


def test_cmscouponpricer_abc_exists():
    """Test CmsCouponPricer ABC is accessible."""
    assert hasattr(ql.base, "CmsCouponPricer")


def test_meanrevertingpricer_abc_exists():
    """Test MeanRevertingPricer ABC is accessible."""
    assert hasattr(ql.base, "MeanRevertingPricer")


def test_lineartsrpricer_settings():
    """Test LinearTsrPricerSettings construction and builder."""
    settings = ql.LinearTsrPricerSettings()
    assert settings is not None
    settings.withVegaRatio(0.02)
    settings.withBSStdDevs(2.5)


def test_lineartsrpricer_strategy_enum():
    """Test LinearTsrPricerStrategy enum values."""
    assert ql.LinearTsrPricerStrategy.RateBound is not None
    assert ql.LinearTsrPricerStrategy.VegaRatio is not None
    assert ql.LinearTsrPricerStrategy.PriceThreshold is not None
    assert ql.LinearTsrPricerStrategy.BSStdDevs is not None


def test_lineartsrpricer_construction(cms_env):
    """Test LinearTsrPricer construction with hidden handles."""
    d = cms_env
    swaption_vol = ql.ConstantSwaptionVolatility(
        2, d["calendar"], ql.ModifiedFollowing, 0.20, d["dc"]
    )
    mean_reversion = ql.SimpleQuote(0.01)
    pricer = ql.LinearTsrPricer(swaption_vol, mean_reversion)
    assert pricer is not None
    assert pricer.meanReversion() == pytest.approx(0.01)


def test_lineartsrpricer_is_cmscouponpricer(cms_env):
    """Test LinearTsrPricer inherits CmsCouponPricer."""
    d = cms_env
    swaption_vol = ql.ConstantSwaptionVolatility(
        2, d["calendar"], ql.ModifiedFollowing, 0.20, d["dc"]
    )
    mean_reversion = ql.SimpleQuote(0.01)
    pricer = ql.LinearTsrPricer(swaption_vol, mean_reversion)
    assert isinstance(pricer, ql.base.CmsCouponPricer)
    assert isinstance(pricer, ql.base.MeanRevertingPricer)


# ---------------------------------------------------------------------------
# Session 3: Inflation cashflows, coupons, pricers
# ---------------------------------------------------------------------------


@pytest.fixture
def inflation_env():
    """Shared setup for inflation cashflow tests."""
    today = ql.Date(15, ql.January, 2025)
    ql.Settings.instance().evaluationDate = today

    calendar = ql.TARGET()
    dc = ql.Actual365Fixed()
    observation_lag = ql.Period(3, ql.Months)

    # Build a flat yield curve
    flat_rate = ql.FlatForward(today, 0.03, dc)

    # CPI index
    cpi = ql.USCPI()

    # Add a fixing for the index at a date consistent with observation lag
    fixing_date = ql.Date(15, ql.October, 2024)
    cpi.addFixing(fixing_date, 310.0)
    # Add another fixing for a later date
    fixing_date2 = ql.Date(15, ql.January, 2025)
    cpi.addFixing(fixing_date2, 312.0)

    # YoY inflation index from the CPI
    yoy_idx = ql.YoYInflationIndex(cpi)

    # Schedule for legs: 1-year quarterly
    schedule = ql.MakeSchedule(
        effectiveDate=ql.Date(15, ql.January, 2025),
        terminationDate=ql.Date(15, ql.January, 2026),
        tenor=ql.Period(3, ql.Months),
        calendar=calendar,
        convention=ql.ModifiedFollowing,
    )

    env = {
        "today": today,
        "calendar": calendar,
        "dc": dc,
        "observation_lag": observation_lag,
        "flat_rate": flat_rate,
        "cpi": cpi,
        "yoy_idx": yoy_idx,
        "schedule": schedule,
    }
    yield env
    ql.Settings.instance().evaluationDate = ql.Date()
    cpi.clearFixings()
    yoy_idx.clearFixings()


# --- InflationCoupon (ABC) --------------------------------------------------


def test_inflationcoupon_exists_in_base():
    """Test InflationCoupon ABC is accessible on the base submodule."""
    assert hasattr(ql.base, "InflationCoupon")


def test_inflationcoupon_is_coupon():
    """Test InflationCoupon inherits from Coupon."""
    assert issubclass(ql.base.InflationCoupon, ql.base.Coupon)


# --- ZeroInflationCashFlow --------------------------------------------------


def test_zeroinflationcashflow_construction(inflation_env):
    """Test ZeroInflationCashFlow basic construction."""
    d = inflation_env
    notional = 1_000_000.0
    start_date = ql.Date(15, ql.October, 2024)
    end_date = ql.Date(15, ql.January, 2025)
    payment_date = ql.Date(15, ql.January, 2025)

    cf = ql.ZeroInflationCashFlow(
        notional,
        d["cpi"],
        ql.CPI.Flat,
        start_date,
        end_date,
        d["observation_lag"],
        payment_date,
        False,
    )
    assert cf is not None


def test_zeroinflationcashflow_notional(inflation_env):
    """Test ZeroInflationCashFlow notional inspector."""
    d = inflation_env
    notional = 1_000_000.0
    start_date = ql.Date(15, ql.October, 2024)
    end_date = ql.Date(15, ql.January, 2025)
    payment_date = ql.Date(15, ql.January, 2025)

    cf = ql.ZeroInflationCashFlow(
        notional,
        d["cpi"],
        ql.CPI.Flat,
        start_date,
        end_date,
        d["observation_lag"],
        payment_date,
        False,
    )
    assert cf.notional() == pytest.approx(notional)


def test_zeroinflationcashflow_index(inflation_env):
    """Test ZeroInflationCashFlow zeroInflationIndex inspector."""
    d = inflation_env
    start_date = ql.Date(15, ql.October, 2024)
    end_date = ql.Date(15, ql.January, 2025)
    payment_date = ql.Date(15, ql.January, 2025)

    cf = ql.ZeroInflationCashFlow(
        1_000_000.0,
        d["cpi"],
        ql.CPI.Flat,
        start_date,
        end_date,
        d["observation_lag"],
        payment_date,
        False,
    )
    idx = cf.zeroInflationIndex()
    assert idx is not None
    assert idx.name() == d["cpi"].name()


def test_zeroinflationcashflow_growth_only(inflation_env):
    """Test ZeroInflationCashFlow growthOnly flag."""
    d = inflation_env
    start_date = ql.Date(15, ql.October, 2024)
    end_date = ql.Date(15, ql.January, 2025)
    payment_date = ql.Date(15, ql.January, 2025)

    cf_growth = ql.ZeroInflationCashFlow(
        1_000_000.0,
        d["cpi"],
        ql.CPI.Flat,
        start_date,
        end_date,
        d["observation_lag"],
        payment_date,
        True,
    )
    assert cf_growth.growthOnly() is True

    cf_full = ql.ZeroInflationCashFlow(
        1_000_000.0,
        d["cpi"],
        ql.CPI.Flat,
        start_date,
        end_date,
        d["observation_lag"],
        payment_date,
        False,
    )
    assert cf_full.growthOnly() is False


def test_zeroinflationcashflow_is_cashflow(inflation_env):
    """Test ZeroInflationCashFlow inherits from CashFlow."""
    d = inflation_env
    start_date = ql.Date(15, ql.October, 2024)
    end_date = ql.Date(15, ql.January, 2025)
    payment_date = ql.Date(15, ql.January, 2025)

    cf = ql.ZeroInflationCashFlow(
        1_000_000.0,
        d["cpi"],
        ql.CPI.Flat,
        start_date,
        end_date,
        d["observation_lag"],
        payment_date,
        False,
    )
    assert isinstance(cf, ql.base.CashFlow)


def test_zeroinflationcashflow_basedate(inflation_env):
    """Test ZeroInflationCashFlow baseDate inspector."""
    d = inflation_env
    start_date = ql.Date(15, ql.October, 2024)
    end_date = ql.Date(15, ql.January, 2025)
    payment_date = ql.Date(15, ql.January, 2025)

    cf = ql.ZeroInflationCashFlow(
        1_000_000.0,
        d["cpi"],
        ql.CPI.Flat,
        start_date,
        end_date,
        d["observation_lag"],
        payment_date,
        False,
    )
    bd = cf.baseDate()
    assert isinstance(bd, ql.Date)


def test_zeroinflationcashflow_fixingdate(inflation_env):
    """Test ZeroInflationCashFlow fixingDate inspector."""
    d = inflation_env
    start_date = ql.Date(15, ql.October, 2024)
    end_date = ql.Date(15, ql.January, 2025)
    payment_date = ql.Date(15, ql.January, 2025)

    cf = ql.ZeroInflationCashFlow(
        1_000_000.0,
        d["cpi"],
        ql.CPI.Flat,
        start_date,
        end_date,
        d["observation_lag"],
        payment_date,
        False,
    )
    fd = cf.fixingDate()
    assert isinstance(fd, ql.Date)


# --- YoYInflationCoupon -----------------------------------------------------


def test_yoyinflationcoupon_exists():
    """Test YoYInflationCoupon is accessible on the main module."""
    assert hasattr(ql, "YoYInflationCoupon")


def test_yoyinflationcoupon_inherits_inflationcoupon():
    """Test YoYInflationCoupon inherits from InflationCoupon."""
    assert issubclass(ql.YoYInflationCoupon, ql.base.InflationCoupon)


# --- CappedFlooredYoYInflationCoupon ----------------------------------------


def test_cappedfloored_yoy_exists():
    """Test CappedFlooredYoYInflationCoupon is accessible on the main module."""
    assert hasattr(ql, "CappedFlooredYoYInflationCoupon")


def test_cappedfloored_yoy_inherits_yoyinflationcoupon():
    """Test CappedFlooredYoYInflationCoupon inherits from YoYInflationCoupon."""
    assert issubclass(
        ql.CappedFlooredYoYInflationCoupon, ql.YoYInflationCoupon
    )


# --- yoyInflationLeg builder ------------------------------------------------


def test_yoyinflationleg_construction(inflation_env):
    """Test yoyInflationLeg builder construction."""
    d = inflation_env
    leg_builder = ql.yoyInflationLeg(
        d["schedule"],
        d["calendar"],
        d["yoy_idx"],
        d["observation_lag"],
        ql.CPI.Flat,
    )
    assert leg_builder is not None


def test_yoyinflationleg_with_notionals(inflation_env):
    """Test yoyInflationLeg withNotionals method chaining."""
    d = inflation_env
    leg_builder = ql.yoyInflationLeg(
        d["schedule"],
        d["calendar"],
        d["yoy_idx"],
        d["observation_lag"],
        ql.CPI.Flat,
    )
    result = leg_builder.withNotionals([1_000_000.0])
    # Method chaining should return the same builder
    assert result is leg_builder


def test_yoyinflationleg_with_payment_daycounter(inflation_env):
    """Test yoyInflationLeg withPaymentDayCounter method chaining."""
    d = inflation_env
    leg_builder = ql.yoyInflationLeg(
        d["schedule"],
        d["calendar"],
        d["yoy_idx"],
        d["observation_lag"],
        ql.CPI.Flat,
    )
    result = leg_builder.withPaymentDayCounter(ql.Actual365Fixed())
    assert result is leg_builder


def test_yoyinflationleg_with_payment_adjustment(inflation_env):
    """Test yoyInflationLeg withPaymentAdjustment method chaining."""
    d = inflation_env
    leg_builder = ql.yoyInflationLeg(
        d["schedule"],
        d["calendar"],
        d["yoy_idx"],
        d["observation_lag"],
        ql.CPI.Flat,
    )
    result = leg_builder.withPaymentAdjustment(ql.ModifiedFollowing)
    assert result is leg_builder


def test_yoyinflationleg_build(inflation_env):
    """Test yoyInflationLeg build returns a Leg."""
    d = inflation_env
    leg_builder = ql.yoyInflationLeg(
        d["schedule"],
        d["calendar"],
        d["yoy_idx"],
        d["observation_lag"],
        ql.CPI.Flat,
    )
    leg_builder.withNotionals([1_000_000.0])
    leg_builder.withPaymentDayCounter(d["dc"])
    leg_builder.withPaymentAdjustment(ql.ModifiedFollowing)
    built_leg = leg_builder.build()
    assert isinstance(built_leg, list)
    assert len(built_leg) > 0


def test_yoyinflationleg_coupons_are_yoy(inflation_env):
    """Test that built YoY leg coupons are YoYInflationCoupon instances."""
    d = inflation_env
    leg_builder = ql.yoyInflationLeg(
        d["schedule"],
        d["calendar"],
        d["yoy_idx"],
        d["observation_lag"],
        ql.CPI.Flat,
    )
    leg_builder.withNotionals([1_000_000.0])
    leg_builder.withPaymentDayCounter(d["dc"])
    built_leg = leg_builder.build()
    for cf in built_leg:
        assert isinstance(cf, ql.YoYInflationCoupon)
        assert isinstance(cf, ql.base.InflationCoupon)


def test_yoyinflationleg_full_chain(inflation_env):
    """Test yoyInflationLeg with full method chaining."""
    d = inflation_env
    leg_builder = ql.yoyInflationLeg(
        d["schedule"],
        d["calendar"],
        d["yoy_idx"],
        d["observation_lag"],
        ql.CPI.Flat,
    )
    leg_builder.withNotionals([1_000_000.0])
    leg_builder.withPaymentDayCounter(d["dc"])
    leg_builder.withPaymentAdjustment(ql.ModifiedFollowing)
    leg_builder.withFixingDays(2)
    built_leg = leg_builder.build()
    assert len(built_leg) > 0


# --- InflationCoupon inspectors (via YoY coupon) ----------------------------


def test_inflationcoupon_inspectors_via_yoy(inflation_env):
    """Test InflationCoupon inspectors through a built YoY coupon."""
    d = inflation_env
    leg_builder = ql.yoyInflationLeg(
        d["schedule"],
        d["calendar"],
        d["yoy_idx"],
        d["observation_lag"],
        ql.CPI.Flat,
    )
    leg_builder.withNotionals([1_000_000.0])
    leg_builder.withPaymentDayCounter(d["dc"])
    built_leg = leg_builder.build()

    coupon = built_leg[0]

    # observationLag
    lag = coupon.observationLag()
    assert isinstance(lag, ql.Period)

    # fixingDays
    fd = coupon.fixingDays()
    assert isinstance(fd, int)

    # dayCounter
    dc = coupon.dayCounter()
    assert dc is not None

    # index (from InflationCoupon)
    idx = coupon.index()
    assert idx is not None


# --- InflationCouponPricer (ABC) --------------------------------------------


def test_inflationcouponpricer_exists_in_base():
    """Test InflationCouponPricer ABC is accessible on the base submodule."""
    assert hasattr(ql.base, "InflationCouponPricer")


# --- YoYInflationCouponPricer (ABC) -----------------------------------------


def test_yoyinflationcouponpricer_exists():
    """Test YoYInflationCouponPricer is accessible on the main module."""
    assert hasattr(ql, "YoYInflationCouponPricer")


def test_yoyinflationcouponpricer_inherits_inflationcouponpricer():
    """Test YoYInflationCouponPricer inherits from InflationCouponPricer."""
    assert issubclass(
        ql.YoYInflationCouponPricer, ql.base.InflationCouponPricer
    )


# --- BlackYoYInflationCouponPricer ------------------------------------------


def test_blackyoy_pricer_construction_default():
    """Test BlackYoYInflationCouponPricer default construction."""
    pricer = ql.BlackYoYInflationCouponPricer()
    assert pricer is not None


def test_blackyoy_pricer_construction_with_nominal():
    """Test BlackYoYInflationCouponPricer construction with nominal TS."""
    flat_rate = ql.FlatForward(
        ql.Date(15, ql.January, 2025), 0.03, ql.Actual365Fixed()
    )
    nominal_handle = ql.YieldTermStructureHandle(flat_rate)
    pricer = ql.BlackYoYInflationCouponPricer(nominal_handle)
    assert pricer is not None


def test_blackyoy_pricer_construction_with_vol_and_nominal():
    """Test BlackYoYInflationCouponPricer with vol handle and nominal TS."""
    flat_rate = ql.FlatForward(
        ql.Date(15, ql.January, 2025), 0.03, ql.Actual365Fixed()
    )
    nominal_handle = ql.YieldTermStructureHandle(flat_rate)
    vol = ql.ConstantYoYOptionletVolatility(
        0.10, 2, ql.TARGET(), ql.ModifiedFollowing, ql.Actual365Fixed(),
        ql.Period(3, ql.Months), ql.Monthly, False,
    )
    vol_handle = ql.YoYOptionletVolatilitySurfaceHandle(vol)
    pricer = ql.BlackYoYInflationCouponPricer(vol_handle, nominal_handle)
    assert pricer is not None


def test_blackyoy_pricer_inherits_yoypricer():
    """Test BlackYoYInflationCouponPricer inherits from YoYInflationCouponPricer."""
    pricer = ql.BlackYoYInflationCouponPricer()
    assert isinstance(pricer, ql.YoYInflationCouponPricer)
    assert isinstance(pricer, ql.base.InflationCouponPricer)


# --- UnitDisplacedBlackYoYInflationCouponPricer -----------------------------


def test_unitdisplaced_blackyoy_pricer_construction():
    """Test UnitDisplacedBlackYoYInflationCouponPricer default construction."""
    pricer = ql.UnitDisplacedBlackYoYInflationCouponPricer()
    assert pricer is not None


def test_unitdisplaced_blackyoy_pricer_inherits_yoypricer():
    """Test UnitDisplacedBlackYoYInflationCouponPricer inheritance."""
    pricer = ql.UnitDisplacedBlackYoYInflationCouponPricer()
    assert isinstance(pricer, ql.YoYInflationCouponPricer)
    assert isinstance(pricer, ql.base.InflationCouponPricer)


# --- BachelierYoYInflationCouponPricer --------------------------------------


def test_bachelier_yoy_pricer_construction():
    """Test BachelierYoYInflationCouponPricer default construction."""
    pricer = ql.BachelierYoYInflationCouponPricer()
    assert pricer is not None


def test_bachelier_yoy_pricer_inherits_yoypricer():
    """Test BachelierYoYInflationCouponPricer inheritance."""
    pricer = ql.BachelierYoYInflationCouponPricer()
    assert isinstance(pricer, ql.YoYInflationCouponPricer)
    assert isinstance(pricer, ql.base.InflationCouponPricer)


# --- setCouponPricer for inflation ------------------------------------------


def test_setcouponpricer_with_yoy_leg(inflation_env):
    """Test setCouponPricer works with a YoY inflation leg."""
    d = inflation_env
    leg_builder = ql.yoyInflationLeg(
        d["schedule"],
        d["calendar"],
        d["yoy_idx"],
        d["observation_lag"],
        ql.CPI.Flat,
    )
    leg_builder.withNotionals([1_000_000.0])
    leg_builder.withPaymentDayCounter(d["dc"])
    built_leg = leg_builder.build()

    pricer = ql.BlackYoYInflationCouponPricer()
    # Should not raise
    ql.setCouponPricer(built_leg, pricer)

    # Verify pricer is set on each coupon
    for cf in built_leg:
        coupon = cf
        p = coupon.pricer()
        assert p is not None


def test_setcouponpricer_bachelier_with_yoy_leg(inflation_env):
    """Test setCouponPricer with BachelierYoYInflationCouponPricer."""
    d = inflation_env
    leg_builder = ql.yoyInflationLeg(
        d["schedule"],
        d["calendar"],
        d["yoy_idx"],
        d["observation_lag"],
        ql.CPI.Flat,
    )
    leg_builder.withNotionals([1_000_000.0])
    leg_builder.withPaymentDayCounter(d["dc"])
    built_leg = leg_builder.build()

    pricer = ql.BachelierYoYInflationCouponPricer()
    ql.setCouponPricer(built_leg, pricer)

    for cf in built_leg:
        p = cf.pricer()
        assert p is not None


def test_yoy_coupon_set_pricer_directly(inflation_env):
    """Test setPricer on an individual YoY inflation coupon."""
    d = inflation_env
    leg_builder = ql.yoyInflationLeg(
        d["schedule"],
        d["calendar"],
        d["yoy_idx"],
        d["observation_lag"],
        ql.CPI.Flat,
    )
    leg_builder.withNotionals([1_000_000.0])
    leg_builder.withPaymentDayCounter(d["dc"])
    built_leg = leg_builder.build()

    pricer = ql.BlackYoYInflationCouponPricer()
    coupon = built_leg[0]
    coupon.setPricer(pricer)
    assert coupon.pricer() is not None


# =============================================================================
# Dividends (from ql/cashflows/dividend.hpp)
# =============================================================================


def test_fixed_dividend():
    """FixedDividend construction and amount."""
    d = ql.FixedDividend(2.5, ql.Date(15, ql.June, 2025))
    assert d.amount() == pytest.approx(2.5)
    assert d.date() == ql.Date(15, ql.June, 2025)


def test_fractional_dividend_rate_only():
    """FractionalDividend with rate only."""
    d = ql.FractionalDividend(0.03, ql.Date(15, ql.June, 2025))
    assert d.rate() == pytest.approx(0.03)
    assert d.date() == ql.Date(15, ql.June, 2025)


def test_fractional_dividend_with_nominal():
    """FractionalDividend with rate and nominal."""
    d = ql.FractionalDividend(0.03, 100.0, ql.Date(15, ql.June, 2025))
    assert d.amount() == pytest.approx(3.0)
    assert d.rate() == pytest.approx(0.03)
    assert d.nominal() == pytest.approx(100.0)


def test_dividend_vector():
    """DividendVector builds a sequence of fixed dividends."""
    dates = [ql.Date(15, ql.June, 2025), ql.Date(15, ql.December, 2025)]
    amounts = [2.5, 3.0]
    dvec = ql.DividendVector(dates, amounts)
    assert len(dvec) == 2
    assert dvec[0].amount() == pytest.approx(2.5)
    assert dvec[1].amount() == pytest.approx(3.0)


def test_dividend_abc_exists():
    """Dividend ABC is accessible on base."""
    assert hasattr(ql.base, "Dividend")
