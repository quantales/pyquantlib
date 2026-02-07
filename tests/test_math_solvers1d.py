"""
Tests for 1-D root-finding solver bindings.

Corresponds to src/math/solvers1d/*.cpp bindings.
"""

import math

import pytest

import pyquantlib as ql


# =============================================================================
# Brent
# =============================================================================


def test_brent_bracketed():
    """Test Brent solver with explicit bracket."""
    solver = ql.Brent()
    root = solver.solve(lambda x: x**2 - 4, 1e-10, 1.0, 0.0, 10.0)
    assert root == pytest.approx(2.0, abs=1e-10)


def test_brent_autobracketing():
    """Test Brent solver with automatic bracketing."""
    solver = ql.Brent()
    root = solver.solve(lambda x: x**2 - 4, 1e-10, 1.0, 0.1)
    assert root == pytest.approx(2.0, abs=1e-10)


def test_brent_negative_root():
    """Test Brent finds negative root when bracket contains it."""
    solver = ql.Brent()
    root = solver.solve(lambda x: x**2 - 4, 1e-10, -1.0, -10.0, 0.0)
    assert root == pytest.approx(-2.0, abs=1e-10)


def test_brent_trig():
    """Test Brent solver on sin(x) = 0 near pi."""
    solver = ql.Brent()
    root = solver.solve(math.sin, 1e-10, 3.0, 2.0, 4.0)
    assert root == pytest.approx(math.pi, abs=1e-10)


# =============================================================================
# Bisection
# =============================================================================


def test_bisection_bracketed():
    """Test Bisection solver with explicit bracket."""
    solver = ql.Bisection()
    root = solver.solve(lambda x: x**2 - 4, 1e-10, 1.0, 0.0, 10.0)
    assert root == pytest.approx(2.0, abs=1e-10)


def test_bisection_autobracketing():
    """Test Bisection solver with automatic bracketing."""
    solver = ql.Bisection()
    root = solver.solve(lambda x: x**2 - 4, 1e-10, 1.0, 0.1)
    assert root == pytest.approx(2.0, abs=1e-10)


def test_bisection_cubic():
    """Test Bisection on x^3 - 8 = 0."""
    solver = ql.Bisection()
    root = solver.solve(lambda x: x**3 - 8, 1e-8, 1.0, 0.0, 5.0)
    assert root == pytest.approx(2.0, abs=1e-8)


# =============================================================================
# Secant
# =============================================================================


def test_secant_bracketed():
    """Test Secant solver with explicit bracket."""
    solver = ql.Secant()
    root = solver.solve(lambda x: x**2 - 4, 1e-10, 1.0, 0.0, 10.0)
    assert root == pytest.approx(2.0, abs=1e-10)


def test_secant_autobracketing():
    """Test Secant solver with automatic bracketing."""
    solver = ql.Secant()
    root = solver.solve(lambda x: x**2 - 4, 1e-10, 1.0, 0.1)
    assert root == pytest.approx(2.0, abs=1e-10)


def test_secant_exp():
    """Test Secant on exp(x) - 3 = 0."""
    solver = ql.Secant()
    root = solver.solve(lambda x: math.exp(x) - 3.0, 1e-10, 1.0, 0.0, 5.0)
    assert root == pytest.approx(math.log(3.0), abs=1e-10)


# =============================================================================
# Newton
# =============================================================================


def test_newton_bracketed():
    """Test Newton solver with explicit bracket."""
    solver = ql.Newton()
    root = solver.solve(
        lambda x: x**2 - 4,
        lambda x: 2 * x,
        1e-10, 1.0, 0.0, 10.0,
    )
    assert root == pytest.approx(2.0, abs=1e-10)


def test_newton_autobracketing():
    """Test Newton solver with automatic bracketing."""
    solver = ql.Newton()
    root = solver.solve(
        lambda x: x**2 - 4,
        lambda x: 2 * x,
        1e-10, 1.0, 0.1,
    )
    assert root == pytest.approx(2.0, abs=1e-10)


def test_newton_exp():
    """Test Newton on exp(x) - 3 = 0."""
    solver = ql.Newton()
    root = solver.solve(
        lambda x: math.exp(x) - 3.0,
        lambda x: math.exp(x),
        1e-10, 1.0, 0.0, 5.0,
    )
    assert root == pytest.approx(math.log(3.0), abs=1e-10)


# =============================================================================
# Common solver features
# =============================================================================


def test_solver_set_max_evaluations():
    """Test setMaxEvaluations limits function evaluations."""
    solver = ql.Brent()
    solver.setMaxEvaluations(2)
    with pytest.raises(ql.Error):
        solver.solve(lambda x: x**2 - 4, 1e-10, 1.0, 0.1)


def test_solver_set_bounds():
    """Test setLowerBound and setUpperBound."""
    solver = ql.Brent()
    solver.setLowerBound(0.0)
    solver.setUpperBound(100.0)
    root = solver.solve(lambda x: x**2 - 4, 1e-10, 1.0, 0.1)
    assert root == pytest.approx(2.0, abs=1e-10)


def test_solvers_agree():
    """Test that all solvers find the same root."""
    f = lambda x: x**3 - 2 * x - 5
    expected = 2.0945514815  # known root

    brent = ql.Brent().solve(f, 1e-8, 2.0, 1.0, 4.0)
    bisection = ql.Bisection().solve(f, 1e-8, 2.0, 1.0, 4.0)
    secant = ql.Secant().solve(f, 1e-8, 2.0, 1.0, 4.0)
    newton = ql.Newton().solve(
        f, lambda x: 3 * x**2 - 2, 1e-8, 2.0, 1.0, 4.0,
    )

    assert brent == pytest.approx(expected, abs=1e-6)
    assert bisection == pytest.approx(expected, abs=1e-6)
    assert secant == pytest.approx(expected, abs=1e-6)
    assert newton == pytest.approx(expected, abs=1e-6)
