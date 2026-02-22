"""
Tests for experimental volatility module.

Corresponds to src/experimental/volatility/*.cpp bindings.
"""

import math

import pytest

import pyquantlib as ql


# --- SmileSection base class ---


def test_smilesection_base_exists():
    """Test SmileSection base class exists."""
    assert hasattr(ql.base, "SmileSection")


# --- SviSmileSection ---


def test_svismilesection_construction_time():
    """Test SviSmileSection construction with time to expiry."""
    tte = 11.0 / 365
    forward = 123.45
    # SVI parameters: [a, b, sigma, rho, m]
    svi_params = [-0.0666, 0.229, 0.337, 0.439, 0.193]

    smile = ql.SviSmileSection(tte, forward, svi_params)

    assert smile is not None
    assert smile.atmLevel() == pytest.approx(forward)
    assert smile.exerciseTime() == pytest.approx(tte)


def test_svismilesection_construction_date():
    """Test SviSmileSection construction with expiry date."""
    today = ql.Date(15, ql.January, 2026)
    ql.Settings.evaluationDate = today

    expiry = today + ql.Period(11, ql.Days)
    forward = 123.45
    svi_params = [-0.0666, 0.229, 0.337, 0.439, 0.193]

    smile = ql.SviSmileSection(expiry, forward, svi_params)

    assert smile is not None
    assert smile.atmLevel() == pytest.approx(forward)
    assert smile.exerciseDate() == expiry


def test_svismilesection_variance():
    """Test SviSmileSection variance calculation.

    At strike = forward * exp(m), the log-moneyness k = m, so:
    w(m) = a + b * (rho * 0 + sqrt(0 + sigma^2))
         = a + b * sigma
    """
    tte = 11.0 / 365
    forward = 123.45
    a, b, sigma, rho, m = -0.0666, 0.229, 0.337, 0.439, 0.193
    svi_params = [a, b, sigma, rho, m]

    smile = ql.SviSmileSection(tte, forward, svi_params)

    # Strike at k = m
    strike = forward * math.exp(m)
    expected_variance = a + b * sigma

    assert smile.variance(strike) == pytest.approx(expected_variance, rel=1e-10)


def test_svismilesection_volatility():
    """Test SviSmileSection volatility calculation."""
    tte = 1.0  # 1 year for easier math
    forward = 100.0
    a, b, sigma, rho, m = 0.04, 0.1, 0.3, -0.4, 0.0
    svi_params = [a, b, sigma, rho, m]

    smile = ql.SviSmileSection(tte, forward, svi_params)

    # ATM volatility (k = 0 since m = 0)
    # w(0) = a + b * sigma = 0.04 + 0.1 * 0.3 = 0.07
    # vol = sqrt(w / T) = sqrt(0.07)
    expected_atm_var = a + b * sigma
    expected_atm_vol = math.sqrt(expected_atm_var / tte)

    atm_vol = smile.volatility(forward)
    assert atm_vol == pytest.approx(expected_atm_vol, rel=1e-6)


def test_svismilesection_min_max_strike():
    """Test SviSmileSection strike bounds."""
    smile = ql.SviSmileSection(1.0, 100.0, [0.04, 0.1, 0.3, -0.4, 0.0])

    assert smile.minStrike() == 0.0
    assert smile.maxStrike() > 1e10  # QL_MAX_REAL


def test_svismilesection_inheritance():
    """Test SviSmileSection inherits from SmileSection."""
    smile = ql.SviSmileSection(1.0, 100.0, [0.04, 0.1, 0.3, -0.4, 0.0])

    assert isinstance(smile, ql.base.SmileSection)
    assert isinstance(smile, ql.Observable)


def test_svismilesection_option_price():
    """Test SviSmileSection option pricing."""
    tte = 0.5
    forward = 100.0
    svi_params = [0.04, 0.1, 0.3, -0.4, 0.0]

    smile = ql.SviSmileSection(tte, forward, svi_params)

    # Price ATM call
    call_price = smile.optionPrice(forward, ql.OptionType.Call, 1.0)
    put_price = smile.optionPrice(forward, ql.OptionType.Put, 1.0)

    # ATM call and put should be equal (put-call parity with F=K)
    assert call_price == pytest.approx(put_price, rel=1e-6)
    assert call_price == pytest.approx(10.524315781125253, rel=1e-6)


def test_svismilesection_vega():
    """Test SviSmileSection vega calculation."""
    smile = ql.SviSmileSection(1.0, 100.0, [0.04, 0.1, 0.3, -0.4, 0.0])

    vega = smile.vega(100.0)
    assert vega == pytest.approx(0.3954668, rel=1e-6)


def test_svismilesection_density():
    """Test SviSmileSection density calculation."""
    smile = ql.SviSmileSection(1.0, 100.0, [0.04, 0.1, 0.3, -0.4, 0.0])

    density = smile.density(100.0)
    assert density == pytest.approx(0.01735287, rel=1e-6)


# --- Helper functions ---


def test_svi_total_variance():
    """Test sviTotalVariance helper function."""
    a, b, sigma, rho, m = 0.04, 0.1, 0.3, -0.4, 0.0
    k = 0.1  # log-moneyness

    variance = ql.sviTotalVariance(a, b, sigma, rho, m, k)

    expected = a + b * (rho * (k - m) + math.sqrt((k - m) ** 2 + sigma**2))

    assert variance == pytest.approx(expected, rel=1e-10)


def test_svi_total_variance_at_m():
    """Test sviTotalVariance at k = m simplifies to a + b * sigma."""
    a, b, sigma, rho, m = -0.0666, 0.229, 0.337, 0.439, 0.193

    variance = ql.sviTotalVariance(a, b, sigma, rho, m, m)

    assert variance == pytest.approx(a + b * sigma, rel=1e-10)


def test_check_svi_parameters_valid():
    """Test checkSviParameters with valid parameters."""
    # Valid parameters
    a, b, sigma, rho, m = 0.04, 0.1, 0.3, -0.4, 0.0
    tte = 1.0

    # Should not raise
    ql.checkSviParameters(a, b, sigma, rho, m, tte)


def test_check_svi_parameters_negative_b():
    """Test checkSviParameters rejects negative b."""
    with pytest.raises(ql.Error, match="b .* must be non negative"):
        ql.checkSviParameters(0.04, -0.1, 0.3, -0.4, 0.0, 1.0)


def test_check_svi_parameters_invalid_rho():
    """Test checkSviParameters rejects |rho| >= 1."""
    with pytest.raises(ql.Error, match="rho .* must be in"):
        ql.checkSviParameters(0.04, 0.1, 0.3, 1.0, 0.0, 1.0)


def test_check_svi_parameters_negative_sigma():
    """Test checkSviParameters rejects sigma <= 0."""
    with pytest.raises(ql.Error, match="sigma .* must be positive"):
        ql.checkSviParameters(0.04, 0.1, 0.0, -0.4, 0.0, 1.0)


def test_check_svi_parameters_butterfly_arbitrage():
    """Test checkSviParameters rejects butterfly arbitrage."""
    # b * (1 + |rho|) must be <= 4
    with pytest.raises(ql.Error, match="must be less than or equal to 4"):
        ql.checkSviParameters(0.04, 3.0, 0.3, 0.9, 0.0, 1.0)
