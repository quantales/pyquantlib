import pytest

import pyquantlib as ql
from pyquantlib.base import PricingEngine


class MyArguments(PricingEngine.arguments):
    def __init__(self):
        super().__init__()
        self.spot_price = None

    def validate(self):
        if self.spot_price is None or self.spot_price <= 0:
            raise ql.Error("Spot price must be positive.")


class MyResults(PricingEngine.results):
    def __init__(self):
        super().__init__()
        self.value = None

    def reset(self):
        self.value = None


class MyPricingEngine(PricingEngine):
    def __init__(self, multiplier):
        super().__init__()
        self._multiplier = multiplier
        self._arguments = MyArguments()
        self._results = MyResults()

    def getArguments(self):
        return self._arguments

    def getResults(self):
        return self._results

    def calculate(self):
        self.getArguments().validate()
        self.getResults().value = self.getArguments().spot_price * self._multiplier

    def reset(self):
        self.getResults().reset()

    def update(self):
        self.notifyObservers()


def test_custom_engine_calculate():
    engine = MyPricingEngine(multiplier=1.5)
    engine.getArguments().spot_price = 100.0

    engine.calculate()

    assert engine.getResults().value == pytest.approx(150.0)


def test_custom_engine_reset():
    engine = MyPricingEngine(multiplier=1.5)
    engine.getArguments().spot_price = 100.0
    engine.calculate()

    engine.reset()

    assert engine.getResults().value is None


def test_custom_arguments_validate():
    engine = MyPricingEngine(multiplier=1.5)
    engine.getArguments().spot_price = -10.0

    with pytest.raises(ql.Error, match="Spot price must be positive"):
        engine.calculate()


def test_inheritance_hierarchy():
    engine = MyPricingEngine(multiplier=1.0)

    assert isinstance(engine, PricingEngine)
    assert isinstance(engine.getArguments(), PricingEngine.arguments)
    assert isinstance(engine.getResults(), PricingEngine.results)
