import pytest
import pyquantlib as ql


def test_coupon_abc_exists():
    assert hasattr(ql.base, 'Coupon')


def test_python_custom_coupon():
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


def test_incomplete_python_coupon_raises():
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
