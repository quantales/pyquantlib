import pytest
import math
import pyquantlib as ql
from pyquantlib.base import CostFunction


class Rosenbrock(CostFunction):
    """Rosenbrock function: f(x,y) = (a-x)^2 + b(y-x^2)^2
    
    Minimum at (a, a^2). With a=1, b=100, minimum at (1, 1).
    """
    def __init__(self, a=1.0, b=100.0):
        super().__init__()
        self.a = a
        self.b = b

    def value(self, x):
        return (self.a - x[0])**2 + self.b * (x[1] - x[0]**2)**2

    def values(self, x):
        return ql.Array([
            self.a - x[0],
            math.sqrt(self.b) * (x[1] - x[0]**2)
        ])


def test_levenbergmarquardt_construction():
    lm = ql.LevenbergMarquardt()
    assert lm is not None

    lm_custom = ql.LevenbergMarquardt(1e-6, 1e-6, 1e-6)
    assert lm_custom is not None


def test_levenbergmarquardt_minimize_rosenbrock():
    """Full integration test: minimize Rosenbrock function."""
    cost = Rosenbrock(a=1.0, b=100.0)
    constraint = ql.NoConstraint()
    initial = ql.Array([-1.0, 1.0])

    problem = ql.Problem(cost, constraint, initial)
    endCriteria = ql.EndCriteria(1000, 100, 1e-8, 1e-8, 1e-8)

    lm = ql.LevenbergMarquardt()
    result = lm.minimize(problem, endCriteria)

    # Check convergence
    assert ql.EndCriteria.succeeded(result)

    # Check solution is close to (1, 1)
    solution = problem.currentValue()
    assert solution[0] == pytest.approx(1.0, abs=1e-4)
    assert solution[1] == pytest.approx(1.0, abs=1e-4)

    # Check function value is close to 0
    assert problem.functionValue() == pytest.approx(0.0, abs=1e-8)


def test_levenbergmarquardt_with_constraint():
    """Test optimization with positive constraint."""
    class SumSquares(CostFunction):
        def __init__(self):
            super().__init__()

        def value(self, x):
            return sum(xi * xi for xi in x)

        def values(self, x):
            return ql.Array([xi for xi in x])

    cost = SumSquares()
    constraint = ql.PositiveConstraint()
    initial = ql.Array([1.0, 2.0])

    problem = ql.Problem(cost, constraint, initial)
    endCriteria = ql.EndCriteria(1000, 100, 1e-8, 1e-8, 1e-8)

    lm = ql.LevenbergMarquardt()
    lm.minimize(problem, endCriteria)

    # Solution should be at or near (0, 0), but constraint keeps it positive
    solution = problem.currentValue()
    assert solution[0] >= 0.0
    assert solution[1] >= 0.0
