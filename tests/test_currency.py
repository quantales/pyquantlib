import pyquantlib as ql


def test_currency_class_exists():
    """Tests that Currency class is accessible."""
    assert hasattr(ql, 'Currency')


def test_empty_currency():
    """Tests default-constructed empty currency."""
    c = ql.Currency()
    assert c.empty()


def test_empty_currency_equality():
    """Tests equality of empty currencies."""
    c1 = ql.Currency()
    c2 = ql.Currency()
    assert c1 == c2
