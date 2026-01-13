import math

import pytest

import pyquantlib as ql


def test_flatforward_exists():
    """Verify FlatForward is in main module."""
    assert hasattr(ql, 'FlatForward')


def test_flatforward_with_rate():
    """Test FlatForward construction with fixed rate."""
    today = ql.Date(15, 6, 2024)
    dc = ql.Actual365Fixed()
    rate = 0.05
    compounding = ql.Compounded
    frequency = ql.Semiannual

    ff = ql.FlatForward(today, rate, dc, compounding, frequency)

    assert ff.compounding() == compounding
    assert ff.compoundingFrequency() == frequency
    assert ff.referenceDate() == today

    # Check zero rate
    future_date = today + ql.Period(2, ql.Years)
    zero_rate = ff.zeroRate(future_date, dc, compounding, frequency)
    assert zero_rate.rate() == pytest.approx(rate)


def test_flatforward_continuous_discount():
    """Test discount factor with continuous compounding (default)."""
    today = ql.Date(15, 6, 2024)
    dc = ql.Actual365Fixed()
    rate = 0.05

    ff = ql.FlatForward(today, rate, dc)

    future_date = today + ql.Period(1, ql.Years)
    time = dc.yearFraction(today, future_date)
    expected_discount = math.exp(-rate * time)

    assert ff.discount(future_date) == pytest.approx(expected_discount)


def test_flatforward_compounded_discount():
    """Test discount factor with compounded interest."""
    today = ql.Date(15, 6, 2024)
    dc = ql.Actual365Fixed()
    rate = 0.05
    frequency = ql.Semiannual

    ff = ql.FlatForward(today, rate, dc, ql.Compounded, frequency)

    future_date = today + ql.Period(2, ql.Years)
    time = dc.yearFraction(today, future_date)
    f = int(frequency)
    expected_discount = math.pow(1.0 + rate / f, -f * time)

    assert ff.discount(future_date) == pytest.approx(expected_discount)


def test_flatforward_with_quote_handle():
    """Test FlatForward linked to Quote via Handle updates automatically."""
    today = ql.Date(15, 6, 2024)
    dc = ql.Actual365Fixed()

    initial_rate = 0.03
    rate_quote = ql.SimpleQuote(initial_rate)
    rate_handle = ql.QuoteHandle(rate_quote)

    ff = ql.FlatForward(today, rate_handle, dc, ql.Continuous)

    one_year = today + ql.Period(1, ql.Years)
    zero_rate = ff.zeroRate(one_year, dc, ql.Continuous)
    assert zero_rate.rate() == pytest.approx(initial_rate)

    # Change quote value
    new_rate = 0.04
    rate_quote.setValue(new_rate)

    # Curve should update automatically
    zero_rate_updated = ff.zeroRate(one_year, dc, ql.Continuous)
    assert zero_rate_updated.rate() == pytest.approx(new_rate)


def test_flatforward_with_settlement_days():
    """Test FlatForward construction with settlement days."""
    dc = ql.Actual365Fixed()
    calendar = ql.TARGET()
    rate = 0.05

    ff = ql.FlatForward(2, calendar, rate, dc)

    assert ff.settlementDays() == 2
    assert ff.calendar().name() == calendar.name()


def test_flatforward_in_yts_handle():
    """Test FlatForward works with YieldTermStructureHandle."""
    today = ql.Date(15, 6, 2024)
    dc = ql.Actual365Fixed()
    rate = 0.04

    ff = ql.FlatForward(today, rate, dc)
    handle = ql.YieldTermStructureHandle(ff)

    assert not handle.empty()

    retrieved = handle.currentLink()
    future_date = today + ql.Period(1, ql.Years)
    expected_discount = math.exp(-rate * 1.0)

    assert retrieved.discount(future_date) == pytest.approx(expected_discount)
