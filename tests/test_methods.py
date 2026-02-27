"""
Tests for methods module.

Corresponds to src/methods/*.cpp bindings (ql/math/optimization/).
"""

import math

import pytest

import pyquantlib as ql
from pyquantlib.base import CostFunction, OptimizationMethod


# =============================================================================
# Test Helpers
# =============================================================================


class SumSquares(CostFunction):
    """Simple sum of squares cost function for testing."""
    def __init__(self):
        super().__init__()

    def value(self, x):
        return sum(xi * xi for xi in x)

    def values(self, x):
        return ql.Array([xi * xi for xi in x])


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


# =============================================================================
# EndCriteria
# =============================================================================


@pytest.fixture
def end_criteria():
    """Fixture to create a standard EndCriteria object for testing."""
    return ql.EndCriteria(
        maxIterations=100,
        maxStationaryStateIterations=10,
        rootEpsilon=1e-5,
        functionEpsilon=1e-5,
        gradientNormEpsilon=1e-5
    )


def test_endcriteria_creation_and_properties(end_criteria):
    """Test EndCriteria construction and property accessors."""
    assert end_criteria.maxIterations == 100
    assert end_criteria.maxStationaryStateIterations == 10
    assert end_criteria.rootEpsilon == 1e-5
    assert end_criteria.functionEpsilon == 1e-5
    assert end_criteria.gradientNormEpsilon == 1e-5


def test_endcriteria_stationary_point(end_criteria):
    """Test EndCriteria checkStationaryPoint method."""
    # Points far apart - should not end
    has_ended, _ = end_criteria.checkStationaryPoint(
        xOld=1.0, xNew=1.1, statState=0,
        ecType=ql.EndCriteria.Type.Unknown
    )
    assert not has_ended

    # Points close but not enough stationary iterations
    has_ended_close, _ = end_criteria.checkStationaryPoint(
        xOld=1.0, xNew=1.0000001, statState=0,
        ecType=ql.EndCriteria.Type.Unknown
    )
    assert not has_ended_close

    # After exceeding max stationary iterations
    has_ended_final, _ = end_criteria.checkStationaryPoint(
        xOld=1.0, xNew=1.0000001, statState=10,
        ecType=ql.EndCriteria.Type.Unknown
    )
    assert has_ended_final


def test_endcriteria_static_succeeded():
    """Test EndCriteria.succeeded static method."""
    assert ql.EndCriteria.succeeded(ql.EndCriteria.Type.StationaryPoint)
    assert ql.EndCriteria.succeeded(ql.EndCriteria.Type.StationaryFunctionValue)
    assert ql.EndCriteria.succeeded(ql.EndCriteria.Type.StationaryFunctionAccuracy)
    assert not ql.EndCriteria.succeeded(ql.EndCriteria.Type.None_)
    assert not ql.EndCriteria.succeeded(ql.EndCriteria.Type.ZeroGradientNorm)
    assert not ql.EndCriteria.succeeded(ql.EndCriteria.Type.FunctionEpsilonTooSmall)
    assert not ql.EndCriteria.succeeded(ql.EndCriteria.Type.Unknown)


# =============================================================================
# Constraint (ABC)
# =============================================================================


def test_constraint_abc_exists():
    """Test Constraint ABC is accessible in base module."""
    assert hasattr(ql.base, 'Constraint')


def test_noconstraint():
    """Test NoConstraint accepts any values."""
    c = ql.NoConstraint()
    assert not c.empty()
    assert c.test(ql.Array([1.0, 2.0, 3.0]))
    assert c.test(ql.Array([-1.0, -2.0, -3.0]))


def test_positiveconstraint():
    """Test PositiveConstraint requires all positive values."""
    c = ql.PositiveConstraint()
    assert not c.empty()
    assert c.test(ql.Array([1.0, 2.0, 3.0]))
    assert not c.test(ql.Array([-1.0, 2.0, 3.0]))
    assert not c.test(ql.Array([0.0, 1.0, 2.0]))


def test_boundaryconstraint():
    """Test BoundaryConstraint enforces bounds."""
    c = ql.BoundaryConstraint(0.0, 10.0)
    assert not c.empty()
    assert c.test(ql.Array([1.0, 5.0, 9.0]))
    assert not c.test(ql.Array([-1.0, 5.0, 9.0]))
    assert not c.test(ql.Array([1.0, 5.0, 11.0]))


def test_compositeconstraint():
    """Test CompositeConstraint combines multiple constraints."""
    c1 = ql.PositiveConstraint()
    c2 = ql.BoundaryConstraint(0.0, 10.0)
    c = ql.CompositeConstraint(c1, c2)
    assert not c.empty()
    assert c.test(ql.Array([1.0, 5.0, 9.0]))
    assert not c.test(ql.Array([-1.0, 5.0, 9.0]))
    assert not c.test(ql.Array([1.0, 5.0, 11.0]))


# =============================================================================
# CostFunction (ABC)
# =============================================================================


def test_costfunction_abc_exists():
    """Test CostFunction ABC is accessible in base module."""
    assert hasattr(ql.base, 'CostFunction')


def test_costfunction_abstract_zombie():
    """Test abstract CostFunction creates zombie object."""
    zombie = CostFunction()

    with pytest.raises(RuntimeError, match="pure virtual"):
        zombie.value(ql.Array([1.0, 2.0]))


def test_costfunction_python_subclass():
    """Test Python subclass implementing CostFunction."""
    f = SumSquares()
    x = ql.Array([1.0, 2.0, 3.0])

    assert f.value(x) == pytest.approx(14.0)

    v = f.values(x)
    assert len(v) == 3
    assert v[0] == pytest.approx(1.0)
    assert v[1] == pytest.approx(4.0)
    assert v[2] == pytest.approx(9.0)


# =============================================================================
# OptimizationMethod (ABC)
# =============================================================================


def test_optimizationmethod_abc_exists():
    """Test OptimizationMethod ABC is accessible in base module."""
    assert hasattr(ql.base, 'OptimizationMethod')


def test_optimizationmethod_abstract_zombie():
    """Test abstract OptimizationMethod creates zombie object."""
    zombie = OptimizationMethod()
    # Cannot test minimize without Problem and EndCriteria
    # Just verify object creation works
    assert zombie is not None


# =============================================================================
# Problem
# =============================================================================


def test_problem_construction():
    """Test Problem construction."""
    cost = SumSquares()
    constraint = ql.NoConstraint()
    initial = ql.Array([1.0, 2.0, 3.0])

    problem = ql.Problem(cost, constraint, initial)

    assert problem is not None
    assert len(problem.currentValue()) == 3


def test_problem_value():
    """Test Problem value evaluation."""
    cost = SumSquares()
    constraint = ql.NoConstraint()
    initial = ql.Array([1.0, 2.0, 3.0])

    problem = ql.Problem(cost, constraint, initial)

    # 1^2 + 2^2 + 3^2 = 14
    assert problem.value(initial) == pytest.approx(14.0)


def test_problem_values():
    """Test Problem values evaluation."""
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
    """Test Problem constraint accessor."""
    cost = SumSquares()
    constraint = ql.PositiveConstraint()
    initial = ql.Array([1.0, 2.0, 3.0])

    problem = ql.Problem(cost, constraint, initial)

    c = problem.constraint()
    assert c.test(ql.Array([1.0, 2.0, 3.0]))
    assert not c.test(ql.Array([-1.0, 2.0, 3.0]))


# =============================================================================
# LevenbergMarquardt
# =============================================================================


def test_levenbergmarquardt_construction():
    """Test LevenbergMarquardt construction."""
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
    class ConstrainedSumSquares(CostFunction):
        def __init__(self):
            super().__init__()

        def value(self, x):
            return sum(xi * xi for xi in x)

        def values(self, x):
            return ql.Array(list(x))

    cost = ConstrainedSumSquares()
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


# =============================================================================
# LsmBasisSystem / PolynomialType
# =============================================================================


def test_polynomialtype_enum_values():
    """Test PolynomialType enum values exist and have correct integer values."""
    assert int(ql.PolynomialType.Monomial) == 0
    assert int(ql.PolynomialType.Laguerre) == 1
    assert int(ql.PolynomialType.Hermite) == 2
    assert int(ql.PolynomialType.Hyperbolic) == 3
    assert int(ql.PolynomialType.Legendre) == 4
    assert int(ql.PolynomialType.Chebyshev) == 5
    assert int(ql.PolynomialType.Chebyshev2nd) == 6


def test_polynomialtype_roundtrip():
    """Test PolynomialType can be passed to and from Python."""
    pt = ql.PolynomialType.Laguerre
    assert pt == ql.PolynomialType.Laguerre
    assert pt != ql.PolynomialType.Monomial
