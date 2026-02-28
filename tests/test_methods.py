"""
Tests for methods module.

Corresponds to src/methods/*.cpp bindings.
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
