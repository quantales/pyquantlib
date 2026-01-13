import pytest

import pyquantlib as ql
from pyquantlib.base import CostFunction


def test_costfunction_abc_exists():
    assert hasattr(ql.base, 'CostFunction')


def test_abstract_costfunction_zombie():
    zombie = CostFunction()

    with pytest.raises(RuntimeError, match="pure virtual"):
        zombie.value(ql.Array([1.0, 2.0]))


def test_custom_costfunction_subclass():
    class SumSquares(CostFunction):
        def __init__(self):
            super().__init__()

        def value(self, x):
            return sum(xi * xi for xi in x)

        def values(self, x):
            return ql.Array([xi * xi for xi in x])

    f = SumSquares()
    x = ql.Array([1.0, 2.0, 3.0])

    assert f.value(x) == pytest.approx(14.0)

    v = f.values(x)
    assert len(v) == 3
    assert v[0] == pytest.approx(1.0)
    assert v[1] == pytest.approx(4.0)
    assert v[2] == pytest.approx(9.0)
