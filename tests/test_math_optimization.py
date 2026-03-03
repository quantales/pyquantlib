"""Tests for optimization method bindings.

Corresponds to src/math/optimization/*.cpp bindings.
"""

import math

import pytest

import pyquantlib as ql


# ---------------------------------------------------------------------------
# Simplex
# ---------------------------------------------------------------------------

def test_simplex_construction():
    opt = ql.Simplex(0.1)
    assert opt.lambda_() == pytest.approx(0.1)


def test_simplex_minimize_rosenbrock():
    """Minimize 2-D Rosenbrock function near origin."""
    class Rosenbrock(ql.base.CostFunction):
        def value(self, x):
            return (1.0 - x[0])**2 + 100.0 * (x[1] - x[0]**2)**2
        def values(self, x):
            return ql.Array([self.value(x)])

    cost = Rosenbrock()
    constraint = ql.NoConstraint()
    ec = ql.EndCriteria(1000, 100, 1e-10, 1e-10, 1e-10)
    opt = ql.Simplex(0.1)
    problem = ql.Problem(cost, constraint, ql.Array([0.0, 0.0]))
    opt.minimize(problem, ec)
    x = problem.currentValue()
    assert x[0] == pytest.approx(1.0, abs=1e-3)
    assert x[1] == pytest.approx(1.0, abs=1e-3)


# ---------------------------------------------------------------------------
# ConjugateGradient
# ---------------------------------------------------------------------------

def test_conjugategradient_construction():
    opt = ql.ConjugateGradient()
    assert isinstance(opt, ql.base.OptimizationMethod)


# ---------------------------------------------------------------------------
# SteepestDescent
# ---------------------------------------------------------------------------

def test_steepestdescent_construction():
    opt = ql.SteepestDescent()
    assert isinstance(opt, ql.base.OptimizationMethod)


# ---------------------------------------------------------------------------
# BFGS
# ---------------------------------------------------------------------------

def test_bfgs_construction():
    opt = ql.BFGS()
    assert isinstance(opt, ql.base.OptimizationMethod)


# ---------------------------------------------------------------------------
# DifferentialEvolution
# ---------------------------------------------------------------------------

def test_de_enums():
    assert hasattr(ql, "DEStrategy")
    assert hasattr(ql, "DECrossoverType")
    assert hasattr(ql.DEStrategy, "Rand1Standard")
    assert hasattr(ql.DEStrategy, "BestMemberWithJitter")
    assert hasattr(ql.DECrossoverType, "Normal")
    assert hasattr(ql.DECrossoverType, "Binomial")
    assert hasattr(ql.DECrossoverType, "Exponential")


def test_de_configuration():
    config = ql.DEConfiguration()
    assert config.populationMembers == 100
    assert config.stepsizeWeight == pytest.approx(0.2)
    assert config.crossoverProbability == pytest.approx(0.9)
    assert config.seed == 0


def test_de_configuration_builder():
    config = (ql.DEConfiguration()
        .withStrategy(ql.DEStrategy.Rand1Standard)
        .withCrossoverType(ql.DECrossoverType.Binomial)
        .withPopulationMembers(50)
        .withStepsizeWeight(0.5)
        .withCrossoverProbability(0.8)
        .withSeed(42))
    assert config.strategy == ql.DEStrategy.Rand1Standard
    assert config.crossoverType == ql.DECrossoverType.Binomial
    assert config.populationMembers == 50
    assert config.stepsizeWeight == pytest.approx(0.5)
    assert config.crossoverProbability == pytest.approx(0.8)
    assert config.seed == 42


def test_de_construction():
    opt = ql.DifferentialEvolution()
    assert isinstance(opt, ql.base.OptimizationMethod)


def test_de_minimize_sphere():
    """Minimize sphere function f(x) = x[0]^2 + x[1]^2."""
    class Sphere(ql.base.CostFunction):
        def value(self, x):
            return x[0]**2 + x[1]**2
        def values(self, x):
            return ql.Array([self.value(x)])

    config = (ql.DEConfiguration()
        .withPopulationMembers(50)
        .withSeed(42)
        .withBounds(True)
        .withUpperBound(ql.Array([5.0, 5.0]))
        .withLowerBound(ql.Array([-5.0, -5.0])))
    opt = ql.DifferentialEvolution(config)
    ec = ql.EndCriteria(1000, 100, 1e-10, 1e-10, 1e-10)
    cost = Sphere()
    constraint = ql.NoConstraint()
    problem = ql.Problem(cost, constraint, ql.Array([3.0, 3.0]))
    opt.minimize(problem, ec)
    x = problem.currentValue()
    assert x[0] == pytest.approx(0.0, abs=1e-3)
    assert x[1] == pytest.approx(0.0, abs=1e-3)
