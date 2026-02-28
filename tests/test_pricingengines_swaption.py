"""
Tests for swaption pricing engines.

Corresponds to src/pricingengines/swaption/*.cpp bindings.
"""

import pytest

import pyquantlib as ql


@pytest.fixture(scope="module")
def swaption_env():
    """Environment for swaption pricing tests."""
    original_date = ql.Settings.instance().evaluationDate
    today = ql.Date(15, ql.January, 2026)
    ql.Settings.instance().evaluationDate = today

    # Term structure
    dc = ql.Actual365Fixed()
    curve = ql.FlatForward(today, 0.05, dc)

    # Index
    index = ql.Euribor6M(curve)

    # Create a vanilla swap
    fixed_schedule = ql.Schedule(
        today + ql.Period(1, ql.Years),
        today + ql.Period(6, ql.Years),
        ql.Period(1, ql.Years),
        ql.TARGET(),
        ql.ModifiedFollowing,
        ql.ModifiedFollowing,
        ql.DateGeneration.Forward,
        False,
    )
    float_schedule = ql.Schedule(
        today + ql.Period(1, ql.Years),
        today + ql.Period(6, ql.Years),
        ql.Period(6, ql.Months),
        ql.TARGET(),
        ql.ModifiedFollowing,
        ql.ModifiedFollowing,
        ql.DateGeneration.Forward,
        False,
    )
    swap = ql.VanillaSwap(
        ql.SwapType.Payer,
        1000000.0,
        fixed_schedule,
        0.05,
        ql.Thirty360(ql.Thirty360.BondBasis),
        float_schedule,
        index,
        0.0,
        ql.Actual360(),
    )

    # Create a European swaption
    exercise = ql.EuropeanExercise(today + ql.Period(1, ql.Years))
    swaption = ql.Swaption(swap, exercise)

    yield {
        "today": today,
        "curve": curve,
        "index": index,
        "swap": swap,
        "swaption": swaption,
    }

    ql.Settings.instance().evaluationDate = original_date


# --- TreeSwaptionEngine ---


def test_treeswaptionengine_construction_timesteps(swaption_env):
    """Test TreeSwaptionEngine construction with time steps."""
    env = swaption_env

    model = ql.HullWhite(env["curve"], a=0.1, sigma=0.01)
    engine = ql.TreeSwaptionEngine(model, timeSteps=50)
    assert engine is not None


def test_treeswaptionengine_construction_timegrid(swaption_env):
    """Test TreeSwaptionEngine construction with time grid."""
    env = swaption_env

    model = ql.HullWhite(env["curve"], a=0.1, sigma=0.01)
    times = [0.0, 0.5, 1.0, 2.0, 3.0, 4.0, 5.0]
    time_grid = ql.TimeGrid(times)
    engine = ql.TreeSwaptionEngine(model, timeGrid=time_grid)
    assert engine is not None


def test_treeswaptionengine_pricing(swaption_env):
    """Test TreeSwaptionEngine swaption pricing."""
    env = swaption_env

    model = ql.HullWhite(env["curve"], a=0.1, sigma=0.01)
    engine = ql.TreeSwaptionEngine(model, timeSteps=100)
    env["swaption"].setPricingEngine(engine)

    npv = env["swaption"].NPV()
    assert npv == pytest.approx(15996.569867907741, rel=1e-5)


# --- JamshidianSwaptionEngine ---


def test_jamshidianswaptionengine_construction(swaption_env):
    """Test JamshidianSwaptionEngine construction."""
    env = swaption_env

    model = ql.HullWhite(env["curve"], a=0.1, sigma=0.01)
    engine = ql.JamshidianSwaptionEngine(model)
    assert engine is not None


def test_jamshidianswaptionengine_pricing(swaption_env):
    """Test JamshidianSwaptionEngine swaption pricing."""
    env = swaption_env

    model = ql.HullWhite(env["curve"], a=0.1, sigma=0.01)
    engine = ql.JamshidianSwaptionEngine(model)
    env["swaption"].setPricingEngine(engine)

    npv = env["swaption"].NPV()
    assert npv == pytest.approx(15860.419233975226, rel=1e-5)


# --- G2SwaptionEngine ---


def test_g2swaptionengine_construction(swaption_env):
    """Test G2SwaptionEngine construction."""
    env = swaption_env

    model = ql.G2(env["curve"], a=0.1, sigma=0.01, b=0.1, eta=0.01, rho=-0.75)
    engine = ql.G2SwaptionEngine(model, range=6.0, intervals=200)
    assert engine is not None


def test_g2swaptionengine_pricing(swaption_env):
    """Test G2SwaptionEngine swaption pricing."""
    env = swaption_env

    model = ql.G2(env["curve"], a=0.1, sigma=0.01, b=0.1, eta=0.01, rho=-0.75)
    engine = ql.G2SwaptionEngine(model, range=6.0, intervals=200)
    env["swaption"].setPricingEngine(engine)

    npv = env["swaption"].NPV()
    assert npv == pytest.approx(12050.213410784432, rel=1e-5)


# --- FdHullWhiteSwaptionEngine ---


def test_fdhullwhiteswaptionengine_construction(swaption_env):
    """Test FdHullWhiteSwaptionEngine construction."""
    env = swaption_env

    model = ql.HullWhite(env["curve"], a=0.1, sigma=0.01)
    engine = ql.FdHullWhiteSwaptionEngine(model)
    assert engine is not None


def test_fdhullwhiteswaptionengine_with_params(swaption_env):
    """Test FdHullWhiteSwaptionEngine construction with parameters."""
    env = swaption_env

    model = ql.HullWhite(env["curve"], a=0.1, sigma=0.01)
    # NOTE: xGrid must be a multiple of 40 due to suspected QuantLib bug
    # (non-deterministic results with other grid sizes on MSVC Release builds)
    engine = ql.FdHullWhiteSwaptionEngine(
        model, tGrid=50, xGrid=80, dampingSteps=0
    )
    assert engine is not None


def test_fdhullwhiteswaptionengine_pricing(swaption_env):
    """Test FdHullWhiteSwaptionEngine swaption pricing."""
    env = swaption_env

    model = ql.HullWhite(env["curve"], a=0.1, sigma=0.01)
    # NOTE: xGrid must be a multiple of 40 due to suspected QuantLib bug
    # (non-deterministic results with other grid sizes on MSVC Release builds)
    engine = ql.FdHullWhiteSwaptionEngine(model, tGrid=100, xGrid=200)
    env["swaption"].setPricingEngine(engine)

    npv = env["swaption"].NPV()
    assert npv == pytest.approx(15860.169093245760, rel=1e-5)


# --- FdG2SwaptionEngine ---


def test_fdg2swaptionengine_construction(swaption_env):
    """Test FdG2SwaptionEngine construction."""
    env = swaption_env

    model = ql.G2(env["curve"], a=0.1, sigma=0.01, b=0.1, eta=0.01, rho=-0.75)
    engine = ql.FdG2SwaptionEngine(model)
    assert engine is not None


def test_fdg2swaptionengine_with_params(swaption_env):
    """Test FdG2SwaptionEngine construction with parameters."""
    env = swaption_env

    model = ql.G2(env["curve"], a=0.1, sigma=0.01, b=0.1, eta=0.01, rho=-0.75)
    engine = ql.FdG2SwaptionEngine(
        model, tGrid=50, xGrid=25, yGrid=25, dampingSteps=0
    )
    assert engine is not None


def test_fdg2swaptionengine_pricing(swaption_env):
    """Test FdG2SwaptionEngine swaption pricing."""
    env = swaption_env

    model = ql.G2(env["curve"], a=0.1, sigma=0.01, b=0.1, eta=0.01, rho=-0.75)
    engine = ql.FdG2SwaptionEngine(model)
    env["swaption"].setPricingEngine(engine)

    npv = env["swaption"].NPV()
    assert npv == pytest.approx(11913.177527894266, rel=1e-5)


# --- BlackSwaptionEngine ---


def test_blackswaptionengine_constant_vol(swaption_env):
    """Test BlackSwaptionEngine with constant vol."""
    env = swaption_env
    engine = ql.BlackSwaptionEngine(env["curve"], 0.20)
    assert engine is not None

    env["swaption"].setPricingEngine(engine)
    npv = env["swaption"].NPV()
    assert npv == pytest.approx(19361.82, rel=1e-4)


def test_blackswaptionengine_pricing(swaption_env):
    """Test BlackSwaptionEngine swaption pricing."""
    env = swaption_env
    engine = ql.BlackSwaptionEngine(env["curve"], 0.20)
    env["swaption"].setPricingEngine(engine)

    npv = env["swaption"].NPV()
    assert npv == pytest.approx(19361.82, abs=10.0)


def test_blackswaptionengine_quote_vol(swaption_env):
    """Test BlackSwaptionEngine with Quote vol."""
    env = swaption_env
    vol_quote = ql.SimpleQuote(0.20)
    engine = ql.BlackSwaptionEngine(env["curve"], vol_quote)
    env["swaption"].setPricingEngine(engine)

    npv1 = env["swaption"].NPV()
    vol_quote.setValue(0.30)
    npv2 = env["swaption"].NPV()
    assert npv2 > npv1


def test_blackswaptionengine_handle_constructor(swaption_env):
    """Test BlackSwaptionEngine with explicit YieldTermStructureHandle."""
    env = swaption_env
    engine = ql.BlackSwaptionEngine(
        ql.YieldTermStructureHandle(env["curve"]), 0.20,
    )
    env["swaption"].setPricingEngine(engine)
    assert env["swaption"].NPV() == pytest.approx(19361.8214, rel=1e-4)


def test_blackswaptionengine_displacement(swaption_env):
    """Test BlackSwaptionEngine with displacement (shifted lognormal)."""
    env = swaption_env
    engine = ql.BlackSwaptionEngine(env["curve"], 0.20, displacement=0.01)
    env["swaption"].setPricingEngine(engine)
    assert env["swaption"].NPV() == pytest.approx(22608.0820, rel=1e-4)


# --- BachelierSwaptionEngine ---


def test_bachelierswaptionengine_construction(swaption_env):
    """Test BachelierSwaptionEngine construction."""
    env = swaption_env
    engine = ql.BachelierSwaptionEngine(env["curve"], 0.005)
    env["swaption"].setPricingEngine(engine)
    assert env["swaption"].NPV() == pytest.approx(11130.8843, rel=1e-4)


def test_bachelierswaptionengine_pricing(swaption_env):
    """Test BachelierSwaptionEngine swaption pricing."""
    env = swaption_env
    engine = ql.BachelierSwaptionEngine(env["curve"], 0.005)
    env["swaption"].setPricingEngine(engine)

    npv = env["swaption"].NPV()
    assert npv == pytest.approx(11130.8843, rel=1e-4)


def test_bachelierswaptionengine_quote_vol(swaption_env):
    """Test BachelierSwaptionEngine with Quote vol."""
    env = swaption_env
    vol_quote = ql.SimpleQuote(0.005)
    engine = ql.BachelierSwaptionEngine(env["curve"], vol_quote)
    env["swaption"].setPricingEngine(engine)

    npv1 = env["swaption"].NPV()
    vol_quote.setValue(0.010)
    npv2 = env["swaption"].NPV()
    assert npv2 > npv1


def test_bachelierswaptionengine_handle_constructor(swaption_env):
    """Test BachelierSwaptionEngine with explicit YieldTermStructureHandle."""
    env = swaption_env
    engine = ql.BachelierSwaptionEngine(
        ql.YieldTermStructureHandle(env["curve"]), 0.005,
    )
    env["swaption"].setPricingEngine(engine)
    assert env["swaption"].NPV() == pytest.approx(11130.8843, rel=1e-4)


# =============================================================================
# Gaussian1dSwaptionEngine
# =============================================================================


@pytest.fixture(scope="module")
def g1d_swaption_env():
    """Environment for Gaussian1D swaption engine tests."""
    import datetime

    ql.Settings.evaluationDate = datetime.date(2024, 1, 15)
    rf = ql.FlatForward(datetime.date(2024, 1, 15), 0.05, ql.Actual365Fixed())
    ts_handle = ql.YieldTermStructureHandle(rf)
    gsr = ql.Gsr(ts_handle, [], [0.01], 0.1)
    index = ql.Euribor6M(ts_handle)
    swap = ql.MakeVanillaSwap(ql.Period("5Y"), index, 0.05, ql.Period("1Y"))
    exercise = ql.EuropeanExercise(ql.Date(17, ql.January, 2025))
    swaption = ql.Swaption(swap, exercise)

    return {
        "gsr": gsr,
        "ts_handle": ts_handle,
        "swap": swap,
        "swaption": swaption,
        "index": index,
    }


def test_gaussian1dswaptionengine(g1d_swaption_env):
    """Test Gaussian1dSwaptionEngine with GSR model."""
    env = g1d_swaption_env
    engine = ql.Gaussian1dSwaptionEngine(env["gsr"])
    env["swaption"].setPricingEngine(engine)
    assert env["swaption"].NPV() == pytest.approx(0.015898946807894027, rel=1e-4)


def test_gaussian1dswaptionengine_probabilities_enum():
    """Test Gaussian1dSwaptionEngine Probabilities enum."""
    assert int(ql.Gaussian1dSwaptionEngine.None_) == 0
    assert int(ql.Gaussian1dSwaptionEngine.Naive) == 1
    assert int(ql.Gaussian1dSwaptionEngine.Digital) == 2


def test_gaussian1dswaptionengine_bermudan(g1d_swaption_env):
    """Test Gaussian1dSwaptionEngine with Bermudan swaption."""
    env = g1d_swaption_env
    dates = [ql.Date(17, ql.January, d) for d in range(2025, 2029)]
    bermudan = ql.BermudanExercise(dates)
    bermudan_swaption = ql.Swaption(env["swap"], bermudan)
    engine = ql.Gaussian1dSwaptionEngine(env["gsr"])
    bermudan_swaption.setPricingEngine(engine)
    assert bermudan_swaption.NPV() == pytest.approx(0.021788033257121142, rel=1e-4)


# =============================================================================
# Gaussian1dJamshidianSwaptionEngine
# =============================================================================


def test_gaussian1djamshidianswaptionengine(g1d_swaption_env):
    """Test Gaussian1dJamshidianSwaptionEngine with GSR model."""
    env = g1d_swaption_env
    engine = ql.Gaussian1dJamshidianSwaptionEngine(env["gsr"])
    env["swaption"].setPricingEngine(engine)
    assert env["swaption"].NPV() == pytest.approx(0.01589467525904184, rel=1e-4)


# =============================================================================
# Gaussian1dNonstandardSwaptionEngine
# =============================================================================


@pytest.fixture(scope="module")
def g1d_nonstandard_env():
    """Environment for Gaussian1D nonstandard swaption engine tests."""
    import datetime

    ql.Settings.evaluationDate = datetime.date(2024, 1, 15)
    rf = ql.FlatForward(datetime.date(2024, 1, 15), 0.05, ql.Actual365Fixed())
    ts_handle = ql.YieldTermStructureHandle(rf)
    gsr = ql.Gsr(ts_handle, [], [0.01], 0.1)
    index = ql.Euribor6M(ts_handle)

    fixedSchedule = ql.Schedule(
        ql.Date(17, ql.January, 2025),
        ql.Date(17, ql.January, 2030),
        ql.Period("1Y"),
        ql.TARGET(),
        ql.ModifiedFollowing,
        ql.ModifiedFollowing,
        ql.DateGeneration.Forward,
        False,
    )
    floatingSchedule = ql.Schedule(
        ql.Date(17, ql.January, 2025),
        ql.Date(17, ql.January, 2030),
        ql.Period("6M"),
        ql.TARGET(),
        ql.ModifiedFollowing,
        ql.ModifiedFollowing,
        ql.DateGeneration.Forward,
        False,
    )
    nsSwap = ql.NonstandardSwap(
        ql.SwapType.Payer,
        [1.0] * 5,
        [1.0] * 10,
        fixedSchedule,
        [0.05] * 5,
        ql.Thirty360(ql.Thirty360.BondBasis),
        floatingSchedule,
        index,
        [1.0] * 10,
        [0.0] * 10,
        ql.Actual360(),
        False,
    )
    exercise = ql.EuropeanExercise(ql.Date(15, ql.January, 2025))
    nsSwaption = ql.NonstandardSwaption(nsSwap, exercise)

    return {"gsr": gsr, "nsSwaption": nsSwaption}


def test_gaussian1dnonstandardswaptionengine(g1d_nonstandard_env):
    """Test Gaussian1dNonstandardSwaptionEngine with GSR model."""
    env = g1d_nonstandard_env
    engine = ql.Gaussian1dNonstandardSwaptionEngine(env["gsr"])
    env["nsSwaption"].setPricingEngine(engine)
    assert env["nsSwaption"].NPV() == pytest.approx(0.015859955420623774, rel=1e-4)


def test_gaussian1dnonstandardswaptionengine_probabilities_enum():
    """Test Gaussian1dNonstandardSwaptionEngine Probabilities enum."""
    assert int(ql.Gaussian1dNonstandardSwaptionEngine.None_) == 0
    assert int(ql.Gaussian1dNonstandardSwaptionEngine.Naive) == 1
    assert int(ql.Gaussian1dNonstandardSwaptionEngine.Digital) == 2


# =============================================================================
# Gaussian1dFloatFloatSwaptionEngine
# =============================================================================


@pytest.fixture(scope="module")
def g1d_floatfloat_env():
    """Environment for Gaussian1D float-float swaption engine tests."""
    import datetime

    ql.Settings.evaluationDate = datetime.date(2024, 1, 15)
    rf = ql.FlatForward(datetime.date(2024, 1, 15), 0.05, ql.Actual365Fixed())
    ts_handle = ql.YieldTermStructureHandle(rf)
    gsr = ql.Gsr(ts_handle, [], [0.01], 0.1)

    schedule = ql.Schedule(
        ql.Date(17, ql.January, 2025),
        ql.Date(17, ql.January, 2030),
        ql.Period("6M"),
        ql.TARGET(),
        ql.ModifiedFollowing,
        ql.ModifiedFollowing,
        ql.DateGeneration.Forward,
        False,
    )
    euribor6m = ql.Euribor6M(ts_handle)
    euribor3m = ql.Euribor3M(ts_handle)

    ffs = ql.FloatFloatSwap(
        ql.SwapType.Payer,
        1.0,
        1.0,
        schedule,
        euribor6m,
        ql.Actual360(),
        schedule,
        euribor3m,
        ql.Actual360(),
        spread1=0.0,
        spread2=0.01,
    )
    exercise = ql.EuropeanExercise(ql.Date(15, ql.January, 2025))
    ffSwaption = ql.FloatFloatSwaption(ffs, exercise)

    return {"gsr": gsr, "ffSwaption": ffSwaption}


def test_gaussian1dfloatfloatswaptionengine(g1d_floatfloat_env):
    """Test Gaussian1dFloatFloatSwaptionEngine with GSR model."""
    env = g1d_floatfloat_env
    engine = ql.Gaussian1dFloatFloatSwaptionEngine(env["gsr"])
    env["ffSwaption"].setPricingEngine(engine)
    assert env["ffSwaption"].NPV() == pytest.approx(0.04059638281889203, rel=1e-4)


def test_gaussian1dfloatfloatswaptionengine_probabilities_enum():
    """Test Gaussian1dFloatFloatSwaptionEngine Probabilities enum."""
    assert int(ql.Gaussian1dFloatFloatSwaptionEngine.None_) == 0
    assert int(ql.Gaussian1dFloatFloatSwaptionEngine.Naive) == 1
    assert int(ql.Gaussian1dFloatFloatSwaptionEngine.Digital) == 2
