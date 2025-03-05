import pytest
import pyquantlib as ql


# --- CashFlow ABC ---

def test_event_abc_exists():
    assert hasattr(ql.base, 'Event')


def test_cashflow_abc_exists():
    assert hasattr(ql.base, 'CashFlow')


def test_abstract_cashflow_zombie():
    """Direct instantiation creates a zombie object."""
    zombie = ql.base.CashFlow()

    with pytest.raises(RuntimeError, match="Tried to call pure virtual function"):
        zombie.amount()

    with pytest.raises(RuntimeError, match="Tried to call pure virtual function"):
        zombie.date()


# --- Python CashFlow subclass ---

def test_python_custom_cashflow():
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


def test_incomplete_python_cashflow_raises():
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


# --- SimpleCashFlow ---

def test_simplecashflow_construction():
    cf = ql.SimpleCashFlow(100.0, ql.Date(15, 5, 2024))

    assert cf.amount() == pytest.approx(100.0)
    assert cf.date() == ql.Date(15, 5, 2024)


def test_simplecashflow_isinstance():
    cf = ql.SimpleCashFlow(100.0, ql.Date(15, 5, 2024))
    assert isinstance(cf, ql.base.CashFlow)


def test_simplecashflow_has_occurred():
    date = ql.Date(15, 5, 2024)
    cf = ql.SimpleCashFlow(100.0, date)

    # Default includeRefDate=false: date() <= refDate
    assert cf.hasOccurred(date)

    # includeRefDate=true: date() < refDate (strict)
    assert not cf.hasOccurred(date, True)

    # After/before event date
    assert cf.hasOccurred(date + ql.Period("1D"))
    assert not cf.hasOccurred(date - ql.Period("1D"))


# --- Redemption ---

def test_redemption_construction():
    cf = ql.Redemption(1000.0, ql.Date(31, 12, 2025))

    assert cf.amount() == pytest.approx(1000.0)
    assert cf.date() == ql.Date(31, 12, 2025)


def test_redemption_inheritance():
    cf = ql.Redemption(1000.0, ql.Date(31, 12, 2025))
    assert isinstance(cf, ql.SimpleCashFlow)
    assert isinstance(cf, ql.base.CashFlow)


# --- AmortizingPayment ---

def test_amortizingpayment_construction():
    cf = ql.AmortizingPayment(75.50, ql.Date(30, 6, 2025))

    assert cf.amount() == pytest.approx(75.50)
    assert cf.date() == ql.Date(30, 6, 2025)


def test_amortizingpayment_inheritance():
    cf = ql.AmortizingPayment(75.50, ql.Date(30, 6, 2025))
    assert isinstance(cf, ql.SimpleCashFlow)
    assert isinstance(cf, ql.base.CashFlow)


# --- Polymorphism ---

def test_cashflow_polymorphism():
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
