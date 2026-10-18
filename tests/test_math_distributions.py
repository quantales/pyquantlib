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


# =============================================================================
# Gamma, Poisson, chi-square, Student t, binomial distributions
#
# Reference values below were obtained independently with scipy.special and
# scipy.stats.
# =============================================================================


def test_gammafunction_values():
    """GammaFunction matches the gamma function and its logarithm."""
    gamma = ql.GammaFunction()
    assert gamma.value(5.5) == pytest.approx(52.34277778455352, rel=1e-10)
    assert gamma.logValue(5.5) == pytest.approx(3.9578139676187165, rel=1e-10)
    assert gamma.value(5.0) == pytest.approx(24.0, rel=1e-10)


def test_cumulativegammadistribution_values():
    """CumulativeGammaDistribution is the regularized lower incomplete gamma function."""
    # QuantLib stops its series at a 3e-7 relative tolerance, hence rel=1e-6
    assert ql.CumulativeGammaDistribution(2.0)(1.5) == pytest.approx(
        0.4421745996289252, rel=1e-6)
    assert ql.CumulativeGammaDistribution(0.5)(0.7) == pytest.approx(
        0.7632764293621428, rel=1e-6)
    # a = 1 is the exponential distribution
    assert ql.CumulativeGammaDistribution(1.0)(2.0) == pytest.approx(
        1.0 - math.exp(-2.0), rel=1e-6)


def test_poissondistribution_values():
    """PoissonDistribution and its cumulative form match the Poisson law."""
    pmf = ql.PoissonDistribution(3.0)
    assert pmf(2) == pytest.approx(0.22404180765538775, rel=1e-10)
    assert pmf(0) == pytest.approx(math.exp(-3.0), rel=1e-12)
    cdf = ql.CumulativePoissonDistribution(3.0)
    assert cdf(4) == pytest.approx(0.8152632445237722, rel=1e-10)
    assert cdf(4) == pytest.approx(sum(pmf(k) for k in range(5)), rel=1e-10)


def test_inversecumulativepoisson_quantiles():
    """InverseCumulativePoisson returns the smallest k reaching the probability."""
    assert ql.InverseCumulativePoisson(3.0)(0.7) == 4.0
    assert ql.InverseCumulativePoisson(2.5)(0.99) == 7.0
    # The default mean is QuantLib's own (1.0)
    assert ql.InverseCumulativePoisson()(0.5) == 1.0


def test_cumulativechisquaredistribution_values():
    """CumulativeChiSquareDistribution matches the chi-square law."""
    # built on the gamma distribution, so accurate to about 1e-8
    assert ql.CumulativeChiSquareDistribution(4.0)(3.5) == pytest.approx(
        0.522121655511276, rel=1e-6)
    assert ql.CumulativeChiSquareDistribution(1.0)(1.2) == pytest.approx(
        0.7266783217077017, rel=1e-6)


def test_noncentralchisquare_values():
    """The non-central cumulative distribution matches the non-central chi-square law."""
    assert ql.NonCentralCumulativeChiSquareDistribution(3.0, 2.0)(5.0) == pytest.approx(
        0.5934051800831556, rel=1e-8)
    assert ql.NonCentralCumulativeChiSquareDistribution(5.0, 4.0)(12.0) == pytest.approx(
        0.7588990165427218, rel=1e-8)
    # a zero non-centrality parameter reduces to the central distribution
    assert ql.NonCentralCumulativeChiSquareDistribution(4.0, 0.0)(3.5) == pytest.approx(
        ql.CumulativeChiSquareDistribution(4.0)(3.5), rel=1e-6)


def test_noncentralchisquare_sankaran_approximation():
    """The Sankaran approximation stays close to the exact distribution."""
    exact = ql.NonCentralCumulativeChiSquareDistribution(5.0, 4.0)(12.0)
    approx = ql.NonCentralCumulativeChiSquareSankaranApprox(5.0, 4.0)(12.0)
    assert approx == pytest.approx(exact, abs=5e-3)


def test_inversenoncentralchisquare_quantiles():
    """The inverse non-central chi-square distribution returns the quantile."""
    inv = ql.InverseNonCentralCumulativeChiSquareDistribution(3.0, 2.0)
    assert inv(0.9) == pytest.approx(10.047198516640961, rel=1e-6)
    assert ql.InverseNonCentralCumulativeChiSquareDistribution(5.0, 4.0)(0.5) == pytest.approx(
        8.122166600325594, rel=1e-6)
    tight = ql.InverseNonCentralCumulativeChiSquareDistribution(3.0, 2.0, 100, 1e-12)
    assert tight(0.9) == pytest.approx(10.047198516640961, rel=1e-9)


def test_studentdistribution_density():
    """StudentDistribution matches the Student t density."""
    assert ql.StudentDistribution(5)(1.2) == pytest.approx(0.1776586134649355, rel=1e-10)
    assert ql.StudentDistribution(10)(0.0) == pytest.approx(0.38910838396603104, rel=1e-10)


def test_cumulativestudentdistribution_values():
    """CumulativeStudentDistribution matches the Student t law."""
    assert ql.CumulativeStudentDistribution(5)(1.2) == pytest.approx(
        0.8580544716469487, rel=1e-8)
    assert ql.CumulativeStudentDistribution(3)(-0.7) == pytest.approx(
        0.2671634991523818, rel=1e-8)
    assert ql.CumulativeStudentDistribution(4)(0.0) == pytest.approx(0.5, rel=1e-12)


def test_inversecumulativestudent_quantiles():
    """InverseCumulativeStudent returns Student t quantiles."""
    # QuantLib 1.43 inverts with a 1e-6 Newton accuracy; 1.44 uses Boost.Math
    assert ql.InverseCumulativeStudent(10)(0.975) == pytest.approx(
        2.2281388519862744, abs=1e-5)
    assert ql.InverseCumulativeStudent(3)(0.9) == pytest.approx(1.637744353696209, abs=1e-5)
    assert ql.InverseCumulativeStudent(3)(0.1) == pytest.approx(-1.6377443536962089, abs=1e-5)


def test_student_inverse_round_trips_cumulative():
    """The inverse and cumulative Student distributions are consistent."""
    cdf = ql.CumulativeStudentDistribution(6)
    inv = ql.InverseCumulativeStudent(6)
    for p in (0.05, 0.3, 0.5, 0.8, 0.99):
        assert cdf(inv(p)) == pytest.approx(p, abs=1e-5)


def test_student_rejects_invalid_degrees_of_freedom():
    """Non-positive degrees of freedom are rejected."""
    for cls in (ql.StudentDistribution, ql.CumulativeStudentDistribution,
                ql.InverseCumulativeStudent):
        with pytest.raises(ql.Error, match="invalid parameter"):
            cls(0)


def test_binomialdistribution_values():
    """BinomialDistribution and its cumulative form match the binomial law."""
    assert ql.BinomialDistribution(0.3, 10)(3) == pytest.approx(0.2668279319999998, rel=1e-10)
    assert ql.CumulativeBinomialDistribution(0.3, 10)(3) == pytest.approx(
        0.6496107184000001, rel=1e-10)
    assert ql.CumulativeBinomialDistribution(0.3, 10)(10) == pytest.approx(1.0, rel=1e-12)


def test_binomial_coefficients():
    """binomialCoefficient and its logarithm match the combinatorial value."""
    assert ql.binomialCoefficient(10, 3) == 120.0
    assert ql.binomialCoefficientLn(10, 3) == pytest.approx(4.787491742782046, rel=1e-10)
    assert ql.binomialCoefficientLn(50, 25) == pytest.approx(32.47055650581199, rel=1e-10)


def test_peizerpratt_method2_inversion():
    """The Peizer-Pratt inversion reproduces the normal quantile for odd n."""
    assert ql.PeizerPrattMethod2Inversion(0.0, 51) == pytest.approx(0.5, rel=1e-12)
    p = ql.PeizerPrattMethod2Inversion(1.0, 51)
    assert p == pytest.approx(0.5693335115559703, rel=1e-10)
    # defining property: 1 - CumulativeBinomial((n-1)/2, n, p) ~ Phi(z)
    assert 1.0 - ql.CumulativeBinomialDistribution(p, 51)(25) == pytest.approx(
        ql.CumulativeNormalDistribution()(1.0), abs=1e-4)
    with pytest.raises(ql.Error, match="odd"):
        ql.PeizerPrattMethod2Inversion(1.0, 50)


def test_bivariate_cumulative_student_is_not_independent_at_zero_correlation():
    """Zero correlation does not mean independence: the components share the chi-square factor."""
    joint = ql.BivariateCumulativeStudentDistribution(4, 0.0)
    marginal = ql.CumulativeStudentDistribution(4)
    # scipy.stats.multivariate_t(df=4).cdf([0.4, -1.1]); scipy integrates numerically
    assert joint(0.4, -1.1) == pytest.approx(0.10332943574595067, rel=1e-4)
    assert joint(0.4, -1.1) != pytest.approx(marginal(0.4) * marginal(-1.1), rel=1e-2)


def test_bivariate_cumulative_student_symmetry_and_marginals():
    """The joint law is symmetric and tends to the marginal as one argument grows."""
    joint = ql.BivariateCumulativeStudentDistribution(4, 0.5)
    marginal = ql.CumulativeStudentDistribution(4)
    assert joint(0.4, -1.1) == pytest.approx(joint(-1.1, 0.4), rel=1e-10)
    assert joint(1e3, -1.1) == pytest.approx(marginal(-1.1), rel=1e-6)
    assert joint(0.4, 1e3) == pytest.approx(marginal(0.4), rel=1e-6)


def test_bivariate_cumulative_student_values():
    """The joint cumulative probability matches scipy's multivariate t."""
    assert ql.BivariateCumulativeStudentDistribution(4, 0.5)(0.5, -0.3) == pytest.approx(
        0.32895299946237533, rel=1e-4)
    assert ql.BivariateCumulativeStudentDistribution(7, -0.3)(1.0, 0.8) == pytest.approx(
        0.6224191407889117, rel=1e-4)
