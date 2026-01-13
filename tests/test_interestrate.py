import math

import pytest

import pyquantlib as ql


@pytest.fixture(scope="module")
def setup_interest_rate_test():
    """Provides common objects for InterestRate tests."""
    day_counter = ql.Actual365Fixed()
    start_date = ql.Date(1, 2, 2025)
    end_date = ql.Date(1, 2, 2026)
    return {
        "rate": 0.05,
        "day_counter": day_counter,
        "compounding": ql.Compounded,
        "frequency": ql.Annual,
        "start_date": start_date,
        "end_date": end_date,
        "time": day_counter.yearFraction(start_date, end_date)
    }

def test_interestrate_constructors(setup_interest_rate_test):
    """Tests the constructors of the InterestRate class."""
    # Default constructor
    ir_default = ql.InterestRate()
    # A default-constructed InterestRate has a Null value
    print(ir_default)
    assert ir_default.isNull()

    # Full constructor
    r = setup_interest_rate_test["rate"]
    dc = setup_interest_rate_test["day_counter"]
    comp = setup_interest_rate_test["compounding"]
    freq = setup_interest_rate_test["frequency"]

    ir = ql.InterestRate(r, dc, comp, freq)

    assert ir.rate() == pytest.approx(r)

    assert ir.dayCounter() is not None
    assert ir.compounding() == comp
    assert ir.frequency() == freq

def test_interestrate_inspectors(setup_interest_rate_test):
    """Tests the inspector methods of InterestRate."""
    r = 0.025
    dc = ql.Thirty360(ql.Thirty360.USA)

    # Test with discrete compounding (frequency should be stored)
    ir_discrete = ql.InterestRate(r, dc, ql.Compounded, ql.Quarterly)
    assert ir_discrete.rate() == pytest.approx(r)
    assert ir_discrete.compounding() == ql.Compounded
    assert ir_discrete.frequency() == ql.Quarterly

    # Test with continuous compounding (frequency should be ignored and set to NoFrequency)
    ir_continuous = ql.InterestRate(r, dc, ql.Continuous, ql.Quarterly) # Pass Quarterly...
    assert ir_continuous.rate() == pytest.approx(r)
    assert ir_continuous.compounding() == ql.Continuous
    # ...but assert that the stored frequency is NoFrequency, as it's not applicable.
    assert ir_continuous.frequency() == ql.NoFrequency

    # Test dayCounter separately
    assert ir_discrete.dayCounter().name() == dc.name()
    assert ir_continuous.dayCounter().name() == dc.name()

def test_interestrate_factors(setup_interest_rate_test):
    """Tests discountFactor and compoundFactor methods."""
    r = setup_interest_rate_test["rate"]
    dc = setup_interest_rate_test["day_counter"]
    start = setup_interest_rate_test["start_date"]
    end = setup_interest_rate_test["end_date"]
    t = setup_interest_rate_test["time"]

    # Simple case: Continuous compounding
    ir_cont = ql.InterestRate(r, dc, ql.Continuous, ql.Annual)

    # Test with time `t`
    expected_compound_cont = math.exp(r * t)
    assert ir_cont.compoundFactor(t) == pytest.approx(expected_compound_cont)
    assert ir_cont.discountFactor(t) == pytest.approx(1.0 / expected_compound_cont)

    # Test with dates
    assert ir_cont.compoundFactor(start, end) == pytest.approx(expected_compound_cont)
    assert ir_cont.discountFactor(start, end) == pytest.approx(1.0 / expected_compound_cont)

    # Compounded case - tested via equivalentRate in other tests
    # ir_comp = ql.InterestRate(r, dc, ql.Compounded, ql.Annual)
    # expected_compound_comp = (1 + r / ql.Annual) ** (ql.Annual * t) # (1+r)^t for Annual
    # assert ir_comp.compoundFactor(t) == pytest.approx(expected_compound_comp)
    # assert ir_comp.discountFactor(t) == pytest.approx(1.0 / expected_compound_comp)

def test_interestrate_implied_and_equivalent_rate(setup_interest_rate_test):
    """Tests impliedRate (static) and equivalentRate methods."""
    r = setup_interest_rate_test["rate"]
    dc = setup_interest_rate_test["day_counter"]
    t = setup_interest_rate_test["time"]

    # Start with a known rate
    ir = ql.InterestRate(r, dc, ql.Compounded, ql.Annual)

    # Calculate compound factor
    compound_factor = ir.compoundFactor(t)

    # 1. Test impliedRate (static method)
    # What rate, under continuous compounding, gives the same compound factor?
    implied_ir = ql.InterestRate.impliedRate(
        compound_factor, dc, ql.Continuous, ql.Annual, t
    )

    # For Continuous: compound = e^(r_implied * t) => r_implied = ln(compound) / t
    expected_implied_rate = math.log(compound_factor) / t
    assert implied_ir.rate() == pytest.approx(expected_implied_rate)
    assert implied_ir.compounding() == ql.Continuous

    # 2. Test equivalentRate (instance method)
    # What is the equivalent continuous rate for our original compounded rate?
    equivalent_ir = ir.equivalentRate(ql.Continuous, ql.Annual, t)

    assert equivalent_ir.rate() == pytest.approx(expected_implied_rate)
    assert equivalent_ir.compounding() == ql.Continuous

    # Check that the two results are consistent
    assert implied_ir.rate() == pytest.approx(equivalent_ir.rate())

def test_interestrate_string_representation(setup_interest_rate_test):
    """Tests the __str__ and __repr__ for InterestRate, if bound."""
    ir = ql.InterestRate(
        0.03, ql.Actual360(), ql.Compounded, ql.Quarterly
    )

    # Using __str__ binding
    s = str(ir)
    # Example output from QL: "3.000000 % Actual/360 Quarterly compounding"
    assert "3.000000 %" in s
    assert "Actual/360" in s
    assert "Quarterly" in s

    # Using __repr__ binding
    # Example output from QL: "<InterestRate: 3.000000 % Actual/360 Quarterly compounding>"
    r = repr(ir)
    assert r.startswith("<InterestRate:")
    assert "%" in r
    assert r.endswith(">")


def test_interestrate_float_conversion():
    """Tests the __float__ method."""
    rate_value = 0.045
    ir = ql.InterestRate(rate_value, ql.Actual365Fixed(), ql.Continuous, ql.Annual)

    # Check if casting works
    assert float(ir) == pytest.approx(rate_value)

def test_interestrate_equality():
    """Tests the __eq__ and __ne__ methods."""
    ir1 = ql.InterestRate(0.05, ql.Actual365Fixed(), ql.Compounded, ql.Annual)
    ir2 = ql.InterestRate(0.05, ql.Actual365Fixed(), ql.Compounded, ql.Annual)
    ir3_diff_rate = ql.InterestRate(0.06, ql.Actual365Fixed(), ql.Compounded, ql.Annual)
    ir4_diff_dc = ql.InterestRate(0.05, ql.Actual360(), ql.Compounded, ql.Annual)
    ir5_diff_comp = ql.InterestRate(0.05, ql.Actual365Fixed(), ql.Continuous, ql.Annual)
    ir6_diff_freq = ql.InterestRate(0.05, ql.Actual365Fixed(), ql.Compounded, ql.Semiannual)

    # Test equality
    assert ir1 == ir2
    assert not (ir1 == ir3_diff_rate)
    assert not (ir1 == ir4_diff_dc)
    assert not (ir1 == ir5_diff_comp)
    assert not (ir1 == ir6_diff_freq)

    # Test inequality
    assert not (ir1 != ir2)
    assert ir1 != ir3_diff_rate
    assert ir1 != ir4_diff_dc
    assert ir1 != ir5_diff_comp
    assert ir1 != ir6_diff_freq

def test_interestrate_hashable():
    """Tests the __hash__ method for use in sets and dicts."""
    ir1 = ql.InterestRate(0.05, ql.Actual365Fixed(), ql.Compounded, ql.Annual)
    ir2 = ql.InterestRate(0.05, ql.Actual365Fixed(), ql.Compounded, ql.Annual)
    ir3 = ql.InterestRate(0.06, ql.Actual365Fixed(), ql.Compounded, ql.Annual)

    # Hashes of equal objects should be equal
    assert hash(ir1) == hash(ir2)
    # Hashes of different objects are not guaranteed to be different,
    # but for these simple changes, they almost certainly will be.
    assert hash(ir1) != hash(ir3)

    # Test usage in a set
    rate_set = {ir1, ir2, ir3}
    assert len(rate_set) == 2  # ir1 and ir2 should collapse into one entry
    assert ir1 in rate_set
    assert ir2 in rate_set
    assert ir3 in rate_set

    # Test usage in a dict
    rate_dict = {ir1: "first", ir3: "third"}
    assert rate_dict[ir1] == "first"
    # Check that ir2, which is equal to ir1, can be used as a key
    assert rate_dict[ir2] == "first"
