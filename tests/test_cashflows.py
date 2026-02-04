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
