"""Tests for numerical integration bindings.

Corresponds to src/math/integrals/*.cpp bindings.
"""

import math

import pytest

import pyquantlib as ql


# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------

def _sin(x):
    return math.sin(x)

def _exp(x):
    return math.exp(x)

def _x_squared(x):
    return x * x

def _gaussian(x):
    """Standard normal density (unnormalized)."""
    return math.exp(-0.5 * x * x)


# ---------------------------------------------------------------------------
# Integrator ABC
# ---------------------------------------------------------------------------

def test_integrator_is_abstract():
    """Integrator cannot be constructed directly."""
    with pytest.raises(TypeError):
        ql.base.Integrator()


# ---------------------------------------------------------------------------
# SegmentIntegral
# ---------------------------------------------------------------------------

def test_segmentintegral_sin():
    integrator = ql.SegmentIntegral(1000)
    result = integrator(_sin, 0.0, math.pi)
    assert result == pytest.approx(2.0, rel=1e-4)


def test_segmentintegral_x_squared():
    integrator = ql.SegmentIntegral(1000)
    result = integrator(_x_squared, 0.0, 1.0)
    assert result == pytest.approx(1.0 / 3.0, rel=1e-4)


def test_segmentintegral_inspectors():
    integrator = ql.SegmentIntegral(500)
    assert integrator.absoluteAccuracy() == pytest.approx(1.0)
    assert integrator.maxEvaluations() == 1


# ---------------------------------------------------------------------------
# TrapezoidIntegral
# ---------------------------------------------------------------------------

def test_trapezoidintegral_sin():
    integrator = ql.TrapezoidIntegral(1e-8, 100)
    result = integrator(_sin, 0.0, math.pi)
    assert result == pytest.approx(2.0, rel=1e-6)


def test_trapezoidintegral_exp():
    integrator = ql.TrapezoidIntegral(1e-8, 100)
    result = integrator(_exp, 0.0, 1.0)
    assert result == pytest.approx(math.e - 1.0, rel=1e-6)


# ---------------------------------------------------------------------------
# MidPointTrapezoidIntegral
# ---------------------------------------------------------------------------

def test_midpointtrapezoidintegral_sin():
    integrator = ql.MidPointTrapezoidIntegral(1e-4, 20)
    result = integrator(_sin, 0.0, math.pi)
    assert result == pytest.approx(2.0, rel=1e-4)


# ---------------------------------------------------------------------------
# SimpsonIntegral
# ---------------------------------------------------------------------------

def test_simpsonintegral_sin():
    integrator = ql.SimpsonIntegral(1e-8, 100)
    result = integrator(_sin, 0.0, math.pi)
    assert result == pytest.approx(2.0, rel=1e-8)


def test_simpsonintegral_x_squared():
    integrator = ql.SimpsonIntegral(1e-8, 100)
    result = integrator(_x_squared, 0.0, 1.0)
    assert result == pytest.approx(1.0 / 3.0, rel=1e-8)


# ---------------------------------------------------------------------------
# GaussKronrodAdaptive
# ---------------------------------------------------------------------------

def test_gausskronrodadaptive_sin():
    integrator = ql.GaussKronrodAdaptive(1e-10)
    result = integrator(_sin, 0.0, math.pi)
    assert result == pytest.approx(2.0, rel=1e-10)


def test_gausskronrodadaptive_with_max_evals():
    integrator = ql.GaussKronrodAdaptive(1e-8, maxFunctionEvaluations=10000)
    result = integrator(_sin, 0.0, math.pi)
    assert result == pytest.approx(2.0, rel=1e-8)


# ---------------------------------------------------------------------------
# GaussKronrodNonAdaptive
# ---------------------------------------------------------------------------

def test_gausskronrodnonadaptive_sin():
    integrator = ql.GaussKronrodNonAdaptive(1e-8, 10000, 1e-6)
    result = integrator(_sin, 0.0, math.pi)
    assert result == pytest.approx(2.0, rel=1e-6)


def test_gausskronrodnonadaptive_relative_accuracy():
    integrator = ql.GaussKronrodNonAdaptive(1e-8, 10000, 1e-6)
    assert integrator.relativeAccuracy() == pytest.approx(1e-6)


# ---------------------------------------------------------------------------
# GaussLobattoIntegral
# ---------------------------------------------------------------------------

def test_gausslobatto_sin():
    integrator = ql.GaussLobattoIntegral(1000, 1e-10)
    result = integrator(_sin, 0.0, math.pi)
    assert result == pytest.approx(2.0, rel=1e-10)


def test_gausslobatto_with_rel_accuracy():
    integrator = ql.GaussLobattoIntegral(1000, 1e-10, relAccuracy=1e-8)
    result = integrator(_sin, 0.0, math.pi)
    assert result == pytest.approx(2.0, rel=1e-8)


# ---------------------------------------------------------------------------
# TanhSinhIntegral
# ---------------------------------------------------------------------------

def test_tanhsinhintegral_sin():
    integrator = ql.TanhSinhIntegral()
    result = integrator(_sin, 0.0, math.pi)
    assert result == pytest.approx(2.0, rel=1e-10)


def test_tanhsinhintegral_gaussian():
    integrator = ql.TanhSinhIntegral()
    result = integrator(_gaussian, -10.0, 10.0)
    assert result == pytest.approx(math.sqrt(2.0 * math.pi), rel=1e-8)


# ---------------------------------------------------------------------------
# ExpSinhIntegral
# ---------------------------------------------------------------------------

def test_expsinhintegral_half_infinite():
    """Test half-infinite interval [0, inf) integration."""
    integrator = ql.ExpSinhIntegral()
    # Integrate exp(-x) over [0, inf) = 1.0
    result = integrator.integrateHalfInfinite(lambda x: math.exp(-x))
    assert result == pytest.approx(1.0, rel=1e-8)


# ---------------------------------------------------------------------------
# Integrator base class methods
# ---------------------------------------------------------------------------

def test_integrator_base_methods():
    integrator = ql.SimpsonIntegral(1e-8, 100)
    assert integrator.absoluteAccuracy() == pytest.approx(1e-8)
    assert integrator.maxEvaluations() == 100

    integrator(_sin, 0.0, math.pi)
    assert integrator.numberOfEvaluations() > 0


def test_integrator_set_accuracy():
    integrator = ql.SimpsonIntegral(1e-6, 50)
    integrator.setAbsoluteAccuracy(1e-10)
    assert integrator.absoluteAccuracy() == pytest.approx(1e-10)
    integrator.setMaxEvaluations(200)
    assert integrator.maxEvaluations() == 200


# ---------------------------------------------------------------------------
# GaussianQuadrature hierarchy
# ---------------------------------------------------------------------------

def test_gausslegendre_integration():
    """Gauss-Legendre integrates polynomials exactly on [-1, 1]."""
    quad = ql.GaussLegendreIntegration(5)
    # x^4 integrated on [-1, 1] = 2/5
    result = quad(lambda x: x**4)
    assert result == pytest.approx(2.0 / 5.0, rel=1e-12)


def test_gausslegendre_order():
    quad = ql.GaussLegendreIntegration(10)
    assert quad.order() == 10


def test_gausslegendre_weights_and_x():
    quad = ql.GaussLegendreIntegration(5)
    assert len(quad.weights()) == 5
    assert len(quad.x()) == 5


def test_gausslaguerre_integration():
    """Gauss-Laguerre uses nodes optimal for exp(-x) weight on [0, inf)."""
    quad = ql.GaussLaguerreIntegration(32)
    # integral of exp(-x) dx from 0 to inf = 1.0
    result = quad(lambda x: math.exp(-x))
    assert result == pytest.approx(1.0, rel=1e-8)


def test_gausshermite_integration():
    """Gauss-Hermite uses nodes optimal for exp(-x^2) weight on (-inf, inf)."""
    quad = ql.GaussHermiteIntegration(32)
    # integral of exp(-x^2) dx from -inf to inf = sqrt(pi)
    result = quad(lambda x: math.exp(-x * x))
    assert result == pytest.approx(math.sqrt(math.pi), rel=1e-8)


def test_gaussjacobi_integration():
    quad = ql.GaussJacobiIntegration(10, 0.0, 0.0)
    # With alpha=beta=0, weight = 1, so this is Legendre
    result = quad(lambda x: x * x)
    assert result == pytest.approx(2.0 / 3.0, rel=1e-12)


def test_gausshyperbolic_integration():
    quad = ql.GaussHyperbolicIntegration(32)
    # Nodes optimal for 1/cosh(x) weight on (-inf, inf)
    # integral of 1/cosh(x) dx from -inf to inf = pi
    result = quad(lambda x: 1.0 / math.cosh(x))
    assert result == pytest.approx(math.pi, rel=1e-8)


def test_gausschebyshev_integration():
    quad = ql.GaussChebyshevIntegration(32)
    # Nodes optimal for (1-x^2)^(-1/2) weight on [-1, 1]
    # integral of 1 dx from -1 to 1 = 2 (approx with Chebyshev nodes)
    result = quad(lambda x: 1.0)
    assert result == pytest.approx(2.0008034163, rel=1e-4)


def test_gausschebyshev2nd_integration():
    quad = ql.GaussChebyshev2ndIntegration(32)
    # Nodes optimal for (1-x^2)^(1/2) weight on [-1, 1]
    # integral of 1 dx from -1 to 1 = 2 (approx with Chebyshev 2nd kind nodes)
    result = quad(lambda x: 1.0)
    assert result == pytest.approx(1.9984892722, rel=1e-4)


def test_gaussgegenbauer_integration():
    quad = ql.GaussGegenbauerIntegration(32, 0.5)
    # lambda=0.5 -> weight = (1-x^2)^0, i.e. unit weight = Legendre
    # integral of x^4 dx from -1 to 1 = 2/5
    result = quad(lambda x: x**4)
    assert result == pytest.approx(2.0 / 5.0, rel=1e-10)


# ---------------------------------------------------------------------------
# TabulatedGaussLegendre
# ---------------------------------------------------------------------------

def test_tabulatedgausslegendre():
    quad = ql.TabulatedGaussLegendre(20)
    assert quad.order() == 20
    result = quad(lambda x: x * x)
    assert result == pytest.approx(2.0 / 3.0, rel=1e-10)


def test_tabulatedgausslegendre_order_7():
    quad = ql.TabulatedGaussLegendre(7)
    assert quad.order() == 7


# ---------------------------------------------------------------------------
# GaussianQuadratureIntegrator (Integrator subclasses)
# ---------------------------------------------------------------------------

def test_gausslegendreintegrator():
    integrator = ql.GaussLegendreIntegrator(64)
    result = integrator(_sin, 0.0, math.pi)
    assert result == pytest.approx(2.0, rel=1e-10)


def test_gausschebyshevintegrator():
    integrator = ql.GaussChebyshevIntegrator(64)
    result = integrator(_sin, 0.0, math.pi)
    assert result == pytest.approx(2.0, rel=1e-4)


def test_gausschebyshev2ndintegrator():
    integrator = ql.GaussChebyshev2ndIntegrator(64)
    result = integrator(_sin, 0.0, math.pi)
    assert result == pytest.approx(2.0, rel=1e-4)
