"""Tests for ql/indexes/*.hpp bindings."""

import pytest

import pyquantlib as ql


# --- IborIndex ---


@pytest.fixture
def yield_curve():
    """Simple flat yield curve for index tests."""
    today = ql.Date(15, ql.June, 2025)
    ql.Settings.instance().evaluationDate = today
    dc = ql.Actual365Fixed()
    return ql.FlatForward(today, 0.05, dc)


def test_iborindex_construction():
    """Test IborIndex construction."""
    today = ql.Date(15, ql.June, 2025)
    ql.Settings.instance().evaluationDate = today

    index = ql.IborIndex(
        "TestIbor",
        ql.Period(3, ql.Months),
        2,  # settlement days
        ql.EURCurrency(),
        ql.TARGET(),
        ql.ModifiedFollowing,
        False,  # end of month
        ql.Actual360(),
    )

    assert index is not None
    assert index.familyName() == "TestIbor"
    assert index.tenor() == ql.Period(3, ql.Months)


def test_iborindex_with_curve(yield_curve):
    """Test IborIndex with forwarding term structure."""
    index = ql.IborIndex(
        "TestIbor",
        ql.Period(6, ql.Months),
        2,
        ql.EURCurrency(),
        ql.TARGET(),
        ql.ModifiedFollowing,
        True,
        ql.Actual360(),
        yield_curve,
    )

    assert index is not None
    assert index.endOfMonth() is True


def test_iborindex_clone(yield_curve):
    """Test IborIndex clone method."""
    index = ql.IborIndex(
        "TestIbor",
        ql.Period(3, ql.Months),
        2,
        ql.EURCurrency(),
        ql.TARGET(),
        ql.ModifiedFollowing,
        False,
        ql.Actual360(),
    )

    cloned = index.clone(ql.YieldTermStructureHandle(yield_curve))
    assert cloned is not None


# --- Euribor ---


def test_euribor_construction():
    """Test Euribor construction with tenor."""
    today = ql.Date(15, ql.June, 2025)
    ql.Settings.instance().evaluationDate = today

    euribor = ql.Euribor(ql.Period(6, ql.Months))

    assert euribor is not None
    assert euribor.tenor() == ql.Period(6, ql.Months)
    assert "Euribor" in euribor.name()


def test_euribor_with_curve(yield_curve):
    """Test Euribor with forwarding term structure."""
    euribor = ql.Euribor(ql.Period(3, ql.Months), yield_curve)

    assert euribor is not None


def test_euribor6m(yield_curve):
    """Test Euribor6M convenience class."""
    euribor = ql.Euribor6M(yield_curve)

    assert euribor is not None
    assert euribor.tenor() == ql.Period(6, ql.Months)


def test_euribor6m_no_curve():
    """Test Euribor6M without forwarding curve."""
    today = ql.Date(15, ql.June, 2025)
    ql.Settings.instance().evaluationDate = today

    euribor = ql.Euribor6M()

    assert euribor is not None
    assert euribor.tenor() == ql.Period(6, ql.Months)


def test_euribor3m(yield_curve):
    """Test Euribor3M convenience class."""
    euribor = ql.Euribor3M(yield_curve)

    assert euribor is not None
    assert euribor.tenor() == ql.Period(3, ql.Months)


def test_euribor1m(yield_curve):
    """Test Euribor1M convenience class."""
    euribor = ql.Euribor1M(yield_curve)

    assert euribor is not None
    assert euribor.tenor() == ql.Period(1, ql.Months)


def test_euribor1y(yield_curve):
    """Test Euribor1Y convenience class."""
    euribor = ql.Euribor1Y(yield_curve)

    assert euribor is not None
    assert euribor.tenor() == ql.Period(1, ql.Years)


def test_euribor_fixing(yield_curve):
    """Test Euribor fixing calculation."""
    today = ql.Date(15, ql.June, 2025)
    ql.Settings.instance().evaluationDate = today

    euribor = ql.Euribor6M(yield_curve)

    # Get a valid fixing date
    fixing_date = euribor.fixingCalendar().advance(
        today, ql.Period(2, ql.Days), ql.Following
    )

    # Should be able to forecast fixing
    if euribor.isValidFixingDate(fixing_date):
        rate = euribor.fixing(fixing_date, True)
        assert rate == pytest.approx(0.04993839342800618, rel=1e-5)
