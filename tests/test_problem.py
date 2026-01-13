import pytest

import pyquantlib as ql
from pyquantlib.base import CostFunction


class SumSquares(CostFunction):
    """Simple sum of squares cost function for testing."""
    def __init__(self):
        super().__init__()

    def value(self, x):
        return sum(xi * xi for xi in x)

    def values(self, x):
        return ql.Array([xi * xi for xi in x])


def test_problem_construction():
    cost = SumSquares()
    constraint = ql.NoConstraint()
    initial = ql.Array([1.0, 2.0, 3.0])

    problem = ql.Problem(cost, constraint, initial)

    assert problem is not None
    assert len(problem.currentValue()) == 3


def test_problem_value():
    cost = SumSquares()
    constraint = ql.NoConstraint()
    initial = ql.Array([1.0, 2.0, 3.0])

    problem = ql.Problem(cost, constraint, initial)

    # 1^2 + 2^2 + 3^2 = 14
    assert problem.value(initial) == pytest.approx(14.0)


def test_problem_values():
    cost = SumSquares()
    constraint = ql.NoConstraint()
    initial = ql.Array([1.0, 2.0, 3.0])

    problem = ql.Problem(cost, constraint, initial)

    values = problem.values(initial)
    assert len(values) == 3
    assert values[0] == pytest.approx(1.0)
    assert values[1] == pytest.approx(4.0)
    assert values[2] == pytest.approx(9.0)


def test_problem_constraint():
    cost = SumSquares()
    constraint = ql.PositiveConstraint()
    initial = ql.Array([1.0, 2.0, 3.0])

    problem = ql.Problem(cost, constraint, initial)

    c = problem.constraint()
    assert c.test(ql.Array([1.0, 2.0, 3.0]))
    assert not c.test(ql.Array([-1.0, 2.0, 3.0]))
