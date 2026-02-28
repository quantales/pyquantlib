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
    assert cap.NPV() == pytest.approx(11177.5902, rel=1e-4)


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


# =============================================================================
# AnalyticCapFloorEngine
# =============================================================================


@pytest.fixture(scope="module")
def hw_capfloor_env():
    """Setup for Hull-White cap/floor engine tests."""
    import datetime

    ql.Settings.evaluationDate = datetime.date(2024, 1, 15)
    rf = ql.FlatForward(datetime.date(2024, 1, 15), 0.05, ql.Actual365Fixed())
    ts_handle = ql.YieldTermStructureHandle(rf)
    hw = ql.HullWhite(ts_handle, 0.1, 0.01)
    index = ql.Euribor6M(ts_handle)
    cap = ql.MakeCapFloor(ql.CapFloorType.Cap, ql.Period("5Y"), index, strike=0.05)
    return {"rf": rf, "ts_handle": ts_handle, "hw": hw, "cap": cap}


def test_analyticcapfloorengine(hw_capfloor_env):
    """Test analytic cap/floor engine with Hull-White model."""
    env = hw_capfloor_env
    engine = ql.AnalyticCapFloorEngine(env["hw"], env["ts_handle"])
    cap = env["cap"]
    cap.setPricingEngine(engine)
    assert cap.NPV() == pytest.approx(0.0201463090, rel=1e-4)


def test_analyticcapfloorengine_hidden_handle(hw_capfloor_env):
    """Test analytic cap/floor engine with hidden handle constructor."""
    env = hw_capfloor_env
    engine = ql.AnalyticCapFloorEngine(env["hw"], env["rf"])
    cap = env["cap"]
    cap.setPricingEngine(engine)
    assert cap.NPV() == pytest.approx(0.0201463090, rel=1e-4)


# =============================================================================
# TreeCapFloorEngine
# =============================================================================


def test_treecapfloorengine(hw_capfloor_env):
    """Test tree cap/floor engine with Hull-White model."""
    env = hw_capfloor_env
    engine = ql.TreeCapFloorEngine(env["hw"], 100, env["ts_handle"])
    cap = env["cap"]
    cap.setPricingEngine(engine)
    assert cap.NPV() == pytest.approx(0.0200793549, rel=1e-3)


def test_treecapfloorengine_hidden_handle(hw_capfloor_env):
    """Test tree cap/floor engine with hidden handle constructor."""
    env = hw_capfloor_env
    engine = ql.TreeCapFloorEngine(env["hw"], 100, env["rf"])
    cap = env["cap"]
    cap.setPricingEngine(engine)
    assert cap.NPV() == pytest.approx(0.0200793549, rel=1e-3)
