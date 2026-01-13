import pytest

import pyquantlib as ql


@pytest.fixture
def mc_env():
    """Market environment for MC engine tests."""
    today = ql.Date(20, 2, 2025)
    ql.Settings.instance().evaluationDate = today

    dc = ql.Actual365Fixed()
    cal = ql.TARGET()

    risk_free_ts = ql.FlatForward(today, 0.05, dc)
    dividend_ts = ql.FlatForward(today, 0.01, dc)
    vol_ts = ql.BlackConstantVol(today, cal, 0.20, dc)

    spot = ql.SimpleQuote(100.0)
    process = ql.BlackScholesMertonProcess(
        ql.QuoteHandle(spot),
        ql.YieldTermStructureHandle(dividend_ts),
        ql.YieldTermStructureHandle(risk_free_ts),
        ql.BlackVolTermStructureHandle(vol_ts),
    )

    payoff = ql.PlainVanillaPayoff(ql.OptionType.Call, 100.0)
    exercise_date = today + ql.Period(1, ql.Years)
    exercise = ql.EuropeanExercise(exercise_date)
    option = ql.VanillaOption(payoff, exercise)

    return {"option": option, "process": process}


def test_mc_engine_pseudorandom(mc_env):
    """Test MCEuropeanEngine with pseudorandom RNG."""
    engine = ql.MCEuropeanEngine(
        process=mc_env["process"],
        rngType="pseudorandom",
        timeSteps=10,
        requiredSamples=1000,
        seed=42,
    )

    assert engine is not None


def test_mc_engine_lowdiscrepancy(mc_env):
    """Test MCEuropeanEngine with low discrepancy RNG."""
    engine = ql.MCEuropeanEngine(
        process=mc_env["process"],
        rngType="lowdiscrepancy",
        timeSteps=10,
        requiredSamples=1000,
    )

    assert engine is not None


def test_mc_engine_pricing(mc_env):
    """Test MC engine produces reasonable prices."""
    option = mc_env["option"]

    engine = ql.MCEuropeanEngine(
        process=mc_env["process"],
        rngType="pseudorandom",
        timeSteps=52,
        requiredSamples=10000,
        seed=12345,
    )

    option.setPricingEngine(engine)
    npv = option.NPV()

    expected_npv = 9.687424197269415
    assert npv == pytest.approx(expected_npv, abs=1e-4)


def test_mc_engine_lowdiscrepancy_pricing(mc_env):
    """Test low discrepancy MC pricing."""
    option = mc_env["option"]

    engine = ql.MCEuropeanEngine(
        process=mc_env["process"],
        rngType="lowdiscrepancy",
        timeSteps=1,
        requiredSamples=10000,
        seed=12345,
    )

    option.setPricingEngine(engine)
    npv = option.NPV()

    expected_npv = 9.818793862668565
    assert npv == pytest.approx(expected_npv, abs=1e-4)


def test_mc_engine_antithetic(mc_env):
    """Test MC engine with antithetic variates."""
    option = mc_env["option"]

    engine = ql.MCEuropeanEngine(
        process=mc_env["process"],
        rngType="pseudorandom",
        timeSteps=10,
        antitheticVariate=True,
        requiredSamples=5000,
        maxSamples=100000,
        seed=8675309,
    )

    option.setPricingEngine(engine)
    npv = option.NPV()

    expected_npv = 9.8862132025707
    assert npv == pytest.approx(expected_npv, abs=1e-2)


def test_mc_engine_invalid_rng(mc_env):
    """Test error handling for invalid RNG type."""
    with pytest.raises(RuntimeError, match="Unsupported RNG type"):
        ql.MCEuropeanEngine(
            mc_env["process"], "invalid_rng", timeSteps=10, requiredSamples=1000
        )


def test_mc_engine_seed_reproducibility(mc_env):
    """Test same seed produces reproducible results."""
    engine1 = ql.MCEuropeanEngine(
        mc_env["process"], "pseudorandom", timeSteps=10, requiredSamples=1000, seed=42
    )
    engine2 = ql.MCEuropeanEngine(
        mc_env["process"], "pseudorandom", timeSteps=10, requiredSamples=1000, seed=42
    )

    payoff = ql.PlainVanillaPayoff(ql.OptionType.Call, 100.0)
    exercise = mc_env["option"].exercise()

    option1 = ql.VanillaOption(payoff, exercise)
    option2 = ql.VanillaOption(payoff, exercise)

    option1.setPricingEngine(engine1)
    option2.setPricingEngine(engine2)

    assert option1.NPV() == pytest.approx(option2.NPV(), abs=1e-10)
