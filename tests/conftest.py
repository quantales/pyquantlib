"""
Shared pytest fixtures for PyQuantLib tests.

These fixtures provide common market environments and objects used across
multiple test modules, eliminating duplication and ensuring consistency.
"""

import pytest

import pyquantlib as ql


# =============================================================================
# Basic Components
# =============================================================================


@pytest.fixture
def evaluation_date():
    """Standard evaluation date for tests. Restores original date after test."""
    original_date = ql.Settings.instance().evaluationDate
    today = ql.Date(15, ql.May, 2025)
    ql.Settings.instance().evaluationDate = today
    yield today
    ql.Settings.instance().evaluationDate = original_date


@pytest.fixture
def day_counter():
    """Standard day counter (Actual/365 Fixed)."""
    return ql.Actual365Fixed()


@pytest.fixture
def calendar():
    """Standard calendar (TARGET)."""
    return ql.TARGET()


# =============================================================================
# Term Structures
# =============================================================================


@pytest.fixture
def flat_rate_curve(evaluation_date, day_counter):
    """Flat 5% yield curve."""
    return ql.FlatForward(evaluation_date, 0.05, day_counter)


@pytest.fixture
def flat_dividend_curve(evaluation_date, day_counter):
    """Flat 0% dividend curve."""
    return ql.FlatForward(evaluation_date, 0.0, day_counter)


@pytest.fixture
def flat_vol_surface(evaluation_date, calendar, day_counter):
    """Flat 20% volatility surface."""
    return ql.BlackConstantVol(evaluation_date, calendar, 0.20, day_counter)


# =============================================================================
# Quotes
# =============================================================================


@pytest.fixture
def spot_quote():
    """Standard spot quote at 100."""
    return ql.SimpleQuote(100.0)


@pytest.fixture
def rate_quote():
    """Standard rate quote at 5%."""
    return ql.SimpleQuote(0.05)


@pytest.fixture
def vol_quote():
    """Standard volatility quote at 20%."""
    return ql.SimpleQuote(0.20)


# =============================================================================
# Processes
# =============================================================================


@pytest.fixture
def bsm_process(spot_quote, flat_dividend_curve, flat_rate_curve, flat_vol_surface):
    """Standard Black-Scholes-Merton process."""
    return ql.BlackScholesMertonProcess(
        ql.QuoteHandle(spot_quote),
        ql.YieldTermStructureHandle(flat_dividend_curve),
        ql.YieldTermStructureHandle(flat_rate_curve),
        ql.BlackVolTermStructureHandle(flat_vol_surface),
    )


@pytest.fixture
def gbs_process(spot_quote, flat_dividend_curve, flat_rate_curve, flat_vol_surface):
    """Generalized Black-Scholes process."""
    return ql.GeneralizedBlackScholesProcess(
        ql.QuoteHandle(spot_quote),
        ql.YieldTermStructureHandle(flat_dividend_curve),
        ql.YieldTermStructureHandle(flat_rate_curve),
        ql.BlackVolTermStructureHandle(flat_vol_surface),
    )


# =============================================================================
# Options
# =============================================================================


@pytest.fixture
def european_call_option(evaluation_date):
    """ATM European call option, 1Y maturity."""
    payoff = ql.PlainVanillaPayoff(ql.OptionType.Call, 100.0)
    maturity = evaluation_date + ql.Period(1, ql.Years)
    exercise = ql.EuropeanExercise(maturity)
    return ql.VanillaOption(payoff, exercise)


@pytest.fixture
def european_put_option(evaluation_date):
    """ATM European put option, 1Y maturity."""
    payoff = ql.PlainVanillaPayoff(ql.OptionType.Put, 100.0)
    maturity = evaluation_date + ql.Period(1, ql.Years)
    exercise = ql.EuropeanExercise(maturity)
    return ql.VanillaOption(payoff, exercise)


@pytest.fixture
def american_put_option(evaluation_date):
    """ATM American put option, 1Y maturity."""
    payoff = ql.PlainVanillaPayoff(ql.OptionType.Put, 100.0)
    maturity = evaluation_date + ql.Period(1, ql.Years)
    exercise = ql.AmericanExercise(evaluation_date, maturity)
    return ql.VanillaOption(payoff, exercise)


# =============================================================================
# Heston Model
# =============================================================================


@pytest.fixture
def heston_process(evaluation_date, day_counter):
    """Standard Heston process with typical parameters."""
    spot = ql.SimpleQuote(100.0)
    risk_free_ts = ql.FlatForward(evaluation_date, 0.05, day_counter)
    dividend_ts = ql.FlatForward(evaluation_date, 0.02, day_counter)

    v0 = 0.04      # Initial variance
    kappa = 2.0    # Mean reversion speed
    theta = 0.04   # Long-term variance
    sigma = 0.3    # Vol of vol
    rho = -0.7     # Correlation

    return ql.HestonProcess(
        ql.YieldTermStructureHandle(risk_free_ts),
        ql.YieldTermStructureHandle(dividend_ts),
        ql.QuoteHandle(spot),
        v0, kappa, theta, sigma, rho,
    )


@pytest.fixture
def heston_model(heston_process):
    """Standard Heston model."""
    return ql.HestonModel(heston_process)
