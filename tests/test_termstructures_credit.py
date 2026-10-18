"""
Tests for credit term structure bindings.

Corresponds to src/termstructures/credit/*.cpp bindings.
"""

import math

import pytest

import pyquantlib as ql

# =============================================================================
# DefaultProbabilityTermStructure (ABC)
# =============================================================================


def test_defaultprobabilitytermstructure_abc_exists():
    """Test DefaultProbabilityTermStructure is in base submodule."""
    assert hasattr(ql.base, "DefaultProbabilityTermStructure")


def test_defaultprobabilitytermstructure_handle_exists():
    """Test handle types exist."""
    assert hasattr(ql, "DefaultProbabilityTermStructureHandle")
    assert hasattr(ql, "RelinkableDefaultProbabilityTermStructureHandle")


def test_defaultprobabilitytermstructure_handle_empty():
    """Test empty handle behavior."""
    handle = ql.DefaultProbabilityTermStructureHandle()
    assert handle.empty()


# =============================================================================
# FlatHazardRate
# =============================================================================


@pytest.fixture(scope="module")
def credit_env():
    """Common data for credit term structure tests."""
    original_date = ql.Settings.instance().evaluationDate
    today = ql.Date(15, ql.January, 2025)
    ql.Settings.instance().evaluationDate = today

    dc = ql.Actual365Fixed()
    discount_curve = ql.FlatForward(today, 0.02, dc)

    yield {
        "today": today,
        "dc": dc,
        "discount_curve": discount_curve,
    }

    ql.Settings.instance().evaluationDate = original_date


def test_flathazardrate_construction(credit_env):
    """Test FlatHazardRate construction with Date and Rate."""
    fhr = ql.FlatHazardRate(credit_env["today"], 0.01, credit_env["dc"])
    assert fhr is not None
    assert fhr.referenceDate() == credit_env["today"]


def test_flathazardrate_construction_quote(credit_env):
    """Test FlatHazardRate construction with Quote handle."""
    quote = ql.SimpleQuote(0.01)
    fhr = ql.FlatHazardRate(
        credit_env["today"], ql.QuoteHandle(quote), credit_env["dc"],
    )
    assert fhr is not None


def test_flathazardrate_construction_hidden_handle(credit_env):
    """Test FlatHazardRate construction with hidden handle."""
    quote = ql.SimpleQuote(0.01)
    fhr = ql.FlatHazardRate(credit_env["today"], quote, credit_env["dc"])
    assert fhr is not None


def test_flathazardrate_survival_probability(credit_env):
    """Test FlatHazardRate survival probability."""
    hazard_rate = 0.01
    fhr = ql.FlatHazardRate(credit_env["today"], hazard_rate, credit_env["dc"])

    one_year = credit_env["today"] + ql.Period(1, ql.Years)
    sp = fhr.survivalProbability(one_year)
    assert 0 < sp < 1
    # For flat hazard rate: S(t) = exp(-h*t) ~ exp(-0.01*1) ~ 0.99
    assert sp == pytest.approx(0.99005, abs=0.001)


def test_flathazardrate_default_probability(credit_env):
    """Test FlatHazardRate default probability."""
    hazard_rate = 0.01
    fhr = ql.FlatHazardRate(credit_env["today"], hazard_rate, credit_env["dc"])

    one_year = credit_env["today"] + ql.Period(1, ql.Years)
    dp = fhr.defaultProbability(one_year)
    sp = fhr.survivalProbability(one_year)
    assert dp == pytest.approx(1.0 - sp, abs=1e-10)


def test_flathazardrate_hazard_rate(credit_env):
    """Test FlatHazardRate hazard rate recovery."""
    hazard_rate = 0.02
    fhr = ql.FlatHazardRate(credit_env["today"], hazard_rate, credit_env["dc"])

    one_year = credit_env["today"] + ql.Period(1, ql.Years)
    hr = fhr.hazardRate(one_year)
    assert hr == pytest.approx(hazard_rate, abs=1e-10)


def test_flathazardrate_default_density(credit_env):
    """Test FlatHazardRate default density."""
    hazard_rate = 0.01
    fhr = ql.FlatHazardRate(credit_env["today"], hazard_rate, credit_env["dc"])

    one_year = credit_env["today"] + ql.Period(1, ql.Years)
    dd = fhr.defaultDensity(one_year)
    assert dd == pytest.approx(0.009900498337, rel=1e-6)


def test_flathazardrate_in_handle(credit_env):
    """Test FlatHazardRate works in a handle."""
    fhr = ql.FlatHazardRate(credit_env["today"], 0.01, credit_env["dc"])
    handle = ql.DefaultProbabilityTermStructureHandle(fhr)
    assert not handle.empty()


def test_flathazardrate_relinkable_handle(credit_env):
    """Test FlatHazardRate with relinkable handle."""
    fhr1 = ql.FlatHazardRate(credit_env["today"], 0.01, credit_env["dc"])
    fhr2 = ql.FlatHazardRate(credit_env["today"], 0.05, credit_env["dc"])

    handle = ql.RelinkableDefaultProbabilityTermStructureHandle(fhr1)
    one_year = credit_env["today"] + ql.Period(1, ql.Years)
    sp1 = handle.currentLink().survivalProbability(one_year)

    handle.linkTo(fhr2)
    sp2 = handle.currentLink().survivalProbability(one_year)

    assert sp1 > sp2  # Higher hazard rate -> lower survival


def test_flathazardrate_quote_update(credit_env):
    """Test FlatHazardRate updates when quote changes."""
    quote = ql.SimpleQuote(0.01)
    fhr = ql.FlatHazardRate(credit_env["today"], quote, credit_env["dc"])

    one_year = credit_env["today"] + ql.Period(1, ql.Years)
    sp1 = fhr.survivalProbability(one_year)

    quote.setValue(0.05)
    sp2 = fhr.survivalProbability(one_year)

    assert sp1 > sp2


# =============================================================================
# DefaultProbabilityHelper (ABC)
# =============================================================================


def test_defaultprobabilityhelper_abc_exists():
    """Test DefaultProbabilityHelper is in base submodule."""
    assert hasattr(ql.base, "DefaultProbabilityHelper")


# =============================================================================
# SpreadCdsHelper
# =============================================================================


def test_spreadcdshelper_construction(credit_env):
    """Test SpreadCdsHelper construction with Rate."""
    helper = ql.SpreadCdsHelper(
        0.01,  # 100 bps
        ql.Period(5, ql.Years),
        0,
        ql.TARGET(),
        ql.Quarterly,
        ql.Following,
        ql.DateGeneration.TwentiethIMM,
        ql.Actual360(),
        0.4,
        ql.YieldTermStructureHandle(credit_env["discount_curve"]),
    )
    assert helper is not None


def test_spreadcdshelper_construction_quote(credit_env):
    """Test SpreadCdsHelper construction with Quote handle."""
    quote = ql.SimpleQuote(0.01)
    helper = ql.SpreadCdsHelper(
        ql.QuoteHandle(quote),
        ql.Period(5, ql.Years),
        0,
        ql.TARGET(),
        ql.Quarterly,
        ql.Following,
        ql.DateGeneration.TwentiethIMM,
        ql.Actual360(),
        0.4,
        ql.YieldTermStructureHandle(credit_env["discount_curve"]),
    )
    assert helper is not None


def test_spreadcdshelper_maturity_date(credit_env):
    """Test SpreadCdsHelper maturity date."""
    helper = ql.SpreadCdsHelper(
        0.01,
        ql.Period(5, ql.Years),
        0,
        ql.TARGET(),
        ql.Quarterly,
        ql.Following,
        ql.DateGeneration.TwentiethIMM,
        ql.Actual360(),
        0.4,
        ql.YieldTermStructureHandle(credit_env["discount_curve"]),
    )
    assert helper.maturityDate() > credit_env["today"]
    assert helper.latestDate() >= helper.maturityDate()


# =============================================================================
# UpfrontCdsHelper
# =============================================================================


def test_upfrontcdshelper_construction(credit_env):
    """Test UpfrontCdsHelper construction with Rate."""
    helper = ql.UpfrontCdsHelper(
        0.02,   # 2% upfront
        0.005,  # 50 bps running
        ql.Period(5, ql.Years),
        0,
        ql.TARGET(),
        ql.Quarterly,
        ql.Following,
        ql.DateGeneration.TwentiethIMM,
        ql.Actual360(),
        0.4,
        ql.YieldTermStructureHandle(credit_env["discount_curve"]),
    )
    assert helper is not None


def test_upfrontcdshelper_construction_quote(credit_env):
    """Test UpfrontCdsHelper construction with Quote handle."""
    quote = ql.SimpleQuote(0.02)
    helper = ql.UpfrontCdsHelper(
        ql.QuoteHandle(quote),
        0.005,
        ql.Period(5, ql.Years),
        0,
        ql.TARGET(),
        ql.Quarterly,
        ql.Following,
        ql.DateGeneration.TwentiethIMM,
        ql.Actual360(),
        0.4,
        ql.YieldTermStructureHandle(credit_env["discount_curve"]),
    )
    assert helper is not None


def test_upfrontcdshelper_maturity_date(credit_env):
    """Test UpfrontCdsHelper maturity date."""
    helper = ql.UpfrontCdsHelper(
        0.02, 0.005, ql.Period(5, ql.Years), 0, ql.TARGET(),
        ql.Quarterly, ql.Following, ql.DateGeneration.TwentiethIMM,
        ql.Actual360(), 0.4,
        ql.YieldTermStructureHandle(credit_env["discount_curve"]),
    )
    assert helper.maturityDate() > credit_env["today"]
    assert helper.latestDate() >= helper.maturityDate()


# =============================================================================
# PiecewiseDefaultCurve
# =============================================================================


def test_piecewisedefaultcurve_log_linear_survival(credit_env):
    """Test PiecewiseLogLinearSurvival construction and use."""
    helpers = []
    for tenor_years, spread in [(1, 0.005), (3, 0.008), (5, 0.01), (7, 0.012)]:
        helpers.append(ql.SpreadCdsHelper(
            spread,
            ql.Period(tenor_years, ql.Years),
            0,
            ql.TARGET(),
            ql.Quarterly,
            ql.Following,
            ql.DateGeneration.TwentiethIMM,
            ql.Actual360(),
            0.4,
            ql.YieldTermStructureHandle(credit_env["discount_curve"]),
        ))

    curve = ql.PiecewiseLogLinearSurvival(
        credit_env["today"], helpers, credit_env["dc"],
    )
    assert curve is not None

    one_year = credit_env["today"] + ql.Period(1, ql.Years)
    sp = curve.survivalProbability(one_year)
    assert 0 < sp < 1

    five_years = credit_env["today"] + ql.Period(5, ql.Years)
    sp5 = curve.survivalProbability(five_years)
    assert sp5 < sp  # Longer tenor -> lower survival


def test_piecewisedefaultcurve_flat_hazard(credit_env):
    """Test PiecewiseFlatHazardRate is alias for PiecewiseBackwardFlatHazard."""
    assert ql.PiecewiseFlatHazardRate is ql.PiecewiseBackwardFlatHazard


def test_piecewisedefaultcurve_backward_flat_hazard(credit_env):
    """Test PiecewiseBackwardFlatHazard construction."""
    helpers = []
    for tenor_years, spread in [(1, 0.005), (5, 0.01)]:
        helpers.append(ql.SpreadCdsHelper(
            spread,
            ql.Period(tenor_years, ql.Years),
            0,
            ql.TARGET(),
            ql.Quarterly,
            ql.Following,
            ql.DateGeneration.TwentiethIMM,
            ql.Actual360(),
            0.4,
            ql.YieldTermStructureHandle(credit_env["discount_curve"]),
        ))

    curve = ql.PiecewiseBackwardFlatHazard(
        credit_env["today"], helpers, credit_env["dc"],
    )
    assert curve is not None
    one_year = credit_env["today"] + ql.Period(1, ql.Years)
    assert 0 < curve.survivalProbability(one_year) < 1


def test_piecewisedefaultcurve_nodes(credit_env):
    """Test PiecewiseDefaultCurve nodes accessor."""
    helpers = []
    for tenor_years, spread in [(1, 0.005), (3, 0.008), (5, 0.01)]:
        helpers.append(ql.SpreadCdsHelper(
            spread,
            ql.Period(tenor_years, ql.Years),
            0,
            ql.TARGET(),
            ql.Quarterly,
            ql.Following,
            ql.DateGeneration.TwentiethIMM,
            ql.Actual360(),
            0.4,
            ql.YieldTermStructureHandle(credit_env["discount_curve"]),
        ))

    curve = ql.PiecewiseLogLinearSurvival(
        credit_env["today"], helpers, credit_env["dc"],
    )
    nodes = curve.nodes()
    assert len(nodes) > 0
    # First node should be at reference date with value 1.0
    assert nodes[0][1] == pytest.approx(1.0)


# =============================================================================
# Interpolated curves: HazardRateCurve, DefaultDensityCurve, SurvivalProbabilityCurve
# =============================================================================


@pytest.fixture
def curve_dates(credit_env):
    """Reference date plus one and two years (365 days each on Actual/365)."""
    today = credit_env["today"]
    return [today, today + ql.Period(1, ql.Years), today + ql.Period(2, ql.Years)]


def test_hazardratecurve_backward_flat_survival(credit_env, curve_dates):
    """HazardRateCurve holds each node's rate over the segment ending at it."""
    rates = [0.01, 0.02, 0.03]
    curve = ql.HazardRateCurve(curve_dates, rates, credit_env["dc"])
    assert curve.referenceDate() == curve_dates[0]
    assert curve.maxDate() == curve_dates[2]
    assert curve.hazardRate(curve_dates[1]) == pytest.approx(0.02, rel=1e-12)
    assert curve.survivalProbability(curve_dates[1]) == pytest.approx(
        math.exp(-0.02), rel=1e-12)
    assert curve.survivalProbability(curve_dates[2]) == pytest.approx(
        math.exp(-0.05), rel=1e-12)


def test_hazardratecurve_extrapolates_last_rate(credit_env, curve_dates):
    """Beyond the last node the last hazard rate is held flat."""
    curve = ql.HazardRateCurve(curve_dates, [0.01, 0.02, 0.03], credit_env["dc"])
    three_years = credit_env["today"] + ql.Period(3, ql.Years)
    assert curve.survivalProbability(three_years, True) == pytest.approx(
        math.exp(-0.08), rel=1e-12)


def test_hazardratecurve_inspectors(credit_env, curve_dates):
    """HazardRateCurve exposes its nodes."""
    rates = [0.01, 0.02, 0.03]
    curve = ql.HazardRateCurve(curve_dates, rates, credit_env["dc"])
    assert curve.dates() == curve_dates
    assert curve.hazardRates() == rates
    assert curve.data() == rates
    assert curve.times() == pytest.approx([0.0, 1.0, 2.0], abs=1e-12)
    assert curve.nodes() == list(zip(curve_dates, rates))


def test_hazardratecurve_with_calendar_and_jump(credit_env, curve_dates):
    """A jump multiplies the survival probability after the jump date."""
    jump = ql.SimpleQuote(0.9)
    jump_date = curve_dates[0] + ql.Period(6, ql.Months)
    curve = ql.HazardRateCurve(curve_dates, [0.01, 0.02, 0.03], credit_env["dc"],
                               ql.TARGET(), [ql.QuoteHandle(jump)], [jump_date])
    assert curve.survivalProbability(curve_dates[1]) == pytest.approx(
        0.9 * math.exp(-0.02), rel=1e-12)
    before = curve_dates[0] + ql.Period(3, ql.Months)
    assert curve.survivalProbability(before) == pytest.approx(
        math.exp(-0.02 * credit_env["dc"].yearFraction(curve_dates[0], before)),
        rel=1e-12)


def test_hazardratecurve_is_default_probability_curve(credit_env, curve_dates):
    """HazardRateCurve can drive a default-probability handle."""
    curve = ql.HazardRateCurve(curve_dates, [0.01, 0.02, 0.03], credit_env["dc"])
    handle = ql.DefaultProbabilityTermStructureHandle(curve)
    assert handle.currentLink().survivalProbability(curve_dates[1]) == pytest.approx(
        math.exp(-0.02), rel=1e-12)


def test_defaultdensitycurve_linear_density(credit_env, curve_dates):
    """DefaultDensityCurve integrates a linear density into the default probability."""
    densities = [0.01, 0.03, 0.03]
    curve = ql.DefaultDensityCurve(curve_dates, densities, credit_env["dc"])
    # integral of a density rising linearly from 0.01 to 0.03 over one year
    assert curve.defaultProbability(curve_dates[1]) == pytest.approx(0.02, rel=1e-12)
    assert curve.survivalProbability(curve_dates[1]) == pytest.approx(0.98, rel=1e-12)
    assert curve.defaultDensity(curve_dates[1]) == pytest.approx(0.03, rel=1e-12)
    assert curve.hazardRate(curve_dates[1]) == pytest.approx(0.03 / 0.98, rel=1e-12)
    # constant 0.03 density over the second year
    assert curve.survivalProbability(curve_dates[2]) == pytest.approx(0.95, rel=1e-12)


def test_defaultdensitycurve_inspectors(credit_env, curve_dates):
    """DefaultDensityCurve exposes its nodes."""
    densities = [0.01, 0.03, 0.03]
    curve = ql.DefaultDensityCurve(curve_dates, densities, credit_env["dc"],
                                   ql.TARGET())
    assert curve.dates() == curve_dates
    assert curve.defaultDensities() == densities
    assert curve.nodes() == list(zip(curve_dates, densities))
    assert curve.maxDate() == curve_dates[2]


def test_survivalprobabilitycurve_log_linear(credit_env, curve_dates):
    """SurvivalProbabilityCurve interpolates the log of the survival probability."""
    probs = [1.0, 0.98, 0.95]
    curve = ql.SurvivalProbabilityCurve(curve_dates, probs, credit_env["dc"])
    assert curve.survivalProbability(curve_dates[1]) == pytest.approx(0.98, rel=1e-12)
    assert curve.survivalProbability(curve_dates[2]) == pytest.approx(0.95, rel=1e-12)
    # 73 days = 0.2 years on Actual/365, inside the first segment
    mid = curve_dates[0] + 73
    assert curve.survivalProbability(mid) == pytest.approx(0.98 ** 0.2, rel=1e-12)
    assert curve.hazardRate(mid) == pytest.approx(-math.log(0.98), rel=1e-9)


def test_survivalprobabilitycurve_inspectors(credit_env, curve_dates):
    """SurvivalProbabilityCurve exposes its nodes."""
    probs = [1.0, 0.98, 0.95]
    curve = ql.SurvivalProbabilityCurve(curve_dates, probs, credit_env["dc"],
                                        ql.TARGET())
    assert curve.dates() == curve_dates
    assert curve.survivalProbabilities() == probs
    assert curve.nodes() == list(zip(curve_dates, probs))
    assert curve.referenceDate() == curve_dates[0]


def test_interpolated_credit_curve_rejects_bad_input(credit_env, curve_dates):
    """Mismatched node counts are rejected by QuantLib."""
    with pytest.raises(ql.Error):
        ql.HazardRateCurve(curve_dates, [0.01, 0.02], credit_env["dc"])
    with pytest.raises(ql.Error):
        ql.SurvivalProbabilityCurve(curve_dates, [0.99, 0.98, 0.95], credit_env["dc"])
