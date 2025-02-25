import pytest
import pyquantlib as ql


class TestRoundingType:
    def test_enum_values(self):
        assert ql.Rounding.Type.None_ is not None
        assert ql.Rounding.Type.Up is not None
        assert ql.Rounding.Type.Down is not None
        assert ql.Rounding.Type.Closest is not None
        assert ql.Rounding.Type.Floor is not None
        assert ql.Rounding.Type.Ceiling is not None


class TestRounding:
    def test_constructor_defaults(self):
        r = ql.Rounding(2)
        assert r.precision == 2
        assert r.type == ql.Rounding.Type.Closest
        assert r.roundingDigit == 5

    def test_constructor_full(self):
        r = ql.Rounding(3, ql.Rounding.Type.Up, 3)
        assert r.precision == 3
        assert r.type == ql.Rounding.Type.Up
        assert r.roundingDigit == 3

    def test_call(self):
        r = ql.Rounding(2)
        assert r(1.234) == pytest.approx(1.23)
        assert r(1.235) == pytest.approx(1.24)
        assert r(1.236) == pytest.approx(1.24)


class TestConcreteRoundings:
    def test_up_rounding(self):
        r = ql.UpRounding(2)
        assert r(1.231) == pytest.approx(1.24)
        assert r(1.239) == pytest.approx(1.24)

    def test_down_rounding(self):
        r = ql.DownRounding(2)
        assert r(1.231) == pytest.approx(1.23)
        assert r(1.239) == pytest.approx(1.23)

    def test_closest_rounding(self):
        r = ql.ClosestRounding(2)
        assert r(1.234) == pytest.approx(1.23)
        assert r(1.236) == pytest.approx(1.24)

    def test_ceiling_truncation(self):
        r = ql.CeilingTruncation(2)
        assert r(1.231) == pytest.approx(1.23)
        assert r(-1.231) == pytest.approx(-1.23)

    def test_floor_truncation(self):
        r = ql.FloorTruncation(2)
        assert r(1.239) == pytest.approx(1.24)
        assert r(-1.239) == pytest.approx(-1.23)
