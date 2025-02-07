import pyquantlib as ql


def test_money_class_exists():
    """Tests that Money class is accessible."""
    assert hasattr(ql, 'Money')


def test_money_conversion_type_enum():
    """Tests Money.ConversionType enum."""
    assert hasattr(ql.Money, 'NoConversion')
    assert hasattr(ql.Money, 'BaseCurrencyConversion')
    assert hasattr(ql.Money, 'AutomatedConversion')


def test_money_settings_singleton():
    """Tests Money.Settings singleton is accessible."""
    settings = ql.Money.Settings.instance()
    assert settings is not None


def test_default_money():
    """Tests default-constructed Money."""
    m = ql.Money()
    assert m.value() == 0.0
    assert m.currency().empty()
