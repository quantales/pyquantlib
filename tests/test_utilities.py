"""
Tests for utilities module.

Corresponds to src/utilities/*.cpp bindings.
"""

import pytest

import pyquantlib as ql


# =============================================================================
# Rounding.Type Enum
# =============================================================================


def test_rounding_type_enum_values():
    """Test Rounding.Type enum values exist."""
    assert ql.Rounding.Type.None_ is not None
    assert ql.Rounding.Type.Up is not None
    assert ql.Rounding.Type.Down is not None
    assert ql.Rounding.Type.Closest is not None
    assert ql.Rounding.Type.Floor is not None
    assert ql.Rounding.Type.Ceiling is not None


# =============================================================================
# Rounding
# =============================================================================


def test_rounding_constructor_defaults():
    """Test Rounding construction with default parameters."""
    r = ql.Rounding(2)
    assert r.precision == 2
    assert r.type == ql.Rounding.Type.Closest
    assert r.roundingDigit == 5


def test_rounding_constructor_full():
    """Test Rounding construction with all parameters."""
    r = ql.Rounding(3, ql.Rounding.Type.Up, 3)
    assert r.precision == 3
    assert r.type == ql.Rounding.Type.Up
    assert r.roundingDigit == 3


def test_rounding_call():
    """Test Rounding call operator."""
    r = ql.Rounding(2)
    assert r(1.234) == pytest.approx(1.23)
    assert r(1.235) == pytest.approx(1.24)
    assert r(1.236) == pytest.approx(1.24)


# =============================================================================
# Concrete Roundings
# =============================================================================


def test_uprounding():
    """Test UpRounding always rounds up."""
    r = ql.UpRounding(2)
    assert r(1.231) == pytest.approx(1.24)
    assert r(1.239) == pytest.approx(1.24)


def test_downrounding():
    """Test DownRounding always rounds down."""
    r = ql.DownRounding(2)
    assert r(1.231) == pytest.approx(1.23)
    assert r(1.239) == pytest.approx(1.23)


def test_closestrounding():
    """Test ClosestRounding rounds to nearest."""
    r = ql.ClosestRounding(2)
    assert r(1.234) == pytest.approx(1.23)
    assert r(1.236) == pytest.approx(1.24)


def test_ceilingtruncation():
    """Test CeilingTruncation truncates toward positive infinity."""
    r = ql.CeilingTruncation(2)
    assert r(1.231) == pytest.approx(1.23)
    assert r(-1.231) == pytest.approx(-1.23)


def test_floortruncation():
    """Test FloorTruncation truncates toward negative infinity."""
    r = ql.FloorTruncation(2)
    assert r(1.239) == pytest.approx(1.24)
    assert r(-1.239) == pytest.approx(-1.23)
