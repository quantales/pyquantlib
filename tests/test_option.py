import pytest
import pyquantlib as ql


def test_option_type_enum():
    assert ql.OptionType.Call == ql.Call
    assert ql.OptionType.Put == ql.Put
    assert ql.Call != ql.Put


def test_greeks_class():
    greeks = ql.Greeks()
    
    greeks.delta = 0.5
    greeks.gamma = 0.1
    greeks.theta = -0.02
    greeks.vega = 0.25
    greeks.rho = 0.03
    greeks.dividendRho = 0.01
    
    assert greeks.delta == 0.5
    assert greeks.gamma == 0.1
    assert greeks.theta == -0.02
    assert greeks.vega == 0.25
    assert greeks.rho == 0.03
    assert greeks.dividendRho == 0.01


def test_more_greeks_class():
    more_greeks = ql.MoreGreeks()
    
    more_greeks.itmCashProbability = 0.6
    more_greeks.strikeSensitivity = -0.5
    
    assert more_greeks.itmCashProbability == 0.6
    assert more_greeks.strikeSensitivity == -0.5


def test_option_abc_exists():
    assert hasattr(ql.base, 'Option')
