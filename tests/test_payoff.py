import pytest
import pyquantlib as ql
from pyquantlib.base import Payoff


def test_payoff_abc_exists():
    assert hasattr(ql.base, 'Payoff')


def test_abstract_payoff_zombie():
    zombie = Payoff()

    with pytest.raises(RuntimeError, match="Tried to call pure virtual function"):
        zombie.name()


def test_custom_payoff_subclass():
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
