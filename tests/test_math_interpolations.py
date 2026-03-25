"""Tests for interpolation bindings.

Corresponds to src/math/interpolations/*.cpp bindings.
"""

import math

import numpy as np
import pytest

import pyquantlib as ql


# ---------------------------------------------------------------------------
# ForwardFlatInterpolation
# ---------------------------------------------------------------------------

def test_forwardflat_construction():
    x = [1.0, 2.0, 3.0]
    y = [10.0, 20.0, 30.0]
    interp = ql.ForwardFlatInterpolation(x, y)
    assert isinstance(interp, ql.base.Interpolation)


def test_forwardflat_call():
    x = [1.0, 2.0, 3.0]
    y = [10.0, 20.0, 30.0]
    interp = ql.ForwardFlatInterpolation(x, y)

    # At nodes
    assert interp(1.0) == pytest.approx(10.0)
    assert interp(2.0) == pytest.approx(20.0)
    assert interp(3.0) == pytest.approx(30.0)

    # Between nodes - forward flat uses current node's value
    assert interp(1.5) == pytest.approx(10.0)
    assert interp(2.5) == pytest.approx(20.0)


def test_forwardflat_data_lifetime():
    def create_interp():
        return ql.ForwardFlatInterpolation([1.0, 2.0, 3.0], [10.0, 20.0, 30.0])

    interp = create_interp()
    assert interp(1.5) == pytest.approx(10.0)


# ---------------------------------------------------------------------------
# LagrangeInterpolation
# ---------------------------------------------------------------------------

def test_lagrange_construction():
    x = [1.0, 2.0, 3.0]
    y = [1.0, 4.0, 9.0]
    interp = ql.LagrangeInterpolation(x, y)
    assert isinstance(interp, ql.base.Interpolation)


def test_lagrange_call():
    # Use non-zero nodes (QL Lagrange has a known tolerance issue at x=0)
    x = [1.0, 2.0, 3.0]
    y = [1.0, 4.0, 9.0]  # y = x^2
    interp = ql.LagrangeInterpolation(x, y)

    assert interp(1.0) == pytest.approx(1.0)
    assert interp(2.0) == pytest.approx(4.0)
    assert interp(3.0) == pytest.approx(9.0)
    assert interp(1.5) == pytest.approx(2.25, rel=1e-10)
    assert interp(2.5) == pytest.approx(6.25, rel=1e-10)


def test_lagrange_value_with_alt_y():
    """Test Lagrange value() with alternative y values."""
    x = [1.0, 2.0, 3.0]
    y = [1.0, 4.0, 9.0]
    interp = ql.LagrangeInterpolation(x, y)

    # Evaluate with different y: [1, 8, 27] (3 points give degree-2 polynomial)
    alt_y = ql.Array([1.0, 8.0, 27.0])
    assert interp.value(alt_y, 1.5) == pytest.approx(3.0, rel=1e-10)
    assert interp.value(alt_y, 2.0) == pytest.approx(8.0, rel=1e-10)


def test_lagrange_data_lifetime():
    def create_interp():
        return ql.LagrangeInterpolation([1.0, 2.0, 3.0], [1.0, 4.0, 9.0])

    interp = create_interp()
    assert interp(1.5) == pytest.approx(2.25, rel=1e-10)


# ---------------------------------------------------------------------------
# Interpolation2D base
# ---------------------------------------------------------------------------

def test_interpolation2d_base_exists():
    assert hasattr(ql.base, "Interpolation2D")


# ---------------------------------------------------------------------------
# BilinearInterpolation
# ---------------------------------------------------------------------------

def test_bilinear_construction():
    x = [0.0, 1.0]
    y = [0.0, 1.0]
    # QL convention: z[y_idx][x_idx], so z.rows = len(y), z.columns = len(x)
    z = ql.Matrix([[1.0, 2.0], [3.0, 4.0]])
    interp = ql.BilinearInterpolation(x, y, z)
    assert isinstance(interp, ql.base.Interpolation2D)


def test_bilinear_call():
    x = [0.0, 1.0]
    y = [0.0, 1.0]
    # QL convention: z[y_idx][x_idx]
    # z[0][0]=1 at (x=0,y=0), z[0][1]=2 at (x=1,y=0)
    # z[1][0]=3 at (x=0,y=1), z[1][1]=4 at (x=1,y=1)
    z = ql.Matrix([[1.0, 2.0], [3.0, 4.0]])
    interp = ql.BilinearInterpolation(x, y, z)

    assert interp(0.0, 0.0) == pytest.approx(1.0)
    assert interp(1.0, 0.0) == pytest.approx(2.0)
    assert interp(0.0, 1.0) == pytest.approx(3.0)
    assert interp(1.0, 1.0) == pytest.approx(4.0)

    # Center - bilinear average
    assert interp(0.5, 0.5) == pytest.approx(2.5)


def test_bilinear_inspectors():
    x = [1.0, 2.0, 3.0]
    y = [10.0, 20.0]
    # z.rows = len(y) = 2, z.columns = len(x) = 3
    z = ql.Matrix([[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]])
    interp = ql.BilinearInterpolation(x, y, z)

    assert interp.xMin() == pytest.approx(1.0)
    assert interp.xMax() == pytest.approx(3.0)
    assert interp.yMin() == pytest.approx(10.0)
    assert interp.yMax() == pytest.approx(20.0)
    assert interp.isInRange(2.0, 15.0)
    assert not interp.isInRange(0.0, 15.0)


def test_bilinear_data_lifetime():
    def create_interp():
        return ql.BilinearInterpolation(
            [0.0, 1.0], [0.0, 1.0],
            ql.Matrix([[1.0, 2.0], [3.0, 4.0]]))

    interp = create_interp()
    assert interp(0.5, 0.5) == pytest.approx(2.5)


# ---------------------------------------------------------------------------
# BicubicSpline
# ---------------------------------------------------------------------------

def test_bicubicspline_construction():
    x = [0.0, 1.0, 2.0]
    y = [0.0, 1.0, 2.0]
    # z[y_idx][x_idx] = x * y
    z = ql.Matrix([
        [0.0, 0.0, 0.0],   # y=0: all zeros
        [0.0, 1.0, 2.0],   # y=1: x * 1
        [0.0, 2.0, 4.0],   # y=2: x * 2
    ])
    interp = ql.BicubicSpline(x, y, z)
    assert isinstance(interp, ql.base.Interpolation2D)


def test_bicubicspline_call():
    x = [0.0, 1.0, 2.0]
    y = [0.0, 1.0, 2.0]
    # z[y_idx][x_idx] = x * y
    z = ql.Matrix([
        [0.0, 0.0, 0.0],
        [0.0, 1.0, 2.0],
        [0.0, 2.0, 4.0],
    ])
    interp = ql.BicubicSpline(x, y, z)

    # At nodes
    assert interp(0.0, 0.0) == pytest.approx(0.0)
    assert interp(1.0, 1.0) == pytest.approx(1.0)
    assert interp(2.0, 2.0) == pytest.approx(4.0)

    # Between nodes
    assert interp(0.5, 0.5) == pytest.approx(0.25, abs=0.1)


def test_bicubicspline_derivatives():
    x = [0.0, 1.0, 2.0]
    y = [0.0, 1.0, 2.0]
    # z[y_idx][x_idx] = x * y
    z = ql.Matrix([
        [0.0, 0.0, 0.0],
        [0.0, 1.0, 2.0],
        [0.0, 2.0, 4.0],
    ])
    interp = ql.BicubicSpline(x, y, z)

    # derivativeX at (1, 1): d/dx (x*y) = y = 1
    dx = interp.derivativeX(1.0, 1.0)
    assert dx == pytest.approx(1.0, abs=0.2)

    # derivativeY at (1, 1): d/dy (x*y) = x = 1
    dy = interp.derivativeY(1.0, 1.0)
    assert dy == pytest.approx(1.0, abs=0.2)


def test_bicubicspline_data_lifetime():
    def create_interp():
        return ql.BicubicSpline(
            [0.0, 1.0, 2.0], [0.0, 1.0, 2.0],
            ql.Matrix([
                [0.0, 0.0, 0.0],
                [0.0, 1.0, 2.0],
                [0.0, 2.0, 4.0],
            ]))

    interp = create_interp()
    assert interp(1.0, 1.0) == pytest.approx(1.0)


# ---------------------------------------------------------------------------
# ChebyshevInterpolation
# ---------------------------------------------------------------------------

def test_chebyshev_enum():
    assert hasattr(ql, "ChebyshevPointsType")
    assert hasattr(ql.ChebyshevPointsType, "FirstKind")
    assert hasattr(ql.ChebyshevPointsType, "SecondKind")


def test_chebyshev_from_function():
    """Chebyshev interpolation of sin(x) on [-1, 1]."""
    interp = ql.ChebyshevInterpolation(20, math.sin)
    assert interp(0.0) == pytest.approx(0.0, abs=1e-10)
    assert interp(0.5) == pytest.approx(math.sin(0.5), rel=1e-10)


def test_chebyshev_from_array():
    """Construct from pre-computed y values."""
    n = 10
    nodes = ql.ChebyshevInterpolation.nodesStatic(n, ql.ChebyshevPointsType.SecondKind)
    y = ql.Array([math.cos(x) for x in nodes])
    interp = ql.ChebyshevInterpolation(y)
    assert interp(0.0) == pytest.approx(1.0, abs=1e-6)


def test_chebyshev_nodes():
    interp = ql.ChebyshevInterpolation(5, lambda x: x)
    nodes = interp.nodes()
    assert len(nodes) == 5


def test_chebyshev_update_y():
    interp = ql.ChebyshevInterpolation(10, math.sin)
    # Update to cos
    nodes = interp.nodes()
    new_y = ql.Array([math.cos(x) for x in nodes])
    interp.updateY(new_y)
    assert interp(0.0) == pytest.approx(1.0, abs=1e-6)


# ---------------------------------------------------------------------------
# RichardsonExtrapolation
# ---------------------------------------------------------------------------

def test_richardson_construction():
    f = lambda h: math.sin(h) / h  # limit as h->0 is 1.0
    re = ql.RichardsonExtrapolation(f, 0.1, n=2.0)
    assert re is not None


def test_richardson_call():
    # f(h) = sin(h)/h has error O(h^2), n=2 tells Richardson the order
    f = lambda h: math.sin(h) / h
    re = ql.RichardsonExtrapolation(f, 0.01, n=2.0)
    result = re(2.0)
    assert result == pytest.approx(1.0, rel=1e-8)


def test_richardson_second_order():
    # Two-arg overload does not require n (t must be > s)
    f = lambda h: math.sin(h) / h
    re = ql.RichardsonExtrapolation(f, 0.01)
    result = re(4.0, 2.0)
    assert result == pytest.approx(1.0, rel=1e-10)


# ---------------------------------------------------------------------------
# MixedLinearCubicInterpolation
# ---------------------------------------------------------------------------

def test_mixed_interpolation_behavior_enum():
    """MixedInterpolationBehavior enum is accessible."""
    assert ql.MixedInterpolationBehavior.ShareRanges is not None
    assert ql.MixedInterpolationBehavior.SplitRanges is not None


def test_mixed_linear_cubic_construction():
    """MixedLinearCubicInterpolation constructs and evaluates."""
    x = [0.0, 1.0, 2.0, 3.0, 4.0, 5.0]
    y = [0.0, 1.0, 4.0, 9.0, 16.0, 25.0]
    # Switch at n=2: first 2 points linear, rest cubic
    interp = ql.MixedLinearCubicInterpolation(x, y, n=2)
    assert isinstance(interp, ql.base.Interpolation)

    # At nodes
    assert interp(0.0) == pytest.approx(0.0)
    assert interp(3.0) == pytest.approx(9.0)
    assert interp(5.0) == pytest.approx(25.0)

    # Between nodes
    val = interp(2.5)
    assert 4.0 < val < 9.0


def test_mixed_linear_cubic_natural_spline():
    """MixedLinearCubicNaturalSpline convenience class."""
    x = [0.0, 1.0, 2.0, 3.0, 4.0, 5.0]
    y = [0.0, 1.0, 4.0, 9.0, 16.0, 25.0]
    interp = ql.MixedLinearCubicNaturalSpline(x, y, n=2)
    assert isinstance(interp, ql.MixedLinearCubicInterpolation)
    assert interp(3.0) == pytest.approx(9.0)


def test_mixed_linear_monotonic_cubic():
    """MixedLinearMonotonicCubicNaturalSpline preserves monotonicity."""
    x = [0.0, 1.0, 2.0, 3.0, 4.0, 5.0]
    y = [1.0, 2.0, 3.0, 5.0, 8.0, 13.0]
    interp = ql.MixedLinearMonotonicCubicNaturalSpline(x, y, n=2)
    assert isinstance(interp, ql.MixedLinearCubicInterpolation)

    # Check monotonicity between nodes
    prev = interp(0.0)
    for t in np.linspace(0.1, 5.0, 50):
        val = interp(t)
        assert val >= prev - 1e-10
        prev = val


def test_mixed_linear_kruger():
    """MixedLinearKrugerCubic convenience class."""
    x = [0.0, 1.0, 2.0, 3.0, 4.0, 5.0]
    y = [0.0, 1.0, 4.0, 9.0, 16.0, 25.0]
    interp = ql.MixedLinearKrugerCubic(x, y, n=2)
    assert isinstance(interp, ql.MixedLinearCubicInterpolation)
    assert interp(4.0) == pytest.approx(16.0)


def test_mixed_linear_fritsch_butland():
    """MixedLinearFritschButlandCubic convenience class."""
    x = [0.0, 1.0, 2.0, 3.0, 4.0, 5.0]
    y = [0.0, 1.0, 4.0, 9.0, 16.0, 25.0]
    interp = ql.MixedLinearFritschButlandCubic(x, y, n=2)
    assert isinstance(interp, ql.MixedLinearCubicInterpolation)
    assert interp(5.0) == pytest.approx(25.0)


def test_mixed_split_ranges():
    """SplitRanges behavior splits interpolation at switch point."""
    x = [0.0, 1.0, 2.0, 3.0, 4.0, 5.0]
    y = [0.0, 1.0, 4.0, 9.0, 16.0, 25.0]
    interp = ql.MixedLinearCubicNaturalSpline(
        x, y, n=2, behavior=ql.MixedInterpolationBehavior.SplitRanges)

    # Should still hit nodes exactly
    assert interp(0.0) == pytest.approx(0.0)
    assert interp(2.0) == pytest.approx(4.0)
    assert interp(5.0) == pytest.approx(25.0)


def test_mixed_data_lifetime():
    """Interpolation survives after input lists go out of scope."""
    def make():
        x = [0.0, 1.0, 2.0, 3.0, 4.0, 5.0]
        y = [0.0, 1.0, 4.0, 9.0, 16.0, 25.0]
        return ql.MixedLinearCubicNaturalSpline(x, y, n=2)

    interp = make()
    assert interp(3.0) == pytest.approx(9.0)


# ---------------------------------------------------------------------------
# LogCubicInterpolation
# ---------------------------------------------------------------------------

def test_log_cubic_construction():
    """LogCubicInterpolation constructs and evaluates."""
    x = [1.0, 2.0, 3.0, 4.0, 5.0]
    y = [1.0, 2.0, 3.0, 4.0, 5.0]  # must be positive for log
    interp = ql.LogCubicInterpolation(x, y)
    assert isinstance(interp, ql.base.Interpolation)
    assert interp(1.0) == pytest.approx(1.0)
    assert interp(5.0) == pytest.approx(5.0)


def test_log_cubic_natural_spline():
    """LogCubicNaturalSpline convenience class."""
    x = [1.0, 2.0, 3.0, 4.0, 5.0]
    y = [0.01, 0.02, 0.03, 0.04, 0.05]
    interp = ql.LogCubicNaturalSpline(x, y)
    assert isinstance(interp, ql.base.Interpolation)
    assert interp(3.0) == pytest.approx(0.03)


def test_monotonic_log_cubic_natural_spline():
    """MonotonicLogCubicNaturalSpline preserves monotonicity."""
    x = [1.0, 2.0, 3.0, 4.0, 5.0]
    y = [0.90, 0.92, 0.95, 0.97, 0.99]
    interp = ql.MonotonicLogCubicNaturalSpline(x, y)
    assert isinstance(interp, ql.base.Interpolation)

    prev = interp(1.0)
    for t in np.linspace(1.1, 5.0, 40):
        val = interp(t)
        assert val >= prev - 1e-10
        prev = val


def test_kruger_log_cubic():
    """KrugerLogCubic convenience class."""
    x = [1.0, 2.0, 3.0, 4.0, 5.0]
    y = [0.01, 0.02, 0.03, 0.04, 0.05]
    interp = ql.KrugerLogCubic(x, y)
    assert isinstance(interp, ql.base.Interpolation)
    assert interp(4.0) == pytest.approx(0.04)


def test_harmonic_log_cubic():
    """HarmonicLogCubic convenience class."""
    x = [1.0, 2.0, 3.0, 4.0, 5.0]
    y = [0.01, 0.02, 0.03, 0.04, 0.05]
    interp = ql.HarmonicLogCubic(x, y)
    assert isinstance(interp, ql.base.Interpolation)
    assert interp(5.0) == pytest.approx(0.05)


def test_fritsch_butland_log_cubic():
    """FritschButlandLogCubic convenience class."""
    x = [1.0, 2.0, 3.0, 4.0, 5.0]
    y = [0.01, 0.02, 0.03, 0.04, 0.05]
    interp = ql.FritschButlandLogCubic(x, y)
    assert isinstance(interp, ql.base.Interpolation)
    assert interp(3.0) == pytest.approx(0.03)


def test_log_cubic_data_lifetime():
    """Log-cubic interpolation survives after input lists go out of scope."""
    def make():
        x = [1.0, 2.0, 3.0, 4.0, 5.0]
        y = [0.01, 0.02, 0.03, 0.04, 0.05]
        return ql.KrugerLogCubic(x, y)

    interp = make()
    assert interp(3.0) == pytest.approx(0.03)


# ---------------------------------------------------------------------------
# LogMixedLinearCubicInterpolation
# ---------------------------------------------------------------------------

def test_log_mixed_construction():
    """LogMixedLinearCubicInterpolation constructs and evaluates."""
    x = [1.0, 2.0, 3.0, 4.0, 5.0, 6.0]
    y = [0.90, 0.92, 0.95, 0.97, 0.98, 0.99]
    interp = ql.LogMixedLinearCubicInterpolation(x, y, n=2)
    assert isinstance(interp, ql.base.Interpolation)
    assert interp(1.0) == pytest.approx(0.90)
    assert interp(6.0) == pytest.approx(0.99)


def test_log_mixed_natural_spline():
    """LogMixedLinearCubicNaturalSpline convenience class."""
    x = [1.0, 2.0, 3.0, 4.0, 5.0, 6.0]
    y = [0.90, 0.92, 0.95, 0.97, 0.98, 0.99]
    interp = ql.LogMixedLinearCubicNaturalSpline(x, y, n=2)
    assert isinstance(interp, ql.base.Interpolation)
    assert interp(4.0) == pytest.approx(0.97)


def test_log_mixed_data_lifetime():
    """Log-mixed interpolation survives after input lists go out of scope."""
    def make():
        x = [1.0, 2.0, 3.0, 4.0, 5.0, 6.0]
        y = [0.90, 0.92, 0.95, 0.97, 0.98, 0.99]
        return ql.LogMixedLinearCubicNaturalSpline(x, y, n=2)

    interp = make()
    assert interp(3.0) == pytest.approx(0.95)
