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


# =============================================================================
# FalsePosition, Ridder, NewtonSafe, Halley
# =============================================================================


@pytest.mark.parametrize("solver_cls", [ql.FalsePosition, ql.Ridder],
                         ids=["FalsePosition", "Ridder"])
def test_bracketing_solvers(solver_cls):
    """FalsePosition and Ridder find a root with and without a bracket."""
    solver = solver_cls()
    bracketed = solver.solve(lambda x: x**2 - 4, 1e-10, 1.0, 0.0, 10.0)
    assert bracketed == pytest.approx(2.0, abs=1e-9)
    auto = solver_cls().solve(lambda x: x**2 - 4, 1e-10, 1.0, 0.1)
    assert auto == pytest.approx(2.0, abs=1e-9)
    negative = solver_cls().solve(lambda x: x**2 - 4, 1e-10, -1.0, -10.0, 0.0)
    assert negative == pytest.approx(-2.0, abs=1e-9)


@pytest.mark.parametrize("solver_cls", [ql.FalsePosition, ql.Ridder],
                         ids=["FalsePosition", "Ridder"])
def test_bracketing_solvers_trig(solver_cls):
    """The solvers handle a transcendental equation, cos(x) = x."""
    root = solver_cls().solve(lambda x: math.cos(x) - x, 1e-12, 0.5, 0.0, 1.0)
    assert root == pytest.approx(0.7390851332151607, abs=1e-10)


@pytest.mark.parametrize("solver_cls", [ql.FalsePosition, ql.Ridder],
                         ids=["FalsePosition", "Ridder"])
def test_bracketing_solvers_bad_bracket(solver_cls):
    """A bracket without a sign change is rejected."""
    with pytest.raises(ql.Error):
        solver_cls().solve(lambda x: x**2 + 1, 1e-10, 1.0, 0.0, 10.0)


def test_bracketing_solvers_max_evaluations():
    """A tight evaluation limit makes the solver fail."""
    solver = ql.FalsePosition()
    solver.setMaxEvaluations(2)
    with pytest.raises(ql.Error):
        solver.solve(lambda x: x**3 - 2, 1e-14, 1.0, 0.0, 10.0)


def test_newtonsafe_bracketed():
    """NewtonSafe finds a root inside an explicit bracket."""
    solver = ql.NewtonSafe()
    root = solver.solve(lambda x: x**2 - 2, lambda x: 2 * x, 1e-12, 1.0, 0.0, 10.0)
    assert root == pytest.approx(math.sqrt(2.0), abs=1e-10)


def test_newtonsafe_autobracketing():
    """NewtonSafe brackets automatically from a guess and a step."""
    root = ql.NewtonSafe().solve(lambda x: x**2 - 2, lambda x: 2 * x, 1e-12, 1.0, 0.1)
    assert root == pytest.approx(math.sqrt(2.0), abs=1e-10)


def test_newtonsafe_stays_in_bracket_with_flat_derivative():
    """A near-zero derivative at the guess does not send NewtonSafe out of the bracket."""
    # f(x) = x**3 - 1 has f'(0) = 0; a plain Newton step from 0 would diverge
    root = ql.NewtonSafe().solve(lambda x: x**3 - 1, lambda x: 3 * x**2,
                                 1e-12, 0.0, -2.0, 3.0)
    assert root == pytest.approx(1.0, abs=1e-10)


def test_halley_bracketed():
    """Halley finds a root using first and second derivatives."""
    root = ql.Halley().solve(lambda x: x**2 - 2, lambda x: 2 * x, lambda x: 2.0,
                             1e-12, 1.0, 0.0, 10.0)
    assert root == pytest.approx(math.sqrt(2.0), abs=1e-10)


def test_halley_autobracketing():
    """Halley brackets automatically from a guess and a step."""
    root = ql.Halley().solve(lambda x: x**3 - 5, lambda x: 3 * x**2, lambda x: 6 * x,
                             1e-12, 2.0, 0.1)
    assert root == pytest.approx(5.0 ** (1.0 / 3.0), abs=1e-10)


def test_derivative_solvers_set_bounds_and_evaluations():
    """NewtonSafe and Halley expose the common solver controls."""
    for solver in (ql.NewtonSafe(), ql.Halley()):
        solver.setMaxEvaluations(100)
        solver.setLowerBound(0.0)
        solver.setUpperBound(10.0)
