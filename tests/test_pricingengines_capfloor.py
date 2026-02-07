"""
Tests for cap/floor pricing engines.

Corresponds to src/pricingengines/capfloor/*.cpp bindings.
"""

import pytest

import pyquantlib as ql


@pytest.fixture(scope="module")
def capfloor_setup():
    """Setup for cap/floor engine tests."""
    today = ql.Date(15, ql.January, 2025)
    ql.Settings.evaluationDate = today

    dc = ql.Actual365Fixed()
    curve = ql.FlatForward(today, 0.04, dc)
    euribor = ql.Euribor6M(curve)

    schedule = ql.Schedule(
        ql.Date(17, ql.January, 2025),
        ql.Date(17, ql.January, 2030),
        ql.Period(6, ql.Months),
        ql.TARGET(),
        ql.ModifiedFollowing,
        ql.ModifiedFollowing,
        ql.DateGeneration.Forward,
        False,
    )

    leg = ql.IborLeg(schedule, euribor).withNotionals([1_000_000.0]).build()
    cap = ql.Cap(leg, [0.05])

    return {
        "today": today,
        "curve": curve,
        "cap": cap,
        "leg": leg,
    }


# =============================================================================
# BlackCapFloorEngine
# =============================================================================


def test_blackcapfloorengine_scalar_vol(capfloor_setup):
    """Test BlackCapFloorEngine with scalar volatility."""
    engine = ql.BlackCapFloorEngine(capfloor_setup["curve"], 0.20)
    cap = ql.Cap(capfloor_setup["leg"], [0.05])
    cap.setPricingEngine(engine)
    assert cap.NPV() == pytest.approx(7405.716086124158, rel=1e-6)


def test_blackcapfloorengine_hidden_handle(capfloor_setup):
    """Test BlackCapFloorEngine with hidden handle constructor."""
    engine = ql.BlackCapFloorEngine(capfloor_setup["curve"], 0.20)
    assert engine is not None


def test_blackcapfloorengine_quote_vol(capfloor_setup):
    """Test BlackCapFloorEngine with Quote volatility."""
    vol_quote = ql.SimpleQuote(0.20)
    engine = ql.BlackCapFloorEngine(
        ql.YieldTermStructureHandle(capfloor_setup["curve"]),
        ql.QuoteHandle(vol_quote),
    )
    cap = ql.Cap(capfloor_setup["leg"], [0.05])
    cap.setPricingEngine(engine)
    assert cap.NPV() == pytest.approx(7405.716086124158, rel=1e-6)


def test_blackcapfloorengine_displacement(capfloor_setup):
    """Test BlackCapFloorEngine with displacement."""
    engine = ql.BlackCapFloorEngine(capfloor_setup["curve"], 0.20, displacement=0.01)
    cap = ql.Cap(capfloor_setup["leg"], [0.05])
    cap.setPricingEngine(engine)
    # Displaced diffusion gives different NPV
    assert cap.NPV() > 0


# =============================================================================
# BachelierCapFloorEngine
# =============================================================================


def test_bacheliercapfloorengine_scalar_vol(capfloor_setup):
    """Test BachelierCapFloorEngine with scalar volatility."""
    engine = ql.BachelierCapFloorEngine(capfloor_setup["curve"], 0.005)
    cap = ql.Cap(capfloor_setup["leg"], [0.05])
    cap.setPricingEngine(engine)
    assert cap.NPV() == pytest.approx(1606.1185633197292, rel=1e-6)


def test_bacheliercapfloorengine_hidden_handle(capfloor_setup):
    """Test BachelierCapFloorEngine with hidden handle constructor."""
    engine = ql.BachelierCapFloorEngine(capfloor_setup["curve"], 0.005)
    assert engine is not None


def test_bacheliercapfloorengine_quote_vol(capfloor_setup):
    """Test BachelierCapFloorEngine with Quote volatility."""
    vol_quote = ql.SimpleQuote(0.005)
    engine = ql.BachelierCapFloorEngine(
        ql.YieldTermStructureHandle(capfloor_setup["curve"]),
        ql.QuoteHandle(vol_quote),
    )
    cap = ql.Cap(capfloor_setup["leg"], [0.05])
    cap.setPricingEngine(engine)
    assert cap.NPV() == pytest.approx(1606.1185633197292, rel=1e-6)
