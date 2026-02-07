"""
Tests for mathematical distribution bindings.

Corresponds to src/math/distributions/*.cpp bindings.
"""

import math

import pytest

import pyquantlib as ql


# =============================================================================
# NormalDistribution
# =============================================================================


def test_normaldistribution_standard():
    """Test standard normal PDF at x=0."""
    n = ql.NormalDistribution()
    # PDF at x=0 for standard normal = 1/sqrt(2*pi)
    expected = 1.0 / math.sqrt(2.0 * math.pi)
    assert n(0.0) == pytest.approx(expected, rel=1e-10)


def test_normaldistribution_symmetry():
    """Test that standard normal PDF is symmetric."""
    n = ql.NormalDistribution()
    assert n(1.0) == pytest.approx(n(-1.0), rel=1e-10)


def test_normaldistribution_custom_params():
    """Test normal PDF with custom average and sigma."""
    n = ql.NormalDistribution(average=2.0, sigma=0.5)
    # Peak should be at x=average
    assert n(2.0) > n(1.0)
    assert n(2.0) > n(3.0)


def test_normaldistribution_derivative():
    """Test NormalDistribution derivative."""
    n = ql.NormalDistribution()
    # Derivative at x=0 should be 0 (peak of the bell curve)
    assert n.derivative(0.0) == pytest.approx(0.0, abs=1e-10)
    # Derivative at x=1 should be negative (descending)
    assert n.derivative(1.0) < 0.0


# =============================================================================
# CumulativeNormalDistribution
# =============================================================================


def test_cumulativenormal_at_zero():
    """Test CDF at x=0 for standard normal."""
    cdf = ql.CumulativeNormalDistribution()
    assert cdf(0.0) == pytest.approx(0.5, rel=1e-10)


def test_cumulativenormal_bounds():
    """Test CDF approaches 0 and 1 at extremes."""
    cdf = ql.CumulativeNormalDistribution()
    assert cdf(-10.0) == pytest.approx(0.0, abs=1e-10)
    assert cdf(10.0) == pytest.approx(1.0, abs=1e-10)


def test_cumulativenormal_known_values():
    """Test CDF at well-known quantiles."""
    cdf = ql.CumulativeNormalDistribution()
    # P(X <= 1) ~ 0.8413
    assert cdf(1.0) == pytest.approx(0.8413447, rel=1e-5)
    # P(X <= -1) ~ 0.1587
    assert cdf(-1.0) == pytest.approx(0.1586553, rel=1e-5)
    # P(X <= 1.96) ~ 0.975
    assert cdf(1.96) == pytest.approx(0.975, rel=1e-3)


def test_cumulativenormal_derivative():
    """Test CDF derivative equals PDF."""
    cdf = ql.CumulativeNormalDistribution()
    pdf = ql.NormalDistribution()
    for x in [-2.0, -1.0, 0.0, 1.0, 2.0]:
        assert cdf.derivative(x) == pytest.approx(pdf(x), rel=1e-10)


# =============================================================================
# InverseCumulativeNormal
# =============================================================================


def test_inversecumulativenormal_at_half():
    """Test inverse CDF at 0.5 for standard normal."""
    inv = ql.InverseCumulativeNormal()
    assert inv(0.5) == pytest.approx(0.0, abs=1e-10)


def test_inversecumulativenormal_roundtrip():
    """Test CDF(InvCDF(p)) == p."""
    cdf = ql.CumulativeNormalDistribution()
    inv = ql.InverseCumulativeNormal()
    for p in [0.01, 0.1, 0.25, 0.5, 0.75, 0.9, 0.99]:
        assert cdf(inv(p)) == pytest.approx(p, rel=1e-8)


def test_inversecumulativenormal_standard_value():
    """Test the static standard_value method."""
    assert ql.InverseCumulativeNormal.standard_value(0.5) == pytest.approx(0.0, abs=1e-10)
    assert ql.InverseCumulativeNormal.standard_value(0.975) == pytest.approx(1.96, rel=1e-3)


def test_inversecumulativenormal_custom_params():
    """Test inverse CDF with custom average and sigma."""
    inv = ql.InverseCumulativeNormal(average=5.0, sigma=2.0)
    # At p=0.5, should return the average
    assert inv(0.5) == pytest.approx(5.0, abs=1e-10)


# =============================================================================
# BivariateCumulativeNormalDistribution
# =============================================================================


def test_bivariate_independent():
    """Test bivariate CDF with zero correlation (independent)."""
    bvn = ql.BivariateCumulativeNormalDistribution(0.0)
    cdf = ql.CumulativeNormalDistribution()
    # For rho=0: P(X<=x, Y<=y) = P(X<=x) * P(Y<=y)
    for x, y in [(0.0, 0.0), (1.0, 1.0), (-1.0, 0.5)]:
        assert bvn(x, y) == pytest.approx(cdf(x) * cdf(y), rel=1e-6)


def test_bivariate_perfect_positive_correlation():
    """Test bivariate CDF with rho=0.9999 (near-perfect positive)."""
    bvn = ql.BivariateCumulativeNormalDistribution(0.9999)
    cdf = ql.CumulativeNormalDistribution()
    # For rho~1: P(X<=x, Y<=y) ~ min(P(X<=x), P(Y<=y))
    assert bvn(0.0, 0.0) == pytest.approx(cdf(0.0), rel=1e-2)


def test_bivariate_symmetry():
    """Test that bivariate CDF is symmetric in arguments for symmetric rho."""
    bvn = ql.BivariateCumulativeNormalDistribution(0.5)
    assert bvn(1.0, 2.0) == pytest.approx(bvn(2.0, 1.0), rel=1e-10)
