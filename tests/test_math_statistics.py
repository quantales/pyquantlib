"""
Tests for statistics classes.

Corresponds to src/math/statistics/*.cpp bindings.
"""

import pytest
import pyquantlib as ql


# =============================================================================
# Statistics (= RiskStatistics)
# =============================================================================


def test_statistics_construction():
    """Test Statistics default construction."""
    stats = ql.Statistics()
    assert stats.samples() == 0


def test_statistics_basic():
    """Test basic statistical measures on [1, 2, 3, 4, 5]."""
    stats = ql.Statistics()
    for x in [1.0, 2.0, 3.0, 4.0, 5.0]:
        stats.add(x)

    assert stats.samples() == 5
    assert stats.mean() == pytest.approx(3.0)
    assert stats.variance() == pytest.approx(2.5)
    assert stats.standardDeviation() == pytest.approx(1.5811388300841898)
    assert stats.errorEstimate() == pytest.approx(0.7071067811865476)
    assert stats.skewness() == pytest.approx(0.0, abs=1e-14)
    assert stats.kurtosis() == pytest.approx(-1.2, rel=1e-10)
    assert stats.min() == pytest.approx(1.0)
    assert stats.max() == pytest.approx(5.0)


def test_statistics_weighted():
    """Test Statistics with weighted observations."""
    stats = ql.Statistics()
    stats.add(1.0, 2.0)
    stats.add(3.0, 1.0)

    assert stats.samples() == 2
    assert stats.weightSum() == pytest.approx(3.0)
    # weighted mean = (1*2 + 3*1) / 3 = 5/3
    assert stats.mean() == pytest.approx(5.0 / 3.0)


def test_statistics_percentile():
    """Test empirical percentile."""
    stats = ql.Statistics()
    for x in [1.0, 2.0, 3.0, 4.0, 5.0]:
        stats.add(x)

    assert stats.percentile(0.5) == pytest.approx(3.0)


def test_statistics_gaussian_measures():
    """Test Gaussian-assumption risk measures."""
    stats = ql.Statistics()
    for x in [-2.0, -1.0, 0.0, 1.0, 3.0, 5.0]:
        stats.add(x)

    assert stats.gaussianPercentile(0.95) == pytest.approx(5.289253483671162)
    assert stats.gaussianValueAtRisk(0.95) == pytest.approx(3.289253483671162)


def test_statistics_risk_measures():
    """Test empirical risk measures on data with negatives."""
    stats = ql.Statistics()
    for x in [-2.0, -1.0, 0.0, 1.0, 3.0, 5.0]:
        stats.add(x)

    assert stats.downsideVariance() == pytest.approx(5.0)
    assert stats.downsideDeviation() == pytest.approx(2.23606797749979)
    assert stats.semiVariance() == pytest.approx(7.0)
    assert stats.semiDeviation() == pytest.approx(2.6457513110645907)
    assert stats.valueAtRisk(0.95) == pytest.approx(2.0)
    assert stats.shortfall(1.0) == pytest.approx(0.5)
    assert stats.averageShortfall(1.0) == pytest.approx(2.0)


def test_statistics_add_sequence():
    """Test addSequence method."""
    stats = ql.Statistics()
    stats.addSequence([10.0, 20.0, 30.0])

    assert stats.samples() == 3
    assert stats.mean() == pytest.approx(20.0)


def test_statistics_add_sequence_weighted():
    """Test addSequence with weights."""
    stats = ql.Statistics()
    stats.addSequence([10.0, 20.0, 30.0], [1.0, 2.0, 3.0])

    assert stats.samples() == 3
    assert stats.weightSum() == pytest.approx(6.0)


def test_statistics_reset():
    """Test reset clears all data."""
    stats = ql.Statistics()
    stats.addSequence([1.0, 2.0, 3.0])
    assert stats.samples() == 3

    stats.reset()
    assert stats.samples() == 0


def test_statistics_sort():
    """Test sort doesn't raise."""
    stats = ql.Statistics()
    stats.addSequence([3.0, 1.0, 2.0])
    stats.sort()
    assert stats.percentile(0.5) == pytest.approx(2.0)


# =============================================================================
# IncrementalStatistics
# =============================================================================


def test_incrementalstatistics_construction():
    """Test IncrementalStatistics default construction."""
    stats = ql.IncrementalStatistics()
    assert stats.samples() == 0


def test_incrementalstatistics_basic():
    """Test basic measures on [1, 2, 3, 4, 5]."""
    stats = ql.IncrementalStatistics()
    for x in [1.0, 2.0, 3.0, 4.0, 5.0]:
        stats.add(x)

    assert stats.samples() == 5
    assert stats.mean() == pytest.approx(3.0)
    assert stats.variance() == pytest.approx(2.5)
    assert stats.standardDeviation() == pytest.approx(1.5811388300841898)
    assert stats.skewness() == pytest.approx(0.0, abs=1e-14)
    assert stats.kurtosis() == pytest.approx(-1.2, rel=1e-6)
    assert stats.min() == pytest.approx(1.0)
    assert stats.max() == pytest.approx(5.0)


def test_incrementalstatistics_downside():
    """Test downside measures with negative observations."""
    stats = ql.IncrementalStatistics()
    for x in [-2.0, -1.0, 0.0, 1.0, 3.0, 5.0]:
        stats.add(x)

    assert stats.downsideSamples() == 2
    assert stats.downsideVariance() == pytest.approx(5.0)
    assert stats.downsideDeviation() == pytest.approx(2.23606797749979)


def test_incrementalstatistics_add_sequence():
    """Test addSequence method."""
    stats = ql.IncrementalStatistics()
    stats.addSequence([10.0, 20.0, 30.0])

    assert stats.samples() == 3
    assert stats.mean() == pytest.approx(20.0)


def test_incrementalstatistics_add_sequence_weighted():
    """Test addSequence with weights."""
    stats = ql.IncrementalStatistics()
    stats.addSequence([10.0, 20.0, 30.0], [1.0, 2.0, 3.0])

    assert stats.samples() == 3
    assert stats.mean() == pytest.approx(23.333333333333332)


def test_incrementalstatistics_reset():
    """Test reset clears all data."""
    stats = ql.IncrementalStatistics()
    stats.addSequence([1.0, 2.0, 3.0])
    assert stats.samples() == 3

    stats.reset()
    assert stats.samples() == 0


# =============================================================================
# SequenceStatistics
# =============================================================================


def test_sequencestatistics_construction():
    """Test SequenceStatistics construction with dimension."""
    stats = ql.SequenceStatistics(3)
    assert stats.size() == 3
    assert stats.samples() == 0


def test_sequencestatistics_basic():
    """Test basic N-dimensional measures on 2D data."""
    stats = ql.SequenceStatistics(2)
    stats.add([1.0, 10.0])
    stats.add([2.0, 20.0])
    stats.add([3.0, 30.0])
    stats.add([4.0, 40.0])
    stats.add([5.0, 50.0])

    assert stats.size() == 2
    assert stats.samples() == 5

    mean = stats.mean()
    assert mean[0] == pytest.approx(3.0)
    assert mean[1] == pytest.approx(30.0)

    var = stats.variance()
    assert var[0] == pytest.approx(2.5)
    assert var[1] == pytest.approx(250.0)

    sd = stats.standardDeviation()
    assert sd[0] == pytest.approx(1.5811388300841898)
    assert sd[1] == pytest.approx(15.811388300841896)


def test_sequencestatistics_covariance():
    """Test covariance matrix (perfectly correlated data)."""
    stats = ql.SequenceStatistics(2)
    stats.add([1.0, 10.0])
    stats.add([2.0, 20.0])
    stats.add([3.0, 30.0])
    stats.add([4.0, 40.0])
    stats.add([5.0, 50.0])

    cov = stats.covariance()
    assert cov[0][0] == pytest.approx(2.5)
    assert cov[0][1] == pytest.approx(25.0)
    assert cov[1][0] == pytest.approx(25.0)
    assert cov[1][1] == pytest.approx(250.0)


def test_sequencestatistics_correlation():
    """Test correlation matrix (perfectly correlated data)."""
    stats = ql.SequenceStatistics(2)
    stats.add([1.0, 10.0])
    stats.add([2.0, 20.0])
    stats.add([3.0, 30.0])
    stats.add([4.0, 40.0])
    stats.add([5.0, 50.0])

    cor = stats.correlation()
    assert cor[0][0] == pytest.approx(1.0)
    assert cor[0][1] == pytest.approx(1.0)
    assert cor[1][0] == pytest.approx(1.0)
    assert cor[1][1] == pytest.approx(1.0)


def test_sequencestatistics_weighted():
    """Test add with weight."""
    stats = ql.SequenceStatistics(2)
    stats.add([1.0, 2.0], 3.0)
    stats.add([3.0, 4.0], 1.0)

    assert stats.samples() == 2
    assert stats.weightSum() == pytest.approx(4.0)


def test_sequencestatistics_reset():
    """Test reset clears data and optionally changes dimension."""
    stats = ql.SequenceStatistics(2)
    stats.add([1.0, 2.0])
    assert stats.samples() == 1

    stats.reset(3)
    assert stats.size() == 3
    assert stats.samples() == 0
