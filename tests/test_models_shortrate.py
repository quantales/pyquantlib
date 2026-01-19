"""Tests for ql/models/shortrate/*.hpp bindings."""

import pytest

import pyquantlib as ql


# --- Vasicek ---


def test_vasicek_construction():
    """Test Vasicek model construction with defaults."""
    model = ql.Vasicek()
    assert model is not None


def test_vasicek_construction_with_params():
    """Test Vasicek model construction with parameters."""
    model = ql.Vasicek(
        r0=0.05,
        a=0.3,
        b=0.03,
        sigma=0.01,
    )
    assert model is not None


def test_vasicek_parameter_accessors():
    """Test Vasicek parameter accessors."""
    r0 = 0.05
    a = 0.3
    b = 0.03
    sigma = 0.01

    model = ql.Vasicek(r0=r0, a=a, b=b, sigma=sigma)

    assert model.r0() == pytest.approx(r0)
    assert model.a() == pytest.approx(a)
    assert model.b() == pytest.approx(b)
    assert model.sigma() == pytest.approx(sigma)


def test_vasicek_params_method():
    """Test Vasicek params() returns calibratable parameters."""
    model = ql.Vasicek(r0=0.05, a=0.3, b=0.03, sigma=0.01)

    params = model.params()
    assert len(params) == 4
