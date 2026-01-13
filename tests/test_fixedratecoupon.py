import pytest

import pyquantlib as ql


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
    interest_rate = ql.InterestRate(0.05, ql.Actual360(), ql.Simple, ql.Annual)
    start_date = leg_data["schedule"][0]
    end_date = leg_data["schedule"][1]

    coupon = ql.FixedRateCoupon(end_date, 1000.0, interest_rate, start_date, end_date)

    assert isinstance(coupon, ql.base.Coupon)
    assert isinstance(coupon, ql.base.CashFlow)
    assert isinstance(coupon, ql.base.Event)
    assert isinstance(coupon, ql.Observable)


def test_fixedrateleg_builder(leg_data):
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
    schedule = leg_data["schedule"]

    leg = ql.FixedRateLeg(schedule) \
            .withNotionals(leg_data["nominal"]) \
            .withCouponRates(leg_data["rate"], leg_data["day_counter"]) \
            .build()

    assert len(leg) == 4
    assert leg[0].nominal() == pytest.approx(leg_data["nominal"])
    assert leg[0].rate() == pytest.approx(leg_data["rate"])


def test_fixedrateleg_multiple_rates(leg_data):
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
