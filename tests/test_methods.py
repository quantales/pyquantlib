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
