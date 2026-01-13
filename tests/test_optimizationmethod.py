import pyquantlib as ql
from pyquantlib.base import OptimizationMethod


def test_optimizationmethod_abc_exists():
    assert hasattr(ql.base, 'OptimizationMethod')


def test_abstract_optimizationmethod_zombie():
    zombie = OptimizationMethod()

    # Cannot test minimize without Problem and EndCriteria
    # Just verify object creation works
    assert zombie is not None
