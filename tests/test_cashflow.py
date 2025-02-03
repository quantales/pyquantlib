import pyquantlib as ql
import pytest


def test_event_abc_exists():
    """Tests that Event ABC is accessible."""
    assert hasattr(ql.base, 'Event')


def test_cashflow_abc_exists():
    """Tests that CashFlow ABC is accessible."""
    assert hasattr(ql.base, 'CashFlow')


def test_python_custom_cashflow_inheritance():
    """Tests creating a custom CashFlow class in Python."""
    
    class CustomCashFlow(ql.base.CashFlow):
        def __init__(self, amount, date):
            super().__init__()
            self._amount = amount
            self._date = date

        def amount(self):
            return self._amount

        def date(self):
            return self._date

    cf = CustomCashFlow(100.0, ql.Date(3, 2, 2025))
    
    assert cf.amount() == pytest.approx(100.0)
    assert cf.date() == ql.Date(3, 2, 2025)


def test_incomplete_cashflow_raises_error():
    """Tests that incomplete CashFlow subclass raises error on pure virtual call."""
    
    class IncompleteCashFlow(ql.base.CashFlow):
        def __init__(self, date):
            super().__init__()
            self._date = date

        def date(self):
            return self._date
        # amount() not implemented

    cf = IncompleteCashFlow(ql.Date(3, 2, 2025))
    
    assert cf.date() == ql.Date(3, 2, 2025)
    
    with pytest.raises(RuntimeError, match="Tried to call pure virtual function"):
        cf.amount()


def test_abstract_cashflow_zombie():
    """Tests that direct instantiation creates a zombie object."""
    zombie = ql.base.CashFlow()
    
    with pytest.raises(RuntimeError, match="Tried to call pure virtual function"):
        zombie.amount()
    
    with pytest.raises(RuntimeError, match="Tried to call pure virtual function"):
        zombie.date()
