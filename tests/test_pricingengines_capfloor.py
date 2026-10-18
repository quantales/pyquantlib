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


# =============================================================================
# Gaussian1dCapFloorEngine
# =============================================================================


@pytest.fixture(scope="module")
def g1d_capfloor_env():
    """Setup for Gaussian1D cap/floor engine tests."""
    import datetime

    ql.Settings.evaluationDate = datetime.date(2024, 1, 15)
    rf = ql.FlatForward(datetime.date(2024, 1, 15), 0.05, ql.Actual365Fixed())
    ts_handle = ql.YieldTermStructureHandle(rf)
    gsr = ql.Gsr(ts_handle, [], [0.01], 0.1)
    index = ql.Euribor6M(ts_handle)
    cap = ql.MakeCapFloor(ql.CapFloorType.Cap, ql.Period("5Y"), index, strike=0.05)
    return {"gsr": gsr, "cap": cap}


def test_gaussian1dcapfloorengine(g1d_capfloor_env):
    """Test Gaussian1dCapFloorEngine with GSR model."""
    env = g1d_capfloor_env
    engine = ql.Gaussian1dCapFloorEngine(env["gsr"])
    env["cap"].setPricingEngine(engine)
    assert env["cap"].NPV() == pytest.approx(0.020103807954722542, rel=1e-4)


# =============================================================================
# Cap/floor engines with an optionlet volatility structure
# =============================================================================

@pytest.fixture
def capfloor_today(capfloor_setup):
    """capfloor_setup with the evaluation date reset (other fixtures move it)."""
    ql.Settings.evaluationDate = capfloor_setup["today"]
    return capfloor_setup


# Flat 20% Black volatility NPV and 0.5% normal volatility NPV reused from the
# scalar-volatility tests above.
_BLACK_FLAT_20_NPV = 7405.716086124158
_BACHELIER_FLAT_50BP_NPV = 1606.1185633197292


def _flat_optionlet_vol(vol, vol_type=ql.VolatilityType.ShiftedLognormal):
    return ql.ConstantOptionletVolatility(
        0, ql.TARGET(), ql.Following, vol, ql.Actual365Fixed(), vol_type)


def test_blackcapfloorengine_optionlet_vol(capfloor_today):
    """BlackCapFloorEngine prices off an optionlet volatility structure."""
    engine = ql.BlackCapFloorEngine(capfloor_today["curve"], _flat_optionlet_vol(0.20))
    cap = ql.Cap(capfloor_today["leg"], [0.05])
    cap.setPricingEngine(engine)
    assert cap.NPV() == pytest.approx(_BLACK_FLAT_20_NPV, rel=1e-8)


def test_blackcapfloorengine_optionlet_vol_handle(capfloor_today):
    """BlackCapFloorEngine accepts explicit curve and volatility handles."""
    engine = ql.BlackCapFloorEngine(
        ql.YieldTermStructureHandle(capfloor_today["curve"]),
        ql.OptionletVolatilityStructureHandle(_flat_optionlet_vol(0.20)))
    cap = ql.Cap(capfloor_today["leg"], [0.05])
    cap.setPricingEngine(engine)
    assert cap.NPV() == pytest.approx(_BLACK_FLAT_20_NPV, rel=1e-8)


def test_bacheliercapfloorengine_optionlet_vol(capfloor_today):
    """BachelierCapFloorEngine prices off a normal optionlet volatility structure."""
    vol = _flat_optionlet_vol(0.005, ql.VolatilityType.Normal)
    engine = ql.BachelierCapFloorEngine(capfloor_today["curve"], vol)
    cap = ql.Cap(capfloor_today["leg"], [0.05])
    cap.setPricingEngine(engine)
    assert cap.NPV() == pytest.approx(_BACHELIER_FLAT_50BP_NPV, rel=1e-8)


def test_bacheliercapfloorengine_optionlet_vol_handle(capfloor_today):
    """BachelierCapFloorEngine accepts explicit curve and volatility handles."""
    vol = _flat_optionlet_vol(0.005, ql.VolatilityType.Normal)
    engine = ql.BachelierCapFloorEngine(
        ql.YieldTermStructureHandle(capfloor_today["curve"]),
        ql.OptionletVolatilityStructureHandle(vol))
    cap = ql.Cap(capfloor_today["leg"], [0.05])
    cap.setPricingEngine(engine)
    assert cap.NPV() == pytest.approx(_BACHELIER_FLAT_50BP_NPV, rel=1e-8)


def test_capfloorengine_spreaded_optionlet_vol(capfloor_today):
    """A 19% base volatility plus a 1% spread prices like a flat 20% volatility."""
    spread = ql.SimpleQuote(0.01)
    spreaded = ql.SpreadedOptionletVolatility(_flat_optionlet_vol(0.19), spread)
    engine = ql.BlackCapFloorEngine(capfloor_today["curve"], spreaded)
    cap = ql.Cap(capfloor_today["leg"], [0.05])
    cap.setPricingEngine(engine)
    assert cap.NPV() == pytest.approx(_BLACK_FLAT_20_NPV, rel=1e-8)
    # Bumping the spread to zero reprices at the 19% base volatility
    spread.setValue(0.0)
    flat19 = ql.Cap(capfloor_today["leg"], [0.05])
    flat19.setPricingEngine(ql.BlackCapFloorEngine(capfloor_today["curve"], 0.19))
    assert cap.NPV() == pytest.approx(flat19.NPV(), rel=1e-8)


def test_capfloorengine_capletvariancecurve(capfloor_today):
    """A caplet variance curve with a constant 20% volatility prices like a flat 20%."""
    today = capfloor_today["today"]
    dates = [today + ql.Period(y, ql.Years) for y in range(1, 6)]
    vol = ql.CapletVarianceCurve(today, dates, [0.20] * 5, ql.Actual365Fixed())
    engine = ql.BlackCapFloorEngine(capfloor_today["curve"], vol)
    cap = ql.Cap(capfloor_today["leg"], [0.05])
    cap.setPricingEngine(engine)
    assert cap.NPV() == pytest.approx(_BLACK_FLAT_20_NPV, rel=1e-6)
