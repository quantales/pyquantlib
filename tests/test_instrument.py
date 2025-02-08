import pytest
import pyquantlib as ql
from pyquantlib.base import Instrument


def test_instrument_abc_exists():
    assert hasattr(ql.base, 'Instrument')


def test_abstract_instrument_zombie():
    zombie = Instrument()

    with pytest.raises(RuntimeError, match="Tried to call pure virtual function"):
        zombie.isExpired()


def test_instrument_results_class():
    results = Instrument.results()
    assert results.value == 0.0
