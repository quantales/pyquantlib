import pyquantlib as ql
import pytest
import math


# --- Test Constructors ---
def test_period_constructors():
    # Default constructor (0 days)
    p_default = ql.Period()
    assert str(p_default) == "0D"

    # Constructor with length and TimeUnit
    p_3m = ql.Period(3, ql.Months)
    assert p_3m.length() == 3
    assert p_3m.units() == ql.Months

    p_2y = ql.Period(2, ql.Years)
    assert p_2y.length() == 2
    assert p_2y.units() == ql.Years

    p_7d = ql.Period(7, ql.Days)
    assert p_7d.length() == 7
    assert p_7d.units() == ql.Days

    p_4w = ql.Period(4, ql.Weeks)
    assert p_4w.length() == 4
    assert p_4w.units() == ql.Weeks

    # Constructor with Frequency
    p_annual = ql.Period(ql.Annual) # 1Y
    assert p_annual.length() == 1
    assert p_annual.units() == ql.Years
    assert p_annual.frequency() == ql.Annual

    p_semiannual = ql.Period(ql.Semiannual) # 6M
    assert p_semiannual.length() == 6
    assert p_semiannual.units() == ql.Months
    assert p_semiannual.frequency() == ql.Semiannual

    p_quarterly = ql.Period(ql.Quarterly) # 3M
    assert p_quarterly.length() == 3
    assert p_quarterly.units() == ql.Months
    assert p_quarterly.frequency() == ql.Quarterly
    
    p_monthly = ql.Period(ql.Monthly) # 1M
    assert p_monthly.length() == 1
    assert p_monthly.units() == ql.Months
    assert p_monthly.frequency() == ql.Monthly

    p_weekly = ql.Period(ql.Weekly) # 1W
    assert p_weekly.length() == 1
    assert p_weekly.units() == ql.Weeks
    assert p_weekly.frequency() == ql.Weekly
    
    p_daily = ql.Period(ql.Daily) # 1D
    assert p_daily.length() == 1
    assert p_daily.units() == ql.Days
    assert p_daily.frequency() == ql.Daily

    p_once = ql.Period(ql.Once) # 0Y
    assert p_once.length() == 0 
    assert p_once.units() == ql.Years
    assert p_once.frequency() == ql.Once
    
    p_nofreq = ql.Period(ql.NoFrequency) # 0D
    assert p_nofreq.length() == 0
    assert p_nofreq.units() == ql.Days
    assert p_nofreq.frequency() == ql.NoFrequency


# --- Test String Constructor ---
@pytest.mark.parametrize("period_str, length, unit", [
    ("1D", 1, ql.Days), ("1d", 1, ql.Days),
    ("1W", 1, ql.Weeks), ("1w", 1, ql.Weeks),
    ("1M", 1, ql.Months), ("1m", 1, ql.Months),
    ("1Y", 1, ql.Years), ("1y", 1, ql.Years),
    ("0D", 0, ql.Days), ("0M", 0, ql.Months),
    ("12M", 12, ql.Months),
    ("52W", 52, ql.Weeks),
    ("365D", 365, ql.Days),
    ("18M", 18, ql.Months),
    ("2Y6M", 30, ql.Months), # QuantLib::PeriodParser normalizes this
    ("1W2D", 9, ql.Days),   # QuantLib::PeriodParser normalizes this
])
def test_period_from_string_valid(period_str, length, unit):
    p = ql.Period(period_str)
    # After parsing complex strings, QuantLib normalizes them.
    # For example, "2Y6M" becomes "30M". "1W2D" becomes "9D".
    # So, we need to compare against the normalized form or check the components
    # if the parse function in the binding already uses QuantLib::PeriodParser::parse which normalizes.
    # The binding indeed uses PeriodParser::parse.
    
    # Let's compare the parsed period with an equivalent constructed period that is also normalized
    # This is tricky because the internal normalization logic can be complex.
    # A simpler check: compare string representations after QL's internal formatting
    # Or, check that p == Period(length, unit) after normalization of BOTH
    # For now, let's check if constructing Period(length, unit) and then parsing string are equivalent
    # if the string represents an already simple form.
    # For "2Y6M" -> 30M, length will be 30, unit will be Months
    # For "1W2D" -> 9D, length will be 9, unit will be Days
    
    # Let's create the expected period, then normalize both and compare
    # This is harder to test directly without knowing QL's exact normalization rules for ALL cases.
    # Let's test that the parsed period matches a known equivalent.
    # The parameters `length` and `unit` are for the *normalized* form from PeriodParser.
    expected_p = ql.Period(length, unit)
    assert p == expected_p # Relies on Period equality after normalization by parse.
    assert p.length() == length
    assert p.units() == unit


@pytest.mark.parametrize("invalid_str", [
    "1X", "ABC", "1", "M", "1M2", "1D1M", "Y1", ""
])
def test_period_from_string_invalid(invalid_str):
    with pytest.raises(ValueError, match="Invalid period string"):
        ql.Period(invalid_str)

# --- Test Member Functions ---
def test_period_members():
    p_6m = ql.Period(6, ql.Months)
    assert p_6m.length() == 6
    assert p_6m.units() == ql.Months
    assert p_6m.frequency() == ql.Semiannual

    p_1y = ql.Period(1, ql.Years)
    assert p_1y.length() == 1
    assert p_1y.units() == ql.Years
    assert p_1y.frequency() == ql.Annual
    
    # Test normalize and normalized
    p_12m = ql.Period(12, ql.Months)
    p_12m_normalized_copy = p_12m.normalized()
    
    assert p_12m_normalized_copy.length() == 1
    assert p_12m_normalized_copy.units() == ql.Years
    assert p_12m.length() == 12 # Original should be unchanged by .normalized()
    assert p_12m.units() == ql.Months

    p_12m.normalize() # In-place normalization
    assert p_12m.length() == 1
    assert p_12m.units() == ql.Years

    p_13m = ql.Period(13, ql.Months)
    p_13m.normalize()
    assert p_13m.length() == 13 # 13M doesn't normalize to 1Y1M by default in QL Period
    assert p_13m.units() == ql.Months # It stays as months unless it's an exact multiple of years/weeks.

    p_7d = ql.Period(7, ql.Days)
    p_7d_norm_copy = p_7d.normalized()
    assert p_7d_norm_copy.length() == 1
    assert p_7d_norm_copy.units() == ql.Weeks
    
    p_7d.normalize()
    assert p_7d.length() == 1
    assert p_7d.units() == ql.Weeks


# --- Test In-place Operators ---
def test_period_inplace_operators():
    # +=
    p1 = ql.Period(3, ql.Months)
    p2 = ql.Period(6, ql.Months)
    p1 += p2
    assert p1 == ql.Period(9, ql.Months)
    
    p3 = ql.Period(1, ql.Years)
    p1 += p3 # 9M + 1Y = 21M
    p1.normalize() # 21M
    assert p1 == ql.Period(21, ql.Months)

    # -=
    p4 = ql.Period(1, ql.Years) # 12M
    p5 = ql.Period(3, ql.Months)
    p4 -= p5 # 12M - 3M = 9M
    assert p4 == ql.Period(9, ql.Months)

    # *=
    p6 = ql.Period(2, ql.Weeks)
    p6 *= 3
    assert p6 == ql.Period(6, ql.Weeks)

    # /=
    p7 = ql.Period(10, ql.Months)
    p7 /= 2
    assert p7 == ql.Period(5, ql.Months)

    # Test division by zero for /=
    p8 = ql.Period(1, ql.Years)
    with pytest.raises(ql.Error):
        p8 /= 0
    
# --- Test Rich Comparisons ---
def test_period_comparisons():
    p6m = ql.Period(6, ql.Months)
    p1y = ql.Period(1, ql.Years)
    p12m = ql.Period(12, ql.Months)
    p18m = ql.Period(18, ql.Months)
    p2w = ql.Period(2, ql.Weeks) # approx 14 days
    p15d = ql.Period(15, ql.Days)

    assert p6m == ql.Period(6, ql.Months)
    assert p1y == p12m.normalized() # Comparing normalized forms
    assert p1y != p6m
    
    assert p6m < p1y
    assert p1y > p6m
    assert p6m <= p1y
    assert p6m <= ql.Period(6, ql.Months)
    assert p1y >= p6m
    assert p1y >= p12m.normalized()
    
    assert ql.Period("1Y") > ql.Period("11M")
    assert ql.Period("12M") == ql.Period("1Y").normalized() 
   
    assert ql.Period(12, ql.Months) == ql.Period(1, ql.Years)
    assert ql.Period(1, ql.Years) == ql.Period(1, ql.Years)

    # Test with Weeks and Days
    assert ql.Period(2, ql.Weeks) == ql.Period(14, ql.Days) # 2*7 == 14*1

# --- Test Arithmetic Operators ---
def test_period_arithmetic():
    p3m = ql.Period(3, ql.Months)
    p6m = ql.Period(6, ql.Months)

    # Negation
    neg_p3m = -p3m
    assert neg_p3m.length() == -3
    assert neg_p3m.units() == ql.Months

    # Addition
    p9m = p3m + p6m
    assert p9m == ql.Period(9, ql.Months)
    
    p1y = ql.Period(1, ql.Years)
    p1y3m = p1y + p3m # 1Y + 3M = 15M 
    assert p1y3m.units() == ql.Months
    assert p1y3m.length() == 15

    # Subtraction
    p_minus_3m = p6m - p3m
    assert p_minus_3m == ql.Period(3, ql.Months)

    # Multiplication by Integer
    p_mult = p3m * 4 # 3M * 4 = 12M
    assert p_mult.length() == 12
    assert p_mult.units() == ql.Months
    p_mult.normalize()
    assert p_mult == ql.Period(1, ql.Years)

    p_rmult = 2 * p6m # 2 * 6M = 12M
    assert p_rmult.length() == 12
    assert p_rmult.units() == ql.Months
    p_rmult.normalize()
    assert p_rmult == ql.Period(1, ql.Years)

    # Division by Integer
    p_div = ql.Period(2, ql.Years) / 2 # 2Y / 2 = 1Y
    assert p_div == ql.Period(1, ql.Years)

    p_div_months = ql.Period(18, ql.Months) / 3 # 18M / 3 = 6M
    assert p_div_months == ql.Period(6, ql.Months)
    
    # Test division by zero
    with pytest.raises(ql.Error):
        _ = ql.Period(1, ql.Years) / 0

# --- Test String Representations ---
def test_period_str_repr():
    p_5w = ql.Period(5, ql.Weeks)
    assert str(p_5w) == "5W"
    assert repr(p_5w).startswith("<Period: ")
    assert str(p_5w) in repr(p_5w) 
    assert repr(p_5w).endswith(">")

    p_10d = ql.Period("10d")
    assert str(p_10d) == "10D"
    assert repr(p_10d) == "<Period: 10D>"

    # The string output of Period usually simplifies (e.g., to largest units or normalized form)
    # Let's check a known normalization: "2Y6M" -> "30M"
    p_30m_from_str = ql.Period("2Y6M")
    assert str(p_30m_from_str) == "30M" 
    assert repr(p_30m_from_str) == "<Period: 30M>"

# --- Test Hash ---
def test_period_hash():
    p1 = ql.Period(1, ql.Years)
    p2 = ql.Period(12, ql.Months).normalized() # 1Y
    p3 = ql.Period(1, ql.Years)
    p4 = ql.Period(6, ql.Months)

    assert hash(p1) == hash(p2) # Hash relies on normalized form
    assert hash(p1) == hash(p3)
    assert hash(p1) != hash(p4) # Different periods

    # Test usability in sets/dictionary keys
    period_set = {p1, p2, p3, p4}
    assert len(period_set) == 2 # p1,p2,p3 are equivalent after normalization, p4 is different
    
    period_dict = {p1: "one_year", p4: "six_months"}
    assert period_dict[p2] == "one_year" # p2 is equivalent to p1

# --- Test Free Functions ---
def test_period_free_functions():
    p_1y = ql.Period(1, ql.Years)
    p_2m = ql.Period(2, ql.Months)
    p_3w = ql.Period(3, ql.Weeks)
    p_10d = ql.Period(10, ql.Days)
    p_18m = ql.Period(18, ql.Months) # 1.5 years

    # Test years()
    assert ql.years(p_1y) == 1
    assert ql.years(p_18m) == 1.5
    
    # Test months()
    assert ql.months(p_1y) == 12
    assert ql.months(p_2m) == 2
    assert ql.months(p_18m) == 18

    # Test weeks()
    assert ql.weeks(p_3w) == 3
    assert int(ql.weeks(p_10d)) == 1 # Integer part of 10/7
    
    # Test days()
    assert ql.days(p_3w) == 21
    assert ql.days(p_10d) == 10

    # Test zero period
    p_zero = ql.Period(0, ql.Days)
    assert ql.years(p_zero) == 0
    assert ql.months(p_zero) == 0
    assert ql.weeks(p_zero) == 0
    assert ql.days(p_zero) == 0

