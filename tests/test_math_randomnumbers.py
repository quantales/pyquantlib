"""
Tests for math/randomnumbers module.

Corresponds to src/math/randomnumbers/*.cpp bindings.
"""

import pytest

import pyquantlib as ql


# =============================================================================
# MersenneTwisterUniformRng
# =============================================================================


def test_mt_construction_default_seed():
    """Test MT construction with default seed."""
    rng = ql.MersenneTwisterUniformRng()
    s = rng.next()
    assert 0.0 < s.value < 1.0
    assert s.weight == 1.0


def test_mt_construction_with_seed():
    """Test MT construction with specific seed produces deterministic output."""
    rng = ql.MersenneTwisterUniformRng(42)
    s = rng.next()
    assert s.value == pytest.approx(0.37454011442605406, rel=1e-10)
    assert s.weight == 1.0


def test_mt_next_real():
    """Test MT nextReal returns value in (0, 1)."""
    rng = ql.MersenneTwisterUniformRng(42)
    rng.next()  # skip first
    r = rng.nextReal()
    assert r == pytest.approx(0.7965429843170568, rel=1e-10)


def test_mt_next_int32():
    """Test MT nextInt32 returns unsigned 32-bit integer."""
    rng = ql.MersenneTwisterUniformRng(42)
    rng.next()
    rng.nextReal()
    i = rng.nextInt32()
    assert i == 4083286876


def test_mt_construction_with_vector_seeds():
    """Test MT construction with vector of seeds."""
    rng = ql.MersenneTwisterUniformRng([1, 2, 3])
    s = rng.next()
    assert s.value == pytest.approx(0.6098612766945735, rel=1e-10)


def test_mt_reproducibility():
    """Test two RNGs with same seed produce identical sequences."""
    rng1 = ql.MersenneTwisterUniformRng(123)
    rng2 = ql.MersenneTwisterUniformRng(123)
    for _ in range(10):
        assert rng1.nextReal() == rng2.nextReal()


# =============================================================================
# SobolRsg
# =============================================================================


def test_sobol_direction_integers_enum():
    """Test DirectionIntegers enum values."""
    di = ql.SobolRsg.DirectionIntegers
    assert int(di.Unit) == 0
    assert int(di.Jaeckel) == 1
    assert int(di.SobolLevitan) == 2
    assert int(di.SobolLevitanLemieux) == 3
    assert int(di.JoeKuoD5) == 4
    assert int(di.JoeKuoD6) == 5
    assert int(di.JoeKuoD7) == 6
    assert int(di.Kuo) == 7
    assert int(di.Kuo2) == 8
    assert int(di.Kuo3) == 9


def test_sobol_construction():
    """Test Sobol sequence generator construction."""
    sobol = ql.SobolRsg(3, 0)
    assert sobol.dimension() == 3


def test_sobol_first_sequence():
    """Test Sobol first sequence values (known midpoint)."""
    sobol = ql.SobolRsg(3, 0)
    seq = sobol.nextSequence()
    assert seq.value == pytest.approx([0.5, 0.5, 0.5], rel=1e-10)
    assert seq.weight == 1.0


def test_sobol_second_sequence():
    """Test Sobol second sequence values."""
    sobol = ql.SobolRsg(3, 0)
    sobol.nextSequence()
    seq = sobol.nextSequence()
    assert seq.value == pytest.approx([0.75, 0.25, 0.75], rel=1e-10)


def test_sobol_third_sequence():
    """Test Sobol third sequence values."""
    sobol = ql.SobolRsg(3, 0)
    sobol.nextSequence()
    sobol.nextSequence()
    seq = sobol.nextSequence()
    assert seq.value == pytest.approx([0.25, 0.75, 0.25], rel=1e-10)


def test_sobol_last_sequence():
    """Test lastSequence returns copy of most recent sequence."""
    sobol = ql.SobolRsg(3, 0)
    seq1 = sobol.nextSequence()
    seq2 = sobol.lastSequence()
    assert seq1.value == seq2.value
    assert seq1.weight == seq2.weight


def test_sobol_skip_to():
    """Test skipTo jumps to correct position."""
    sobol = ql.SobolRsg(3, 0)
    sobol.skipTo(5)
    seq = sobol.nextSequence()
    assert seq.value == pytest.approx([0.625, 0.125, 0.375], rel=1e-10)


def test_sobol_uniformity():
    """Test Sobol sequence values stay in [0, 1]."""
    sobol = ql.SobolRsg(5, 0)
    for _ in range(100):
        seq = sobol.nextSequence()
        for v in seq.value:
            assert 0.0 <= v <= 1.0


# =============================================================================
# HaltonRsg
# =============================================================================


def test_halton_construction():
    """Test Halton sequence generator construction."""
    halton = ql.HaltonRsg(3)
    assert halton.dimension() == 3


def test_halton_first_sequence():
    """Test Halton first sequence values (deterministic, no random start)."""
    halton = ql.HaltonRsg(3, 0, False, False)
    seq = halton.nextSequence()
    assert seq.value[0] == pytest.approx(0.5, rel=1e-10)
    assert seq.value[1] == pytest.approx(1.0 / 3.0, rel=1e-10)
    assert seq.value[2] == pytest.approx(0.2, rel=1e-10)
    assert seq.weight == 1.0


def test_halton_second_sequence():
    """Test Halton second sequence values."""
    halton = ql.HaltonRsg(3, 0, False, False)
    halton.nextSequence()
    seq = halton.nextSequence()
    assert seq.value[0] == pytest.approx(0.25, rel=1e-10)
    assert seq.value[1] == pytest.approx(2.0 / 3.0, rel=1e-10)
    assert seq.value[2] == pytest.approx(0.4, rel=1e-10)


def test_halton_uniformity():
    """Test Halton sequence values stay in [0, 1]."""
    halton = ql.HaltonRsg(5, 0, True, False)
    for _ in range(100):
        seq = halton.nextSequence()
        for v in seq.value:
            assert 0.0 <= v <= 1.0


# =============================================================================
# Burley2020SobolRsg
# =============================================================================


def test_burley2020sobol_construction():
    """Test Burley2020 scrambled Sobol construction."""
    rsg = ql.Burley2020SobolRsg(3)
    assert rsg.dimension() == 3


def test_burley2020sobol_first_sequence():
    """Test Burley2020 Sobol first sequence values."""
    rsg = ql.Burley2020SobolRsg(3, 42, ql.SobolRsg.DirectionIntegers.Jaeckel, 43)
    seq = rsg.nextSequence()
    assert seq.value[0] == pytest.approx(0.9181515972595662, rel=1e-10)
    assert seq.value[1] == pytest.approx(0.32165447482839227, rel=1e-10)
    assert seq.value[2] == pytest.approx(0.31782629038207233, rel=1e-10)
    assert seq.weight == 1.0


def test_burley2020sobol_second_sequence():
    """Test Burley2020 Sobol second sequence values."""
    rsg = ql.Burley2020SobolRsg(3, 42, ql.SobolRsg.DirectionIntegers.Jaeckel, 43)
    rsg.nextSequence()
    seq = rsg.nextSequence()
    assert seq.value[0] == pytest.approx(0.3266997954342514, rel=1e-10)
    assert seq.value[1] == pytest.approx(0.9593072687275708, rel=1e-10)
    assert seq.value[2] == pytest.approx(0.4291225718334317, rel=1e-10)


def test_burley2020sobol_skip_to():
    """Test Burley2020 Sobol skipTo."""
    rsg = ql.Burley2020SobolRsg(3)
    rsg.skipTo(10)
    seq = rsg.nextSequence()
    assert len(seq.value) == 3
    assert seq.weight == 1.0


def test_burley2020sobol_differs_from_sobol():
    """Test scrambled Sobol produces different values than regular Sobol."""
    sobol = ql.SobolRsg(3, 0)
    burley = ql.Burley2020SobolRsg(3, 42, ql.SobolRsg.DirectionIntegers.Jaeckel, 43)
    s1 = sobol.nextSequence()
    b1 = burley.nextSequence()
    assert s1.value != pytest.approx(b1.value, abs=1e-6)


# =============================================================================
# BoxMullerGaussianRng
# =============================================================================


def test_boxmuller_construction_with_seed():
    """Test BoxMuller construction with seed."""
    rng = ql.BoxMullerGaussianRng(42)
    s = rng.next()
    assert s.value == pytest.approx(-0.5169641644548718, rel=1e-10)
    assert s.weight == 1.0


def test_boxmuller_construction_with_rng():
    """Test BoxMuller construction from MT RNG object."""
    mt = ql.MersenneTwisterUniformRng(42)
    rng = ql.BoxMullerGaussianRng(mt)
    s = rng.next()
    assert s.value == pytest.approx(-0.5169641644548718, rel=1e-10)


def test_boxmuller_produces_pairs():
    """Test BoxMuller produces Gaussian pairs."""
    rng = ql.BoxMullerGaussianRng(42)
    s1 = rng.next()
    s2 = rng.next()
    assert s1.value == pytest.approx(-0.5169641644548718, rel=1e-10)
    assert s2.value == pytest.approx(1.2219212173764127, rel=1e-10)


def test_boxmuller_gaussian_properties():
    """Test BoxMuller output has roughly Gaussian mean and variance."""
    rng = ql.BoxMullerGaussianRng(42)
    values = [rng.next().value for _ in range(10000)]
    mean = sum(values) / len(values)
    var = sum((v - mean) ** 2 for v in values) / len(values)
    assert mean == pytest.approx(0.0, abs=0.05)
    assert var == pytest.approx(1.0, abs=0.1)


# =============================================================================
# GaussianRandomGenerator (InverseCumulativeRng)
# =============================================================================


def test_gaussian_rng_construction_with_seed():
    """Test GaussianRandomGenerator construction with seed."""
    rng = ql.GaussianRandomGenerator(42)
    s = rng.next()
    assert s.value == pytest.approx(-0.31985239197154675, rel=1e-10)
    assert s.weight == 1.0


def test_gaussian_rng_construction_with_rng():
    """Test GaussianRandomGenerator construction from MT RNG object."""
    mt = ql.MersenneTwisterUniformRng(42)
    rng = ql.GaussianRandomGenerator(mt)
    s = rng.next()
    assert s.value == pytest.approx(-0.31985239197154675, rel=1e-10)


def test_gaussian_rng_gaussian_properties():
    """Test inverse cumulative RNG output has roughly Gaussian distribution."""
    rng = ql.GaussianRandomGenerator(99)
    values = [rng.next().value for _ in range(10000)]
    mean = sum(values) / len(values)
    var = sum((v - mean) ** 2 for v in values) / len(values)
    assert mean == pytest.approx(0.0, abs=0.05)
    assert var == pytest.approx(1.0, abs=0.1)


# =============================================================================
# UniformRandomSequenceGenerator (RandomSequenceGenerator)
# =============================================================================


def test_uniform_rsg_construction_with_seed():
    """Test UniformRandomSequenceGenerator construction with seed."""
    rsg = ql.UniformRandomSequenceGenerator(3, 42)
    assert rsg.dimension() == 3


def test_uniform_rsg_first_sequence():
    """Test UniformRSG first sequence values."""
    rsg = ql.UniformRandomSequenceGenerator(3, 42)
    seq = rsg.nextSequence()
    assert seq.value == pytest.approx(
        [0.37454011442605406, 0.7965429843170568, 0.9507143116788939],
        rel=1e-10)
    assert seq.weight == 1.0


def test_uniform_rsg_last_sequence():
    """Test UniformRSG lastSequence returns most recent."""
    rsg = ql.UniformRandomSequenceGenerator(3, 42)
    seq = rsg.nextSequence()
    last = rsg.lastSequence()
    assert seq.value == last.value


def test_uniform_rsg_construction_with_rng():
    """Test UniformRSG construction from MT RNG object."""
    mt = ql.MersenneTwisterUniformRng(42)
    rsg = ql.UniformRandomSequenceGenerator(3, mt)
    seq = rsg.nextSequence()
    assert seq.value == pytest.approx(
        [0.37454011442605406, 0.7965429843170568, 0.9507143116788939],
        rel=1e-10)


def test_uniform_rsg_next_int32_sequence():
    """Test UniformRSG nextInt32Sequence returns integer values."""
    rsg = ql.UniformRandomSequenceGenerator(3, 42)
    ints = rsg.nextInt32Sequence()
    assert len(ints) == 3
    for v in ints:
        assert isinstance(v, int)
        assert 0 <= v <= 2**32 - 1


# =============================================================================
# GaussianRandomSequenceGenerator (InverseCumulativeRsg with MT)
# =============================================================================


def test_gaussian_rsg_construction_with_seed():
    """Test GaussianRandomSequenceGenerator construction with seed."""
    rsg = ql.GaussianRandomSequenceGenerator(3, 42)
    assert rsg.dimension() == 3


def test_gaussian_rsg_first_sequence():
    """Test GaussianRSG first sequence values."""
    rsg = ql.GaussianRandomSequenceGenerator(3, 42)
    seq = rsg.nextSequence()
    assert seq.value == pytest.approx(
        [-0.31985239197154675, 0.8293364834726858, 1.6518193787298954],
        rel=1e-10)
    assert seq.weight == 1.0


def test_gaussian_rsg_last_sequence():
    """Test GaussianRSG lastSequence returns most recent."""
    rsg = ql.GaussianRandomSequenceGenerator(3, 42)
    seq = rsg.nextSequence()
    last = rsg.lastSequence()
    assert seq.value == pytest.approx(last.value, rel=1e-15)


def test_gaussian_rsg_construction_with_ursg():
    """Test GaussianRSG construction from UniformRSG object."""
    ursg = ql.UniformRandomSequenceGenerator(3, 42)
    grsg = ql.GaussianRandomSequenceGenerator(ursg)
    seq = grsg.nextSequence()
    assert seq.value == pytest.approx(
        [-0.31985239197154675, 0.8293364834726858, 1.6518193787298954],
        rel=1e-10)


# =============================================================================
# GaussianLowDiscrepancySequenceGenerator (InverseCumulativeRsg with Sobol)
# =============================================================================


def test_gaussian_ldsg_construction():
    """Test GaussianLowDiscrepancySequenceGenerator construction."""
    rsg = ql.GaussianLowDiscrepancySequenceGenerator(3, 0)
    assert rsg.dimension() == 3


def test_gaussian_ldsg_first_sequence():
    """Test GaussianLDSG first sequence (Sobol midpoint -> zero)."""
    rsg = ql.GaussianLowDiscrepancySequenceGenerator(3, 0)
    seq = rsg.nextSequence()
    # Sobol first point is (0.5, 0.5, 0.5), inverse normal of 0.5 = 0.0
    assert seq.value == pytest.approx([0.0, 0.0, 0.0], abs=1e-10)
    assert seq.weight == 1.0


def test_gaussian_ldsg_second_sequence():
    """Test GaussianLDSG second sequence values."""
    rsg = ql.GaussianLowDiscrepancySequenceGenerator(3, 0)
    rsg.nextSequence()
    seq = rsg.nextSequence()
    assert seq.value == pytest.approx(
        [0.6744897502234225, -0.6744897502234225, 0.6744897502234225],
        rel=1e-10)


def test_gaussian_ldsg_construction_with_sobol():
    """Test GaussianLDSG construction from SobolRsg object."""
    sobol = ql.SobolRsg(3, 0)
    rsg = ql.GaussianLowDiscrepancySequenceGenerator(sobol)
    seq = rsg.nextSequence()
    assert seq.value == pytest.approx([0.0, 0.0, 0.0], abs=1e-10)


def test_gaussian_ldsg_with_direction_integers():
    """Test GaussianLDSG with specific direction integers."""
    rsg = ql.GaussianLowDiscrepancySequenceGenerator(
        3, 0, ql.SobolRsg.DirectionIntegers.JoeKuoD7)
    seq = rsg.nextSequence()
    assert len(seq.value) == 3
    assert seq.weight == 1.0


# =============================================================================
# SobolBrownianBridgeRsg
# =============================================================================


def test_sobol_brownian_bridge_construction():
    """Test SobolBrownianBridgeRsg construction."""
    rsg = ql.SobolBrownianBridgeRsg(2, 3)
    assert rsg.dimension() == 6  # factors x steps


def test_sobol_brownian_bridge_first_sequence():
    """Test SobolBrownianBridgeRsg first sequence (all zeros for Sobol midpoint)."""
    rsg = ql.SobolBrownianBridgeRsg(2, 3)
    seq = rsg.nextSequence()
    assert seq.value == pytest.approx([0.0] * 6, abs=1e-10)
    assert seq.weight == 1.0


def test_sobol_brownian_bridge_with_ordering():
    """Test SobolBrownianBridgeRsg with different orderings."""
    for ordering in [ql.Ordering.Factors, ql.Ordering.Steps, ql.Ordering.Diagonal]:
        rsg = ql.SobolBrownianBridgeRsg(2, 3, ordering)
        seq = rsg.nextSequence()
        assert len(seq.value) == 6


def test_sobol_brownian_bridge_last_sequence():
    """Test SobolBrownianBridgeRsg lastSequence returns most recent."""
    rsg = ql.SobolBrownianBridgeRsg(2, 3)
    seq = rsg.nextSequence()
    last = rsg.lastSequence()
    assert seq.value == pytest.approx(last.value, abs=1e-15)


# =============================================================================
# Burley2020SobolBrownianBridgeRsg
# =============================================================================


def test_burley2020_brownian_bridge_construction():
    """Test Burley2020SobolBrownianBridgeRsg construction."""
    rsg = ql.Burley2020SobolBrownianBridgeRsg(2, 3)
    assert rsg.dimension() == 6  # factors x steps


def test_burley2020_brownian_bridge_first_sequence():
    """Test Burley2020SobolBrownianBridgeRsg first sequence values."""
    rsg = ql.Burley2020SobolBrownianBridgeRsg(2, 3)
    seq = rsg.nextSequence()
    assert seq.value[0] == pytest.approx(0.9398948176716029, rel=1e-10)
    assert seq.value[1] == pytest.approx(-0.451082668052647, rel=1e-10)
    assert seq.value[2] == pytest.approx(0.4577318335382752, rel=1e-10)
    assert seq.value[3] == pytest.approx(-0.06314067665477635, rel=1e-10)
    assert seq.value[4] == pytest.approx(1.0146790818631997, rel=1e-10)
    assert seq.value[5] == pytest.approx(-0.2878500932361654, rel=1e-10)
    assert seq.weight == 1.0


def test_burley2020_brownian_bridge_differs_from_sobol():
    """Test scrambled Brownian bridge produces different values than plain."""
    sbb = ql.SobolBrownianBridgeRsg(2, 3)
    bsbb = ql.Burley2020SobolBrownianBridgeRsg(2, 3)
    # Skip first (all zeros for plain Sobol)
    sbb.nextSequence()
    bsbb.nextSequence()
    s = sbb.nextSequence()
    b = bsbb.nextSequence()
    assert s.value != pytest.approx(b.value, abs=1e-6)


def test_burley2020_brownian_bridge_with_ordering():
    """Test Burley2020SobolBrownianBridgeRsg with different orderings."""
    for ordering in [ql.Ordering.Factors, ql.Ordering.Steps, ql.Ordering.Diagonal]:
        rsg = ql.Burley2020SobolBrownianBridgeRsg(2, 3, ordering)
        seq = rsg.nextSequence()
        assert len(seq.value) == 6


# =============================================================================
# Ordering enum
# =============================================================================


def test_ordering_enum_values():
    """Test Ordering enum values."""
    assert int(ql.Ordering.Factors) == 0
    assert int(ql.Ordering.Steps) == 1
    assert int(ql.Ordering.Diagonal) == 2


def test_ordering_enum_roundtrip():
    """Test Ordering enum can be passed and compared."""
    o = ql.Ordering.Diagonal
    assert o == ql.Ordering.Diagonal
    assert o != ql.Ordering.Factors
