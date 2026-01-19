"""Tests for ql/instruments/*.hpp bindings."""

import pytest

import pyquantlib as ql


# --- Swap ---


def test_swap_type_enum():
    """Test SwapType enum values."""
    assert ql.SwapType.Payer is not None
    assert ql.SwapType.Receiver is not None
    assert int(ql.SwapType.Payer) == 1
    assert int(ql.SwapType.Receiver) == -1


def test_swap_construction_two_legs():
    """Test Swap construction from two legs."""
    # Create simple fixed cash flows as legs
    today = ql.Date(15, ql.June, 2025)
    ql.Settings.instance().evaluationDate = today

    # Simple legs with fixed cash flows
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

    # payer[i] = True means leg i is paid
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
