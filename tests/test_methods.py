"""
Tests for methods module.

Corresponds to src/methods/*.cpp bindings.
"""

import math

import pytest

import pyquantlib as ql
from pyquantlib.base import (
    CostFunction,
    FdmInnerValueCalculator,
    FdmStepCondition,
    OptimizationMethod,
    RiskNeutralDensityCalculator,
)


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


# =============================================================================
# SampleNumber (Sample<Real>)
# =============================================================================


def test_sample_number_construction():
    """Test SampleNumber construction and field access."""
    s = ql.SampleNumber(0.5, 1.0)
    assert s.value == pytest.approx(0.5)
    assert s.weight == pytest.approx(1.0)


def test_sample_number_readwrite():
    """Test SampleNumber fields are read-write."""
    s = ql.SampleNumber(0.0, 0.0)
    s.value = 3.14
    s.weight = 2.0
    assert s.value == pytest.approx(3.14)
    assert s.weight == pytest.approx(2.0)


def test_sample_number_repr():
    """Test SampleNumber repr."""
    s = ql.SampleNumber(0.5, 1.0)
    r = repr(s)
    assert "0.5" in r
    assert "1.0" in r


# =============================================================================
# SampleRealVector (Sample<vector<Real>>)
# =============================================================================


def test_sample_real_vector_construction():
    """Test SampleRealVector construction and field access."""
    s = ql.SampleRealVector([0.1, 0.2, 0.3], 1.0)
    assert s.value == pytest.approx([0.1, 0.2, 0.3])
    assert s.weight == pytest.approx(1.0)


def test_sample_real_vector_readwrite():
    """Test SampleRealVector fields are read-write."""
    s = ql.SampleRealVector([0.0], 0.0)
    s.value = [1.0, 2.0, 3.0]
    s.weight = 0.5
    assert s.value == pytest.approx([1.0, 2.0, 3.0])
    assert s.weight == pytest.approx(0.5)


def test_sample_real_vector_repr():
    """Test SampleRealVector repr."""
    s = ql.SampleRealVector([0.1, 0.2], 1.0)
    r = repr(s)
    assert "dim=2" in r
    assert "1.0" in r


# =============================================================================
# Path
# =============================================================================


def test_path_construction():
    """Test Path construction from TimeGrid."""
    grid = ql.TimeGrid(1.0, 10)
    p = ql.Path(grid)
    assert p.length() == 11
    assert not p.empty()


def test_path_construction_with_values():
    """Test Path construction from TimeGrid and Array."""
    grid = ql.TimeGrid(1.0, 4)
    values = ql.Array([100.0, 101.0, 99.0, 102.0, 103.0])
    p = ql.Path(grid, values)
    assert p.length() == 5
    assert p[0] == pytest.approx(100.0)
    assert p[4] == pytest.approx(103.0)


def test_path_getitem_negative():
    """Test Path negative indexing."""
    grid = ql.TimeGrid(1.0, 4)
    values = ql.Array([100.0, 101.0, 99.0, 102.0, 103.0])
    p = ql.Path(grid, values)
    assert p[-1] == pytest.approx(103.0)
    assert p[-5] == pytest.approx(100.0)


def test_path_getitem_out_of_range():
    """Test Path index out of range raises IndexError."""
    grid = ql.TimeGrid(1.0, 4)
    p = ql.Path(grid)
    with pytest.raises(IndexError):
        p[11]
    with pytest.raises(IndexError):
        p[-12]


def test_path_value_and_time():
    """Test Path value() and time() methods."""
    grid = ql.TimeGrid(1.0, 4)
    values = ql.Array([100.0, 101.0, 99.0, 102.0, 103.0])
    p = ql.Path(grid, values)
    assert p.value(0) == pytest.approx(100.0)
    assert p.value(4) == pytest.approx(103.0)
    assert p.time(0) == pytest.approx(0.0)
    assert p.time(4) == pytest.approx(1.0)


def test_path_front_back():
    """Test Path front() and back() methods."""
    grid = ql.TimeGrid(1.0, 4)
    values = ql.Array([100.0, 101.0, 99.0, 102.0, 103.0])
    p = ql.Path(grid, values)
    assert p.front() == pytest.approx(100.0)
    assert p.back() == pytest.approx(103.0)


def test_path_timegrid():
    """Test Path timeGrid() returns the underlying grid."""
    grid = ql.TimeGrid(1.0, 4)
    p = ql.Path(grid)
    tg = p.timeGrid()
    assert len(tg) == 5
    assert tg[0] == pytest.approx(0.0)
    assert tg[4] == pytest.approx(1.0)


def test_path_len():
    """Test Path __len__."""
    grid = ql.TimeGrid(1.0, 10)
    p = ql.Path(grid)
    assert len(p) == 11


def test_path_repr():
    """Test Path repr."""
    grid = ql.TimeGrid(1.0, 10)
    p = ql.Path(grid)
    assert "length=11" in repr(p)


# =============================================================================
# MultiPath
# =============================================================================


def test_multipath_construction():
    """Test MultiPath construction from nAsset and TimeGrid."""
    grid = ql.TimeGrid(1.0, 5)
    mp = ql.MultiPath(3, grid)
    assert mp.assetNumber() == 3
    assert mp.pathSize() == 6


def test_multipath_getitem():
    """Test MultiPath __getitem__ returns Path."""
    grid = ql.TimeGrid(1.0, 5)
    mp = ql.MultiPath(3, grid)
    path = mp[0]
    assert path.length() == 6


def test_multipath_getitem_negative():
    """Test MultiPath negative indexing."""
    grid = ql.TimeGrid(1.0, 5)
    mp = ql.MultiPath(3, grid)
    path = mp[-1]
    assert path.length() == 6


def test_multipath_getitem_out_of_range():
    """Test MultiPath index out of range raises IndexError."""
    grid = ql.TimeGrid(1.0, 5)
    mp = ql.MultiPath(3, grid)
    with pytest.raises(IndexError):
        mp[3]


def test_multipath_len():
    """Test MultiPath __len__ returns asset number."""
    grid = ql.TimeGrid(1.0, 5)
    mp = ql.MultiPath(3, grid)
    assert len(mp) == 3


def test_multipath_repr():
    """Test MultiPath repr."""
    grid = ql.TimeGrid(1.0, 5)
    mp = ql.MultiPath(3, grid)
    r = repr(mp)
    assert "assets=3" in r
    assert "pathSize=6" in r


# =============================================================================
# SamplePath / SampleMultiPath
# =============================================================================


def test_samplepath_type_exists():
    """Test SamplePath type is available."""
    assert hasattr(ql, "SamplePath")


def test_samplemultipath_type_exists():
    """Test SampleMultiPath type is available."""
    assert hasattr(ql, "SampleMultiPath")


# =============================================================================
# BrownianBridge
# =============================================================================


def test_brownianbridge_from_steps():
    """Test BrownianBridge construction from number of steps."""
    bb = ql.BrownianBridge(10)
    assert bb.size() == 10


def test_brownianbridge_from_times():
    """Test BrownianBridge construction from time vector."""
    times = [0.25, 0.5, 0.75, 1.0]
    bb = ql.BrownianBridge(times)
    assert bb.size() == 4
    assert bb.times() == pytest.approx(times)


def test_brownianbridge_from_timegrid():
    """Test BrownianBridge construction from TimeGrid."""
    grid = ql.TimeGrid(1.0, 4)  # 5 points, 4 steps
    bb = ql.BrownianBridge(timeGrid=grid)
    assert bb.size() == 4


def test_brownianbridge_inspectors():
    """Test BrownianBridge inspector methods return vectors."""
    bb = ql.BrownianBridge(5)
    assert len(bb.bridgeIndex()) == 5
    assert len(bb.leftIndex()) == 5
    assert len(bb.rightIndex()) == 5
    assert len(bb.leftWeight()) == 5
    assert len(bb.rightWeight()) == 5
    assert len(bb.stdDeviation()) == 5


def test_brownianbridge_transform():
    """Test BrownianBridge transform with known input."""
    bb = ql.BrownianBridge(4)
    # Use unit variates as input
    input_variates = [1.0, 0.5, -0.5, 0.3]
    output = bb.transform(input_variates)
    assert len(output) == 4
    # Output should be finite real numbers
    assert all(math.isfinite(v) for v in output)


def test_brownianbridge_transform_zeros():
    """Test BrownianBridge transform with zero input gives zero output."""
    bb = ql.BrownianBridge(4)
    output = bb.transform([0.0, 0.0, 0.0, 0.0])
    assert output == pytest.approx([0.0, 0.0, 0.0, 0.0])


def test_brownianbridge_repr():
    """Test BrownianBridge repr."""
    bb = ql.BrownianBridge(10)
    assert "size=10" in repr(bb)


# =============================================================================
# BrownianGenerator ABCs
# =============================================================================


def test_browniangenerator_abc_exists():
    """Test BrownianGenerator ABC is accessible."""
    assert hasattr(ql.base, "BrownianGenerator")


def test_browniangeneratorfactory_abc_exists():
    """Test BrownianGeneratorFactory ABC is accessible."""
    assert hasattr(ql.base, "BrownianGeneratorFactory")


# =============================================================================
# MTBrownianGenerator
# =============================================================================


def test_mtbrowniangenerator_construction():
    """Test MTBrownianGenerator construction."""
    gen = ql.MTBrownianGenerator(2, 5, 42)
    assert gen.numberOfFactors() == 2
    assert gen.numberOfSteps() == 5


def test_mtbrowniangenerator_nextpath_nextstep():
    """Test MTBrownianGenerator path/step generation."""
    gen = ql.MTBrownianGenerator(2, 3, 42)
    weight = gen.nextPath()
    assert weight == pytest.approx(1.0)

    step_weight, variates = gen.nextStep()
    assert step_weight == pytest.approx(1.0)
    assert len(variates) == 2
    assert all(math.isfinite(v) for v in variates)


def test_mtbrowniangenerator_deterministic():
    """Test MTBrownianGenerator produces deterministic results with same seed."""
    gen1 = ql.MTBrownianGenerator(1, 3, 42)
    gen2 = ql.MTBrownianGenerator(1, 3, 42)
    gen1.nextPath()
    gen2.nextPath()
    _, v1 = gen1.nextStep()
    _, v2 = gen2.nextStep()
    assert v1 == pytest.approx(v2)


def test_mtbrowniangeneratorfactory():
    """Test MTBrownianGeneratorFactory creates generators."""
    factory = ql.MTBrownianGeneratorFactory(42)
    gen = factory.create(2, 5)
    assert gen.numberOfFactors() == 2
    assert gen.numberOfSteps() == 5


# =============================================================================
# SobolBrownianGenerator
# =============================================================================


def test_sobolbrowniangenerator_construction():
    """Test SobolBrownianGenerator construction."""
    gen = ql.SobolBrownianGenerator(2, 5, ql.Ordering.Diagonal)
    assert gen.numberOfFactors() == 2
    assert gen.numberOfSteps() == 5


def test_sobolbrowniangenerator_nextpath_nextstep():
    """Test SobolBrownianGenerator generates paths."""
    gen = ql.SobolBrownianGenerator(2, 3, ql.Ordering.Steps)
    weight = gen.nextPath()
    assert weight == pytest.approx(1.0)

    step_weight, variates = gen.nextStep()
    assert step_weight == pytest.approx(1.0)
    assert len(variates) == 2


def test_sobolbrowniangeneratorfactory():
    """Test SobolBrownianGeneratorFactory creates generators."""
    factory = ql.SobolBrownianGeneratorFactory(ql.Ordering.Diagonal)
    gen = factory.create(2, 5)
    assert gen.numberOfFactors() == 2
    assert gen.numberOfSteps() == 5


def test_burley2020sobolbrowniangenerator_construction():
    """Test Burley2020SobolBrownianGenerator construction."""
    gen = ql.Burley2020SobolBrownianGenerator(
        2, 5, ql.Ordering.Diagonal, 42,
        ql.SobolRsg.DirectionIntegers.Jaeckel, 43,
    )
    assert gen.numberOfFactors() == 2
    assert gen.numberOfSteps() == 5


def test_burley2020sobolbrowniangeneratorfactory():
    """Test Burley2020SobolBrownianGeneratorFactory creates generators."""
    factory = ql.Burley2020SobolBrownianGeneratorFactory(ql.Ordering.Diagonal)
    gen = factory.create(2, 5)
    assert gen.numberOfFactors() == 2
    assert gen.numberOfSteps() == 5


# =============================================================================
# GaussianPathGenerator
# =============================================================================


@pytest.fixture
def bsm_process():
    """Create a simple BSM process for path generation tests."""
    today = ql.Date(15, 6, 2025)
    ql.Settings.evaluationDate = today

    spot = ql.SimpleQuote(100.0)
    flat_ts = ql.FlatForward(today, 0.05, ql.Actual365Fixed())
    flat_vol = ql.BlackConstantVol(
        today, ql.NullCalendar(), 0.20, ql.Actual365Fixed()
    )
    return ql.BlackScholesMertonProcess(
        ql.QuoteHandle(spot),
        ql.YieldTermStructureHandle(flat_ts),
        ql.YieldTermStructureHandle(flat_ts),
        ql.BlackVolTermStructureHandle(flat_vol),
    )


def test_gaussian_path_generator(bsm_process):
    """Test GaussianPathGenerator construction and path generation."""
    time_steps = 10
    length = 1.0
    rng = ql.UniformRandomSequenceGenerator(
        time_steps, ql.MersenneTwisterUniformRng(42)
    )
    gsg = ql.GaussianRandomSequenceGenerator(rng)
    gen = ql.GaussianPathGenerator(
        bsm_process, length, time_steps, gsg, False
    )

    assert gen.size() == time_steps

    sample = gen.next()
    path = sample.value
    assert path.length() == 11
    assert path.front() == pytest.approx(100.0)
    assert sample.weight == pytest.approx(1.0)
    # Path values should be positive (GBM)
    for i in range(path.length()):
        assert path[i] > 0.0


def test_gaussian_path_generator_with_timegrid(bsm_process):
    """Test GaussianPathGenerator with TimeGrid constructor."""
    grid = ql.TimeGrid(1.0, 10)
    rng = ql.UniformRandomSequenceGenerator(
        10, ql.MersenneTwisterUniformRng(42)
    )
    gsg = ql.GaussianRandomSequenceGenerator(rng)
    gen = ql.GaussianPathGenerator(bsm_process, grid, gsg, False)

    sample = gen.next()
    assert sample.value.length() == 11
    assert sample.value.front() == pytest.approx(100.0)


def test_gaussian_path_generator_antithetic(bsm_process):
    """Test GaussianPathGenerator antithetic path generation."""
    rng = ql.UniformRandomSequenceGenerator(
        10, ql.MersenneTwisterUniformRng(42)
    )
    gsg = ql.GaussianRandomSequenceGenerator(rng)
    gen = ql.GaussianPathGenerator(bsm_process, 1.0, 10, gsg, False)

    sample = gen.next()
    anti = gen.antithetic()
    # Both should start at 100
    assert sample.value.front() == pytest.approx(100.0)
    assert anti.value.front() == pytest.approx(100.0)
    # But differ at the end
    assert sample.value.back() != pytest.approx(anti.value.back(), rel=1e-6)


def test_gaussian_path_generator_brownian_bridge(bsm_process):
    """Test GaussianPathGenerator with Brownian bridge."""
    rng = ql.UniformRandomSequenceGenerator(
        10, ql.MersenneTwisterUniformRng(42)
    )
    gsg = ql.GaussianRandomSequenceGenerator(rng)
    gen = ql.GaussianPathGenerator(bsm_process, 1.0, 10, gsg, True)

    sample = gen.next()
    assert sample.value.length() == 11
    assert sample.value.front() == pytest.approx(100.0)


def test_gaussian_path_generator_timegrid_accessor(bsm_process):
    """Test GaussianPathGenerator timeGrid accessor."""
    rng = ql.UniformRandomSequenceGenerator(
        10, ql.MersenneTwisterUniformRng(42)
    )
    gsg = ql.GaussianRandomSequenceGenerator(rng)
    gen = ql.GaussianPathGenerator(bsm_process, 1.0, 10, gsg, False)
    tg = gen.timeGrid()
    assert len(tg) == 11
    assert tg[0] == pytest.approx(0.0)
    assert tg[10] == pytest.approx(1.0)


def test_gaussian_path_generator_deterministic(bsm_process):
    """Test same seed produces same paths."""
    def make_gen():
        rng = ql.UniformRandomSequenceGenerator(
            10, ql.MersenneTwisterUniformRng(42)
        )
        gsg = ql.GaussianRandomSequenceGenerator(rng)
        return ql.GaussianPathGenerator(bsm_process, 1.0, 10, gsg, False)

    gen1 = make_gen()
    gen2 = make_gen()
    p1 = gen1.next().value
    p2 = gen2.next().value
    for i in range(p1.length()):
        assert p1[i] == pytest.approx(p2[i])


# =============================================================================
# GaussianSobolPathGenerator
# =============================================================================


def test_gaussian_sobol_path_generator(bsm_process):
    """Test GaussianSobolPathGenerator construction and path generation."""
    time_steps = 10
    sobol = ql.SobolRsg(time_steps)
    gsg = ql.GaussianLowDiscrepancySequenceGenerator(sobol)
    gen = ql.GaussianSobolPathGenerator(
        bsm_process, 1.0, time_steps, gsg, False
    )

    sample = gen.next()
    path = sample.value
    assert path.length() == 11
    assert path.front() == pytest.approx(100.0)
    assert sample.weight == pytest.approx(1.0)


def test_gaussian_sobol_path_generator_with_bridge(bsm_process):
    """Test GaussianSobolPathGenerator with Brownian bridge."""
    time_steps = 10
    sobol = ql.SobolRsg(time_steps)
    gsg = ql.GaussianLowDiscrepancySequenceGenerator(sobol)
    gen = ql.GaussianSobolPathGenerator(
        bsm_process, 1.0, time_steps, gsg, True
    )

    sample = gen.next()
    assert sample.value.length() == 11
    assert sample.value.front() == pytest.approx(100.0)


# =============================================================================
# GaussianMultiPathGenerator
# =============================================================================


@pytest.fixture
def heston_process():
    """Create a Heston process for multi-path generation tests."""
    today = ql.Date(15, 6, 2025)
    ql.Settings.evaluationDate = today

    spot = ql.SimpleQuote(100.0)
    flat_ts = ql.FlatForward(today, 0.05, ql.Actual365Fixed())
    risk_free = ql.YieldTermStructureHandle(flat_ts)
    dividend = ql.YieldTermStructureHandle(flat_ts)
    return ql.HestonProcess(
        risk_free, dividend, ql.QuoteHandle(spot),
        0.04, 1.0, 0.04, 0.5, -0.7,
    )


def test_gaussian_multipath_generator(heston_process):
    """Test GaussianMultiPathGenerator with Heston process."""
    time_steps = 10
    grid = ql.TimeGrid(1.0, time_steps)
    dim = heston_process.factors() * time_steps
    rng = ql.UniformRandomSequenceGenerator(
        dim, ql.MersenneTwisterUniformRng(42)
    )
    gsg = ql.GaussianRandomSequenceGenerator(rng)
    gen = ql.GaussianMultiPathGenerator(heston_process, grid, gsg)

    sample = gen.next()
    mp = sample.value
    assert mp.assetNumber() == heston_process.size()
    assert mp.pathSize() == 11
    assert sample.weight == pytest.approx(1.0)
    # Spot path should start at initial value
    assert mp[0].front() == pytest.approx(100.0)


def test_gaussian_multipath_generator_antithetic(heston_process):
    """Test GaussianMultiPathGenerator antithetic generation."""
    time_steps = 10
    grid = ql.TimeGrid(1.0, time_steps)
    dim = heston_process.factors() * time_steps
    rng = ql.UniformRandomSequenceGenerator(
        dim, ql.MersenneTwisterUniformRng(42)
    )
    gsg = ql.GaussianRandomSequenceGenerator(rng)
    gen = ql.GaussianMultiPathGenerator(heston_process, grid, gsg)

    sample = gen.next()
    anti = gen.antithetic()
    # Both start at same initial values
    assert sample.value[0].front() == pytest.approx(anti.value[0].front())
    # But diverge
    assert sample.value[0].back() != pytest.approx(
        anti.value[0].back(), rel=1e-6
    )


# =============================================================================
# GaussianSobolMultiPathGenerator
# =============================================================================


def test_gaussian_sobol_multipath_generator(heston_process):
    """Test GaussianSobolMultiPathGenerator with Heston process."""
    time_steps = 10
    grid = ql.TimeGrid(1.0, time_steps)
    dim = heston_process.factors() * time_steps
    sobol = ql.SobolRsg(dim)
    gsg = ql.GaussianLowDiscrepancySequenceGenerator(sobol)
    gen = ql.GaussianSobolMultiPathGenerator(heston_process, grid, gsg)

    sample = gen.next()
    mp = sample.value
    assert mp.assetNumber() == heston_process.size()
    assert mp.pathSize() == 11
    assert mp[0].front() == pytest.approx(100.0)


# =============================================================================
# FdmLinearOpIterator
# =============================================================================


def test_fdmlinearopiterator_default():
    """Default iterator starts at index 0."""
    it = ql.FdmLinearOpIterator()
    assert it.index() == 0


def test_fdmlinearopiterator_from_index():
    """Construct with specific flat index."""
    it = ql.FdmLinearOpIterator(5)
    assert it.index() == 5


def test_fdmlinearopiterator_from_dim():
    """Construct from dimension vector; coordinates start at origin."""
    it = ql.FdmLinearOpIterator([3, 4])
    assert it.index() == 0
    assert list(it.coordinates()) == [0, 0]


def test_fdmlinearopiterator_full_construction():
    """Construct with dim, coordinates, and flat index."""
    it = ql.FdmLinearOpIterator([3, 4], [1, 2], 7)
    assert it.index() == 7
    assert list(it.coordinates()) == [1, 2]


def test_fdmlinearopiterator_increment_and_notequal():
    """Increment advances index and coordinates."""
    it = ql.FdmLinearOpIterator([3, 4])
    it2 = ql.FdmLinearOpIterator([3, 4], [1, 0], 1)
    assert it.notEqual(it2)
    it.increment()
    assert it.index() == 1
    assert list(it.coordinates()) == [1, 0]
    assert not it.notEqual(it2)


# =============================================================================
# FdmLinearOpLayout
# =============================================================================


def test_fdmlinearoplayout_construction():
    """Layout from dimension vector."""
    layout = ql.FdmLinearOpLayout([3, 4])
    assert layout.size() == 12
    assert list(layout.dim()) == [3, 4]
    assert list(layout.spacing()) == [1, 3]


def test_fdmlinearoplayout_index():
    """Flat index from coordinates."""
    layout = ql.FdmLinearOpLayout([3, 4])
    assert layout.index([0, 0]) == 0
    assert layout.index([1, 2]) == 7
    assert layout.index([2, 3]) == 11


def test_fdmlinearoplayout_begin_end():
    """begin/end return valid iterators."""
    layout = ql.FdmLinearOpLayout([3, 4])
    begin = layout.begin()
    end = layout.end()
    assert begin.index() == 0
    assert end.index() == 12
    assert begin.notEqual(end)


def test_fdmlinearoplayout_iteration():
    """Python iteration over layout yields correct count."""
    layout = ql.FdmLinearOpLayout([3, 4])
    count = sum(1 for _ in layout)
    assert count == 12


def test_fdmlinearoplayout_len():
    """__len__ returns total grid points."""
    layout = ql.FdmLinearOpLayout([5, 3, 2])
    assert len(layout) == 30


def test_fdmlinearoplayout_neighbourhood():
    """Neighbour index in single dimension."""
    layout = ql.FdmLinearOpLayout([3, 4])
    it = layout.begin()
    assert layout.neighbourhood(it, 0, 1) == 1
    assert layout.neighbourhood(it, 1, 1) == 3


def test_fdmlinearoplayout_iter_neighbourhood():
    """Neighbour iterator in a dimension."""
    layout = ql.FdmLinearOpLayout([3, 4])
    it = layout.begin()
    nb = layout.iter_neighbourhood(it, 0, 1)
    assert nb.index() == 1


# =============================================================================
# Fdm1dMesher
# =============================================================================


def test_fdm1dmesher_construction():
    """Base 1D mesher construction."""
    m = ql.Fdm1dMesher(5)
    assert m.size() == 5
    assert len(m) == 5


# =============================================================================
# Uniform1dMesher
# =============================================================================


def test_uniform1dmesher_construction():
    """Uniform grid from start to end."""
    m = ql.Uniform1dMesher(0.0, 1.0, 5)
    assert m.size() == 5
    assert m.location(0) == pytest.approx(0.0)
    assert m.location(4) == pytest.approx(1.0)


def test_uniform1dmesher_spacing():
    """Uniform spacing between grid points."""
    m = ql.Uniform1dMesher(0.0, 1.0, 5)
    assert m.dplus(0) == pytest.approx(0.25)
    assert m.dminus(1) == pytest.approx(0.25)
    locs = m.locations()
    assert [locs[i] for i in range(5)] == pytest.approx([0.0, 0.25, 0.5, 0.75, 1.0])


def test_uniform1dmesher_is_fdm1dmesher():
    """Uniform1dMesher is a subclass of Fdm1dMesher."""
    m = ql.Uniform1dMesher(0.0, 1.0, 5)
    assert isinstance(m, ql.Fdm1dMesher)


# =============================================================================
# Concentrating1dMesher
# =============================================================================


def test_concentrating1dmesher_no_cpoint():
    """Construction without concentration point."""
    m = ql.Concentrating1dMesher(0.0, 1.0, 11)
    assert m.size() == 11
    assert m.location(0) == pytest.approx(0.0)
    assert m.location(10) == pytest.approx(1.0)


def test_concentrating1dmesher_with_cpoint():
    """Single concentration point increases density near target."""
    m = ql.Concentrating1dMesher(0.0, 1.0, 11, cPoint=(0.5, 0.1))
    assert m.size() == 11
    assert m.location(0) == pytest.approx(0.0)
    assert m.location(5) == pytest.approx(0.5, abs=1e-6)
    assert m.location(10) == pytest.approx(1.0)


def test_concentrating1dmesher_multi_cpoints():
    """Multiple concentration points with required flag."""
    m = ql.Concentrating1dMesher(
        0.0, 1.0, 21,
        cPoints=[(0.25, 0.1, True), (0.75, 0.1, True)],
    )
    assert m.size() == 21
    locs = [m.location(i) for i in range(m.size())]
    assert any(abs(l - 0.25) < 1e-6 for l in locs)
    assert any(abs(l - 0.75) < 1e-6 for l in locs)


# =============================================================================
# Predefined1dMesher
# =============================================================================


def test_predefined1dmesher_construction():
    """Predefined grid from explicit points."""
    pts = [1.0, 2.0, 4.0, 8.0]
    m = ql.Predefined1dMesher(pts)
    assert m.size() == 4
    locs = [m.location(i) for i in range(m.size())]
    assert locs == pytest.approx(pts)


def test_predefined1dmesher_differences():
    """Forward and backward differences match point spacing."""
    m = ql.Predefined1dMesher([1.0, 2.0, 4.0, 8.0])
    assert m.dplus(0) == pytest.approx(1.0)
    assert m.dplus(1) == pytest.approx(2.0)
    assert m.dminus(1) == pytest.approx(1.0)


# =============================================================================
# FdmQuantoHelper
# =============================================================================


@pytest.fixture
def fdm_market_data():
    """Market data for FDM mesher tests."""
    today = ql.Date(15, 6, 2025)
    ql.Settings.evaluationDate = today
    flat_r = ql.FlatForward(today, 0.05, ql.Actual365Fixed())
    flat_div = ql.FlatForward(today, 0.02, ql.Actual365Fixed())
    flat_vol = ql.BlackConstantVol(
        today, ql.NullCalendar(), 0.20, ql.Actual365Fixed()
    )
    spot = ql.SimpleQuote(100.0)
    return {
        "today": today,
        "spot": spot,
        "rTS": flat_r,
        "divTS": flat_div,
        "vol": flat_vol,
    }


def test_fdmquantohelper_construction(fdm_market_data):
    """FdmQuantoHelper construction and member access."""
    d = fdm_market_data
    fx_vol = ql.BlackConstantVol(
        d["today"], ql.NullCalendar(), 0.10, ql.Actual365Fixed()
    )
    helper = ql.FdmQuantoHelper(d["rTS"], d["divTS"], fx_vol, 0.3, 1.2)
    assert helper.equityFxCorrelation == pytest.approx(0.3)
    assert helper.exchRateATMlevel == pytest.approx(1.2)


def test_fdmquantohelper_scalar_adjustment(fdm_market_data):
    """Scalar quanto adjustment."""
    d = fdm_market_data
    fx_vol = ql.BlackConstantVol(
        d["today"], ql.NullCalendar(), 0.10, ql.Actual365Fixed()
    )
    helper = ql.FdmQuantoHelper(d["rTS"], d["divTS"], fx_vol, 0.3, 1.2)
    adj = helper.quantoAdjustment(0.20, 0.0, 1.0)
    assert adj == pytest.approx(0.036, rel=1e-6)


def test_fdmquantohelper_array_adjustment(fdm_market_data):
    """Array quanto adjustment."""
    d = fdm_market_data
    fx_vol = ql.BlackConstantVol(
        d["today"], ql.NullCalendar(), 0.10, ql.Actual365Fixed()
    )
    helper = ql.FdmQuantoHelper(d["rTS"], d["divTS"], fx_vol, 0.3, 1.2)
    arr = ql.Array([0.20, 0.25, 0.30])
    adj = helper.quantoAdjustment(arr, 0.0, 1.0)
    expected = [0.036, 0.0375, 0.039]
    assert [float(adj[i]) for i in range(3)] == pytest.approx(expected, rel=1e-6)


# =============================================================================
# FdmBlackScholesMesher
# =============================================================================


def test_fdmblackscholesmesher_construction(fdm_market_data):
    """Black-Scholes mesher construction."""
    d = fdm_market_data
    bsm = ql.BlackScholesMertonProcess(
        ql.QuoteHandle(d["spot"]),
        ql.YieldTermStructureHandle(d["divTS"]),
        ql.YieldTermStructureHandle(d["rTS"]),
        ql.BlackVolTermStructureHandle(d["vol"]),
    )
    m = ql.FdmBlackScholesMesher(50, bsm, 1.0, 100.0)
    assert m.size() == 50
    assert m.location(0) == pytest.approx(3.48946524, rel=1e-4)
    assert m.location(25) == pytest.approx(4.64324580, rel=1e-4)
    assert m.location(49) == pytest.approx(5.75087513, rel=1e-4)


def test_fdmblackscholesmesher_processhelper(fdm_market_data):
    """processHelper static method returns a BSM process."""
    d = fdm_market_data
    proc = ql.FdmBlackScholesMesher.processHelper(
        ql.QuoteHandle(d["spot"]),
        ql.YieldTermStructureHandle(d["rTS"]),
        ql.YieldTermStructureHandle(d["divTS"]),
        0.20,
    )
    assert type(proc).__name__ == "GeneralizedBlackScholesProcess"


# =============================================================================
# FdmHestonVarianceMesher
# =============================================================================


def test_fdmhestonvariancemesher_construction(fdm_market_data):
    """Heston variance mesher construction and volaEstimate."""
    d = fdm_market_data
    heston = ql.HestonProcess(
        ql.YieldTermStructureHandle(d["rTS"]),
        ql.YieldTermStructureHandle(d["divTS"]),
        ql.QuoteHandle(d["spot"]),
        0.04, 1.0, 0.04, 0.5, -0.7,
    )
    m = ql.FdmHestonVarianceMesher(10, heston, 1.0)
    assert m.size() == 10
    assert m.volaEstimate() == pytest.approx(0.1761347, rel=1e-4)
    assert m.location(0) == pytest.approx(0.0, abs=1e-10)
    assert m.location(9) == pytest.approx(0.51823509, rel=1e-4)


def test_fdmhestonlocalvolvariancemesher_construction(fdm_market_data):
    """Heston local vol variance mesher construction."""
    d = fdm_market_data
    heston = ql.HestonProcess(
        ql.YieldTermStructureHandle(d["rTS"]),
        ql.YieldTermStructureHandle(d["divTS"]),
        ql.QuoteHandle(d["spot"]),
        0.04, 1.0, 0.04, 0.5, -0.7,
    )
    loc_vol = ql.LocalConstantVol(d["today"], 0.20, ql.Actual365Fixed())
    m = ql.FdmHestonLocalVolatilityVarianceMesher(10, heston, loc_vol, 1.0)
    assert m.size() == 10
    assert m.volaEstimate() == pytest.approx(0.03522694, rel=1e-4)


# =============================================================================
# FdmCEV1dMesher
# =============================================================================


def test_fdmcev1dmesher_construction():
    """CEV mesher construction."""
    m = ql.FdmCEV1dMesher(20, 100.0, 0.20, 0.5, 1.0)
    assert m.size() == 20
    assert m.location(0) == pytest.approx(61.793644, rel=1e-4)
    assert m.location(10) == pytest.approx(114.19132607, rel=1e-4)


def test_fdmcev1dmesher_with_cpoint():
    """CEV mesher with concentration point."""
    m = ql.FdmCEV1dMesher(20, 100.0, 0.20, 0.5, 1.0, cPoint=(100.0, 0.1))
    assert m.size() == 20


# =============================================================================
# FdmSimpleProcess1dMesher
# =============================================================================


def test_fdmsimpleprocess1dmesher_construction(fdm_market_data):
    """Simple process 1D mesher construction."""
    d = fdm_market_data
    bsm = ql.BlackScholesMertonProcess(
        ql.QuoteHandle(d["spot"]),
        ql.YieldTermStructureHandle(d["divTS"]),
        ql.YieldTermStructureHandle(d["rTS"]),
        ql.BlackVolTermStructureHandle(d["vol"]),
    )
    m = ql.FdmSimpleProcess1dMesher(10, bsm, 1.0)
    assert m.size() == 10
    assert m.location(0) == pytest.approx(60.00751554, rel=1e-4)
    assert m.location(5) == pytest.approx(102.57127044, rel=1e-4)


# =============================================================================
# FdmMesher (ABC)
# =============================================================================


def test_fdmmesher_cannot_instantiate():
    """FdmMesher is abstract and cannot be instantiated."""
    with pytest.raises(TypeError):
        ql.FdmMesher()


# =============================================================================
# FdmMesherComposite
# =============================================================================


def test_fdmmeshercomposite_1d():
    """1D composite mesher."""
    m = ql.Uniform1dMesher(0.0, 1.0, 3)
    comp = ql.FdmMesherComposite(m)
    assert comp.layout().size() == 3
    assert list(comp.layout().dim()) == [3]


def test_fdmmeshercomposite_2d():
    """2D composite mesher."""
    m1 = ql.Uniform1dMesher(0.0, 1.0, 3)
    m2 = ql.Uniform1dMesher(0.0, 2.0, 4)
    comp = ql.FdmMesherComposite(m1, m2)
    assert comp.layout().size() == 12
    assert list(comp.layout().dim()) == [3, 4]


def test_fdmmeshercomposite_3d():
    """3D composite mesher."""
    m1 = ql.Uniform1dMesher(0.0, 1.0, 3)
    m2 = ql.Uniform1dMesher(0.0, 2.0, 4)
    m3 = ql.Uniform1dMesher(0.0, 3.0, 2)
    comp = ql.FdmMesherComposite(m1, m2, m3)
    assert comp.layout().size() == 24
    assert list(comp.layout().dim()) == [3, 4, 2]


def test_fdmmeshercomposite_from_vector():
    """Composite mesher from vector of 1D meshers."""
    meshers = [
        ql.Uniform1dMesher(0.0, 1.0, 3),
        ql.Uniform1dMesher(0.0, 2.0, 4),
    ]
    comp = ql.FdmMesherComposite(meshers)
    assert comp.layout().size() == 12


def test_fdmmeshercomposite_getfdm1dmeshers():
    """getFdm1dMeshers returns underlying meshers."""
    m1 = ql.Uniform1dMesher(0.0, 1.0, 3)
    m2 = ql.Uniform1dMesher(0.0, 2.0, 4)
    comp = ql.FdmMesherComposite(m1, m2)
    meshers = comp.getFdm1dMeshers()
    assert len(meshers) == 2
    assert meshers[0].size() == 3
    assert meshers[1].size() == 4


def test_fdmmeshercomposite_locations():
    """Locations per direction in composite mesher."""
    m1 = ql.Uniform1dMesher(0.0, 1.0, 3)
    m2 = ql.Uniform1dMesher(0.0, 2.0, 4)
    comp = ql.FdmMesherComposite(m1, m2)
    locs0 = comp.locations(0)
    locs1 = comp.locations(1)
    assert len(locs0) == 12
    assert len(locs1) == 12
    assert float(locs0[0]) == pytest.approx(0.0)
    assert float(locs0[1]) == pytest.approx(0.5)


def test_fdmmeshercomposite_dplus_location():
    """dplus and location via iterator on composite mesher."""
    m1 = ql.Uniform1dMesher(0.0, 1.0, 3)
    m2 = ql.Uniform1dMesher(0.0, 2.0, 4)
    comp = ql.FdmMesherComposite(m1, m2)
    it = comp.layout().begin()
    assert comp.dplus(it, 0) == pytest.approx(0.5)
    assert comp.location(it, 0) == pytest.approx(0.0)
    assert comp.location(it, 1) == pytest.approx(0.0)


# =============================================================================
# FDM Operators
# =============================================================================


def test_fdmlinearop_abc():
    """FdmLinearOp cannot be instantiated (ABC)."""
    with pytest.raises(TypeError):
        ql.FdmLinearOp()


def test_fdmlinearopcomposite_abc():
    """FdmLinearOpComposite cannot be instantiated (ABC)."""
    with pytest.raises(TypeError):
        ql.FdmLinearOpComposite()


def test_boundarycondition_abc():
    """FdmBoundaryCondition cannot be instantiated (ABC)."""
    with pytest.raises(TypeError):
        ql.FdmBoundaryCondition()


def test_boundarycondition_side_enum():
    """BoundaryConditionSide enum values."""
    assert int(ql.BoundaryConditionSide.None_) == 0
    assert int(ql.BoundaryConditionSide.Upper) == 1
    assert int(ql.BoundaryConditionSide.Lower) == 2


def test_triplebandlinearop_construction():
    """TripleBandLinearOp construction and apply."""
    mesher = ql.FdmMesherComposite(ql.Uniform1dMesher(0.0, 1.0, 5))
    op = ql.TripleBandLinearOp(0, mesher)
    a = ql.Array([1.0, 2.0, 3.0, 4.0, 5.0])
    result = op.apply(a)
    assert len(result) == 5


def test_triplebandlinearop_solve_splitting():
    """TripleBandLinearOp solve_splitting."""
    mesher = ql.FdmMesherComposite(ql.Uniform1dMesher(0.0, 1.0, 5))
    op = ql.TripleBandLinearOp(0, mesher)
    a = ql.Array([1.0, 2.0, 3.0, 4.0, 5.0])
    result = op.solve_splitting(a, 1.0)
    assert len(result) == 5


def test_triplebandlinearop_mult_add():
    """TripleBandLinearOp mult and add."""
    mesher = ql.FdmMesherComposite(ql.Uniform1dMesher(0.0, 1.0, 5))
    op = ql.TripleBandLinearOp(0, mesher)
    u = ql.Array([1.0, 1.0, 1.0, 1.0, 1.0])
    m = op.mult(u)
    assert isinstance(m, ql.TripleBandLinearOp)
    mr = op.multR(u)
    assert isinstance(mr, ql.TripleBandLinearOp)
    added = op.add(op)
    assert isinstance(added, ql.TripleBandLinearOp)
    arr_added = op.add(u)
    assert isinstance(arr_added, ql.TripleBandLinearOp)


def test_firstderivativeop_construction():
    """FirstDerivativeOp construction and inheritance."""
    mesher = ql.FdmMesherComposite(ql.Uniform1dMesher(0.0, 1.0, 10))
    op = ql.FirstDerivativeOp(0, mesher)
    assert isinstance(op, ql.TripleBandLinearOp)
    assert isinstance(op, ql.FdmLinearOp)
    a = ql.Array([float(i) for i in range(10)])
    result = op.apply(a)
    assert len(result) == 10


def test_secondderivativeop_construction():
    """SecondDerivativeOp construction and inheritance."""
    mesher = ql.FdmMesherComposite(ql.Uniform1dMesher(0.0, 1.0, 10))
    op = ql.SecondDerivativeOp(0, mesher)
    assert isinstance(op, ql.TripleBandLinearOp)
    a = ql.Array([float(i * i) for i in range(10)])
    result = op.apply(a)
    assert len(result) == 10


def test_firstderivativeop_linear_function():
    """First derivative of a linear function should be constant."""
    n = 20
    mesher = ql.FdmMesherComposite(ql.Uniform1dMesher(0.0, 1.0, n))
    dx = ql.FirstDerivativeOp(0, mesher)
    locs = mesher.locations(0)
    a = ql.Array([float(locs[i]) for i in range(n)])
    result = dx.apply(a)
    for i in range(1, n - 1):
        assert float(result[i]) == pytest.approx(1.0, abs=1e-10)


def test_secondderivativeop_quadratic():
    """Second derivative of x^2 should be 2."""
    n = 20
    mesher = ql.FdmMesherComposite(ql.Uniform1dMesher(0.0, 1.0, n))
    dxx = ql.SecondDerivativeOp(0, mesher)
    locs = mesher.locations(0)
    a = ql.Array([float(locs[i]) ** 2 for i in range(n)])
    result = dxx.apply(a)
    for i in range(1, n - 1):
        assert float(result[i]) == pytest.approx(2.0, abs=1e-6)


def test_ninepointlinearop_construction():
    """NinePointLinearOp construction."""
    m1 = ql.Uniform1dMesher(0.0, 1.0, 5)
    m2 = ql.Uniform1dMesher(0.0, 1.0, 5)
    mesher = ql.FdmMesherComposite(m1, m2)
    op = ql.NinePointLinearOp(0, 1, mesher)
    assert isinstance(op, ql.FdmLinearOp)
    a = ql.Array([0.0] * 25)
    result = op.apply(a)
    assert len(result) == 25


def test_secondordermixedderivativeop_construction():
    """SecondOrderMixedDerivativeOp construction and inheritance."""
    m1 = ql.Uniform1dMesher(0.0, 1.0, 5)
    m2 = ql.Uniform1dMesher(0.0, 1.0, 5)
    mesher = ql.FdmMesherComposite(m1, m2)
    op = ql.SecondOrderMixedDerivativeOp(0, 1, mesher)
    assert isinstance(op, ql.NinePointLinearOp)


# =============================================================================
# FDM Process Operators
# =============================================================================


@pytest.fixture
def bs_operator_data():
    """Setup for Black-Scholes operator tests."""
    today = ql.Date(15, 6, 2025)
    ql.Settings.evaluationDate = today
    spot = ql.SimpleQuote(100.0)
    rTS = ql.FlatForward(today, 0.05, ql.Actual365Fixed())
    divTS = ql.FlatForward(today, 0.02, ql.Actual365Fixed())
    vol = ql.BlackConstantVol(today, ql.NullCalendar(), 0.20, ql.Actual365Fixed())
    process = ql.BlackScholesMertonProcess(
        ql.QuoteHandle(spot),
        ql.YieldTermStructureHandle(divTS),
        ql.YieldTermStructureHandle(rTS),
        ql.BlackVolTermStructureHandle(vol),
    )
    bs_mesher = ql.FdmBlackScholesMesher(50, process, 1.0, 100.0)
    mesher = ql.FdmMesherComposite(bs_mesher)
    return {
        "today": today, "process": process, "mesher": mesher,
        "rTS": rTS, "divTS": divTS, "spot": spot, "vol": vol,
    }


def test_fdmblackscholesop_construction(bs_operator_data):
    """FdmBlackScholesOp construction."""
    d = bs_operator_data
    op = ql.FdmBlackScholesOp(d["mesher"], d["process"], 100.0)
    assert isinstance(op, ql.FdmLinearOpComposite)
    assert isinstance(op, ql.FdmLinearOp)
    assert op.size() == 1


def test_fdmblackscholesop_apply(bs_operator_data):
    """FdmBlackScholesOp apply returns result of correct size."""
    d = bs_operator_data
    op = ql.FdmBlackScholesOp(d["mesher"], d["process"], 100.0)
    op.setTime(0.0, 1.0)
    a = ql.Array([1.0] * 50)
    result = op.apply(a)
    assert len(result) == 50


def test_fdmblackscholesop_solve_splitting(bs_operator_data):
    """FdmBlackScholesOp solve_splitting and preconditioner."""
    d = bs_operator_data
    op = ql.FdmBlackScholesOp(d["mesher"], d["process"], 100.0)
    op.setTime(0.0, 1.0)
    a = ql.Array([1.0] * 50)
    result = op.solve_splitting(0, a, 1.0)
    assert len(result) == 50
    pre = op.preconditioner(a, 1.0)
    assert len(pre) == 50


def test_fdmblackscholesop_with_localvol(bs_operator_data):
    """FdmBlackScholesOp with localVol=True."""
    d = bs_operator_data
    op = ql.FdmBlackScholesOp(
        d["mesher"], d["process"], 100.0, localVol=True,
        illegalLocalVolOverwrite=0.20)
    assert op.size() == 1


def test_fdmblackscholesfwdop_construction(bs_operator_data):
    """FdmBlackScholesFwdOp construction."""
    d = bs_operator_data
    op = ql.FdmBlackScholesFwdOp(d["mesher"], d["process"], 100.0)
    assert isinstance(op, ql.FdmLinearOpComposite)
    assert op.size() == 1


def test_fdm2dblackscholesop_construction(bs_operator_data):
    """Fdm2dBlackScholesOp construction."""
    d = bs_operator_data
    bs_mesher2 = ql.FdmBlackScholesMesher(50, d["process"], 1.0, 100.0)
    mesher2d = ql.FdmMesherComposite(
        ql.FdmBlackScholesMesher(30, d["process"], 1.0, 100.0),
        bs_mesher2,
    )
    op = ql.Fdm2dBlackScholesOp(
        mesher2d, d["process"], d["process"], 0.5, 1.0)
    assert isinstance(op, ql.FdmLinearOpComposite)
    assert op.size() == 2


@pytest.fixture
def heston_setup():
    """Setup for Heston-based operator tests."""
    today = ql.Date(15, 6, 2025)
    ql.Settings.evaluationDate = today
    rTS = ql.FlatForward(today, 0.05, ql.Actual365Fixed())
    divTS = ql.FlatForward(today, 0.02, ql.Actual365Fixed())
    spot = ql.SimpleQuote(100.0)
    vol = ql.BlackConstantVol(today, ql.NullCalendar(), 0.20, ql.Actual365Fixed())
    bsm = ql.BlackScholesMertonProcess(
        ql.QuoteHandle(spot),
        ql.YieldTermStructureHandle(divTS),
        ql.YieldTermStructureHandle(rTS),
        ql.BlackVolTermStructureHandle(vol),
    )
    heston = ql.HestonProcess(
        ql.YieldTermStructureHandle(rTS),
        ql.YieldTermStructureHandle(divTS),
        ql.QuoteHandle(spot),
        0.04, 1.0, 0.04, 0.5, -0.7,
    )
    return {
        "today": today, "rTS": rTS, "divTS": divTS, "spot": spot,
        "bsm": bsm, "heston": heston,
    }


def test_fdmhestonop_construction(heston_setup):
    """FdmHestonOp construction."""
    d = heston_setup
    bs_mesher = ql.FdmBlackScholesMesher(50, d["bsm"], 1.0, 100.0)
    var_mesher = ql.FdmHestonVarianceMesher(10, d["heston"], 1.0)
    mesher = ql.FdmMesherComposite(bs_mesher, var_mesher)
    op = ql.FdmHestonOp(mesher, d["heston"])
    assert isinstance(op, ql.FdmLinearOpComposite)
    assert op.size() == 2


def test_fdmhestonfwdop_construction(heston_setup):
    """FdmHestonFwdOp construction."""
    d = heston_setup
    bs_mesher = ql.FdmBlackScholesMesher(50, d["bsm"], 1.0, 100.0)
    var_mesher = ql.FdmHestonVarianceMesher(10, d["heston"], 1.0)
    mesher = ql.FdmMesherComposite(bs_mesher, var_mesher)
    op = ql.FdmHestonFwdOp(mesher, d["heston"])
    assert isinstance(op, ql.FdmLinearOpComposite)
    assert op.size() == 2


def test_fdmhestonhullwhiteop_construction(heston_setup):
    """FdmHestonHullWhiteOp construction."""
    d = heston_setup
    hw = ql.HullWhiteProcess(ql.YieldTermStructureHandle(d["rTS"]), 0.01, 0.01)
    bs_mesher = ql.FdmBlackScholesMesher(20, d["bsm"], 1.0, 100.0)
    var_mesher = ql.FdmHestonVarianceMesher(10, d["heston"], 1.0)
    rate_mesher = ql.Uniform1dMesher(-0.05, 0.10, 5)
    mesher = ql.FdmMesherComposite(bs_mesher, var_mesher, rate_mesher)
    op = ql.FdmHestonHullWhiteOp(mesher, d["heston"], hw, 0.1)
    assert isinstance(op, ql.FdmLinearOpComposite)
    assert op.size() == 3


def test_fdmhullwhiteop_construction():
    """FdmHullWhiteOp construction."""
    today = ql.Date(15, 6, 2025)
    ql.Settings.evaluationDate = today
    rTS = ql.FlatForward(today, 0.05, ql.Actual365Fixed())
    hw = ql.HullWhite(ql.YieldTermStructureHandle(rTS))
    mesher = ql.FdmMesherComposite(ql.Uniform1dMesher(-0.10, 0.10, 20))
    op = ql.FdmHullWhiteOp(mesher, hw, 0)
    assert isinstance(op, ql.FdmLinearOpComposite)
    assert op.size() == 1


def test_fdmg2op_construction():
    """FdmG2Op construction."""
    today = ql.Date(15, 6, 2025)
    ql.Settings.evaluationDate = today
    rTS = ql.FlatForward(today, 0.05, ql.Actual365Fixed())
    g2 = ql.G2(ql.YieldTermStructureHandle(rTS))
    m1 = ql.Uniform1dMesher(-0.10, 0.10, 10)
    m2 = ql.Uniform1dMesher(-0.10, 0.10, 10)
    mesher = ql.FdmMesherComposite(m1, m2)
    op = ql.FdmG2Op(mesher, g2, 0, 1)
    assert isinstance(op, ql.FdmLinearOpComposite)
    assert op.size() == 2


def test_fdmcevop_construction():
    """FdmCEVOp construction."""
    today = ql.Date(15, 6, 2025)
    ql.Settings.evaluationDate = today
    rTS = ql.FlatForward(today, 0.05, ql.Actual365Fixed())
    mesher = ql.FdmMesherComposite(ql.Uniform1dMesher(50.0, 150.0, 50))
    op = ql.FdmCEVOp(mesher, rTS, 100.0, 0.3, 0.5, 0)
    assert isinstance(op, ql.FdmLinearOpComposite)
    assert op.size() == 1


def test_fdmsabrop_construction():
    """FdmSabrOp construction."""
    today = ql.Date(15, 6, 2025)
    ql.Settings.evaluationDate = today
    rTS = ql.FlatForward(today, 0.05, ql.Actual365Fixed())
    m_f = ql.Uniform1dMesher(50.0, 150.0, 30)
    m_a = ql.Uniform1dMesher(0.01, 1.0, 10)
    mesher = ql.FdmMesherComposite(m_f, m_a)
    op = ql.FdmSabrOp(mesher, rTS, 100.0, 0.3, 0.5, 0.4, -0.5)
    assert isinstance(op, ql.FdmLinearOpComposite)
    assert op.size() == 2


def test_fdmlocalvolfwdop_construction(bs_operator_data):
    """FdmLocalVolFwdOp construction."""
    d = bs_operator_data
    local_vol = ql.LocalConstantVol(d["today"], 0.20, ql.Actual365Fixed())
    mesher = ql.FdmMesherComposite(
        ql.FdmBlackScholesMesher(50, d["process"], 1.0, 100.0))
    op = ql.FdmLocalVolFwdOp(mesher, d["spot"], d["rTS"], d["divTS"], local_vol)
    assert isinstance(op, ql.FdmLinearOpComposite)
    assert op.size() == 1


def test_fdmsquarerootfwdop_construction():
    """FdmSquareRootFwdOp construction and methods."""
    mesher = ql.FdmMesherComposite(ql.Uniform1dMesher(0.001, 0.5, 20))
    op = ql.FdmSquareRootFwdOp(
        mesher, kappa=1.0, theta=0.04, sigma=0.5, direction=0)
    assert isinstance(op, ql.FdmLinearOpComposite)
    assert op.size() == 1
    lb = op.lowerBoundaryFactor()
    ub = op.upperBoundaryFactor()
    assert lb != ub
    v0 = op.v(0)
    assert isinstance(v0, float)


def test_fdmsquarerootfwdop_transformations():
    """FdmSquareRootFwdOp with different transformation types."""
    mesher = ql.FdmMesherComposite(ql.Uniform1dMesher(0.001, 0.5, 20))
    for t in [ql.FdmSquareRootFwdOpTransformationType.Plain,
              ql.FdmSquareRootFwdOpTransformationType.Power,
              ql.FdmSquareRootFwdOpTransformationType.Log]:
        op = ql.FdmSquareRootFwdOp(
            mesher, kappa=1.0, theta=0.04, sigma=0.5, direction=0, type=t)
        assert op.size() == 1


def test_fdmornsteinuhlenbeckop_construction():
    """FdmOrnsteinUhlenbeckOp construction."""
    today = ql.Date(15, 6, 2025)
    ql.Settings.evaluationDate = today
    rTS = ql.FlatForward(today, 0.05, ql.Actual365Fixed())
    ou = ql.OrnsteinUhlenbeckProcess(0.1, 0.2)
    mesher = ql.FdmMesherComposite(ql.Uniform1dMesher(-1.0, 1.0, 20))
    op = ql.FdmOrnsteinUhlenbeckOp(mesher, ou, rTS)
    assert isinstance(op, ql.FdmLinearOpComposite)
    assert op.size() == 1


# =============================================================================
# FDM Schemes
# =============================================================================


def test_expliciteulerscheme_construction(bs_operator_data):
    """ExplicitEulerScheme construction and step."""
    d = bs_operator_data
    op = ql.FdmBlackScholesOp(d["mesher"], d["process"], 100.0)
    op.setTime(0.0, 1.0)
    scheme = ql.ExplicitEulerScheme(op)
    scheme.setStep(0.001)
    a = ql.Array([max(float(d["mesher"].locations(0)[i]) - 100.0, 0.0)
                  for i in range(50)])
    result = scheme.step(a, 1.0)
    assert len(result) == 50


def test_impliciteulerscheme_construction(bs_operator_data):
    """ImplicitEulerScheme construction and step."""
    d = bs_operator_data
    op = ql.FdmBlackScholesOp(d["mesher"], d["process"], 100.0)
    op.setTime(0.0, 1.0)
    scheme = ql.ImplicitEulerScheme(op)
    scheme.setStep(0.01)
    a = ql.Array([max(float(d["mesher"].locations(0)[i]) - 100.0, 0.0)
                  for i in range(50)])
    result = scheme.step(a, 1.0)
    assert len(result) == 50


def test_impliciteulerscheme_solver_type():
    """ImplicitEulerScheme solver type enum."""
    assert ql.ImplicitEulerSolverType.BiCGstab is not None
    assert ql.ImplicitEulerSolverType.GMRES is not None


def test_impliciteulerscheme_with_gmres(bs_operator_data):
    """ImplicitEulerScheme with GMRES solver."""
    d = bs_operator_data
    op = ql.FdmBlackScholesOp(d["mesher"], d["process"], 100.0)
    op.setTime(0.0, 1.0)
    scheme = ql.ImplicitEulerScheme(
        op, solverType=ql.ImplicitEulerSolverType.GMRES)
    scheme.setStep(0.01)
    a = ql.Array([1.0] * 50)
    result = scheme.step(a, 1.0)
    assert len(result) == 50


def test_cranknicolsonscheme_construction(bs_operator_data):
    """CrankNicolsonScheme construction and step."""
    d = bs_operator_data
    op = ql.FdmBlackScholesOp(d["mesher"], d["process"], 100.0)
    op.setTime(0.0, 1.0)
    scheme = ql.CrankNicolsonScheme(0.5, op)
    scheme.setStep(0.01)
    a = ql.Array([max(float(d["mesher"].locations(0)[i]) - 100.0, 0.0)
                  for i in range(50)])
    result = scheme.step(a, 1.0)
    assert len(result) == 50


def test_douglasscheme_construction(heston_setup):
    """DouglasScheme construction with 2D operator."""
    d = heston_setup
    bs_mesher = ql.FdmBlackScholesMesher(20, d["bsm"], 1.0, 100.0)
    var_mesher = ql.FdmHestonVarianceMesher(10, d["heston"], 1.0)
    mesher = ql.FdmMesherComposite(bs_mesher, var_mesher)
    op = ql.FdmHestonOp(mesher, d["heston"])
    scheme = ql.DouglasScheme(0.5, op)
    scheme.setStep(0.01)
    n = 20 * 10
    a = ql.Array([1.0] * n)
    result = scheme.step(a, 1.0)
    assert len(result) == n


def test_craigsneydscheme_construction(heston_setup):
    """CraigSneydScheme construction."""
    d = heston_setup
    bs_mesher = ql.FdmBlackScholesMesher(20, d["bsm"], 1.0, 100.0)
    var_mesher = ql.FdmHestonVarianceMesher(10, d["heston"], 1.0)
    mesher = ql.FdmMesherComposite(bs_mesher, var_mesher)
    op = ql.FdmHestonOp(mesher, d["heston"])
    scheme = ql.CraigSneydScheme(0.5, 0.5, op)
    scheme.setStep(0.01)
    n = 20 * 10
    a = ql.Array([1.0] * n)
    result = scheme.step(a, 1.0)
    assert len(result) == n


def test_hundsdorferscheme_construction(heston_setup):
    """HundsdorferScheme construction."""
    d = heston_setup
    bs_mesher = ql.FdmBlackScholesMesher(20, d["bsm"], 1.0, 100.0)
    var_mesher = ql.FdmHestonVarianceMesher(10, d["heston"], 1.0)
    mesher = ql.FdmMesherComposite(bs_mesher, var_mesher)
    op = ql.FdmHestonOp(mesher, d["heston"])
    scheme = ql.HundsdorferScheme(0.5, 0.5, op)
    scheme.setStep(0.01)
    n = 20 * 10
    a = ql.Array([1.0] * n)
    result = scheme.step(a, 1.0)
    assert len(result) == n


def test_modifiedcraigsneydscheme_construction(heston_setup):
    """ModifiedCraigSneydScheme construction."""
    d = heston_setup
    bs_mesher = ql.FdmBlackScholesMesher(20, d["bsm"], 1.0, 100.0)
    var_mesher = ql.FdmHestonVarianceMesher(10, d["heston"], 1.0)
    mesher = ql.FdmMesherComposite(bs_mesher, var_mesher)
    op = ql.FdmHestonOp(mesher, d["heston"])
    scheme = ql.ModifiedCraigSneydScheme(0.5, 0.5, op)
    scheme.setStep(0.01)
    n = 20 * 10
    a = ql.Array([1.0] * n)
    result = scheme.step(a, 1.0)
    assert len(result) == n


def test_methodoflinesscheme_construction(bs_operator_data):
    """MethodOfLinesScheme construction."""
    d = bs_operator_data
    op = ql.FdmBlackScholesOp(d["mesher"], d["process"], 100.0)
    op.setTime(0.0, 1.0)
    scheme = ql.MethodOfLinesScheme(1e-6, 0.001, op)
    scheme.setStep(0.01)
    a = ql.Array([max(float(d["mesher"].locations(0)[i]) - 100.0, 0.0)
                  for i in range(50)])
    result = scheme.step(a, 1.0)
    assert len(result) == 50


def test_fdmblackscholesop_polymorphic_apply(bs_operator_data):
    """Polymorphic apply through FdmLinearOp base."""
    d = bs_operator_data
    op = ql.FdmBlackScholesOp(d["mesher"], d["process"], 100.0)
    op.setTime(0.0, 1.0)
    base_op: ql.FdmLinearOp = op
    a = ql.Array([1.0] * 50)
    result = base_op.apply(a)
    assert len(result) == 50


def test_fdmlinearopcomposite_methods(bs_operator_data):
    """FdmLinearOpComposite methods accessible on derived operator."""
    d = bs_operator_data
    op = ql.FdmBlackScholesOp(d["mesher"], d["process"], 100.0)
    op.setTime(0.0, 1.0)
    a = ql.Array([1.0] * 50)
    r_mixed = op.apply_mixed(a)
    assert len(r_mixed) == 50
    r_dir = op.apply_direction(0, a)
    assert len(r_dir) == 50
    r_split = op.solve_splitting(0, a, 1.0)
    assert len(r_split) == 50
    r_pre = op.preconditioner(a, 1.0)
    assert len(r_pre) == 50


# =============================================================================
# FDM Step Conditions, Inner Value Calculators, Solvers & RND Calculators
# =============================================================================


@pytest.fixture
def fdm_bs_setup():
    """Common setup for FDM step condition, solver, and RND tests."""
    today = ql.Date(15, 6, 2025)
    ql.Settings.evaluationDate = today
    dc = ql.Actual365Fixed()
    spot = ql.SimpleQuote(100.0)
    rTS = ql.FlatForward(today, 0.05, dc)
    divTS = ql.FlatForward(today, 0.02, dc)
    vol = ql.BlackConstantVol(today, ql.NullCalendar(), 0.20, dc)
    process = ql.BlackScholesMertonProcess(
        ql.QuoteHandle(spot),
        ql.YieldTermStructureHandle(divTS),
        ql.YieldTermStructureHandle(rTS),
        ql.BlackVolTermStructureHandle(vol),
    )
    maturity = 1.0
    strike = 100.0
    n_grid = 100
    bs_mesher = ql.FdmBlackScholesMesher(n_grid, process, maturity, strike)
    mesher = ql.FdmMesherComposite(bs_mesher)
    payoff = ql.PlainVanillaPayoff(ql.OptionType.Call, strike)
    return {
        "today": today, "dc": dc, "spot": spot,
        "rTS": rTS, "divTS": divTS, "vol": vol,
        "process": process, "mesher": mesher,
        "payoff": payoff, "strike": strike, "maturity": maturity,
        "n_grid": n_grid,
    }


# -- FdmZeroInnerValue --

def test_fdmzeroinnervalue_returns_zero(fdm_bs_setup):
    """FdmZeroInnerValue returns 0 for any point."""
    calc = ql.FdmZeroInnerValue()
    d = fdm_bs_setup
    layout = d["mesher"].layout()
    it = layout.begin()
    assert calc.innerValue(it, 0.5) == 0.0
    assert calc.avgInnerValue(it, 0.5) == 0.0


# -- FdmCellAveragingInnerValue --

def test_fdmcellaveragingInnervalue_construction(fdm_bs_setup):
    """FdmCellAveragingInnerValue construction."""
    d = fdm_bs_setup
    calc = ql.FdmCellAveragingInnerValue(d["payoff"], d["mesher"], 0)
    assert isinstance(calc, FdmInnerValueCalculator)


def test_fdmcellaveragingInnervalue_with_mapping(fdm_bs_setup):
    """FdmCellAveragingInnerValue with grid mapping function."""
    d = fdm_bs_setup
    calc = ql.FdmCellAveragingInnerValue(
        d["payoff"], d["mesher"], 0, gridMapping=math.exp)
    assert isinstance(calc, FdmInnerValueCalculator)


# -- FdmLogInnerValue --

def test_fdmloginnervalue_construction(fdm_bs_setup):
    """FdmLogInnerValue construction."""
    d = fdm_bs_setup
    calc = ql.FdmLogInnerValue(d["payoff"], d["mesher"], 0)
    assert isinstance(calc, ql.FdmCellAveragingInnerValue)
    assert isinstance(calc, FdmInnerValueCalculator)


def test_fdmloginnervalue_values(fdm_bs_setup):
    """FdmLogInnerValue returns inner value on log grid."""
    d = fdm_bs_setup
    calc = ql.FdmLogInnerValue(d["payoff"], d["mesher"], 0)
    layout = d["mesher"].layout()
    it = layout.begin()
    val = calc.innerValue(it, 0.0)
    assert isinstance(val, float)


# -- FdmLogBasketInnerValue --

def test_fdmlogbasketinnervalue_construction(fdm_bs_setup):
    """FdmLogBasketInnerValue construction with basket payoff."""
    d = fdm_bs_setup
    basket_payoff = ql.AverageBasketPayoff(d["payoff"], [1.0])
    calc = ql.FdmLogBasketInnerValue(basket_payoff, d["mesher"])
    assert isinstance(calc, FdmInnerValueCalculator)


# -- FdmSnapshotCondition --

def test_fdmsnapshotcondition_construction():
    """FdmSnapshotCondition construction."""
    cond = ql.FdmSnapshotCondition(0.5)
    assert isinstance(cond, FdmStepCondition)
    assert cond.getTime() == 0.5


def test_fdmsnapshotcondition_getvalues():
    """FdmSnapshotCondition getValues returns array."""
    cond = ql.FdmSnapshotCondition(0.5)
    vals = cond.getValues()
    assert isinstance(vals, ql.Array)


# -- FdmAmericanStepCondition --

def test_fdmamericanstepcondition_construction(fdm_bs_setup):
    """FdmAmericanStepCondition construction."""
    d = fdm_bs_setup
    calc = ql.FdmLogInnerValue(d["payoff"], d["mesher"], 0)
    cond = ql.FdmAmericanStepCondition(d["mesher"], calc)
    assert isinstance(cond, FdmStepCondition)


# -- FdmBermudanStepCondition --

def test_fdmbermudanstepcondition_construction(fdm_bs_setup):
    """FdmBermudanStepCondition construction."""
    d = fdm_bs_setup
    calc = ql.FdmLogInnerValue(d["payoff"], d["mesher"], 0)
    dates = [d["today"] + ql.Period(3, ql.Months),
             d["today"] + ql.Period(6, ql.Months),
             d["today"] + ql.Period(9, ql.Months)]
    cond = ql.FdmBermudanStepCondition(dates, d["today"], d["dc"],
                                        d["mesher"], calc)
    assert isinstance(cond, FdmStepCondition)
    times = cond.exerciseTimes()
    assert len(times) == 3


# -- FdmDividendHandler --

def test_fdmdividendhandler_construction(fdm_bs_setup):
    """FdmDividendHandler construction with dividend schedule."""
    d = fdm_bs_setup
    div1 = ql.FixedDividend(2.0, d["today"] + ql.Period(3, ql.Months))
    div2 = ql.FixedDividend(2.0, d["today"] + ql.Period(6, ql.Months))
    handler = ql.FdmDividendHandler([div1, div2], d["mesher"],
                                     d["today"], d["dc"], 0)
    assert isinstance(handler, FdmStepCondition)


def test_fdmdividendhandler_accessors(fdm_bs_setup):
    """FdmDividendHandler dividend times, dates, and amounts."""
    d = fdm_bs_setup
    div_date = d["today"] + ql.Period(6, ql.Months)
    div1 = ql.FixedDividend(2.5, div_date)
    handler = ql.FdmDividendHandler([div1], d["mesher"],
                                     d["today"], d["dc"], 0)
    assert len(handler.dividendTimes()) == 1
    assert len(handler.dividendDates()) == 1
    assert handler.dividendDates()[0] == div_date
    assert len(handler.dividends()) == 1


# -- FdmStepConditionComposite --

def test_fdmstepconditioncomposite_construction():
    """FdmStepConditionComposite from stopping times and conditions."""
    comp = ql.FdmStepConditionComposite([], [])
    assert isinstance(comp, FdmStepCondition)
    assert len(comp.stoppingTimes()) == 0


def test_fdmstepconditioncomposite_vanillacomposite(fdm_bs_setup):
    """FdmStepConditionComposite.vanillaComposite static factory."""
    d = fdm_bs_setup
    calc = ql.FdmLogInnerValue(d["payoff"], d["mesher"], 0)
    exercise = ql.EuropeanExercise(d["today"] + ql.Period(1, ql.Years))
    comp = ql.FdmStepConditionComposite.vanillaComposite(
        [], exercise, d["mesher"], calc, d["today"], d["dc"])
    assert isinstance(comp, FdmStepCondition)


def test_fdmstepconditioncomposite_joinconditions(fdm_bs_setup):
    """FdmStepConditionComposite.joinConditions static factory."""
    d = fdm_bs_setup
    calc = ql.FdmLogInnerValue(d["payoff"], d["mesher"], 0)
    exercise = ql.EuropeanExercise(d["today"] + ql.Period(1, ql.Years))
    comp = ql.FdmStepConditionComposite.vanillaComposite(
        [], exercise, d["mesher"], calc, d["today"], d["dc"])
    snapshot = ql.FdmSnapshotCondition(0.5)
    joined = ql.FdmStepConditionComposite.joinConditions(snapshot, comp)
    assert isinstance(joined, ql.FdmStepConditionComposite)


# -- FdmSolverDesc --

def test_fdmsolverdesc_construction(fdm_bs_setup):
    """FdmSolverDesc construction with kwargs."""
    d = fdm_bs_setup
    calc = ql.FdmLogInnerValue(d["payoff"], d["mesher"], 0)
    exercise = ql.EuropeanExercise(d["today"] + ql.Period(1, ql.Years))
    conditions = ql.FdmStepConditionComposite.vanillaComposite(
        [], exercise, d["mesher"], calc, d["today"], d["dc"])
    desc = ql.FdmSolverDesc(
        mesher=d["mesher"], bcSet=[], condition=conditions,
        calculator=calc, maturity=d["maturity"],
        timeSteps=100, dampingSteps=0)
    assert desc.maturity == d["maturity"]
    assert desc.timeSteps == 100
    assert desc.dampingSteps == 0


# -- FdmBackwardSolver --

def test_fdmbackwardsolver_construction(fdm_bs_setup):
    """FdmBackwardSolver construction."""
    d = fdm_bs_setup
    op = ql.FdmBlackScholesOp(d["mesher"], d["process"], d["strike"])
    solver = ql.FdmBackwardSolver(op)
    assert isinstance(solver, ql.FdmBackwardSolver)


def test_fdmbackwardsolver_rollback(fdm_bs_setup):
    """FdmBackwardSolver rollback returns modified array."""
    d = fdm_bs_setup
    op = ql.FdmBlackScholesOp(d["mesher"], d["process"], d["strike"])
    solver = ql.FdmBackwardSolver(op)
    layout = d["mesher"].layout()
    n = layout.size()
    a = ql.Array(n, 0.0)
    for i in range(n):
        x = d["mesher"].location(layout.begin(), 0)  # first point
        a[i] = max(0.1 * i, 0.0)
    result = solver.rollback(a, 1.0, 0.0, 100, 0)
    assert len(result) == n
    assert any(result[i] != a[i] for i in range(n))


# -- Fdm1DimSolver --

def test_fdm1dimsolver_greeks(fdm_bs_setup):
    """Fdm1DimSolver theta, derivativeX, derivativeXX."""
    d = fdm_bs_setup
    calc = ql.FdmLogInnerValue(d["payoff"], d["mesher"], 0)
    exercise = ql.EuropeanExercise(d["today"] + ql.Period(1, ql.Years))
    conditions = ql.FdmStepConditionComposite.vanillaComposite(
        [], exercise, d["mesher"], calc, d["today"], d["dc"])
    desc = ql.FdmSolverDesc(
        mesher=d["mesher"], bcSet=[], condition=conditions,
        calculator=calc, maturity=d["maturity"], timeSteps=100)
    op = ql.FdmBlackScholesOp(d["mesher"], d["process"], d["strike"])
    solver = ql.Fdm1DimSolver(desc, ql.FdmSchemeDesc.Douglas(), op)
    x = math.log(100.0)
    theta = solver.thetaAt(x)
    dx = solver.derivativeX(x)
    dxx = solver.derivativeXX(x)
    assert isinstance(theta, float)
    assert isinstance(dx, float)
    assert isinstance(dxx, float)


# -- FdmBlackScholesSolver --

def test_fdmblackscholessolver_greeks(fdm_bs_setup):
    """FdmBlackScholesSolver deltaAt, gammaAt, thetaAt."""
    d = fdm_bs_setup
    calc = ql.FdmLogInnerValue(d["payoff"], d["mesher"], 0)
    exercise = ql.EuropeanExercise(d["today"] + ql.Period(1, ql.Years))
    conditions = ql.FdmStepConditionComposite.vanillaComposite(
        [], exercise, d["mesher"], calc, d["today"], d["dc"])
    desc = ql.FdmSolverDesc(
        mesher=d["mesher"], bcSet=[], condition=conditions,
        calculator=calc, maturity=d["maturity"], timeSteps=100)
    solver = ql.FdmBlackScholesSolver(d["process"], d["strike"], desc)
    delta = solver.deltaAt(100.0)
    gamma = solver.gammaAt(100.0)
    theta = solver.thetaAt(100.0)
    assert isinstance(delta, float)
    assert isinstance(gamma, float)
    assert isinstance(theta, float)
    # ATM call delta should be around 0.5-0.7
    assert 0.4 < delta < 0.8


# -- BSMRNDCalculator --

def test_bsmrndcalculator_construction(fdm_bs_setup):
    """BSMRNDCalculator construction."""
    d = fdm_bs_setup
    calc = ql.BSMRNDCalculator(d["process"])
    assert isinstance(calc, RiskNeutralDensityCalculator)


def test_bsmrndcalculator_pdf(fdm_bs_setup):
    """BSMRNDCalculator pdf returns positive density (log-space input)."""
    d = fdm_bs_setup
    calc = ql.BSMRNDCalculator(d["process"])
    # BSMRNDCalculator uses log-space: x = log(S)
    pdf_val = calc.pdf(math.log(100.0), 1.0)
    assert pdf_val > 0.0
    assert pdf_val == pytest.approx(1.9922, rel=1e-2)


def test_bsmrndcalculator_invcdf(fdm_bs_setup):
    """BSMRNDCalculator invcdf is inverse of cdf (log-space)."""
    d = fdm_bs_setup
    calc = ql.BSMRNDCalculator(d["process"])
    x = math.log(100.0)
    p = calc.cdf(x, 1.0)
    x_back = calc.invcdf(p, 1.0)
    assert x_back == pytest.approx(x, rel=1e-6)


# -- GBSMRNDCalculator --

def test_gbsmrndcalculator_construction(fdm_bs_setup):
    """GBSMRNDCalculator construction."""
    d = fdm_bs_setup
    calc = ql.GBSMRNDCalculator(d["process"])
    assert isinstance(calc, RiskNeutralDensityCalculator)


def test_gbsmrndcalculator_pdf(fdm_bs_setup):
    """GBSMRNDCalculator pdf in spot-space returns positive density."""
    d = fdm_bs_setup
    gbsm_calc = ql.GBSMRNDCalculator(d["process"])
    # GBSMRNDCalculator uses spot-space: x = S
    gbsm_pdf = gbsm_calc.pdf(100.0, 1.0)
    assert gbsm_pdf > 0.0
    assert gbsm_pdf == pytest.approx(0.01992, rel=1e-2)


# -- HestonRNDCalculator --

def test_hestonrndcalculator_construction(fdm_bs_setup):
    """HestonRNDCalculator construction."""
    d = fdm_bs_setup
    heston = ql.HestonProcess(
        ql.YieldTermStructureHandle(d["rTS"]),
        ql.YieldTermStructureHandle(d["divTS"]),
        ql.QuoteHandle(d["spot"]),
        0.04, 1.0, 0.04, 0.5, -0.7,
    )
    calc = ql.HestonRNDCalculator(heston, 1e-4, 100000)
    assert isinstance(calc, RiskNeutralDensityCalculator)


def test_hestonrndcalculator_pdf(fdm_bs_setup):
    """HestonRNDCalculator pdf returns positive density (log-space)."""
    d = fdm_bs_setup
    heston = ql.HestonProcess(
        ql.YieldTermStructureHandle(d["rTS"]),
        ql.YieldTermStructureHandle(d["divTS"]),
        ql.QuoteHandle(d["spot"]),
        0.04, 2.0, 0.04, 0.3, -0.5,
    )
    calc = ql.HestonRNDCalculator(heston, 1e-8, 100000)
    pdf_val = calc.pdf(math.log(100.0), 1.0)
    assert pdf_val > 0.0
    assert pdf_val == pytest.approx(2.0111, rel=1e-2)


def test_hestonrndcalculator_cdf(fdm_bs_setup):
    """HestonRNDCalculator cdf returns valid probability (log-space)."""
    d = fdm_bs_setup
    heston = ql.HestonProcess(
        ql.YieldTermStructureHandle(d["rTS"]),
        ql.YieldTermStructureHandle(d["divTS"]),
        ql.QuoteHandle(d["spot"]),
        0.04, 2.0, 0.04, 0.3, -0.5,
    )
    calc = ql.HestonRNDCalculator(heston, 1e-8, 100000)
    cdf_val = calc.cdf(math.log(100.0), 1.0)
    assert 0.0 < cdf_val < 1.0
    assert cdf_val == pytest.approx(0.4350, rel=1e-2)


# -- CEVRNDCalculator --

def test_cevrndcalculator_construction():
    """CEVRNDCalculator construction."""
    calc = ql.CEVRNDCalculator(100.0, 0.3, 0.5)
    assert isinstance(calc, RiskNeutralDensityCalculator)


def test_cevrndcalculator_pdf():
    """CEVRNDCalculator pdf returns positive density."""
    calc = ql.CEVRNDCalculator(100.0, 0.3, 0.5)
    pdf_val = calc.pdf(100.0, 1.0)
    assert pdf_val > 0.0


def test_cevrndcalculator_cdf():
    """CEVRNDCalculator cdf returns valid probability."""
    calc = ql.CEVRNDCalculator(100.0, 0.3, 0.5)
    cdf_val = calc.cdf(100.0, 1.0)
    assert 0.0 < cdf_val < 1.0


def test_cevrndcalculator_massatzero():
    """CEVRNDCalculator massAtZero returns non-negative mass."""
    calc = ql.CEVRNDCalculator(100.0, 0.3, 0.5)
    mass = calc.massAtZero(1.0)
    assert mass >= 0.0


# -- SquareRootProcessRNDCalculator --

def test_squarerootprocessrndcalculator_construction():
    """SquareRootProcessRNDCalculator construction."""
    calc = ql.SquareRootProcessRNDCalculator(0.04, 1.0, 0.04, 0.5)
    assert isinstance(calc, RiskNeutralDensityCalculator)


def test_squarerootprocessrndcalculator_pdf():
    """SquareRootProcessRNDCalculator pdf returns positive density."""
    calc = ql.SquareRootProcessRNDCalculator(0.04, 1.0, 0.04, 0.5)
    pdf_val = calc.pdf(0.04, 1.0)
    assert pdf_val > 0.0


def test_squarerootprocessrndcalculator_cdf():
    """SquareRootProcessRNDCalculator cdf returns valid probability."""
    calc = ql.SquareRootProcessRNDCalculator(0.04, 1.0, 0.04, 0.5)
    cdf_val = calc.cdf(0.04, 1.0)
    assert 0.0 < cdf_val < 1.0


def test_squarerootprocessrndcalculator_stationary():
    """SquareRootProcessRNDCalculator stationary distribution methods."""
    calc = ql.SquareRootProcessRNDCalculator(0.04, 1.0, 0.04, 0.5)
    pdf_s = calc.stationary_pdf(0.04)
    cdf_s = calc.stationary_cdf(0.04)
    inv_s = calc.stationary_invcdf(cdf_s)
    assert pdf_s > 0.0
    assert 0.0 < cdf_s < 1.0
    assert inv_s == pytest.approx(0.04, rel=1e-4)


# -- End-to-end FDM European option pricing --

def test_fdm_european_call_end_to_end(fdm_bs_setup):
    """End-to-end FDM pricing of European call vs Black-Scholes analytic."""
    d = fdm_bs_setup
    # Analytic BS price for comparison
    engine = ql.AnalyticEuropeanEngine(d["process"])
    exercise = ql.EuropeanExercise(d["today"] + ql.Period(1, ql.Years))
    option = ql.VanillaOption(d["payoff"], exercise)
    option.setPricingEngine(engine)
    analytic_npv = option.NPV()

    # FDM price via Fdm1DimSolver
    calc = ql.FdmLogInnerValue(d["payoff"], d["mesher"], 0)
    conditions = ql.FdmStepConditionComposite.vanillaComposite(
        [], exercise, d["mesher"], calc, d["today"], d["dc"])
    desc = ql.FdmSolverDesc(
        mesher=d["mesher"], bcSet=[], condition=conditions,
        calculator=calc, maturity=d["maturity"], timeSteps=100)
    op = ql.FdmBlackScholesOp(d["mesher"], d["process"], d["strike"])
    solver = ql.Fdm1DimSolver(desc, ql.FdmSchemeDesc.Douglas(), op)
    fdm_npv = solver.interpolateAt(math.log(100.0))

    assert fdm_npv == pytest.approx(analytic_npv, rel=1e-3)


def test_fdmblackscholessolver_vs_analytic(fdm_bs_setup):
    """FdmBlackScholesSolver vs Black-Scholes analytic price."""
    d = fdm_bs_setup
    engine = ql.AnalyticEuropeanEngine(d["process"])
    exercise = ql.EuropeanExercise(d["today"] + ql.Period(1, ql.Years))
    option = ql.VanillaOption(d["payoff"], exercise)
    option.setPricingEngine(engine)
    analytic_npv = option.NPV()
    analytic_delta = option.delta()

    calc = ql.FdmLogInnerValue(d["payoff"], d["mesher"], 0)
    conditions = ql.FdmStepConditionComposite.vanillaComposite(
        [], exercise, d["mesher"], calc, d["today"], d["dc"])
    desc = ql.FdmSolverDesc(
        mesher=d["mesher"], bcSet=[], condition=conditions,
        calculator=calc, maturity=d["maturity"], timeSteps=100)
    solver = ql.FdmBlackScholesSolver(d["process"], d["strike"], desc)

    assert solver.valueAt(100.0) == pytest.approx(analytic_npv, rel=1e-3)
    assert solver.deltaAt(100.0) == pytest.approx(analytic_delta, rel=1e-2)


def test_fdm_heston_european_call_2d():
    """2D Heston FDM pricing vs AnalyticHestonEngine."""
    today = ql.Date(15, 6, 2025)
    ql.Settings.evaluationDate = today
    dc = ql.Actual365Fixed()
    spot_val = 100.0
    strike = 100.0
    maturity_date = today + ql.Period(1, ql.Years)
    maturity = dc.yearFraction(today, maturity_date)

    rTS = ql.FlatForward(today, 0.05, dc)
    divTS = ql.FlatForward(today, 0.02, dc)
    spot = ql.SimpleQuote(spot_val)

    v0, kappa, theta, sigma, rho = 0.04, 1.0, 0.04, 0.5, -0.7
    heston = ql.HestonProcess(
        ql.YieldTermStructureHandle(rTS),
        ql.YieldTermStructureHandle(divTS),
        ql.QuoteHandle(spot),
        v0, kappa, theta, sigma, rho,
    )
    model = ql.HestonModel(heston)

    # Analytic benchmark
    payoff = ql.PlainVanillaPayoff(ql.OptionType.Call, strike)
    exercise = ql.EuropeanExercise(maturity_date)
    option = ql.VanillaOption(payoff, exercise)
    option.setPricingEngine(ql.AnalyticHestonEngine(model, 1e-10, 1000))
    analytic_npv = option.NPV()

    # FDM 2D solve: need BSM process for the mesher only
    vol_handle = ql.BlackConstantVol(today, ql.NullCalendar(), 0.20, dc)
    bsm = ql.BlackScholesMertonProcess(
        ql.QuoteHandle(spot),
        ql.YieldTermStructureHandle(divTS),
        ql.YieldTermStructureHandle(rTS),
        ql.BlackVolTermStructureHandle(vol_handle),
    )
    bs_mesher = ql.FdmBlackScholesMesher(100, bsm, maturity, strike)
    var_mesher = ql.FdmHestonVarianceMesher(25, heston, maturity)
    mesher = ql.FdmMesherComposite(bs_mesher, var_mesher)

    calc = ql.FdmLogInnerValue(payoff, mesher, 0)
    conditions = ql.FdmStepConditionComposite.vanillaComposite(
        [], exercise, mesher, calc, today, dc)
    desc = ql.FdmSolverDesc(
        mesher=mesher, bcSet=[], condition=conditions,
        calculator=calc, maturity=maturity, timeSteps=100, dampingSteps=0)
    op = ql.FdmHestonOp(mesher, heston)
    solver = ql.Fdm2DimSolver(desc, ql.FdmSchemeDesc.Hundsdorfer(), op)

    fdm_npv = solver.interpolateAt(math.log(spot_val), v0)
    assert fdm_npv == pytest.approx(analytic_npv, rel=5e-3)


def test_fdm_american_put_vs_european():
    """1D FDM American put vs European put (American >= European)."""
    today = ql.Date(15, 6, 2025)
    ql.Settings.evaluationDate = today
    dc = ql.Actual365Fixed()
    spot_val = 100.0
    strike = 100.0
    maturity_date = today + ql.Period(1, ql.Years)
    maturity = dc.yearFraction(today, maturity_date)

    rTS = ql.FlatForward(today, 0.05, dc)
    divTS = ql.FlatForward(today, 0.0, dc)
    spot = ql.SimpleQuote(spot_val)
    vol = ql.BlackConstantVol(today, ql.NullCalendar(), 0.20, dc)
    process = ql.BlackScholesMertonProcess(
        ql.QuoteHandle(spot),
        ql.YieldTermStructureHandle(divTS),
        ql.YieldTermStructureHandle(rTS),
        ql.BlackVolTermStructureHandle(vol),
    )

    put_payoff = ql.PlainVanillaPayoff(ql.OptionType.Put, strike)

    # European put (analytic)
    euro_exercise = ql.EuropeanExercise(maturity_date)
    euro_option = ql.VanillaOption(put_payoff, euro_exercise)
    euro_option.setPricingEngine(ql.AnalyticEuropeanEngine(process))
    euro_npv = euro_option.NPV()

    # American put via FDM with FdmAmericanStepCondition
    mesher = ql.FdmMesherComposite(
        ql.FdmBlackScholesMesher(200, process, maturity, strike))
    calc = ql.FdmLogInnerValue(put_payoff, mesher, 0)

    # Build American step condition via vanillaComposite with AmericanExercise
    amer_exercise = ql.AmericanExercise(today, maturity_date)
    conditions = ql.FdmStepConditionComposite.vanillaComposite(
        [], amer_exercise, mesher, calc, today, dc)
    desc = ql.FdmSolverDesc(
        mesher=mesher, bcSet=[], condition=conditions,
        calculator=calc, maturity=maturity, timeSteps=200, dampingSteps=0)
    solver = ql.FdmBlackScholesSolver(process, strike, desc)
    amer_npv = solver.valueAt(spot_val)

    # American put must be >= European put
    assert amer_npv >= euro_npv
    # American ATM put with r=5%, no dividends has meaningful early-exercise premium
    assert amer_npv == pytest.approx(6.0861, rel=5e-3)
