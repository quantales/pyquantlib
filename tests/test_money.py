import pytest
import sys
import pyquantlib as ql


@pytest.fixture
def setup_money_env():
    """
    Set up an environment for Money tests.
    Sets up exchange rates, and ensures the
    Money.Settings singleton is reset after each test.
    """
    # Setup Exchange Rates
    manager = ql.ExchangeRateManager.instance()
    manager.clear()
    eur = ql.EURCurrency()
    usd = ql.USDCurrency()
    manager.add(ql.ExchangeRate(eur, usd, 1.1))

    # Setup Money Settings
    money_settings = ql.Money.Settings.instance()
    original_conv_type = money_settings.conversionType
    original_base_ccy = money_settings.baseCurrency

    yield {"eur": eur, "usd": usd}

    # Teardown: Reset everything to default state
    manager.clear()
    money_settings.conversionType = original_conv_type
    money_settings.baseCurrency = original_base_ccy


def test_money_creation_and_accessors():
    """Tests basic creation and accessor methods."""
    eur = ql.EURCurrency()
    m = ql.Money(123.45, eur)

    assert m.value() == 123.45
    assert m.currency() == eur
    assert "123.45 EUR" in str(m)
    assert "<Money: 123.45 EUR>" in repr(m)

    # Default constructor
    m_empty = ql.Money()
    assert m_empty.value() == 0.0
    assert m_empty.currency().empty()


def test_money_conversion_type_enum():
    """Tests Money.ConversionType enum values."""
    assert hasattr(ql.Money, 'NoConversion')
    assert hasattr(ql.Money, 'BaseCurrencyConversion')
    assert hasattr(ql.Money, 'AutomatedConversion')


def test_money_settings_singleton():
    """Tests Money.Settings singleton is accessible."""
    settings = ql.Money.Settings.instance()
    assert settings is not None


def test_money_unary_operators():
    """Tests unary plus and minus operators."""
    eur = ql.EURCurrency()
    m = ql.Money(50.0, eur)

    # Unary plus
    m_plus = +m
    assert m_plus.value() == 50.0
    assert m_plus.currency() == eur
    assert id(m) != id(m_plus)

    # Unary minus
    m_minus = -m
    assert m_minus.value() == -50.0
    assert m_minus.currency() == eur


def test_money_inplace_arithmetic():
    """Tests in-place arithmetic operators (+=, -=, *=, /=)."""
    usd = ql.USDCurrency()
    m1 = ql.Money(100.0, usd)
    m2 = ql.Money(25.0, usd)

    m1 += m2
    assert m1.value() == 125.0

    m1 -= m2
    assert m1.value() == 100.0

    m1 *= 2.0
    assert m1.value() == 200.0

    m1 /= 4.0
    assert m1.value() == 50.0


def test_money_comparison_operators():
    """Tests comparison operators for same-currency Money objects."""
    gbp = ql.GBPCurrency()
    m100a = ql.Money(100.0, gbp)
    m100b = ql.Money(100.0, gbp)
    m200 = ql.Money(200.0, gbp)

    assert m100a == m100b
    assert m100a != m200
    assert m100a < m200
    assert m200 > m100a
    assert m100a <= m100b
    assert m100a >= m100b


def test_money_rounded_method():
    """Tests rounded() method using currency's rounding convention."""
    eur = ql.EURCurrency()
    m_unrounded = ql.Money(123.45678, eur)

    m_rounded = m_unrounded.rounded()

    assert m_rounded.value() == pytest.approx(123.46)
    assert m_rounded.currency() == eur
    assert id(m_unrounded) != id(m_rounded)


def test_module_level_close_functions(setup_money_env):
    """Tests close() and close_enough() with NoConversion setting."""
    eur = setup_money_env["eur"]
    usd = setup_money_env["usd"]

    ql.Money.Settings.instance().conversionType = ql.Money.NoConversion

    m1 = ql.Money(100.0, eur)
    m_same = ql.Money(100.0, eur)
    assert ql.close(m1, m_same)

    # Different currencies should raise error with NoConversion
    m_different_currency = ql.Money(100.0, usd)
    with pytest.raises(ql.Error, match="currency mismatch"):
        ql.close(m1, m_different_currency)


@pytest.mark.skipif(sys.platform == "darwin",
    reason="Settings.evaluationDate issue on macOS - requires QuantLib static build")
def test_cross_currency_close_with_conversion(setup_money_env):
    """Tests close() across currencies with AutomatedConversion enabled."""
    eur = setup_money_env["eur"]
    usd = setup_money_env["usd"]

    ql.Money.Settings.instance().conversionType = ql.Money.AutomatedConversion
    ql.Money.Settings.instance().baseCurrency = eur
    ql.Money.Settings.instance().baseCurrency = eur

    # 100.0 EUR = 110.0 USD (rate 1.1)
    m_eur = ql.Money(100.0, eur)
    m_usd = ql.Money(110.0, usd)

    assert ql.close(m_eur, m_usd)

    m_usd_different = ql.Money(110.1, usd)
    assert not ql.close(m_eur, m_usd_different)
