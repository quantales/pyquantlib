import pyquantlib as ql


def test_exchangerate_class_exists():
    """Tests that ExchangeRate class is accessible."""
    assert hasattr(ql, 'ExchangeRate')


def test_exchangerate_type_enum():
    """Tests ExchangeRate.Type enum."""
    assert hasattr(ql.ExchangeRate, 'Direct')
    assert hasattr(ql.ExchangeRate, 'Derived')


def test_exchangerate_chain_method_exists():
    """Tests that chain static method is accessible."""
    assert hasattr(ql.ExchangeRate, 'chain')
